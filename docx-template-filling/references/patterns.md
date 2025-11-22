# DOCX Template Filling - Detailed Patterns Reference

This reference contains detailed technical patterns for template filling. Load when implementing specific operations.

## Content Range Extraction Pattern

Extract multi-paragraph sections between marker paragraphs.

```python
def extract_content_ranges(doc, markers):
    """
    Extract content sections between marker paragraphs.

    Args:
        doc: Document object
        markers: List of marker texts (e.g., ["Task 1:", "Task 2:", "Task 3:"])

    Returns:
        Dict of marker -> (start_idx, end_idx, paragraphs)

    Example:
        ranges = extract_content_ranges(doc, ["Task 1:", "Task 2:", "References"])
        # Returns: {
        #   "Task 1:": (5, 64, [para objects]),
        #   "Task 2:": (65, 107, [para objects]),
        #   "References": (108, 199, [para objects])
        # }
    """
    # Find all markers
    marker_positions = []
    for i, para in enumerate(doc.paragraphs):
        for marker in markers:
            if marker in para.text:
                marker_positions.append((marker, i))

    # Sort by position
    marker_positions.sort(key=lambda x: x[1])

    # Extract ranges between markers
    ranges = {}
    for i, (marker, start_idx) in enumerate(marker_positions):
        # Content starts AFTER the marker paragraph
        content_start = start_idx + 1

        # Content ends at next marker (or end of document)
        if i + 1 < len(marker_positions):
            content_end = marker_positions[i + 1][1]
        else:
            content_end = len(doc.paragraphs)

        # Extract paragraph range
        content_paras = doc.paragraphs[content_start:content_end]

        ranges[marker] = {
            'start_idx': content_start,
            'end_idx': content_end,
            'paragraphs': content_paras,
            'count': len(content_paras)
        }

    return ranges
```

## Table Identity Detection Strategies

python-docx doesn't assign table IDs. Identify tables by examining content.

### Strategy 1: Check First Cell Text

```python
def identify_tables(doc):
    """
    Identify tables by examining their content.

    Returns dict of table_type -> table_index
    """
    table_identities = {}

    for i, table in enumerate(doc.tables):
        # Strategy 1: Check first cell text
        first_cell = table.rows[0].cells[0].text.strip()

        if "ID" in first_cell or "Name" in first_cell:
            table_identities['info'] = i

        elif "Grading" in first_cell or "Points" in first_cell or "Score" in first_cell:
            table_identities['scoring'] = i

        # Strategy 2: Check dimensions
        elif len(table.rows) == 9 and len(table.columns) == 4:
            # Likely the comparison table
            table_identities['comparison'] = i

        # Strategy 3: Check header row content
        else:
            first_row_text = " ".join([c.text for c in table.rows[0].cells])

            if "Metric" in first_row_text and "Original" in first_row_text:
                table_identities['comparison'] = i

            elif all(keyword in first_row_text.lower()
                    for keyword in ['name', 'id']):
                table_identities['info'] = i

    return table_identities
```

### Usage

```python
doc = Document('template.docx')
tables = identify_tables(doc)

# Now safely access tables by type
if 'info' in tables:
    info_table = doc.tables[tables['info']]
    info_table.rows[0].cells[1].text = "Jane Smith"

if 'scoring' in tables:
    # Leave scoring table untouched
    print("Preserving scoring table")

if 'comparison' in tables:
    comparison_table = doc.tables[tables['comparison']]
    # Move or modify as needed
```

## Robust Anchor Matching Modes

Trade-off between precision and robustness.

```python
def find_anchors(doc, anchor_text, mode='exact'):
    """
    Find anchor paragraphs with configurable matching.

    Args:
        doc: Document object
        anchor_text: Text to search for
        mode: 'exact' (fragile to spacing) or 'partial' (more robust)

    Returns:
        List of paragraph indices
    """
    anchors = []

    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()

        if mode == 'exact':
            # Exact match - fragile to whitespace changes
            if text == anchor_text:
                anchors.append(i)

        elif mode == 'partial':
            # Partial match - more robust
            if anchor_text in text:
                anchors.append(i)

        elif mode == 'smart':
            # Smart match - case-insensitive, whitespace-tolerant
            normalized_text = ' '.join(text.lower().split())
            normalized_anchor = ' '.join(anchor_text.lower().split())

            if normalized_anchor == normalized_text:
                anchors.append(i)

    return anchors
```

**Guidelines:**
- Use `exact` when anchor is highly specific (e.g., "Answer:" with no other text)
- Use `partial` when anchor might have prefix/suffix (e.g., "Summary Table: Comparison")
- Use `smart` for maximum robustness

## XML-Level Paragraph Insertion

Insert paragraphs at specific positions without stale reference issues.

```python
def insert_paragraphs_after_anchor(doc, anchor_text, content_paragraphs):
    """
    Insert content immediately after anchor paragraph using XML API.

    This is forensically clean - inserted paragraphs become part of
    the original document structure without artifacts.

    Args:
        doc: Document object
        anchor_text: Text to search for (e.g., "Answer:")
        content_paragraphs: List of paragraph objects from source document

    Returns:
        Number of paragraphs inserted
    """
    # Find anchor
    anchor_idx = None
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip() == anchor_text:
            anchor_idx = i
            break

    if anchor_idx is None:
        raise ValueError(f"Anchor '{anchor_text}' not found in template")

    # Get XML elements
    anchor_element = doc.paragraphs[anchor_idx]._element
    parent = anchor_element.getparent()

    # Insert each paragraph right after anchor
    inserted_count = 0
    for source_para in content_paragraphs:
        # Use XML element directly - preserves all formatting
        new_para_element = source_para._element

        # Insert after anchor position
        parent.insert(
            parent.index(anchor_element) + 1 + inserted_count,
            new_para_element
        )
        inserted_count += 1

    return inserted_count
```

**Why XML API:**
- `doc.add_paragraph()` appends at end → wrong position
- `para.insert_paragraph_before()` has index tracking issues
- XML API: direct element manipulation → correct position, zero artifacts

## Table Element Repositioning

Move existing table to new position without recreating.

```python
def move_table_to_position(doc, table_index, insert_before_para_index):
    """
    Move existing table to new position without recreating.

    Use when table is in wrong location but must preserve its structure.
    """
    table = doc.tables[table_index]
    table_element = table._element

    # Remove from current position
    current_parent = table_element.getparent()
    current_parent.remove(table_element)

    # Insert at new position
    target_para = doc.paragraphs[insert_before_para_index]
    target_element = target_para._element
    target_parent = target_element.getparent()

    target_parent.insert(
        target_parent.index(target_element),
        table_element
    )
```

## Reverse-Order Multi-Anchor Insertion

Insert at multiple positions without index shifting.

```python
def insert_at_multiple_anchors(doc, anchor_content_pairs):
    """
    Insert content at multiple anchor positions safely.

    Args:
        anchor_content_pairs: List of (anchor_idx, content_paras) tuples
    """
    # Sort in reverse order (largest index first)
    sorted_pairs = sorted(anchor_content_pairs, key=lambda x: x[0], reverse=True)

    # Insert from bottom up to preserve earlier indices
    for anchor_idx, content_paras in sorted_pairs:
        insert_after(doc, anchor_idx, content_paras)
```

**Why reverse order:**
```python
# Example: Template has "Answer:" at paragraphs 18, 27, 37

# WRONG: Forward insertion shifts later indices
insert_after(doc, 18, task1_content)  # Task 1 inserted
# Now the "Answer:" that WAS at 27 is now at 27 + len(task1_content)
insert_after(doc, 27, task2_content)  # WRONG! Inserts at wrong position

# CORRECT: Reverse order preserves earlier indices
insert_after(doc, 37, task3_content)  # Insert last first
insert_after(doc, 27, task2_content)  # Middle still at 27
insert_after(doc, 18, task1_content)  # First still at 18
```

## Selective Table Cell Modification

Fill specific cells without recreating table.

```python
def fill_table_cells(template, table_index, cell_values):
    """
    Fill specific cells in existing table without recreating.

    Args:
        template: Document object
        table_index: Which table to modify (0-indexed)
        cell_values: Dict of (row, col) -> value

    Example:
        fill_table_cells(doc, 0, {
            (0, 1): "5",
            (1, 1): "Jane Smith",
            (1, 2): "S12345"
        })
    """
    table = template.tables[table_index]

    for (row, col), value in cell_values.items():
        # Modify existing cell - don't recreate
        table.rows[row].cells[col].text = value

    # Table structure, styles, borders all preserved
```

**Key principle:** Modify cells in place. Never remove and recreate the table.

## Complete Multi-Section Workflow

```python
from docx import Document

# STEP 1: Load template (never copy, never recreate)
template = Document('Form_Template.docx')

# STEP 2: Inspect structure
print("=== Template Structure ===")
print(f"Tables: {len(template.tables)}")
print(f"Paragraphs: {len(template.paragraphs)}")

# Find anchors
answer_positions = []
for i, para in enumerate(template.paragraphs):
    if para.text.strip() == "Answer:":
        answer_positions.append(i)
        print(f"  Found 'Answer:' at paragraph {i}")

# STEP 3: Fill info table (if exists)
if len(template.tables) > 0:
    info_table = template.tables[0]

    # Check if this is the info table
    if "Name" in info_table.rows[0].cells[0].text:
        # Fill cells in place
        info_table.rows[0].cells[1].text = "Jane Smith"
        info_table.rows[1].cells[1].text = "S12345"
        info_table.rows[2].cells[1].text = "Dept A"
        print("  Filled info table")

# STEP 4: Load content
content_doc = Document('my_content.docx')

# Find where each section starts
section1_start = None
section2_start = None

for i, para in enumerate(content_doc.paragraphs):
    if "Section 1" in para.text or "Question 1" in para.text:
        section1_start = i + 1  # Content starts after header
    elif "Section 2" in para.text or "Question 2" in para.text:
        section2_start = i + 1

# Extract content paragraphs
section1_paragraphs = content_doc.paragraphs[section1_start:section2_start-1]
section2_paragraphs = content_doc.paragraphs[section2_start:]

# STEP 5: Insert at anchors using XML API
def insert_after(doc, anchor_idx, content_paras):
    anchor_elem = doc.paragraphs[anchor_idx]._element
    parent = anchor_elem.getparent()

    for offset, para in enumerate(content_paras):
        parent.insert(
            parent.index(anchor_elem) + 1 + offset,
            para._element
        )

# Insert in REVERSE order to preserve indices
insert_after(template, answer_positions[1], section2_paragraphs)
insert_after(template, answer_positions[0], section1_paragraphs)

print(f"  Inserted {len(section1_paragraphs)} paragraphs for Section 1")
print(f"  Inserted {len(section2_paragraphs)} paragraphs for Section 2")

# STEP 6: Save (original template fully preserved with content inserted)
template.save('Form_Completed.docx')

print("\n✓ Template filled - zero artifacts")
```

## Verification Pattern

```python
def verify_template_preservation(original_path, filled_path):
    """
    Verify that only expected content was added.

    Checks:
    - Table count unchanged (unless expected)
    - Section count unchanged
    - Styles unchanged
    - Headers/footers preserved
    """
    original = Document(original_path)
    filled = Document(filled_path)

    # 1. Table count
    if len(original.tables) != len(filled.tables):
        print(f"Warning: Table count changed: {len(original.tables)} → {len(filled.tables)}")
    else:
        print(f"✓ Table count preserved: {len(original.tables)}")

    # 2. Section count
    if len(original.sections) != len(filled.sections):
        print(f"Warning: Section count changed")
    else:
        print(f"✓ Section count preserved: {len(original.sections)}")

    # 3. Check specific table integrity
    for i, (orig_table, fill_table) in enumerate(zip(original.tables, filled.tables)):
        orig_rows = len(orig_table.rows)
        fill_rows = len(fill_table.rows)

        if orig_rows != fill_rows:
            print(f"Warning: Table {i} rows changed: {orig_rows} → {fill_rows}")
        else:
            print(f"✓ Table {i} structure preserved")

    # 4. Headers/Footers
    for i, (orig_sec, fill_sec) in enumerate(zip(original.sections, filled.sections)):
        orig_header = orig_sec.header.paragraphs[0].text if orig_sec.header.paragraphs else ""
        fill_header = fill_sec.header.paragraphs[0].text if fill_sec.header.paragraphs else ""

        if orig_header != fill_header:
            print(f"Warning: Section {i} header changed")
        else:
            print(f"✓ Section {i} header preserved")
```
