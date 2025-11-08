# DOCX Advanced Patterns Skill

Advanced python-docx patterns for handling complex document structures beyond basic `.text` extraction. Complements the official docx skill.

## What This Skill Does

Provides specialized extraction patterns for python-docx workflows, focusing on:
- ✅ **Nested table content extraction** (tables within table cells)
- ✅ **Form and checklist processing** (checkbox options, rating scales)
- ✅ **Complex cell structure handling** (multi-row layouts)
- ✅ **Content that doesn't appear with `.text` property**

## When to Use

**Use this skill when:**
- Cell text appears empty but visual content exists
- Working with forms that have checkbox options
- Processing evaluation documents with rating scales
- Extracting data from cells with complex nested layouts
- Translating documents with checklists

**Not suitable for:**
- Basic text extraction (use official docx skill)
- Document creation (use official docx skill)
- Simple paragraph/table reading

## Quick Start

### Installation

**In Claude Code:**
```bash
cp -r docx-advanced-patterns ~/.claude/skills/
```

**In Claude.ai:**
1. Create ZIP: `zip -r docx-advanced-patterns.zip docx-advanced-patterns/`
2. Upload via Settings → Skills → Upload Custom Skill

**Via API:**
```python
from anthropic import Anthropic

client = Anthropic()
with open('docx-advanced-patterns.zip', 'rb') as f:
    skill = client.skills.create(file=f)
```

### Dependencies

```bash
pip install python-docx>=0.8.11
```

### Basic Usage

**Prompt:**
```
Extract content from form.docx including all checkbox options
using the docx-advanced-patterns skill.
```

Claude will automatically:
1. Detect cells with nested tables
2. Extract content using `cell.tables` property
3. Handle checkbox characters and form fields
4. Return complete cell content

## Key Feature: Nested Table Extraction

### The Problem

python-docx's `cell.text` property only extracts direct paragraph text:

```python
cell = table.rows[1].cells[0]
print(cell.text)  # Output: '' or '\n'
# But cell visually contains:
#   High potential    ☐
#   Moderate potential ☐
#   Low potential     ☐
```

### The Solution

Use `cell.tables` property to detect and extract nested content:

```python
from docx import Document

def extract_cell_content_with_nested_tables(cell):
    """Extract all text including nested tables"""
    text_parts = []

    # Direct paragraphs
    for para in cell.paragraphs:
        if para.text.strip():
            text_parts.append(para.text.strip())

    # Nested tables
    if cell.tables:
        for nested_table in cell.tables:
            for nested_row in nested_table.rows:
                text = nested_row.cells[0].text.strip()
                if text and text not in ['⁮', '☐', '☑', '☒']:
                    text_parts.append(text)

    return '\n'.join(text_parts) if text_parts else ''

# Usage
doc = Document('form.docx')
cell = doc.tables[0].rows[1].cells[0]

content = extract_cell_content_with_nested_tables(cell)
print(content)
# Output:
# High potential
# Moderate potential
# Low potential
```

## Use Cases

### 1. Government Forms
Extract checkbox grids and form fields:
- Tax forms
- Applications
- Permits
- Compliance documents

### 2. Evaluation Forms
Process rating scales and assessment options:
- Feasibility analysis
- Performance reviews
- Quality assessments
- Feedback forms

### 3. Surveys & Questionnaires
Extract multiple choice and checkbox options:
- Customer surveys
- Employee feedback
- Research questionnaires
- Poll documents

### 4. Business Checklists
Handle option lists and checkboxes:
- Quality checklists
- Safety protocols
- Compliance checklists
- Process verification forms

### 5. Complex Data Tables
Extract from cells with nested layouts:
- Dashboard-style tables
- Multi-column cells
- Hierarchical data
- Structured forms

## Integration with Official docx Skill

This skill **complements** (not replaces) the official docx skill:

| Feature | Official docx Skill | This Skill |
|---------|---------------------|------------|
| Document creation | ✓ | - |
| Basic text extraction | ✓ | - |
| Tracked changes | ✓ | - |
| Comment handling | ✓ | - |
| **Nested table extraction** | - | **✓** |
| **Form processing** | - | **✓** |
| **Checklist handling** | - | **✓** |

**Use together for comprehensive document handling.**

## Examples

### Example 1: Extract Form Responses

```python
from docx import Document

def extract_form_responses(docx_path):
    """Extract all form checkbox options"""
    doc = Document(docx_path)
    responses = {}

    for table in doc.tables:
        for row in table.rows:
            question = row.cells[0].text.strip()

            # Check for nested table options
            if row.cells[1].tables:
                options = extract_cell_content_with_nested_tables(row.cells[1])
                responses[question] = options.split('\n')

    return responses

# Usage
form_data = extract_form_responses('application_form.docx')
for question, options in form_data.items():
    print(f"{question}:")
    for option in options:
        print(f"  - {option}")
```

### Example 2: Process Evaluation Document

```python
def extract_evaluation_criteria(docx_path):
    """Extract criteria and rating scales"""
    doc = Document(docx_path)
    evaluations = []

    for table in doc.tables:
        for row_idx, row in enumerate(table.rows[1:], 1):
            criterion = row.cells[0].text.strip()
            rating_options = extract_cell_content_with_nested_tables(row.cells[1])

            evaluations.append({
                'criterion': criterion,
                'options': rating_options.split('\n'),
                'row': row_idx
            })

    return evaluations
```

### Example 3: Detect All Nested Tables

```python
def analyze_document_structure(docx_path):
    """Find all cells with nested tables"""
    doc = Document(docx_path)
    nested_cells = []

    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if cell.tables:
                    nested_cells.append({
                        'table': t_idx,
                        'row': r_idx,
                        'col': c_idx,
                        'count': len(cell.tables)
                    })

    return nested_cells

# Usage
structure = analyze_document_structure('complex_form.docx')
for item in structure:
    print(f"Nested table at Table {item['table']}, "
          f"Row {item['row']}, Col {item['col']}")
```

## Troubleshooting

### Issue: cell.text returns empty but content visible in Word

**Solution:** Cell likely contains nested table. Check `cell.tables`:
```python
if cell.tables:
    print(f"Content is in {len(cell.tables)} nested table(s)")
    content = extract_cell_content_with_nested_tables(cell)
```

### Issue: Checkbox characters appear in output

**Solution:** Filter them out (already handled in extraction function):
```python
if text not in ['⁮', '☐', '☑', '☒']:
    # Process text
```

### Issue: Multi-line content not preserved

**Solution:** Use `'\n'.join()` to preserve structure:
```python
return '\n'.join(text_parts)  # Maintains line breaks
```

## Performance

### For Large Documents

Build a cache of nested table locations:
```python
def build_nested_cache(doc):
    """Pre-compute nested table locations"""
    cache = {}
    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                if cell.tables:
                    cache[(t_idx, r_idx, c_idx)] = len(cell.tables)
    return cache

# Usage
cache = build_nested_cache(doc)

# Later, check cache before extraction
if (t_idx, r_idx, c_idx) in cache:
    content = extract_cell_content_with_nested_tables(cell)
else:
    content = cell.text
```

## Best Practices

1. **Always check for nested tables first**
   ```python
   if cell.tables:
       use_nested_extraction()
   ```

2. **Filter checkbox characters**
   ```python
   CHECKBOX_CHARS = ['⁮', '☐', '☑', '☒']
   ```

3. **Preserve line structure**
   ```python
   '\n'.join(lines)  # Not ' '.join()
   ```

4. **Test with sample documents**
   ```python
   def test_extraction():
       # Verify extraction works
       assert 'expected_content' in result
   ```

## Contributing

This pattern is not currently in the official Anthropic `docx` skill.

**To contribute:**
1. Fork https://github.com/anthropics/skills
2. Add to `document-skills/docx/SKILL.md`
3. Submit pull request with:
   - Pattern description
   - Code examples
   - Use cases

## Documentation

- `SKILL.md` - Complete technical documentation
- `README.md` - This file
- See also: [python-docx documentation](https://python-docx.readthedocs.io/)

## Version History

**v1.0.0** (2025-01-08)
- Initial release
- Nested table extraction pattern
- Form and checklist processing
- Example implementations
- Integration with official docx skill

## License

MIT License - Free for personal and commercial use

## Support

For issues or questions:
- Technical details: See `SKILL.md`
- Examples: See examples in this README
- python-docx docs: https://python-docx.readthedocs.io/

## Credits

Developed from real-world document processing needs including:
- Government forms with checkbox grids
- Business evaluation documents
- Complex survey forms
- RTL translation workflows
