const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiError(response.status, body.detail || body.message || `Errore ${response.status}`);
  }
  return response.json();
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

export function submitQuery(text: string, caseId?: string) {
  return fetchApi<import("./types").QueryResponse>("/api/query", {
    method: "POST",
    body: JSON.stringify({ text, case_id: caseId || null, stream: false }),
  });
}

export function submitCaseQuery(caseId: string, text: string) {
  return fetchApi<import("./types").QueryResponse>(`/api/cases/${caseId}/query`, {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

export function getPreLoadedQueries() {
  return fetchApi<{ queries: import("./types").PreLoadedQuery[] }>("/api/pre-loaded-queries");
}

export function getCorpusMetadata() {
  return fetchApi<import("./types").CorpusMetadata>("/api/corpus-metadata");
}

export function createCase(data: {
  patient_name: string;
  diagnosis: string;
  breed?: string;
  age?: string;
  stage?: string;
  immunophenotype?: string;
  notes?: string;
}) {
  return fetchApi<import("./types").Case>("/api/cases", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function getCase(id: string) {
  return fetchApi<import("./types").Case>(`/api/cases/${id}`);
}

export function explainPaper(doi: string) {
  return fetchApi<import("./types").ExplainPaperResponse>("/api/explain-paper", {
    method: "POST",
    body: JSON.stringify({ doi }),
  });
}

export { API_BASE };
