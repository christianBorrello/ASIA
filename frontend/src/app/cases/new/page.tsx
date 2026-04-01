"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createCase } from "@/lib/api";
import BodyMap from "@/components/cases/BodyMap";
import BodySystemPanel from "@/components/cases/BodySystemPanel";
import type { BodySystemFinding } from "@/lib/types";

export default function NewCasePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeSystem, setActiveSystem] = useState<string | null>(null);
  const [findings, setFindings] = useState<Record<string, BodySystemFinding[]>>({});

  const [form, setForm] = useState({
    patient_name: "",
    diagnosis: "",
    breed: "",
    age: "",
    stage: "",
    immunophenotype: "",
    notes: "",
  });

  const updateField = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const addFinding = (systemId: string, note: string) => {
    setFindings((prev) => ({
      ...prev,
      [systemId]: [
        ...(prev[systemId] || []),
        { id: crypto.randomUUID(), note, created_at: new Date().toISOString() },
      ],
    }));
  };

  const removeFinding = (systemId: string, findingId: string) => {
    setFindings((prev) => ({
      ...prev,
      [systemId]: (prev[systemId] || []).filter((f) => f.id !== findingId),
    }));
  };

  const handleSubmit = async () => {
    if (!form.patient_name.trim() || !form.diagnosis.trim()) {
      setError("Nome paziente e diagnosi sono obbligatori");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const newCase = await createCase({
        patient_name: form.patient_name,
        diagnosis: form.diagnosis,
        breed: form.breed || undefined,
        age: form.age || undefined,
        stage: form.stage || undefined,
        immunophenotype: form.immunophenotype || undefined,
        notes: form.notes || undefined,
      });

      // Store case locally for the cases list
      const stored = JSON.parse(localStorage.getItem("asia-cases") || "[]");
      stored.unshift({ ...newCase, body_systems: findings });
      localStorage.setItem("asia-cases", JSON.stringify(stored));

      router.push(`/cases/${newCase.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Errore nella creazione del caso");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-page max-w-5xl mx-auto px-4 py-8">
      <div className="mb-8">
        <button onClick={() => router.back()} className="text-sm text-[var(--color-text-muted)] hover:text-primary transition-colors flex items-center gap-1 mb-4">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Torna ai casi
        </button>
        <h1 className="font-serif text-2xl font-bold text-[var(--color-text)]">Nuovo caso clinico</h1>
        <p className="text-sm text-[var(--color-text-muted)] mt-1">
          Compila i dati del paziente e usa la mappa anatomica per annotare i problemi
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Patient Form */}
        <div className="space-y-6">
          <div className="card p-6 space-y-4">
            <h2 className="font-semibold text-sm text-[var(--color-text-secondary)] uppercase tracking-wider">
              Dati paziente
            </h2>

            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">
                  Nome paziente *
                </label>
                <input
                  type="text"
                  value={form.patient_name}
                  onChange={(e) => updateField("patient_name", e.target.value)}
                  placeholder="Es: Asia"
                  className="input-field"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">Razza</label>
                <input
                  type="text"
                  value={form.breed}
                  onChange={(e) => updateField("breed", e.target.value)}
                  placeholder="Es: Golden Retriever"
                  className="input-field"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">Et&agrave;</label>
                <input
                  type="text"
                  value={form.age}
                  onChange={(e) => updateField("age", e.target.value)}
                  placeholder="Es: 8 anni"
                  className="input-field"
                />
              </div>
              <div className="col-span-2">
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">
                  Diagnosi *
                </label>
                <input
                  type="text"
                  value={form.diagnosis}
                  onChange={(e) => updateField("diagnosis", e.target.value)}
                  placeholder="Es: Linfoma multicentrico B-cell"
                  className="input-field"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">Stadio</label>
                <select
                  value={form.stage}
                  onChange={(e) => updateField("stage", e.target.value)}
                  className="input-field"
                >
                  <option value="">Seleziona...</option>
                  <option value="I">I</option>
                  <option value="II">II</option>
                  <option value="III">III</option>
                  <option value="IIIa">IIIa</option>
                  <option value="IIIb">IIIb</option>
                  <option value="IV">IV</option>
                  <option value="V">V</option>
                </select>
              </div>
              <div>
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">
                  Immunofenotipo
                </label>
                <select
                  value={form.immunophenotype}
                  onChange={(e) => updateField("immunophenotype", e.target.value)}
                  className="input-field"
                >
                  <option value="">Seleziona...</option>
                  <option value="B-cell">B-cell</option>
                  <option value="T-cell">T-cell</option>
                  <option value="Null cell">Null cell</option>
                  <option value="Non determinato">Non determinato</option>
                </select>
              </div>
              <div className="col-span-2">
                <label className="text-xs font-medium text-[var(--color-text-secondary)] mb-1 block">
                  Note cliniche
                </label>
                <textarea
                  value={form.notes}
                  onChange={(e) => updateField("notes", e.target.value)}
                  placeholder="Annotazioni cliniche aggiuntive..."
                  rows={3}
                  className="input-field resize-none"
                />
              </div>
            </div>
          </div>

          {/* Body system panel */}
          {activeSystem && (
            <BodySystemPanel
              systemId={activeSystem}
              findings={findings[activeSystem] || []}
              onAddFinding={addFinding}
              onRemoveFinding={removeFinding}
              onClose={() => setActiveSystem(null)}
            />
          )}

          {error && (
            <div className="px-4 py-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-800">
              {error}
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="btn-primary w-full text-center"
          >
            {loading ? "Creazione in corso..." : "Crea caso"}
          </button>
        </div>

        {/* Right: Body Map */}
        <div className="lg:sticky lg:top-20 self-start">
          <BodyMap
            findings={findings}
            onSystemClick={setActiveSystem}
            activeSystem={activeSystem}
          />
        </div>
      </div>
    </div>
  );
}
