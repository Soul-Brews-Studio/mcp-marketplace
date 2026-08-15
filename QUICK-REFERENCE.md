# plugin-marketplace - Quick Reference

## Install

```bash
# Inside Claude Code:
/plugin marketplace add Soul-Brews-Studio/plugin-marketplace
/plugin install oracle-skills@soul-brews-plugin
/plugin install ralph-soulbrews@soul-brews-plugin

# Or via ghq (for manual/global install):
ghq get -u Soul-Brews-Studio/plugin-marketplace
```

## Key Files

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Plugin registry |
| `oracle-skills/skills/*/SKILL.md` | Skill definitions |
| `oracle-skills/commands/*.md` | Command docs |
| `ralph-soulbrews/hooks/stop-hook.sh` | Loop continuation logic |
| `README.md` | Usage documentation |

## Entry Points

- Main: `.claude-plugin/marketplace.json` (plugin discovery)
- Config: Each plugin's own structure
- Skills: `oracle-skills/skills/[name]/SKILL.md`

## Available Skills (oracle-skills)

| Skill | Purpose |
|-------|---------|
| `/trace` | Find across git, repos, Oracle |
| `/rrr` | Session retrospective |
| `/recap` | Fresh start orientation |
| `/learn` | Clone repo for study |
| `/project` | Project lifecycle (learn/incubate) |
| `/feel` | Mood logging |
| `/fyi` | Info logging |
| `/forward` | Session handoff |
| `/standup` | Daily check |
| `/schedule` | Calendar queries |
| `/watch` | YouTube learning via Gemini |
| `/where-we-are` | Session awareness |
| `/context-finder` | Fast codebase search |

## Ralph Commands

| Command | Purpose |
|---------|---------|
| `/ralph-loop` | Start iterative loop |
| `/cancel-ralph` | Cancel active loop |
| `/check-updates` | Check upstream |

## Links

- Repo: https://github.com/Soul-Brews-Studio/plugin-marketplace
- Oracle Framework: https://github.com/Soul-Brews-Studio/oracle-framework
- Original Ralph: https://ghuntley.com/ralph/
