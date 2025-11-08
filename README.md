# Claude Skills Collection

Custom Claude skills for document processing and RTL language translation.

## Available Skills

### 1. rtl-document-translation

Translate structured documents (DOCX) to RTL languages (Arabic, Hebrew, Urdu) while preserving exact formatting, table structures, colors, and layouts.

**Features:**
- 3-level RTL formatting (text direction, alignment, layout)
- Background color preservation
- Multi-pass translation matching
- Quote normalization
- Nested table content extraction
- Automated verification

**Use Cases:**
- Business reports
- Financial forecasts
- Evaluation documents
- Forms and checklists

[See rtl-document-translation/README.md for details](rtl-document-translation/README.md)

### 2. docx-advanced-patterns

Advanced python-docx patterns for handling nested tables, complex cell structures, and content extraction beyond basic `.text` property.

**Features:**
- Nested table content extraction
- Form and checklist processing
- Complex cell structure handling
- Checkbox character filtering

**Use Cases:**
- Government forms
- Evaluation documents with rating scales
- Surveys with multiple choice
- Business checklists

[See docx-advanced-patterns/README.md for details](docx-advanced-patterns/README.md)

## Installation

### In Claude Code

```bash
# Clone this repository
git clone https://github.com/belumume/claude-skills.git

# Copy skills to Claude skills directory
cp -r claude-skills/rtl-document-translation ~/.claude/skills/
cp -r claude-skills/docx-advanced-patterns ~/.claude/skills/
```

### In Claude.ai

1. Download this repository as ZIP
2. Extract the skill folders
3. Go to Settings → Skills → Upload Custom Skill
4. Upload each skill folder

### Via API

```python
from anthropic import Anthropic

client = Anthropic()

# Upload rtl-document-translation skill
with open('rtl-document-translation.zip', 'rb') as f:
    skill1 = client.skills.create(file=f)

# Upload docx-advanced-patterns skill
with open('docx-advanced-patterns.zip', 'rb') as f:
    skill2 = client.skills.create(file=f)
```

## Dependencies

Both skills require:
- Python >= 3.8
- python-docx >= 0.8.11

RTL translation skill also needs:
- Pillow >= 9.0.0 (for image comparisons)

Install dependencies:
```bash
pip install python-docx>=0.8.11 Pillow>=9.0.0
```

## Usage Examples

### RTL Translation

```
Translate "Financial_Report.docx" to Arabic using the rtl-document-translation skill.

Requirements:
- Preserve all table structures
- Maintain color scheme
- Font: Simplified Arabic
```

### Nested Table Extraction

```
Extract content from "form.docx" including all checkbox options
using the docx-advanced-patterns skill.
```

## Contributing

Found a bug or have a suggestion? Please open an issue!

## Community Contribution

The **nested table extraction pattern** from docx-advanced-patterns has been submitted to the official Anthropic docx skill:
- **Pull Request:** https://github.com/anthropics/skills/pull/87
- **Status:** Under review

## License

MIT License - Free for personal and commercial use

## Acknowledgments

Developed from real-world document processing needs:
- Arabic translation of business documents
- Government forms with nested tables
- Evaluation documents with complex layouts
- RTL language formatting challenges

## Support

For issues or questions:
- Open an issue in this repository
- See individual skill README files for detailed documentation
- python-docx docs: https://python-docx.readthedocs.io/
