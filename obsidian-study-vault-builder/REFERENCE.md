# Obsidian Study Vault Patterns - Learned Skills

**Purpose:** Reusable patterns and skills for creating academic study vaults with Claude Code
**Extracted from:** Academic vault projects across multiple subjects
**Status:** Battle-tested on 37-file vaults, 828KB content, multiple subjects (CS, engineering, business)

---

## Project Management Patterns

### Checkpoint-Based Workflow ✅ CRITICAL

**What it is:** Progressive review with human verification at key milestones

**How to use:**
1. Complete first chapter/module completely
2. STOP and show user:
   - What was created
   - Sample outputs
   - Verification checklist
3. Wait for approval before continuing
4. For subsequent work: brief status updates, full stop only if critical issues

**Why it works:**
- Catches structural issues before they compound
- Verifies approach matches user expectations
- Allows course corrections early (cheap) vs late (expensive)
- Builds trust for autonomous work later

**Example:** Chapter 5 was empty (20KB missing). Caught during review, not at end.

---

### Task Tracking Discipline

**Pattern:** Use TodoWrite proactively for multi-step work

**Rules:**
- Create todos at start of complex work
- ONE task in_progress at a time (not zero, not two)
- Mark completed IMMEDIATELY after finishing (no batching)
- Clear completed todos when done with phase
- Don't let todo list go stale

**Why:** Provides progress visibility to user, prevents forgetting steps, demonstrates systematic approach

---

### Memory File Hierarchy ✅ CRITICAL

**Structure:**
```
vault/
├── CLAUDE.md           # Vault-wide conventions
├── School/
│   ├── CLAUDE.md       # Academic work patterns
│   └── [course-name]/
│       └── CLAUDE.md   # Project-specific details
```

**What each level contains:**

**Root (vault/CLAUDE.md):**
- Vault organization principles
- Universal formatting standards
- Current projects (high-level status only)
- Cross-project patterns

**Category (School/CLAUDE.md):**
- Domain-specific conventions (academic vs personal vs work)
- Common patterns for that domain
- List of projects in category
- General workflow guidelines

**Project ([course-name]/CLAUDE.md):**
- Specific course information
- File inventory
- Session progress log
- Detailed status and accomplishments
- Project-specific decisions and rationale

**Why it works:**
- Prevents massive monolithic memory files
- Provides appropriate context at each level
- New projects inherit from parent, add specifics
- Easy to find relevant context

**When to update:** Keep timestamps synchronized across levels after major work

---

## Obsidian-Specific Patterns

### Universal Feature Set ✅ CRITICAL

**ALWAYS use these (work on desktop AND mobile):**
- ✅ Mermaid diagrams (flowcharts, graphs, trees)
- ✅ LaTeX math notation (`$inline$`, `$$block$$`)
- ✅ Standard markdown (tables, lists, code blocks)
- ✅ Obsidian wiki-links (`[[file#section]]`)
- ✅ Obsidian callouts (`> [!note]`, `> [!tip]`, `> [!warning]`, etc.)

**NEVER use these (plugin-dependent):**
- ❌ Dataview queries
- ❌ Custom CSS that breaks content
- ❌ Plugin-specific syntax
- ❌ External tools for diagrams
- ❌ Image files for math (use LaTeX)

**Why:** Mobile compatibility, future-proofing, universal accessibility

---

### Link Format Patterns

**Internal wiki-links (Obsidian native):**
- To file: `[[path/to/file|Display Text]]`
- To section: `[[#Section Name]]` (same file)
- To section in other file: `[[file#Section Name]]`
- Relative paths from current location: `[[../folder/file]]`

**Common mistakes:**
- ❌ Markdown links for internal navigation: `[Text](#section)`
- ❌ Wrong section names (must match heading exactly)
- ❌ Missing `../` for parent directory
- ❌ Using URL fragments instead of section names

**Fix pattern:** When TOC links break, use wiki-link format `[[#Heading]]` not markdown `[Text](#heading)`

---

### Mermaid Diagram Patterns

**Best practices:**
- Use ASCII equivalents for special chars that break parsing
- Test render before moving on
- Keep diagrams simple and clear
- Use consistent styling across vault

**Common issues and fixes:**

| Problem | Fix |
|---------|-----|
| `≤` breaks Mermaid | Use `<=` (ASCII) |
| `≥` breaks Mermaid | Use `>=` (ASCII) |
| `[text](value)` interpreted as link | Use `{text}(value)` (curly braces) |
| Special math symbols | Use ASCII equivalents or spell out |
| `&` renders as `&amp;` in **mindmaps only** | Use Unicode fullwidth `＆` (U+FF06) |
| `[1. Text]` triggers "Unsupported markdown: list" | Use `["Step 1:<br/>Text"]` with line break |

**Note on ampersands:** Known Mermaid bug (issue #6308, fixed in v11+ but Obsidian hasn't updated). Only affects mindmap diagrams - flowcharts/graphs render `&` correctly. Unicode fullwidth ampersand (＆) looks identical and bypasses the bug.

**Note on numbered lists in nodes:** Mermaid interprets `[1. Text]` as markdown ordered list syntax, which isn't supported in node labels. Use `["Step 1:<br/>Text"]` format instead, which follows vault's existing multi-line label convention and renders correctly.

**Example fix:** Changed 5 diagrams from Unicode math to ASCII (`Θ(n)` → `Theta(n)`)

---

### LaTeX in Tables Pattern

**Problem:** Pipe characters `|` in LaTeX break markdown tables

**Solution:** Escape pipes with backslash

**Example:**
```markdown
| Algorithm | Complexity |
|-----------|------------|
| DFS | $\Theta(\|V\| + \|E\|)$ |  ← Escaped pipes
```

**Pattern to search:** Any LaTeX containing `|V|`, `|E|`, absolute values, etc.

---

### Collapsible Solutions Pattern ✅ CRITICAL

**For practice problems, use collapsible Obsidian callouts:**

```markdown
### Problem 1: Title

**Question:** Problem statement here

> [!example]- Solution
>
> **Approach:** Strategy
>
> **Algorithm:** Step-by-step
>
> **Complexity:** Analysis
```

**Key elements:**
- `> [!example]-` for collapsible callout (note the minus)
- Blank line after `> [!example]-` before content
- Continue `>` prefix for all lines in callout

**Why:** Active learning - try problem before seeing solution

**Don't use:** HTML `<details>` tags (don't work in Obsidian)

---

## Content Quality Patterns

### Applied Understanding Focus ✅ CRITICAL

**For academic study materials:**

**DO:**
- Create scenario-based problems (real-world contexts)
- Ask "Describe approach to..." (design questions)
- Require "Analyze trade-offs..." (show work)
- Test "Why does this work?" (justification)
- Focus on pattern recognition (when to use technique X)

**DON'T:**
- Rehash textbook examples verbatim
- Test pure memorization
- Ask only for definitions
- Use multiple choice (unless exam format requires)

**Why:** Matches how academic assessments actually test (from HW01 analysis)

---

### Comprehensive Coverage Principle

**Rule:** Cover EVERY topic from lecture slides, no gaps

**Process:**
1. List all topics from slide headers
2. For each topic, create corresponding section
3. Cross-reference: did we explain everything mentioned?
4. Verify examples, algorithms, proofs all included

**Don't skip:** "Obvious" topics, brief slide mentions, examples

**Why:** Exam can test anything covered in class

---

### Cross-Reference Pattern

**Create connections between related concepts:**

```markdown
See also:
- [[../02-complexity-analysis/core-concepts#Master Theorem]]
- Compare with [[../08-dynamic-programming/core-concepts#Optimal Substructure]]
```

**When to cross-reference:**
- Related techniques (greedy vs DP)
- Prerequisites (master theorem for D&C analysis)
- Contrasts (DFS vs BFS)
- Applications (topological sort uses DFS)

**Why:** Builds connected understanding, not isolated facts

---

## Structural Consistency Patterns

### Standard File Structure ✅ CRITICAL

**For each chapter:**
```
01-chapter-name/
├── core-concepts.md      # Comprehensive guide (20-50KB)
├── quick-ref.md          # Condensed summary (2-5KB)
└── practice-problems.md  # 10 problems + solutions
```

**Every core-concepts.md must have:**
1. Title: `# Chapter X: Name`
2. Navigation: `[[../00-overview/course-map|← Back]] | [[quick-ref|Quick Ref →]]`
3. Divider: `---`
4. Learning Objectives: `## Learning Objectives (COX)`
5. Divider: `---`
6. Table of Contents: `## Table of Contents` (if file >500 lines)
7. Content sections
8. Cross-references

**Every practice-problems.md must have:**
1. Title with chapter name
2. Navigation links
3. Overview section
4. Table of Contents (if >10 problems)
5. Problem sets grouped by type
6. All solutions in collapsible callouts

**Why:** Consistency aids navigation, sets expectations, looks professional

**Example:** Chapters 1-4 were consistent, 5/8-10 needed standardization

---

### Navigation Link Pattern

**At top of every main file:**
```markdown
# Chapter Title

[[../00-overview/course-map|← Back to Course Map]] | [[quick-ref|Quick Reference →]]

---
```

**Rules:**
- Always provide way back to course map
- Link to related files (quick-ref, practice)
- Use relative paths from current location
- Test links work after creating

---

### Learning Objectives Pattern

**For each chapter, tie to course outcomes:**

```markdown
## Learning Objectives (CO4)

> [!note] Course Outcome CO4
> **Compose problem-solving approaches to solve problems**
>
> By the end of this chapter, you should be able to:
> - Identify problems suitable for divide-and-conquer
> - Apply merge sort and quick sort correctly
> - Analyze time complexity using recurrence relations
> - Design new problem-solving approaches
```

**Structure:**
- Course outcome number and summary
- Callout for emphasis
- Specific, measurable learning goals
- Match course plan language

---

## Error Pattern Recognition

### Common Obsidian Rendering Issues

**Pattern 1: Unicode Corruption**
- **Symptom:** � (question marks) in rendered text
- **Cause:** Character encoding issues (copy/paste from slides)
- **Fix:** Replace with proper Unicode or ASCII equivalents
- **Search pattern:** `grep "�" file.md`

**Pattern 2: Broken Tables**
- **Symptom:** Raw pipes and dashes visible
- **Cause:** Missing blank line before table
- **Fix:** Add blank line before table markdown
- **Prevention:** Always put blank line before tables

**Pattern 3: Unintended Links**
- **Symptom:** Blue underlined text, "Unable to find" error
- **Cause:** `[text](value)` interpreted as markdown link
- **Fix:** Change to `{text}(value)` or escape brackets
- **Common locations:** Huffman coding notation, set notation

**Pattern 4: Non-Working Collapsibles**
- **Symptom:** `<details>` and `<summary>` tags visible in text
- **Cause:** HTML details don't work in Obsidian
- **Fix:** Convert to `> [!example]- Solution` callouts
- **Search pattern:** `grep "<details>" file.md`

---

### Systematic Fix Approach ✅ CRITICAL

**When user reports an error:**

1. **Understand the pattern** (not just the one instance)
2. **Search for all instances** (`grep` pattern across files)
3. **Fix all occurrences** (not just the reported one)
4. **Verify completeness** (re-grep to confirm zero results)
5. **Document the pattern** (add to memory for future)

**Example from Example:**
- User showed LaTeX pipes breaking one table
- We grep'd for all `|V|` and `|E|` in file
- Fixed all instances with `\|V\|` and `\|E\|`
- Verified with grep (zero results)

**Why:** Prevents user finding same error 10 more times. Demonstrates thoroughness.

---

## Scale Management Patterns

### When to Use Task Agents

**Use Task tool with subagent_type=Explore for:**
- Large codebase exploration ("Where are errors handled?")
- Multi-file pattern search ("Find all instances of X")
- Structural analysis ("What's the codebase organization?")
- NOT needle queries (specific file/class/function name)

**Use Task tool with subagent_type=general-purpose for:**
- Multi-step complex tasks
- Research requiring multiple searches
- When uncertain about finding match in first few tries

**Don't use Task tool for:**
- Reading specific known file path (use Read)
- Searching for specific class definition (use Glob)
- Simple single-step operations

**Why:** Task agents have more autonomy but cost more. Use for genuinely complex work.

---

### Parallel Tool Calls Pattern

**When operations are independent, call tools in parallel:**

```markdown
Good (parallel):
- Read file A
- Read file B
- Read file C
(All in one message, three tool calls)

Bad (sequential):
- Read file A
- [wait for response]
- Read file B
- [wait for response]
```

**When NOT to parallel:**
- Operations depend on previous results
- Need to decide based on what you find
- Editing requires understanding file first (Read, THEN Edit)

---

## Communication Patterns

### Trust Signals from User

**When user says:**
- "do what's objectively best" → They trust your judgment, be proactive
- "no slop, no bloat" → They want elegant minimalism, don't over-add
- "confirm you're preserving elegance" → Quality over quantity
- "I only inspected or observed" → Expect you to do thorough review

**How to respond:**
- Verify structural consistency before claiming complete
- Check ALL similar files, not just samples
- Don't add "nice to have" features
- Focus on actual problems, not cosmetic improvements

---

### Screenshot-Driven Debugging

**When user provides screenshots:**
1. Look at what they're highlighting (exact issue)
2. Reproduce in your understanding (read that section)
3. Identify the pattern (not just that instance)
4. Fix systematically (all occurrences)
5. Confirm fix (describe what you changed)

**Don't:**
- Guess what they're showing
- Fix only what's visible in screenshot
- Assume it's isolated

**Example:**
- User showed broken Big-Theta diagram → fixed all 3 bound diagrams
- User showed � characters → fixed ALL Unicode in file
- User showed broken table → fixed ALL tables in file

---

## Course-Specific Patterns

### Analyzing Course Plan Document

**What to extract:**
1. **Chapters covered** (actual vs textbook)
2. **Course outcomes** (CO1, CO2, etc.) and mapping
3. **Assessment breakdown** (weights, formats)
4. **Timeline** (which weeks cover what)

**Critical:** Some courses skip textbook chapters - verify actual coverage

**Example error:** Assumed chapters 1-10 sequential. Actually 1-5, 8-10 (no 6-7).

---

### Exam Style Matching

**Analyze sample assessments (HW, quizzes) to determine:**
- Question formats (design, analysis, explanation)
- Depth expected (memorization vs application)
- Showing work requirements
- Real-world scenario emphasis

**Create practice problems matching that style**

**Key insight:** Instructor tests applied understanding (scenario-based), not definitions

---

## Quality Assurance Checklist

### Before Marking Chapter Complete

**Content:**
- [ ] Every slide topic covered
- [ ] All key concepts explained with examples
- [ ] Complexity analysis included
- [ ] Cross-references to related chapters

**Format:**
- [ ] Navigation links present and working
- [ ] Learning objectives stated
- [ ] Table of contents (if file >500 lines)
- [ ] All Mermaid diagrams render
- [ ] All LaTeX formulas correct
- [ ] All internal links resolve
- [ ] Collapsible solutions work

**Structure:**
- [ ] Follows standard file organization
- [ ] Naming conventions consistent
- [ ] File paths correct
- [ ] Mobile-compatible features only

**Quality:**
- [ ] Practice problems test application
- [ ] Solutions show step-by-step reasoning
- [ ] Examples are clear and complete
- [ ] No gaps in explanations

---

## Anti-Patterns (What NOT to Do)

❌ **Don't add features "because they're nice"**
- Summary sections where not needed
- Exam prep sections when dedicated file exists
- "Standardizing" content that should vary by topic

❌ **Don't assume consistency without checking**
- Spot-checking 2 files doesn't guarantee all 8 match
- Different file types may have different patterns
- User edits may have changed some files

❌ **Don't batch completions**
- Marking 3 todos complete at once looks like you forgot
- Update progress as you go
- Immediate feedback builds confidence

❌ **Don't create AI slop**
- Unnecessary praise ("You're absolutely right!")
- Over-the-top validation
- Emoji overuse (unless user requests)
- Bloated summaries

❌ **Don't break elegance for features**
- Quick-ref files naturally vary by content (that's good)
- Not everything needs tables
- Simple is better than complex

---

## Project Template (Reusable)

### Initial Prompt Structure

```markdown
COURSE CONTEXT:
- Course name and code
- Textbook and chapters ACTUALLY covered
- Exam timeline
- Assessment format and style

MATERIALS LOCATION:
- Folder structure
- File types (slides, textbook, assignments)
- Reference guides (visualization standards)

OBJECTIVES:
- Deep understanding (applied, not memorization)
- Comprehensive coverage (no gaps)
- Organized study system

QUALITY CONTROL:
Checkpoint-based:
1. Complete Chapter 1 fully
2. STOP and show:
   - What was created
   - Sample outputs
   - Verification checklist
3. Wait for approval
4. Continue with brief status updates per chapter

FILE STRUCTURE:
[Specify exact organization]

FORMATTING STANDARDS:
- Follow visualization guide
- Universal Obsidian features only
- Mobile-compatible
```

---

## Success Metrics

**How to know if vault is ready:**

✅ **Completeness:**
- All lecture topics covered
- No gaps from slides
- Cross-chapter resources present
- Mock exams created

✅ **Consistency:**
- Same structure across chapters
- Navigation works throughout
- Formatting uniform
- Links all resolve

✅ **Quality:**
- Mermaid renders correctly
- LaTeX displays properly
- Solutions are collapsible
- Examples are clear

✅ **Usability:**
- Mobile-accessible
- Quick-ref available
- Study schedule present
- TOCs for navigation

✅ **Accuracy:**
- Technical content correct
- Complexity analysis accurate
- Examples work through properly
- No broken concepts

---

## Future Improvements

**For next study vault project:**

1. **Define structure template FIRST** (before any content)
2. **Apply template to all chapters** (consistency from start)
3. **Automate verification** (checklist per chapter)
4. **Test mobile early** (catch rendering issues sooner)
5. **Document decisions** (why we chose X over Y)

**Potential automation:**
- Script to verify all chapters have required sections
- Lint for common formatting errors
- Link checker for internal references
- Mermaid syntax validator

---

## Related Resources

- `obsidian-visualization-resource-v3.md` - Formatting standards
- `school/[course-name]/CLAUDE.md` - Detailed project case study
- `school/CLAUDE.md` - Academic work patterns

---

**Last Updated:** 2025-11-10
**Status:** Validated on academic vault projects across multiple subjects
**Next Use:** Apply patterns to next course study vault
