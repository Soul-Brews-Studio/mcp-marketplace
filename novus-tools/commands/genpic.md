---
description: Generate images using Google Flow (free) with Playwright browser automation. Use when user says "genpic", "generate image", "create image", "draw", or wants AI-generated images.
---

**EXECUTE NOW:**

# /genpic — Free AI Image Generation via Google Flow

Generate images using Google Flow (labs.google/fx) with Playwright browser automation.

## Usage

```
/genpic "a cat floating in space with planets"
/genpic "prompt" --url https://labs.google/fx/tools/flow/project/{id}
/genpic "prompt" --output /tmp/my-image.jpg
```

## Prerequisites

- Playwright MCP server running
- User logged into Google account in Playwright browser (one-time)

## Step 1: Navigate

```
browser_navigate → "https://labs.google/fx/tools/flow"
```

Or use `--url` for existing project.

## Step 2: Check Login

```
browser_snapshot
```

If login form visible — STOP, tell user to log in at `https://labs.google/fx`.

## Step 3: Enhance & Type Prompt

1. Translate non-English prompts to English (better results)
2. Add quality keywords if missing: "high quality, detailed, cinematic lighting"
3. Type into prompt textbox (find by placeholder text, not hardcoded ref)

## Step 4: Generate

Click generate button. Wait 15-30 seconds. Re-snapshot to check progress.

## Step 5: Download

1. Click first generated image
2. Extract image URL via `browser_evaluate("(el) => el.src")`
3. Download via browser fetch + base64 decode:

```bash
cat genpic-base64.txt | sed 's/^"data:image\/jpeg;base64,//' | sed 's/"$//' | base64 -d > /tmp/genpic-output.jpg
```

## Step 6: Report

```markdown
## Generated: {prompt}
**Model**: Nano Banana 2
**Saved to**: {output_path}
```

## Fallback

If fetch fails, use `browser_take_screenshot` of the image element.

## Tips

- English prompts > other languages for quality
- Google Flow is completely free with a Google account
- Project URLs are reusable for iteration

---
ARGUMENTS: $ARGUMENTS
