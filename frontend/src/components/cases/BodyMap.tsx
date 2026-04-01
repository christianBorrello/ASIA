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
      <h3 className="text-sm font-semibold text-[var(--color-text-secondary)] mb-4 flex items-center gap-2">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
        </svg>
        Mappa anatomica
      </h3>

      {/* Dog silhouette with hotspots */}
      <div className="relative w-full aspect-[16/10] bg-gradient-to-b from-primary/[0.02] to-primary/[0.06] rounded-xl overflow-hidden border border-[var(--color-border)]">
        {/* Dog silhouette SVG */}
        <svg
          viewBox="0 0 400 250"
          className="absolute inset-0 w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Simplified dog silhouette - side view */}
          <path
            d="M85 140 C75 130, 70 115, 75 105 C78 98, 82 92, 88 88
               C92 85, 95 78, 92 72 C90 68, 88 62, 92 58
               C96 54, 102 52, 108 55 C112 57, 115 60, 118 62
               C125 58, 135 56, 145 58
               C155 60, 165 65, 172 70
               C180 75, 195 78, 210 80
               C230 83, 250 85, 270 84
               C290 83, 305 80, 315 78
               C322 75, 328 72, 332 68
               C336 62, 340 58, 338 52
               C336 46, 330 42, 325 44
               C320 46, 318 52, 320 58
               C318 62, 315 65, 312 68
               C305 78, 295 85, 290 92
               C285 100, 282 110, 280 120
               C278 135, 275 148, 278 160
               C280 168, 285 175, 288 182
               C290 188, 292 195, 288 200
               C284 204, 278 202, 276 198
               C273 192, 272 185, 270 178
               C268 170, 265 162, 260 158
               C250 162, 240 165, 230 168
               C220 172, 200 175, 180 172
               C165 170, 155 168, 148 165
               C142 162, 138 165, 135 170
               C132 178, 130 185, 128 192
               C127 198, 125 205, 120 208
               C115 212, 110 208, 112 202
               C114 196, 118 188, 120 180
               C122 170, 118 160, 110 155
               C100 150, 92 148, 85 140 Z"
            fill="currentColor"
            stroke="currentColor"
            strokeWidth="1.5"
            className="text-primary/10"
          />
          {/* Tail */}
          <path
            d="M85 140 C78 132, 65 128, 55 135 C48 140, 42 148, 45 155"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            className="text-primary/20"
            strokeLinecap="round"
          />
          {/* Eye */}
          <circle cx="330" cy="50" r="3" fill="currentColor" className="text-primary/30" />
          {/* Ear */}
          <path
            d="M315 42 C312 32, 318 25, 325 28 C330 30, 332 36, 330 42"
            fill="currentColor"
            stroke="currentColor"
            strokeWidth="1"
            className="text-primary/15"
          />
        </svg>

        {/* Hotspots */}
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

              {/* Finding count badge */}
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
            bg-[var(--color-text)] text-white text-xs font-medium shadow-lg
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
                  : "text-[var(--color-text-secondary)] hover:bg-black/5"
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
