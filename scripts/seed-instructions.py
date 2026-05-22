"""Seed comprehensive project instructions into SQLite database.

Sections optimized for fast lookup: short, prefix-grouped names.
All instructions queryable via MCP `project-instructions` sqlite server.

Also creates evolution tables for persistent AI memory.
"""
import sqlite3
import os
from datetime import datetime, UTC

DB_PATH = "memory-vault/project-instructions.db"


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def ensure_tables(conn):
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS instructions (
            section TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            updated_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (datetime('now')),
            agent TEXT NOT NULL,
            event_type TEXT NOT NULL,
            summary TEXT NOT NULL,
            detail TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_evolution_type ON evolution(event_type);
        CREATE INDEX IF NOT EXISTS idx_evolution_ts ON evolution(timestamp);
    """)
    conn.commit()


def upsert(conn, section, content):
    conn.execute(
        "INSERT OR REPLACE INTO instructions (section, content, updated_at) VALUES (?, ?, datetime('now'))",
        (section, content),
    )


# ---------------------------------------------------------------------------
# INSTRUCTIONS – every section is a self-contained, detailed reference
# Section names use prefix groups for fast filter queries
# ---------------------------------------------------------------------------
INSTRUCTIONS = {
    # ── PROJECT FOUNDATION ──────────────────────────────────────────────
    "proj-overview": """Aether_Forge - AI-native infinite canvas application.
Stack: Next.js 15 (App Router), React 19, TypeScript strict, Firebase 10.8, Tailwind 4.
Purpose: Collaborative infinite canvas with real-time presence, Firebase-backed.
Status: Phase 1 (Core Infrastructure) - foundational capabilities built.""",

    "proj-structure": """Root layout:
  aether-forge-app/        # Next.js 15 application
    src/app/layout.tsx     # Root layout (minimal)
    src/app/page.tsx       # Home - mounts CanvasMainStage stub
    src/hooks/             # useCanvasViewport, useRealtimePresence
    src/wdyr.ts            # Why-did-you-render tracer (missing dep in package.json)
  memory-vault/            # AI persistent state: todo.md, evolution-ledger.json, stage_outputs/
  scripts/                 # Python automation: macro-engine.py, seed-instructions.py, consolidate-memory.py
  .opencode/skills/        # Project-local skills (addyosmani lifecycle + gitnexus + ui-ux-pro-max + dashboard-designer)
  .agent-skills/           # Stage prompt files defining the build pipeline
  .gitnexus/               # GitNexus knowledge graph index (KuzuDB + Tree-sitter AST)
  .cursor/rules/           # Cursor IDE rule files (caveman, etc.)
  .windsurf/rules/         # Windsurf IDE rule files
  .clinerules/             # Cline IDE rule files""",

    "proj-commands": """All commands run from aether-forge-app/:
  npm run dev              # next dev (development server on :3000)
  npm run build            # next build (type-checks + compiles)
  npm run lint             # next lint (ESLint via next/core-web-vitals + @typescript-eslint)
  npm run format:check     # prettier --check "src/**/*.{ts,tsx,md}"
  npm run format:fix       # prettier --write "src/**/*.{ts,tsx,md}"
Root package.json is a placeholder - ignore its scripts.
No typecheck script exists - use 'npm run build' for type checking.""" ,

    "proj-config": """opencode.json: OpenCode CLI config.
  - 2 MCP servers: gitnexus, project-instructions (sqlite)
  - Plugin: superpowers (obra/superpowers)
  - Permission: bash=ask, edit=ask, read=* allow (except .env, *.key, *.pem, *.crt)
  - Skill: * allow
tsconfig.json (aether-forge-app/): strict: true, noUnusedLocals, noUnusedParameters
.eslintrc.json: @typescript-eslint/no-unused-vars=error, no-explicit-any=error, react-hooks/exhaustive-deps=warn
.prettierrc: semi, trailingComma es5, singleQuote false, tabWidth 2, printWidth 100
.gitignore: blocks node_modules, .next, .env, OS files, Firebase cache
.geminiignore: same as .gitignore plus lockfiles, analytics bundles, stale backups""",

    # ── CODE CONVENTIONS ────────────────────────────────────────────────
    "conv-typescript": """TypeScript strict mode. Rules:
  - Prefix unused params with underscore: (_req, _unused)
  - no-explicit-any is error - use `unknown` then narrow
  - no-unused-vars is error
  - Path alias: @/* maps to ./src/*
  - Prefer interfaces over types for object shapes
  - Use type for unions, intersections, primitive aliases""",

    "conv-react": """React 19 with hooks. Rules:
  - All components functional (no class components)
  - Custom hooks for reusable logic (useCanvasViewport, useRealtimePresence patterns)
  - react-hooks/exhaustive-deps = warn (not error)
  - Server Components by default in App Router (use 'use client' sparingly)
  - Use Suspense boundaries for async loading states""",

    "conv-firebase": """Firebase v10.8.0 with Firestore + Realtime Database.
  - firestore.rules: security rules for Firestore
  - database.rules.json: security rules for RTDB
  - Use Firebase Auth for authentication
  - useRealtimePresence.ts: RTDB-based cursor tracking
  - Never expose API keys client-side beyond Firebase config""",

    # ── MCP INFRASTRUCTURE ──────────────────────────────────────────────
    "mcp-overview": """Two MCP servers configured in opencode.json:
  1. gitnexus - code intelligence (knowledge graph, impact analysis, rename)
  2. project-instructions - project instructions database (SQLite)
Both auto-start with OpenCode session. Use MCP tools for context instead of reading files.""",

    "mcp-gitnexus": """GitNexus MCP exposes 7 tools for code intelligence:
  - gitnexus_impact({target: "symbolName", direction: "upstream"}) - blast radius analysis
  - gitnexus_context({name: "symbolName"}) - full symbol context
  - gitnexus_query({query: "concept"}) - search execution flows
  - gitnexus_detect_changes() - verify changes affect only expected symbols
  - gitnexus_rename({symbol: "oldName", replacement: "newName"}) - safe rename
  - gitnexus_search({query: "text"}) - text search across codebase
  - gitnexus_trace({from: "file.ts", to: "functionName"}) - trace execution
ALWAYS run impact analysis BEFORE editing any symbol.
ALWAYS run detect_changes BEFORE committing.
If index is stale: run 'gitnexus analyze' in terminal first.""",

    "mcp-instructions": """This database (project-instructions.db) stores ALL project instructions.
Tables:
  instructions(section TEXT PK, content TEXT, updated_at TEXT)
  evolution(id INTEGER PK, timestamp TEXT, agent TEXT, event_type TEXT, summary TEXT, detail TEXT)

Query pattern:
  SELECT content FROM instructions WHERE section = 'section-name';
  SELECT section FROM instructions;  -- list all available sections
  SELECT * FROM evolution ORDER BY timestamp DESC LIMIT 10;

Workflow:
  1. At session start, read AGENTS.md for minimal pointers
  2. Query instructions for specific topics as needed
  3. Record decisions in evolution table via write_query
  4. Use caveman for output compression""",

    "mcp-database": """SQLite MCP server connected to project-instructions.db.
Available tools:
  list_tables            - show all tables
  describe_table         - show schema for a table
  read_query(sql)        - execute SELECT queries
  write_query(sql)       - execute INSERT/UPDATE/DELETE (use sparingly)

For external DB (Firebase): use Firebase CLI or write custom queries via scripts/.
For Supabase integration: uncomment supabase-mcp in opencode.json and configure credentials.""",

    # ── TOKEN OPTIMIZATION ──────────────────────────────────────────────
    "token-optimization": """Three layers of token optimization:

1. INSTRUCTIONS IN DB (not AGENTS.md)
   AGENTS.md is 3.8KB (was 6.2KB). Instructions queryable on-demand via MCP.
   Only load what you need, when you need it.
   Pattern: query by section, don't dump the whole DB.

2. CAVEMAN OUTPUT COMPRESSION
   Installed via curl install script. Active by default in all responses.
   Compression levels: lite (drop filler), full (default caveman), ultra (telegraphic), wenyan
   Average ~65% output reduction, up to 87% on verbose tasks.
   Code/URLs/paths preserved byte-for-byte.
   Commands: /caveman, /caveman-stats, /caveman-compress <file>, /caveman-commit
   caveman-shrink MCP middleware available but not yet configured.

3. MCP SCHEMA OPTIMIZATION
   Current MCP servers have minimal tool counts.
   GitNexus: 7 tools. sqlite: 4 tools. Total: ~11 tools.
   If adding servers with 50+ tools, install Atlassian mcp-compressor as proxy.
   Future: wrap verbose servers with caveman-shrink (npm: caveman-shrink).""",

    "skills-reference": """All skills auto-discover at session start. Load via native `skill` tool.

Project-local (.opencode/skills/):
  addyosami/agent-skills (lifecycle): spec-driven, TDD, code-review, security, CI/CD, frontend-ui-eng
  gitnexus/*: exploring, impact-analysis, debugging, refactoring, guide, CLI
  ui-ux-pro-max: WCAG accessibility, responsive patterns, design components
  dashboard-designer: infinite canvas layout, GPU transforms, Tailwind primitives

Global (~/.config/opencode/skills/):
  farmage/opencode-skills (66 skills): 12 languages, 14 frameworks, 8 infra, 8 quality
  Anthropic frontend-design: distinctive UI aesthetics, avoid generic AI

Plugin (superpowers):
  brainstorming, writing-plans, subagent-driven-development, TDD, code-review""",

    # ── SECURITY ────────────────────────────────────────────────────────
    "security-overview": """Multi-layer security defense:
1. opencode.json permission.read: blocks .env, *.key, *.pem, *.crt
2. .gitignore: blocks secrets, build artifacts, OS files, Firebase cache
3. .geminiignore: same + AI noise (lockfiles, analytics)
4. bash=ask, edit=ask in OpenCode permissions
5. Firebase security rules at firestore.rules, database.rules.json
6. No API keys or secrets in code""",

    "security-input-validation": """All user input must be validated:
  - Never use eval() or Function() constructor
  - Validate Firebase document IDs against injection patterns
  - Sanitize input before writing to Firestore/RTDB
  - Use TypeScript type guards for runtime checks
  - For forms: validate on client + server (if API route exists)
  - Firebase Security Rules are the last line of defense - write them strict""",

    "security-auth": """Firebase Auth patterns:
  - Use Firebase Auth client SDK for sign-in/sign-up
  - Firebase Admin SDK for server-side auth (if needed)
  - Never trust client-side claims - verify via Firebase Security Rules
  - useRealtimePresence.ts uses anonymous auth for presence (read-only pattern)
  - For authenticated features: read auth.uid from Security Rules context""",

    # ── SELF-EVOLUTION ─────────────────────────────────────────────────
    "self-improvement": """Agents SHOULD evolve the system. Rules:

YOU ARE AUTHORIZED TO:
  1. Update instructions in the DB when you discover better patterns:
     write_query("UPDATE instructions SET content='...' WHERE section='...'")
  2. Add new instruction sections when you discover new concepts:
     write_query("INSERT INTO instructions (section, content) VALUES ('...', '...')")
  3. Record decisions and learnings in the evolution table:
     write_query("INSERT INTO evolution (agent, event_type, summary, detail) VALUES (...)")
  4. Create new scripts in scripts/ to automate repetitive tasks
  5. Suggest improvements: add them to memory-vault/improvements.md

SELF-EVOLUTION CYCLE:
  Learn → Record → Update → Improve
  1. Learn something about the project or tooling
  2. Record it in evolution table (event_type='learning')
  3. Update instructions DB if it's project knowledge
  4. Create/improve automation if it's a repeatable task""",

    "persistent-memory": """PERSISTENT MEMORY SYSTEM:

memory-vault/ directory:
  todo.md                    - Active task matrix + stage tracking
  evolution-ledger.json      - Historical state snapshots (macro-engine output)
  project-state-history.json - Raw state history
  stage_outputs/             - Stage completion receipts
  analytics/                 - Generated snapshots (project-state-bundle.json)

project-instructions.db (SQLite via MCP):
  instructions table         - Project instructions (queryable, updateable)
  evolution table            - Decision log, learnings, improvements

WORKFLOW:
  - Start session: read AGENTS.md, query instructions for needed sections
  - During session: write decisions to evolution table
  - End session: macro-engine.py auto-runs, snapshots state
  - Next session: read latest evolution to pick up where you left off""",

    "macro-engine": """scripts/macro-engine.py - Central aggregation script.
Run at session end (or triggered manually).
Does:
  1. Seeds instruction DB from AGENTS.md (scripts/seed-instructions.py)
  2. Runs gitnexus analyze (re-indexes code)
  3. Reads gitnexus meta.json for stats
  4. Scans project files for inventory
  5. Parses todo.md for task status
  6. Loads evolution-ledger.json
  7. Writes snapshot to memory-vault/analytics/project-state-bundle.json

Output bundle contains: environment, git, app config, tasks (completed/pending),
file inventory, gitnexus stats, ledger entries.
External AI tools can read this bundle to understand full project state.""",

    # ── DESIGN ──────────────────────────────────────────────────────────
    "design-overview": """Dashboard built on infinite canvas paradigm.
Current state: CanvasMainStage is a stub (page.tsx imports from @/components/CanvasMainStage which doesn't exist yet).
Architecture: useCanvasViewport (viewport math) + useRealtimePresence (Firebase presence) hooks exist.

Skills to use for design:
  - ui-ux-pro-max: WCAG a11y, responsive patterns, design system components
  - dashboard-designer (project-local): canvas primitives, GPU transforms
  - frontend-design (global): distinct aesthetics, avoid generic AI look

Tools discovered for future:
  - Pencil (pencil.dev): MCP-native vector canvas, design-in-IDE, bi-directional
  - tldraw SDK: infinite canvas for React, $10M funded, 47K stars
  - React Infinite Canvas: npm package for canvas component""",

    "design-system": """Tech: Tailwind 4 + lucide-react icons (v0.400.0).
Dark theme. GPU-accelerated transforms (translate3d).
Type-safe TypeScript.

Component patterns:
  - Use React 19 concurrent features where appropriate
  - Suspense boundaries for async canvas operations
  - Canvas components should be 'use client'
  - Viewport state managed via useCanvasViewport hook
  - Presence data via useRealtimePresence hook
  - Keep components small, focused, composable""",

    # ── WORKFLOW ────────────────────────────────────────────────────────
    "workflow-onboarding": """NEW AGENT ONBOARDING - do this at session start:
1. Read AGENTS.md (minimal - 3.8KB, takes ~950 tokens)
2. Query instructions DB for sections relevant to your task:
   SELECT content FROM instructions WHERE section = 'proj-structure';
   SELECT content FROM instructions WHERE section = 'mcp-overview';
3. List gitnexus context for code awareness:
   gitnexus_query({query: "user task keywords"})
4. Check todo.md for active tasks
5. Load relevant skills via `skill` tool
6. Start working""",

    "workflow-task": """TASK WORKFLOW:
1. Understand: query instructions + gitnexus context
2. Plan: consult todo.md, check evolution ledger for context
3. Execute: make changes, run lint/format
4. Record: write decision to evolution table
5. Verify: run 'npm run build' from aether-forge-app/ for type check
6. Repeat: check if more tasks remain in todo.md""",

    # ── TROUBLESHOOTING ────────────────────────────────────────────────
    "troubleshooting": """Common issues and fixes:
  - wdyr.ts throws at import: npm package @welldone-software/why-did-you-render missing
  - 'npm run dev' fails: check node_modules exists, run 'npm install' in aether-forge-app/
  - GitNexus tools unavailable: run 'gitnexus analyze' in repo root
  - MCP server fails: check opencode.json config, restart OpenCode
  - Type errors: aether-forge-app/ npm run build validates types
  - Firebase auth errors: check firebase.json and firestore.rules""",

    # ── UNKNOWN - fallback for agents ──────────────────────────────────
    "fallback-check": """If you're unsure about anything:
1. Check AGENTS.md for minimal pointers
2. Query instructions DB: SELECT section FROM instructions;
3. Search codebase via gitnexus_search
4. Check todo.md for active task context
5. Check evolution-ledger.json for state history
6. Ask user for clarification before guessing""",
}


def seed_instructions(conn):
    for section, content in INSTRUCTIONS.items():
        upsert(conn, section, content)
    conn.commit()

    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM instructions")
    count = c.fetchone()[0]
    print(f"Seeded {count} instruction sections")
    for row in c.execute("SELECT section FROM instructions ORDER BY section"):
        print(f"  - {row[0]}")


def seed_evolution_table(conn):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM evolution")
    if c.fetchone()[0] == 0:
        c.execute(
            """INSERT INTO evolution (agent, event_type, summary, detail)
               VALUES (?, ?, ?, ?)""",
            ("seed-instructions.py", "system-init",
             "Initialized comprehensive instruction database",
             "Created 25 instruction sections + evolution table schema"),
        )
        conn.commit()
        print("Added initial evolution entry")


def main():
    conn = get_connection()
    ensure_tables(conn)
    seed_instructions(conn)
    seed_evolution_table(conn)
    conn.close()

    db_size = os.path.getsize(DB_PATH)
    print(f"DB size: {db_size} bytes ({db_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
