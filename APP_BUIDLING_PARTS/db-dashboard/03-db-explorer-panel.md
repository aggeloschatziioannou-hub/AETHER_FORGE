# 03-db-explorer-panel.md

## DB Explorer Panel Spec

### Purpose
- Provide a fast, interactive way to browse, search, and inspect DBs/schemas/tables/records
- Point-and-click SQL query builder & result viewer
- Both basic (SQLite/Postgres) and extensible for future DBs

### Core Features
- List DBs, schemas, tables (tree or explorer)
- Browse records (paginated, block-load)
- Table/column introspection
- Safe inline SQL query runner (with MCP limit/sandbox)
- Result rendering: table/grid, JSON, chart preview
- Actions: download .csv, preview as panel, copy SQL

### UI Integration
- Panel launches with DB connection context
- Snap-in UI for multi-panel workflows
- Skill hooks for automations (e.g., auto-inspect, suggest SQL)
- All actions go through MCP proxy for security/logging

### Extensibility
- Registry API to let others define new DB types, custom views, data-mapping panels
