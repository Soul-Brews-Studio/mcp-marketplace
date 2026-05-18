#!/bin/bash
# vsearch — Hybrid BM25 + TF-IDF vault search shortcut
# Usage: vsearch <query> [--type subfolder] [--limit N] [--bm25|--vector]
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
exec python3 "$SCRIPT_DIR/vsearch.py" "$@"
