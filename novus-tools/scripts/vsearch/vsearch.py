#!/usr/bin/env python3
"""
vsearch — Hybrid BM25 + TF-IDF Vector search for local markdown vaults
v2.0: BM25 + TF-IDF with Reciprocal Rank Fusion (RRF)

Usage: python3 vsearch.py <query> [options]

Architecture:
  BM25 (lexical) ──┐
                    ├── RRF Fusion → final ranked results
  TF-IDF (semantic)─┘

RRF formula: score(d) = sum( 1/(k + rank_i(d)) )  where k=60 (default)

Configuration:
  Set VAULT_DIR below to point to your markdown knowledge base.
"""

import os
import re
import sys
import json
import math
import time
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Optional

# ── Try numpy (optional, graceful fallback to stdlib) ─────────────────────────
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ── BM25 parameters ──────────────────────────────────────────────────────────
K1 = 1.5   # term frequency saturation
B  = 0.75  # length normalization

# ── RRF parameters ───────────────────────────────────────────────────────────
RRF_K = 60  # constant in 1/(k + rank) — higher = more weight to lower ranks

# ── TF-IDF parameters ───────────────────────────────────────────────────────
MIN_DF = 1      # minimum document frequency to include term in vocabulary
MAX_DF_RATIO = 0.85  # max fraction of docs a term can appear in (stop-word filter)

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIGURATION — Set your vault path here
# ══════════════════════════════════════════════════════════════════════════════
# Point this to your markdown knowledge base directory.
# Examples:
#   VAULT_DIR = Path.home() / "notes"
#   VAULT_DIR = Path.home() / "obsidian-vault"
#   VAULT_DIR = Path("docs")
VAULT_DIR = Path(__file__).parent.parent.parent / "docs"

CACHE_DIR = Path(__file__).parent
CACHE_FILE = CACHE_DIR / ".index_cache.json"
VECTOR_CACHE_FILE = CACHE_DIR / ".vector_cache.npz"
VECTOR_META_FILE = CACHE_DIR / ".vector_meta.json"


# ── tokenizer (multilingual — supports Thai, CJK, Latin, numbers) ───────────
def tokenize(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r'[฀-๿一-鿿぀-ゟ゠-ヿa-z0-9]+', text)
    return [t for t in tokens if len(t) > 1]


# ── index builder ────────────────────────────────────────────────────────────
def build_index(vault: Path, subtree: str | None = None) -> dict:
    docs = {}

    search_root = vault / subtree if subtree else vault

    if not search_root.exists():
        return docs

    for md in sorted(search_root.rglob("*.md")):
        rel = str(md.relative_to(vault))
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        lines = text.splitlines()
        title = next((l.lstrip("#").strip() for l in lines if l.startswith("#")), rel)
        tokens = tokenize(text)

        docs[rel] = {
            "path": rel,
            "title": title[:80],
            "tokens": tokens,
            "text": text,
        }

    return docs


# ══════════════════════════════════════════════════════════════════════════════
#  BM25 Engine
# ══════════════════════════════════════════════════════════════════════════════

def compute_bm25(docs: dict, query_tokens: list[str]) -> list[tuple[str, float]]:
    if not docs:
        return []

    doc_lengths = {k: len(v["tokens"]) for k, v in docs.items()}
    avg_len = sum(doc_lengths.values()) / len(doc_lengths) if doc_lengths else 1
    N = len(docs)

    inv: dict[str, set] = defaultdict(set)
    for doc_id, doc in docs.items():
        for t in set(doc["tokens"]):
            inv[t].add(doc_id)

    tf: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for doc_id, doc in docs.items():
        for t in doc["tokens"]:
            tf[t][doc_id] += 1

    scores: dict[str, float] = defaultdict(float)

    for term in query_tokens:
        if term not in inv:
            continue
        df = len(inv[term])
        idf = math.log((N - df + 0.5) / (df + 0.5) + 1)

        for doc_id in inv[term]:
            freq = tf[term][doc_id]
            dl   = doc_lengths[doc_id]
            norm = freq * (K1 + 1) / (freq + K1 * (1 - B + B * dl / avg_len))
            scores[doc_id] += idf * norm

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TF-IDF Vector Engine
# ══════════════════════════════════════════════════════════════════════════════

class TFIDFVectorizer:
    """
    Lightweight TF-IDF vectorizer with cosine similarity search.
    numpy-accelerated when available, falls back to pure Python.
    """

    def __init__(self):
        self.vocab: list[str] = []
        self.vocab_idx: dict[str, int] = {}
        self.idf: list[float] = []
        self.doc_ids: list[str] = []
        self.doc_vectors = None
        self._fingerprint: str = ""

    def _compute_fingerprint(self, docs: dict) -> str:
        key = f"{len(docs)}:" + "|".join(sorted(docs.keys())[:20])
        return hashlib.md5(key.encode()).hexdigest()[:12]

    def fit(self, docs: dict):
        N = len(docs)
        if N == 0:
            return

        self._fingerprint = self._compute_fingerprint(docs)
        self.doc_ids = sorted(docs.keys())

        df: Counter = Counter()
        doc_tfs: dict[str, Counter] = {}

        for doc_id in self.doc_ids:
            tokens = docs[doc_id]["tokens"]
            tf_count = Counter(tokens)
            doc_tfs[doc_id] = tf_count
            for term in tf_count:
                df[term] += 1

        max_df = int(N * MAX_DF_RATIO)
        self.vocab = sorted([
            term for term, freq in df.items()
            if freq >= MIN_DF and freq <= max_df
        ])
        self.vocab_idx = {t: i for i, t in enumerate(self.vocab)}
        V = len(self.vocab)

        if V == 0:
            return

        self.idf = [math.log(N / df[t]) + 1.0 for t in self.vocab]

        if HAS_NUMPY:
            self._build_vectors_numpy(docs, doc_tfs, V)
        else:
            self._build_vectors_stdlib(docs, doc_tfs, V)

    def _build_vectors_numpy(self, docs, doc_tfs, V):
        N = len(self.doc_ids)
        idf_arr = np.array(self.idf, dtype=np.float32)
        matrix = np.zeros((N, V), dtype=np.float32)

        for i, doc_id in enumerate(self.doc_ids):
            tf_count = doc_tfs[doc_id]
            for term, count in tf_count.items():
                if term in self.vocab_idx:
                    j = self.vocab_idx[term]
                    matrix[i, j] = (1 + math.log(count)) * idf_arr[j]

        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        matrix /= norms

        self.doc_vectors = matrix

    def _build_vectors_stdlib(self, docs, doc_tfs, V):
        matrix = []
        for doc_id in self.doc_ids:
            vec = [0.0] * V
            tf_count = doc_tfs[doc_id]
            for term, count in tf_count.items():
                if term in self.vocab_idx:
                    j = self.vocab_idx[term]
                    vec[j] = (1 + math.log(count)) * self.idf[j]
            norm = math.sqrt(sum(x * x for x in vec))
            if norm > 0:
                vec = [x / norm for x in vec]
            matrix.append(vec)

        self.doc_vectors = matrix

    def query(self, query_tokens: list[str]) -> list[tuple[str, float]]:
        if not self.vocab or self.doc_vectors is None:
            return []

        V = len(self.vocab)
        qtf = Counter(query_tokens)

        if HAS_NUMPY:
            qvec = np.zeros(V, dtype=np.float32)
            for term, count in qtf.items():
                if term in self.vocab_idx:
                    j = self.vocab_idx[term]
                    qvec[j] = (1 + math.log(count)) * self.idf[j]
            norm = np.linalg.norm(qvec)
            if norm == 0:
                return []
            qvec /= norm

            similarities = self.doc_vectors @ qvec
            nonzero = np.nonzero(similarities > 0)[0]
            ranked_idx = nonzero[np.argsort(similarities[nonzero])[::-1]]

            return [(self.doc_ids[i], float(similarities[i])) for i in ranked_idx]
        else:
            qvec = [0.0] * V
            for term, count in qtf.items():
                if term in self.vocab_idx:
                    j = self.vocab_idx[term]
                    qvec[j] = (1 + math.log(count)) * self.idf[j]
            norm = math.sqrt(sum(x * x for x in qvec))
            if norm == 0:
                return []
            qvec = [x / norm for x in qvec]

            results = []
            for i, doc_id in enumerate(self.doc_ids):
                dvec = self.doc_vectors[i]
                sim = sum(a * b for a, b in zip(qvec, dvec))
                if sim > 0:
                    results.append((doc_id, sim))

            return sorted(results, key=lambda x: x[1], reverse=True)

    def save_cache(self):
        if self.doc_vectors is None or not self.vocab:
            return

        meta = {
            "fingerprint": self._fingerprint,
            "vocab_size": len(self.vocab),
            "doc_count": len(self.doc_ids),
            "vocab": self.vocab,
            "idf": self.idf,
            "doc_ids": self.doc_ids,
        }
        VECTOR_META_FILE.write_text(json.dumps(meta), encoding="utf-8")

        if HAS_NUMPY:
            np.savez_compressed(VECTOR_CACHE_FILE, vectors=self.doc_vectors)
        else:
            cache_path = VECTOR_CACHE_FILE.with_suffix(".json")
            cache_path.write_text(json.dumps(self.doc_vectors), encoding="utf-8")

    def load_cache(self, docs: dict) -> bool:
        if not VECTOR_META_FILE.exists():
            return False

        try:
            meta = json.loads(VECTOR_META_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return False

        expected_fp = self._compute_fingerprint(docs)
        if meta.get("fingerprint") != expected_fp:
            return False

        self.vocab = meta["vocab"]
        self.vocab_idx = {t: i for i, t in enumerate(self.vocab)}
        self.idf = meta["idf"]
        self.doc_ids = meta["doc_ids"]
        self._fingerprint = meta["fingerprint"]

        if HAS_NUMPY and VECTOR_CACHE_FILE.exists():
            data = np.load(VECTOR_CACHE_FILE)
            self.doc_vectors = data["vectors"]
            return True
        elif not HAS_NUMPY:
            cache_path = VECTOR_CACHE_FILE.with_suffix(".json")
            if cache_path.exists():
                self.doc_vectors = json.loads(cache_path.read_text(encoding="utf-8"))
                return True

        return False


# ══════════════════════════════════════════════════════════════════════════════
#  Reciprocal Rank Fusion (RRF)
# ══════════════════════════════════════════════════════════════════════════════

def reciprocal_rank_fusion(
    *rankings: list[tuple[str, float]],
    k: int = RRF_K,
) -> list[tuple[str, float]]:
    """
    Combine multiple ranked lists using RRF.
    Formula: score(d) = sum( 1/(k + rank_i(d)) )
    """
    fused: dict[str, float] = defaultdict(float)

    for ranking in rankings:
        for rank, (doc_id, _score) in enumerate(ranking, start=1):
            fused[doc_id] += 1.0 / (k + rank)

    return sorted(fused.items(), key=lambda x: x[1], reverse=True)


# ══════════════════════════════════════════════════════════════════════════════
#  Display helpers
# ══════════════════════════════════════════════════════════════════════════════

def snippet(text: str, query_tokens: list[str], window: int = 120) -> str:
    lower = text.lower()
    best_pos = len(text)
    for t in query_tokens:
        idx = lower.find(t)
        if idx != -1 and idx < best_pos:
            best_pos = idx

    if best_pos == len(text):
        return text[:window].replace("\n", " ").strip()

    start = max(0, best_pos - 40)
    end   = min(len(text), best_pos + window)
    raw   = text[start:end].replace("\n", " ").strip()
    return ("..." if start > 0 else "") + raw + ("..." if end < len(text) else "")


def c(code: str, text: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[{code}m{text}\033[0m"


def highlight(text: str, tokens: list[str]) -> str:
    for t in tokens:
        text = re.sub(re.escape(t), c("33;1", t), text, flags=re.IGNORECASE)
    return text


def mode_badge(mode: str) -> str:
    badges = {
        "hybrid": c("35;1", "HYBRID"),
        "bm25":   c("34;1", "BM25"),
        "vector": c("36;1", "VECTOR"),
    }
    return badges.get(mode, mode)


# ══════════════════════════════════════════════════════════════════════════════
#  Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="vsearch — Hybrid BM25 + Vector search for markdown vaults",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  (default)     Hybrid: BM25 + TF-IDF vector, fused with RRF
  --bm25        BM25 only (lexical keyword matching)
  --vector      TF-IDF vector only (cosine similarity)

Examples:
  vsearch "search query"
  vsearch --type docs "topic"
  vsearch --limit 10 "broad query"
  vsearch --bm25 "exact keywords"
  vsearch --vector "semantic search"
  vsearch --stats
  vsearch --rebuild-vectors
""",
    )
    parser.add_argument("query", nargs="*", help="Search terms")
    parser.add_argument("--type", "-t", help="Limit to subdirectory name")
    parser.add_argument("--limit", "-n", type=int, default=5, help="Max results (default 5)")
    parser.add_argument("--stats", action="store_true", help="Show vault stats")
    parser.add_argument("--snippet-len", type=int, default=120, help="Snippet length")
    parser.add_argument("--bm25", action="store_true", help="BM25 only (skip vector)")
    parser.add_argument("--vector", action="store_true", help="Vector only (skip BM25)")
    parser.add_argument("--rrf-k", type=int, default=RRF_K, help=f"RRF constant k (default {RRF_K})")
    parser.add_argument("--rebuild-vectors", action="store_true", help="Force rebuild vector index")
    parser.add_argument("--debug", action="store_true", help="Show per-engine rankings")
    parser.add_argument("--vault", help="Override vault directory path")

    args = parser.parse_args()

    vault = Path(args.vault) if args.vault else VAULT_DIR
    subtree = args.type if args.type else None
    scope_label = f"{vault}/{subtree}" if subtree else str(vault)

    if not vault.exists():
        print(f"Vault not found: {vault}", file=sys.stderr)
        print(f"Set VAULT_DIR in {__file__} or use --vault <path>", file=sys.stderr)
        sys.exit(1)

    # ── Stats mode ───────────────────────────────────────────────────────────
    if args.stats:
        t0 = time.time()
        docs = build_index(vault, subtree)
        elapsed = time.time() - t0
        total_tokens = sum(len(d["tokens"]) for d in docs.values())
        total_lines  = sum(len(d["text"].splitlines()) for d in docs.values())

        vec_status = "not built"
        if VECTOR_META_FILE.exists():
            try:
                meta = json.loads(VECTOR_META_FILE.read_text(encoding="utf-8"))
                vec_vocab = meta.get("vocab_size", 0)
                vec_docs = meta.get("doc_count", 0)
                vec_status = f"{vec_docs} docs, {vec_vocab} terms"
            except (json.JSONDecodeError, OSError):
                vec_status = "corrupt"

        print(f"\n{c('36;1', scope_label + ' stats')}")
        print(f"  files      : {c('1', str(len(docs)))}")
        print(f"  lines      : {c('1', str(total_lines))}")
        print(f"  tokens     : {c('1', str(total_tokens))}")
        print(f"  indexed    : {c('32', f'{elapsed:.2f}s')}")
        print(f"  vector idx : {c('35', vec_status)}")
        print(f"  numpy      : {c('32' if HAS_NUMPY else '31', 'yes' if HAS_NUMPY else 'no')}\n")
        return

    # ── Rebuild vectors mode ─────────────────────────────────────────────────
    if args.rebuild_vectors:
        print(f"{c('36;1', 'Rebuilding vector index...')}")
        t0 = time.time()
        docs = build_index(vault, subtree)

        vectorizer = TFIDFVectorizer()
        vectorizer.fit(docs)
        vectorizer.save_cache()
        elapsed = time.time() - t0
        print(f"  {len(docs)} docs, {len(vectorizer.vocab)} vocab terms")
        print(f"  Built in {c('32', f'{elapsed:.2f}s')}")
        print(f"  Saved to {VECTOR_META_FILE.name} + {VECTOR_CACHE_FILE.name}\n")
        return

    if not args.query:
        parser.print_help()
        sys.exit(0)

    query_str = " ".join(args.query)
    query_tokens = tokenize(query_str)

    if not query_tokens:
        print("No valid tokens in query.", file=sys.stderr)
        sys.exit(1)

    # ── Determine search mode ────────────────────────────────────────────────
    if args.bm25:
        search_mode = "bm25"
    elif args.vector:
        search_mode = "vector"
    else:
        search_mode = "hybrid"

    # ── Build index ──────────────────────────────────────────────────────────
    t0 = time.time()
    docs = build_index(vault, subtree)
    t_index = time.time() - t0

    # ── BM25 search ──────────────────────────────────────────────────────────
    bm25_ranked = []
    t_bm25 = 0
    if search_mode in ("bm25", "hybrid"):
        t1 = time.time()
        bm25_ranked = compute_bm25(docs, query_tokens)
        t_bm25 = time.time() - t1

    # ── Vector search ────────────────────────────────────────────────────────
    vec_ranked = []
    t_vec = 0
    if search_mode in ("vector", "hybrid"):
        t1 = time.time()
        vectorizer = TFIDFVectorizer()

        cache_hit = vectorizer.load_cache(docs)
        if not cache_hit:
            vectorizer.fit(docs)
            vectorizer.save_cache()

        vec_ranked = vectorizer.query(query_tokens)
        t_vec = time.time() - t1

    # ── Fuse results ─────────────────────────────────────────────────────────
    t1 = time.time()
    if search_mode == "hybrid":
        final_ranked = reciprocal_rank_fusion(bm25_ranked, vec_ranked, k=args.rrf_k)
    elif search_mode == "bm25":
        final_ranked = [(doc_id, score) for doc_id, score in bm25_ranked]
    else:
        final_ranked = [(doc_id, score) for doc_id, score in vec_ranked]
    t_fuse = time.time() - t1

    elapsed = time.time() - t0

    top = final_ranked[: args.limit]

    # ── Display ──────────────────────────────────────────────────────────────
    print(f"\n{c('36;1', 'vsearch')} {mode_badge(search_mode)} {c('2', f'[{scope_label}]')}  query: {c('33;1', query_str)}")

    timing_parts = [f"index {t_index:.2f}s"]
    if t_bm25 > 0:
        timing_parts.append(f"bm25 {t_bm25:.3f}s")
    if t_vec > 0:
        timing_parts.append(f"vector {t_vec:.3f}s")
    timing_str = " | ".join(timing_parts)

    print(c("2", f"  {len(docs)} docs — {timing_str} — top {len(top)}/{len(final_ranked)} hits\n"))

    if not top:
        print(c("31", "  No results found."))
        return

    bm25_rank_map = {doc_id: rank for rank, (doc_id, _) in enumerate(bm25_ranked, 1)}
    vec_rank_map = {doc_id: rank for rank, (doc_id, _) in enumerate(vec_ranked, 1)}

    for rank, (doc_id, score) in enumerate(top, 1):
        doc  = docs[doc_id]
        snip = snippet(doc["text"], query_tokens, args.snippet_len)
        snip = highlight(snip, query_tokens)

        print(f"  {c('32;1', str(rank))}. {c('1', doc['title'])}")

        score_str = f"score={score:.4f}"
        if args.debug and search_mode == "hybrid":
            bm25_r = bm25_rank_map.get(doc_id, "-")
            vec_r = vec_rank_map.get(doc_id, "-")
            score_str += f"  bm25=#{bm25_r} vec=#{vec_r}"

        print(f"     {c('2', doc['path'])}  {c('33', score_str)}")
        print(f"     {snip}")
        print()


if __name__ == "__main__":
    main()
