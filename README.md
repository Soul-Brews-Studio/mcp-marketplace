# Soul Brews Plugin Marketplace

Claude Code plugins and skills for Oracle philosophy.

> **Version**: 1.3.2 | **Updated**: 2026-01-16 02:11 UTC

## Plugins

| Plugin | Version | Updated | Description |
|--------|---------|---------|-------------|
| oracle-skills | 1.5.0 | 2026-01-16 02:11 UTC | 13 Oracle skills |
| ralph-soulbrews | 1.0.0 | 2026-01-16 02:11 UTC | Self-referential AI loops |
| novus-tools | 1.0.0 | 2026-05-18 | 5 productivity skills from Novus Fleet |

## Installation

Inside Claude Code:
```
# Add marketplace (once)
/plugin marketplace add Soul-Brews-Studio/plugin-marketplace

# Install plugins
/plugin install oracle-skills@soul-brews-plugin
/plugin install ralph-soulbrews@soul-brews-plugin
/plugin install novus-tools@soul-brews-plugin
```

## Uninstall

```
# Remove plugins
/plugin uninstall oracle-skills@soul-brews-plugin
/plugin uninstall ralph-soulbrews@soul-brews-plugin
/plugin uninstall novus-tools@soul-brews-plugin

# Remove marketplace (optional)
/plugin marketplace remove soul-brews-plugin
```

## oracle-skills (v1.5.0)

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

## ralph-soulbrews (v1.0.0)

Self-referential AI loops (fork of Anthropic's ralph-wiggum):

| Command | Purpose |
|---------|---------|
| `/ralph-loop` | Start iterative development loop |
| `/cancel-ralph` | Cancel active loop |
| `/check-updates` | Check for upstream updates |

## novus-tools (v1.0.0)

5 productivity skills from the Novus Fleet:

| Skill | Purpose |
|-------|---------|
| `/pordee` | Token-compressed communication (60-75% savings) |
| `/video` | Video frame extraction + AI vision analysis |
| `/vsearch` | Hybrid BM25 + TF-IDF local markdown search |
| `/genpic` | Free AI image generation via Google Flow |
| `/transcribe` | Multi-source transcription (YouTube, video, audio, image) |

## Philosophy

> "The Oracle Keeps the Human Human"

See [Oracle Philosophy](oracle-skills/docs/philosophy/ORACLE-PHILOSOPHY.md)

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-16 | 1.3.2 | Current release |

## License

MIT
