"use client";

import { CanvasMainStage } from "@/components/CanvasMainStage";
import { useState, useEffect } from "react";
import "@/wdyr"; // Initialize the agent's rendering optimization tracer

export default function Home() {
  // Mock authentication profiles to satisfy our real-time security perimeters
  const [session, setSession] = useState<{ userId: string; canvasId: string } | null>(null);

  useEffect(() => {
    // Generate transient sandbox credentials for testing purposes
    setSession({
      userId: `user_dev_${Math.random().toString(36).substring(2, 7)}`,
      canvasId: "canvas_primary_matrix",
    });
  }, []);

  if (!session) {
    return (
      <div className="w-screen h-screen flex items-center justify-center bg-zinc-950 font-mono text-xs text-zinc-500">
        INITIALIZING_AETHER_FORGE_CONTEXT...
      </div>
    );
  }

  return (
    <main className="w-screen h-screen overflow-hidden relative bg-zinc-950">
      {/* Upper Status Panel HUD Overlay */}
      <div className="absolute top-4 left-4 z-50 p-3 rounded-md border border-zinc-800/80 bg-zinc-900/90 text-[11px] font-mono text-zinc-400 backdrop-blur-md pointer-events-none shadow-xl">
        <div className="flex items-center gap-2 mb-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-zinc-200 font-bold tracking-wider">AETHER_FORGE // CONTROL_HUD</span>
        </div>
        ID: <span className="text-blue-400">{session.userId}</span><br />
        CHROME_STAGE: <span className="text-zinc-300">ACTIVE</span>
      </div>

      {/* Mount the Core Infinite Layout Canvas Matrix Components */}
      <CanvasMainStage 
        canvasId={session.canvasId}
        userId={session.userId}
        isAuthenticated={true}
      />
    </main>
  );
}