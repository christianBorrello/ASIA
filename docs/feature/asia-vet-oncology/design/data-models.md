# Data Models -- ASIA Vet Oncology MVP

**Feature ID**: asia-vet-oncology
**Wave**: DESIGN
**Date**: 2026-04-01

---

## PostgreSQL Schema

### Extension

```sql
CREATE EXTENSION IF NOT EXISTS vector;  -- pgvector
```

---

### Table: papers

Stores paper metadata ingested from PubMed and Semantic Scholar.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Internal paper ID |
| pmid | VARCHAR(20) | UNIQUE, NULLABLE | PubMed ID |
| doi | VARCHAR(255) | UNIQUE, NULLABLE | Digital Object Identifier |
| title | TEXT | NOT NULL | Paper title (English) |
| authors | JSONB | NOT NULL | Array of author objects: [{name, affiliation}] |
| journal | VARCHAR(255) | | Journal name |
| year | SMALLINT | NOT NULL | Publication year |
| abstract_text | TEXT | | Full abstract text (English) |
| study_type | VARCHAR(50) | | meta_analysis, rct, prospective_multicenter, prospective, retrospective, case_series, case_report, review, expert_opinion |
| sample_size | INTEGER | | Number of subjects in study |
| species | VARCHAR(50) | DEFAULT 'canine' | Target species |
| cancer_type | VARCHAR(100) | DEFAULT 'multicentric_lymphoma' | Cancer type |
| citation_count | INTEGER | DEFAULT 0 | From Semantic Scholar |
| tldr | TEXT | | AI-generated summary from Semantic Scholar |
| is_retracted | BOOLEAN | DEFAULT FALSE | Retraction status from PubMed |
| is_open_access | BOOLEAN | DEFAULT FALSE | Open access availability |
| quality_score | FLOAT | | Computed: study_type_weight * recency * citation_factor |
| source | VARCHAR(20) | NOT NULL | 'pubmed', 'semantic_scholar', 'manual' |
| ingested_at | TIMESTAMPTZ | DEFAULT NOW() | When paper was added to corpus |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Last metadata update |

**Indexes**:
- `idx_papers_doi` on `doi` (unique, for DOI lookups)
- `idx_papers_pmid` on `pmid` (unique, for PubMed lookups)
- `idx_papers_year` on `year` (for recency filtering)
- `idx_papers_study_type` on `study_type` (for evidence level computation)
- `idx_papers_quality` on `quality_score DESC` (for ranking)

---

### Table: chunks

Stores text chunks from papers with their vector embeddings. Each paper is split into chunks for more precise retrieval.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Chunk ID |
| paper_id | UUID | FK -> papers(id) ON DELETE CASCADE | Parent paper |
| chunk_index | SMALLINT | NOT NULL | Position within paper (0-based) |
| chunk_text | TEXT | NOT NULL | Text content of the chunk |
| chunk_type | VARCHAR(30) | NOT NULL | 'title', 'abstract', 'methods', 'results', 'conclusion', 'full_abstract' |
| embedding | vector(384) | NOT NULL | Vector embedding (384 dims for MiniLM) |
| token_count | INTEGER | | Approximate token count for chunk |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes**:
- `idx_chunks_paper` on `paper_id` (for paper -> chunks lookup)
- `idx_chunks_embedding_ivfflat` on `embedding` using ivfflat (vector_cosine_ops) WITH (lists = 50) -- tuned for ~5000-10000 chunks

**Notes on embedding dimension**: If the embedding model changes (e.g., from 384 to 768 dimensions), the vector column and index must be recreated. The embedding dimension is defined in `config/settings.py` as a single source of truth.

**Chunking strategy for MVP**: For papers with only abstracts (majority of corpus), the abstract is stored as a single chunk (`chunk_type = 'full_abstract'`). For open-access papers with full text, the text is split into sections (methods, results, conclusion) as separate chunks.

---

### Table: cases

Stores veterinary cases created by the vet.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Case ID |
| patient_name | VARCHAR(100) | NOT NULL | Patient name |
| breed | VARCHAR(100) | | Dog breed |
| age | VARCHAR(50) | | Age (free text, e.g., "7 anni") |
| diagnosis | VARCHAR(255) | NOT NULL | Clinical diagnosis |
| stage | VARCHAR(20) | | Cancer stage (I-V) |
| immunophenotype | VARCHAR(50) | | B-cell, T-cell, null cell, etc. |
| notes | TEXT | | Free-text clinical notes |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes**:
- `idx_cases_created` on `created_at DESC` (for listing cases by recency)

---

### Table: case_queries

Stores queries and responses associated with a case.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Query record ID |
| case_id | UUID | FK -> cases(id) ON DELETE CASCADE, NULLABLE | Associated case (NULL for homepage queries) |
| query_text | TEXT | NOT NULL | Original Italian query text |
| response_synthesis | TEXT | | Italian synthesis text with citation markers |
| response_citations | JSONB | | Array of citation objects |
| evidence_level | VARCHAR(10) | | 'ALTO', 'MODERATO', 'BASSO' |
| evidence_score | FLOAT | | Numeric score from scoring algorithm |
| study_count | INTEGER | | Number of studies cited |
| total_sample_size | INTEGER | | Sum of sample sizes across cited studies |
| comparison_table | JSONB | | Structured table data (null if not a comparison query) |
| reflection_note | TEXT | | Transparency note if citations were removed |
| retrieval_chunks | JSONB | | IDs and scores of retrieved chunks (for debugging) |
| response_time_ms | INTEGER | | Total response time in milliseconds |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**Indexes**:
- `idx_case_queries_case` on `case_id, created_at DESC` (for case query history)
- `idx_case_queries_created` on `created_at DESC` (for global query log)

---

### Table: ingestion_runs

Tracks ingestion pipeline execution for corpus date metadata.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Run ID |
| started_at | TIMESTAMPTZ | NOT NULL | Run start time |
| completed_at | TIMESTAMPTZ | | Run completion time |
| status | VARCHAR(20) | NOT NULL | 'running', 'completed', 'failed' |
| papers_fetched | INTEGER | DEFAULT 0 | Papers retrieved from sources |
| papers_new | INTEGER | DEFAULT 0 | New papers added to corpus |
| papers_updated | INTEGER | DEFAULT 0 | Existing papers with updated metadata |
| errors | JSONB | | Array of error messages |
| source | VARCHAR(20) | | 'pubmed', 'semantic_scholar', 'both' |

**Indexes**:
- `idx_ingestion_runs_completed` on `completed_at DESC` (for corpus date: latest completed run)

---

## Citation JSONB Structure

The `response_citations` field in `case_queries` stores an array of citation objects:

```json
[
  {
    "citation_id": 1,
    "paper_id": "uuid",
    "author_display": "Garrett LD et al.",
    "year": 2002,
    "journal": "JAVMA",
    "study_type": "retrospective",
    "sample_size": 58,
    "doi": "10.2460/javma.2002.221.xxx",
    "claim_summary": "CHOP remission rate 80%",
    "verification_status": "SUPPORTA"
  }
]
```

---

## Comparison Table JSONB Structure

The `comparison_table` field stores structured protocol comparison data:

```json
{
  "columns": ["protocol", "drugs", "remission_rate", "median_survival", "sample_size", "citation_id"],
  "rows": [
    {
      "protocol": "CHOP-19",
      "drugs": "Ciclofosfamide, Doxorubicina, Vincristina, Prednisone",
      "remission_rate": "80-90%",
      "median_survival": "10-12 mesi (B-cell)",
      "sample_size": 408,
      "citation_id": 3
    }
  ]
}
```

---

## Estimated Storage (MVP)

| Table | Estimated Rows | Estimated Size |
|-------|---------------|---------------|
| papers | ~2000 | ~5MB (metadata + abstracts) |
| chunks | ~5000 | ~50MB (text + 384-dim vectors) |
| cases | ~5-10 (demo) | <1MB |
| case_queries | ~50-100 (demo) | <1MB |
| ingestion_runs | ~10-30 | <1MB |
| **IVFFlat index** | -- | ~20MB |
| **Total** | -- | **~75MB** |

Well within PostgreSQL running on M1 8GB.
