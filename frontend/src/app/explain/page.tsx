"use client";

import { useState } from "react";
import { explainPaper } from "@/lib/api";
import type { ExplainPaperResponse } from "@/lib/types";

export default function ExplainPaperPage() {
  const [doi, setDoi] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ExplainPaperResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!doi.trim()) {
      setError("Inserisci un DOI o titolo del paper");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await explainPaper(doi.trim());
      if (data.error) {
        setError(data.message || "Paper non trovato");
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Errore durante l\u2019analisi");
    } finally {
      setLoading(false);
    }
  };

  const sections = result?.summary
    ? [
        { key: "objective", label: "Obiettivo", icon: "\u{1F3AF}" },
        { key: "methodology", label: "Metodologia", icon: "\u{1F52C}" },
        { key: "results", label: "Risultati chiave", icon: "\u{1F4CA}" },
        { key: "implications", label: "Implicazioni pratiche", icon: "\u{1F4A1}" },
        { key: "corpus_context", label: "Contesto nel corpus ASIA", icon: "\u{1F4DA}" },
      ]
    : [];

  return (
    <div className="animate-page max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="font-serif text-2xl font-bold text-[var(--color-text)]">Analizza un paper</h1>
        <p className="text-sm text-[var(--color-text-muted)] mt-1">
          Inserisci un DOI per ricevere un riassunto clinico strutturato in italiano
        </p>
      </div>

      {/* Input */}
      <div className="card p-6 mb-6">
        <label className="text-xs font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider mb-2 block">
          DOI del paper
        </label>
        <div className="flex gap-3">
          <input
            type="text"
            value={doi}
            onChange={(e) => setDoi(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
            placeholder="Es: 10.1111/vco.12345"
            className="input-field font-mono text-sm flex-1"
          />
          <button
            onClick={handleSubmit}
            disabled={loading || !doi.trim()}
            className="btn-primary shrink-0"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Analisi...
              </span>
            ) : (
              "Analizza"
            )}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="card p-5 border-amber-200 bg-amber-50 mb-6">
          <div className="flex items-start gap-3">
            <svg className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
            </svg>
            <div>
              <p className="text-sm font-medium text-amber-800">{error}</p>
              <p className="text-xs text-amber-700 mt-1">Verifica il DOI e riprova, oppure prova con il titolo del paper.</p>
            </div>
          </div>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-4 stagger-children">
          {/* Paper header */}
          <div className="card p-6">
            <h2 className="font-serif text-lg font-semibold text-[var(--color-text)] mb-2">
              {result.title}
            </h2>
            <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)] flex-wrap">
              <span>{result.authors}</span>
              <span>&middot;</span>
              <span>{result.journal}, {result.year}</span>
              {result.doi && (
                <>
                  <span>&middot;</span>
                  <a
                    href={`https://doi.org/${result.doi}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:text-primary-light font-mono text-xs transition-colors"
                  >
                    {result.doi}
                  </a>
                </>
              )}
            </div>
            {result.abstract_only && (
              <div className="mt-3 flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-50 border border-amber-200">
                <svg className="w-4 h-4 text-amber-600" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                </svg>
                <p className="text-xs text-amber-800">
                  Questo riassunto \u00e8 basato solo sull&apos;abstract. Il paper non \u00e8 nel corpus ASIA.
                </p>
              </div>
            )}
          </div>

          {/* Sections */}
          {sections.map(({ key, label, icon }) => {
            const content = result.summary[key as keyof typeof result.summary];
            if (!content) return null;
            return (
              <div key={key} className="card p-5">
                <h3 className="text-sm font-semibold text-[var(--color-text-secondary)] flex items-center gap-2 mb-3">
                  <span>{icon}</span>
                  {label}
                </h3>
                <p className="synthesis-text text-base text-[var(--color-text)] leading-relaxed">
                  {content}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
