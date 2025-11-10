# Claude Skills Collection

Personal collection of custom Claude skills, created as I discover patterns and solve real-world problems.

## Skills

### Knowledge Management & Education

#### obsidian-study-vault-builder
Generate comprehensive, mobile-compatible Obsidian study vaults from course materials using checkpoint-based workflow and applied learning principles. Battle-tested on 37-file academic vault.

[See obsidian-study-vault-builder/README.md](obsidian-study-vault-builder/README.md)

### Document Processing

#### rtl-document-translation
Translate structured documents (DOCX) to RTL languages (Arabic, Hebrew, Urdu) while preserving exact formatting, table structures, colors, and layouts.

[See rtl-document-translation/README.md](rtl-document-translation/README.md)

#### docx-advanced-patterns
Advanced python-docx patterns for nested tables, complex cell structures, and content extraction beyond basic `.text` property.

[See docx-advanced-patterns/README.md](docx-advanced-patterns/README.md)

---

*More skills will be added as I discover and document new patterns.*

## Installation

### Quick Install (All Skills)

```bash
# Clone this repository
git clone https://github.com/belumume/claude-skills.git

# Copy all skills to Claude
cp -r claude-skills/*/ ~/.claude/skills/
```

### Individual Skill

```bash
# Install specific skill
cp -r claude-skills/rtl-document-translation ~/.claude/skills/
```

### In Claude.ai

1. Download this repository as ZIP
2. Extract individual skill folders
3. Settings → Skills → Upload Custom Skill

### Via API

```python
from anthropic import Anthropic

client = Anthropic()

# Upload a skill
with open('skill-name.zip', 'rb') as f:
    skill = client.skills.create(file=f)
```

## Repository Structure

```
claude-skills/
├── README.md                      # This file
├── skill-name/                    # Each skill in its own directory
│   ├── SKILL.md                   # Skill definition (required)
│   ├── README.md                  # User documentation
│   └── ...                        # Additional files
└── another-skill/
    └── ...
```

## Contributing

**Want to add a skill?** Open a PR or issue!

**Found a bug?** Open an issue!

**Have a suggestion?** Open an issue!

This is a personal collection, but contributions are welcome.

## Community Contributions

Skills or patterns from this repo that have been contributed upstream:

- **Nested table extraction** → [Anthropic docx skill PR #87](https://github.com/anthropics/skills/pull/87) (under review)

## License

MIT License - Free for personal and commercial use

## About

This collection grows organically as I:
- Encounter new problems
- Discover useful patterns
- Document reusable solutions
- Learn new Claude capabilities

Each skill is battle-tested on real-world use cases before being added.
