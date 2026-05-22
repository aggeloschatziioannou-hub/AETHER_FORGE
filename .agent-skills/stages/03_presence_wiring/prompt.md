### 🛰️ FEATURE SPEC: useRealtimePresence Subsystem

#### 1. INTENT SIGNATURE (Agentic JTBD)
- **When:** An authenticated user activates a session window or navigates their cursor across the infinite canvas,
- **I want to:** Debounce cursor coordinates and stream transient session metrics to `/presence/{canvasId}/{userId}` via the Firebase Realtime Database SDK,
- **So that:** All concurrent user viewports render collaborative telemetry inside a 100ms throttle boundary with automatic lifecycle cleanup upon disconnect.

#### 2. DATA CONTRACT & TRANSIENT STATE PROPERTIES
- **Local Reactive Coordinates:** Track incoming multi-user cursor pools using an object mapping: `Record<string, { x: number, y: number, viewportOffset: { x: number, y: number }, lastActive: number }>`
- **Network Performance Ceilings:** - Throttling: Local pointer events must pass through a strict **100ms throttle filter** to prevent token velocity spikes (>100 mutations/sec) and database read/write cost scaling.
  - Lifecycle Hook: Must call `onDisconnect()` to programmatically purge the transient node path from the global RTDB cluster when a connection severs, preventing phantom cursor leakage.