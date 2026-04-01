export type EvidenceLevel = "ALTO" | "MODERATO" | "BASSO";

export interface Source {
  id?: number;
  citation_id?: number;
  author?: string;
  author_display?: string;
  year: number;
  journal: string;
  doi: string | null;
  study_type?: string;
  sample_size?: number | null;
  title?: string;
}

export interface QueryResponse {
  query_text: string;
  synthesis: string | null;
  evidence_level: EvidenceLevel | null;
  evidence_score: number | null;
  sources: Source[];
  study_count: number | null;
  total_sample_size: number | null;
  papers_analyzed: number | null;
  disclaimer: string;
  reflection_note?: string;
  comparison_table?: ComparisonTable;
  message?: string;
  scope_explanation?: string;
  suggestions?: string[];
  used_fallback?: boolean;
  fallback_model?: string;
  primary_model?: string;
}

export interface LlmStatusResponse {
  primary_available: boolean;
  model: string;
}

export interface ComparisonTable {
  headers: string[];
  rows: ComparisonRow[];
}

export interface ComparisonRow {
  protocol: string;
  remission_rate: string;
  median_survival: string;
  citation: string;
  [key: string]: string;
}

export interface PreLoadedQuery {
  id: string;
  text: string;
  query_text?: string;
  topic: string;
  topic_label?: string;
}

export interface CorpusMetadata {
  corpus_date: string;
  paper_count: number;
  disclaimer_text: string;
}

export interface Case {
  id: string;
  patient_name: string;
  diagnosis: string;
  breed: string | null;
  age: string | null;
  stage: string | null;
  immunophenotype: string | null;
  notes: string | null;
  body_systems?: Record<string, BodySystemFinding[]>;
  created_at: string | null;
  updated_at: string | null;
  queries?: CaseQueryRecord[];
}

export interface CaseQueryRecord {
  id: string;
  query_text: string;
  synthesis: string | null;
  sources: Source[];
  evidence_score: number | null;
  study_count: number | null;
  created_at: string | null;
}

export interface BodySystemFinding {
  id: string;
  note: string;
  created_at: string;
}

export interface BodySystem {
  id: string;
  name_it: string;
  name_en: string;
  emoji: string;
  structures: string[];
  description: string;
  position: { top: string; left: string };
  color: string;
}

export interface ExplainPaperResponse {
  title: string;
  authors: string;
  year: number;
  journal: string;
  doi: string;
  summary: {
    objective: string;
    methodology: string;
    results: string;
    implications: string;
    corpus_context: string;
  };
  abstract_only?: boolean;
  error?: boolean;
  message?: string;
  suggestions?: string[];
}

export interface SSEEvent {
  event: "metadata" | "sources" | "token" | "done" | "heartbeat";
  data: Record<string, unknown>;
}
