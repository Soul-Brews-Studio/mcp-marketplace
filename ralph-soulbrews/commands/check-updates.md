# Check for Ralph Wiggum Updates

Check for new versions and updates from the official ralph-wiggum plugin.

## Instructions

1. **Check upstream repository for changes:**

```bash
# Fetch latest from official ralph-wiggum
gh api repos/anthropics/claude-code/contents/plugins/ralph-wiggum --jq '.[] | "\(.name) \(.sha | .[0:7])"' 2>/dev/null || echo "Check manually: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum"
```

2. **Check recent commits to ralph-wiggum:**

```bash
gh api repos/anthropics/claude-code/commits --jq '[.[] | select(.commit.message | test("ralph"; "i"))] | .[0:5] | .[] | "\(.sha | .[0:7]) \(.commit.message | split("\n")[0])"' 2>/dev/null
```

3. **Check open PRs related to ralph:**

```bash
gh pr list --repo anthropics/claude-code --search "ralph" --state all --limit 10 --json number,title,state,url --jq '.[] | "#\(.number) [\(.state)] \(.title)"'
```

4. **Check our fork's PR status:**

```bash
gh pr view 15853 --repo anthropics/claude-code --json state,title,mergedAt --jq '"PR #15853: \(.state) - \(.title)"'
```

5. **Compare local version with upstream:**

```bash
# Show local ralph-local version
echo "=== Local ralph-local ==="
git -C plugins/ralph-local log --oneline -3 2>/dev/null || echo "Not in ralph-local directory"

# Show what's different from upstream
echo ""
echo "=== Key differences from upstream ==="
echo "1. Session isolation (PR #15853)"
echo "2. Parse error fixes"
echo "3. Worktree isolation"
echo "4. Oracle Forum integration"
echo "5. Write tool usage"
```

## Report Format

After running checks, report to user:

```
📦 Ralph Updates Check

**Upstream Status:**
- Latest commits: [list recent ralph-related commits]
- Open PRs: [list any open PRs]

**Our PR #15853:**
- Status: [OPEN/MERGED/CLOSED]
- Session isolation fix

**Local Version:**
- Last commit: [hash] [message]
- Sync status: [UP TO DATE / NEEDS SYNC]

**Recommendations:**
- [Any actions needed]
```
