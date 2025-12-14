# document-quality-standards

Patterns from OpenAI skills that Anthropic's document-skills plugin lacks.

## What it adds

- Visual verification workflow (render → inspect → fix loop)
- Typography hygiene (U+2011 avoidance, ASCII hyphens)
- Extended spreadsheet color codes
- Helper cells over complex formulas
- Dynamic array function warnings

## Usage

Automatically discovered by Claude. Complements the official `xlsx`, `pdf`, `docx`, `pptx` skills.

## Dependencies

- poppler-utils (`pdftoppm`)
- libreoffice (`soffice`)
- openpyxl
