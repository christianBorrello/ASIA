# Interview Log -- ASIA Vet Oncology

**Feature ID**: asia-vet-oncology
**Date**: 2026-03-31
**Status**: Questionnaire designed, ready to deploy

---

## Interview Strategy

Standard discovery calls for 5-8 live interviews. Our constraints:

- **Access**: 1 vet team (Asia's veterinary team)
- **Format**: Vets are time-pressed; a form they fill at their convenience is lower friction than scheduling interviews
- **Goal**: Capture past behavior and real pain points BEFORE showing them the MVP

The questionnaire is designed following Mom Test principles:
- Questions about past behavior, not future intent
- No mention of ASIA or the solution until Part 2
- Seeks specific examples, not opinions
- Tests commitment, not enthusiasm

---

## Pre-Interview: Christian's Input (Founder as Proxy)

**Date**: 2026-03-31
**Source**: Christian (pet owner, direct experience with the problem)

| Question | Response | Evidence Type |
|----------|----------|---------------|
| What triggered this project? | Asia's diagnostic journey -- months of visits, exams, overlapping hypotheses before a radiograph revealed a mass near the heart. Suspected mediastinal lymphoma with hypercalcemia | Past behavior (lived experience) |
| What was the hardest part? | "The diagnostic phase was very difficult because the case was complicated" | Emotional intensity (frustration) |
| What do you believe the tool could have changed? | "Could have made a difference in reaching a diagnosis faster" | Assumption (not validated with vets yet) |
| Access to vets? | Only Asia's vet team. No broad network | Constraint |
| How to validate? | Build MVP and present to vet team. Use a form/questionnaire for structured feedback | Preferred approach |
| Pricing model? | Free for professionals | Decision |

**Assessment**: Christian's experience confirms the problem exists from the owner's side. The key gap is vet-side confirmation. His instinct to build-then-validate is pragmatic given his constraint (one vet team, no broad access).

---

## Questionnaire Design

The questionnaire has 3 parts:
1. **Part 1 (Pre-MVP)**: About their current workflow -- deploy BEFORE showing the MVP
2. **Part 2 (During/After MVP Demo)**: Reaction to ASIA after seeing it
3. **Part 3 (Commitment Test)**: Would they actually use it?

Parts 2 and 3 are deployed after the MVP demo. Part 1 should go out as soon as possible.

---

## QUESTIONARIO PER IL TEAM VETERINARIO

### Parte 1: Il Vostro Lavoro Oggi (PRIMA di vedere ASIA)

*Questo questionario ci aiuta a capire come gestite i casi oncologici oggi. Non ci sono risposte giuste o sbagliate -- ci interessa la vostra esperienza reale. Richiede circa 10 minuti.*

---

**Contesto professionale**

1. Da quanti anni gestite casi oncologici nella vostra pratica?

2. Approssimativamente quanti casi oncologici canini gestite in un mese?

3. Di questi, quanti sono linfomi?

---

**L'ultimo caso complesso**

*Pensate all'ultimo caso oncologico canino che vi ha richiesto di cercare informazioni nella letteratura scientifica.*

4. Che tipo di caso era? (specie, tumore, stadio -- quello che ricordate)

5. Qual era la domanda clinica specifica a cui cercavate risposta?

6. Dove avete cercato le informazioni? (Selezionate tutto cio che si applica)
   - [ ] PubMed / Google Scholar
   - [ ] VIN (Veterinary Information Network)
   - [ ] Plumb's
   - [ ] Libri di testo
   - [ ] Colleghi / specialisti (telefono, email, WhatsApp)
   - [ ] Altro: _______________

7. Quanto tempo ci e voluto per trovare una risposta soddisfacente?
   - [ ] Meno di 15 minuti
   - [ ] 15-30 minuti
   - [ ] 30-60 minuti
   - [ ] Piu di un'ora
   - [ ] Non ho trovato una risposta soddisfacente

8. Qual e stata la parte piu difficile di quella ricerca?

9. Alla fine, quanto eravate sicuri che la decisione presa fosse supportata dalla migliore evidenza disponibile?
   - [ ] Molto sicuro/a
   - [ ] Abbastanza sicuro/a
   - [ ] Poco sicuro/a
   - [ ] Per niente sicuro/a

---

**Barriere quotidiane**

10. Nella vostra esperienza, la letteratura scientifica in inglese e un ostacolo nella pratica clinica quotidiana?
    - [ ] Si, significativo -- rallenta molto il mio lavoro
    - [ ] Si, moderato -- riesco a leggere ma con fatica
    - [ ] No, leggo l'inglese scientifico senza problemi
    - [ ] Non cerco letteratura in inglese (uso altre fonti)

11. Quando dovete confrontare protocolli terapeutici (es. CHOP-19 vs CHOP-25 vs COP), come fate oggi?

12. Pensate a un momento durante una chemioterapia in cui avete dovuto prendere una decisione rapida su un effetto collaterale (es. neutropenia, tossicita GI). Come avete gestito la ricerca di informazioni in quel momento?

13. Quanto tempo dedicate mediamente alla comunicazione con il proprietario per spiegare diagnosi e opzioni terapeutiche per un caso oncologico?
    - [ ] Meno di 10 minuti
    - [ ] 10-20 minuti
    - [ ] 20-30 minuti
    - [ ] Piu di 30 minuti

---

**Strumenti e apertura al cambiamento**

14. Usate gia strumenti digitali per supportare le vostre decisioni cliniche? Se si, quali?

15. Cosa manca negli strumenti che usate oggi per l'oncologia?

16. Avete mai usato strumenti basati su intelligenza artificiale (come ChatGPT, Perplexity, o simili) per domande cliniche? Se si, raccontate un esempio specifico.

17. Se li avete usati: vi siete fidati della risposta? Perche si o perche no?

---

### Parte 2: Dopo Aver Visto ASIA (durante o dopo la demo)

*Avete appena visto ASIA rispondere a domande sul linfoma canino. Queste domande riguardano la vostra reazione.*

---

18. Qual e stata la vostra prima reazione vedendo la risposta di ASIA?

19. Per ciascuna delle 5 domande mostrate, quanto era accurata la risposta? (1 = imprecisa, 5 = accurata)

    | Domanda | Accuratezza (1-5) | Commento |
    |---------|-------------------|----------|
    | Protocollo prima linea B-cell stadio III | | |
    | CHOP-19 vs CHOP-25 | | |
    | Rescue dopo CHOP | | |
    | Prognosi T-cell vs B-cell | | |
    | Dose doxorubicina e neutropenia | | |

20. Avete notato errori o imprecisioni nelle risposte? Se si, quali?

21. Le citazioni ai paper originali vi sono parse:
    - [ ] Molto utili -- ho verificato e corrispondevano
    - [ ] Utili -- non ho verificato ma mi danno fiducia
    - [ ] Poco utili -- non le guarderei comunque
    - [ ] Problematiche -- ho notato citazioni non corrette

22. La qualita dell'italiano medico nelle risposte era:
    - [ ] Naturale e corretta
    - [ ] Accettabile con qualche imprecisione
    - [ ] Mediocre -- termini sbagliati o innaturali
    - [ ] Inaccettabile per uso clinico

23. Quanto vi fidereste di questa risposta per prendere una decisione clinica? (1 = per niente, 5 = molto)

24. Se questo strumento fosse esistito durante il caso di Asia, avrebbe cambiato qualcosa nel vostro percorso diagnostico o terapeutico? In che modo?

25. Cosa manca in queste risposte che avreste bisogno di vedere per considerare lo strumento utile nella pratica?

---

### Parte 3: Test di Impegno (Commitment Test)

*Queste ultime domande ci aiutano a capire se ASIA ha un futuro reale.*

---

26. Se ASIA fosse disponibile domani (gratis), lo usereste per il vostro prossimo caso oncologico?
    - [ ] Si, lo proverei subito
    - [ ] Forse, se avessi un caso adatto
    - [ ] Probabilmente no
    - [ ] No

27. Per quale tipo di domanda clinica lo usereste per primo?

28. C'e un collega a cui consigliereste di provarlo? (Se si, sareste disposti a fare un'introduzione?)

29. Preferireste usare ASIA come:
    - [ ] Sito web
    - [ ] App mobile
    - [ ] Bot WhatsApp/Telegram
    - [ ] Integrato nel gestionale della clinica
    - [ ] Altro: _______________

30. La cosa piu importante che ASIA dovrebbe fare per diventare uno strumento che usate regolarmente e: _______________

---

## Come Interpretare le Risposte

### Segnali forti (problem validated):
- Domanda 7: "Piu di un'ora" o "Non ho trovato risposta" = friction reale
- Domanda 8: Risposta dettagliata e specifica = il problema e vissuto
- Domanda 10: "Significativo" o "Moderato" = language barrier confirmed
- Domanda 12: Descrizione di un momento di stress con ricerca difficile = micro-decision pain confirmed
- Domanda 20: Nessun errore trovato = feasibility validated
- Domanda 26: "Si, lo proverei subito" + Domanda 28: "Si, posso presentarvi [nome]" = commitment reale

### Segnali deboli (more investigation needed):
- Domanda 7: "Meno di 15 minuti" = forse il problema non e percepito come grave
- Domanda 10: "Leggo l'inglese senza problemi" = language barrier assumption challenged
- Domanda 26: "Forse" = politeness, not commitment
- Domanda 30: Risposta generica = disengagement

### Kill signals:
- Domanda 20: Errori multipli trovati nelle risposte = feasibility risk
- Domanda 22: "Inaccettabile" = Italian quality risk
- Domanda 23: Rating 1-2 = trust barrier too high
- Domanda 26: "No" from multiple vets = adoption risk confirmed
- Domanda 8: "Non e un problema" = problem hypothesis wrong

---

## Interviews Completed

| # | Date | Participant | Type | Key Findings |
|---|------|------------|------|-------------|
| 0 | 2026-03-31 | Christian (founder/owner) | Pre-interview | Problem experienced from owner side; diagnostic delay; believes tool would have helped |
| 1 | TBD | Vet team member 1 | Questionnaire | Pending |
| 2 | TBD | Vet team member 2 | Questionnaire | Pending |
| 3 | TBD | Vet team member 3 | Questionnaire | Pending |

---

## Notes for Christian

- **Consegna Parte 1 il prima possibile** -- idealmente prima di iniziare a sviluppare l'MVP, cosi catturi il loro stato "prima" senza influenzarli
- **Parti 2 e 3 vanno dopo la demo** -- quando il veterinario ha visto ASIA in azione
- **Se possibile, consegna a mano** -- il tasso di risposta sara molto piu alto rispetto a una email
- **Non vendere il progetto** -- di' qualcosa come: "Sto lavorando a un progetto ispirato dal caso di Asia e vorrei capire se ha senso. Mi aiutereste a trovare gli errori?"
- **Il framing "aiutami a trovare errori"** e fondamentale -- attiva la modalita critica, non la cortesia
