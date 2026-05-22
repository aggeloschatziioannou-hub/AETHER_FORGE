### 🛰️ FEATURE SPEC: Environment and Tooling Fortification Subsystem

#### 1. INTENT SIGNATURE (Agentic JTBD)
- **When:** Initializing or re-building the Aether_Forge developer terminal environment within Project IDX,
- **I want to:** Declaratively inject system binaries, register automated lifecycle hooks, and mount code-quality linting extensions in `.idx/dev.nix`,
- **So that:** The workspace instantiates an isolated, reproducible serverless development state with automated linting perimeters on every boot loop.

#### 2. DATA CONTRACT & ENVIRONMENT PROPERTIES
- **Binary Whitelist:** Enforce absolute version declarations for runtime engines (`pkgs.nodejs_22`).
- **Lifecycle Hook (onCreate):** Must programmatically trigger automated package management routines (`npm install`) within the client sandbox subfolder (`aether-forge-app`) to prevent dependency fragmentation.
- **Visual & Linting Matrix Extensions:**
  - ESLint Protocol Engine: `dbaeumer.vscode-eslint`
  - Prettier Compactor: `esbenp.prettier-vscode`