# PDF Guard

Prevents Claude Code context crashes from PDF reads.

## Features
- Blocks direct PDF reads (forces extraction)
- Warns at 100KB, blocks at 500KB
- Tracks cumulative reads (warns 100K tokens, blocks 150K)

## Install
```
claude plugin install pdf-guard@belumume/claude-skills
```

## Requirements
- Python 3.10+
- PyMuPDF (`pip install pymupdf`)
