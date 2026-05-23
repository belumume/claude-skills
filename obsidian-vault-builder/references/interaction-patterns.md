# Claude Code <-> Obsidian vault interaction patterns

Five patterns, increasing complexity. Pick by the operation, not by preference for one tool.

## Pattern 1: read directly via filesystem

Most reads: use the Read tool. Pull the vault path from the user's `CLAUDE.md` rather than hardcoding.

## Pattern 2: vault search via `obsidian.com` CLI

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

Multi-vault: `obsidian.com --vault=<name> <subcommand>` targets a specific vault. Useful when more than one vault is open or when scripting across vaults.

Universal escape hatch: `obsidian.com command id=<command-id>` executes any registered Obsidian command (including plugin commands). `obsidian.com commands` lists all available command IDs. CLI also has subcommands for `bases`, `publish:*`, `sync:*`, `quickadd:*`, `templater:*`, `snippets`, `themes`, `hotkey`, `hotkeys`; see `obsidian.com help` for the full ~100-command catalog.

## Pattern 3: Local REST API direct (curl)

Skip community MCP wrappers; most are stale or archived. Curl directly:

```bash
curl -H "Authorization: Bearer $OBSIDIAN_REST_API_KEY" \
  https://127.0.0.1:27124/vault/path/to/note.md
```

For production use, install the self-signed cert into the OS trust store rather than passing `-k` everywhere. Cert is downloadable via the "this certificate" link in Local REST API plugin settings.

## Pattern 4: Bases queries

For new dashboards prefer Bases over Dataview (lighter, core, mobile-friendly):

```yaml
where status = "active" AND priority = "high" AND due >= 2026-05-01
```

## Pattern 5: external tool to embed (PNG/SVG)

When a visualization exceeds Mermaid's expressiveness (algorithm traces, statistical plots, network diagrams, publication-quality figures), generate externally and embed:

- Python: Matplotlib, NetworkX, Seaborn, drawsvg, CairoSVG
- Graphviz/DOT for graph hierarchies
- TikZ (LaTeX) for publication-quality technical diagrams
- D3.js / Plotly for data-driven (export static for vault)

Workflow: create externally, save as PNG/SVG to `<project>/assets/`, embed via `![[../assets/asset.png]]`. Use relative paths so the vault stays portable across re-orgs.
