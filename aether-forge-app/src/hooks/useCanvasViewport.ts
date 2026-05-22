import { useState, useCallback, useRef, MouseEvent, WheelEvent } from "react";

interface Coordinate {
  x: number;
  y: number;
}

interface CanvasViewportState {
  panOffset: Coordinate;
  zoomScale: number;
  isDragging: boolean;
}

export const useCanvasViewport = (
  minZoom: number = 0.15,
  maxZoom: number = 3.00
) => {
  const [viewport, setViewport] = useState<CanvasViewportState>({
    panOffset: { x: 0, y: 0 },
    zoomScale: 1.0,
    isDragging: false,
  });

  // Mutable tracking references to bypass React re-render batch loops during ultra-rapid mouse ticks
  const dragStartRef = useRef<Coordinate>({ x: 0, y: 0 });
  const panStartRef = useRef<Coordinate>({ x: 0, y: 0 });

  // 1. Capture Entry Vector for Drag-Panning Operations
  const handlePointerDown = useCallback((e: MouseEvent<HTMLDivElement>) => {
    // Restrict viewport panning operations strictly to left-click interactions on empty space
    if (e.button !== 0) return;

    setViewport((prev) => {
      dragStartRef.current = { x: e.clientX, y: e.clientY };
      panStartRef.current = { ...prev.panOffset };
      return { ...prev, isDragging: true };
    });
  }, []);

  // 2. Compute Active Translation Deltas relative to Vector Path Movements
  const handlePointerMove = useCallback((e: MouseEvent<HTMLDivElement>) => {
    setViewport((prev) => {
      if (!prev.isDragging) return prev;

      const deltaX = e.clientX - dragStartRef.current.x;
      const deltaY = e.clientY - dragStartRef.current.y;

      return {
        ...prev,
        panOffset: {
          x: panStartRef.current.x + deltaX,
          y: panStartRef.current.y + deltaY,
        },
      };
    });
  }, []);

  // 3. Sever Viewport Pan Capturing State
  const handlePointerUp = useCallback(() => {
    setViewport((prev) => ({ ...prev, isDragging: false }));
  }, []);

  // 4. Calculate Trigonometric Scale Transformations Anchored Exactly Over Your Pixel Cursor Focus
  const handleWheelZoom = useCallback(
    (e: WheelEvent<HTMLDivElement>) => {
      e.preventDefault();

      const containerBounds = e.currentTarget.getBoundingClientRect();
      const mouseX = e.clientX - containerBounds.left;
      const mouseY = e.clientY - containerBounds.top;

      setViewport((prev) => {
        // Enforce deterministic scaling multipliers
        const zoomIntensity = 0.05;
        const wheelDelta = -e.deltaY;
        const factor = Math.exp(wheelDelta * zoomIntensity * 0.01);
        
        // Impose strict maximum/minimum scale ceiling clamps
        const targetZoom = Math.min(Math.max(prev.zoomScale * factor, minZoom), maxZoom);
        
        if (targetZoom === prev.zoomScale) return prev;

        // Shift pan offsets proportionally to retain spatial anchoring over pixel focus
        const ratio = targetZoom / prev.zoomScale;
        const nextPanX = mouseX - (mouseX - prev.panOffset.x) * ratio;
        const nextPanY = mouseY - (mouseY - prev.panOffset.y) * ratio;

        return {
          isDragging: prev.isDragging,
          zoomScale: targetZoom,
          panOffset: { x: nextPanX, y: nextPanY },
        };
      });
    },
    [minZoom, maxZoom]
  );

  return {
    viewport,
    handlePointerDown,
    handlePointerMove,
    handlePointerUp,
    handleWheelZoom,
  };
};