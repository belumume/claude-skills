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

For maximum portability across Obsidian versions and devices, prefer:

- Mermaid diagrams (renders without plugins)
- LaTeX math (`$inline$`, `$$block$$`, renders without plugins in current versions)
- Standard markdown (tables, lists, code blocks)
- Wiki-links and core callouts

Plugin-dependent syntax (Dataview queries, custom CSS classes, plugin-only callout types) breaks if a future user opens the vault without that plugin. For long-lived shared content, prefer the universal set; use plugin features for personal dashboards only.

## Status

v0.1.0. Patterns are the result of a research arc with multi-wave agent verification, end-to-end mobile sync test, and Smart Connections empirical multilingual evaluation. NOT yet validated by an external full PKM build. Bump to v1.0 only after that lands.

For the academically-focused sibling, see `obsidian-study-vault-builder` (battle-tested across 37-file/828KB academic study vaults).
