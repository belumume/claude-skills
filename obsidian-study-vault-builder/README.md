# Obsidian Study Vault Builder

> **Battle-tested skill for generating comprehensive, mobile-compatible Obsidian study vaults from academic course materials.**

Transform lecture slides, textbooks, and course materials into structured, exam-ready Obsidian vaults with checkpoint-based quality assurance and mobile-first design.

## What It Does

- **Structured organization** - Course map, chapter guides, cross-references, mock exams
- **Mobile-first design** - Mermaid + LaTeX only, no plugins required
- **Checkpoint workflow** - Progressive review catches errors early
- **Applied learning** - Scenario-based problems test understanding, not memorization
- **Comprehensive coverage** - Every lecture topic explained, no gaps
- **Consistent structure** - Same patterns across all chapters

## Battle-Tested

Validated on:
- 37 markdown files, 828KB content
- 8 course chapters, 80 practice problems
- 2 complete mock exams
- 100% mobile-compatible, zero rendering errors
- **Time saved:** ~80 hours of manual work

## Quick Start

```bash
# Install
cp -r obsidian-study-vault-builder ~/.claude/skills/

# Use with Claude Code
cd ~/obsidian-vault/school/
claude-code
```

Prompt Claude:
```
Build comprehensive study materials for my [Course Name] course.
Course location: /path/to/materials/
Use obsidian-study-vault-builder skill.
```

## What You Get

```
course-name/
├── 00-overview/        # Course map, schedule, strategy
├── 01-chapter-name/    # core-concepts.md, quick-ref.md, practice-problems.md
├── 02-chapter-name/    # Same structure for each chapter
├── cross-chapter/      # Comparisons, patterns, catalog
└── mock-exams/         # Practice tests with solutions
```

## Key Features

### 1. Checkpoint Workflow
Claude generates Chapter 1, STOPS for your review, then continues after approval.

### 2. Applied Understanding
Problems test application, not memorization. Real-world scenarios, not "Given array X..."

### 3. Systematic Error Fixing
When issue found: identify pattern → find ALL → fix ALL → verify zero remaining

## Mobile-Compatible

Works perfectly on any device:
- ✅ Mermaid diagrams (no external tools)
- ✅ LaTeX math notation
- ✅ Collapsible solution callouts
- ✅ Wiki-links for navigation
- ✅ NO plugins required

## FAQ

**Q: Works for non-CS subjects?**
A: Yes! Math, Physics, Chemistry, Business, Medicine - any structured course.

**Q: Can I customize output?**
A: Yes, ask Claude to use custom structure.

**Q: Time investment?**
A: 2-4 hours with Claude vs 60-80 hours manual.

## Example Output

### Sample Problem
```markdown
### Problem: Meeting Scheduler

**Difficulty:** ⭐⭐ Moderate

**Scenario:** You're building a scheduling system for 10,000 employees...

**Question:** Design an efficient algorithm to find common time slots...

> [!example]- Solution
>
> **Approach:** Use divide-and-conquer...
> **Complexity:** O(n·m log n)...
> **Why it's better:** Brute force is O(n·m^n) - exponential!
```

## Comparison

| Aspect | Manual | This Skill |
|--------|--------|------------|
| Time | 60-80 hours | 2-4 hours |
| Consistency | Varies | Perfect |
| Mobile | Often breaks | Always works |

## Contributing

**Open an issue or PR:** https://github.com/belumume/claude-skills

## License

MIT License - Free for personal and commercial use

---

**Ready to build your study vault?** 📚
