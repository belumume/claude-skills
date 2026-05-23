# Obsidian plugins (foundation + AI-layer + Smart Connections multilingual)

## Foundation plugins

These are in Obsidian's official community plugin store. Install only what's needed:

1. **Local REST API** (coddingtonbear): base layer for Claude Code <-> vault interaction. HTTPS bearer token; store the key in a password manager. Loopback-only on `127.0.0.1:27124`.
2. **Obsidian Git**: auto-commit on a schedule, push to a private remote. Note: Obsidian Sync's 30-day version history is NOT a backup; this is.
3. **Templater**: automation foundation for templates and user scripts.
4. **Daily Notes** (core, no install): maintained baseline for daily scaffolding. The companion **Calendar** plugin (`liamcain/obsidian-calendar-plugin`) is ~23 months stale (same author-abandonment pattern as Periodic Notes); still functional but no fixes incoming. For weekly/monthly/quarterly/yearly scopes, **Periodic Notes** (`liamcain/obsidian-periodic-notes`) is the only widely-used option; ~21 months stale but still functional. Bases-based date views (querying frontmatter `date` properties) can replace Calendar's sidebar UI for many users. `luiisca/obsidian-periodic-notes-calendar` is a smaller, actively-maintained alternative combining both. Templater handles custom periodic-note generation for setups that outgrow Periodic Notes.
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
