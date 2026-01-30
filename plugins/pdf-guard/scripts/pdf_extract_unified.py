#!/usr/bin/env python3
"""
Unified PDF Extraction - Creates a single markdown file with text and
inline image references at their exact positions.

Usage:
    python pdf_extract_unified.py <pdf_path>

Output:
    <pdf_name>_unified.md  - Markdown with text + image refs in context
    <pdf_name>_images/     - PNG images per page
"""

import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_unified(pdf_path: Path):
    """Create unified markdown with text and inline image references."""

    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    base = pdf_path.with_suffix("")
    page_count = len(doc)
    img_dir = Path(f"{base}_images")
    img_dir.mkdir(exist_ok=True)

    print(f"Processing: {pdf_path.name} ({page_count} pages)")

    unified_path = Path(f"{base}_unified.md")
    with open(unified_path, "w", encoding="utf-8") as f:
        f.write(f"# {pdf_path.stem}\n\n")
        f.write(f"*Extracted from: {pdf_path.name} ({page_count} pages)*\n\n")
        f.write("---\n\n")

        for i, page in enumerate(doc, 1):
            # Save page image
            img_path = img_dir / f"page-{i:03d}.png"
            pix = page.get_pixmap(dpi=150)
            pix.save(img_path)

            # Get text and detect if page has significant images/diagrams
            text = page.get_text()
            has_images = len(page.get_images()) > 0
            has_drawings = len(page.get_drawings()) > 5  # drawings = vector graphics

            # Write page header
            f.write(f"## Page {i}\n\n")

            # If page has diagrams/images, show image reference FIRST
            if has_images or has_drawings:
                rel_img = img_path.relative_to(pdf_path.parent)
                f.write(f"**[Visual content on this page - see: {rel_img}]**\n\n")

            # Write text content
            if text.strip():
                # Clean up text (remove excessive whitespace)
                cleaned = "\n".join(
                    line.strip() for line in text.split("\n") if line.strip()
                )
                f.write(f"{cleaned}\n\n")
            else:
                f.write("*[No text content - page is primarily visual]*\n\n")

            f.write("---\n\n")

    doc.close()
    print(f"  Unified: {unified_path.name}")
    print(f"  Images:  {img_dir.name}/ ({page_count} pages)")
    print("Done.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python pdf_extract_unified.py <pdf_path>")
        sys.exit(1)

    pdf_path = Path(sys.argv[1]).resolve()
    extract_unified(pdf_path)


if __name__ == "__main__":
    main()
