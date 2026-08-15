# plugin-marketplace - Code Snippets

## Key Patterns

### 1. Plugin Marketplace JSON Structure

**What**: The `marketplace.json` declares plugins with their skills as path arrays.
**Why it's clever**: Single source of truth - Claude Code auto-discovers skills from these paths.

```json
{
  "name": "soul-brews-plugin",
  "version": "1.3.2",
  "plugins": [
    {
      "name": "oracle-skills",
      "source": "./oracle-skills",
      "skills": [
        "./skills/trace",
        "./skills/recap",
        "./skills/rrr"
      ]
    }
  ]
}
```

### 2. ghq-based Installation with Symlinks

**What**: Clone via ghq, then symlink skills to ~/.claude/skills/.
**Why it's clever**: One source of truth (ghq), global availability (symlinks), easy updates.

```bash
ghq get -u Soul-Brews-Studio/oracle-proof-of-concept-skills && \
for s in $(ghq root)/github.com/Soul-Brews-Studio/oracle-proof-of-concept-skills/skills/*/; do \
  mkdir -p ~/.claude/skills && ln -sf "$s" ~/.claude/skills/; \
done
```

### 3. Ralph Loop Stop Hook Pattern

**What**: Hook intercepts exit, feeds same prompt back, creates self-referential loop.
**Why it's clever**: No external bash loop needed - loop happens inside current session.

```bash
# User runs ONCE:
/ralph-loop "Your task" --completion-promise "DONE"

# Then Claude Code automatically:
# 1. Works on task
# 2. Tries to exit
# 3. Stop hook blocks exit
# 4. Stop hook feeds SAME prompt back
# 5. Repeat until completion promise found
```

The hook in `hooks/stop-hook.sh` creates the self-referential feedback where:
- Prompt never changes between iterations
- Claude's previous work persists in files
- Each iteration sees modified files and git history
