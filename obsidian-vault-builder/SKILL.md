---
name: obsidian-vault-builder
description: Use when adding/editing/querying content in an existing Obsidian vault, configuring plugins, integrating Claude Code with Obsidian via Local REST API or CLI, automating ongoing capture/organization/retrieval, or designing a personal knowledge management workflow. Action-shape: ongoing-capture and editing of an existing vault. For BUILDING academic study vaults from scratch (course prep, exam-ready, mock-exam content), use obsidian-study-vault-builder instead.
version: 0.1.0
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

**For academic study vault construction** (course prep, lecture notes, mock exams, exam-ready content), use the sibling skill `obsidian-study-vault-builder` instead. This skill is for ongoing PKM operation; the sibling is for greenfield study-vault builds.

## When to use

- User asks to add/edit/query content in an Obsidian vault
- User asks to install or configure Obsidian plugins
- User wants to integrate Claude Code with Obsidian via Local REST API or CLI
- User wants to automate ongoing capture/organization/retrieval
- User wants to design a PKM workflow

## Multi-vault layout (when applicable)

Many PKM users run more than one vault: a personal/manual vault (off-limits to agents) plus a Claude-native vault (default agent target). When the user has both, default writes target the Claude-native vault unless they explicitly extend access to the personal one.

Specific paths and override env vars belong in the user's `CLAUDE.md`, not in this skill, so the skill stays portable. For strong off-limits enforcement on the personal vault, consider a structural enforcement hook at the agent boundary that blocks Write/Edit/Bash mutations targeting paths under the personal vault.

## Foundation plugins

These are in Obsidian's official community plugin store. Install only what's needed:

1. **Local REST API** (coddingtonbear): base layer for Claude Code <-> vault interaction. HTTPS bearer token; store the key in a password manager. Loopback-only on `127.0.0.1:27124`.
2. **Obsidian Git**: auto-commit on a schedule, push to a private remote. Note: Obsidian Sync's 30-day version history is NOT a backup; this is.
3. **Templater**: automation foundation for templates and user scripts.
4. **Periodic Notes**: daily/weekly/monthly scaffolding.
5. **Style Settings**: theme customization without writing CSS.
6. **QuickAdd**: macros and capture pipelines.
7. **Smart Connections**: passive sidebar discovery via local embeddings (free).
8. **Bases** (CORE built-in, no install required): replaces ~70% of Dataview use cases.

Plugin-bloat discipline: ~10 active plugins as a soft cap. Anything beyond requires a startup-time measurement before/after to confirm acceptable launch latency.

## AI-layer plugins (caveat-heavy)

Several Claude/Codex-integrating plugins exist with varying vetting status. Always verify current store-listing status before recommending:

- **ObsidiBot** (formerly Cortex; ScottKirvan/ObsidiBot): Claude Code chat panel inside Obsidian. Beta as of skill authoring; verify store status before install.
- **Claudian** (YishenTu/claudian, plugin id `realclaudian`): GUI alternative to terminal Claude Code. Listed in registry with a "not manually reviewed by Obsidian staff" warning shown at install time.
- **Agent Client** (RAIT-09): multi-agent flexibility (Claude/Codex/Gemini). Optional.

Apply the "does this add capability beyond Claude Code reading the vault directly?" test per-plugin. For terminal Claude Code users, the test usually returns "no" for these. Default-skip; install only on explicit user request after surfacing the trust escalation (file-drop or BRAT installs run with full vault read/write/bash access).

## Smart Connections language coverage

Smart Connections ships with an English-only default embedding model. For multilingual vaults (Arabic, Hebrew, CJK, etc.), the default model produces near-noise similarity scores on out-of-distribution content. Workaround:

1. Close Obsidian completely (so the plugin isn't holding state)
2. Edit `<vault>/.smart-env/smart_env.json` and change `smart_sources.embed_model.transformers.model_key` to a multilingual model. Recommended: `BAAI/bge-m3` (100+ languages, 1024 dims) or `intfloat/multilingual-e5-base` (~100 languages, 768 dims)
3. Add a corresponding entry to `<vault>/.smart-env/embedding_models/embedding_models.ajson` with the new `model_key`, `dims`, `max_tokens`
4. Update `embedding_models.default_model_key` in `smart_env.json` to reference the new entry
5. Delete `<vault>/.smart-env/multi/*.ajson` (the per-file embeddings) to force re-embed
6. Reopen Obsidian. Smart Connections will download the new model on first load (~500 MB for bge-m3).

Verify multilingual coverage empirically before relying on it for production search.

## Claude Code <-> vault interaction patterns

### Pattern 1: read directly via filesystem

Most reads: just read the file via the Read tool. Use the vault path from the user's `CLAUDE.md`.

### Pattern 2: vault search via `obsidian.com` CLI

Useful for index-aware operations:

```bash
obsidian.com search query="<text>"
obsidian.com unresolved          # broken wiki-links
obsidian.com tags counts         # tag inventory
obsidian.com property:set name=<key> value=<val> path=<file>
```

Manual-vs-CLI mapping (prefer CLI when index-aware semantics matter):

| Manual | CLI |
|---|---|
| `grep -r "^- \[ \]" *.md` (unfinished tasks) | `obsidian.com tasks daily` |
| `find . -name '*.md' \| wc -l` (file count) | `obsidian.com files folder=<x> total` |
| Manually scanning for broken links | `obsidian.com unresolved` |
| Tag inventory via grep | `obsidian.com tags counts` |
| File frontmatter edit | `obsidian.com property:set name=<key> value=<val> path=<file>` |
| Open vault file in OS file manager | `obsidian.com open path=<file>` (in-app) |

### Pattern 3: Local REST API direct (curl)

Skip community MCP wrappers; most are stale or archived. Curl directly:

```bash
curl -k -H "Authorization: Bearer $OBSIDIAN_REST_API_KEY" \
  https://127.0.0.1:27124/vault/path/to/note.md
```

For production use, install the self-signed cert into the OS trust store rather than passing `-k` everywhere.

### Pattern 4: Bases queries

For new dashboards prefer Bases over Dataview (lighter, core, mobile-friendly):

```yaml
where status = "active" AND priority = "high" AND due >= 2026-05-01
```

### Pattern 5: external tool to embed (PNG/SVG)

When a visualization exceeds Mermaid's expressiveness (algorithm traces, statistical plots, network diagrams, publication-quality figures), generate externally and embed:

- Python: Matplotlib, NetworkX, Seaborn, drawsvg, CairoSVG
- Graphviz/DOT for graph hierarchies
- TikZ (LaTeX) for publication-quality technical diagrams
- D3.js / Plotly for data-driven (export static for vault)

Workflow: create externally, save as PNG/SVG to `<project>/assets/`, embed via `![[../assets/asset.png]]`. Use relative paths so the vault stays portable across re-orgs.

## Diagram tool selection (beyond Mermaid)

Mermaid is the default for universal compatibility. When it hits a limit, reach for one of these:

| Tool | Best for | Platform | Complexity |
|---|---|---|---|
| Mermaid | Standard flowcharts, sequences, class, state, ER, Gantt, mindmap | Universal (desktop + mobile) | Low-Medium |
| Excalidraw | Hand-drawn sketches, whiteboard thinking, annotations | Desktop full; mobile view+basic edit | Low |
| Draw.io | Professional system architecture, complex technical | Desktop | High |
| D2 | Modern software architecture (cleaner syntax than PlantUML) | Desktop (requires D2 install) | Medium |
| PlantUML | Advanced UML beyond Mermaid (sequence, use case, activity, component) | Desktop | High |
| Pikchr | Lightweight technical diagrams (PIC-syntax, client-side render) | Plugin | Medium |
| WaveDrom | Digital timing diagrams for hardware/EE documentation | Desktop/Plugin | Medium |
| Kroki | Unified API serving 25+ formats (BlockDiag, BPMN, C4, D2, Mermaid, PlantUML, Vega, etc.) | Self-host or public | Medium |
| Python+Matplotlib | Algorithm traces, statistical plots, scientific viz (export PNG) | External -> embed | Variable |
| TikZ (LaTeX) | Publication-quality technical diagrams | External -> embed | High |

### Decision tree

- Simple flowchart or sequence -> Mermaid
- Complex UML -> PlantUML or D2
- Hand-drawn aesthetic -> Excalidraw (desktop) or external image
- Professional architecture -> Draw.io or D2
- Hardware timing diagram -> WaveDrom
- Data visualization -> Vega/Charts plugin or Python -> PNG
- Quick sketch -> Excalidraw
- Algorithm trace -> Python (Matplotlib) -> PNG
- Mind map -> Canvas Mindmap or Mermaid mindmap
- Math notation -> LaTeX (always)
- Any of the above but you want one syntax for all -> Kroki

### Tool selection factors

When picking among options, weigh:

- **Concept complexity**: simple -> Mermaid; complex -> external tool
- **Precision needed**: rough -> Excalidraw; exact -> D2 or PlantUML
- **Platform priority**: mobile-important -> universal formats only; desktop-only -> full toolset
- **Editability**: frequent updates -> text-based (Mermaid, D2); one-time -> image acceptable
- **Time available**: quick -> Mermaid or Excalidraw; detailed -> external generation
- **Dynamic vs static**: data-driven -> programmatic (Vega, Python); static -> diagram tool
- **Version control**: text-based formats track in git cleanly; binary needs Git LFS for size

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

## When NOT to use Obsidian

- Team collaboration: Notion
- Daily journaling + outlining primary: Logseq
- Already in Emacs: Org-mode/Org-roam
- Mac with heavy PDF workflow: DEVONthink + Obsidian split
- VS Code minimal-tooling: Foam/Dendron
- Spatial-narrative thinking: Tinderbox

## Common Obsidian rendering pitfalls (writing markdown to a vault)

When generating markdown content for an Obsidian vault, these are the recurring rendering issues. Patterns extracted from a now-deprecated companion skill that generated 37+ academic study files.

### Mermaid diagrams

- `≤` and `≥` break Mermaid parsing. Use ASCII `<=` / `>=`.
- `[1. Text]` triggers "Unsupported markdown: list" error in node labels. Use `["Step 1:<br/>Text"]` (quoted with HTML break).
- `[text](value)` inside node labels is interpreted as link syntax. Use `{text}(value)` (curly braces).
- `&` in mindmap nodes (only) renders as `&amp;` (Mermaid issue #6308, fixed v11+ but not in current Obsidian's bundled version). Workaround: Unicode fullwidth ampersand `＆` (U+FF06). Flowcharts/graphs render `&` correctly.
- Diagnose via `grep -r "≤\|≥\|∞\|∈\|≠" *.md` then ASCII-substitute.

### LaTeX in markdown tables

Pipe characters `|` in LaTeX break markdown table parsing.

```markdown
| Algorithm | Complexity |
|-----------|------------|
| DFS       | $\Theta(\|V\| + \|E\|)$  | <- escaped pipes
```

Search pattern: `grep -r "| \\$.*|.*\\$" *.md` to find unescaped pipes inside LaTeX inside table cells.

### Wiki-link vs markdown-link conventions

For internal vault navigation, use wiki-link form, NOT markdown link form:

- Same-file section: `[[#Section Name]]` (NOT `[Section](#section)`)
- Other-file section: `[[file#Section Name]]`
- Display text override: `[[file|Display Text]]`
- Relative path to parent: `[[../folder/file]]`

Markdown links to internal sections often break in Obsidian's renderer; wiki-links resolve via the link index.

### Collapsible callouts for active-learning content

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

### Universal-features discipline (mobile + future-proofing)

| Universal (works everywhere) | Desktop-enhanced (mobile-limited) |
|---|---|
| Mermaid diagrams | Excalidraw (view + basic edit on mobile) |
| LaTeX math (`$inline$`, `$$block$$`) | Canvas (functional but small-screen UX) |
| Standard markdown (tables, lists, code blocks) | Dataview (mobile requires plugin) |
| Embedded images | Complex PlantUML |
| Wiki-links and core callouts | Advanced Canvas features |

For long-lived shared content, prefer the universal set; use plugin-dependent features for personal dashboards only.

Mobile vault sizing rule of thumb: keep under 3-4k files for acceptable startup latency on phones. 10-15 active plugins maximum (or do startup-time measurements before each install).

### Document platform dependencies inline

When generating notes that depend on desktop-only features, prepend a Platform Notes callout so future-readers know what works where:

```markdown
> [!info] Platform Notes
> **Desktop**: Full Excalidraw editing, Dataview queries, Canvas multi-pane.
> **Mobile**: Static diagram exports, markdown tables, core callouts.
> **Plugins**: Excalidraw, Dataview (optional but enhanced experience).
```

### Other rendering pitfalls

- **Unicode corruption from copy/paste**: symptom is literal `?` characters in rendered text. Diagnose via `grep '?' <file>.md`. Re-encode the source.
- **Broken tables (missing blank line)**: pipes/dashes render as literal text. Fix: ensure ONE blank line before any markdown table.
- **HTML details/summary tags don't render in Obsidian**: don't use `<details>`/`<summary>`; use the `> [!example]-` callout form documented above.

## CLAUDE.md hierarchy within a vault

For vaults spanning multiple knowledge domains, layer CLAUDE.md files at appropriate depths:

- **Vault-root CLAUDE.md**: vault conventions (folder structure principles, universal-features discipline, plugin philosophy, naming rules)
- **Category folder CLAUDE.md** (e.g., `Projects/CLAUDE.md`, `Reference/CLAUDE.md`): domain-specific patterns
- **Project folder CLAUDE.md**: project-specific facts (deadlines, collaborators, source materials)

Prevents monolithic memory files; provides the right amount of context at each depth without context-pollution. New projects inherit from parent layers and only add specifics.

## Asset organization

Per-project: keep diagrams/images in `<project>/assets/`, code samples in `<project>/code/`. Use relative paths (`![[../assets/x.png]]` from notes) so the vault stays portable across re-orgs. Avoid absolute paths.

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

## Status

v0.1.0. Patterns are the result of a research arc with multi-wave agent verification, end-to-end mobile sync test, and Smart Connections empirical multilingual evaluation. NOT yet validated by an external full PKM build. Bump to v1.0 only after that lands.

For the academically-focused sibling, see `obsidian-study-vault-builder` (battle-tested across 37-file/828KB academic study vaults).
