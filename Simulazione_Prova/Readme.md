# 📊 Progetto - Raccolta e Analisi Dati sulla Pesca in Italia

## 🧾 OGGETTO

La prova consiste nella progettazione e realizzazione di alcuni componenti software costituenti un’applicazione per la raccolta di dati riguardo il settore economico della pesca in Italia, la loro normalizzazione in un database di raccolta e la successiva analisi con strumenti matematico-statistici su viste tabellari e/o grafiche.

---

## 📖 DESCRIZIONE

L’Italia, al centro del mediterraneo, è un paese con una importante economia legata alla pesca.  
È richiesto di predisporre alcune componenti software per la raccolta dei dati relativi, per la loro pulizia e normalizzazione, per il calcolo di alcune analisi statistiche, produzione di una API di esposizione metriche calcolate ed eventuale presentazione dei dati in formati tabellari e/o grafici.

---

## ✅ REQUIREMENTS

L’applicazione deve prevedere:

1. Una **struttura database** atta ad ospitare i dati descritti nei punti successivi.

2. Uno **script, o processo**, in un linguaggio a piacere, di **importazione dei 3 dati pubblici**, a partire da uno dei formati resi disponibili dalle pagine elencate nel paragrafo **COLLEGAMENTI DATI PUBBLICI** e **ALTRI DATI**, su altrettante **tabelle strutturate a piacere**, ma che siano sufficienti a contenere tutto il dato tabellare esposto.

3. Uno **script di post-processamento** dei dati di cui sopra al fine di **normalizzare eventuali dati mancanti** (ad esempio tramite interpolazione di dato mancante temporale: ho il dato di una certa regione del 2001 e del 2004, mancando il 2002 e 2003 li aggiungo in database mediante semplice interpolazione).

4. Il **calcolo di alcune serie dati** specificate nel paragrafo **SERIE CALCOLATE**, e relativa persistenza su base dati con struttura a scelta.

5. Una **API di esportazione** delle **SERIE CALCOLATE** e delle **3 tabelle** con un filtro non limitato `DA ANNO`, `A ANNO` dove `A ANNO >= DA ANNO`.

6. **(FACOLTATIVO)** Un esempio di **plottaggio** via linguaggio scelto o mediante applicazione web + API di una delle **SERIE CALCOLATE** a scelta.

---

## 📈 SERIE CALCOLATE

Una volta importati e normalizzati i dati si potrà procedere, come descritto al punto 4 dei **REQUIREMENTS**, al calcolo delle seguenti serie, **sempre PER ANNO**:

1. **Produttività totale** (in migliaia di euro) delle 5 Aree: Nord-ovest, Nord-est, Centro, Sud, Isole.
2. **Produttività totale nazionale** (in migliaia di euro).
3. **Media percentuale del valore aggiunto** pesca/piscicoltura per le 5 Aree: Nord-ovest, Nord-est, Centro, Sud, Isole.
4. **Media variazione percentuale occupazione nazionale**.
5. **Media variazione percentuale occupazione** delle 5 Aree: Nord-ovest, Nord-est, Centro, Sud, Isole.

📌 **Nota metodologica**:  
Non avendo la quantità di riferimento per le percentuali di cui ai punti sopra, si accetta il loro utilizzo e calcolo **in modo non proporzionato**.

---

## 📦 DELIVERABLES

- 🗄️ Creare la **base dati** necessaria alla gestione dell’applicazione.

- 🔧 Sviluppare le **componenti backend** delle funzionalità indicate nei Requirements.

### ℹ️ Requisiti tecnici aggiuntivi

- Il linguaggio di **back-end è scelto liberamente** tra quelli insegnati nel corso.
- La comunicazione **backend/frontend deve avvenire via Web API su protocollo HTTP**.
- Per la **persistenza dei dati** è possibile utilizzare qualsiasi tecnologia:
  - **Database relazionali** (es. MySQL, SQL Server…)
  - **NoSQL** (es. MongoDB…)
