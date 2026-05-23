# Academic study vault scaffold (course prep + exam-ready content)

For course-prep vaults (lecture notes, exam-ready material, mock exams), the standard PKM scaffold is wrong shape. Use this proven scaffold instead. Folded from the deprecated `obsidian-study-vault-builder` skill 2026-05-15; battle-tested on 37-file/828KB academic vaults.

## Standard study vault structure

```
course-name/
├── 00-overview/              # Course map, schedule, exam strategy
│   ├── course-map.md         # Master TOC: chapters + cross-chapter links
│   ├── schedule.md           # Lecture/assessment dates
│   └── exam-strategy.md      # Topic priorities, instructor patterns
├── 01-chapter-name/          # One folder per chapter
│   ├── core-concepts.md      # Comprehensive guide (20-50KB)
│   ├── quick-ref.md          # Condensed summary (2-5KB)
│   └── practice-problems.md  # 10 problems + collapsible solutions
├── 02-chapter-name/          # Same per-chapter trio
├── cross-chapter/            # Topic comparisons that span chapters
│   ├── pattern-catalog.md    # Reusable patterns
│   └── exam-style-mapping.md # Which patterns appear in which exam style
└── mock-exams/               # Past papers + simulated tests
    ├── 2026-midterm-1.md
    └── 2026-final-practice.md
```

Why this shape:
- `00-overview/course-map.md` is the entry point; every chapter file links back here
- Per-chapter trio gives three reading depths (deep / quick / applied)
- `cross-chapter/` lifts comparisons out of any single chapter (they belong to none)
- `mock-exams/` is the rehearsal layer for exam-style alignment

## Per-chapter file structure (universal)

Each `01-chapter-name/` follows this pattern. The structure is required for the cross-chapter cross-references in patterns above to work consistently.

**`core-concepts.md` must contain (in order):**
1. Title: `# Chapter X: Name`
2. Navigation: `[[../00-overview/course-map|← Back]] | [[quick-ref|Quick Ref →]]`
3. Divider: `---`
4. Learning Objectives: `## Learning Objectives (COX)` block
5. Divider: `---`
6. Table of Contents: `## Table of Contents` (if file >500 lines)
7. Content sections with examples
8. Cross-references to other chapters

**`quick-ref.md` must contain:**
1. Title + navigation back to `core-concepts.md`
2. Condensed key concepts (no examples, no explanations — just what + when)
3. Quick-lookup tables (complexities, formulas, rules)

**`practice-problems.md` must contain:**
1. Title with chapter name
2. Navigation links back to `core-concepts.md` and `quick-ref.md`
3. Overview section
4. Table of Contents (if >10 problems)
5. Problem sets grouped by type
6. All solutions in collapsible callouts (`> [!example]-`)

## Academic content patterns

Three patterns universal for any course-prep vault:

### Navigation link pattern

Every chapter file starts with the same shape, providing reader orientation:

```markdown
# Chapter Title

[[../00-overview/course-map|← Back to Course Map]] | [[quick-ref|Quick Reference →]]

---
```

Rules:
- Always provide a way back to course map (anchor of the vault)
- Link to sibling files (quick-ref, practice)
- Use relative paths from current location
- Test links work via `obsidian.com unresolved` after creating

### Learning objectives pattern (CO mapping)

University courses typically map to Course Outcomes (CO1, CO2, ...). Tie each chapter to its CO so the vault doubles as an exam-prep matrix:

```markdown
## Learning Objectives (CO4)

> [!note] Course Outcome CO4
> **Compose problem-solving approaches to solve problems**
>
> By the end of this chapter, you should be able to:
> - Identify problems suitable for divide-and-conquer
> - Apply the algorithm with correct complexity analysis
> - Compare divide-and-conquer vs dynamic-programming trade-offs
```

For non-university content (textbook chapters, self-study), substitute "Learning Objectives" without the CO label.

### Applied understanding (not memorization)

Practice problems should test application, not recall. Question patterns that work:

- "Design [system] for [context]. Current [problem]. Describe solution to achieve [goal]. Analyze trade-offs and justify."
- "Given [scenario], which algorithm is appropriate and why? Compare against the alternative."
- "Trace [algorithm] on [input], showing state at each step."

Adapts to subject domain:
- CS: Algorithm design scenarios
- Medicine: Case-based diagnosis
- Business: Strategic analysis
- Physics: Experimental design
- Math: Proof-construction or counterexample

Avoid: "Define X." "What is Y?" "List the steps of Z." These test memorization, fail to predict exam performance, and bore the student.

## Comprehensive coverage principle

Every topic from source materials must appear in the vault. Coverage gaps cause exam-day surprises. Validation:

1. Extract source outline (textbook TOC, syllabus, lecture index)
2. Cross-reference against vault TOC
3. Diff produces gap list
4. Build out the gaps before declaring "complete"

Concrete: `comm -23 <(sort source-outline.txt) <(sort vault-toc.txt)` returns topics in source NOT in vault.

## CLAUDE.md layering within a vault

Per the official Claude Code memory model (https://code.claude.com/docs/en/memory), CLAUDE.md files are loaded by walking up the directory tree from cwd; all discovered files concatenate into context (they don't override each other). Subdirectory CLAUDE.md files lazy-load when Claude reads files there.

Practical application for vaults spanning multiple knowledge domains: layer CLAUDE.md files at appropriate depths.

- Vault-root CLAUDE.md: vault conventions (folder structure principles, universal-features discipline, plugin philosophy, naming rules)
- Category folder CLAUDE.md (e.g., `Projects/CLAUDE.md`, `Reference/CLAUDE.md`): domain-specific patterns
- Project folder CLAUDE.md: project-specific facts (deadlines, collaborators, source materials)

Official guidance recommends keeping each CLAUDE.md under 200 lines. For path-scoped rules, `.claude/rules/*.md` with `paths` frontmatter is an alternative to nested CLAUDE.md.
