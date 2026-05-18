---
description: Ultra-compressed Thai+English communication mode. Cuts ~60-75% of tokens by speaking concisely while preserving technical accuracy. Use when user says "pordee", "speak short", "compress tokens", or wants shorter responses.
---

**EXECUTE NOW:**

# /pordee — Token-Compressed Communication Mode

Activate ultra-compressed communication. Cuts 60-75% of tokens by removing filler, hedging, and pleasantries while preserving technical accuracy.

## Usage

```
/pordee              # Activate full compression
/pordee lite         # Lite mode (grammar intact, drop filler)
/pordee stop         # Deactivate
```

## Behavior

When activated:

1. **Drop** all filler words, hedging, pleasantries, and redundant particles
2. **Swap** verbose phrases for terse equivalents (e.g., "in order to" -> "to")
3. **Use** fragments when clear. Pattern: `[thing] [action] [reason]. [next step].`
4. **Keep** code blocks, error messages, file paths, and technical terms byte-for-byte unchanged
5. **Persist** across all responses until explicitly stopped

## Auto-Clarity Exceptions

Temporarily write normal prose for:
- Security warnings
- Irreversible actions (DROP TABLE, rm -rf, force push)
- Multi-step sequences where order matters
- User says "what?", "explain clearly", "I don't understand"

## Examples

**Normal** (~80 tokens): "Sure, I'd be happy to explain! Actually, the reason your React component is re-rendering is likely because you're passing a new object reference as a prop every time the component renders, which causes React to see the prop as changed."

**Pordee full** (~22 tokens): "New object ref every render. Inline object prop = new ref = re-render. Wrap with `useMemo`."

---
ARGUMENTS: $ARGUMENTS
