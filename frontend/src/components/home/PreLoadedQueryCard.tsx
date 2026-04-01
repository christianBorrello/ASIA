"use client";

import type { PreLoadedQuery } from "@/lib/types";

interface Props {
  query: PreLoadedQuery;
  onClick: (text: string) => void;
}

const TOPIC_ICONS: Record<string, string> = {
  "prima linea": "\u{1F48A}",
  confronto: "\u{2696}\u{FE0F}",
  rescue: "\u{1F6A8}",
  prognosi: "\u{1F4CA}",
  dose: "\u{1F9EA}",
};

function getIcon(label?: string): string {
  if (!label) return "\u{1F52C}";
  for (const [key, icon] of Object.entries(TOPIC_ICONS)) {
    if (label.toLowerCase().includes(key)) return icon;
  }
  return "\u{1F52C}";
}

export default function PreLoadedQueryCard({ query, onClick }: Props) {
  return (
    <button
      onClick={() => onClick(query.query_text)}
      className="card group text-left p-4 transition-all duration-200
        hover:shadow-md hover:border-primary/20 hover:-translate-y-0.5
        active:scale-[0.98] active:shadow-sm
        min-h-[44px] cursor-pointer w-full"
    >
      <div className="flex items-start gap-3">
        <span className="text-xl mt-0.5 group-hover:scale-110 transition-transform duration-200">
          {getIcon(query.topic_label)}
        </span>
        <div className="flex-1 min-w-0">
          <p className="text-xs font-semibold text-primary/60 uppercase tracking-wider mb-1">
            {query.topic_label}
          </p>
          <p className="text-sm text-[var(--color-text)] leading-snug line-clamp-2">
            {query.query_text}
          </p>
        </div>
        <svg
          className="w-4 h-4 text-[var(--color-text-muted)] shrink-0 mt-1
            group-hover:text-primary group-hover:translate-x-0.5 transition-all duration-200"
          fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
        </svg>
      </div>
    </button>
  );
}
