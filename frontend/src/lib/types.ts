export type EvidenceLevel = "ALTO" | "MODERATO" | "BASSO";

export interface Paper {
  id: string;
  pmid?: string;
  doi?: string;
  title: string;
  authors: Record<string, unknown>[];
  journal?: string;
  year: number;
  abstract_text?: string;
  study_type?: string;
  species: string;
  cancer_type: string;
}

export interface CaseQuery {
  id: string;
  case_id?: string;
  query_text: string;
  response_synthesis?: string;
  evidence_level?: EvidenceLevel;
  evidence_score?: number;
  study_count?: number;
}

export interface Case {
  id: string;
  patient_name: string;
  breed?: string;
  age?: string;
  diagnosis: string;
  stage?: string;
  immunophenotype?: string;
}
