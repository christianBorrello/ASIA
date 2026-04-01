# ASIA — Definizione MVP

> MVP progettato per il demo al team veterinario di Asia. L'obiettivo è dimostrare il valore del tool con un prodotto reale e funzionante, non un mockup.

---

## Scope

**Dominio:** Linfoma multicentrico canino (B-cell e T-cell)
**Target demo:** Team veterinario di Asia (1-3 veterinari)
**Lingua:** Interfaccia e sintesi in italiano, paper in inglese
**Backend:** Pipeline reale (PubMed ingestion, embedding, pgvector, Claude Sonnet)

---

## Feature incluse nell'MVP

### 1. Clinical Query — Sintesi RAG completa

Il cuore di ASIA. Il veterinario scrive una domanda in linguaggio naturale e riceve:

- **Risposta sintetica** in italiano (2-3 frasi)
- **Indicatore di evidenza** (tipo studio, numero studi, sample size totale)
- **Dettagli con citazioni inline** a livello di frase `[1]`, `[2]`
- **Per ogni citazione:** autore, journal, anno, tipo studio, sample size, DOI cliccabile
- **Disclaimer medico** sempre visibile, non nascondibile
- **Streaming** della risposta (SSE)

**Acceptance criteria — 5 query critiche:**

1. *"Qual è il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"*
2. *"CHOP-19 vs CHOP-25: differenze negli outcome?"*
3. *"Protocolli di rescue per recidiva precoce dopo CHOP?"*
4. *"Prognosi linfoma T-cell vs B-cell?"*
5. *"Aggiustamento dose doxorubicina per neutropenia?"*

Le 5 query devono produrre risposte accurate, ben citate, in italiano chiaro.

### 2. Tabella confronto protocolli

Quando la query riguarda un confronto tra protocolli, la risposta include una tabella strutturata auto-generata:

| Protocollo | Farmaci | Tasso remissione | Sopravvivenza mediana | Tipo studio | n | Costo | Citazione |
|------------|---------|------------------|----------------------|-------------|---|-------|-----------|

Generata dal RAG come parte della sintesi, non da un database separato.

### 3. 5 query pre-caricate

Nella homepage, le 5 query critiche sono presentate come bottoni/card cliccabili. Il veterinario clicca e vede subito una risposta di qualità.

**Perché:** Garantisce un demo sicuro (zero rischio di query che fallisce). Mostra immediatamente il livello di qualità. Le risposte sono comunque generate dal RAG reale (non hardcoded), ma sono state testate e validate in anticipo.

### 4. Explain This Paper

Il veterinario incolla un DOI o titolo di un paper. ASIA:
- Recupera il paper dal corpus (o lo cerca su PubMed/Semantic Scholar)
- Fornisce un riassunto clinico strutturato in italiano:
  - Obiettivo dello studio
  - Metodologia e qualità (tipo studio, sample size, limiti)
  - Risultati chiave
  - Implicazioni pratiche per il clinico
  - Come si posiziona rispetto all'evidenza esistente nel corpus

### 5. Case Mode (basilare)

Un "caso" è un contenitore a cui il veterinario associa tutte le ricerche e operazioni:

- **Crea caso:** nome paziente, razza, età, diagnosi, stadio, immunofenotipo, note
- **Ogni query fatta dentro un caso** viene salvata e associata al caso
- **Storico del caso:** lista cronologica di tutte le query e risposte
- **Contesto automatico:** quando il vet fa una nuova query dentro un caso, il contesto del caso (razza, diagnosi, stadio, etc.) viene automaticamente incluso nella query RAG per risposte più pertinenti

Non serve: condivisione casi, export, analytics, integrazione con gestionali. Solo il contenitore base.

### 6. Frontend — Una pagina, curata

- **Homepage:** logo ASIA + campo di ricerca + 5 query suggerite + "Crea nuovo caso" + "Explain a paper"
- **Pagina risposta:** sintesi streaming + panel fonti espandibile + tabella protocolli (quando applicabile)
- **Pagina caso:** dettagli caso + storico query
- **Design:** pulito, professionale, tablet-first (Tailwind). Non deve sembrare un prototipo — deve sembrare un prodotto
- **Responsive:** funziona su tablet e desktop
- **No auth per MVP** (demo in contesto controllato)

---

## Feature esplicitamente escluse dall'MVP

| Feature | Perché dopo |
|---------|-------------|
| **Complication Advisor** | Richiede indicizzazione specifica della letteratura sugli effetti collaterali. v1.1 |
| **Owner Communication Generator** | Alto valore ma aggiunge scope. v1.1 |
| **Monitoring Checklist** | Richiede dati strutturati sui protocolli. v1.1 |
| **New Evidence Alert** | Richiede sistema di notifiche + subscription. v1.1 |
| **Community Annotations** | Richiede utenti attivi. Post-MVP |
| **Case Outcome Registry** | Richiede trust e base utenti. Post-MVP |
| **WhatsApp/Telegram bot** | Canale alternativo, non core. Post-MVP |
| **Voice query** | Nice-to-have. Post-MVP |
| **Autenticazione utenti** | Demo controllato, non serve per ora. v1.1 |
| **Multi-tumore** | MVP = solo linfoma multicentrico. Post-validazione |
| **Multilingua** | MVP = solo italiano. Post-validazione |
| **Offline mode** | Complessità tecnica alta. Post-MVP |
| **Hybrid search (keyword + semantic)** | Semantic search basta per il corpus MVP. v1.1 se i dati lo giustificano |
| **Cross-encoder re-ranking** | Over-engineering per corpus piccolo. Post-MVP |

---

## Stack tecnico (confermato)

| Layer | Tecnologia |
|-------|-----------|
| Backend | FastAPI (Python 3.12+) |
| Frontend | Next.js + TypeScript + Tailwind |
| Database | PostgreSQL 16 + pgvector |
| LLM | Adapter pattern: interfaccia comune `LLMProvider` con implementazioni swappabili. MVP: `GroqProvider` (Llama 3.3 70B, costo zero). Futuro: `AnthropicProvider`, `OpenAIProvider`, `OllamaProvider`. Cambio provider via config/env var |
| Embedding | sentence-transformers (modello da benchmarkare) |
| Ingestion | PubMed E-utilities + Semantic Scholar API |
| Task scheduling | APScheduler (non Celery) |
| Container | Docker Compose |
| Licenza | Apache 2.0 |

---

## Pipeline dati MVP

1. **Ingestion:** Query PubMed per linfoma multicentrico canino → ~2000 paper
2. **Parsing:** Estrazione metadati + abstract
3. **Retraction check:** Verifica stato retraction via PubMed
4. **Embedding:** Abstract → embedding con sentence-transformers
5. **Indexing:** pgvector (IVFFlat)
6. **Quality scoring:** Tipo studio × citation count × recency
7. **Arricchimento:** Citation count e TLDR da Semantic Scholar API

---

## Mitigazione hallucination (MVP)

1. **Retrieval limitato** al corpus indicizzato (no web search generica)
2. **Self-reflective RAG** — genera, verifica citazioni, raffina (max 2 iterazioni). Nota: la qualità dipende dal modello. Se Llama 3.3 70B via Groq non è sufficiente per l'italiano medico, valutare Mixtral o upgrade a provider a pagamento
3. **Soglia di confidenza** — sotto soglia risponde "Non ho trovato evidenze sufficienti"
4. **Citazioni verificabili** — ogni citazione ha DOI cliccabile
5. **Disclaimer** sempre presente

---

## Acceptance criteria per il demo

Il demo è riuscito se:

- [ ] Le 5 query critiche producono risposte accurate (verificate dal vet)
- [ ] Le citazioni corrispondono a paper reali e pertinenti
- [ ] L'italiano medico è giudicato "naturale e corretto" o "accettabile"
- [ ] Il vet può fare domande libere (non solo le 5 pre-caricate) e ricevere risposte sensate
- [ ] La tabella confronto protocolli è generata per almeno 1 query
- [ ] Explain This Paper funziona con un DOI fornito dal vet
- [ ] Il Case Mode permette di creare un caso e associarci query
- [ ] Il vet esprime interesse a usarlo per un caso reale (commitment test dal questionario Parte 3)

---

## Cosa NON è l'obiettivo del demo

- Non dimostrare scalabilità
- Non dimostrare che funziona per tutti i tumori
- Non impressionare con il design
- **Dimostrare che ASIA dà risposte utili, accurate e verificabili a domande cliniche reali sul linfoma canino, in italiano, in pochi secondi**

---

## Documenti di riferimento

- [Vision completa](vision.md)
- [Brainstorm](brainstorm.md)
- [Market Research](market-research.md)
- [Discovery artifacts](feature/asia-vet-oncology/discover/)
- [Questionari per vet team](../Questionari/)
