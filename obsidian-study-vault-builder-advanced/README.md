# Obsidian Study Vault Builder - Advanced

> **Comprehensive battle-tested patterns for academic study vault generation in Obsidian**

Advanced skill with complete error patterns, systematic fix workflows, quality checklists, and lessons learned from real-world projects. Targets CS students and power users building large-scale study vaults (20+ files, 500KB+).

## What's Different from the General Version?

| Feature | General Version | Advanced Version |
|---------|----------------|------------------|
| **Target Users** | All students, quick projects | CS students, power users, large projects |
| **Content** | Core workflow (35 lines) | Complete patterns (750+ lines) |
| **Error Patterns** | None | 8 documented with fixes |
| **Quality Checklists** | Basic | Comprehensive (50+ items) |
| **Fix Workflows** | Generic | Systematic 5-step approach |
| **Examples** | High-level | Real file paths, actual errors |
| **Memory Patterns** | Not covered | Three-level hierarchy documented |
| **When to Use** | Simple projects | Complex projects, quality-critical work |

## Battle-Tested Results

This skill is extracted from a completed Algorithms final exam preparation project:

**Validated on:**
- 37 markdown files
- 828KB of content
- 8 course chapters
- 80 practice problems with solutions
- 2 complete mock exams
- 100% mobile-compatible
- Zero rendering errors
- ~80 hours manual work saved

**Patterns documented:**
- 8 error types with systematic fixes
- 5-step fix workflow
- 50+ quality checklist items
- Checkpoint-based generation workflow
- Memory file hierarchy (3 levels)
- Cross-reference patterns
- Applied understanding principles

## When to Use This Skill

### Choose Advanced Version When:

- Building vault with **20+ files**
- Content size **500KB+**
- Need **zero rendering errors** (exam-critical material)
- Want **systematic error prevention** before issues appear
- Preparing for **high-stakes assessments** (finals, comps)
- Building **multi-chapter** comprehensive coverage
- Need **quality assurance** workflows
- Want **checkpoint-based** progressive review

### Choose General Version When:

- Quick reference vault (5-10 files)
- Single topic/module
- Exploratory project
- Don't need comprehensive error patterns
- Time-constrained (< 2 hours)

## Key Patterns Included

### 1. Checkpoint-Based Workflow

**Never generate all chapters upfront.** Progressive validation:

1. Generate Chapter 1 only → **STOP**
2. User reviews format, structure, quality
3. Fix any issues (cheap at 1 chapter)
4. Continue with Chapters 2-N using validated pattern

**Time saved:** 5+ hours of rework prevented

**Documented:**
- When to stop
- What to review
- How to validate
- When to continue

### 2. Error Pattern Recognition (8 Patterns)

Each pattern includes:
- **Symptom** - How to detect
- **Diagnosis** - How to find all occurrences
- **Fix** - Exact solution
- **Systematic approach** - Fix everything, not just one

**Patterns documented:**

1. **Unicode corruption in Mermaid** - `≤` → `<=`, `∞` → `infinity`
2. **Broken tables (LaTeX pipes)** - `$|V|$` → `$\\|V\\|$` in tables
3. **Missing collapsible solutions** - Add `> [!example]- Solution`
4. **Inconsistent navigation** - Standard template for all files
5. **Missing learning objectives** - Add to every core-concepts.md
6. **Inconsistent TOC** - Format once, apply everywhere
7. **Empty core concepts** - Detect with `find . -size -10k`, fix with comprehensive rewrite
8. **Broken cross-references** - Section name mismatches

**Real examples from actual project included.**

### 3. Systematic Fix Approach (5 Steps)

When any error found:

1. **Identify pattern** - Is this recurring?
2. **Search ALL occurrences** - `grep -r` patterns provided
3. **Fix everything** - Not just one instance
4. **Verify zero remaining** - Confirm with grep
5. **Update checklist** - Document for future

**Prevents:** Partial fixes, missed instances, recurring problems

### 4. Memory File Hierarchy

Three-level context structure:

**Level 1: Root** (`obsidian/CLAUDE.md`)
- Vault-wide conventions
- Universal formatting (Mermaid, LaTeX, callouts)

**Level 2: School** (`obsidian/School/CLAUDE.md`)
- Academic-specific patterns
- Study philosophy
- Exam prep approaches

**Level 3: Project** (`obsidian/School/algorithms/CLAUDE.md`)
- Course-specific details
- File inventory
- Status tracking
- Specific fixes applied

**Benefits:**
- Appropriate detail at each scope
- No redundant information
- Scales to multiple courses
- Easy maintenance

### 5. Quality Assurance Checklist (50+ Items)

**Structural Consistency:**
- [ ] All core-concepts have Navigation
- [ ] All files have Learning Objectives
- [ ] All files have TOC
- [ ] All solutions are collapsible

**Content Completeness:**
- [ ] Every lecture topic covered
- [ ] All algorithms documented
- [ ] All examples included
- [ ] Cross-references present

**Format Correctness:**
- [ ] No Unicode in Mermaid
- [ ] All LaTeX pipes escaped
- [ ] All links work
- [ ] All anchors match headings

**Mobile Compatibility:**
- [ ] No plugin dependencies
- [ ] Mermaid for diagrams
- [ ] LaTeX for math
- [ ] Universal features only

**Assessment Alignment:**
- [ ] Practice matches exam style
- [ ] Mock exams mirror format
- [ ] Questions require reasoning
- [ ] Solutions show work

### 6. Applied Understanding Principle

**Bad questions (memorization):**
- "What is the time complexity of binary search?"
- "List the steps of merge sort"
- "Define divide and conquer"

**Good questions (applied understanding):**
- "Design a customer lookup system for 1M records. Current linear search takes 5s. Describe algorithm to reduce to milliseconds. Analyze complexity and justify choice."
- "Your video streaming service buffers too often. Propose caching algorithm. Analyze trade-offs between LRU, LFU, MRU. Which would you choose and why?"

**Components:**
1. Real-world context
2. Constraints
3. Multiple steps (describe, analyze, justify)
4. Reasoning required

**Why:** Matches actual exam style, tests understanding, prepares for interviews

### 7. Obsidian-Specific Best Practices

**Universal features only (mobile-first):**
- ✅ Mermaid diagrams (not images)
- ✅ LaTeX math (not images)
- ✅ Standard callouts (6 types)
- ✅ Internal wiki-links
- ✅ Markdown tables
- ❌ No plugins
- ❌ No custom callout types
- ❌ No external dependencies

**Why:** Students study on phones/tablets. Plugin-free = works everywhere.

**Documented:**
- Link format patterns (relative vs absolute)
- Mermaid special character handling
- LaTeX escaping in tables
- Collapsible solution format
- Cross-reference patterns

### 8. Comprehensive Coverage Principle

**Every topic from lectures must appear in vault:**

1. Scan all lecture slides
2. Extract every algorithm (even briefly mentioned)
3. Include all examples from instructor
4. Cover edge cases discussed
5. Match assessment style

**Validation:**
- Cross-reference lecture outline with vault TOC
- Check every algorithm appears in catalog
- Verify practice problems cover all topics
- No gaps where lectures covered but vault silent

**Example documented:** Even minor algorithms (Cocktail Shaker Sort) must be included.

## Installation

```bash
# Clone the repository
git clone https://github.com/belumume/claude-skills.git

# Install advanced skill locally
cp -r claude-skills/obsidian-study-vault-builder-advanced ~/.claude/skills/

# Verify installation
ls ~/.claude/skills/obsidian-study-vault-builder-advanced/
# Should show: SKILL.md, README.md
```

## Usage

### Basic Usage

```
Build comprehensive study materials for my Data Structures course.

Use the obsidian-study-vault-builder-advanced skill.

Course location: /courses/ds/
Exam: 3 months
Course has: 12 chapters, weekly lectures, scenario-based exams

Requirements:
- Zero rendering errors (exam-critical)
- Complete coverage of all lecture topics
- Mobile-compatible (study on phone)
- Checkpoint review after Chapter 1
```

### With Specific Requirements

```
Generate Algorithms study vault with advanced patterns.

Use obsidian-study-vault-builder-advanced skill.

Materials: C:\IU\Level 6\Algorithms\
Chapters: 1-5, 8-10 (skip 6-7 per syllabus)
Timeline: 1 month until final exam
Exam style: "Describe/Analyze/Explain" questions, show work

Apply:
- Systematic error prevention
- Quality checklist verification
- Checkpoint after Chapter 1
- Applied understanding in practice problems
```

### After Previous General Session

```
I previously used obsidian-study-vault-builder for a quick vault.
Now I need to upgrade it to zero-error quality for final exam.

Use obsidian-study-vault-builder-advanced skill.

Apply:
- Error pattern recognition (scan all files)
- Systematic fix workflow
- Quality assurance checklist
- Mobile compatibility verification
```

## What You Get

### File Structure

```
course-name/
├── 00-overview/
│   ├── course-map.md          # Visual course structure
│   ├── study-schedule.md      # Timeline-based plan
│   └── exam-strategy.md       # Assessment approach
│
├── 01-chapter-name/
│   ├── core-concepts.md       # Comprehensive (20-50KB)
│   ├── quick-ref.md           # Condensed (2-5KB)
│   └── practice-problems.md   # 10+ problems + collapsible solutions
│
├── cross-chapter/
│   ├── algorithm-catalog.md   # All algorithms (25+)
│   ├── complexity-cheatsheet.md
│   ├── pattern-recognition.md
│   └── comparisons.md
│
└── mock-exams/
    ├── mock-exam-01.md
    └── mock-exam-01-solutions.md
```

### Quality Guarantees

With advanced skill applied:

- **Zero rendering errors** - All Mermaid/LaTeX/tables work
- **All links functional** - No broken cross-references
- **Consistent structure** - Same patterns across all files
- **Mobile-compatible** - Works on any device
- **Complete coverage** - Every lecture topic included
- **Applied problems** - Scenario-based, matches exam style
- **Collapsible solutions** - Active recall enabled

## Comparison: General vs Advanced

| Metric | General | Advanced |
|--------|---------|----------|
| **SKILL.md Size** | 35 lines | 750+ lines |
| **Error Patterns** | None | 8 documented |
| **Fix Workflows** | Generic | 5-step systematic |
| **Quality Checklist** | Basic | 50+ items |
| **Real Examples** | None | Actual file paths |
| **Time Investment** | 1-2 hours | 2-4 hours (includes QA) |
| **Output Quality** | Good | Zero-error |
| **Best For** | Quick projects | Exam-critical work |
| **Rework Risk** | 10-20% | < 5% |

## Real-World Example

**Project:** Algorithms CCS 3302 Final Exam Preparation

**Input:**
- 8 lecture chapters (100+ slides)
- Textbook sections
- Course plan with outcomes
- Past exam samples

**Process with Advanced Skill:**

1. **Chapter 1 generated** (30 min)
   - core-concepts.md (28KB)
   - quick-ref.md (2KB)
   - practice-problems.md (10 problems)

2. **Checkpoint review** (15 min)
   - User verifies format, structure, quality
   - Catches Unicode in Mermaid early
   - Validates applied understanding approach
   - Approves to continue

3. **Chapters 2-8 generated** (90 min)
   - Uses validated pattern
   - No format issues propagate
   - Systematic application

4. **Quality assurance** (30 min)
   - Run error pattern searches
   - Fix all instances systematically
   - Verify checklist (50+ items)
   - Test in Obsidian mobile

**Output:**
- 37 files, 828KB content
- 80 practice problems with solutions
- 2 mock exams
- 25+ algorithms documented
- Zero rendering errors
- 100% mobile-compatible

**Time:** 2.5 hours vs 80 hours manual

**Quality:** Exam-ready immediately, no rework needed

## Common Questions

**Q: Do I need both general and advanced skills?**

A: No. Install one:
- **General** - Quick projects, learning, exploration
- **Advanced** - Serious projects, exam prep, zero-error requirements

**Q: Can I upgrade from general to advanced mid-project?**

A: Yes. Run error pattern scans, apply systematic fixes, use quality checklist.

**Q: How much longer does advanced workflow take?**

A: +30-60 min for QA, but saves 3-5 hours of rework. Net: faster overall.

**Q: Is advanced overkill for small projects?**

A: Yes. For 5-10 file vaults, general version is sufficient.

**Q: What if I find new error patterns?**

A: Document them, update this skill, contribute back. Use `skills-extraction-meta-prompt.md`.

## Contributing

Found a new error pattern? Improved a workflow?

1. Document the pattern:
   - Symptom (how to detect)
   - Diagnosis (how to find all)
   - Fix (exact solution)
   - Systematic approach

2. Create PR: https://github.com/belumume/claude-skills

3. Include:
   - Real example from your project
   - Before/after
   - Grep patterns for searching

## License

MIT License - Free for personal and academic use

---

**Ready to build exam-critical study vaults with comprehensive error prevention and quality assurance built in.**
