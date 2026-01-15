# Soul Brews MCP Marketplace

MCP servers and skills for Oracle philosophy.

## Installation

```bash
# Add marketplace (once)
/plugin marketplace add Soul-Brews-Studio/mcp-marketplace

# Install plugins
/plugin install oracle-skills@soul-brews-studio-mcp
/plugin install ralph-local@soul-brews-studio-mcp
```

## Uninstall

```bash
# Remove plugins
/plugin uninstall oracle-skills@soul-brews-studio-mcp
/plugin uninstall ralph-local@soul-brews-studio-mcp

# Remove marketplace (optional)
/plugin marketplace remove soul-brews-studio-mcp
```

## Plugins

### oracle-skills

13 essential Claude Code skills:

| Skill | Purpose |
|-------|---------|
| `/trace` | Find projects across git history, repos, docs |
| `/rrr` | Create session retrospective |
| `/recap` | Fresh start context summary |
| `/feel` | Log emotions/feelings |
| `/fyi` | Log information for reference |
| `/forward` | Session handoff |
| `/learn` | Clone repo for study |
| `/project` | Project lifecycle management |
| `/standup` | Daily standup check |
| `/watch` | Learn from YouTube videos |
| `/where-we-are` | Session awareness |
| `/schedule` | Calendar/schedule queries |
| `/context-finder` | Fast search through codebase |

### ralph-local

Self-referential AI loops (fork of Anthropic's ralph-wiggum):

| Command | Purpose |
|---------|---------|
| `/ralph-loop` | Start iterative development loop |
| `/cancel-ralph` | Cancel active loop |
| `/check-updates` | Check for upstream updates |

## Philosophy

> "The Oracle Keeps the Human Human"

See [Oracle Philosophy](oracle-skills/docs/philosophy/ORACLE-PHILOSOPHY.md)

## License

MIT
