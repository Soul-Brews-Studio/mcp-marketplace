---
name: vsearch
description: |
  Hybrid BM25 + TF-IDF vector search across local markdown files.
  Use when user says "vsearch", "search vault", "search notes", "find in docs",
  or needs ranked full-text search across a markdown knowledge base.
---

# /vsearch — Hybrid BM25 + TF-IDF Local Search

Ranked search across a local markdown knowledge base using BM25 (lexical) + TF-IDF (semantic) with Reciprocal Rank Fusion.

## Usage

```bash
# Default: Hybrid (BM25 + TF-IDF vector, fused with RRF)
bash scripts/vsearch/vsearch.sh "query terms"

# Filter by subdirectory
bash scripts/vsearch/vsearch.sh "query" --type <subfolder-name>

# Limit results
bash scripts/vsearch/vsearch.sh "query" --limit 10

# BM25 only (exact keyword matching)
bash scripts/vsearch/vsearch.sh "query" --bm25

# Vector only (TF-IDF cosine similarity)
bash scripts/vsearch/vsearch.sh "query" --vector

# Debug: show per-engine rank positions
bash scripts/vsearch/vsearch.sh "query" --debug

# Show index stats
bash scripts/vsearch/vsearch.sh --stats

# Rebuild vector index
bash scripts/vsearch/vsearch.sh --rebuild-vectors
```

## Configuration

Edit the top of `scripts/vsearch/vsearch.py` to set your vault path:

```python
VAULT_DIR = Path("path/to/your/markdown/vault")
```

The script searches all `.md` files recursively under the vault directory.

## Architecture

- **BM25** (k1=1.5, b=0.75): lexical keyword matching
- **TF-IDF vectors** (log-normalized TF, L2-normalized): cosine similarity
- **RRF fusion** (k=60): `score(d) = 1/(k+rank_bm25) + 1/(k+rank_vec)`
- numpy-accelerated, graceful fallback to stdlib
- Vector cache auto-built and persisted for fast reload

## Dependencies

- Python 3.8+
- numpy (optional, for faster vector operations — falls back to stdlib)

---
ARGUMENTS: $ARGUMENTS
