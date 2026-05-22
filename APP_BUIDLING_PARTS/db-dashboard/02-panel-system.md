# 02-panel-system.md

## Infinite Canvas & Panel/Widget System

### Overview
- Main UI = infinite canvas (Next.js 15/React, React Flow or similar)
- Panels/widgets = self-contained React modules, hot-loadable, extensible
- Built with minified state footprint, fast cleanup, lazy mounting/unmount
- Drag, resize, minimize, stack/lock panels; position/layout saved/replayed
- Panels can be pure UI, DB tools, or skill/MCP-driven agents

### Panel Integration
- Registry-based panel discovery (no hardcoded imports)
- Loader/host component manages lifecycle, error isolation
- Weak-coupled event system for inter-panel comms
- Per-panel state container (react context+signals)
- Opencode can inject instructions/skills to automate/test panels

### UI/UX Specs
- Keyboard and mouse nav, context menu
- Panel launcher (searchable add menu)
- Accessibility: focus/ARIA, themable
- Robust to missing/slow panels — fallback containers
- NixOS/read-only-friendly; robust for airgapped/offline
