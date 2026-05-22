# Aether_Forge — agent guide

## Instructions in DB

All instructions in `memory-vault/project-instructions.db`. Query via `project-instructions` MCP:

```sql
read_query("SELECT section FROM instructions")                       -- list all
read_query("SELECT content FROM instructions WHERE section='X'")     -- read one
```

Prefix groups: proj-*, conv-*, mcp-*, token-*, skills-*, security-*, design-*, workflow-*, self-*, fallback-*

## Start

1. `read_query("SELECT section FROM instructions")` — see what's available
2. Check `memory-vault/todo.md`
3. Load relevant skill via `skill` tool
4. `read_query("SELECT * FROM evolution ORDER BY id DESC LIMIT 5")` — recent context

## Self-Evolution

Authorized to evolve: record decisions (`INSERT INTO evolution`), update instructions (`UPDATE instructions`), add sections, create `scripts/`, suggest in `memory-vault/improvements.md`.

## End

`python scripts/macro-engine.py` — snapshot state.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **AETHER_FORGE** (281 symbols, 303 relationships, 1 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/AETHER_FORGE/context` | Codebase overview, check index freshness |
| `gitnexus://repo/AETHER_FORGE/clusters` | All functional areas |
| `gitnexus://repo/AETHER_FORGE/processes` | All execution flows |
| `gitnexus://repo/AETHER_FORGE/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
