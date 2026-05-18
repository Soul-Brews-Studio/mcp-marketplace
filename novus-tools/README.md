# novus-tools

> 5 practical Claude Code skills from the Novus Fleet

**By Novus Fleet (Nexus_Of_Novus)** | **Version**: 1.0.0

## Skills

| Skill | Purpose | Category |
|-------|---------|----------|
| `/pordee` | Token-compressed communication (60-75% savings) | Efficiency |
| `/video` | Video frame extraction + AI vision analysis | Media |
| `/vsearch` | Hybrid BM25 + TF-IDF local markdown search | Search |
| `/genpic` | Free AI image generation via Google Flow | Media |
| `/transcribe` | Multi-source transcription (YouTube, video, audio, image) | Media |

## Installation

Inside Claude Code:
```
# Add marketplace (once)
/plugin marketplace add Soul-Brews-Studio/plugin-marketplace

# Install plugin
/plugin install novus-tools@soul-brews-plugin
```

## Uninstall

```
/plugin uninstall novus-tools@soul-brews-plugin
```

## Skill Details

### /pordee — Token Compression

Activate ultra-compressed communication mode. Drops filler, hedging, and pleasantries while keeping code and technical terms exact. Supports two levels: `lite` (grammar intact) and `full` (fragments OK).

```
/pordee              # Activate full compression
/pordee lite         # Lite mode
/pordee stop         # Deactivate
```

### /video — Video Frame Extraction

Extract frames from video files using ffmpeg, then analyze with Claude's vision. Optional audio transcription with Whisper.

```
/video /path/to/video.mp4
/video /path/to/video.mp4 --audio
/video /path/to/video.mp4 --frames 1
```

**Dependencies**: `pip install imageio-ffmpeg` (required), `pip install openai-whisper` (optional)

### /vsearch — Hybrid Vault Search

BM25 + TF-IDF vector search with Reciprocal Rank Fusion across any markdown directory. Includes a standalone Python script with numpy acceleration and graceful stdlib fallback.

```
/vsearch "search query"
/vsearch "query" --bm25          # Keyword only
/vsearch "query" --vector        # Semantic only
/vsearch --stats                 # Index stats
```

**Configuration**: Edit `VAULT_DIR` in `scripts/vsearch/vsearch.py` to point to your markdown directory.

### /genpic — Free AI Image Generation

Generate images using Google Flow (labs.google/fx) via Playwright browser automation. Completely free with a Google account.

```
/genpic "a sunset over mountains, cinematic lighting"
/genpic "prompt" --output /tmp/my-image.jpg
```

**Prerequisites**: Playwright MCP server, Google account logged in.

### /transcribe — Multi-Source Transcription

Transcribe from YouTube URLs (via yt-dlp captions), local video/audio (via Whisper), or images (via Claude vision).

```
/transcribe https://youtube.com/watch?v=xxx
/transcribe /path/to/video.mp4
/transcribe /path/to/image.png
```

**Dependencies**: `pip install yt-dlp` (YouTube), `pip install openai-whisper` (audio), `pip install imageio-ffmpeg` (video)

## Philosophy

These skills were born from daily use across the Novus Fleet — a multi-Oracle AI agent system. Each skill survived the test of real-world usage: if it wasn't used every week, it didn't make the cut.

> "Tools should be practical, not theoretical."

## License

MIT
