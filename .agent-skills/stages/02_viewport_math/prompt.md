### 🛰️ FEATURE SPEC:useCanvasViewport Subsystem

#### 1. INTENT SIGNATURE (Agentic JTBD)
- **When:** A user pans, trackpad-drags, or scrolls mouse-wheel zoom actions across the interactive Aether_Forge workspace grid layout,
- **I want to:** Continuously intercept event coordinates and compute clamped vector transformations within isolated React 19 client states,
- **So that:** The visual layer updates smoothly at a constant 60 FPS performance budget with absolute cursor focus anchoring.

#### 2. DATA CONTRACT & TRANSIENT STATE PROPERTIES
- `panOffset`: Coordinate pixel coordinate map `{ x: number, y: number }` tracking active navigation offsets.
- `zoomScale`: Floating-point scale scalar bounded strictly between a macro ceiling of `3.00` and a micro floor of `0.15` to prevent rendering overflow anomalies.
- `isDragging`: Binary toggle flag indicating if the viewport backdrop is currently experiencing an active drag-panning interaction.