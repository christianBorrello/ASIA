"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { Case } from "@/lib/types";

export default function CasesListPage() {
  const router = useRouter();
  const [cases, setCases] = useState<Case[]>([]);

  useEffect(() => {
    // For MVP, cases are stored locally since we don't have a list endpoint
    const stored = localStorage.getItem("asia-cases");
    if (stored) setCases(JSON.parse(stored));
  }, []);

  return (
    <div className="animate-page max-w-3xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="font-serif text-2xl font-bold text-[var(--color-text)]">Casi clinici</h1>
          <p className="text-sm text-[var(--color-text-muted)] mt-1">
            Gestisci i tuoi casi oncologici
          </p>
        </div>
        <button onClick={() => router.push("/cases/new")} className="btn-primary flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Nuovo caso
        </button>
      </div>

      {cases.length === 0 ? (
        <div className="card p-12 text-center">
          <div className="w-16 h-16 rounded-full bg-primary/5 flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-primary/40" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z" />
            </svg>
          </div>
          <p className="text-[var(--color-text-secondary)] mb-4">Nessun caso ancora creato</p>
          <button onClick={() => router.push("/cases/new")} className="btn-secondary">
            Crea il primo caso
          </button>
        </div>
      ) : (
        <div className="space-y-3 stagger-children">
          {cases.map((c) => (
            <button
              key={c.id}
              onClick={() => router.push(`/cases/${c.id}`)}
              className="card w-full text-left p-5 hover:shadow-md hover:border-primary/20
                hover:-translate-y-0.5 transition-all duration-200 active:scale-[0.99]"
            >
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-[var(--color-text)]">{c.patient_name}</h3>
                  <p className="text-sm text-[var(--color-text-secondary)] mt-0.5">{c.diagnosis}</p>
                  <div className="flex items-center gap-2 mt-2 text-xs text-[var(--color-text-muted)]">
                    {c.breed && <span>{c.breed}</span>}
                    {c.breed && c.age && <span>&middot;</span>}
                    {c.age && <span>{c.age}</span>}
                    {c.stage && <span>&middot; Stadio {c.stage}</span>}
                  </div>
                </div>
                <svg className="w-5 h-5 text-[var(--color-text-muted)] shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
