# Vault QA Checklist (companion to obsidian-vault-builder/SKILL.md)

Use before declaring a chapter / section / vault "complete." The CLI verifications below replace manual grep-based checks when the Obsidian app is running. Fall back to grep/manual when the app is closed.

## Content

- [ ] Every topic from source materials covered (cross-reference source outline against vault TOC)
- [ ] All key concepts explained with examples (no "TODO: add example" stubs)
- [ ] Complexity / cost / trade-off analysis included where domain applies
- [ ] Cross-references to related chapters present and resolving

## Format

- [ ] Navigation links present and working at the top of every main file
- [ ] Learning objectives stated (and CO-mapped if academic)
- [ ] Table of contents present for any file >500 lines
- [ ] All Mermaid diagrams render (preview them in Obsidian, not just markdown)
- [ ] All LaTeX formulas correct (inline `$...$` and block `$$...$$` render)
- [ ] All internal wiki-links resolve (`obsidian.com unresolved` returns clean)
- [ ] Collapsible solutions in practice files work (`[!example]-` form, blank line after marker)

## Structure

- [ ] Follows the standard file organization (see SKILL.md "Academic study vault scaffold" or PKM scaffold)
- [ ] Naming conventions consistent (kebab-case, no spaces in filenames)
- [ ] File paths correct (relative paths for portability)
- [ ] Mobile-compatible features only for shared content

## Quality (assessment alignment)

- [ ] Practice problems test application (not memorization — see SKILL.md "Applied understanding")
- [ ] Solutions show step-by-step reasoning, not just final answer
- [ ] Examples are clear and complete (a fresh reader can follow)
- [ ] No gaps in explanations (no "and you can show that..." hand-waves)

## CLI verification commands (run after build)

| Manual check | CLI replacement |
|---|---|
| `grep -r "TODO" *.md` | `obsidian.com search query=TODO path=<course>` |
| Manual link checking | `obsidian.com unresolved` (broken wiki-links across vault) |
| Count files manually | `obsidian.com files folder=<course> total` |
| Check frontmatter manually | `obsidian.com properties path=<file>` |
| Find disconnected files | `obsidian.com orphans` + `obsidian.com deadends` |
| Verify tags exist | `obsidian.com tags counts` |
| Search by content | `obsidian.com search query="<text>" path=<folder>` |

Requires Obsidian app running. Falls back to grep/manual if app is closed.

## Anti-patterns to avoid (final pass)

- Don't add features "because they're nice" — summary sections where not needed, exam-prep sections when a dedicated file exists, "standardizing" content that should vary by topic
- Don't assume consistency without checking — spot-checking 2 files doesn't guarantee all 8 match; different file types may have different patterns; user edits may have shifted some files since generation
- Don't batch completions — marking 3 todos complete at once looks like you forgot; update progress as you go
- Don't create AI slop — unnecessary praise, over-the-top validation, emoji overuse, bloated summaries
- Don't break elegance for features — quick-ref files naturally vary by content; not everything needs tables; simple beats complex

## Project template (reusable initial prompt structure)

When kicking off a new course-prep vault build, give the agent this context shape:

```markdown
COURSE CONTEXT:
- Course name and code
- Textbook and chapters ACTUALLY covered
- Exam timeline
- Assessment format and style

MATERIALS LOCATION:
- Folder structure
- File types (slides, textbook, assignments, lecture transcripts)
- Reference guides (visualization standards, course outcomes)

OBJECTIVES:
- Deep understanding (applied, not memorization)
- Comprehensive coverage (no gaps from source outline)
- Organized study system

QUALITY CONTROL:
Checkpoint-based (per SKILL.md):
1. Complete chapter 1 fully
2. STOP and show what was created + sample outputs + verification checklist
3. Wait for approval
4. Continue with brief status updates per chapter

FILE STRUCTURE:
Use SKILL.md "Academic study vault scaffold" + per-chapter trio.

FORMATTING STANDARDS:
- Follow visualization guide
- Universal Obsidian features only (no plugin-dependent rendering for shared content)
- Mobile-compatible
```
