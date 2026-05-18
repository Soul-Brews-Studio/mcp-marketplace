---
name: genpic
description: |
  Generate images using Google Flow (labs.google/fx) with Playwright browser automation.
  Free AI image generation with Google account. Use when user says "genpic", "generate image",
  "create image", "draw", or wants AI-generated images.
---

# /genpic — Generate Images via Google Flow

Generate images using Google Flow (labs.google/fx) with Playwright browser automation and Nano Banana 2 model.

## Usage

```
/genpic "a cat floating in space with planets"
/genpic "prompt" --url https://labs.google/fx/tools/flow/project/{id}
/genpic "prompt" --output /tmp/my-image.jpg
```

## Prerequisites

- Playwright MCP server running and connected
- User logged into Google account in Playwright browser (one-time manual login)
- If not logged in: prompt user to open `https://labs.google/fx` and log in manually

## Workflow

### Step 1: Navigate to Google Flow

```
mcp__playwright__browser_navigate
url: {user-provided project URL} OR "https://labs.google/fx/tools/flow"
```

If user provides a project URL, use it. Otherwise navigate to base URL (auto-creates new project).

### Step 2: Detect Login State

```
mcp__playwright__browser_snapshot
```

Check snapshot for login indicators:
- If textbox "Email or phone" or "Password" visible — **STOP** — tell user to log in manually
- If prompt textbox visible — proceed

### Step 3: Prompt Translation

If user gives a non-English prompt — translate to English before typing. English prompts produce better, more consistent results.

Keep the original for display/logging.

### Step 4: Type the Prompt

```
mcp__playwright__browser_type
target: {textbox ref with prompt placeholder}
text: {English prompt}
```

**Important:** Identify the textbox by its placeholder text, not by hardcoded ref numbers. Refs change every page load.

### Step 5: Click Generate

```
mcp__playwright__browser_click
target: {button containing generate/create text}
element: "Generate button"
```

The model defaults to "Nano Banana 2" — no need to change it.

### Step 6: Wait for Generation (15-30 seconds)

```bash
sleep 20
```

Then take a snapshot to check progress:

```
mcp__playwright__browser_snapshot
```

Look for:
- Progress percentage — wait more
- Generated image buttons — generation complete
- If still generating after 20s, wait another 10s and re-check

### Step 7: Open Generated Image

Click the first generated image to open the editor view.

### Step 8: Extract Image URL

Take snapshot of editor to find the `img` element, then extract the source URL:

```
mcp__playwright__browser_evaluate
target: {img ref}
element: "Generated image"
function: "(el) => el.src"
```

### Step 9: Download Image

Download via browser fetch (bypasses auth — uses browser cookies):

```
mcp__playwright__browser_evaluate
function: |
  async () => {
    const res = await fetch('{IMAGE_URL}');
    const blob = await res.blob();
    const reader = new FileReader();
    return new Promise(resolve => {
      reader.onload = () => resolve(reader.result);
      reader.readAsDataURL(blob);
    });
  }
filename: "genpic-base64.txt"
element: "Download image via fetch"
```

Then decode base64 to file:

```bash
cat genpic-base64.txt | sed 's/^"data:image\/jpeg;base64,//' | sed 's/"$//' | base64 -d > {OUTPUT_PATH}
```

Default output path: `/tmp/genpic-{slugified-prompt}.jpg`

### Step 10: Report Result

```markdown
## Generated: {prompt}
**Model**: Nano Banana 2
**Project**: {project_url}
**Saved to**: {output_path}
```

Clean up temp files: `rm -f genpic-base64.txt`

## Error Handling

| Error | Action |
|-------|--------|
| Not logged in to Google | Tell user to open `https://labs.google/fx` and log in |
| Textbox not found | Wait 5s, re-snapshot. If still missing — screenshot for debug |
| Generation timeout >60s | Retry once with same prompt |
| Image URL extraction fails | Click download button as fallback |
| base64 decode fails | Use `browser_take_screenshot` of the image as fallback |

## Alternative Download (Fallback)

If fetch+base64 fails, use Playwright screenshot of the image element:

```
mcp__playwright__browser_take_screenshot
target: {img ref}
type: png
filename: "/tmp/genpic-output.png"
```

Lower quality than original but works as fallback.

## Tips

- English prompts produce better results than other languages
- Add style keywords: "cinematic lighting", "ultra high quality", "detailed", "vibrant colors"
- Multiple images generated (usually 2) — first one is used by default
- Project URLs are reusable — bookmark for iterating on a concept
- Google Flow is free with a Google account

## Prompt Enhancement

Before sending, enhance the user's prompt:
1. Add quality keywords if missing: "high quality, detailed"
2. Add lighting if missing: "cinematic lighting" or "natural lighting"
3. Add style if appropriate: "photorealistic" or "digital art" or "illustration"
4. Keep it under 200 words

---
ARGUMENTS: $ARGUMENTS
