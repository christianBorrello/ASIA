"use client";

import { useMemo, type ReactNode } from "react";

interface Props {
  text: string;
  streaming?: boolean;
  onCitationClick?: (id: number) => void;
}

/**
 * Renders synthesis text with inline citation markers [N] as clickable badges.
 * Uses React elements (not innerHTML) to avoid XSS risks.
 */
export default function SynthesisView({ text, streaming = false, onCitationClick }: Props) {
  const elements = useMemo((): ReactNode[] => {
    const parts: ReactNode[] = [];
    const citationPattern = /\[(\d+)\]/g;
    let lastIndex = 0;
    let match;
    let key = 0;

    while ((match = citationPattern.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(<span key={key++}>{text.slice(lastIndex, match.index)}</span>);
      }
      const citNum = parseInt(match[1], 10);
      parts.push(
        <button
          key={key++}
          onClick={() => onCitationClick?.(citNum)}
          className="citation-marker mx-0.5 align-super text-[10px]"
          aria-label={`Citazione ${citNum}`}
        >
          {citNum}
        </button>
      );
      lastIndex = citationPattern.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push(<span key={key++}>{text.slice(lastIndex)}</span>);
    }

    return parts;
  }, [text, onCitationClick]);

  return (
    <div className={`synthesis-text text-[var(--color-text)] ${streaming ? "streaming-cursor" : ""}`}>
      {elements}
    </div>
  );
}
