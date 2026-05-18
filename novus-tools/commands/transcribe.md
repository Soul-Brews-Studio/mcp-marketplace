---
description: Multi-source transcription — YouTube, local video/audio, images. Use when user says "transcribe", "what does this say", "extract text from", or shares media to transcribe.
---

**EXECUTE NOW:**

# /transcribe — Multi-Source Transcription

Transcribe content from YouTube URLs, local video/audio files, and images.

## Usage

```
/transcribe https://youtube.com/watch?v=xxx     # YouTube captions
/transcribe /path/to/video.mp4                   # Local video
/transcribe /path/to/audio.mp3                   # Local audio
/transcribe /path/to/image.png                   # Image OCR via vision
```

## Step 1: Detect Input Type

| Input | Detection | Workflow |
|-------|-----------|----------|
| YouTube URL | Contains `youtube.com` or `youtu.be` | yt-dlp captions |
| Video file | Extension: .mp4, .mov, .webm, .avi | ffmpeg + whisper |
| Audio file | Extension: .mp3, .wav, .m4a, .ogg | whisper directly |
| Image file | Extension: .png, .jpg, .jpeg, .webp | Claude Read (vision) |

## Step 2A: YouTube

```bash
yt-dlp --write-auto-sub --sub-lang "en" --skip-download \
  --sub-format "vtt" -o "/tmp/yt_%(id)s" "<URL>"

# Clean captions
cat /tmp/yt_*.vtt | grep -v "^WEBVTT\|^$\|-->\|align\|position" \
  | sed 's/<[^>]*>//g' | sort -u
```

Then summarize with Claude.

## Step 2B: Local Video

```bash
ffmpeg -i <file> -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio.wav
whisper /tmp/audio.wav --model small --output_format txt
```

Or use `/video` skill for visual frame analysis.

## Step 2C: Local Audio

```bash
whisper <file> --model small --output_format txt
```

## Step 2D: Image

Use Claude's Read tool directly — Claude reads images natively via multimodal vision.

## Step 3: Output

```markdown
**Type:** YouTube / Video / Audio / Image
**Source:** <URL or filename>

**Content:**
<Main content summary>

**Key Points:**
- ...
- ...
```

## Dependencies

- `pip install yt-dlp` (YouTube)
- `pip install openai-whisper` (audio transcription)
- `pip install imageio-ffmpeg` (video audio extraction)

---
ARGUMENTS: $ARGUMENTS
