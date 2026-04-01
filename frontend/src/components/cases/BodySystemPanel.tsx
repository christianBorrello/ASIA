"use client";

import { useState } from "react";
import { BODY_SYSTEMS } from "@/lib/constants";
import type { BodySystemFinding } from "@/lib/types";

interface Props {
  systemId: string;
  findings: BodySystemFinding[];
  onAddFinding: (systemId: string, note: string) => void;
  onRemoveFinding: (systemId: string, findingId: string) => void;
  onClose: () => void;
}

export default function BodySystemPanel({
  systemId,
  findings,
  onAddFinding,
  onRemoveFinding,
  onClose,
}: Props) {
  const [note, setNote] = useState("");
  const system = BODY_SYSTEMS.find((s) => s.id === systemId);
  if (!system) return null;

  const handleAdd = () => {
    if (note.trim()) {
      onAddFinding(systemId, note.trim());
      setNote("");
    }
  };

  return (
    <div className="card overflow-hidden">
      {/* Header */}
      <div
        className="px-4 py-3 flex items-center justify-between"
        style={{ backgroundColor: `${system.color}11`, borderBottom: `2px solid ${system.color}33` }}
      >
        <div className="flex items-center gap-2">
          <span className="text-xl">{system.emoji}</span>
          <div>
            <h3 className="font-semibold text-sm text-[var(--color-text)]">{system.name_it}</h3>
            <p className="text-xs text-[var(--color-text-muted)]">{system.description}</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="w-8 h-8 rounded-lg flex items-center justify-center hover:bg-black/5 transition-colors min-h-[44px] min-w-[44px]"
          aria-label="Chiudi"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Structures */}
      <div className="px-4 py-3 border-b border-[var(--color-border)]">
        <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-2">
          Strutture
        </p>
        <div className="flex flex-wrap gap-1.5">
          {system.structures.map((s) => (
            <span key={s} className="px-2 py-0.5 rounded-md text-xs bg-black/5 text-[var(--color-text-secondary)]">
              {s}
            </span>
          ))}
        </div>
      </div>

      {/* Findings */}
      <div className="px-4 py-3">
        <p className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider mb-2">
          Annotazioni ({findings.length})
        </p>

        {findings.length > 0 && (
          <div className="space-y-2 mb-3">
            {findings.map((f) => (
              <div key={f.id} className="flex items-start gap-2 group">
                <div className="flex-1 px-3 py-2 rounded-lg bg-surface text-sm text-[var(--color-text)]">
                  {f.note}
                  <span className="text-xs text-[var(--color-text-muted)] ml-2">
                    {new Date(f.created_at).toLocaleDateString("it-IT")}
                  </span>
                </div>
                <button
                  onClick={() => onRemoveFinding(systemId, f.id)}
                  className="opacity-0 group-hover:opacity-100 w-7 h-7 rounded flex items-center justify-center
                    text-red-400 hover:text-red-600 hover:bg-red-50 transition-all min-h-[44px] min-w-[44px]"
                  aria-label="Rimuovi annotazione"
                >
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Add finding */}
        <div className="flex gap-2">
          <input
            type="text"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAdd()}
            placeholder="Aggiungi annotazione..."
            className="input-field text-sm"
          />
          <button
            onClick={handleAdd}
            disabled={!note.trim()}
            className="btn-primary text-sm px-4 shrink-0 disabled:opacity-40"
          >
            Aggiungi
          </button>
        </div>
      </div>
    </div>
  );
}
