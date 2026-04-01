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
      <div className="relative w-full aspect-[5/3] bg-gradient-to-b from-primary/[0.02] to-primary/[0.05] rounded-xl overflow-hidden border border-gray-200">
        {/* Dog silhouette SVG — side view, head RIGHT, tail LEFT */}
        <svg
          viewBox="0 0 500 300"
          className="absolute inset-0 w-full h-full p-4"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Body */}
          <ellipse cx="250" cy="145" rx="130" ry="60" className="fill-primary/[0.07] stroke-primary/20" strokeWidth="1.5" />

          {/* Neck */}
          <path d="M370 120 Q390 100, 400 80 Q405 70, 410 75 Q415 80, 410 95 Q400 115, 385 130"
            className="fill-primary/[0.07] stroke-primary/20" strokeWidth="1.5" />

          {/* Head */}
          <ellipse cx="420" cy="68" rx="35" ry="28" className="fill-primary/[0.07] stroke-primary/20" strokeWidth="1.5" />

          {/* Muzzle */}
          <ellipse cx="452" cy="75" rx="18" ry="12" className="fill-primary/[0.07] stroke-primary/20" strokeWidth="1.5" />

          {/* Nose */}
          <circle cx="468" cy="73" r="4" className="fill-primary/30" />

          {/* Eye */}
          <circle cx="430" cy="62" r="4" className="fill-primary/30" />

          {/* Ear */}
          <path d="M405 48 Q398 25, 410 20 Q420 18, 422 35 Q423 45, 418 50"
            className="fill-primary/[0.10] stroke-primary/20" strokeWidth="1.5" />

          {/* Front leg left */}
          <path d="M340 185 Q338 210, 340 240 Q341 255, 348 258 Q355 260, 355 255 Q354 245, 350 240 Q348 220, 350 200"
            className="fill-primary/[0.05] stroke-primary/20" strokeWidth="1.5" />

          {/* Front leg right */}
          <path d="M360 185 Q358 215, 360 240 Q361 255, 368 258 Q375 260, 375 255 Q374 245, 370 240 Q368 220, 370 200"
            className="fill-primary/[0.05] stroke-primary/20" strokeWidth="1.5" />

          {/* Hind leg left */}
          <path d="M155 175 Q145 195, 140 215 Q135 235, 138 250 Q140 258, 148 260 Q155 260, 155 252 Q153 240, 155 225 Q160 205, 165 190"
            className="fill-primary/[0.05] stroke-primary/20" strokeWidth="1.5" />

          {/* Hind leg right */}
          <path d="M170 180 Q162 200, 158 220 Q154 240, 157 252 Q159 260, 167 262 Q174 262, 174 254 Q172 242, 174 228 Q178 208, 182 195"
            className="fill-primary/[0.05] stroke-primary/20" strokeWidth="1.5" />

          {/* Tail */}
          <path d="M120 130 Q90 110, 75 85 Q68 72, 72 68"
            fill="none" className="stroke-primary/20" strokeWidth="3" strokeLinecap="round" />

          {/* Belly line */}
          <path d="M170 195 Q250 205, 340 195"
            fill="none" className="stroke-primary/10" strokeWidth="1" strokeDasharray="4 4" />
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
