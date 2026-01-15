# Soul Brews Plugin Marketplace

Claude Code plugins and skills for Oracle philosophy.

> **Version**: {{MARKETPLACE_VERSION}} | **Updated**: {{DATE}} {{TIME}}

## Plugins

| Plugin | Version | Updated | Description |
|--------|---------|---------|-------------|
| oracle-skills | {{ORACLE_VERSION}} | {{DATE}} | 13 Oracle skills |
| ralph-soulbrews | {{RALPH_VERSION}} | {{DATE}} | Self-referential AI loops |

## Installation

```bash
# Add marketplace (once)
claude plugin marketplace add Soul-Brews-Studio/plugin-marketplace

# Install plugins
claude plugin install oracle-skills@soul-brews-plugin
claude plugin install ralph-soulbrews@soul-brews-plugin
```

## Uninstall

```bash
# Remove plugins
claude plugin uninstall oracle-skills@soul-brews-plugin
claude plugin uninstall ralph-soulbrews@soul-brews-plugin

# Remove marketplace (optional)
claude plugin marketplace remove soul-brews-plugin
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
