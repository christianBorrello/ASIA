# Journey: Veterinarian Clinical Query -- Visual Map

**Persona**: Dott.ssa Giulia Mancini, veterinaria generalista con 8 anni di esperienza, gestisce 3-5 casi oncologici al mese. Lavora in una clinica a Bologna. Legge l'inglese scientifico con fatica. Ha un Golden Retriever di 7 anni appena diagnosticato con linfoma multicentrico B-cell stadio III sul tavolo.

**Goal**: Get an evidence-based treatment recommendation for a canine lymphoma case, in Italian, with verifiable citations, in under 2 minutes.

---

## Emotional Arc

```
Confidence
    ^
    |                                                          *** SATISFIED ***
    |                                                       **   "Posso usare
    |                                                     *      questo"
    |                                              ****
    |                                           * TRUSTING
    |                                         *  "Le citazioni
    |                                        *    corrispondono"
    |                                      *
    |                               ****
    |                            * FOCUSED
    |                          *  "La risposta
    |                        *    ha senso"
    |                      *
    |               ***
    |            * CURIOUS
    |          *  "Vediamo cosa
    |        *    risponde"
    |      *
    | ***
    | SKEPTICAL
    | "Funzionera
    |  davvero?"
    +-------------------------------------------------------------> Time
    Step 1      Step 2       Step 3        Step 4        Step 5
    ARRIVE      QUERY        READ          VERIFY        DECIDE
```

---

## Journey Flow

```
+============+     +=============+     +==============+     +=============+     +=============+
| 1. ARRIVE  |---->| 2. QUERY    |---->| 3. READ      |---->| 4. VERIFY   |---->| 5. DECIDE   |
| Homepage   |     | Type or     |     | Streaming    |     | Check       |     | Confident   |
|            |     | click       |     | response     |     | citations   |     | enough to   |
|            |     | pre-loaded  |     | in Italian   |     | & evidence  |     | act         |
+============+     +=============+     +==============+     +=============+     +=============+
  Feels:             Feels:             Feels:              Feels:              Feels:
  Skeptical          Curious            Focused             Trusting            Satisfied
  "Another AI?"      "Let's see"        "This makes         "Sources are        "I can use
                                         sense"              real"               this"
```

---

## Step 1: ARRIVE -- Homepage First Impression

**Trigger**: Dott.ssa Mancini opens ASIA for the first time. She has a patient in active treatment and needs an answer.

**Emotional state**: Skeptical, time-pressed, slightly anxious about the patient. She has tried ChatGPT before and found the answers unverifiable.

**What she sees**:

```
+----------------------------------------------------------------------+
|                                                                      |
|                          [ASIA Logo]                                 |
|         Aggregated Scientific Intelligence for Animals               |
|                                                                      |
|  +----------------------------------------------------------------+  |
|  |  Scrivi la tua domanda clinica...                              |  |
|  +----------------------------------------------------------------+  |
|                                                                      |
|  Domande suggerite:                                                  |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Qual e il protocollo di prima linea per un linfoma            |   |
|  | multicentrico B-cell stadio III?                              |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | CHOP-19 vs CHOP-25: differenze negli outcome?                |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Protocolli di rescue per recidiva precoce dopo CHOP?         |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Prognosi linfoma T-cell vs B-cell?                           |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  +--------------------------------------------------------------+   |
|  | Aggiustamento dose doxorubicina per neutropenia?             |   |
|  +--------------------------------------------------------------+   |
|                                                                      |
|  [+ Crea nuovo caso]        [Explain a Paper]                       |
|                                                                      |
+----------------------------------------------------------------------+
|  Disclaimer: ASIA e un supporto alla decisione clinica basato sulla  |
|  letteratura scientifica. Non sostituisce il giudizio del veterinario.|
|  Corpus aggiornato al: marzo 2026                                    |
+----------------------------------------------------------------------+
```

**Design intent**:
- Pre-loaded queries are the first thing she tries (safe demo path)
- Disclaimer always visible, never dismissible -- builds trust through honesty
- Clean, professional -- must not look like a toy or prototype
- Tablet-first layout (she may use it at the clinic on a tablet)

**Emotional transition**: Skeptical -> Curious. The pre-loaded queries lower the barrier. "Let me try one of these."

---

## Step 2: QUERY -- Ask or Click

**Action**: Dott.ssa Mancini clicks the first pre-loaded query: "Qual e il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"

**Alternative path**: She types her own question in the search box. For the demo, pre-loaded queries are the safe path.

**What she sees** (immediately, within 100ms):

```
+----------------------------------------------------------------------+
|  <- Torna alla home                                                  |
|                                                                      |
|  Domanda:                                                            |
|  "Qual e il protocollo di prima linea per un linfoma multicentrico   |
|   B-cell stadio III?"                                                |
|                                                                      |
|  +----------------------------------------------------------------+  |
|  |  [Streaming indicator: dots animating]                         |  |
|  |  Analisi della letteratura in corso...                         |  |
|  +----------------------------------------------------------------+  |
|                                                                      |
+----------------------------------------------------------------------+
```

**Emotional transition**: Curious -> Engaged. Immediate response (streaming starts within seconds). She sees words appearing.

---

## Step 3: READ -- Streaming Response in Italian

**What she sees** (response streams in, SSE):

```
+----------------------------------------------------------------------+
|  <- Torna alla home                                                  |
|                                                                      |
|  Domanda:                                                            |
|  "Qual e il protocollo di prima linea per un linfoma multicentrico   |
|   B-cell stadio III?"                                                |
|                                                                      |
|  +-- Sintesi -------------------------------------------------+     |
|  |                                                             |     |
|  |  Il protocollo di prima linea raccomandato per il linfoma   |     |
|  |  multicentrico B-cell stadio III e il CHOP (ciclofosfamide, |     |
|  |  doxorubicina, vincristina, prednisone), con un tasso di    |     |
|  |  remissione completa dell'80-90% [1][2]. Lo studio          |     |
|  |  multicentrico europeo di Sorenmo et al. (2020) ha          |     |
|  |  dimostrato che il protocollo a 19 settimane (CHOP-19) e    |     |
|  |  quello a 25 settimane (CHOP-25) hanno outcome equivalenti  |     |
|  |  [3]. La sopravvivenza mediana per i linfomi B-cell trattati|     |
|  |  con CHOP e di 10-14 mesi [1][2][4].                        |     |
|  |                                                             |     |
|  +-------------------------------------------------------------+     |
|                                                                      |
|  Livello di evidenza: MODERATO                                       |
|  Studi: 4 | Tipo: 1 prospettico multicentrico, 3 retrospettivi      |
|  Sample size totale: ~850 cani                                       |
|                                                                      |
|  +-- Fonti -----------------------------------------------[v]-+     |
|  |                                                             |     |
|  |  [1] Garrett LD et al. (2002) JAVMA                         |     |
|  |      Retrospettivo, n=58. Remissione CHOP 80%.              |     |
|  |      DOI: 10.2460/javma.2002.221.xxx                        |     |
|  |                                                             |     |
|  |  [2] Simon D et al. (2006) JVIM                             |     |
|  |      Prospettico, n=77. Sopravvivenza mediana 12 mesi.      |     |
|  |      DOI: 10.1111/j.1939-1676.2006.xxx                      |     |
|  |                                                             |     |
|  |  [3] Sorenmo KU et al. (2020) Vet Comp Oncol               |     |
|  |      Multicentrico prospettico, n=408. CHOP-19 = CHOP-25.   |     |
|  |      DOI: 10.1111/vco.xxx                                   |     |
|  |                                                             |     |
|  |  [4] Vail DM et al. (2013) JVIM                             |     |
|  |      Retrospettivo, n=307. B-cell vs T-cell prognosi.        |     |
|  |      DOI: 10.1111/jvim.xxx                                  |     |
|  +-------------------------------------------------------------+     |
|                                                                      |
+----------------------------------------------------------------------+
|  Disclaimer: ASIA e un supporto alla decisione clinica. Non          |
|  sostituisce il giudizio del veterinario. Corpus: marzo 2026         |
+----------------------------------------------------------------------+
```

**Key design decisions**:
- Synthesis first (2-3 sentences), details expandable
- Sentence-level citations [1][2][3] -- not just paper-level
- Evidence level indicator prominent (MODERATO, not hidden)
- Source panel shows: author, year, journal, study type, sample size, DOI link
- Disclaimer persists on every page

**Emotional transition**: Focused -> Building trust. "The answer makes clinical sense. The citations are specific papers I recognize."

---

## Step 4: VERIFY -- Check Citations and Evidence

**Action**: Dott.ssa Mancini clicks on DOI link [3] (Sorenmo et al.) to verify the claim about CHOP-19 vs CHOP-25 equivalence.

**What happens**: The DOI opens in a new tab showing the actual paper on the journal website. She scans the abstract and confirms the claim matches.

**Alternative action**: She clicks "Explain This Paper" to get a structured clinical summary of the Sorenmo paper.

**Emotional transition**: Building trust -> Trusting. "The citation is real. The claim matches. This is not hallucinating."

---

## Step 5: DECIDE -- Confidence to Act

**State**: Dott.ssa Mancini now has:
- A synthesized answer in Italian she can understand quickly
- Specific citations she can verify (and has verified one)
- Evidence level and study quality visible
- Enough confidence to discuss CHOP-19 with the patient's owner

**What she does next** (one of):
- Asks a follow-up question: "Aggiustamento dose doxorubicina per neutropenia?"
- Creates a case for this patient and associates the query
- Returns to homepage for another pre-loaded query

**Emotional transition**: Trusting -> Satisfied. "I can use this. It saves me time and gives me verifiable evidence."

---

## Error Paths

### E1: No Evidence Found

```
+--------------------------------------------------------------+
|  Sintesi:                                                     |
|                                                               |
|  Non sono state trovate evidenze sufficienti nel corpus per   |
|  rispondere a questa domanda con il livello di affidabilita   |
|  richiesto.                                                   |
|                                                               |
|  Possibili motivi:                                            |
|  - La domanda riguarda un ambito fuori dal corpus attuale     |
|    (linfoma multicentrico canino)                             |
|  - I termini usati non corrispondono alla letteratura         |
|    indicizzata                                                |
|                                                               |
|  Suggerimenti:                                                |
|  - Riformula la domanda con termini piu specifici             |
|  - Prova una delle domande suggerite nella homepage           |
|  - Consulta PubMed direttamente: [link PubMed query]         |
+--------------------------------------------------------------+
```

**Design intent**: Honest about limitations. Does not fabricate an answer. Suggests alternatives.

### E2: Slow Response (>10 seconds)

```
+--------------------------------------------------------------+
|  Analisi della letteratura in corso...                        |
|  [===========>                          ] 45%                 |
|                                                               |
|  Sto analizzando 12 paper rilevanti.                          |
|  Tempo stimato: ~15 secondi                                   |
+--------------------------------------------------------------+
```

**Design intent**: Progress indicator with paper count gives confidence that real work is happening, not a frozen screen.

### E3: Citation Mismatch (Hallucination Detected)

If the self-reflective RAG detects a citation mismatch during its verification pass:

```
+--------------------------------------------------------------+
|  Nota: Una citazione inizialmente identificata e stata        |
|  rimossa perche non supportava adeguatamente l'affermazione.  |
|  La sintesi riflette solo fonti verificate.                   |
+--------------------------------------------------------------+
```

**Design intent**: Transparency about the system's self-correction builds trust more than hiding it.

---

## Protocol Comparison Table (Query 2: CHOP-19 vs CHOP-25)

When the query involves comparing protocols, the response includes a structured table:

```
+----------------------------------------------------------------------+
|  Confronto protocolli:                                                |
|                                                                       |
|  +------------------------------------------------------------------+|
|  | Protocollo | Farmaci         | Remissione | Sopravvivenza | n    ||
|  |------------|-----------------|------------|---------------|------||
|  | CHOP-19    | Ciclofosfamide, | 80-90%     | 10-12 mesi    | 408  ||
|  |            | Doxorubicina,   |            | (B-cell)      |      ||
|  |            | Vincristina,    |            |               |      ||
|  |            | Prednisone      |            |               |      ||
|  |------------|-----------------|------------|---------------|------||
|  | CHOP-25    | Stessi farmaci, | 80-90%     | 10-12 mesi    | 408  ||
|  |            | schedule esteso |            | (B-cell)      |      ||
|  |            | 25 settimane    |            |               |      ||
|  |------------|-----------------|------------|---------------|------||
|  | COP        | Ciclofosfamide, | 60-70%     | 6-8 mesi      | vari ||
|  |            | Vincristina,    |            |               |      ||
|  |            | Prednisone      |            |               |      ||
|  +------------------------------------------------------------------+|
|                                                                       |
|  Fonte: Sorenmo et al. 2020 [3] (CHOP-19 = CHOP-25);                |
|  Garrett et al. 2002 [1]; vari studi COP                            |
+----------------------------------------------------------------------+
```

---

## Case Mode Journey (Step 5 Alternative)

When Dott.ssa Mancini creates a case:

```
+----------------------------------------------------------------------+
|  Nuovo Caso                                                          |
|                                                                      |
|  Nome paziente: [Luna                                      ]         |
|  Razza:         [Golden Retriever                          ]         |
|  Eta:           [7 anni                                    ]         |
|  Diagnosi:      [Linfoma multicentrico                     ]         |
|  Stadio:        [III                                       ]         |
|  Immunofenotipo:[B-cell                                    ]         |
|  Note:          [Linfonodi periferici aumentati, buone     ]         |
|                 [condizioni generali, substadio a          ]         |
|                                                                      |
|  [Crea caso]     [Annulla]                                           |
+----------------------------------------------------------------------+
```

After creation, queries within the case auto-inject context:

```
+----------------------------------------------------------------------+
|  Caso: Luna -- Golden Retriever, 7 anni                              |
|  Linfoma multicentrico B-cell, stadio IIIa                           |
|                                                                      |
|  +----------------------------------------------------------------+  |
|  |  Scrivi la tua domanda per questo caso...                      |  |
|  +----------------------------------------------------------------+  |
|                                                                      |
|  Storico:                                                            |
|  [14:32] Qual e il protocollo di prima linea...                     |
|  [14:35] Aggiustamento dose doxorubicina per neutropenia?            |
|                                                                      |
+----------------------------------------------------------------------+
```

**Design intent**: The case context (breed, diagnosis, stage, immunophenotype) is automatically injected into each RAG query, producing more specific answers without the vet having to repeat themselves.

---

## Explain This Paper Journey

```
+----------------------------------------------------------------------+
|  Explain This Paper                                                  |
|                                                                      |
|  Incolla un DOI o titolo:                                            |
|  +----------------------------------------------------------------+  |
|  |  10.1111/vco.12345                                             |  |
|  +----------------------------------------------------------------+  |
|  [Analizza]                                                          |
|                                                                      |
+----------------------------------------------------------------------+
```

Response:

```
+----------------------------------------------------------------------+
|  Riassunto clinico: Sorenmo KU et al. (2020)                        |
|  "Multi-center randomized trial comparing..."                        |
|                                                                      |
|  Obiettivo: Confrontare CHOP-19 e CHOP-25 in termini di efficacia   |
|  e tossicita nel linfoma multicentrico canino.                       |
|                                                                      |
|  Metodologia: Studio prospettico multicentrico randomizzato.         |
|  n=408, 12 centri europei. Quality: ALTA (RCT multicentrico)        |
|                                                                      |
|  Risultati chiave:                                                   |
|  - Nessuna differenza significativa in remissione o sopravvivenza    |
|  - Tossicita comparabile tra i due protocolli                        |
|  - B-cell: sopravvivenza superiore vs T-cell in entrambi i gruppi   |
|                                                                      |
|  Implicazioni pratiche:                                              |
|  CHOP-19 e preferibile per la durata piu breve senza compromettere  |
|  l'efficacia. Riduce il carico per paziente e proprietario.         |
|                                                                      |
|  Nel contesto del corpus ASIA:                                       |
|  Questo studio conferma e aggiorna i dati di Garrett (2002) e       |
|  Simon (2006) con un campione piu ampio e design piu robusto.       |
+----------------------------------------------------------------------+
```
