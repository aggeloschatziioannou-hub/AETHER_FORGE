"use client";

import React, { useState, useEffect } from "react";

interface InstructionPayload {
  status: string;
  target_resource: string;
  tables: Array<{ name: string }>;
}

export default function InstructionExplorer() {
  const [dataState, setDataState] = useState<InstructionPayload | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/instructions")
      .then((res) => res.json())
      .then((data) => {
        setDataState(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="w-screen h-screen flex items-center justify-center bg-zinc-950 font-mono text-xs text-zinc-500 tracking-widest animate-pulse">
        SWEEPING_INSTRUCTION_RELATIONAL_MATRICES...
      </div>
    );
  }

  return (
    <div className="w-screen h-screen bg-zinc-950 text-zinc-300 font-mono p-8 overflow-y-auto selection:bg-blue-500 selection:text-white">
      {/* Upper Status HUD Display Panel */}
      <div className="mb-8 p-4 rounded border border-zinc-800 bg-zinc-900/40 backdrop-blur-md shadow-xl">
        <div className="flex items-center gap-2 text-sm font-bold text-zinc-100 tracking-wide">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
          AETHER_FORGE // KNOWLEDGE_BASE_EXPLORER
        </div>
        <p className="text-[11px] text-zinc-500 mt-1.5 uppercase">
          Source Disk: <span className="text-zinc-400">{dataState?.target_resource || "project-instructions.db"}</span> // Engine Status: <span className="text-emerald-400">{dataState?.status || "READY"}</span>
        </p>
      </div>

      {/* Main UI System Grid Structure */}
      <div className="grid grid-cols-4 gap-6">
        {/* Left-Hand Sidebar Navigation Tree Column */}
        <div className="col-span-1 border border-zinc-800 rounded p-4 bg-zinc-900/10 min-h-[400px]">
          <h2 className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-4">Relational Tables</h2>
          <ul className="space-y-2 text-xs">
            {dataState?.tables?.map((item, index) => (
              <li 
                key={index} 
                className="flex items-center gap-2 p-2.5 rounded bg-zinc-900/50 border border-zinc-800/60 cursor-pointer hover:border-blue-500 transition-colors"
              >
                <span className="text-blue-500 text-xs">⚡</span>
                <span className="text-zinc-300 font-semibold">{item.name}</span>
              </li>
            ))}
            <li className="flex items-center gap-2 p-2.5 rounded bg-zinc-900/20 border border-zinc-800/40 opacity-60">
              <span className="text-zinc-500 text-xs">📁</span>
              <span className="text-zinc-500 font-mono">instruction_blocks (25 Loaded)</span>
            </li>
          </ul>
        </div>

        {/* Right-Hand Target Document Inspector Core Frame */}
        <div className="col-span-3 border border-zinc-800 rounded p-6 bg-zinc-900/10">
          <h2 className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-4">Active Instruction Payload</h2>
          <div className="p-4 rounded bg-zinc-950 border border-zinc-900 font-mono text-xs text-zinc-400 leading-relaxed shadow-inner">
            Select an instruction configuration schema node from the left navigation tree path index panel to run live database table queries...
          </div>
        </div>
      </div>
    </div>
  );
}