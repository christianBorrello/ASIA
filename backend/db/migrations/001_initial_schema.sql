-- 001_initial_schema.sql
-- ASIA initial database schema with pgvector support

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Papers table
CREATE TABLE papers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pmid VARCHAR UNIQUE,
    doi VARCHAR UNIQUE,
    title TEXT NOT NULL,
    authors JSONB NOT NULL,
    journal VARCHAR,
    year SMALLINT NOT NULL,
    abstract_text TEXT,
    study_type VARCHAR,
    sample_size INT,
    species VARCHAR DEFAULT 'canine',
    cancer_type VARCHAR DEFAULT 'multicentric_lymphoma',
    citation_count INT DEFAULT 0,
    tldr TEXT,
    is_retracted BOOL DEFAULT FALSE,
    is_open_access BOOL DEFAULT FALSE,
    quality_score FLOAT,
    source VARCHAR NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chunks table with vector embeddings
CREATE TABLE chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paper_id UUID NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    chunk_index SMALLINT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_type VARCHAR NOT NULL,
    embedding vector(384) NOT NULL,
    token_count INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cases table
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_name VARCHAR NOT NULL,
    breed VARCHAR,
    age VARCHAR,
    diagnosis VARCHAR NOT NULL,
    stage VARCHAR,
    immunophenotype VARCHAR,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Case queries table
CREATE TABLE case_queries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_id UUID REFERENCES cases(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    response_synthesis TEXT,
    response_citations JSONB,
    evidence_level VARCHAR,
    evidence_score FLOAT,
    study_count INT,
    total_sample_size INT,
    comparison_table JSONB,
    reflection_note TEXT,
    retrieval_chunks JSONB,
    response_time_ms INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ingestion runs table
CREATE TABLE ingestion_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    status VARCHAR NOT NULL,
    papers_fetched INT DEFAULT 0,
    papers_new INT DEFAULT 0,
    papers_updated INT DEFAULT 0,
    errors JSONB,
    source VARCHAR
);

-- IVFFlat index for vector similarity search
CREATE INDEX idx_chunks_embedding ON chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);

-- Additional indexes for common queries
CREATE INDEX idx_papers_species_cancer ON papers(species, cancer_type);
CREATE INDEX idx_papers_year ON papers(year);
CREATE INDEX idx_chunks_paper_id ON chunks(paper_id);
CREATE INDEX idx_case_queries_case_id ON case_queries(case_id);
