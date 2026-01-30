#!/usr/bin/env python3
"""
Global PDF Extraction Tool for Claude Code
Extracts text (with page markers) and images from PDFs safely.

Usage:
    python pdf_extract.py <pdf_path> [--text-only] [--images-only]

Output:
    <pdf_name>.txt        - Text with PAGE markers
    <pdf_name>_images/    - PNG images per page
    <pdf_name>_index.txt  - Page index with content summaries
"""

import sys
import argparse
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERROR: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def extract_pdf(pdf_path: Path, text: bool = True, images: bool = True):
    """Extract text and/or images from a PDF with page correlation."""

    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        sys.exit(1)

    if pdf_path.suffix.lower() != ".pdf":
        print(f"ERROR: Not a PDF file: {pdf_path}")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    base = pdf_path.with_suffix("")
    page_count = len(doc)

    print(f"Processing: {pdf_path.name} ({page_count} pages)")

    # Extract text with page markers
    if text:
        txt_path = base.with_suffix(".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            for i, page in enumerate(doc, 1):
                f.write(f"\n{'=' * 60}\n")
                f.write(f"PAGE {i} of {page_count}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(page.get_text())
        print(f"  Text: {txt_path.name}")

    # Extract images
    if images:
        img_dir = Path(f"{base}_images")
        img_dir.mkdir(exist_ok=True)
        for i, page in enumerate(doc, 1):
            img_path = img_dir / f"page-{i:03d}.png"
            pix = page.get_pixmap(dpi=150)
            pix.save(img_path)
        print(f"  Images: {img_dir.name}/ ({page_count} pages)")

    # Create index file (maps pages to first line of content)
    index_path = Path(f"{base}_index.txt")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"PDF: {pdf_path.name}\n")
        f.write(f"Pages: {page_count}\n")
        f.write(f"Text file: {base.name}.txt\n")
        f.write(f"Images folder: {base.name}_images/\n")
        f.write(f"\n{'=' * 60}\n")
        f.write("PAGE INDEX (first 100 chars of each page):\n")
        f.write(f"{'=' * 60}\n\n")
        for i, page in enumerate(doc, 1):
            text_preview = page.get_text()[:100].replace("\n", " ").strip()
            f.write(f"Page {i:3d}: {text_preview}...\n")
            if images:
                f.write(f"         -> {base.name}_images/page-{i:03d}.png\n")
    print(f"  Index: {index_path.name}")

    doc.close()
    print("Done.")


def main():
    parser = argparse.ArgumentParser(description="Extract text and images from PDF")
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--text-only", action="store_true", help="Extract only text")
    parser.add_argument(
        "--images-only", action="store_true", help="Extract only images"
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()

    if args.text_only:
        extract_pdf(pdf_path, text=True, images=False)
    elif args.images_only:
        extract_pdf(pdf_path, text=False, images=True)
    else:
        extract_pdf(pdf_path, text=True, images=True)


if __name__ == "__main__":
    main()
