---
name: transcribe
description: |
  Multi-source transcription — YouTube URL, local video/audio, image files.
  Use when user says "transcribe", "what does this video say", "extract text from",
  or shares a video/audio/image and wants to know what's in it.
---

# /transcribe — Multi-Source Transcription

Transcribe content from multiple sources with the best workflow for each type.

## Input Types & Workflow

### 1. YouTube URL
```bash
# Pull auto-captions
yt-dlp --write-auto-sub --sub-lang "en" --skip-download \
  --sub-format "vtt" -o "/tmp/yt_%(id)s" "<URL>"

# Clean caption file
cat /tmp/yt_<ID>.en.vtt | grep -v "^WEBVTT\|^$\|-->\|align\|position" \
  | sed 's/<[^>]*>//g' | sort -u
```
Then summarize the content.

### 2. Local Video/Audio File
1. Use ffmpeg to extract audio: `ffmpeg -i <file> -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio.wav`
2. Transcribe with whisper: `whisper /tmp/audio.wav --model small --output_format txt`
3. Or use the `/video` skill for frame-by-frame visual analysis

### 3. Image File
1. Use the `Read` tool to read the image directly (Claude multimodal vision)
2. Extract and report all visible text, diagrams, or content

## Output Format
```
**Type:** YouTube / Video / Audio / Image
**Source:** <URL or filename>

**Content:**
<Main content summary>

**Key Points:**
- ...
- ...
```

## Dependencies

- **yt-dlp** — for YouTube caption extraction
  - Install: `pip install yt-dlp`
- **whisper** (optional) — for audio transcription
  - Install: `pip install openai-whisper`
- **ffmpeg** — for audio extraction from video
  - Install: `pip install imageio-ffmpeg` (bundled) or system package

## Notes
- YouTube captions may be noisy — summarize with Claude rather than copying raw
- For long videos (>5 min), prefer YouTube captions over whisper (faster)
- Images are read natively by Claude — no OCR tool needed
- Whisper supports many languages: `--language en`, `--language th`, etc.

---
ARGUMENTS: $ARGUMENTS
