"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import SearchBox from "@/components/shared/SearchBox";
import PreLoadedQueryCard from "@/components/home/PreLoadedQueryCard";
import { getPreLoadedQueries, getCorpusMetadata } from "@/lib/api";
import type { PreLoadedQuery, CorpusMetadata } from "@/lib/types";

export default function HomePage() {
  const router = useRouter();
  const [queries, setQueries] = useState<PreLoadedQuery[]>([]);
  const [metadata, setMetadata] = useState<CorpusMetadata | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getPreLoadedQueries().then((d) => setQueries(d.queries)).catch(() => {});
    getCorpusMetadata().then(setMetadata).catch(() => {});
  }, []);

  const handleQuery = (text: string) => {
    setLoading(true);
    const encoded = encodeURIComponent(text);
    router.push(`/query?q=${encoded}`);
  };

  return (
    <div className="animate-page">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-primary/[0.03] to-transparent" />
        <div className="relative max-w-3xl mx-auto px-4 pt-16 pb-12 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary/5 border border-primary/10 mb-6">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-medium text-primary/70">
              {metadata ? `${metadata.paper_count} paper indicizzati` : "Caricamento corpus\u2026"}
            </span>
          </div>

          <h1 className="font-serif text-4xl md:text-5xl font-bold text-primary-dark tracking-tight mb-4 text-balance">
            Evidenze scientifiche per l&apos;oncologia veterinaria
          </h1>
          <p className="text-lg text-[var(--color-text-secondary)] mb-8 max-w-xl mx-auto text-balance">
            Poni una domanda clinica sul linfoma canino e ricevi una sintesi basata
            sulla letteratura, con citazioni verificabili.
          </p>

          <SearchBox onSubmit={handleQuery} loading={loading} />

          {metadata && (
            <p className="mt-4 text-xs text-[var(--color-text-muted)]">
              Corpus aggiornato al {metadata.corpus_date} &middot; Focus: linfoma multicentrico canino
            </p>
          )}
        </div>
      </section>

      {/* Pre-loaded Queries */}
      <section className="max-w-3xl mx-auto px-4 pb-8">
        <h2 className="text-sm font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-4">
          Domande suggerite
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 stagger-children">
          {queries.map((q) => (
            <PreLoadedQueryCard key={q.id} query={q} onClick={handleQuery} />
          ))}
        </div>
      </section>

      {/* Quick Actions */}
      <section className="max-w-3xl mx-auto px-4 pb-16">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <button
            onClick={() => router.push("/cases/new")}
            className="card p-5 text-left group hover:shadow-md hover:border-primary/20
              hover:-translate-y-0.5 transition-all duration-200 active:scale-[0.98]"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center
                group-hover:bg-primary/20 transition-colors">
                <svg className="w-5 h-5 text-primary" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              </div>
              <div>
                <p className="font-semibold text-[var(--color-text)]">Crea nuovo caso</p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  Associa ricerche a un paziente specifico
                </p>
              </div>
            </div>
          </button>

          <button
            onClick={() => router.push("/explain")}
            className="card p-5 text-left group hover:shadow-md hover:border-primary/20
              hover:-translate-y-0.5 transition-all duration-200 active:scale-[0.98]"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center
                group-hover:bg-accent/20 transition-colors">
                <svg className="w-5 h-5 text-accent" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9zm3.75 11.625a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                </svg>
              </div>
              <div>
                <p className="font-semibold text-[var(--color-text)]">Analizza un paper</p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  Inserisci un DOI per un riassunto clinico in italiano
                </p>
              </div>
            </div>
          </button>
        </div>
      </section>
    </div>
  );
}
