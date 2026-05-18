---
name: video
description: |
  Extract visual and audio content from video files using frame extraction + AI vision.
  Use when user says "video", "extract frames", "analyze video", "what's in this video",
  or shares a video file path to analyze.
---

# /video — Extract Content from Video Files

Extract visual and audio content from video files using frame extraction + AI vision.

**Best for**: short videos (under 3 min) — screen recordings, reels, demos, tutorials.
**Not ideal for**: long audio-heavy content (>5 min). Transcription on CPU is too slow.

## Usage

```
/video [path]              # Extract frames + read content
/video [path] --audio      # Extract frames + transcribe audio (short videos only, requires whisper)
/video [path] --frames N   # Custom frames per second (default: 0.5 = 1 frame per 2 sec)
```

## How It Works

1. **Extract frames** using imageio-ffmpeg (bundled ffmpeg binary)
2. **Read frames** using Claude's vision capability
3. **Synthesize** all frame content into a coherent summary
4. Optionally **transcribe audio** with whisper

## Step 0: Parse Arguments

```
PATH = first argument (required)
FPS = 0.5 (default) or --frames value
AUDIO = false (default) or --audio flag
```

## Step 1: Extract Frames + Metadata

```python
python3 -c "
import imageio_ffmpeg, subprocess, os

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video_path = '[VIDEO_PATH]'
out_dir = '/tmp/video_frames'

# Clean previous frames
import glob
for f in glob.glob(f'{out_dir}/frame_*.jpg'):
    os.remove(f)

os.makedirs(out_dir, exist_ok=True)

# Get duration
info = subprocess.run([ffmpeg, '-i', video_path], capture_output=True, text=True)
for line in info.stderr.split('\n'):
    if 'Duration' in line:
        print(line.strip())

# Extract frames at FPS rate
subprocess.run([ffmpeg, '-i', video_path,
    '-vf', 'fps=[FPS]', '-q:v', '2',
    f'{out_dir}/frame_%03d.jpg', '-y'],
    capture_output=True, text=True)

# Extract audio if requested
if [AUDIO]:
    subprocess.run([ffmpeg, '-i', video_path,
        '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
        f'{out_dir}/audio.wav', '-y'],
        capture_output=True, text=True)

frames = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])
print(f'Extracted {len(frames)} frames')
for f in frames:
    sz = os.path.getsize(os.path.join(out_dir, f))
    print(f'  {f} ({sz//1024}KB)')
"
```

## Step 2: Read All Frames

Read every extracted frame using the Read tool (Claude vision reads images natively).

```
Read /tmp/video_frames/frame_001.jpg
Read /tmp/video_frames/frame_002.jpg
...
```

**Read ALL frames in parallel** — batch as many Read calls as possible in a single message.

## Step 3: Synthesize Content

After reading all frames, produce:

```markdown
## Video Analysis: [filename]

**Duration**: X seconds | **Frames**: N extracted | **FPS**: X

### Visual Content
[Describe what's shown across all frames — text on screen, UI elements, diagrams, people, etc.]

### Text Extracted
[Any text visible on screen — code, terminal output, chat messages, slides, etc.]

### Key Content
[The actual substance — what is being shown/taught/demonstrated]

### Summary
[1-2 paragraph synthesis of the entire video content]
```

## Step 4: Audio Transcription (if --audio)

If whisper is available:
```bash
whisper /tmp/video_frames/audio.wav --model small --output_format txt
```

If whisper is NOT available:
```bash
pip install openai-whisper
```

Add transcription to output:
```markdown
### Audio Transcription
[Transcribed speech]
```

## Dependencies

- **imageio-ffmpeg** (Python) — bundled ffmpeg binary, no system install needed
  - Install: `pip install imageio-ffmpeg`
- **whisper** (optional, for audio) — OpenAI Whisper
  - Install: `pip install openai-whisper`

## Notes

- Max practical video length: ~5 min at 0.5 FPS = 150 frames
- For longer videos: increase FPS interval (e.g., --frames 0.2 = 1 frame per 5 sec)
- Claude can read JPG/PNG frames natively — no OCR tool needed
- Frame extraction is fast (~2 sec for a 1-min video)
- Audio extraction produces 16kHz mono WAV (whisper-compatible)

---
ARGUMENTS: $ARGUMENTS
