"use client";

import { useState } from "react";
import { BODY_SYSTEMS } from "@/lib/constants";
import type { BodySystemFinding } from "@/lib/types";

interface Props {
  findings?: Record<string, BodySystemFinding[]>;
  onSystemClick: (systemId: string) => void;
  activeSystem?: string | null;
}

export default function BodyMap({ findings = {}, onSystemClick, activeSystem }: Props) {
  const [hoveredSystem, setHoveredSystem] = useState<string | null>(null);

  return (
    <div className="card p-6">
      <h3 className="text-sm font-semibold text-gray-500 mb-4 flex items-center gap-2">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
        </svg>
        Mappa anatomica
      </h3>

      {/* Dog silhouette with hotspots */}
      <div className="relative w-full aspect-square bg-gradient-to-b from-primary/[0.02] to-primary/[0.04] rounded-xl overflow-hidden border border-gray-200">
        {/* Dog SVG as background image */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src="/dog-silhouette.svg"
          alt="Silhouette anatomica cane"
          className="absolute inset-0 w-full h-full object-contain p-4 pointer-events-none select-none"
          draggable={false}
        />

        {/* Hotspots positioned over the dog */}
        {BODY_SYSTEMS.map((system) => {
          const hasFinding = (findings[system.id]?.length || 0) > 0;
          const isActive = activeSystem === system.id;
          const isHovered = hoveredSystem === system.id;

          return (
            <button
              key={system.id}
              onClick={() => onSystemClick(system.id)}
              onMouseEnter={() => setHoveredSystem(system.id)}
              onMouseLeave={() => setHoveredSystem(null)}
              style={{
                top: system.position.top,
                left: system.position.left,
                backgroundColor: `${system.color}22`,
                borderColor: isActive || isHovered ? system.color : `${system.color}66`,
              }}
              className={`body-map-hotspot
                ${isActive ? "body-map-hotspot-active scale-125" : ""}
                ${hasFinding ? "body-map-hotspot-has-findings" : ""}
                border-2`}
              aria-label={system.name_it}
              title={system.name_it}
            >
              <span className="text-base">{system.emoji}</span>
              {hasFinding && (
                <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-emerald-500 text-white
                  text-[9px] font-bold flex items-center justify-center">
                  {findings[system.id].length}
                </span>
              )}
            </button>
          );
        })}

        {/* Hover tooltip */}
        {hoveredSystem && (
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2 px-3 py-1.5 rounded-lg
            bg-gray-900 text-white text-xs font-medium shadow-lg
            pointer-events-none z-20 whitespace-nowrap">
            {BODY_SYSTEMS.find((s) => s.id === hoveredSystem)?.name_it}
          </div>
        )}
      </div>

      {/* System legend */}
      <div className="mt-4 grid grid-cols-3 sm:grid-cols-4 gap-2">
        {BODY_SYSTEMS.map((system) => {
          const hasFinding = (findings[system.id]?.length || 0) > 0;
          return (
            <button
              key={system.id}
              onClick={() => onSystemClick(system.id)}
              className={`flex items-center gap-1.5 px-2 py-1.5 rounded-lg text-xs transition-all
                min-h-[44px]
                ${activeSystem === system.id
                  ? "bg-primary/10 text-primary font-medium"
                  : "text-gray-500 hover:bg-black/5"
                }
                ${hasFinding ? "ring-1 ring-emerald-300" : ""}`}
            >
              <span>{system.emoji}</span>
              <span className="truncate">{system.name_it.replace("Apparato ", "").replace("Sistema ", "")}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
