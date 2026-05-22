# 00-index.md

## Modular DB Dashboard System — Aether_Forge

A high-level architecture for a modular, infinite-canvas UI for database dashboards, using draggable/resizable panels ("widgets"), orchestrated via an MCP (Meta Command Proxy) Python backend to handle DB connections and workflow logic. This structure centers around extensibility, robustness on read-only/NixOS systems, and human-in-the-loop workflows.

### Components
- Infinite Canvas UI (Next.js 15, React)
- Modular Panel/Widget framework
- Python/FastAPI MCP Proxy for backend connections
- Panel Registry/Loader for plug-and-play tools
- Opencode/skills/MCP integration layer for panel intelligence and automation

### Folder Layout
All technical specs live under `/home/user/aetherforge/APP_BUIDLING_PARTS/db-dashboard/`, each major component gets one markdown doc clearly named and prefixed (00, 01, 02, ...).

### Docs in this Set
- 00-index.md: This overview
- 01-mcp-proxy.md: Python/FastAPI MCP proxy spec
- 02-panel-system.md: UI & panel container/loader/integration
- 03-db-explorer-panel.md: DB Explorer panel spec
- 04-future-roadmap.md: Next areas, extension ideas
