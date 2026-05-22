---
skill_id: "aether_forge_project_analyzer"
tier: "ManyIH-Tier-2"
---

# Aether_Forge Project Analyzer

## 1. Stack Identity
- **Framework:** Next.js 15 (App Router), React 19
- **Language:** TypeScript strict mode
- **Styling:** Tailwind CSS 4
- **Backend:** Firebase 10.8 (Firestore + Realtime Database)
- **Runtime:** Node.js 22

## 2. Code Quality Configuration

### ESLint (`.eslintrc.json`)
- Extends: `next/core-web-vitals`, `plugin:@typescript-eslint/recommended`
- `@typescript-eslint/no-unused-vars`: error (prefix discard params with `_`)
- `@typescript-eslint/no-explicit-any`: error (use `unknown` then narrow)
- `react-hooks/exhaustive-deps`: warn

### Prettier (`.prettierrc`)
- `semi`: true, `trailingComma`: es5, `singleQuote`: false
- `tabWidth`: 2, `printWidth`: 100
- Ignored: `.next/`, `node_modules/`, `out/`, `build/`

### TypeScript (`tsconfig.json`)
- `strict: true`, `noUnusedLocals: true`, `noUnusedParameters: true`
- Path alias: `@/*` → `./src/*`
- Target: ES2022, moduleResolution: bundler

### Commands (run from `aether-forge-app/`)
- `npm run lint` — ESLint check
- `npm run format:check` — Prettier dry-run
- `npm run format:fix` — Prettier auto-format
- `npx tsc --noEmit` — TypeScript strict type check

## 3. Project Structure

```
aether-forge-app/
  src/
    app/layout.tsx         # Root layout
    app/page.tsx           # Home (mounts CanvasMainStage)
    components/            # Canvas components (CanvasMainStage stub)
    hooks/                 # useCanvasViewport, useRealtimePresence
    wdyr.ts                # Why-did-you-render tracer
  .eslintrc.json
  .prettierrc
  .prettierignore
  tsconfig.json
  next.config.ts
  package.json

.idx/dev.nix               # Nix environment (nodejs_22, ESLint/Prettier extensions, previews)
memory-vault/              # AI persistent state
  todo.md
  evolution-ledger.json
  project-instructions.db
  stage_outputs/
scripts/                   # Python automation scripts
.opencode/skills/          # Project-local skills
.agent-skills/             # Stage prompt files
.gitnexus/                 # GitNexus knowledge graph
```

## 4. Key Dependencies
- next@15.5.0, react@19.0.0, react-dom@19.0.0
- firebase@10.8.0, typescript@5.4.2, tailwindcss@4.0.0
- prettier@3.2.5 (dev), lucide-react@0.400.0

## 5. Verification Checklist
- [ ] `.eslintrc.json` enforces `no-explicit-any` error, `no-unused-vars` error with `_` prefix
- [ ] `.prettierrc` matches project style (semi, singleQuote, tabWidth, printWidth)
- [ ] TypeScript strict mode enabled (`strict: true`, `noUnusedLocals`, `noUnusedParameters`)
- [ ] `@/*` path alias resolves to `./src/*`
- [ ] `.idx/dev.nix` has nodejs_22, ESLint/Prettier extensions, onCreate hook, preview config
- [ ] GitNexus index is synced (`npx gitnexus analyze` from project root)
