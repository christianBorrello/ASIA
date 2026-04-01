"use client";

import type { Source } from "@/lib/types";

interface Props {
  sources: Source[];
  activeCitation?: number | null;
  onCitationClick?: (id: number) => void;
}

function studyTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    meta_analysis: "Meta-analisi",
    rct: "RCT",
    prospective_multicenter: "Prospettico multicentrico",
    prospective: "Prospettico",
    retrospective: "Retrospettivo",
    case_series: "Serie di casi",
    case_report: "Case report",
    review: "Review",
  };
  return labels[type] || type;
}

export default function SourcePanel({ sources, activeCitation, onCitationClick }: Props) {
  if (!sources.length) return null;

  return (
    <div className="card divide-y divide-[var(--color-border)]">
      <div className="px-4 py-3 flex items-center gap-2">
        <svg className="w-4 h-4 text-[var(--color-text-muted)]" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
        </svg>
        <h3 className="text-sm font-semibold text-[var(--color-text-secondary)]">
          Fonti ({sources.length})
        </h3>
      </div>

      {sources.map((source, index) => {
        const citId = source.citation_id ?? source.id ?? (index + 1);
        const author = source.author_display || source.author || "Unknown";
        return (
        <button
          key={citId}
          onClick={() => onCitationClick?.(citId)}
          className={`w-full text-left px-4 py-3 transition-colors duration-150
            hover:bg-primary/[0.03]
            ${activeCitation === citId ? "bg-primary/[0.06] border-l-2 border-l-primary" : ""}`}
        >
          <div className="flex items-start gap-3">
            <span className="citation-marker shrink-0 mt-0.5">
              {citId}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 leading-snug">
                {author} ({source.year})
              </p>
              {source.title && (
                <p className="text-xs text-[var(--color-text-secondary)] mt-0.5 line-clamp-2 italic">
                  {source.title}
                </p>
              )}
              <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                {source.journal && (
                  <span className="text-xs text-[var(--color-text-muted)]">{source.journal}</span>
                )}
                {source.study_type && (
                  <span className="inline-flex px-1.5 py-0.5 rounded text-[10px] font-medium bg-black/5 text-[var(--color-text-secondary)]">
                    {studyTypeLabel(source.study_type)}
                  </span>
                )}
                {source.sample_size && (
                  <span className="text-[10px] text-[var(--color-text-muted)]">n={source.sample_size}</span>
                )}
              </div>
              {source.doi && (
                <a
                  href={`https://doi.org/${source.doi}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={(e) => e.stopPropagation()}
                  className="inline-flex items-center gap-1 mt-1.5 text-xs text-primary hover:text-primary-light transition-colors"
                >
                  <span className="font-mono">{source.doi}</span>
                  <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                  </svg>
                </a>
              )}
            </div>
          </div>
        </button>
        );
      })}
    </div>
  );
}
