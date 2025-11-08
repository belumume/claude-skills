# RTL Document Translation - Complete Reference

This file contains complete, production-ready code examples and advanced patterns.

## Complete Implementation Example

### Full Translation Script

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete RTL Document Translation Script
Translates English DOCX to Arabic with structure preservation
"""

import json
import sys
import re
from docx import Document
from docx.shared import RGBColor, Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# CONFIGURATION
# ============================================================================

ENGLISH_DOC = 'english_source.docx'
ARABIC_DOC = 'arabic_output.docx'
TRANSLATION_DICT = 'translation_dictionary.json'

# Font settings
ARABIC_FONT = 'Simplified Arabic'  # or 'Times New Roman' for formal docs
PARAGRAPH_FONT_SIZE = 11
TABLE_FONT_SIZE = 10

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_cell_background(cell):
    """
    Extract cell background color using XML traversal
    Returns hex color (e.g., 'CC0029') or None
    """
    tc = cell._element
    tcPr = tc.tcPr if hasattr(tc, 'tcPr') and tc.tcPr is not None else None

    if tcPr is None:
        return None

    shd_list = tcPr.findall(qn('w:shd'))
    for shd in shd_list:
        fill = shd.get(qn('w:fill'))
        if fill and fill != 'auto':
            return fill.upper()

    return None


def set_cell_background(cell, hex_color):
    """
    Set cell background color
    hex_color: 'CC0029', 'FFE5E5', etc.
    """
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()

    # Remove existing shading
    for shd in tcPr.findall(qn('w:shd')):
        tcPr.remove(shd)

    # Add new shading
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def normalize_text(text):
    """Normalize quotes and unicode spaces"""
    # Convert curly quotes to straight quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")

    # Normalize unicode spaces
    text = re.sub(r'[\u2002\u2003\u2009\u200A\u00A0]+', ' ', text)

    return text.strip()


def translate_text(text, translation_dict):
    """
    Multi-pass translation with normalization fallbacks
    Returns translated text or original if no match
    """
    if not text or not text.strip():
        return text

    # Pass 1: Exact match
    if text in translation_dict:
        return translation_dict[text]

    # Pass 2: Stripped
    stripped = text.strip()
    if stripped in translation_dict:
        return translation_dict[stripped]

    # Pass 3: Normalized quotes
    normalized_quotes = text.replace('\u201c', '"').replace('\u201d', '"')
    normalized_quotes = normalized_quotes.replace('\u2018', "'").replace('\u2019', "'")
    if normalized_quotes in translation_dict:
        return translation_dict[normalized_quotes]

    # Pass 4: Stripped + normalized
    if normalized_quotes.strip() in translation_dict:
        return translation_dict[normalized_quotes.strip()]

    # Pass 5: Unicode spaces
    cleaned = re.sub(r'[\u2002\u2003\u2009\u200A\u00A0]+', ' ', text).strip()
    if cleaned in translation_dict:
        return translation_dict[cleaned]

    # Pass 6: Combined
    cleaned_quotes = re.sub(r'[\u2002\u2003\u2009\u200A\u00A0]+', ' ', normalized_quotes).strip()
    if cleaned_quotes in translation_dict:
        return translation_dict[cleaned_quotes]

    # Pass 7: Normalized whitespace
    normalized_ws = ' '.join(text.split())
    if normalized_ws in translation_dict:
        return translation_dict[normalized_ws]

    # No match - warn and return as-is
    if len(text.strip()) > 1 and any(c.isalpha() for c in text):
        if not re.match(r'^-?\d+$|^\(-?\d+\)$', text.strip()):
            print(f"[WARN] No translation for: '{text.strip()[:50]}'")

    return text


def apply_rtl_to_paragraph(para, arabic_text, font_size=11, bold=False,
                            text_color=None, underline=False):
    """Apply complete RTL formatting to paragraph"""
    para.clear()
    run = para.add_run(arabic_text)

    # RTL text direction
    para.paragraph_format.bidi = True
    run.font.rtl = True
    run.font.complex_script = True

    # Right alignment
    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Font settings
    run.font.name = ARABIC_FONT
    run._element.rPr.rFonts.set(qn('w:ascii'), ARABIC_FONT)
    run._element.rPr.rFonts.set(qn('w:hAnsi'), ARABIC_FONT)
    run._element.rPr.rFonts.set(qn('w:cs'), ARABIC_FONT)

    if font_size:
        run.font.size = Pt(font_size)

    if bold:
        run.font.bold = True

    if underline:
        run.font.underline = True

    if text_color:
        run.font.color.rgb = RGBColor(*text_color)

    return para


def apply_rtl_to_cell(cell, arabic_text, font_size=10, bold=False, text_color=None):
    """Apply complete RTL formatting to table cell"""
    cell.text = ''
    paragraph = cell.paragraphs[0]
    run = paragraph.add_run(arabic_text)

    # RTL text direction
    paragraph.paragraph_format.bidi = True
    run.font.rtl = True
    run.font.complex_script = True

    # Right alignment
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Font settings
    run.font.name = ARABIC_FONT
    run._element.rPr.rFonts.set(qn('w:ascii'), ARABIC_FONT)
    run._element.rPr.rFonts.set(qn('w:hAnsi'), ARABIC_FONT)
    run._element.rPr.rFonts.set(qn('w:cs'), ARABIC_FONT)
    run.font.size = Pt(font_size)

    if bold:
        run.font.bold = True

    if text_color:
        run.font.color.rgb = RGBColor(*text_color)

    return cell


# ============================================================================
# MAIN TRANSLATION FUNCTION
# ============================================================================

def translate_document(eng_doc_path, ar_doc_path, translation_dict_path):
    """
    Main translation function
    Creates Arabic document with identical structure to English
    """
    print("="*80)
    print("RTL DOCUMENT TRANSLATION")
    print("="*80)

    # Load translation dictionary
    print("\n[1/4] Loading translation dictionary...")
    with open(translation_dict_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    print(f"   Loaded {len(translations)} translations")

    # Load English document
    print("[2/4] Loading English document...")
    eng_doc = Document(eng_doc_path)
    print(f"   Sections: {len(eng_doc.sections)}")
    print(f"   Tables: {len(eng_doc.tables)}")
    print(f"   Paragraphs: {len(eng_doc.paragraphs)}")

    # Create Arabic document
    print("[3/4] Creating Arabic document...")
    ar_doc = Document()

    # Remove default paragraph
    if ar_doc.paragraphs:
        p = ar_doc.paragraphs[0]._element
        p.getparent().remove(p)

    # Configure first section (copy from English)
    sec = ar_doc.sections[0]
    eng_sec = eng_doc.sections[0]
    sec.page_width = eng_sec.page_width
    sec.page_height = eng_sec.page_height
    sec.top_margin = eng_sec.top_margin
    sec.bottom_margin = eng_sec.bottom_margin
    sec.left_margin = eng_sec.left_margin
    sec.right_margin = eng_sec.right_margin

    # Process elements in order
    from docx.oxml.text.paragraph import CT_P
    from docx.oxml.table import CT_Tbl

    para_idx = 0
    table_idx = 0

    for element in eng_doc.element.body:
        if isinstance(element, CT_P):
            # Paragraph
            eng_para = eng_doc.paragraphs[para_idx]
            para_idx += 1

            eng_text = eng_para.text
            if not eng_text.strip():
                ar_doc.add_paragraph('')
                continue

            # Translate
            ar_text = translate_text(eng_text, translations)

            # Get formatting
            font_size = PARAGRAPH_FONT_SIZE
            bold = False
            text_color = None
            underline = False

            if eng_para.runs:
                first_run = eng_para.runs[0]
                if first_run.font.size:
                    font_size = first_run.font.size.pt
                if first_run.font.bold:
                    bold = True
                if first_run.font.underline:
                    underline = True
                if first_run.font.color and first_run.font.color.rgb:
                    rgb = first_run.font.color.rgb
                    text_color = (rgb[0], rgb[1], rgb[2])

            # Add Arabic paragraph
            ar_para = ar_doc.add_paragraph()
            apply_rtl_to_paragraph(ar_para, ar_text, font_size, bold, text_color, underline)

        elif isinstance(element, CT_Tbl):
            # Table
            eng_table = eng_doc.tables[table_idx]
            table_idx += 1

            rows = len(eng_table.rows)
            cols = len(eng_table.columns)

            print(f"   Processing Table {table_idx} ({rows}×{cols})...")

            # Create Arabic table
            ar_table = ar_doc.add_table(rows=rows, cols=cols)
            ar_table.style = 'Table Grid'

            # Populate table
            for r_idx, eng_row in enumerate(eng_table.rows):
                for c_idx, eng_cell in enumerate(eng_row.cells):
                    eng_text = eng_cell.text

                    # Translate
                    ar_text = translate_text(eng_text, translations)

                    # Get formatting
                    eng_bg = get_cell_background(eng_cell)
                    eng_text_color = None
                    bold = False

                    if eng_cell.paragraphs and eng_cell.paragraphs[0].runs:
                        for run in eng_cell.paragraphs[0].runs:
                            if run.font.color and run.font.color.rgb:
                                rgb = run.font.color.rgb
                                eng_text_color = (rgb[0], rgb[1], rgb[2])
                                break
                            if run.font.bold:
                                bold = True

                    # Auto-correct white text on dark backgrounds
                    if eng_bg and eng_bg in ['CC0029', 'C00000', '000000']:
                        eng_text_color = (255, 255, 255)

                    # Apply RTL formatting
                    ar_cell = ar_table.rows[r_idx].cells[c_idx]
                    apply_rtl_to_cell(
                        ar_cell,
                        ar_text,
                        font_size=TABLE_FONT_SIZE,
                        bold=bold,
                        text_color=eng_text_color
                    )

                    # Apply background
                    if eng_bg:
                        set_cell_background(ar_cell, eng_bg)

    # Handle multiple sections
    for section_idx in range(1, len(eng_doc.sections)):
        eng_section = eng_doc.sections[section_idx]
        ar_section = ar_doc.add_section()

        ar_section.page_width = eng_section.page_width
        ar_section.page_height = eng_section.page_height
        ar_section.top_margin = eng_section.top_margin
        ar_section.bottom_margin = eng_section.bottom_margin
        ar_section.left_margin = eng_section.left_margin
        ar_section.right_margin = eng_section.right_margin

    print(f"\n[4/4] Processed {para_idx} paragraphs and {table_idx} tables")

    # Save
    ar_doc.save(ar_doc_path)
    print(f"\nSaved to: {ar_doc_path}")

    print("\n" + "="*80)
    print("TRANSLATION COMPLETE")
    print("="*80)


# ============================================================================
# VERIFICATION FUNCTIONS
# ============================================================================

def verify_arabic_document(ar_doc_path, eng_doc_path, translation_dict_path):
    """Comprehensive verification"""
    print("\n" + "="*80)
    print("VERIFICATION")
    print("="*80)

    ar_doc = Document(ar_doc_path)
    eng_doc = Document(eng_doc_path)

    with open(translation_dict_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    # Build allowed English set
    allowed_english = set()
    for key, value in translations.items():
        if key == value and re.search(r'[a-zA-Z]', key):
            allowed_english.add(key.strip())

    # Check 1: Structure
    print("\n[CHECK 1] Structure Verification")
    section_match = len(ar_doc.sections) == len(eng_doc.sections)
    table_match = len(ar_doc.tables) == len(eng_doc.tables)
    para_match = len(ar_doc.paragraphs) == len(eng_doc.paragraphs)

    print(f"   Sections: {len(ar_doc.sections)} (English: {len(eng_doc.sections)}) {'✓' if section_match else '✗'}")
    print(f"   Tables: {len(ar_doc.tables)} (English: {len(eng_doc.tables)}) {'✓' if table_match else '✗'}")
    print(f"   Paragraphs: {len(ar_doc.paragraphs)} (English: {len(eng_doc.paragraphs)}) {'✓' if para_match else '✗'}")

    # Check 2: Alignment
    print("\n[CHECK 2] Alignment Verification")
    total_cells = 0
    right_aligned = 0

    for table in ar_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                total_cells += 1
                if cell.paragraphs and cell.paragraphs[0].alignment == WD_ALIGN_PARAGRAPH.RIGHT:
                    right_aligned += 1

    alignment_pct = (right_aligned / total_cells * 100) if total_cells > 0 else 0
    print(f"   Right-aligned cells: {right_aligned}/{total_cells} ({alignment_pct:.1f}%)")

    # Check 3: English words
    print("\n[CHECK 3] English Word Scan")
    unauthorized_english = []

    def scan_text(text):
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        for word in words:
            if word not in allowed_english:
                # Check if it's a known abbreviation
                if word.upper() not in ['DVD', 'CD', 'TV', 'USB', 'PDF', 'CEO', 'CFO']:
                    unauthorized_english.append(word)

    for para in ar_doc.paragraphs:
        scan_text(para.text)

    for table in ar_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                scan_text(cell.text)

    if unauthorized_english:
        print(f"   ✗ FOUND {len(unauthorized_english)} unauthorized English words:")
        for word in set(unauthorized_english):
            print(f"      - {word}")
    else:
        print(f"   ✓ No unauthorized English found")

    # Summary
    print("\n" + "="*80)
    all_pass = section_match and table_match and alignment_pct == 100 and len(unauthorized_english) == 0
    if all_pass:
        print("✅ ALL CHECKS PASSED")
    else:
        print("⚠️  SOME CHECKS FAILED - Review above")
    print("="*80)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Translate
    translate_document(ENGLISH_DOC, ARABIC_DOC, TRANSLATION_DICT)

    # Verify
    verify_arabic_document(ARABIC_DOC, ENGLISH_DOC, TRANSLATION_DICT)
```

## Advanced Patterns

### Pattern: Dynamic Special Case Handling

For gaps identified during PDF-vs-DOCX verification:

```python
def translate_with_special_cases(eng_text, table_idx, row_idx, col_idx,
                                 translation_dict, special_cases):
    """
    Translate with special case handling
    special_cases: list of {table, row, col, content} dicts
    """
    # Check if this cell is a special case
    for case in special_cases:
        if (case['table'] == table_idx and
            case['row'] == row_idx and
            case['col'] == col_idx):
            # Use special case content instead
            return translate_text(case['content'], translation_dict)

    # Normal translation
    return translate_text(eng_text, translation_dict)
```

### Pattern: Batch Translation Dictionary Creation

```python
def create_translation_dictionary(docx_files, output_path, target_lang='ar'):
    """
    Extract unique texts from multiple documents
    Create comprehensive translation dictionary
    """
    unique_texts = set()

    # Extract all unique texts
    for docx_path in docx_files:
        doc = Document(docx_path)

        # From paragraphs
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                unique_texts.add(text)
                # Also add normalized version
                unique_texts.add(normalize_text(text))

        # From tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()
                    if text:
                        unique_texts.add(text)
                        unique_texts.add(normalize_text(text))

    print(f"Extracted {len(unique_texts)} unique text snippets")

    # Create translations
    translations = {}

    for text in sorted(unique_texts):
        # Skip numbers and scoring notation
        if re.match(r'^-?\d+$|^\(-?\d+\)$', text):
            translations[text] = text  # Self-map
            continue

        # Call translation API (example using Google Translate)
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, dest=target_lang)
            translations[text] = result.text
        except:
            # Fallback: mark for manual translation
            translations[text] = f"[TRANSLATE: {text}]"

    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(translations)} translations to {output_path}")
    return translations
```

### Pattern: Visual Comparison Generator

```python
import subprocess
from PIL import Image

def create_visual_comparisons(eng_docx, ar_docx, output_dir):
    """
    Generate side-by-side comparison images
    Returns list of comparison image paths
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Convert DOCX → PDF
    eng_pdf = eng_docx.replace('.docx', '.pdf')
    ar_pdf = ar_docx.replace('.docx', '.pdf')

    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, eng_docx
    ])

    subprocess.run([
        'soffice', '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, ar_docx
    ])

    # Convert PDF → PNG images
    subprocess.run([
        'pdftoppm', '-png', '-r', '300',
        eng_pdf, f'{output_dir}/eng'
    ])

    subprocess.run([
        'pdftoppm', '-png', '-r', '300',
        ar_pdf, f'{output_dir}/ar'
    ])

    # Create side-by-side comparisons
    eng_images = sorted([f for f in os.listdir(output_dir) if f.startswith('eng-')])
    ar_images = sorted([f for f in os.listdir(output_dir) if f.startswith('ar-')])

    comparison_paths = []

    for idx, (eng_img, ar_img) in enumerate(zip(eng_images, ar_images), 1):
        eng_path = os.path.join(output_dir, eng_img)
        ar_path = os.path.join(output_dir, ar_img)

        eng = Image.open(eng_path)
        ar = Image.open(ar_path)

        # Create side-by-side
        width = eng.width + ar.width + 20  # 20px gap
        height = max(eng.height, ar.height)

        comparison = Image.new('RGB', (width, height), 'white')
        comparison.paste(eng, (0, 0))
        comparison.paste(ar, (eng.width + 20, 0))

        comparison_path = os.path.join(output_dir, f'comparison_page_{idx}.png')
        comparison.save(comparison_path)
        comparison_paths.append(comparison_path)

        print(f"   Created {comparison_path}")

    return comparison_paths
```

## Troubleshooting Guide

### Issue: Background colors not appearing

**Diagnosis:**
```python
# Check if background exists in English
eng_bg = get_cell_background(eng_cell)
print(f"English background: {eng_bg}")

# Check if background applied to Arabic
ar_bg = get_cell_background(ar_cell)
print(f"Arabic background: {ar_bg}")
```

**Fix:** Ensure using XML traversal, not attribute access.

### Issue: Text invisible on dark backgrounds

**Diagnosis:**
```python
# Check text color
if cell.paragraphs and cell.paragraphs[0].runs:
    run = cell.paragraphs[0].runs[0]
    if run.font.color and run.font.color.rgb:
        print(f"Text color: {run.font.color.rgb}")
```

**Fix:** Auto-set white text for dark backgrounds (see Pattern 6 in SKILL.md).

### Issue: Translation misses

**Diagnosis:**
```python
# Enable debug mode
def translate_text_debug(text, translation_dict):
    print(f"Input: '{text}' (repr: {repr(text)})")
    # ... try each pass and print results
```

**Fix:** Add missing normalization passes or update dictionary.

### Issue: Cell alignment wrong

**Diagnosis:**
```python
# Check alignment
for table in ar_doc.tables:
    for row in table.rows:
        for cell in row.cells:
            para = cell.paragraphs[0]
            print(f"Alignment: {para.alignment}")
            print(f"Bidi: {para.paragraph_format.bidi}")
```

**Fix:** Ensure `apply_rtl_to_cell()` called for ALL cells.

## Performance Optimization

For large documents (100+ pages):

```python
# 1. Cache normalized texts
normalized_cache = {}

def normalize_text_cached(text):
    if text not in normalized_cache:
        normalized_cache[text] = normalize_text(text)
    return normalized_cache[text]

# 2. Batch process tables
def process_table_batch(eng_tables, ar_doc, translation_dict):
    """Process multiple tables in batch"""
    for eng_table in eng_tables:
        # ... process table
        pass

# 3. Use multiprocessing for independent documents
from multiprocessing import Pool

def translate_single_doc(args):
    eng_path, ar_path, trans_dict = args
    translate_document(eng_path, ar_path, trans_dict)

# Translate multiple documents in parallel
with Pool(4) as pool:
    pool.map(translate_single_doc, doc_args)
```

## Testing Template

```python
def test_rtl_translation():
    """Comprehensive test suite"""
    # Test 1: Quote normalization
    assert normalize_text('"test"') == normalize_text('"test"')

    # Test 2: Multi-pass matching
    trans_dict = {'test': 'اختبار', ' test ': 'اختبار'}
    assert translate_text('test', trans_dict) == 'اختبار'
    assert translate_text(' test ', trans_dict) == 'اختبار'
    assert translate_text('"test"', trans_dict) == 'اختبار'

    # Test 3: Background detection
    doc = Document()
    table = doc.add_table(1, 1)
    cell = table.rows[0].cells[0]
    set_cell_background(cell, 'CC0029')
    assert get_cell_background(cell) == 'CC0029'

    # Test 4: RTL formatting
    para = doc.add_paragraph()
    apply_rtl_to_paragraph(para, 'اختبار')
    assert para.paragraph_format.bidi == True
    assert para.alignment == WD_ALIGN_PARAGRAPH.RIGHT

    print("✅ All tests passed")

if __name__ == '__main__':
    test_rtl_translation()
```
