# Claude Skills Collection

Personal collection of custom Claude skills and plugins.

## Skills

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

### Architecture & Decision Making

#### deep-brainstorming
Research-hardened brainstorming for high-stakes architecture decisions. 8-phase process with multi-round research, 9-type bias audit, adversarial review, claim provenance tracking, and verification chain termination. Addresses agent failure modes: token exhaustion, hallucinated benchmarks, consensus blindspots, and premature negative claims.

[See deep-brainstorming/](deep-brainstorming/)

### Project Analysis

#### project-retrospective
Multi-agent retrospective for Claude Code projects. Dispatches parallel opus historians to extract structured data from session exports, then synthesizes findings into a comprehensive analysis with decision logs, mistake patterns, and user teaching moments. Supports `last-N` argument for scoped analysis. Requires session exports via `/export`.

[See project-retrospective/](project-retrospective/)

### Workflow Automation

#### rlm-orchestrator
RLM-style orchestration for tasks exceeding single context window limits. Based on [arXiv:2512.24601](https://arxiv.org/abs/2512.24601). Claude Code only.

[See rlm-orchestrator/](rlm-orchestrator/)

#### ralph-loop
Autonomous iteration mode using Stop hooks. Claude Code only.

[See ralph-loop/](ralph-loop/)

## Plugins

#### pdf-guard
Prevents context crashes from PDF reads. Blocks direct PDF reads, warns at 100KB, blocks at 200KB, tracks cumulative reads.

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
