# Soul Brews Plugin Marketplace

Claude Code plugins and skills for Oracle philosophy.

> **Version**: {{MARKETPLACE_VERSION}} | **Updated**: {{DATE}} {{TIME}}

## Plugins

| Plugin | Version | Updated | Description |
|--------|---------|---------|-------------|
| oracle-skills | {{ORACLE_VERSION}} | {{DATE}} {{TIME}} | 13 Oracle skills |
| ralph-soulbrews | {{RALPH_VERSION}} | {{DATE}} {{TIME}} | Self-referential AI loops |

## Installation

Inside Claude Code:
```
# Add marketplace (once)
/plugin marketplace add Soul-Brews-Studio/plugin-marketplace

# Install plugins
/plugin install oracle-skills@soul-brews-plugin
/plugin install ralph-soulbrews@soul-brews-plugin
```

## Uninstall

```
# Remove plugins
/plugin uninstall oracle-skills@soul-brews-plugin
/plugin uninstall ralph-soulbrews@soul-brews-plugin

# Remove marketplace (optional)
/plugin marketplace remove soul-brews-plugin
```

## oracle-skills (v{{ORACLE_VERSION}})

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

## ralph-soulbrews (v{{RALPH_VERSION}})

Self-referential AI loops (fork of Anthropic's ralph-wiggum):

| Command | Purpose |
|---------|---------|
| `/ralph-loop` | Start iterative development loop |
| `/cancel-ralph` | Cancel active loop |
| `/check-updates` | Check for upstream updates |

## Philosophy

> "The Oracle Keeps the Human Human"

See [Oracle Philosophy](oracle-skills/docs/philosophy/ORACLE-PHILOSOPHY.md)

## Version History

| Date | Version | Changes |
|------|---------|---------|
| {{DATE}} | {{MARKETPLACE_VERSION}} | Current release |

## License

MIT
