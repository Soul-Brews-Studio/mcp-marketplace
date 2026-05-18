---
description: Extract visual and audio content from video files using frame extraction + AI vision. Use when user says "video", "extract frames", "analyze video", or shares a video file to analyze.
---

**EXECUTE NOW:**

# /video — Video Frame Extraction + AI Vision

Extract and analyze video content using ffmpeg frame extraction + Claude's vision capability.

## Usage

```
/video [path]              # Extract frames + read content
/video [path] --audio      # Also transcribe audio (requires whisper)
/video [path] --frames N   # Custom FPS (default: 0.5 = 1 frame per 2 sec)
```

## Step 0: Parse Arguments

```
PATH = first argument (required)
FPS = 0.5 (default) or --frames value
AUDIO = false (default) or --audio flag
```

## Step 1: Extract Frames

```python
python3 -c "
import imageio_ffmpeg, subprocess, os, glob

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
video_path = '[VIDEO_PATH]'
out_dir = '/tmp/video_frames'

for f in glob.glob(f'{out_dir}/frame_*.jpg'):
    os.remove(f)
os.makedirs(out_dir, exist_ok=True)

info = subprocess.run([ffmpeg, '-i', video_path], capture_output=True, text=True)
for line in info.stderr.split('\n'):
    if 'Duration' in line:
        print(line.strip())

subprocess.run([ffmpeg, '-i', video_path,
    '-vf', 'fps=[FPS]', '-q:v', '2',
    f'{out_dir}/frame_%03d.jpg', '-y'],
    capture_output=True, text=True)

frames = sorted([f for f in os.listdir(out_dir) if f.endswith('.jpg')])
print(f'Extracted {len(frames)} frames')
"
```

## Step 2: Read All Frames

Read every frame using Claude's Read tool (vision reads images natively). **Read ALL frames in parallel.**

## Step 3: Synthesize

```markdown
## Video Analysis: [filename]
**Duration**: X seconds | **Frames**: N | **FPS**: X

### Visual Content
[What's shown across all frames]

### Text Extracted
[Any visible text — code, terminal output, slides]

### Summary
[1-2 paragraph synthesis]
```

## Step 4: Audio (if --audio)

```bash
whisper /tmp/video_frames/audio.wav --model small --output_format txt
```

## Dependencies

- `pip install imageio-ffmpeg` (bundled ffmpeg)
- `pip install openai-whisper` (optional, for audio)

---
ARGUMENTS: $ARGUMENTS
