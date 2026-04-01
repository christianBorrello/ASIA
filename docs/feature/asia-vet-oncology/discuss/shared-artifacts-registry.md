# Shared Artifacts Registry -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Phase**: DISCUSS -- Coherence Validation

---

## Artifact Registry

### disclaimer_text

| Attribute | Value |
|-----------|-------|
| **Source of truth** | Backend configuration / constants file |
| **Value** | "ASIA e un supporto alla decisione clinica basato sulla letteratura scientifica. Non sostituisce il giudizio del veterinario." |
| **Consumers** | Homepage footer, Response page footer, Case page footer, Explain Paper page footer |
| **Owner** | Frontend constants + backend API |
| **Integration risk** | HIGH -- inconsistent disclaimer text across pages undermines trust. If one page shows a different version, it signals carelessness in a medical context. |
| **Validation** | All pages must render the exact same disclaimer string. Single source in frontend constants. |

---

### corpus_date

| Attribute | Value |
|-----------|-------|
| **Source of truth** | Ingestion pipeline metadata (last successful ingestion timestamp) |
| **Value** | Dynamic: "Corpus aggiornato al: {YYYY-MM}" |
| **Consumers** | Homepage footer, Response page footer |
| **Owner** | Ingestion pipeline |
| **Integration risk** | MEDIUM -- stale corpus date could mislead vets about evidence currency. Must update automatically after each ingestion run. |
| **Validation** | Compare displayed date against ingestion pipeline's last-run metadata. |

---

### pre_loaded_queries

| Attribute | Value |
|-----------|-------|
| **Source of truth** | Backend configuration / seed data |
| **Value** | 5 Italian clinical queries (see mvp.md for exact text) |
| **Consumers** | Homepage query cards |
| **Owner** | Product configuration |
| **Integration risk** | LOW -- static content, changes are infrequent. Risk is that query text displayed on homepage does not match what is sent to RAG pipeline. |
| **Validation** | Query text on card click must exactly match the string sent to the API. |

---

### query_text

| Attribute | Value |
|-----------|-------|
| **Source of truth** | User input (typed) or pre-loaded query selection |
| **Value** | The Italian clinical question as submitted |
| **Consumers** | Response page header, Case history entry, RAG pipeline input |
| **Owner** | Frontend state / API request |
| **Integration risk** | MEDIUM -- query displayed on response page must exactly match what RAG processed. Any transformation (trimming, normalization) must preserve the displayed version. |
| **Validation** | Compare displayed query text against API request payload. |

---

### synthesis_text

| Attribute | Value |
|-----------|-------|
| **Source of truth** | RAG pipeline LLM output |
| **Value** | Italian synthesis with inline citation markers [1][2][3] |
| **Consumers** | Response page main content, Case history response |
| **Owner** | RAG pipeline |
| **Integration risk** | HIGH -- this is the core value. Citation markers must match source panel entries 1:1. |
| **Validation** | Count citation markers in synthesis; must equal number of entries in source panel. Each [n] must link to the correct source. |

---

### citations

| Attribute | Value |
|-----------|-------|
| **Source of truth** | RAG pipeline retrieval + self-reflective verification |
| **Value** | List of: {author, year, journal, study_type, sample_size, doi_url, claim_summary} |
| **Consumers** | Response page source panel, Explain Paper input |
| **Owner** | RAG pipeline + PubMed/Semantic Scholar metadata |
| **Integration risk** | CRITICAL -- hallucinated citations destroy trust. Every citation must reference a real paper with a valid DOI. |
| **Validation** | DOI links must resolve to real papers. Claim in synthesis must match paper content. Self-reflective RAG verifies before display. |

---

### evidence_level

| Attribute | Value |
|-----------|-------|
| **Source of truth** | RAG pipeline scoring algorithm |
| **Value** | ALTO / MODERATO / BASSO (computed from study type x count x sample size) |
| **Consumers** | Response page evidence badge |
| **Owner** | RAG pipeline scoring module |
| **Integration risk** | MEDIUM -- misleading evidence level (e.g., showing ALTO for a single retrospective study) erodes trust. Scoring algorithm must be transparent and consistent. |
| **Validation** | Spot-check evidence levels against manual assessment of cited studies. |

---

### comparison_table

| Attribute | Value |
|-----------|-------|
| **Source of truth** | RAG pipeline structured extraction |
| **Value** | Table with columns: Protocol, Drugs, Remission Rate, Median Survival, Study Type, n, Citation |
| **Consumers** | Response page (when query involves protocol comparison) |
| **Owner** | RAG pipeline |
| **Integration risk** | MEDIUM -- incorrect data in comparison table (wrong remission rates, wrong survival data) is a high-severity clinical error but medium integration risk (single source). |
| **Validation** | Data in table cells must match the cited source papers. Spot-check against known protocol data. |

---

### case_data

| Attribute | Value |
|-----------|-------|
| **Source of truth** | Case creation form (user input) |
| **Value** | {patient_name, breed, age, diagnosis, stage, immunophenotype, notes} |
| **Consumers** | Case page header, RAG context injection, Case query history |
| **Owner** | Database (PostgreSQL) |
| **Integration risk** | MEDIUM -- case data injected into RAG queries must match what was entered. If context injection silently drops fields, responses may be less specific without the vet knowing why. |
| **Validation** | RAG API request payload must include all case fields. Case page header must display all entered fields. |

---

### doi_urls

| Attribute | Value |
|-----------|-------|
| **Source of truth** | PubMed / Semantic Scholar ingestion pipeline metadata |
| **Value** | Valid DOI URLs for each paper in the corpus |
| **Consumers** | Source panel DOI links, Explain Paper feature |
| **Owner** | Ingestion pipeline |
| **Integration risk** | HIGH -- broken DOI links (404, wrong paper) immediately destroy citation trust. |
| **Validation** | Periodic link validation against DOI.org resolver. All DOIs in corpus must resolve. |

---

## Integration Checkpoints

### Checkpoint 1: Query-to-Response Integrity

**Validates**: query_text matches across submission and display; streaming begins within 5 seconds.

**Failure mode**: Query text on response page differs from what was typed/clicked; streaming does not start.

### Checkpoint 2: Citation Consistency

**Validates**: Every citation marker [n] in synthesis has a matching entry in source panel; DOI links resolve.

**Failure mode**: Missing source for a citation marker; DOI 404; citation numbering mismatch.

### Checkpoint 3: Disclaimer Consistency

**Validates**: Identical disclaimer text on all pages.

**Failure mode**: Different wording on different pages; disclaimer missing on one page.

### Checkpoint 4: Case Context Injection

**Validates**: RAG queries within a case include all case fields in the prompt.

**Failure mode**: Context injection drops fields; response is generic instead of case-specific.

### Checkpoint 5: Corpus Date Accuracy

**Validates**: Displayed corpus date matches last ingestion run.

**Failure mode**: Hardcoded date that does not update after ingestion.
