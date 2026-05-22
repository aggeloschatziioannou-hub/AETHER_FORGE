# Aether_Forge - New Session Onboarding

## Quick Context
Aether_Forge is an AI-native infinite canvas application.
Stack: Next.js 15 App Router, React 19, TypeScript strict, Firebase 10.8, Tailwind 4.
Phase 1 (Core Infrastructure). `@/components/CanvasMainStage` is a stub.

## Where to Start

### 1. Read the instruction database
```sql
-- Quickstart: list all sections
SELECT section FROM instructions;
-- Load specific topics as needed (don't dump the whole DB)
SELECT content FROM instructions WHERE section = 'proj-structure';
SELECT content FROM instructions WHERE section = 'proj-commands';
SELECT content FROM instructions WHERE section = 'mcp-overview';
```
**Query via `project-instructions` MCP server's `read_query` tool.**

### 2. Load relevant skills
```bash
# List project-local skills
ls .opencode/skills/
# Load skill via native tool: skill("name") - e.g. skill("gitnexus-exploring")
```

### 3. Load GitNexus context
```
gitnexus_query({query: "what does this project do"})
gitnexus://repo/aetherforge/context
```

### 4. Check task and decision history
```sql
SELECT * FROM evolution ORDER BY id DESC LIMIT 10;
```
Also check `memory-vault/todo.md` for pending tasks.

## Current State (May 2026)

### MCP Servers (in opencode.json)
1. **gitnexus** - code intelligence: knowledge graph (212 nodes/244 edges/9 clusters/1 execution flow), 7 tools
2. **project-instructions** - SQLite instruction DB (25 sections, 52KB)

### Instruction DB Sections
| Prefix | Count | Topics |
|--------|-------|--------|
| proj-* | 4 | overview, structure, commands, config |
| conv-* | 3 | TypeScript, React, Firebase conventions |
| mcp-* | 4 | overview, gitnexus, instructions, database |
| token-* | 1 | token optimization + caveman |
| skills-* | 1 | skill reference (all installed skills) |
| security-* | 3 | overview, input validation, auth |
| self-* | 1 | self-evolution workflow |
| design-* | 2 | overview, design system |
| workflow-* | 2 | onboarding, task workflow |
| troubleshoot | 1 | common issues |
| fallback-* | 1 | if unsure |

### Evolution Table (self-improvement)
Tracked in `evolution` table. Schema:
```sql
CREATE TABLE evolution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT (datetime('now')),
    agent TEXT NOT NULL,
    event_type TEXT NOT NULL,  -- e.g. 'decision', 'learning', 'improvement', 'system-init'
    summary TEXT NOT NULL,
    detail TEXT
);
```

### Project Structure
```
aether-forge-app/          # Next.js application
  src/app/layout.tsx       # Root layout
  src/app/page.tsx         # Home (mounts CanvasMainStage stub)
  src/hooks/               # useCanvasViewport, useRealtimePresence
  src/wdyr.ts              # why-did-you-render (missing npm dep)
memory-vault/              # AI persistent state
  project-instructions.db  # SQLite instruction DB (MCP-served)
  todo.md                  # Task matrix
  evolution-ledger.json    # State snapshots (legacy)
  stage_outputs/           # Stage receipts
  analytics/               # Generated snapshots
  new-chat-prompt.md       # This file (refined new-session prompt)
scripts/                   # Python automation
  macro-engine.py          # Orchestrator: seed DB → gitnexus analyze → snapshot bundle
  seed-instructions.py     # Seeds/updates instruction DB from AGENTS.md
  consolidate-memory.py    # Memory consolidation tool
.opencode/skills/          # Project-local skills
```

### Commands
All from `aether-forge-app/`:
- `npm run dev` - dev server :3000
- `npm run build` - type-check + build
- `npm run lint` - ESLint
- `npm run format:fix` - Prettier write

## Critical Gotchas
- `wdyr.ts` imports missing npm package `@welldone-software/why-did-you-render`
- `npx -y gitnexus@latest` fails with Node 22 "Cannot destructure property 'package'" → use globally installed `gitnexus` directly
- `.gemini/extensions/` is empty → caveman install.gg blocked on non-interactive prompt
- `npm run build` is the type-check command (no separate `npm run typecheck`)
- opencode.json uses `command`+`args` format (not `type`/`enabled`)
- OpenCode uses native `skill` tool (not `TodoWrite` or `Task` with subagents)

## Self-Evolution Workflow
YOU ARE AUTHORIZED to evolve this system:
1. **Learn** something about the project or tooling
2. **Record** in evolution table: `write_query("INSERT INTO evolution (agent, event_type, summary, detail) VALUES ('agent-name', 'learning', '...', '...')")`
3. **Update** instructions: `write_query("UPDATE instructions SET content='...' WHERE section='...'")`
4. **Create scripts** in `scripts/` for repeatable tasks
5. **Log improvements** in `memory-vault/improvements.md`

Cycle: Learn → Record → Update → Improve

## GitNexus Workflow
- ALWAYS run `gitnexus_impact({target: "symbolName", direction: "upstream"})` before editing
- ALWAYS run `gitnexus_detect_changes()` before committing
- NEVER rename via find-and-replace - use `gitnexus_rename`
- If index stale: run `gitnexus analyze` in terminal

## Next Deliverable
Build CanvasMainStage - the infinite canvas component. It should:
- Use `useCanvasViewport` hook for viewport math
- Use `useRealtimePresence` hook for Firebase multiplayer presence
- Be GPU-accelerated (translate3d transforms)
- Support pan/zoom via viewport state
- Show multiplayer cursors from presence data
- Dark theme, Tailwind 4 styling
- TypeScript strict, no `any`

## End Session
Run `python scripts/macro-engine.py` to snapshot state.
