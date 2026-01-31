# PDF Guard

Prevents Claude Code context crashes from large file and PDF reads.

## Features
- Blocks direct PDF reads (forces extraction via scripts)
- Large file guard: warns at 100KB, blocks at 200KB
- Context tracker with RLM-aware guidance:
  - 75K tokens: suggests delegation strategies
  - 100K tokens: warns with RLM orchestration guidance
  - 150K tokens: critical warning (blocking opt-in via `CLAUDE_BLOCK_AT_LIMIT=1`)
- Subagent-safe: doesn't block subagents (they have fresh context)

## Install
```
claude plugin install pdf-guard@belumume/claude-skills
```

## Environment Variables
- `CLAUDE_BLOCK_AT_LIMIT=1` - Enable hard blocking at 150K tokens
- `CLAUDE_SKIP_CONTEXT_TRACKING=1` - Bypass context tracking entirely

## Requirements
- Python 3.10+
- PyMuPDF (`pip install pymupdf`)
