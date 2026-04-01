"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { getCase, submitCaseQuery } from "@/lib/api";
import type { Case, QueryResponse } from "@/lib/types";
import SearchBox from "@/components/shared/SearchBox";
import EvidenceLevel from "@/components/shared/EvidenceLevel";
import SynthesisView from "@/components/query/SynthesisView";
import SourcePanel from "@/components/query/SourcePanel";
import BodyMap from "@/components/cases/BodyMap";

export default function CaseDetailPage() {
  const params = useParams();
  const router = useRouter();
  const caseId = params.id as string;

  const [caseData, setCaseData] = useState<Case | null>(null);
  const [loading, setLoading] = useState(true);
  const [queryLoading, setQueryLoading] = useState(false);
  const [latestResponse, setLatestResponse] = useState<QueryResponse | null>(null);
  const [expandedQuery, setExpandedQuery] = useState<string | null>(null);

  const loadCase = useCallback(async () => {
    try {
      const data = await getCase(caseId);
      setCaseData(data);
    } catch {
      // Case might only be in local storage for body map data
      const stored = JSON.parse(localStorage.getItem("asia-cases") || "[]");
      const local = stored.find((c: Case) => c.id === caseId);
      if (local) setCaseData(local);
    } finally {
      setLoading(false);
    }
  }, [caseId]);

  useEffect(() => { loadCase(); }, [loadCase]);

  const handleQuery = async (text: string) => {
    setQueryLoading(true);
    setLatestResponse(null);
    try {
      const result = await submitCaseQuery(caseId, text);
      setLatestResponse(result as unknown as QueryResponse);
      await loadCase(); // Refresh to get updated query history
    } catch (err) {
      setLatestResponse({
        query_text: text,
        synthesis: null,
        evidence_level: null,
        evidence_score: null,
        sources: [],
        study_count: null,
        total_sample_size: null,
        papers_analyzed: null,
        disclaimer: "",
        message: err instanceof Error ? err.message : "Errore",
      });
    } finally {
      setQueryLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center">
        <div className="w-10 h-10 rounded-full border-2 border-primary/20 border-t-primary animate-spin mx-auto" />
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <p className="text-[var(--color-text-secondary)]">Caso non trovato</p>
      </div>
    );
  }

  return (
    <div className="animate-page max-w-5xl mx-auto px-4 py-8">
      {/* Back + header */}
      <button onClick={() => router.push("/cases")} className="text-sm text-[var(--color-text-muted)] hover:text-primary transition-colors flex items-center gap-1 mb-4">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
        </svg>
        Torna ai casi
      </button>

      {/* Patient header */}
      <div className="card p-6 mb-6">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="font-serif text-2xl font-bold text-[var(--color-text)]">
              {caseData.patient_name}
            </h1>
            <p className="text-base text-[var(--color-text-secondary)] mt-1">{caseData.diagnosis}</p>
            <div className="flex items-center gap-3 mt-3 text-sm text-[var(--color-text-muted)]">
              {caseData.breed && <span>{caseData.breed}</span>}
              {caseData.age && <span>&middot; {caseData.age}</span>}
              {caseData.stage && (
                <span className="px-2 py-0.5 rounded bg-primary/5 text-primary text-xs font-medium">
                  Stadio {caseData.stage}
                </span>
              )}
              {caseData.immunophenotype && (
                <span className="px-2 py-0.5 rounded bg-accent/10 text-accent text-xs font-medium">
                  {caseData.immunophenotype}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Query + History */}
        <div className="lg:col-span-2 space-y-6">
          {/* Query box */}
          <div>
            <h2 className="text-sm font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-3">
              Nuova domanda per {caseData.patient_name}
            </h2>
            <SearchBox
              onSubmit={handleQuery}
              loading={queryLoading}
              size="compact"
              placeholder={`Domanda su ${caseData.patient_name}...`}
            />
            <p className="text-xs text-[var(--color-text-muted)] mt-2">
              Il contesto del paziente viene incluso automaticamente nella ricerca
            </p>
          </div>

          {/* Latest response */}
          {latestResponse?.synthesis && (
            <div className="card p-6 border-primary/20">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-xs font-semibold text-[var(--color-text-muted)]">Ultima risposta</span>
              </div>
              {latestResponse.evidence_level && (
                <div className="mb-3">
                  <EvidenceLevel level={latestResponse.evidence_level} compact />
                </div>
              )}
              <SynthesisView text={latestResponse.synthesis} />
              {latestResponse.sources.length > 0 && (
                <div className="mt-4">
                  <SourcePanel sources={latestResponse.sources} />
                </div>
              )}
            </div>
          )}

          {/* Query history */}
          {caseData.queries && caseData.queries.length > 0 && (
            <div>
              <h2 className="text-sm font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-3">
                Storico domande ({caseData.queries.length})
              </h2>
              <div className="space-y-2">
                {caseData.queries.map((q) => (
                  <div key={q.id} className="card overflow-hidden">
                    <button
                      onClick={() => setExpandedQuery(expandedQuery === q.id ? null : q.id)}
                      className="w-full text-left px-4 py-3 flex items-center justify-between
                        hover:bg-primary/[0.02] transition-colors min-h-[44px]"
                    >
                      <div className="flex-1 min-w-0">
                        <p className="text-sm text-[var(--color-text)] truncate">{q.query_text}</p>
                        <p className="text-xs text-[var(--color-text-muted)] mt-0.5">
                          {q.created_at && new Date(q.created_at).toLocaleString("it-IT")}
                          {q.study_count && ` \u00B7 ${q.study_count} studi`}
                        </p>
                      </div>
                      <svg
                        className={`w-4 h-4 text-[var(--color-text-muted)] shrink-0 transition-transform
                          ${expandedQuery === q.id ? "rotate-180" : ""}`}
                        fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                      </svg>
                    </button>
                    {expandedQuery === q.id && q.synthesis && (
                      <div className="px-4 pb-4 border-t border-[var(--color-border)]">
                        <div className="pt-3">
                          <SynthesisView text={q.synthesis} />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Body Map */}
        <div className="lg:col-span-1">
          <div className="lg:sticky lg:top-20">
            <BodyMap
              findings={caseData.body_systems || {}}
              onSystemClick={() => {}}
              activeSystem={null}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
