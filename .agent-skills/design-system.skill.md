---
skill_id: "aether_forge_design_system_primitive"
tier: "ManyIH-Tier-2"
---

# 🎨 DESIGN SYSTEM CONSTRAINT PRIMITIVE

## 1. INFINITE CANVAS VISUAL PARAMETERS
- **Grid Pattern:** Linear CSS repeating-linear-gradient grid lines.
- **Grid Subdivisions:** 20px primary blocks, 100px major accent containers.
- **Tailwind Theme Primitives:**
  - Canvas background: `bg-zinc-950`
  - Minor Grid Lines: `stroke-zinc-800/40`
  - Major Grid Lines: `stroke-zinc-700/60`
  - Active Dragging State: `cursor-grabbing selection-none border-blue-500`

## 2. CONSTRAINT VERIFICATION MATRIX
Before presenting an interface modification candidate to the user:
1. CHECK: Does the layout component strictly respect our absolute zoom scale bounds (0.15 to 3.00)?
2. VERIFY: Are interactive node elements wrapped inside React 19 concurrent boundaries (`<Suspense>`) to block frame stuttering?
3. REJECT: Any hardcoded inline padding or arbitrary styling elements that bypass our centralized Tailwind theme array.