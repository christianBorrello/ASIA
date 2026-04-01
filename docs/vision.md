# ASIA — Aggregated Scientific Intelligence for Animals

> *Dedicato ad Asia, la cui difficile esperienza diagnostica ha ispirato questo progetto. Perché ogni veterinario — e ogni animale — merita un accesso più rapido alle migliori evidenze disponibili.*

---

## Origine del progetto

ASIA nasce da un'esperienza personale. Asia è un cane che negli ultimi mesi ha affrontato un percorso diagnostico travagliato: visite, esami, ipotesi che si accavallavano. Dopo mesi, una radiografia ha rivelato una massa non identificata vicino al cuore. I valori di calcio nel sangue erano molto alti. I veterinari sospettano un tumore — probabilmente un linfoma.

Durante questo percorso è emerso un problema concreto: **le informazioni scientifiche più aggiornate su diagnosi e terapie oncologiche veterinarie esistono, ma sono disperse, in inglese, e difficili da raggiungere rapidamente per un veterinario che ha un caso davanti**. I paper ci sono. I protocolli terapeutici sono studiati e documentati. Ma aggregarli, confrontarli, capire quale sia la migliore evidenza disponibile per *quel* caso specifico richiede tempo che spesso non c'è.

ASIA vuole colmare questo gap.

---

## Il problema

Un veterinario che gestisce un caso oncologico oggi deve:

1. **Cercare su PubMed** — interfaccia pensata per ricercatori, non clinici. Risultati in inglese, non filtrabili per rilevanza clinica pratica.
2. **Leggere decine di abstract** — in inglese, spesso con terminologia molto specialistica, per estrarre le informazioni rilevanti al suo caso.
3. **Confrontare protocolli terapeutici** — dispersi in paper diversi, con metriche di outcome non sempre confrontabili.
4. **Tradurre mentalmente** — dalla letteratura in inglese alla decisione clinica concreta, sotto pressione di tempo e con un proprietario in ansia.
5. **Gestire micro-decisioni urgenti durante la terapia** — "Il cane ha neutropenia di grado 2 dopo la doxorubicina. Ritardo? Riduco la dose? Cambio farmaco?" — momenti in cui servono risposte evidence-based immediate.
6. **Spiegare al proprietario** — dopo aver preso una decisione, il veterinario deve comunicarla in modo chiaro e empatico, spesso dedicando 15-20 minuti per caso.

Questo processo è lento, frammentato e soggetto a errore. Non perché i veterinari non siano competenti, ma perché **gli strumenti disponibili non sono pensati per supportare la decisione clinica in tempo reale**.

---

## Panorama attuale — Perché la nicchia è vuota

Un'analisi del mercato (37 fonti verificate, marzo 2026) conferma che **nessun tool esistente combina aggregazione di letteratura, sintesi AI, lingua italiana e open source**.

### Cosa esiste oggi

| Tool | Cosa fa | Cosa manca |
|------|---------|-----------|
| **VIN (Veterinary Information Network)** | Forum con 80.000+ membri, specialisti oncologi rispondono a casi. Archivio trentennale di discussioni. | Informazione non strutturata, intrappolata in thread. Nessuna sintesi AI. Solo inglese. Nessun grading dell'evidenza. |
| **Plumb's Standards of Care** | 800+ monografie farmaci, drug interaction checker, algoritmi diagnostici. Peer-reviewed da 200+ specialisti. | Non è focalizzato sull'oncologia. Nessun protocollo completo (es. CHOP scheduling). Nessuna sintesi della letteratura. |
| **VetCompanion / Standards.vet** | Supporto decisionale clinico evidence-based. | Documentazione pubblica limitata. Non focalizzato su oncologia. |
| **ImpriMed** | AI + test di sensibilità farmacologica su cellule vive per linfoma canino. Risultati personalizzati in 6-7 giorni. Sopravvivenza 3x in linfoma B-cell recidivo. | Servizio di laboratorio, non sintesi della letteratura. Costoso. Solo USA. |
| **FidoCure** | Profilazione genomica + AI per trattamenti personalizzati. Sequenziamento + database 2 miliardi di data point. | Come ImpriMed: servizio lab-based, non letteratura. Solo USA. |
| **PubMed / Google Scholar** | Accesso alla letteratura scientifica mondiale. | Tool per ricercatori, non clinici. Nessuna sintesi. Nessun contesto clinico. Solo inglese. |

### Il gap che ASIA colma

Nessun tool al mondo fa per la veterinaria ciò che **UpToDate** fa per la medicina umana: aggregare la letteratura, sintetizzarla con grading dell'evidenza, e presentarla in un formato azionabile per il clinico. ASIA vuole essere quel tool — open source, in italiano, focalizzato sull'oncologia.

---

## La soluzione

ASIA è una piattaforma che **aggrega, indicizza e sintetizza** la letteratura scientifica sull'oncologia veterinaria, presentandola ai veterinari in un formato immediatamente fruibile.

Il veterinario pone una domanda clinica in linguaggio naturale — ad esempio:

> *"Golden Retriever di 8 anni con linfoma multicentrico B-cell, stadio IIIa. Quali protocolli di prima linea mostrano i migliori outcome nei paper più recenti?"*

ASIA risponde con una **sintesi in italiano**, basata sui paper scientifici più rilevanti, con:

- **Citazioni a livello di frase** — ogni affermazione rimanda al passaggio esatto nel paper originale, non solo al paper nel suo insieme (pattern validato da Elicit, che raggiunge il 94-99% di accuratezza nell'estrazione)
- **Livello di evidenza adattato alla veterinaria** — un sistema ispirato a GRADE (usato da UpToDate con 9.400+ raccomandazioni) ma calibrato sulla realtà veterinaria, dove i RCT sono rari e molto dell'evidenza viene da studi retrospettivi e piccoli studi prospettici. Il sistema mostra esplicitamente: tipo di studio, sample size, e anno di pubblicazione
- **Visualizzazione dell'accordo** — ispirata al Consensus Meter di Consensus: "3 studi supportano il Protocollo A. 2 studi mostrano risultati simili per il Protocollo B con minore tossicità. 1 studio contraddice per sottotipi T-cell." Mostrare il disaccordo costruisce fiducia attraverso l'onestà
- **Classificazione delle citazioni** — ispirata a Scite.ai (1.6 miliardi di citazioni classificate): ogni paper citato è marcato come *supporting*, *contrasting* o *mentioning* rispetto al claim. Questo distingue i paper che confermano da quelli che contraddicono
- **Tabelle di confronto protocolli auto-generate** — CHOP-19 vs COP vs single-agent doxorubicina, con colonne: farmaci, dosi, scheduling, tasso di remissione, sopravvivenza mediana, livello di costo, livello di evidenza. Nessun tool lo offre oggi
- **Dati prognostici strutturati** — "Se scegli CHOP-19 per un linfoma B-cell stadio IIIa: remissione tipica 12-14 mesi, percentuale di recidiva entro 6 mesi: ~20%, sopravvivenza mediana: ~12 mesi." Estratti dalla letteratura, non inventati
- **Disclaimer medico** — sempre presente e non nascondibile: il sistema è un supporto alla decisione, non un sostituto del giudizio clinico. Include anche la data di aggiornamento del corpus ("letteratura indicizzata fino a: [data]")

### Il valore fondamentale

**Il veterinario italiano non deve più leggere e tradurre mentalmente decine di paper in inglese.** ASIA fa quel lavoro, sintetizzando in italiano e citando le fonti in modo trasparente e verificabile. La traduzione contestuale dalla letteratura scientifica alla sintesi clinica è essa stessa un valore aggiunto significativo.

---

## Target utente

### Primario — Veterinari italiani

Veterinari generalisti e specialisti in oncologia che gestiscono casi oncologici nel cane. L'Italia ha circa 40.000 veterinari e una forte cultura di attaccamento agli animali domestici. Nessun tool in lingua italiana per il supporto decisionale oncologico esiste oggi.

### Secondario — Veterinari internazionali

L'architettura multilingua permette espansione: spagnolo, portoghese, tedesco, francese. I mercati veterinari in questi paesi hanno lo stesso problema di barriera linguistica con la letteratura in inglese.

### Terziario — Altri utenti futuri

- **Studenti di medicina veterinaria** — strumento didattico per apprendere l'oncologia evidence-based
- **Proprietari di animali** — interfaccia semplificata per comprendere diagnosi e opzioni terapeutiche (vedi "Pet Owner Companion Mode" nella roadmap)
- **Ricercatori in oncologia comparata** — il cancro canino è un modello validato per quello umano (il linfoma non-Hodgkin canino è modello per l'NHL umano; farmaci come ibrutinib, acalabrutinib e selinexor sono stati sviluppati usando dati canini). ASIA può diventare un ponte tra le due comunità

---

## Scope MVP — Linfoma multicentrico canino

L'MVP si concentra sul **linfoma multicentrico canino (B-cell e T-cell)** — la presentazione più comune (~80% dei linfomi canini).

### Perché il linfoma multicentrico

- **Alta prevalenza** — è tra i tumori più comuni nel cane
- **Letteratura abbondante** — stimati 500-1000 paper rilevanti, di cui 100-200 di alta qualità
- **Sottotipi ben classificati** — B-cell (~70%, prognosi migliore) vs T-cell (~30%, prognosi più riservata), classificazione WHO, staging definito (I-V con sotto-staging a/b)
- **Protocolli terapeutici consolidati** — CHOP-19, CHOP-25 (recente studio multicentrico europeo ne conferma l'equivalenza), COP, L-CHOP, rescue protocols (Tanovea, LAP, LOPP, DMAC, dacarbazina, temozolomide), con dati di outcome pubblicati
- **Tassi di remissione elevati** — 80-90% con protocolli CHOP-based, il che rende il supporto decisionale particolarmente impattante
- **Decisioni cliniche concrete** — il sistema può supportare staging, scelta del protocollo, gestione effetti collaterali, valutazione della prognosi, rescue dopo recidiva
- **Motivazione personale** — è il sospetto diagnostico di Asia

### Confini espliciti dell'MVP

**Incluso:** Linfoma multicentrico canino, B-cell e T-cell, tutti gli stadi WHO.
**Escluso per ora:** Linfoma alimentare/gastrointestinale, mediastinico, extranodale (cutaneo, SNC, nasale, renale). Queste forme hanno letterature e percorsi clinici distinti — saranno la prima espansione post-MVP.

### 5 query critiche come acceptance criteria

L'MVP è valido se risponde bene a queste 5 domande:

1. *"Qual è il protocollo di prima linea per un linfoma multicentrico B-cell stadio III?"*
2. *"CHOP-19 vs CHOP-25: differenze negli outcome?"*
3. *"Protocolli di rescue per recidiva precoce dopo CHOP?"*
4. *"Prognosi linfoma T-cell vs B-cell?"*
5. *"Aggiustamento dose doxorubicina per neutropenia?"*

Se ASIA risponde a queste cinque domande in modo accurato, ben citato e in italiano chiaro, l'MVP ha valore.

### Il test dei primi cinque minuti

Un veterinario apre ASIA per la prima volta. Digita una domanda. Se la risposta è impressionante, torna. Se è mediocre, non torna mai più. L'intero MVP deve essere ottimizzato per quella prima impressione.

---

## Feature differenzianti

### Core MVP

#### Clinical Query con sintesi RAG
Il cuore di ASIA: una singola interfaccia dove il veterinario pone domande in linguaggio naturale e riceve risposte sintetizzate con citazioni. L'esperienza è modellata sui migliori tool in medicina umana (UpToDate, Elicit, Consensus) ma calibrata per la veterinaria e in italiano.

Il formato della risposta segue un pattern di **progressive disclosure** (validato da UpToDate e Elicit):

```
[Risposta sintetica — 2-3 frasi]

[Indicatore di evidenza: "Evidenza moderata da 4 studi retrospettivi (n=312 totale)"]

[Dettagli con citazioni inline]
- Finding 1 con citazione [1]
- Finding 2 con citazioni [2][3]
- Finding contrastante con citazione [4]

[Tabella confronto protocolli — quando applicabile]
| Protocollo | Tasso risposta | Sopravvivenza mediana | Tipo studio | n | Citazione |

[Panel fonti]
[1] Autore et al. "Titolo." Journal, Anno. DOI. [Prospettico, n=85] [Supporting: citato 23 volte]
[2] ...

[Disclaimer — sempre presente, non nascondibile]
"Questo strumento è un supporto informativo alla decisione clinica.
Non sostituisce il giudizio del veterinario. Letteratura indicizzata fino a: [data]"
```

#### Linguaggio standardizzato per le raccomandazioni
Ispirato a UpToDate: "La letteratura **supporta fortemente**..." (evidenza forte) vs "La letteratura **suggerisce**..." (evidenza debole). Questa distinzione linguistica è semplice ma potente — segnala al veterinario il livello di confidenza senza richiedere di leggere i dettagli.

### Feature ad alto impatto (post-MVP immediato)

#### Case Mode — Contesto persistente
Un veterinario non fa una domanda isolata: **gestisce un caso nel tempo**, per settimane o mesi. Case Mode permette di creare un contesto persistente (razza, età, staging, immunofenotipo, storia terapeutica) e fare domande sequenziali:

> *"Asia, abbiamo iniziato CHOP-19 tre settimane fa e la paziente è in recidiva. Quali protocolli di rescue mostrano i migliori outcome per recidive precoci?"*

Il sistema ricorda il contesto del caso. Questo trasforma ASIA da tool di ricerca puntuale a **compagno clinico longitudinale**.

#### Complication Advisor — Gestione effetti collaterali
Un modulo dedicato, pre-indicizzato sulla letteratura degli effetti collaterali della chemioterapia. Durante la terapia, le micro-decisioni urgenti (neutropenia, tossicità GI, cistite emorragica da ciclofosfamide, cardiotossicità da doxorubicina) sono i momenti in cui il veterinario ha più bisogno di supporto evidence-based rapido.

#### Owner Communication Generator
Dopo che il veterinario ha deciso il protocollo, ASIA genera una **spiegazione semplificata in italiano per il proprietario**: cosa comporta il trattamento, timeline attesa, effetti collaterali possibili, costi indicativi, prognosi — calibrata sul caso specifico. Risparmia 15-20 minuti per caso e riduce la miscommunicazione.

#### Monitoring Checklist
Per ogni protocollo, auto-generazione di un calendario di monitoraggio: tempistiche esami del sangue, intervalli imaging, valori di laboratorio attesi, red flag. Supporto operativo, non solo intellettuale.

#### "Explain This Paper" Mode
Un veterinario trova un paper (da un collega, una conferenza, un referral). Incolla il DOI o il titolo. ASIA recupera il paper e fornisce: riassunto clinico strutturato in italiano, valutazione della qualità metodologica, implicazioni pratiche, come si posiziona rispetto all'evidenza esistente.

#### Collegamento a trial clinici attivi
Quando pertinente, la risposta include link a trial clinici attivi dal database AVMA e dal COTC (Comparative Oncology Trials Consortium, network di 20 centri accademici). Se esiste un trial rilevante per il caso del paziente, il veterinario lo deve sapere.

---

## Fonti dati

### Fonti primarie di letteratura

| Fonte | Cosa offre | API |
|-------|-----------|-----|
| **PubMed / MEDLINE** | Database principale della letteratura biomedica. Abstract, MeSH terms, metadati, stato di retraction. | E-utilities (REST/XML) |
| **Semantic Scholar** | 225M+ paper, 2.8B citation edges, TLDR summaries AI-generated, grafo citazioni, indicatori di influenza. | REST API (free, 1 req/s) |
| **Europe PMC** | Full-text open access per paper con licenza CC. | REST API |
| **CrossRef** | Metadati DOI, deduplicazione, linking. | REST API |

### Database e registri oncologici veterinari

| Fonte | Cosa offre |
|-------|-----------|
| **ICDC (Integrated Canine Data Commons)** | Dati clinici e genomici canini dall'NCI. API GraphQL. Open access. |
| **AVMA Animal Health Studies Database** | Registro trial clinici veterinari, ricercabile per tipo di tumore e località. |
| **COTC (Comparative Oncology Trials Consortium)** | Network di 20 centri accademici che conduce trial su cancri canini. Parte del NCI Comparative Oncology Program. |
| **VCOG (Veterinary Cooperative Oncology Group)** | Standard di valutazione della risposta (cRECIST) e criteri VCOG-CTCAE per tossicità. |
| **VCGP (Veterinary Cancer Guidelines and Protocols)** | Iniziativa per standardizzare valutazione e reporting dei tumori veterinari. |
| **GIVCS (Global Initiative for Veterinary Cancer Surveillance)** | Standardizzazione globale del reporting oncologico veterinario con approccio One Health. |
| **SAVSNET** | UK: il più grande database open-source di tumori canini e felini (1M+ record). |
| **FDA Green Book** | Database ufficiale FDA dei farmaci veterinari approvati. |

### Ontologie e terminologie

| Risorsa | Utilizzo |
|---------|---------|
| **MeSH (Medical Subject Headings)** | Vocabolario controllato per indicizzazione paper. Già disponibile via PubMed API. |
| **SNOMED CT Veterinary Extension** | Terminologia clinica veterinaria standardizzata. Utile per normalizzare query e risposte. |
| **VeNom (Veterinary Nomenclature)** | Terminologia veterinaria standardizzata usata in UK. |

### Gestione della qualità delle fonti

- **Paper retrattati** — controllati via Retraction Watch database e stato di retraction PubMed. Esclusi dalla sintesi, flaggati se citati.
- **Preprint** — flaggati esplicitamente come "non peer-reviewed". Inclusi solo se la letteratura peer-reviewed è insufficiente, e con disclaimer specifico.
- **Qualità dell'evidenza** — ranking basato su: tipo di studio (meta-analisi > RCT > prospettico > retrospettivo > case series > case report), sample size, citation count, impact factor del journal, anno di pubblicazione.
- **Citazioni supporting vs contrasting** — classificazione ispirata a Scite.ai: un paper citato frequentemente per *contrastare* i suoi risultati va trattato diversamente da uno citato per *supportarli*.
- **Completezza del corpus** — ASIA può sintetizzare solo ciò che ha indicizzato. Molti paper chiave sono dietro paywall. Per l'MVP: solo abstract e metadati (pubblici via PubMed). Full-text solo per paper open access. Trasparenza su cosa è incluso e cosa no.

---

## Design patterns da adottare

> Questi pattern emergono dall'analisi di tool in medicina umana (UpToDate, Elicit, Consensus, Scite.ai, Semantic Scholar, Perplexity) e dalla letteratura accademica su RAG in ambito medico. Sono **suggerimenti validati dalla ricerca**, le cui modalità di implementazione verranno definite nella fase di design.

### 1. Citazioni a livello di frase (da Elicit)
Ogni claim nella sintesi deve essere linkato al **passaggio esatto** nel paper sorgente, non solo al paper nel suo insieme. Elicit dimostra che questo è fattibile con accuratezza del 94-99%.

### 2. Hybrid search: semantica + keyword (da Consensus)
La ricerca semantica (embedding) cattura similarità concettuale ("protocollo chemioterapico multiagente" matcha con "CHOP-based protocol"). La ricerca keyword (BM25) cattura match esatti (nomi farmaci, acronimi, dosaggi). Combinare le due con Reciprocal Rank Fusion è l'attuale best practice.

### 3. Consensus Meter — visualizzazione dell'accordo (da Consensus)
Per domande yes/no o comparazioni, mostrare visivamente se la letteratura è concorde o divisa. "L'80% degli studi supporta CHOP rispetto a COP per B-cell" è immediatamente comprensibile.

### 4. GRADE adattato per veterinaria (da UpToDate)
Il sistema GRADE (usato da UpToDate con 9.400+ raccomandazioni) distingue forza della raccomandazione (forte/debole) e qualità dell'evidenza (alta/moderata/bassa). Va **adattato per la veterinaria**: molto dell'evidenza viene da studi retrospettivi, e uno studio retrospettivo ben disegnato su 200 cani potrebbe essere la migliore evidenza disponibile per un protocollo specifico.

### 5. Mitigazione hallucination multilivello (dalla letteratura accademica)
In contesto medico, l'hallucination è un rischio esistenziale. Self-Reflective RAG riduce le hallucination al 5.8%. Approccio raccomandato:
- **Layer 1:** Retrieval limitato a fonti verificate (corpus indicizzato)
- **Layer 2:** Self-reflective RAG (genera → verifica citazioni → raffina, max 2 iterazioni)
- **Layer 3:** Checker model che verifica allineamento claim-fonte
- **Layer 4:** Confidence score per claim basato sulla qualità del retrieval
- **Layer 5:** "Non ho trovato evidenze sufficienti" quando il retrieval è sotto soglia — **preferire il silenzio all'hallucination**

### 6. Progressive disclosure (da UpToDate/Elicit)
Risposta breve prima, dettagli a richiesta. Non sommergere il veterinario con tutti i dati in una volta. Il clinico sotto pressione vuole la risposta in 10 secondi; il dettaglio lo legge dopo.

### 7. Linguaggio standardizzato per le raccomandazioni (da UpToDate)
"La letteratura **supporta fortemente**" (Grade 1) vs "La letteratura **suggerisce**" (Grade 2). La distinzione linguistica segnala confidenza senza richiedere interpretazione.

---

## Principi guida

### 1. Citazione tracciabile
Ogni affermazione nella sintesi deve rimandare alla fonte originale. Il veterinario deve poter verificare. Nessuna "scatola nera". In contesto clinico, "auditabile" è una feature — ed è un vantaggio strutturale dell'open source rispetto a tool proprietari.

### 2. Supporto, non sostituzione
ASIA è un supporto alla decisione clinica. Non prescrive, non diagnostica. Il disclaimer è sempre presente e non nascondibile. Il linguaggio è sempre "la letteratura suggerisce" — mai "ASIA raccomanda". Questo posizionamento è anche rilevante per il quadro regolatorio (vedi sezione Rischi).

### 3. Open source come motore di fiducia
Il codice è open source (licenza Apache 2.0). Chiunque può deployare la propria istanza, contribuire, estendere. In un contesto medico/clinico, **open source significa auditabile**: veterinari e facoltà possono ispezionare esattamente come vengono generate le risposte, quali paper sono inclusi, come viene pesata l'evidenza. Questo è un vantaggio enorme rispetto a tool commerciali black-box.

### 4. Semplicità dell'MVP
Una sola interfaccia per l'MVP: **Clinical Query**. Un campo di ricerca, una risposta sintetizzata, i paper citati. Niente di più. L'intero MVP è ottimizzato per il "test dei primi cinque minuti": se la prima risposta è impressionante, il veterinario torna.

### 5. Italiano come valore aggiunto
L'interfaccia e le sintesi sono in italiano. I paper restano in inglese (è la lingua della letteratura scientifica). La traduzione contestuale dalla letteratura alla sintesi clinica è parte del valore che ASIA offre. La qualità dell'italiano medico deve essere impeccabile — italiano medico scritto male è peggio di nessuna traduzione.

### 6. Onestà sopra tutto
Quando i paper si contraddicono, ASIA lo mostra. Quando l'evidenza è debole, ASIA lo dice. Quando non trova evidenze sufficienti, ASIA risponde "non ho trovato evidenze sufficienti per rispondere a questa domanda" invece di inventare. La fiducia si costruisce con la trasparenza, non con la completezza apparente.

---

## Rischi e mitigazioni

### Rischi esistenziali

| Rischio | Impatto | Mitigazione |
|---------|---------|------------|
| **Hallucination in contesto medico** | Un dosaggio sbagliato o un'attribuzione errata potrebbe danneggiare un animale e distruggere la fiducia permanentemente | 5 layer di mitigazione (vedi Design Patterns). Citation hallucination (fatti corretti, fonti sbagliate) è il failure mode specifico del RAG da monitorare |
| **Adozione** | Il rischio #1 non è tecnico ma di adozione. I veterinari sono sotto pressione temporale e scettici verso nuovi tool | Beta test con 5-10 veterinari reali (partire dal team veterinario di Asia). Partnership con facoltà italiane (Bologna, Milano, Torino) come canale di distribuzione e credibilità |
| **Qualità dell'italiano medico** | LLM sono English-dominant. Terminologia medica italiana mal gestita peggiora l'esperienza | Test rigoroso con veterinari madrelingua. Benchmark di 3-4 LLM su sintesi veterinaria in italiano. Glossario terminologico verificato |
| **Sostenibilità economica** | Open source non è un modello di business. Costi server + API LLM sono reali e ricorrenti | Opzioni: donazioni, grant EU (Horizon Europe), partnership universitarie, versione hosted freemium, grant per salute digitale italiana |

### Rischi importanti

| Rischio | Impatto | Mitigazione |
|---------|---------|------------|
| **Corpus completeness bias** | Molti paper chiave sono dietro paywall → sintesi biased verso letteratura open access | Trasparenza su cosa è incluso. Per MVP: abstract sempre disponibili. Segnalare quando full-text non è accessibile |
| **Posizionamento regolatorio** | Se ASIA viene classificato come "medical device" sotto EU MDR, servono certificazioni costose | La ricerca indica che il software veterinario CDS cade fuori dallo scope FDA/EU MDR. Posizionamento esplicito come "literature synthesis tool", non diagnostic tool. Mai dire "ASIA raccomanda" — sempre "la letteratura suggerisce". Review legale pre-lancio |
| **LLM provider lock-in** | Dipendenza da API proprietarie (Anthropic, OpenAI) contraddice la promessa open source | Architettura con provider LLM swappabile. Supporto per modelli locali (Llama, Mistral) come opzione di deployment. Trade-off: qualità vs indipendenza |
| **Data freshness vs quality** | Preprint non peer-reviewed possono portare a raccomandazioni poi smentite | MVP: escludere preprint. Solo letteratura peer-reviewed. Ingestion include check retraction status |
| **Responsabilità legale** | Se un vet segue la sintesi di ASIA e l'outcome è negativo | Disclaimer legale robusto. Precedente da UpToDate/DynaMed in medicina umana è rassicurante ma va verificato per la veterinaria |

---

## Strategia evolutiva

Il brainstorm ha identificato tre approcci strategici. La raccomandazione è di implementarli in sequenza:

### Fase A — Literature Intelligence (MVP)
Eccellere in una cosa: la migliore sintesi evidence-based per il linfoma multicentrico canino. RAG perfetto, citazioni perfette, italiano perfetto. Una sola interfaccia. Il "test dei primi cinque minuti" è tutto.

### Fase B — Clinical Workflow Hub (post-MVP)
Andare oltre la ricerca. Aggiungere le feature che trasformano ASIA in uno strumento di lavoro quotidiano:

- **Case Mode** — contesto persistente del caso attraverso sessioni multiple
- **Complication Advisor** — gestione evidence-based degli effetti collaterali in tempo reale
- **Protocol Comparison Tables** — confronto strutturato auto-generato dalla letteratura
- **Owner Communication Generator** — spiegazioni semplificate per i proprietari
- **Monitoring Checklist** — calendario esami e red flag per ogni protocollo
- **"Explain This Paper" Mode** — riassunto clinico strutturato di un paper specifico
- **New Evidence Alert** — notifiche quando esce un paper rilevante per un caso attivo
- **Collegamento trial clinici** — link a AVMA e COTC quando pertinente
- **Export/stampa** — sintesi formattate per la cartella clinica
- **Lente costo-efficacia** — confronto protocolli per costo (farmaci, frequenza visite, monitoraggio) — informazione che la letteratura accademica raramente offre ma i clinici chiedono costantemente

### Fase C — Community Platform (quando ci sono 50+ utenti attivi)
Le feature che creano un moat a lungo termine attraverso network effects:

- **Community Annotations** — oncologi esperti annotano protocolli con note cliniche (flaggate come "esperienza clinica, non evidenza peer-reviewed")
- **"Veterinarian-Verified" Badge** — sintesi confermate da N veterinari praticanti
- **Case Outcome Registry** — i veterinari contribuiscono outcome anonimizzati dei casi trattati. Nel tempo, questo crea un dataset di real-world evidence che complementa la letteratura pubblicata. Questo è il **moat a lungo termine** che trasforma ASIA da tool di letteratura a piattaforma di evidenza
- **Journal Club Tool** — gruppi di veterinari (clinica, facoltà) fanno journal club strutturati attraverso ASIA
- **Gamified Literature Review** — "Aiuta ASIA a migliorare": presenta abstract ai vet, chiedi rilevanza clinica e qualità. Crowdsource la curation del corpus

### Espansioni future

- **Altri tumori** — mastocitoma, osteosarcoma, emangiosarcoma, melanoma orale (forme con letteratura ricca)
- **Altre forme di linfoma** — alimentare, mediastinico, extranodale, cutaneo
- **Altre specie** — gatti, cavalli (con letterature e percorsi clinici distinti)
- **Multilingua** — spagnolo, portoghese, tedesco, francese. L'architettura deve supportarlo dall'inizio
- **Pet Owner Companion Mode** — interfaccia semplificata per proprietari. Potrebbe invertire il modello di adozione: i proprietari scoprono ASIA e lo consigliano al veterinario
- **Ponte oncologia comparata** — mostrare paralleli con l'oncologia umana ("Questo protocollo CHOP è analogo a R-CHOP nell'NHL umano"). Attrae un secondo pubblico (ricercatori) e potenzialmente funding
- **Bot WhatsApp/Telegram** — per il mercato italiano, un bot in un'interfaccia familiare potrebbe avere adozione più alta di una web app
- **Offline-first mobile** — cache delle query più comuni per cliniche rurali senza connessione affidabile
- **Voice query** — input vocale in italiano per uso a mani occupate in clinica
- **Integration con practice management software** — export strutturato verso i gestionali veterinari
- **Conference integration** — sintesi in tempo reale degli abstract presentati a conferenze oncologiche (ESVONC, VCOG)

---

## Partnership strategiche

### Facoltà veterinarie italiane
Bologna, Milano, Torino, Napoli. Offrire ASIA come strumento didattico. Gli studenti imparano l'oncologia evidence-based attraverso ASIA. La facoltà contribuisce annotazioni esperte. ASIA ottiene credibilità, distribuzione e un feedback loop. Questo è il **flywheel di adozione**.

### NCI Comparative Oncology Program
Il programma di oncologia comparata dell'NIH studia i cancri canini come modelli per il cancro umano. ASIA come tool open-source si allinea con la loro missione di rendere i dati accessibili. Potenziale fonte di funding e visibilità.

### Community open source
L'autenticità del progetto (la storia di Asia) è un vantaggio unico. Ogni altro tool in questo spazio è corporate. ASIA è personale. La storia attrae contributor in modo diverso rispetto a un progetto puramente tecnico.

---

## Suggerimenti tecnici

> **Nota:** Questa sezione contiene suggerimenti iniziali basati sull'analisi di mercato e sulla letteratura tecnica. Le decisioni tecniche definitive verranno prese nelle fasi appropriate del processo di design.

### Backend
Python è il candidato naturale. L'ecosistema per NLP, embedding models, parsing di letteratura scientifica e integrazione con API biomediche (BioPython, sentence-transformers, LangChain/LlamaIndex) è incomparabilmente più maturo in Python. FastAPI offre async nativo, type hints e generazione automatica OpenAPI.

### Frontend
Un framework React-based (Next.js o React + Vite). L'importante è che supporti streaming SSE (per le risposte RAG) e sia responsive (veterinari usano tablet in clinica — design tablet-first).

### Database
PostgreSQL con pgvector potrebbe coprire tutte le esigenze con un singolo database: dati relazionali, full-text search (tsvector), e ricerca semantica (vector similarity). Un singolo DB semplifica enormemente il deploy open source.

### RAG Pipeline
Il cuore del sistema. La ricerca accademica suggerisce:
- **Hybrid search** (semantic + keyword con Reciprocal Rank Fusion) come best practice corrente
- **Self-Reflective RAG** per mitigazione hallucination (riduce al 5.8%)
- **Checker models** per verificare allineamento claim-fonte (pattern di Consensus)
- **Medical Graph RAG** (ACL 2025) come architettura di riferimento — usa PubMed web-based search, ha demo Docker disponibile
- Provider LLM swappabile per evitare lock-in

### Ingestion
Job schedulato (non serve un sistema di code distribuito per MVP). Rate limiting rispettoso delle API (PubMed: 3-10 req/s, Semantic Scholar: 1 req/s). Backoff esponenziale.

### Embedding model
Modelli biomedici (PubMedBERT, BioLinkBERT) sono candidati, ma vanno benchmarkati contro modelli generici più recenti. La ricerca mostra che modelli generici più grandi a volte battono quelli domain-specific più vecchi.

### Riferimenti open source rilevanti
- **Medical Graph RAG** (ACL 2025) — [GitHub](https://github.com/ImprintLab/Medical-Graph-RAG) — architettura RAG medica con graph
- **Awesome AI Agents for Healthcare** — [GitHub](https://github.com/AgenticHealthAI/Awesome-AI-Agents-for-Healthcare) — curated list di progetti AI sanitari
- Nessun progetto open-source veterinario AI è stato trovato — ASIA sarebbe il primo

---

## Cosa ASIA non è

- **Non è un motore di ricerca generico** — è focalizzato sull'oncologia veterinaria, con contesto clinico
- **Non è un sistema diagnostico** — non prende decisioni, le supporta. Mai "ASIA raccomanda" — sempre "la letteratura suggerisce"
- **Non è un sostituto di PubMed** — è un layer sopra PubMed (e altre fonti) che aggiunge sintesi, contesto clinico e lingua italiana
- **Non è un prodotto chiuso** — è open source, auditabile, deployabile da chiunque
- **Non è un servizio di laboratorio** — a differenza di ImpriMed e FidoCure, ASIA lavora sulla letteratura pubblicata, non su campioni biologici
- **Non è un tool per ricercatori** — è pensato per clinici sotto pressione temporale, non per chi ha tempo di leggere 40 paper

---

## Prossimi passi

1. **User interviews** con 5-10 veterinari italiani — validare il problema, le feature prioritarie, e le query reali
2. **Corpus analysis** — query PubMed per linfoma multicentrico canino, stimare volume e disponibilità open access, definire il "core 200" paper
3. **Technical spike** su Semantic Scholar API — proof of concept che valida la pipeline dati
4. **Benchmark LLM** — testare 3-4 modelli su sintesi veterinaria in italiano, verificare viabilità di modelli locali
5. **Review legale** — posizionamento regolatorio EU, disclaimer, privacy (GDPR per utenti italiani)
6. **Design architetturale** — procedere con la fase di design (nwave)

---

## Documenti di riferimento

- [Brainstorm completo](brainstorm.md) — 40 idee esplorate con trade-off e analisi strategica
- [Market Research](market-research.md) — 37 fonti, analisi di 6 aree, knowledge gaps e raccomandazioni

---

*ASIA — perché la migliore evidenza scientifica disponibile dovrebbe essere a portata di mano di ogni veterinario, in ogni clinica, per ogni paziente.*
