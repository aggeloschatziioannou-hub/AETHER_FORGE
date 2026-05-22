---
name: lint-and-format
description: Use when running linting, formatting, or type-checking on the Aether_Forge project. Use before committing, after making changes, or when CI reports style/type errors. Use when you need to enforce the project's ESLint, Prettier, or TypeScript strict rules.
---

# Lint and Format

## Overview

Aether_Forge uses three automated quality gates: ESLint (Next.js + TypeScript rules), Prettier (opinionated formatting), and `tsc --noEmit` (strict type checking). All three must pass before any change enters the codebase.

## Quality Gates

| Gate | Command | Config File | Checks |
|------|---------|-------------|--------|
| Lint | `npm run lint` (from `aether-forge-app/`) | `.eslintrc.json` | TypeScript strict, no-explicit-any, no-unused-vars (prefix with `_`), React hooks exhaustiveness |
| Format | `npm run format:check` / `format:fix` | `.prettierrc` | Semicolons on, single quotes off, tabWidth 2, printWidth 100 |
| Types | `npx tsc --noEmit` | `tsconfig.json` | strict: true, noUnusedLocals, noUnusedParameters, noUncheckedIndexedAccess |

## Running Checks

```bash
# From the project root or aether-forge-app directory
cd aether-forge-app

# Lint only
npm run lint

# Format check (dry-run)
npm run format:check

# Auto-format all
npm run format:fix

# Type-check (strict)
npx tsc --noEmit

# Full quality gate (all three)
npm run lint && npm run format:check && npx tsc --noEmit
```

## ESLint Rules (`.eslintrc.json`)

- `@typescript-eslint/no-unused-vars`: `error` — prefix unused params with `_`
- `@typescript-eslint/no-explicit-any`: `error` — use `unknown` then narrow
- `react-hooks/exhaustive-deps`: `warn` — missing React hook deps
- Extends: `next/core-web-vitals`, `plugin:@typescript-eslint/recommended`

## Prettier Config (`.prettierrc`)

- `semi`: true
- `trailingComma`: es5
- `singleQuote`: false
- `tabWidth`: 2
- `printWidth`: 100

## TypeScript Strict Mode

- `strict: true` in tsconfig.json
- `noUnusedLocals: true` — error on unused local variables
- `noUnusedParameters: true` — error on unused params (prefix with `_`)
- `@/*` path alias maps to `./src/*`

## Common Mistakes

- **Skipping format check:** Always run `format:check` before committing. CI will reject formatting drift.
- **Using `any`:** Banned. Use `unknown` and narrow with type guards.
- **Unused parameters without `_` prefix:** `noUnusedParameters: true` will fail. Prefix discard params with `_` (e.g., `_req`, `_unused`).
- **Running from wrong directory:** All commands above must run inside `aether-forge-app/`.

## CI Integration

CI pipeline enforces these gates before merge. If CI fails on lint/format/types, fix locally and re-push. Do not bypass.
