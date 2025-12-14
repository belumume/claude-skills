# Claude Skills Collection

Personal collection of custom Claude skills, created as I discover patterns and solve real-world problems.

## Skills

### Knowledge Management & Education

#### obsidian-study-vault-builder
Build comprehensive, mobile-compatible Obsidian study vaults from academic course materials with checkpoint-based workflow, error pattern recognition, and quality assurance. Works across all subjects - CS, medicine, business, self-study.

**Battle-tested:** 37-file vaults, 828KB content, 910-line comprehensive patterns, ~80 hours saved per project.

[See obsidian-study-vault-builder/README.md](obsidian-study-vault-builder/README.md)

### Document Processing

#### document-quality-standards
Quality patterns for all document operations (DOCX, PDF, XLSX, PPTX). Visual verification workflow, typography hygiene, formula best practices. Patterns from OpenAI skills that Anthropic's document-skills plugin lacks.

[See document-quality-standards/](document-quality-standards/)

#### docx-template-filling
Fill DOCX template forms programmatically while preserving 100% of original structure - logos, footers, styles, metadata. Zero-artifact insertion for forms, applications, and standardized documents. Output indistinguishable from manual filling.

**Key features:** Anchor-based XML insertion, structure preservation, table repositioning, executable inspection script.

[See docx-template-filling/](docx-template-filling/)

#### docx-advanced-patterns
Advanced python-docx patterns for nested tables, complex cell structures, and content extraction beyond basic `.text` property. Complements official docx skill with specialized read techniques.

[See docx-advanced-patterns/README.md](docx-advanced-patterns/README.md)

#### rtl-document-translation
Translate structured documents (DOCX) to RTL languages (Arabic, Hebrew, Urdu) while preserving exact formatting, table structures, colors, and layouts.

[See rtl-document-translation/README.md](rtl-document-translation/README.md)

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
cp -r claude-skills/obsidian-study-vault-builder ~/.claude/skills/
```

### In Claude Web/Desktop

Ready-to-upload ZIPs are in `web-desktop-exports/`:

```
web-desktop-exports/
├── document-quality-standards.zip
├── docx-advanced-patterns.zip
├── docx-template-filling.zip
├── obsidian-study-vault-builder.zip
└── rtl-document-translation.zip
```

1. Download the ZIP for the skill you want
2. Go to Settings → Capabilities
3. Upload the ZIP file

**Note:** Web/desktop exports have stripped frontmatter (name + description only, <200 chars) to meet Claude web/desktop requirements. The original Claude Code skills in the root folders retain full frontmatter (version, dependencies, tags).

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
├── skill-name/                    # Claude Code skills (full frontmatter)
│   ├── SKILL.md                   # Skill definition (required)
│   ├── README.md                  # User documentation
│   └── ...                        # Additional files
├── another-skill/
│   └── ...
└── web-desktop-exports/           # Claude web/desktop versions
    ├── skill-name.zip             # Ready-to-upload ZIPs
    └── skill-name/                # Stripped SKILL.md + supporting files
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
