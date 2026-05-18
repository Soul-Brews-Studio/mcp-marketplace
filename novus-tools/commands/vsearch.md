---
description: Hybrid BM25 + TF-IDF vector search across local markdown files. Use when user says "vsearch", "search vault", "search notes", "find in docs", or needs ranked full-text search.
---

**EXECUTE NOW:**

# /vsearch — Hybrid BM25 + TF-IDF Local Search

Ranked search across a local markdown knowledge base.

## Usage

```bash
/vsearch "query terms"                    # Hybrid search (default)
/vsearch "query" --type <subfolder>       # Filter by subdirectory
/vsearch "query" --limit 10              # More results
/vsearch "query" --bm25                  # BM25 only (exact keywords)
/vsearch "query" --vector                # Vector only (semantic)
/vsearch --stats                         # Show index stats
/vsearch --rebuild-vectors               # Rebuild vector cache
```

## Step 0: Locate Script

```bash
PLUGIN_DIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
VSEARCH="$PLUGIN_DIR/scripts/vsearch/vsearch.sh"
```

Or find it relative to the plugin installation:
```bash
# Adjust VAULT path in scripts/vsearch/vsearch.py to point to your markdown directory
```

## Step 1: Run Search

```bash
bash scripts/vsearch/vsearch.sh "$ARGUMENTS"
```

## Step 2: Display Results

The script outputs ranked results with:
- Title and file path
- Relevance score
- Context snippet with highlighted query terms

## Configuration

Edit `scripts/vsearch/vsearch.py` line `VAULT_DIR = ...` to point to your markdown directory:

```python
VAULT_DIR = Path.home() / "notes"          # Obsidian vault
VAULT_DIR = Path("docs")                   # Project docs
VAULT_DIR = Path.home() / "knowledge"      # Any markdown folder
```

## Architecture

| Engine | Type | Strength |
|--------|------|----------|
| BM25 (k1=1.5, b=0.75) | Lexical | Exact keyword matching |
| TF-IDF (log-TF, L2-norm) | Semantic | Related concept matching |
| RRF (k=60) | Fusion | Best of both engines |

- numpy-accelerated when available, graceful fallback to stdlib
- Vector cache auto-persisted for fast subsequent searches
- Supports Thai, CJK, and Latin text tokenization

---
ARGUMENTS: $ARGUMENTS
