"use client";

export default function Disclaimer({ text }: { text?: string }) {
  const disclaimer =
    text ||
    "Questo strumento \u00e8 un supporto informativo alla decisione clinica. Non sostituisce il giudizio del veterinario.";

  return (
    <div className="w-full bg-primary-dark/5 border-t border-primary/10">
      <div className="max-w-5xl mx-auto px-4 py-2.5 flex items-center gap-2">
        <svg
          className="w-4 h-4 text-primary/60 shrink-0"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
          />
        </svg>
        <p className="text-xs text-primary/60 leading-relaxed">{disclaimer}</p>
      </div>
    </div>
  );
}
