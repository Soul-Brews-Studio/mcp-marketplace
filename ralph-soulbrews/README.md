# Ralph Local

> **Forked from**: [claude-plugins-official/ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) (Anthropic)
> **Enhancements**: Parse error fixes, absolute path support for worktree isolation, Oracle Forum integration
>
> 📢 **Upstream PR**: [#15853](https://github.com/anthropics/claude-code/pull/15853) - Session isolation fix contributed back to official plugin

Implementation of the Ralph Wiggum technique for iterative, self-referential AI development loops in Claude Code.

## 📦 Installation

### Step 1: Add the marketplace

```bash
/plugin marketplace add Soul-Brews-Studio/ralph-local
```

### Step 2: Install the plugin

```bash
/plugin install ralph-local@ralph-local
```

### Or: Clone locally

```bash
# Clone into your project
git clone https://github.com/Soul-Brews-Studio/ralph-local.git plugins/ralph-local

# Add as local marketplace
/plugin marketplace add ./plugins/ralph-local
/plugin install ralph-local@ralph-local
```

---

<details open>
<summary>🤖 <strong>AI Assistant Installation Prompt</strong></summary>

```
Install the ralph-local plugin for iterative AI development loops.

Steps:
1. Add marketplace: /plugin marketplace add Soul-Brews-Studio/ralph-local
2. Install plugin: /plugin install ralph-local@ralph-local
3. Verify: /ralph-loop --help
4. Confirm to user:
   - ✅ Ralph Local plugin installed
   - ✅ Commands: /ralph-loop, /cancel-ralph, /check-updates
   - ✅ Ready to use

Usage example:
/ralph-loop "Build a REST API with tests" --max-iterations 30 --completion-promise "COMPLETE"
```

</details>

---

## 🚀 Quick Start

```bash
# Start a Ralph loop
/ralph-loop "Build a REST API for todos. Requirements: CRUD operations, input validation, tests. Output <promise>COMPLETE</promise> when done." --completion-promise "COMPLETE" --max-iterations 50
```

Claude will:
- Implement the API iteratively
- Run tests and see failures
- Fix bugs based on test output
- Iterate until all requirements met
- Output the completion promise when done

---

## Why This Fork?

This is a local fork of the official `ralph-wiggum` plugin with significant engineering improvements.

### 🔧 What We Engineered (laris-co)

| Feature | Description | Files Changed |
|---------|-------------|---------------|
| **Extensive Error Handling** | Validates numeric fields, handles corrupt state files gracefully, detailed error messages | `hooks/stop-hook.sh` |
| **Worktree Isolation** | Uses `CLAUDE_PROJECT_DIR` for multi-agent worktree support (MAW) | `hooks/stop-hook.sh` |
| **Oracle Forum Integration** | EXIT_LOOP signal support for multi-agent coordination | Pattern documentation |
| **Write Tool Usage** | Uses Write tool instead of bash to preserve special characters | `commands/ralph-loop.md` |
| **Parse Error Fixes** | Fixed backtick pattern that broke eval in cancel command | `commands/cancel-ralph.md` |
| **`/check-updates` Command** | Track upstream changes and PR status | `commands/check-updates.md` |
| **AI Installation Prompt** | Ready-to-use prompt for AI assistants to install | `README.md` |
| **Comprehensive Documentation** | 500+ lines of docs with history, examples, troubleshooting | `README.md` |

### 🔄 Synced from Upstream (PR #15853)

| Feature | Description | Source |
|---------|-------------|--------|
| **Session Isolation** | Each session has own state file (`state/${SESSION_ID}.md`) | [PR #15853](https://github.com/anthropics/claude-code/pull/15853) |
| **SessionStart Hook** | Captures `session_id` and persists as `CLAUDE_SESSION_ID` | [PR #15853](https://github.com/anthropics/claude-code/pull/15853) |
| **Plugin-relative State** | State files in `${PLUGIN_ROOT}/state/` instead of `.claude/` | [PR #15853](https://github.com/anthropics/claude-code/pull/15853) |

### 📊 Engineering Stats

```
Total commits: 10
Lines added: 567+
Files modified: 8
New commands: 1 (/check-updates)
New hooks: 1 (SessionStart)
```

> 🎉 **Contributing Back**: We merged upstream session isolation from [PR #15853](https://github.com/anthropics/claude-code/pull/15853) while keeping our extensive error handling and multi-agent features.

**Credit**: Original concept by [Geoffrey Huntley](https://ghuntley.com/ralph/). Base implementation by Anthropic's Claude Code team. Enhanced by [laris-co](https://github.com/laris-co).

---

## What is Ralph?

Ralph is a development methodology based on continuous AI agent loops. As Geoffrey Huntley describes it: **"Ralph is a Bash loop"** - a simple `while true` that repeatedly feeds an AI agent a prompt file, allowing it to iteratively improve its work until completion.

The technique is named after Ralph Wiggum from The Simpsons, embodying the philosophy of persistent iteration despite setbacks.

### Core Concept

This plugin implements Ralph using a **Stop hook** that intercepts Claude's exit attempts:

```bash
# You run ONCE:
/ralph-loop "Your task description" --completion-promise "DONE"

# Then Claude Code automatically:
# 1. Works on the task
# 2. Tries to exit
# 3. Stop hook blocks exit
# 4. Stop hook feeds the SAME prompt back
# 5. Repeat until completion
```

The loop happens **inside your current session** - you don't need external bash loops. The Stop hook in `hooks/stop-hook.sh` creates the self-referential feedback loop by blocking normal session exit.

This creates a **self-referential feedback loop** where:
- The prompt never changes between iterations
- Claude's previous work persists in files
- Each iteration sees modified files and git history
- Claude autonomously improves by reading its own past work in files

---

## Commands

### /ralph-loop

Start a Ralph loop in your current session.

**Usage:**
```bash
/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"
```

**Options:**
- `--max-iterations <n>` - Stop after N iterations (default: unlimited)
- `--completion-promise <text>` - Phrase that signals completion

**Examples:**

```bash
# Basic usage with safety limit
/ralph-loop "Build a todo CLI app with tests" --max-iterations 30

# With completion promise
/ralph-loop "Implement feature X. Output DONE when complete." --completion-promise "DONE" --max-iterations 20

# Long-running task
/ralph-loop "Refactor codebase to use TypeScript. Output COMPLETE when all files converted and tests pass." --completion-promise "COMPLETE" --max-iterations 100
```

### /cancel-ralph

Cancel the active Ralph loop.

**Usage:**
```bash
/cancel-ralph
```

This will:
1. Show current iteration count if loop is active
2. Remove `.claude/ralph-loop.local.md` to stop the loop
3. Allow normal session exit

---

## Prompt Writing Best Practices

### 1. Clear Completion Criteria

❌ Bad: "Build a todo API and make it good."

✅ Good:
```markdown
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README with API docs
- Output: <promise>COMPLETE</promise>
```

### 2. Incremental Goals

❌ Bad: "Create a complete e-commerce platform."

✅ Good:
```markdown
Phase 1: User authentication (JWT, tests)
Phase 2: Product catalog (list/search, tests)
Phase 3: Shopping cart (add/remove, tests)

Output <promise>COMPLETE</promise> when all phases done.
```

### 3. Self-Correction

❌ Bad: "Write code for feature X."

✅ Good:
```markdown
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Refactor if needed
6. Repeat until all green
7. Output: <promise>COMPLETE</promise>
```

### 4. Escape Hatches

Always use `--max-iterations` as a safety net to prevent infinite loops on impossible tasks:

```bash
# Recommended: Always set a reasonable iteration limit
/ralph-loop "Try to implement feature X" --max-iterations 20

# In your prompt, include what to do if stuck:
# "After 15 iterations, if not complete:
#  - Document what's blocking progress
#  - List what was attempted
#  - Suggest alternative approaches"
```

**Note**: The `--completion-promise` uses exact string matching, so you cannot use it for multiple completion conditions (like "SUCCESS" vs "BLOCKED"). Always rely on `--max-iterations` as your primary safety mechanism.

---

## Philosophy

Ralph embodies several key principles:

### 1. Iteration > Perfection
Don't aim for perfect on first try. Let the loop refine the work.

### 2. Failures Are Data
"Deterministically bad" means failures are predictable and informative. Use them to tune prompts.

### 3. Operator Skill Matters
Success depends on writing good prompts, not just having a good model.

### 4. Persistence Wins
Keep trying until success. The loop handles retry logic automatically.

---

## When to Use Ralph

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement (e.g., getting tests to pass)
- Greenfield projects where you can walk away
- Tasks with automatic verification (tests, linters)
- Long-running development sessions (hours+)
- After planning sessions when context is established

**Not good for:**
- Tasks requiring human judgment or design decisions
- One-shot operations
- Tasks with unclear success criteria
- Production debugging (use targeted debugging instead)
- Cold starts without shared context

---

## Real-World Results

- Successfully generated 6 repositories overnight in Y Combinator hackathon testing
- One $50k contract completed for $297 in API costs
- Created entire programming language ("cursed") over 3 months using this approach
- **PhD thesis documentation**: 90+ consecutive iterations (iterations 84-115) capturing research progress
- **Speckit workflow mastery**: 5 iterations building 3 complete apps with 2x speed improvement each time
- **Oracle v2 infrastructure**: 66 minutes, 28 tasks, 4,479 documents indexed in one session

---

## Integration with Other Tools

Ralph Loop works exceptionally well when combined with other development patterns:

### Ralph + Speckit + Subagents

```
Speckit    → Creates structure (spec → plan → tasks)
Subagents  → Handle bulk work in parallel
Ralph Loop → Ensures completion (iterate until done)
```

**Example workflow:**
1. Use `/speckit.specify` to create feature spec
2. Use `/speckit.plan` to generate implementation plan
3. Use `/speckit.tasks` to break down into actionable tasks
4. Launch Ralph loop to execute: `/ralph-loop "Complete all tasks in tasks.md" --max-iterations 50`

### Multi-Agent Coordination (Advanced)

**Oracle Forum + Ralph Loop** enables multiple agents in simultaneous loops:

```bash
# Agent 1 starts Ralph loop
/ralph-loop "Build backend API. Check oracle_threads() for EXIT_LOOP signal." --max-iterations 50

# Agent 2 starts Ralph loop
/ralph-loop "Build frontend UI. Check oracle_threads() for EXIT_LOOP signal." --max-iterations 50

# Coordinator sends EXIT_LOOP via Oracle Forum Thread when both complete
```

**Why Forum > Search:**
- Status visible across all agents
- Full context history preserved
- Async communication without polling
- Natural completion detection

---

## Development History & Evolution

### Timeline

| Date | Event | Details |
|------|-------|---------|
| **2026-01-04** | Forum Integration | Multi-agent coordination via Oracle Forum proven |
| **2026-01-03** | `/gogogo-ralph` | Fast iteration command for shared context sessions |
| **2026-01-02** | Absolute Path Fix | Worktree isolation improvements for multi-agent work |
| **2026-01-01** | PhD Thesis Session | 90+ iterations (84-115) documenting thesis - MILESTONE |
| **2025-12-31** | Speckit Mastery | 5 iterations, 15 tasks, 3 apps with 2x speed improvement |
| **2025-12-30** | Plugin Fork | `ralph-local` created to fix parse errors from official plugin |
| **2025-12-29** | Initial Exploration | InfluxDB + Ralph Wiggum discovery, pattern documentation |

### Key Milestones

**Pattern Discovery (Dec 29, 2025)**
- First documentation of Ralph loop pattern for long-running tasks
- Core insight: "Self-referential cycle - same prompt feeds back automatically"
- Session result: 66 minutes, 28 tasks, 4,479 documents indexed

**Exit Condition Problem (Dec 30, 2025)**
- Discovered: No auto-stop mechanism leads to infinite loops
- Example: After 65/65 tasks complete, loop continued firing 100+ times
- Solution: Manual cancellation via `rm .claude/ralph-loop.local.md`
- Lesson: Focus tools need clear exit strategy

**Plugin Fork (Dec 30, 2025)**
- Forked from official `ralph-wiggum` to fix `````!` parse error in eval
- Changed to use Write tool instead of bash to preserve special characters
- Tested MAW (multi-agent worktree) delegation - all 5 agents verified
- Checkpoint system tested successfully

**Speckit Integration (Dec 31, 2025)**
- 9 iterations building 3 apps: session-timer, quick-note, focus-log
- Pattern emerged: 2x faster per app (muscle memory effect)
- Key insight: "Tools should feel like extensions of thinking, not interruptions"
- Proved: Ralph + Speckit = productive workflow

**Multi-Agent Breakthrough (Jan 4, 2026)**
- Pure MCP AI-to-AI coordination proven
- Two agents in simultaneous Ralph loops
- Communication via Oracle Forum Thread #11
- Exit pattern: `oracle_threads()` check for EXIT_LOOP signal
- Result: Forum-based exit conditions work reliably

### Major Sessions

**29 Retrospective Sessions** document Ralph usage across:
- Infrastructure work (Oracle v2, MCP integration)
- Plugin development and debugging
- Philosophy sessions (execution mode, 90/10 oracle)
- Multi-agent coordination testing

**19 Learning Documents** capture patterns:
- Core pattern documentation
- Exit condition strategies
- Multi-agent coordination
- Integration with Speckit and subagents

**11 Handoff Documents** preserve context:
- Session state transfers
- Plugin test results
- Multi-agent coordination proofs

---

## Knowledge Base

### Core Learning Documents

**Primary Patterns:**

1. **`ralph-loop-pattern-for-long-running-tasks`** (Dec 29, 2025)
   - What: Self-referential iteration cycle
   - When: Complex multi-phase implementations
   - Why: "Ralph Loop + Speckit + Subagents = Powerful combination"

2. **`ralph-loop-practice-complete-session-pattern`** (Dec 31, 2025)
   - 9 iterations building 3 apps
   - Pattern: 2x faster per app
   - Insight: Tools as thinking extensions

3. **`ralph-loop-needs-exit-condition`** (Dec 30, 2025)
   - Problem: No "done" detection
   - Fix: Manual cancellation required
   - Lesson: Clear exit strategy essential

4. **`ralph-loop-forum-integration-proven`** (Jan 4, 2026)
   - Multi-agent coordination via Oracle Forum
   - Exit pattern: Thread-based EXIT_LOOP signals
   - Why: Status visible, full context history

### File Structure

```
plugins/ralph-local/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   ├── ralph-loop.md        # Main command implementation
│   ├── cancel-ralph.md      # Cancellation command
│   └── help.md             # Usage guide
├── scripts/
│   └── setup-ralph-loop.sh  # Setup script
├── hooks/
│   ├── stop-hook.sh        # Exit interception logic
│   └── hooks.json          # Hook configuration
└── README.md               # This file
```

### State Files

**Active Loop State**: `.claude/ralph-loop.local.md`
- Tracks iteration count
- Stores loop context
- Removed to cancel loop

**Usage:**
```bash
# Check if loop is active
test -f .claude/ralph-loop.local.md && cat .claude/ralph-loop.local.md

# Cancel loop manually
rm .claude/ralph-loop.local.md
```

---

## Advanced Usage

### GoGoGo Mode

For sessions where context is already established:

```bash
/gogogo-ralph "MQTT backend working"
```

**Philosophy**: "We talked enough. Now build."

**Pattern:**
1. Plan in regular session (establish shared context)
2. Switch to GoGoGo mode (remove decision overhead)
3. Ralph executes until completion promise
4. Auto-handoff at 90% context
5. Auto-learning at 70%, blog draft at 85%

**When to use:**
- ✅ After planning session (context exists)
- ✅ After spec discussion (shared understanding)
- ✅ Greenfield projects (can walk away)
- ❌ Cold start (no context)
- ❌ Unclear requirements

### Multi-Agent Pattern

**Setup:**
1. Each agent has own worktree (via MAW - Multi-Agent Worktree)
2. Each agent runs independent Ralph loop
3. Coordination via Oracle Forum threads
4. EXIT_LOOP signal for completion

**Example:**

```bash
# Agent 1: Backend
cd agents/1
/ralph-loop "Build API backend. Check Thread #10 for EXIT_LOOP." --max-iterations 50

# Agent 2: Frontend
cd agents/2
/ralph-loop "Build React UI. Check Thread #10 for EXIT_LOOP." --max-iterations 50

# Coordinator: Monitor progress, send EXIT_LOOP when both complete
```

---

## Troubleshooting

### Loop Won't Stop

**Symptom**: Claude keeps iterating even after task completion

**Solutions:**
1. Use `/cancel-ralph` command
2. Manually remove: `rm .claude/ralph-loop.local.md`
3. Add `--max-iterations` safety limit
4. Use clear `--completion-promise` with exact match

### Parse Errors in Cancel Command

**Symptom**: `eval: ... syntax error near unexpected token`

**Solution**: This fork fixes the `````!` pattern error. Ensure you're using `ralph-local`, not the official `ralph-wiggum`.

### Hook Not Firing

**Symptom**: Loop exits normally instead of continuing

**Check:**
1. Plugin enabled in `.claude/settings.json`
2. Stop hook installed: `ls -la hooks/stop-hook.sh`
3. Hook permissions: `chmod +x hooks/stop-hook.sh`
4. Claude Code version supports stop hooks

### Worktree Isolation Issues

**Symptom**: Multi-agent loops interfering with each other

**Solution**: This fork uses absolute paths. Update to latest version:
```bash
cd plugins/ralph-local
git pull origin main
```

---

## Learn More

### Original Resources

- **Original technique**: https://ghuntley.com/ralph/
- **Ralph Orchestrator**: https://github.com/mikeyobrien/ralph-orchestrator
- **Official Plugin**: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum

### Related Patterns

- **Speckit**: Structured feature development (spec → plan → tasks)
- **Oracle MCP**: Knowledge base search and consultation
- **Claude Mem**: Persistent memory across sessions
- **MAW**: Multi-agent worktree coordination

### Community

- Share your Ralph loop success stories
- Report issues: https://github.com/Soul-Brews-Studio/ralph-local/issues
- Contribute improvements via PR

---

## For Help

Run `/help` in Claude Code for detailed command reference and examples.

---

## 🔍 AI Trace Instructions

> **For AI Assistants**: To trace the complete development history of this plugin:

```
/trace ralph-local in repo laris-co/Nat-s-Agents

Parent commit: c4920605
(contains all development history before graduation)
```

**What you'll find** (64+ files):
- 29 retrospective sessions documenting usage and evolution
- 19 learning documents capturing patterns
- 11 handoff documents preserving session context
- Full commit history from Dec 29, 2025 to Jan 6, 2026

**Quick clone for history access**:
```bash
git clone https://github.com/laris-co/Nat-s-Agents.git
git checkout c4920605
# Now you can trace: plugins/ralph-local/, ψ/memory/retrospectives/, ψ/memory/learnings/
```

**Key retrospectives**:
- `ψ/memory/retrospectives/2026-01/06/07.38_ralph-local-graduation.md` - Final graduation session
- `ψ/memory/retrospectives/2026-01/04/` - Multi-agent Oracle Forum integration
- `ψ/memory/retrospectives/2025-12/31/` - Speckit mastery sessions

---

## License

Same as original ralph-wiggum plugin.

**Credit**: Original concept by Geoffrey Huntley. Implementation by Anthropic's Claude Code team. Fork enhancements by Nat (laris-co).
