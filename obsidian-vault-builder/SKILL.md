---
name: obsidian-vault-builder
description: Use when adding/editing/querying content in an existing Obsidian vault, configuring plugins, integrating Claude Code with Obsidian via Local REST API or CLI, automating ongoing capture/organization/retrieval, designing a personal knowledge management workflow, OR building academic study vaults (course prep, exam-ready, mock-exam content — the durable academic-study patterns from a deprecated companion skill have been folded into this one).
metadata:
  version: 0.2.0
  tags:
    - obsidian
    - knowledge-management
    - markdown
    - vaults
    - pkm
    - tools-for-thought
---

# Obsidian Vault Builder (general PKM, multi-vault aware)

Patterns for operating an Obsidian vault from Claude Code: capture pipelines, plugin selection, REST API integration, file-portability discipline, methodology choice. Multi-vault aware.

For academic study vault construction (course prep, lecture notes, mock exams, exam-ready content): the durable patterns from the deprecated `obsidian-study-vault-builder` skill have been folded into this skill. See `references/academic-vault.md`. The companion skill itself was removed via PR #6 and re-validated 2026-05-15 (over-triggered on exam-prep prompts; structurally misaligned with the interactive-practice approach in `~/.claude/rules/exam-prep-protocol.md`).

## When to use

- User asks to add/edit/query content in an Obsidian vault
- User asks to install or configure Obsidian plugins
- User wants to integrate Claude Code with Obsidian via Local REST API or CLI
- User wants to automate ongoing capture/organization/retrieval
- User wants to design a PKM workflow
- User asks to build a course/exam/study vault (see `references/academic-vault.md`)

## Checkpoint-based vault build (greenfield, large generation tasks)

When generating a vault from scratch or filling in many chapters/sections at once, never generate everything upfront. Use progressive validation:

1. First chapter / first section — then STOP
2. User review — approve format, structure, quality
3. Remaining chapters / sections — continue with validated pattern
4. Final QA pass — systematic verification per `references/qa-checklist.md`

Why this matters:
- Catches format issues before they multiply across 30+ files
- Validates approach matches user needs early
- Adjusts course when cheap (chapter 1) vs expensive (chapter 8)
- Prevents 5+ hours of rework

Approximate time budget for a typical academic course (10 chapters): chapter 1 ~30 min, review ~15 min, remaining ~90 min, QA ~30 min = ~2.5 hours vs 80+ hours manual. Pattern is greenfield-build universal; applies equally to paper/book/codebase-docs generation.

## Multi-vault layout (when applicable)

Many PKM users run more than one vault: a personal/manual vault (off-limits to agents) plus a Claude-native vault (default agent target). When the user has both, default writes target the Claude-native vault unless they explicitly extend access to the personal one.

Specific paths and override env vars belong in the user's `CLAUDE.md`, not in this skill, so the skill stays portable. For strong off-limits enforcement on the personal vault, consider a structural enforcement hook at the agent boundary that blocks Write/Edit/Bash mutations targeting paths under the personal vault.

## Foundation plugins (summary)

Install only what's needed; soft cap ~10 active plugins. Core set:

- **Local REST API** — base layer for Claude Code <-> vault interaction (loopback HTTPS + bearer token)
- **Obsidian Git** — auto-commit + push to private remote (real backup tier)
- **Templater** — automation foundation for templates/scripts
- **Daily Notes** (core) — daily scaffolding baseline
- **Style Settings** — theme customization without CSS
- **QuickAdd** — macros + capture pipelines
- **Smart Connections** (multilingual caveats apply) — passive sidebar discovery via local embeddings
- **Bases** (core) — replaces ~70% of Dataview use cases

Detailed plugin notes (Calendar/Periodic Notes status, Smart Connections multilingual swap, AI-layer plugin caveats): see `references/plugins.md`.

## Claude Code <-> vault interaction patterns (summary)

Five patterns, ordered by complexity:

1. Read directly via filesystem (Read tool)
2. Vault search via `obsidian.com` CLI (index-aware)
3. Local REST API direct (curl)
4. Bases queries (dashboards)
5. External tool to embed (PNG/SVG for complex viz)

Per-pattern details + CLI mapping table + multi-vault notes: see `references/interaction-patterns.md`.

## Diagram tool selection (summary)

Mermaid is default for universal compatibility. When it hits a limit, the alternatives table covers Excalidraw, Draw.io, PlantUML, D2, Pikchr, WaveDrom, Kroki, TikZ, Python+Matplotlib. Tool selection factors: concept complexity, precision, platform priority, editability, time, dynamic-vs-static, version control.

Full table + decision tree + selection factors: see `references/diagrams.md`.

## File-format philosophy

Files are file-portable by definition (markdown, txt, universal formats). Apps are transient tools; data is permanent. Use any Obsidian feature freely (wikilinks, transclusions, callouts, highlights, comments, Dataview/Bases queries).

Caveat: don't let a Dataview/Bases query be the only home of a fact. The query result is Obsidian-only; the underlying notes are portable.

## Methodology choice

| Pick | When | Free source |
|---|---|---|
| Evergreen Notes (Matuschak) | Knowledge work, 2+ year horizon | notes.andymatuschak.org |
| Zettelkasten (Doto) | Long-form output (books/papers) | writing.bobdoto.computer |
| LYT/Ideaverse (Milo) | Original synthesis with MOCs | linkingyourthinking.com |
| PARA (Forte) | Output-driven projects | fortelabs.com |

## Backup discipline

Obsidian Sync's 30-day version history is NOT backup. For real backup:

1. `git init` in vault root
2. `.gitignore` for `.obsidian/workspace*`, `.obsidian/cache*`, `.obsidian/plugins/*/data.json` (plugin credentials), `.smart-env/`, `.trash/`
3. Auto-commit on session close (or scheduled)
4. Push to a private remote (GitHub private repo, or self-hosted)
5. Periodic restore drill: clone the remote into a scratch dir, verify content matches expectation. A backup that has never been restored is hope, not backup.

## Common rendering pitfalls (summary)

Recurring issues when generating markdown for an Obsidian vault: Mermaid node-label syntax, LaTeX pipes in tables, wiki-link vs markdown-link conventions, collapsible callouts for active-learning content, universal-features discipline (mobile + future-proofing), structural-consistency patterns 5-8 (navigation/objectives/TOC/cross-refs), systematic fix approach (grep all -> fix all -> re-grep -> document), and minor unicode/table/HTML-tag pitfalls.

Full content + diagnose+fix recipes + universal-vs-platform feature table: see `references/rendering-pitfalls.md`.

## Anti-patterns

- Plugin bloat (>10 active without startup measurement)
- Structure paralysis (weeks reorganizing folders, zero notes written)
- MOC paralysis (empty MOCs created preemptively)
- Daily-Note-only vault (365 daily notes, zero permanent notes)
- Sync-only backup (Obsidian Sync history is NOT backup; use obsidian-git as second tier)
- Dataview/Bases query as the only home of a fact
- Disabling Restricted Mode without an obsidianpluginaudit.com check
- File-dropping plugins from GitHub releases without surfacing the trust escalation (bypasses both store review and BRAT vetting)
- Committing `.obsidian/plugins/*/data.json` to git (often contains plaintext credentials)
- Sending non-ASCII bodies via REST API PUT without explicit UTF-8 charset header (causes U+FFFD corruption)
- Recommending Smart Connections for multilingual content without first swapping to a multilingual embedding model

## Asset organization

Two patterns are in active community use; neither has clear consensus as the "right" one:

- **Per-project**: `<project>/assets/` for diagrams/images, `<project>/code/` for samples. Relative paths (`![[../assets/x.png]]`) keep the project portable. Best for project-as-unit thinking and easy git submodule.
- **Flat attachment folder**: Obsidian's default; single `attachments/` (or configured equivalent) at vault root, all paste-images go there. Best for cross-cutting reuse and simpler image-management.

Pick based on portability needs (per-project wins) vs cross-vault reuse (flat wins). Avoid absolute paths in either pattern.

For vaults that grow, the standard PKM structure scales:

```
vault/
  Projects/<project-name>/
    notes/
    assets/        # diagrams, images
    code/          # example code
  Resources/       # textbooks, papers, reference PDFs
  Daily-Notes/
  Templates/
```

Tag by concept rather than by location (`#async-patterns` not `#nodejs-folder`). Properties for metadata (`status`, `created`, `tags`). Bases queries for dynamic overviews on top of the static folder structure.

For academic-study vault scaffolds (different shape, 00-overview / 01-chapter / cross-chapter / mock-exams): see `references/academic-vault.md`.

## When NOT to use Obsidian

- Team collaboration: Notion
- Daily journaling + outlining primary: Logseq
- Already in Emacs: Org-mode/Org-roam
- Mac with heavy PDF workflow: DEVONthink + Obsidian split
- VS Code minimal-tooling: Foam/Dendron
- Spatial-narrative thinking: Tinderbox

## Additional resources

### Reference files

For detailed content beyond the summaries above:

- **`references/plugins.md`** — Foundation plugins, AI-layer plugins (caveats), Smart Connections multilingual swap
- **`references/interaction-patterns.md`** — Patterns 1-5 in detail + Manual-vs-CLI mapping table
- **`references/diagrams.md`** — Full diagram tool table + decision tree + selection factors
- **`references/rendering-pitfalls.md`** — Mermaid/LaTeX/wiki-link/collapsibles/universal-features + structural-consistency patterns 5-8 + systematic fix approach
- **`references/academic-vault.md`** — Academic study vault scaffold + per-chapter trio + content patterns (navigation/objectives/applied-understanding) + comprehensive coverage + CLAUDE.md layering
- **`references/qa-checklist.md`** — 50+ item QA checklist for declaring chapters/sections complete (content/format/structure/quality) + CLI verification commands + project template
- **`references/voice-capture-macro.md`** — QuickAdd + ElevenLabs MCP voice-memo-to-daily-note macro (working implementation as of 2026-05-15)

## Status

v0.2.0 (2026-05-23 restructured per canonical agent-skills spec: <500 lines + companion docs in `references/` subdirectory). Patterns are the result of a research arc with multi-wave agent verification, end-to-end mobile sync test, and Smart Connections empirical multilingual evaluation. NOT yet validated by an external full PKM build. Bump to v1.0 only after that lands.

The previously-separate `obsidian-study-vault-builder` skill (battle-tested across 37-file/828KB academic study vaults) was deprecated 2026-05-15 per PR #6 + post-compact re-validation. Its durable patterns are folded into this skill (`references/academic-vault.md` + `references/qa-checklist.md` + `references/rendering-pitfalls.md` § structural-consistency).
