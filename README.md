# Claude Skills Collection

Personal collection of custom Claude skills and plugins.

## Skills

### Knowledge Management & Education

#### obsidian-study-vault-builder
Build comprehensive, mobile-compatible Obsidian study vaults from academic course materials with checkpoint-based workflow, error pattern recognition, and quality assurance.

[See obsidian-study-vault-builder/](obsidian-study-vault-builder/)

### Document Processing

#### document-quality-standards
Quality patterns for all document operations (DOCX, PDF, XLSX, PPTX).

[See document-quality-standards/](document-quality-standards/)

#### docx-template-filling
Fill DOCX template forms programmatically while preserving 100% of original structure.

[See docx-template-filling/](docx-template-filling/)

#### docx-advanced-patterns
Advanced python-docx patterns for nested tables and complex cell structures.

[See docx-advanced-patterns/](docx-advanced-patterns/)

#### rtl-document-translation
Translate structured documents (DOCX) to RTL languages while preserving formatting.

[See rtl-document-translation/](rtl-document-translation/)

### Workflow Automation

#### ralph-loop
Autonomous iteration mode using Stop hooks. Claude Code only.

[See ralph-loop/](ralph-loop/)

## Plugins

#### pdf-guard
Prevents context crashes from PDF reads. Blocks direct PDF reads, warns at 100KB, blocks at 500KB, tracks cumulative reads.

```bash
claude plugin install pdf-guard@belumume/claude-skills
```

[See plugins/pdf-guard/](plugins/pdf-guard/)

## Installation

### Skills
```bash
cp -r claude-skills/skill-name ~/.claude/skills/
```

### Plugins
```bash
claude plugin install plugin-name@belumume/claude-skills
```

### Web/Desktop
Upload ZIPs from `web-desktop-exports/` via Settings → Capabilities.

## Structure

```
claude-skills/
├── skill-name/                    # Skills
│   └── SKILL.md
├── plugins/                       # Plugins
│   └── plugin-name/
│       ├── .claude-plugin/plugin.json
│       ├── hooks/
│       ├── scripts/
│       └── skills/
└── web-desktop-exports/           # Web/desktop ZIPs
```

## License

MIT
