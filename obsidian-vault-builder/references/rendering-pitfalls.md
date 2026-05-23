# Common Obsidian rendering pitfalls (writing markdown to a vault)

When generating markdown content for an Obsidian vault, these are the recurring rendering issues. Patterns extracted from a deprecated companion skill (`obsidian-study-vault-builder`, removed via PR #6 and re-validated 2026-05-15: over-triggered on exam-prep prompts and was structurally misaligned with the interactive-practice approach). The durable patterns below apply to ANY agent writing markdown to a vault, not just academic builds.

## Mermaid diagrams

- `[1. Text]` triggers "Unsupported markdown: list" error in node labels. Use `["Step 1:<br/>Text"]` (quoted with HTML break).
- `[text](value)` inside node labels is interpreted as link syntax. Use `{text}(value)` (curly braces).
- Special-character parsing edge cases persist in some Mermaid v11.x diagram types (sankey, etc.). For mindmap `&` (Mermaid issue #6308) and mindmap `<`/`>` (issue #6396), both fixed in v11.4+ and current Obsidian (1.12.x) bundles a fixed version. Older Obsidian releases may still need ASCII `<=`/`>=` substitution and Unicode fullwidth `＆` workaround.
- Diagnose via `grep -r "≤\|≥\|∞\|∈\|≠" *.md` if targeting older Obsidian.

## LaTeX in markdown tables

Pipe characters `|` in LaTeX break markdown table parsing.

```markdown
| Algorithm | Complexity |
|-----------|------------|
| DFS       | $\Theta(\|V\| + \|E\|)$  | <- escaped pipes
```

Search pattern: `grep -r "| \\$.*|.*\\$" *.md` to find unescaped pipes inside LaTeX inside table cells.

## Wiki-link vs markdown-link conventions

For internal vault navigation, use wiki-link form, NOT markdown link form:

- Same-file section: `[[#Section Name]]` (NOT `[Section](#section)`)
- Other-file section: `[[file#Section Name]]`
- Display text override: `[[file|Display Text]]`
- Relative path to parent: `[[../folder/file]]`

Markdown links to internal sections often break in Obsidian's renderer; wiki-links resolve via the link index.

## Collapsible callouts for active-learning content

For any content where the reader should attempt before seeing the answer (practice problems, quiz questions, exercises), use a collapsible callout:

```markdown
### Problem 1: Title

**Question:** Statement here.

> [!example]- Solution
>
> **Approach:** strategy
>
> **Algorithm:** step-by-step
>
> **Complexity:** analysis
```

The `-` after `[!example]` makes it collapsible (default collapsed). Blank line after the marker is required; subsequent lines must continue with `>` prefix.

## Universal-features discipline (mobile + future-proofing)

| Universal (works everywhere) | Desktop-only or mobile-limited |
|---|---|
| Mermaid diagrams | Excalidraw (view + basic edit on mobile) |
| LaTeX math (`$inline$`, `$$block$$`) | Canvas (functional but small-screen UX) |
| Standard markdown (tables, lists, code blocks) | Dataview (mobile requires plugin) |
| Embedded images | Complex PlantUML |
| Wiki-links and core callouts | Advanced Canvas features |

For long-lived shared content, prefer the universal set; use plugin-dependent features for personal dashboards only.

Mobile vault sizing: with Obsidian 1.10+ progressive loading, vaults of 10k+ notes start under 1 second on phones (Kepano demo'd 17k+ notes). The older 3-4k file limit was a pre-1.10 artifact. Plugin count is the higher driver of mobile startup latency than file count today; soft cap of ~10-15 active plugins remains a good discipline.

### Document platform dependencies inline

When generating notes that depend on desktop-only features, prepend a Platform Notes callout so future-readers know what works where:

```markdown
> [!info] Platform Notes
> **Desktop**: Full Excalidraw editing, Dataview queries, Canvas multi-pane.
> **Mobile**: Static diagram exports, markdown tables, core callouts.
> **Plugins**: Excalidraw, Dataview (optional; richer experience).
```

## Structural-consistency error patterns (5-8)

Patterns 1-4 above are content-rendering errors. Patterns 5-8 are structural-consistency errors that surface when many files are generated. Each carries a diagnose + fix recipe:

- **Pattern 5: Inconsistent navigation across files.** Some files have `[[← Back]] | [[Quick Ref →]]` headers, others don't. Diagnose: `grep -L "← Back" 01-*/core-concepts.md` (lists files WITHOUT the marker). Fix: apply the navigation-link pattern (see `academic-vault.md`) to every file. Verify: re-grep returns empty.
- **Pattern 6: Missing learning objectives.** Some chapter files lack the `## Learning Objectives (COX)` block tying to course outcomes. Diagnose: `grep -L "## Learning Objectives" 01-*/core-concepts.md`. Fix: add the callout per the pattern.
- **Pattern 7: Inconsistent table of contents.** Files >500 lines need a TOC; smaller files don't. Diagnose: `for f in *.md; do lines=$(wc -l < "$f"); if [ "$lines" -gt 500 ] && ! grep -q "## Table of Contents" "$f"; then echo "$f"; fi; done`. Fix: add TOC.
- **Pattern 8: Broken cross-references.** Wiki-links to other chapters fail. Diagnose: `obsidian.com unresolved`. Fix: convert markdown links to wiki-link form; verify with `obsidian.com search` for the target heading text.

## Systematic fix approach (for any consistency error)

When one instance of an inconsistency surfaces, others almost always exist. The diagnose-once, fix-one approach is a trap:

1. **Grep all** — find every file matching the broken pattern, NOT just the one user flagged
2. **Fix all** — apply the corrected pattern across all matches in one pass
3. **Re-grep** — verify zero remaining matches
4. **Document** — add the diagnose+fix to memory so the next session doesn't re-derive it

Evidence: study-vault-builder arc found that user reports of "this file looks wrong" were almost always tip-of-iceberg; 1 user-flagged file -> 4-8 sibling files with the same issue. Spot-fixing required a third round trip. Greedy-grep avoids the loop.

## Other rendering pitfalls

- **Unicode `?` chars in rendered text**: usually a source-app encoding issue (Windows cp1252 vs UTF-8 in the clipboard pipeline) rather than Obsidian itself. Re-encode the source or copy through a UTF-8-aware intermediary.
- **Broken tables (missing blank line)**: pipes/dashes render as literal text. Fix: ensure ONE blank line before any markdown table.
- **HTML details/summary tags don't render in Obsidian**: don't use `<details>`/`<summary>`; use the `> [!example]-` callout form documented above.
