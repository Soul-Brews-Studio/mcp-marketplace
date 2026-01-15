---
description: "Cancel active Ralph Wiggum loop"
allowed-tools: ["Bash"]
---

# Cancel Ralph

Check if a Ralph loop is active and cancel it.

## Step 1: Check for active loop

Run this bash command:
```bash
test -f .claude/ralph-loop.local.md && grep '^iteration:' .claude/ralph-loop.local.md | head -1 || echo "NO_LOOP"
```

## Step 2: Based on output

- **If output is "NO_LOOP"**: Say "No active Ralph loop found."

- **If output shows "iteration: N"**:
  1. Run: `rm .claude/ralph-loop.local.md`
  2. Report: "Cancelled Ralph loop (was at iteration N)"
