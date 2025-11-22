---
name: docx-template-filling
description: Fill DOCX template forms programmatically while preserving 100% of original structure - logos, footers, styles, metadata. Zero-artifact insertion for forms, applications, and standardized documents. Output indistinguishable from manual filling.
version: 1.0.0
dependencies:
  - python>=3.8
  - python-docx>=0.8.11
---

# DOCX Template Filling - Forensic Preservation

Fill template forms programmatically with **zero detectable artifacts**. The filled document must be indistinguishable from manual typing in the original template.

## When to Use This Skill

Invoke when:
- Filling standardized forms and templates
- Completing application forms
- Responding to questionnaires and surveys
- Processing template-based documents
- Any scenario where the recipient must not detect programmatic manipulation

**Critical requirement**: Template integrity must be 100% preserved (logos, footers, headers, styles, metadata, element structure).

## Core Philosophy: Preservation Over Recreation

**WRONG approach**: Extract content from template, generate new document
- Loses metadata
- Changes element IDs
- Alters styles subtly
- Creates detectable artifacts

**RIGHT approach**: Load template, insert content at anchor points using XML API
- Preserves all original elements
- Maintains metadata
- Zero structural changes
- Indistinguishable from manual entry

## Critical Anti-Patterns

### ❌ NEVER: Use pandoc with --reference-doc

```bash
# This SEEMS correct but ONLY copies styles, NOT structure
pandoc content.md -o output.docx --reference-doc=template.docx
```

**What happens**:
- Template's tables disappear
- Logos, headers, footers lost
- Only style definitions copied
- **Looks completely different**

**Why it fails**: `--reference-doc` means "copy the style definitions," NOT "preserve the document structure"

### ❌ NEVER: Append content at the end

```python
# This destroys template structure
template = Document('template.docx')

# Remove content after markers
# ... (deletion logic)

# Append all new content at end
for para in new_content:
    template.add_paragraph(para.text)  # WRONG!
```

**What happens**:
- Template questions appear unanswered
- All answers grouped at end
- Structure broken
- **Obviously programmatic**

### ❌ NEVER: Recreate tables

```python
# DON'T copy table structure and rebuild
new_table = template.add_table(rows=3, cols=2)
# Even if you copy all properties, it's not the original!
```

**What happens**:
- Loses original element IDs
- Style inheritance breaks
- Metadata changes
- **Detectable as modified**

## The Correct Pattern: Anchor-Based XML Insertion

### Step 1: Read Template Structure FIRST

**Always** inspect before modifying:

```python
from docx import Document

template = Document('template.docx')

# 1. Count elements
print(f"Tables: {len(template.tables)}")
print(f"Paragraphs: {len(template.paragraphs)}")
print(f"Sections: {len(template.sections)}")

# 2. Find anchor points (where to insert content)
anchors = []
for i, para in enumerate(template.paragraphs):
    text = para.text.strip()
    if text == "Answer:" or "FILL HERE" in text or text.endswith(":"):
        anchors.append((i, text))
        print(f"  Anchor at paragraph {i}: '{text}'")

# 3. Identify tables to modify vs. preserve
for i, table in enumerate(template.tables):
    first_cell = table.rows[0].cells[0].text
    print(f"  Table {i}: {first_cell[:50]}...")
    # Identify: "Group Info" = modify, "Grading" = preserve
```

**Critical**: Never assume structure. Always inspect first.

### Step 2: Selective Table Filling (Preserve Originals)

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
            (1, 1): "John Doe",
            (1, 2): "S12345"
        })
    """
    table = template.tables[table_index]

    for (row, col), value in cell_values.items():
        # Modify existing cell - don't recreate
        table.rows[row].cells[col].text = value

    # Table structure, styles, borders all preserved
```

**Key principle**: Modify cells in place. Never remove and recreate the table.

### Step 3: Content Insertion at Anchors (XML API)

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

**Why XML API?**
- `doc.add_paragraph()` appends at end → wrong position
- `para.insert_paragraph_before()` has index tracking issues
- XML API: direct element manipulation → correct position, zero artifacts

### Step 4: Table Repositioning (If Needed)

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

**When to use**: Table exists but in wrong location (e.g., summary table after references instead of in summary section).

## Essential Patterns & Pitfalls

### Pattern 1: Systematic Template Inspection (ALWAYS DO THIS FIRST)

**Critical**: Inspect before modifying. Never assume structure.

```python
def inspect_template(doc_path):
    """
    Print complete template structure before any modifications.

    Use this BEFORE every template filling operation to:
    - Identify which tables are which
    - Find anchor points
    - Understand document structure
    - Prevent destructive mistakes
    """
    doc = Document(doc_path)

    print("=" * 70)
    print("TEMPLATE STRUCTURE ANALYSIS")
    print("=" * 70)

    # 1. High-level counts
    print(f"\nDocument Elements:")
    print(f"  Tables: {len(doc.tables)}")
    print(f"  Paragraphs: {len(doc.paragraphs)}")
    print(f"  Sections: {len(doc.sections)}")

    # 2. Table identities
    print(f"\nTable Analysis:")
    for i, table in enumerate(doc.tables):
        first_cell = table.rows[0].cells[0].text[:60]
        print(f"  Table {i}:")
        print(f"    Size: {len(table.rows)}x{len(table.columns)}")
        print(f"    First cell: '{first_cell}...'")

        # Sample first row to identify table type
        first_row_text = " | ".join([c.text[:20] for c in table.rows[0].cells])
        print(f"    First row: {first_row_text}")

    # 3. Potential anchor points
    print(f"\nPotential Anchor Points:")
    anchors_found = 0
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()

        # Common anchor patterns
        if (text.endswith(':') or
            'Answer' in text or
            'Summary' in text or
            'FILL' in text or
            text in ['', '\n']):  # Empty paragraphs might be fill points

            print(f"  Para {i}: '{text}' (style: {para.style.name})")
            anchors_found += 1

            if anchors_found > 20:  # Limit output
                print(f"  ... ({len(doc.paragraphs) - i} more paragraphs)")
                break

    # 4. Headers/Footers
    print(f"\nHeaders/Footers:")
    for i, section in enumerate(doc.sections):
        header_text = section.header.paragraphs[0].text[:50] if section.header.paragraphs else "(empty)"
        footer_text = section.footer.paragraphs[0].text[:50] if section.footer.paragraphs else "(empty)"
        print(f"  Section {i}:")
        print(f"    Header: {header_text}")
        print(f"    Footer: {footer_text}")

    print("=" * 70)

    return doc

# ALWAYS use this before modifying
doc = inspect_template('template.docx')
# Now you know the structure - proceed safely
```

**Why this matters**: I made destructive mistakes by assuming structure. This inspection prevents:
- Modifying wrong tables
- Missing anchor points
- Breaking headers/footers
- Index out-of-bounds errors

### Pattern 2: Content Range Extraction by Markers

**Use case**: Extract multi-paragraph sections between markers (e.g., "Task 1:", "Task 2:", "References").

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

# Usage
content_doc = Document('my_content.docx')
sections = extract_content_ranges(content_doc, ["Task 1:", "Task 2:", "Task 3:"])

# Now insert each section at appropriate anchors
for task_name, info in sections.items():
    print(f"{task_name}: {info['count']} paragraphs")
    # Insert info['paragraphs'] at corresponding anchor in template
```

**Why this matters**: We used this pattern repeatedly. It's fundamental for extracting multi-section documents.

### Pattern 3: Table Identity Detection Strategies

**Problem**: python-docx doesn't give tables IDs. You need to identify "which table is which."

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

# Usage
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

**Why this matters**: Templates often have multiple tables. You need robust identification to avoid modifying the wrong one.

### Pattern 4: Robust Anchor Matching (Exact vs. Partial)

**Trade-off**: Exact matching is precise but fragile. Partial matching is robust but can false-match.

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

# Recommendation: Use 'smart' mode for robustness
answer_anchors = find_anchors(doc, "Answer:", mode='smart')

# For heading-like anchors, partial is often better
summary_section = find_anchors(doc, "Summary Table:", mode='partial')
```

**Guidelines**:
- Use `exact` when anchor is highly specific (e.g., "Answer:" with no other text)
- Use `partial` when anchor might have prefix/suffix (e.g., "Summary Table: Comparison of Algorithms")
- Use `smart` for maximum robustness

### Pattern 5: The `insert_paragraph_before()` Pitfall

**Problem**: After inserting paragraphs, paragraph objects become stale.

```python
# ❌ WRONG: This will crash
def insert_content_wrong(doc, anchor_idx, content_paras):
    insertion_point = doc.paragraphs[anchor_idx]

    for para in content_paras:
        new_para = insertion_point.insert_paragraph_before(para.text)

        # Update insertion point for next paragraph
        para_idx = doc.paragraphs.index(insertion_point)  # ValueError!
        # The doc.paragraphs list rebuilt, insertion_point is stale
        insertion_point = doc.paragraphs[para_idx + 1]

# ✓ CORRECT: Use XML API directly
def insert_content_correct(doc, anchor_idx, content_paras):
    """
    Insert content using XML API - no stale references.
    """
    anchor_element = doc.paragraphs[anchor_idx]._element
    parent = anchor_element.getparent()

    for offset, para in enumerate(content_paras):
        parent.insert(
            parent.index(anchor_element) + 1 + offset,
            para._element
        )

    # No stale references - we work at XML level
```

**Why it fails**:
1. `insert_paragraph_before()` modifies the document XML
2. python-docx's `doc.paragraphs` list is rebuilt
3. Your old `insertion_point` object no longer exists in the new list
4. `.index()` search fails with `ValueError`

**Solution**: Always use XML API for position-sensitive insertions.

### Pattern 6: Reverse-Order Insertion to Preserve Indices

**Problem**: Inserting content changes paragraph indices for later anchors.

```python
# Example: Template has "Answer:" at paragraphs 18, 27, 37

# ❌ WRONG: Forward insertion shifts later indices
insert_after(doc, 18, task1_content)  # Task 1 inserted
# Now the "Answer:" that WAS at 27 is now at 27 + len(task1_content)
insert_after(doc, 27, task2_content)  # WRONG! Inserts at wrong position

# ✓ CORRECT: Reverse order preserves earlier indices
insert_after(doc, 37, task3_content)  # Insert last first
insert_after(doc, 27, task2_content)  # Middle still at 27
insert_after(doc, 18, task1_content)  # First still at 18
```

**Rule**: When inserting at multiple positions, **always insert from bottom to top**.

```python
def insert_at_multiple_anchors(doc, anchor_content_pairs):
    """
    Insert content at multiple anchor positions safely.

    Args:
        anchor_content_pairs: List of (anchor_idx, content_paras) tuples
    """
    # Sort in reverse order (largest index first)
    sorted_pairs = sorted(anchor_content_pairs, key=lambda x: x[0], reverse=True)

    # Insert from bottom up
    for anchor_idx, content_paras in sorted_pairs:
        insert_after(doc, anchor_idx, content_paras)
```

## Complete Workflow: Template Filling

### Scenario: Fill template form with responses

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

# STEP 4: Load your content
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

# STEP 5: Insert answers at anchors using XML API
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

## Verification: Ensuring Zero Artifacts

After filling, verify preservation:

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
        print(f"⚠️  Table count changed: {len(original.tables)} → {len(filled.tables)}")
    else:
        print(f"✓ Table count preserved: {len(original.tables)}")

    # 2. Section count
    if len(original.sections) != len(filled.sections):
        print(f"⚠️  Section count changed")
    else:
        print(f"✓ Section count preserved: {len(original.sections)}")

    # 3. Check specific table integrity (e.g., grading table should be untouched)
    for i, (orig_table, fill_table) in enumerate(zip(original.tables, filled.tables)):
        orig_rows = len(orig_table.rows)
        fill_rows = len(fill_table.rows)

        if orig_rows != fill_rows:
            print(f"⚠️  Table {i} rows changed: {orig_rows} → {fill_rows}")
        else:
            print(f"✓ Table {i} structure preserved")

    # 4. Headers/Footers
    for i, (orig_sec, fill_sec) in enumerate(zip(original.sections, filled.sections)):
        orig_header = orig_sec.header.paragraphs[0].text if orig_sec.header.paragraphs else ""
        fill_header = fill_sec.header.paragraphs[0].text if fill_sec.header.paragraphs else ""

        if orig_header != fill_header:
            print(f"⚠️  Section {i} header changed")
        else:
            print(f"✓ Section {i} header preserved")

# Usage
verify_template_preservation('template.docx', 'filled.docx')
```

## Advanced: Multi-Anchor Insertion Pattern

For templates with multiple fill points:

```python
def fill_template_at_multiple_anchors(template_path, anchor_content_map, output_path):
    """
    Fill template at multiple anchor points in one pass.

    Args:
        template_path: Path to template
        anchor_content_map: Dict of anchor_text -> list of paragraph objects
        output_path: Where to save filled document

    Example:
        fill_template_at_multiple_anchors(
            'template.docx',
            {
                'Answer:': question1_paragraphs,
                'Solution:': question2_paragraphs,
                'Discussion:': discussion_paragraphs
            },
            'completed.docx'
        )
    """
    template = Document(template_path)

    # Find all anchors
    anchor_indices = {}
    for i, para in enumerate(template.paragraphs):
        text = para.text.strip()
        if text in anchor_content_map:
            if text not in anchor_indices:
                anchor_indices[text] = []
            anchor_indices[text].append(i)

    # Sort anchor positions in reverse order
    # (insert from bottom up to preserve earlier indices)
    all_insertions = []
    for anchor_text, content_paras in anchor_content_map.items():
        for idx in anchor_indices.get(anchor_text, []):
            all_insertions.append((idx, content_paras))

    all_insertions.sort(key=lambda x: x[0], reverse=True)

    # Insert content
    for anchor_idx, content_paras in all_insertions:
        anchor_elem = template.paragraphs[anchor_idx]._element
        parent = anchor_elem.getparent()

        for offset, para in enumerate(content_paras):
            parent.insert(
                parent.index(anchor_elem) + 1 + offset,
                para._element
            )

    template.save(output_path)
```

## Common Scenarios

### 1. Form with Info Table + Q&A Sections

```python
template = Document('form_template.docx')

# Fill info table
info_table = template.tables[0]
info_table.rows[0].cells[1].text = "Applicant Name"
info_table.rows[1].cells[1].text = "ID"

# Load responses
responses = Document('my_responses.docx')

# Find "Answer:" markers
answer_positions = [i for i, p in enumerate(template.paragraphs)
                    if p.text.strip() == "Answer:"]

# Insert each response after its marker
for answer_idx, template_para_idx in enumerate(answer_positions):
    # Extract this response's paragraphs from responses doc
    response_content = extract_answer_n(responses, answer_idx)

    # Insert using XML API
    insert_after_anchor(template, template_para_idx, response_content)

template.save('form_completed.docx')
```

### 2. Report with Summary Table Repositioning

```python
template = Document('report_template.docx')

# Fill team info
team_table = template.tables[0]
team_table.rows[0].cells[1].text = "Team 5"

# Insert task solutions
task_anchors = [i for i, p in enumerate(template.paragraphs)
                if p.text.strip() == "Answer:"]

for task_num, anchor_idx in enumerate(task_anchors, 1):
    task_content = load_task_content(task_num)
    insert_after_anchor(template, anchor_idx, task_content)

# Move summary table to correct position
summary_table_heading_idx = next(i for i, p in enumerate(template.paragraphs)
                                  if "Summary Table:" in p.text)

# Table is at end, move it right after "Summary Table:" heading
move_table_to_position(template,
                       table_index=2,  # The summary table
                       insert_before_para_index=summary_table_heading_idx + 1)

template.save('project_completed.docx')
```

### 3. Application Form with Checkboxes Preserved

```python
template = Document('application_form.docx')

# Fill text fields only - don't touch checkboxes
for i, para in enumerate(template.paragraphs):
    if "Name:" in para.text:
        # Add run to existing paragraph instead of replacing
        para.add_run(" John Doe")
    elif "Date:" in para.text:
        para.add_run(" 2024-11-22")

# Checkbox fields are preserved as-is (user checks manually in Word)

template.save('application_filled.docx')
```

## Best Practices

### 1. Always Read Before Writing

```python
# ✓ CORRECT: Inspect first
template = Document('template.docx')
print(f"Structure: {len(template.tables)} tables, {len(template.paragraphs)} paragraphs")

# Find anchors
anchors = find_anchors(template)

# Then modify
fill_template(template, anchors, content)
```

```python
# ✗ WRONG: Assume structure
template = Document('template.docx')
template.tables[0].rows[1].cells[1].text = "Data"  # Might not be the right table!
```

### 2. Use XML API for Position-Sensitive Insertions

```python
# ✓ CORRECT: XML element insertion
parent.insert(index, element._element)
```

```python
# ✗ WRONG: Add methods (append to end)
doc.add_paragraph(text)
doc.add_table(rows, cols)
```

### 3. Preserve Original Element References

```python
# ✓ CORRECT: Modify existing elements
table.rows[0].cells[1].text = "New value"
```

```python
# ✗ WRONG: Delete and recreate
table._element.getparent().remove(table._element)
new_table = doc.add_table(...)  # Not the same element!
```

### 4. Test with Template Comparison

```python
# After filling, manually compare:
# 1. Open original template
# 2. Open filled version
# 3. Verify headers/footers identical
# 4. Verify logo intact
# 5. Verify grading tables empty (if they should be)
# 6. Verify styles unchanged
```

### 5. Handle Errors Gracefully

```python
def safe_fill_cell(table, row, col, value):
    """Fill cell with bounds checking."""
    try:
        if row < len(table.rows) and col < len(table.rows[row].cells):
            table.rows[row].cells[col].text = value
        else:
            print(f"⚠️  Cell ({row}, {col}) out of bounds")
    except Exception as e:
        print(f"⚠️  Error filling cell: {e}")
```

## Troubleshooting

### Issue: Content appears at end instead of after anchor

**Cause**: Using `add_paragraph()` instead of XML insertion

**Fix**:
```python
# Instead of:
doc.add_paragraph(text)

# Use:
parent.insert(index, element._element)
```

### Issue: Table disappeared

**Cause**: Recreated table instead of modifying original

**Fix**:
```python
# Instead of:
doc._element.body.remove(table._element)
new_table = doc.add_table(...)

# Use:
table.rows[0].cells[0].text = "Modified value"
```

### Issue: Styles changed

**Cause**: Created new paragraphs instead of copying from source with styles

**Fix**:
```python
# Use paragraph._element from source document
# This preserves all style information
source_para._element  # Has all original formatting
```

### Issue: Headers/footers lost

**Cause**: Used pandoc or recreated document

**Fix**: Never use pandoc for template filling. Load original template with `Document()` and modify in place.

## Integration with docx-advanced-patterns Skill

This skill (template filling) **complements** `docx-advanced-patterns` (nested table extraction):

**docx-advanced-patterns provides:**
- Reading nested tables from complex cells
- Extracting form checkbox options
- Recursive content extraction

**This skill provides:**
- Writing content to templates
- Preserving document structure
- Anchor-based insertion
- Zero-artifact modifications

**Use together:**
```python
from docx import Document

# Read source with nested content (advanced-patterns skill)
source = Document('complex_source.docx')
for table in source.tables:
    for cell in table.rows[0].cells:
        if cell.tables:  # Nested content
            content = extract_cell_content_with_nested_tables(cell)

# Fill template with extracted content (this skill)
template = Document('template.docx')
anchor_idx = find_anchor(template, "Answer:")
insert_content_after_anchor(template, anchor_idx, content)
```

## Success Criteria

Template filling is successful if:
- [ ] Filled document indistinguishable from manual entry
- [ ] All template tables preserved (count unchanged unless expected)
- [ ] Headers/footers unchanged
- [ ] Logo(s) intact
- [ ] Grading/scoring tables empty (if they should be)
- [ ] Styles identical to original
- [ ] Content inserted at correct anchor points (not at end)
- [ ] Template owner cannot detect programmatic manipulation

## Reference

This skill documents patterns from template filling scenarios where:
- Templates have info tables (to fill) and evaluation/scoring tables (preserve empty)
- Multiple anchor points like "Answer:", "Response:", or "Solution:" for content insertion
- Tables may need repositioning to correct sections
- Document structure must remain intact (headers, footers, logos, branding)
- Zero artifacts requirement (recipient cannot detect automation)

**Use cases**: Forms, questionnaires, standardized documents, applications, reports.

Key lesson: **Preservation over recreation.** Never rebuild - always modify in place.
