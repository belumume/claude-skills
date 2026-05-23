# Diagram tool selection (beyond Mermaid)

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
| Kroki | Unified API serving 25+ formats (BlockDiag, BPMN, C4, D2, Mermaid, PlantUML, Vega, etc.) | Self-hostable or public service; verify the specific format support before adopting |
| Python+Matplotlib | Algorithm traces, statistical plots, scientific viz | External -> embed PNG/SVG |
| TikZ (LaTeX) | Publication-quality technical diagrams | TikZJax (`artisticat1/obsidian-tikzjax`, ~22 months stale; works for most TikZ but unmaintained) for inline; external -> embed PNG/SVG for complex |

## Decision tree

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

## Tool selection factors

When picking among options, weigh:

- **Concept complexity**: simple -> Mermaid; complex -> external tool
- **Precision needed**: rough -> Excalidraw; exact -> D2 or PlantUML
- **Platform priority**: mobile-important -> universal formats only; desktop-only -> full toolset
- **Editability**: frequent updates -> text-based (Mermaid, D2); one-time -> image acceptable
- **Time available**: quick -> Mermaid or Excalidraw; detailed -> external generation
- **Dynamic vs static**: data-driven -> programmatic (Vega, Python); static -> diagram tool
- **Version control**: text-based formats track in git cleanly; binary needs Git LFS for size
