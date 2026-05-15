---
name: obsidian-vault-builder
description: Use when adding/editing/querying content in an existing Obsidian vault, configuring plugins, integrating Claude Code with Obsidian via Local REST API or CLI, automating ongoing capture/organization/retrieval, designing a personal knowledge management workflow, OR building academic study vaults (course prep, exam-ready, mock-exam content — the durable academic-study patterns from a deprecated companion skill have been folded into this one).
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

**For academic study vault construction** (course prep, lecture notes, mock exams, exam-ready content): the durable patterns from the deprecated `obsidian-study-vault-builder` skill have been folded into this one (see "Common Obsidian rendering pitfalls" below + the QA / mobile / universal-features sections). The companion skill itself was removed via PR #6 and re-validated 2026-05-15 (over-triggered on exam-prep prompts; structurally misaligned with the interactive-practice approach in `~/.claude/rules/exam-prep-protocol.md`).

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
4. **Daily Notes** (core, no install): maintained baseline for daily scaffolding. The companion **Calendar** plugin (`liamcain/obsidian-calendar-plugin`) is ~23 months stale (same author-abandonment pattern as Periodic Notes); still functional but no fixes incoming. For weekly/monthly/quarterly/yearly scopes, **Periodic Notes** (`liamcain/obsidian-periodic-notes`) is the only widely-used option; ~21 months stale but still functional. Bases-based date views (querying frontmatter `date` properties) can replace Calendar's sidebar UI for many users. `luiisca/obsidian-periodic-notes-calendar` is a smaller, actively-maintained alternative combining both. Use Templater for custom periodic-note generation if you outgrow Periodic Notes.
5. **Style Settings**: theme customization without writing CSS.
6. **QuickAdd**: macros and capture pipelines.
7. **Smart Connections** (`brianpetro/obsidian-smart-connections`): passive sidebar discovery via local embeddings (free). Note: 475+ open issues and a paywalled v4 have driven users to forks; consider `logancyang/obsidian-copilot` as an alternative or co-primary AI-layer plugin (6.9k+ stars, broader model support including Claude/Gemini/local).
8. **Bases** (CORE built-in, no install required): replaces ~70% of Dataview use cases.

Plugin-bloat discipline: ~10 active plugins as a soft cap. Anything beyond requires a startup-time measurement before/after to confirm acceptable launch latency.

## AI-layer plugins (caveat-heavy)

Several Claude/Codex-integrating plugins exist with varying vetting status. Always verify current store-listing status before recommending:

- **Agent Client** (`RAIT-09/obsidian-agent-client`, registry id `agent-client`): multi-agent flexibility (Claude/Codex/Gemini via standardized ACP). Verified in official store as of 2026-05-15. Store-installable.
- **Claudian** (`YishenTu/claudian`, plugin id `realclaudian`): GUI alternative to terminal Claude Code. NOT in official store as of 2026-05-15; BRAT install only. Verify status before recommending.
- **ObsidiBot** (formerly Cortex; `ScottKirvan/ObsidiBot`): Claude Code chat panel inside Obsidian. NOT in official store as of 2026-05-15; BRAT install only. Verify status before recommending.
- Exclude `m-rgba/obsidian-ai-agent`: archived 2026-04.

Apply the "does this add capability beyond Claude Code reading the vault directly?" test per-plugin. For terminal Claude Code users, the test usually returns "no" for these. Default-skip; install only on explicit user request after surfacing the trust escalation (file-drop or BRAT installs run with full vault read/write/bash access).

## Smart Connections language coverage

Smart Connections ships with an English-only default embedding model. For multilingual vaults (Arabic, Hebrew, CJK, etc.), the default model produces near-noise similarity scores on out-of-distribution content.

**Recommended path (UI)**: open Smart Environment settings in Obsidian. The Default embedding model dropdown lists 3 transformers-compatible options labelled "BGE-micro-v2 (fastest)", "Multilingual E5 Small", "Snowflake Arctic Embed XS (fast)". Internally these resolve to Xenova-hosted ONNX-quantized variants (`Xenova/multilingual-e5-small`, etc.). For Arabic / Hebrew / CJK content, pick "Multilingual E5 Small". Click Test model to download (the Test button may transiently report "Message adapter unloaded" but the actual embedding pipeline still works). Then click Reset data + Re-import to regenerate embeddings.

**Direct-JSON swap path** (NOT recommended, error-prone): the active model is determined by `<vault>/.smart-env/smart_env.json`'s `embedding_models.default_model_key` field, which references an entry in `<vault>/.smart-env/embedding_models/embedding_models.ajson` registry. The `smart_sources.embed_model.transformers.model_key` field is set during UI swaps but appears unused as the source of truth. The registry file is append-only ajson; multiple entries with the same key are tolerated (last-wins semantics). The plugin loads via transformers.js which fetches `huggingface.co/<model>/resolve/main/onnx/model_quantized.onnx`; models without an ONNX-quantized variant at that exact path fail. Tested 2026-05-15: `BAAI/bge-m3` fails (no Xenova ONNX variant). For Pro-tier providers (LM Studio, Ollama, OpenAI, Gemini, OpenRouter) the JSON shape is different per provider. Prefer the UI path; the JSON format isn't a stable API.

For long-term setups, prefer the UI dropdown with a documented model. Verify multilingual coverage empirically before relying on it for production search.

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

Multi-vault: `obsidian.com --vault=<name> <subcommand>` targets a specific vault. Useful when more than one vault is open or you need to script across them.

Universal escape hatch: `obsidian.com command id=<command-id>` executes any registered Obsidian command (including plugin commands). `obsidian.com commands` lists all available command IDs. CLI also has subcommands for `bases`, `publish:*`, `sync:*`, `quickadd:*`, `templater:*`, `snippets`, `themes`, `hotkey`, `hotkeys`; see `obsidian.com help` for the full ~100-command catalog.

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

| Tool | Best for | Plugin status (verified 2026-05-15) |
|---|---|---|
| Mermaid (v11+) | Flowcharts, sequence, class, state, ER, Gantt, mindmap, block, packet, architecture, sankey | Bundled with Obsidian; active |
| Excalidraw | Hand-drawn sketches, whiteboard thinking, annotations | `zsviczian/obsidian-excalidraw-plugin`, active (pushed 2026-05) |
| Draw.io / Diagrams | Professional system architecture, complex technical | Two variants: `zapthedingbat/drawio-obsidian` (offline, active 2026-02), `jensmtg/obsidian-diagrams-net` (online, last 2024-08, maintainer seeking successor). Prefer offline. |
| PlantUML | Advanced UML (sequence, use case, activity, component) beyond Mermaid | `joethei/obsidian-plantuml`, active (pushed 2026-04) |
| D2 | Modern software architecture (cleaner syntax than PlantUML) | `terrastruct/d2-obsidian` STALE (last release 2023-12, plugin lags D2 by major versions). D2 language itself active. Verify before recommending. |
| Pikchr | Lightweight technical diagrams (PIC-syntax, client-side render) | `notlibrary/obsidian-adamantine-pick` (registry id `adamantine-pick`), active (pushed 2026-04) |
| WaveDrom | Digital timing diagrams for hardware/EE documentation | `kingsquirrel152/obsidian-wavedrom` STALE (~16 months no commits). Verify before use. |
| Kroki | Unified API serving 25+ formats (BlockDiag, BPMN, C4, D2, Mermaid, PlantUML, Vega, etc.) | Self-hostable or public service; verify your specific format support before adopting |
| Python+Matplotlib | Algorithm traces, statistical plots, scientific viz | External -> embed PNG/SVG |
| TikZ (LaTeX) | Publication-quality technical diagrams | TikZJax (`artisticat1/obsidian-tikzjax`, ~22 months stale; works for most TikZ but unmaintained) for inline; external -> embed PNG/SVG for complex |

### Decision tree

- Simple flowchart or sequence -> Mermaid
- Block / architecture / packet / sankey diagram -> Mermaid v11+ (added natively)
- Complex UML -> PlantUML (D2 plugin is stale; use the D2 language externally and embed PNG/SVG)
- Hand-drawn aesthetic -> Excalidraw (desktop) or external image
- Professional architecture -> Draw.io (offline variant) or D2 external
- Hardware timing diagram -> WaveDrom (verify plugin freshness or use the wavedrom CLI externally)
- Data visualization -> Vega/Charts plugin or Python -> PNG
- Quick sketch -> Excalidraw
- Algorithm trace -> Python (Matplotlib) -> PNG
- Mind map -> Mermaid mindmap (now stable post v11.4) or Canvas Mindmap
- Math notation -> LaTeX (always)
- Want one syntax for many formats -> Kroki (verify format support)

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

When generating markdown content for an Obsidian vault, these are the recurring rendering issues. Patterns extracted from a deprecated companion skill (`obsidian-study-vault-builder`, removed via PR #6 and re-validated 2026-05-15: over-triggered on exam-prep prompts and was structurally misaligned with the interactive-practice approach). The durable patterns below were folded here permanently because they apply to ANY agent writing markdown to a vault, not just academic builds.

### Mermaid diagrams

- `[1. Text]` triggers "Unsupported markdown: list" error in node labels. Use `["Step 1:<br/>Text"]` (quoted with HTML break).
- `[text](value)` inside node labels is interpreted as link syntax. Use `{text}(value)` (curly braces).
- Special-character parsing edge cases persist in some Mermaid v11.x diagram types (sankey, etc.). For mindmap `&` (Mermaid issue #6308) and mindmap `<`/`>` (issue #6396), both fixed in v11.4+ and current Obsidian (1.12.x) bundles a fixed version. Older Obsidian releases may still need ASCII `<=`/`>=` substitution and Unicode fullwidth `＆` workaround.
- Diagnose via `grep -r "≤\|≥\|∞\|∈\|≠" *.md` if targeting older Obsidian.

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

### Other rendering pitfalls

- **Unicode `?` chars in rendered text**: usually a source-app encoding issue (Windows cp1252 vs UTF-8 in the clipboard pipeline) rather than Obsidian itself. Re-encode the source or copy through a UTF-8-aware intermediary.
- **Broken tables (missing blank line)**: pipes/dashes render as literal text. Fix: ensure ONE blank line before any markdown table.
- **HTML details/summary tags don't render in Obsidian**: don't use `<details>`/`<summary>`; use the `> [!example]-` callout form documented above.

## CLAUDE.md layering within a vault

Per the official Claude Code memory model (https://code.claude.com/docs/en/memory), CLAUDE.md files are loaded by walking up the directory tree from cwd; all discovered files concatenate into context (they don't override each other). Subdirectory CLAUDE.md files lazy-load when Claude reads files there.

Practical application for vaults spanning multiple knowledge domains: layer CLAUDE.md files at appropriate depths.

- Vault-root CLAUDE.md: vault conventions (folder structure principles, universal-features discipline, plugin philosophy, naming rules)
- Category folder CLAUDE.md (e.g., `Projects/CLAUDE.md`, `Reference/CLAUDE.md`): domain-specific patterns
- Project folder CLAUDE.md: project-specific facts (deadlines, collaborators, source materials)

Official guidance recommends keeping each CLAUDE.md under 200 lines. For path-scoped rules, `.claude/rules/*.md` with `paths` frontmatter is an alternative to nested CLAUDE.md.

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

## Status

v0.1.0. Patterns are the result of a research arc with multi-wave agent verification, end-to-end mobile sync test, and Smart Connections empirical multilingual evaluation. NOT yet validated by an external full PKM build. Bump to v1.0 only after that lands.

The previously-separate `obsidian-study-vault-builder` skill (battle-tested across 37-file/828KB academic study vaults) was deprecated 2026-05-15 per PR #6 + post-compact re-validation. Its durable patterns are folded into this skill above.
