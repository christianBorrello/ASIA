"use client";

import type { ComparisonTable as ComparisonTableType } from "@/lib/types";

export default function ComparisonTable({ table }: { table: ComparisonTableType }) {
  if (!table?.rows?.length) return null;

  return (
    <div className="card overflow-hidden my-4">
      <div className="px-4 py-3 bg-primary/[0.03] border-b border-[var(--color-border)]">
        <h3 className="text-sm font-semibold text-primary flex items-center gap-2">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0112 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M12 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M21.75 12c.621 0 1.125.504 1.125 1.125m-18 0V18" />
          </svg>
          Confronto protocolli
        </h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)]">
              {(table.headers || ["Protocollo", "Tasso remissione", "Sopravvivenza mediana", "Citazione"]).map((h) => (
                <th key={h} className="px-4 py-2.5 text-left text-xs font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--color-border)]">
            {table.rows.map((row, i) => (
              <tr key={i} className="hover:bg-primary/[0.02] transition-colors">
                <td className="px-4 py-3 font-medium text-[var(--color-text)]">{row.protocol}</td>
                <td className="px-4 py-3 text-[var(--color-text-secondary)]">{row.remission_rate}</td>
                <td className="px-4 py-3 text-[var(--color-text-secondary)]">{row.median_survival}</td>
                <td className="px-4 py-3">
                  {row.citation && <span className="citation-marker">{row.citation.replace(/[\[\]]/g, "")}</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
