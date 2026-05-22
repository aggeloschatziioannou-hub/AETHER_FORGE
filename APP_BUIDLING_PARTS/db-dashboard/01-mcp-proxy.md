# 01-mcp-proxy.md

## MCP Proxy Backend (Python/FastAPI)

### Purpose:
- Isolate DB credentials and connections from UI for security and maintainability
- Provide safe, flexible workflow backend logic
- Support pluggable skills/AI-powered tools via MCP interface
- Guarantee zero writes unless explicitly allowed, robust logging

### Key Functions:
- Secure DB connection pool/router (Postgres, SQLite, etc.), NixOS-safe
- REST endpoints for query, schema, introspection, config
- Plugin loader for db-specific logic, skill hooks
- Built-in workflow step logging, opaque to UI (audit-grade)
- Result hydration for infinite-canvas consumption (e.g., blockwise streaming, lazy load)

### Tech stack:
- Python 3.11+, FastAPI
- Pure Python for NixOS compatibility
- Optional: Local subprocess bridge (for psql/sqlite shell utilities if needed)

### Example API shape:
- `/query` (POST): run arbitrary safe SQL, params: `db`, `sql`, `args`, `limit`
- `/list-tables` (GET): `db`
- `/introspect-table` (GET): `db`, `table`
- `/metrics` (GET): system, perf, connection health
- `/step-log` (POST): workflow/audit event
