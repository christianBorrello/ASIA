"use client";

import { Suspense, useEffect, useState, useCallback } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { submitQuery, checkLlmStatus } from "@/lib/api";
import type { QueryResponse } from "@/lib/types";
import SearchBox from "@/components/shared/SearchBox";
import EvidenceLevel from "@/components/shared/EvidenceLevel";
import SynthesisView from "@/components/query/SynthesisView";
import SourcePanel from "@/components/query/SourcePanel";
import ComparisonTable from "@/components/query/ComparisonTable";

interface FallbackBannerProps {
  fallbackModel: string;
  onRetry: () => void;
  onDismiss: () => void;
}

function FallbackBanner({ fallbackModel, onRetry, onDismiss }: FallbackBannerProps) {
  const [polling, setPolling] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!polling) return;

    let cancelled = false;

    const poll = async () => {
      try {
        const status = await checkLlmStatus();
        if (cancelled) return;
        if (status.primary_available) {
          setPolling(false);
          setStatusMessage(null);
          onRetry();
          return;
        }
      } catch {
        // Polling failure is non-fatal; will retry next interval
      }
    };

    // Check immediately, then every 15 seconds
    poll();
    const intervalId = setInterval(poll, 15_000);

    return () => {
      cancelled = true;
      clearInterval(intervalId);
    };
  }, [polling, onRetry]);

  const handleRetryClick = () => {
    setPolling(true);
    setStatusMessage("In attesa del modello principale...");
  };

  return (
    <div className="card p-4 border-amber-300 bg-amber-50 mb-6">
      <div className="flex items-start gap-3">
        <svg
          className="w-5 h-5 text-amber-600 shrink-0 mt-0.5"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
          />
        </svg>
        <div className="flex-1">
          <p className="text-sm text-amber-800">
            Risposta generata con un modello ridotto (<strong>{fallbackModel}</strong>) perch&eacute; il modello
            principale &egrave; temporaneamente non disponibile. La qualit&agrave; potrebbe essere inferiore.
          </p>
          <div className="mt-3 flex items-center gap-3">
            {polling ? (
              <div className="flex items-center gap-2 text-sm text-amber-700">
                <div className="w-4 h-4 rounded-full border-2 border-amber-400/30 border-t-amber-600 animate-spin" />
                <span>{statusMessage}</span>
              </div>
            ) : (
              <button
                onClick={handleRetryClick}
                className="text-sm font-medium text-amber-800 bg-amber-200 hover:bg-amber-300 px-3 py-1.5 rounded-md transition-colors"
              >
                Riprova con il modello principale
              </button>
            )}
            <button
              onClick={onDismiss}
              className="text-sm text-amber-700 hover:text-amber-900 underline underline-offset-2 transition-colors"
            >
              Continua con questa risposta
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function QueryContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const queryText = searchParams.get("q") || "";

  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeCitation, setActiveCitation] = useState<number | null>(null);
  const [fallbackDismissed, setFallbackDismissed] = useState(false);

  const executeQuery = useCallback(async (text: string) => {
    setFallbackDismissed(false);
    setLoading(true);
    setError(null);
    setResponse(null);
    try {
      const result = await submitQuery(text);
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Errore durante la ricerca");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (queryText) executeQuery(queryText);
  }, [queryText, executeQuery]);

  const handleNewQuery = (text: string) => {
    router.push(`/query?q=${encodeURIComponent(text)}`);
  };

  const handleRetryWithPrimary = useCallback(() => {
    if (queryText) {
      executeQuery(queryText);
    }
  }, [queryText, executeQuery]);

  const handleDismissFallback = useCallback(() => {
    setFallbackDismissed(true);
  }, []);

  const showFallbackBanner =
    response?.used_fallback === true && !fallbackDismissed && !loading;

  const isNoEvidence = response && !response.synthesis && response.message;

  return (
    <div className="animate-page max-w-5xl mx-auto px-4 py-8">
      <div className="mb-8">
        <SearchBox onSubmit={handleNewQuery} loading={loading} size="compact" />
      </div>

      {queryText && (
        <div className="mb-6">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Domanda</p>
          <h1 className="font-serif text-xl md:text-2xl text-gray-900 leading-snug">{queryText}</h1>
        </div>
      )}

      {showFallbackBanner && response?.fallback_model && (
        <FallbackBanner
          fallbackModel={response.fallback_model}
          onRetry={handleRetryWithPrimary}
          onDismiss={handleDismissFallback}
        />
      )}

      {loading && (
        <div className="card p-8 flex flex-col items-center gap-4">
          <div className="w-12 h-12 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
          <p className="text-sm text-gray-500">Analisi della letteratura in corso...</p>
        </div>
      )}

      {error && (
        <div className="card p-6 border-red-200 bg-red-50">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      {isNoEvidence && (
        <div className="card p-6 border-amber-200 bg-amber-50">
          <div className="flex items-start gap-3">
            <svg className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
            </svg>
            <div>
              <p className="text-sm font-medium text-amber-800 mb-1">{response!.message}</p>
              {response!.scope_explanation && (
                <p className="text-xs text-amber-700 mb-2">{response!.scope_explanation}</p>
              )}
              {response!.suggestions && response!.suggestions.length > 0 && (
                <ul className="space-y-1">
                  {response!.suggestions.map((s, i) => (
                    <li key={i} className="text-xs text-amber-700 flex items-center gap-1.5">
                      <span className="w-1 h-1 rounded-full bg-amber-400" />
                      {s}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      )}

      {response?.synthesis && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            {response.evidence_level && (
              <EvidenceLevel
                level={response.evidence_level}
                studyCount={response.study_count}
                totalSampleSize={response.total_sample_size}
              />
            )}
            <div className="card p-6">
              <SynthesisView text={response.synthesis} onCitationClick={setActiveCitation} />
            </div>
            {response.comparison_table && <ComparisonTable table={response.comparison_table} />}
            {response.reflection_note && (
              <div className="flex items-start gap-2 px-4 py-3 rounded-lg bg-blue-50 border border-blue-200">
                <svg className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
                </svg>
                <p className="text-xs text-blue-800">{response.reflection_note}</p>
              </div>
            )}
          </div>
          <div className="lg:col-span-1">
            <div className="lg:sticky lg:top-20">
              <SourcePanel sources={response.sources} activeCitation={activeCitation} onCitationClick={setActiveCitation} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function QueryPage() {
  return (
    <Suspense fallback={
      <div className="max-w-5xl mx-auto px-4 py-16 text-center">
        <div className="w-10 h-10 rounded-full border-2 border-primary/20 border-t-primary animate-spin mx-auto" />
      </div>
    }>
      <QueryContent />
    </Suspense>
  );
}
