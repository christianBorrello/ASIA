"use client";

import type { EvidenceLevel as EvidenceLevelType } from "@/lib/types";
import { EVIDENCE_CONFIG } from "@/lib/constants";

interface EvidenceLevelProps {
  level: EvidenceLevelType;
  studyCount?: number | null;
  totalSampleSize?: number | null;
  compact?: boolean;
}

export default function EvidenceLevel({
  level,
  studyCount,
  totalSampleSize,
  compact = false,
}: EvidenceLevelProps) {
  const config = EVIDENCE_CONFIG[level];
  if (!config) return null;

  if (compact) {
    return (
      <span
        className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-semibold
          ${config.bg} ${config.color} border ${config.border}`}
      >
        {level}
      </span>
    );
  }

  return (
    <div
      className={`inline-flex items-center gap-3 px-4 py-2.5 rounded-lg border
        ${config.bg} ${config.color} ${config.border}`}
    >
      <div className="flex items-center gap-1.5">
        <div
          className={`w-2.5 h-2.5 rounded-full ${
            level === "ALTO"
              ? "bg-emerald-500"
              : level === "MODERATO"
              ? "bg-amber-500"
              : "bg-red-500"
          }`}
        />
        <span className="font-semibold text-sm">{config.label}</span>
      </div>

      {(studyCount || totalSampleSize) && (
        <span className="text-xs opacity-75">
          {studyCount && `${studyCount} studi`}
          {studyCount && totalSampleSize && " \u00B7 "}
          {totalSampleSize && `n=${totalSampleSize}`}
        </span>
      )}
    </div>
  );
}
