# plugin-marketplace - Architecture

## What It Does

This is a **Claude Code plugin marketplace** - a distribution point for plugins and skills that can be installed via Claude Code's `/plugin` command. It packages Oracle philosophy tools for the broader community.

The marketplace contains two plugins:
1. **oracle-skills** (v1.5.0): 13 essential Claude Code skills for workflow automation
2. **ralph-soulbrews** (v1.0.0): Self-referential AI development loops (fork of Anthropic's ralph-wiggum)

It serves developers who want practical Claude Code skills and learners who want to understand the Oracle philosophy - tools born from real usage over 8 months.

## How It Works

Claude Code's plugin system works via:
1. **marketplace.json** declares available plugins and their skill paths
2. Users add marketplace: `/plugin marketplace add Soul-Brews-Studio/plugin-marketplace`
3. Users install plugins: `/plugin install oracle-skills@soul-brews-plugin`
4. Claude Code reads skill files from declared paths
5. Skills become available as `/commands`

## Components

| Component | Purpose |
|-----------|---------|
| `.claude-plugin/marketplace.json` | Plugin registry - declares plugins and skill paths |
| `oracle-skills/` | 13 skills package |
| `oracle-skills/skills/*/SKILL.md` | Individual skill definitions |
| `oracle-skills/commands/*.md` | Command documentation |
| `oracle-skills/docs/` | Philosophy and journey documentation |
| `ralph-soulbrews/` | Ralph Loop plugin package |
| `ralph-soulbrews/commands/` | ralph-loop, cancel-ralph commands |
| `ralph-soulbrews/hooks/` | Stop hook for loop continuation |
| `README.md` | Marketplace documentation |
| `README.template.md` | Template for auto-generation |

The marketplace.json is the key - it maps plugin names to source directories and declares which skills each plugin provides. Claude Code's plugin system reads this to know what's available.

## Dependencies

| Package | Why |
|---------|-----|
| Claude Code | Required runtime - plugins only work inside Claude Code |
| ghq | Recommended for installation (clone management) |
| Git | For cloning and updates |

No runtime dependencies - pure markdown/bash skills.
