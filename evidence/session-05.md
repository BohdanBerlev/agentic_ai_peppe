# Evidence Session 5 – Kundenänderung `CR-01`, Sicherheitsantwort `SR-01`, Factory `F-NEW-v1.0` & Gesamtbilanz T3–T5

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-09  
**Kunde:** Nordwerk Industrie-Service (Hamburg) · Projekt-ID: `client-01`  
**Session:** `session-05`  
**LLM-Provider-Ausnahmegenehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md)

---

## 0. Vollständige Aufarbeitung des Feedbacks aus Termin 4 (`92/100 Punkte`)

Referenz: [`docs/Review/Feedback_Session_04_Team_3.md`](../docs/Review/Feedback_Session_04_Team_3.md)

| Feedback-Punkt aus Termin 4 | Durchgeführte Lösung & Verweis | Status |
| :--- | :--- | :--- |
| **1. `R-01` reproduzierbar machen (`F-BASE = 6da5414` im Text vs. Git-Tag `5a146a3`)** | Forensisch geklärt und in [`evidence/R01-comparison.md`](R01-comparison.md) dokumentiert: Der `R-01`-Baseline-Lauf `0cef313b` startete am `2026-11-02T09:26:52Z` mit `requests_per_second=0.08` (`max_retries=6`), was exakt dem 3 Minuten später um `09:30 Uhr` committeten und als **`F-BASE` (`5a146a3`)** getaggten Factory-Stand entspricht (`6da5414` von `00:55 Uhr` war der vorangegangene Doku-Commit). Der separate Produkt-Commit von `R-01` liegt reproduzierbar auf `origin/experiment/r-01-baseline` (**`ad7d304`**, direkt abgezweigt von `R-BASE` = `18d222b`). | ✅ **Erledigt** |
| **2. Freigabe an Produktstand binden & Zugänglichkeit Produkt-Repo** | Produkt-Repository (`https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website`) enthält alle getaggten Stände (`v0.1.0-t3` = `3e6121b`, `v0.2.0-rc1` / `R-BASE` = `18d222b`, `CR-01-v1.0` / `v0.3.0` = `f2feebb` / `263d007`). In [`docs/customer-01/acceptance.md`](../docs/customer-01/acceptance.md) und [`evidence/hand-over.md`](hand-over.md) sind Commit, Diff, Testergebnis und menschliche Freigabe eindeutig verknüpft. | ✅ **Erledigt** |
| **3. GitHub-Actions-Läufe (inkl. gescheiterter Issue-Reviewer-Läufe) & Gemini-Freigabe erfassen** | Alle **111 GitHub-Actions-Läufe** des Factory-Repos wurden über die GitHub-API ausgewertet und in [`costs/usage.csv`](../costs/usage.csv) sowie Abschnitt 7 unten erfasst: **53 `CI`-Läufe** (`51 success`, `2 failure`) und **58 `Agentic Issue Reviewer`-Läufe** (`11 success`, `47 failure`, davon `23` Webhook-Fehlläufe am `2026-11-02` bei Issue-Edits ohne CI-Quota bzw. vor `Intended actor = Agent`-Filterung PR #57). Die formale Gemini-Freigabe liegt in [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md). | ✅ **Erledigt** |

---

## 1. Repository-Trennung, Commits & Versionierte Tags (`A1`, `A4`, `B6`, `D2`)

| Rolle / Stand | Repository / Branch | Eingabe-Commit | Ergebnis-Commit & Git-Tag |
| :--- | :--- | :--- | :--- |
| **Produkt-Basis aus Termin 4 (`R-BASE`)** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` (`main`) | `fef6a55` | **`18d222b`** (Tags: **`v0.2.0-rc1`**, **`R-BASE`**) / `7805e3b` (inkl. README) |
| **Produkt-Release Termin 5 (`CR-01`)** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` (`main` & `cr-01-factory`) | `7805e3b` / `316b5d4` | Agent-Commits **`5227307`** (Lauf A: `index_en.html`) $\rightarrow$ **`263d007`** (Lauf B: `index.html`) $\rightarrow$ Release-Commit **`f2feebb`** (Tags: **`CR-01-v1.0`**, **`v0.3.0`**) |
| **`R-01` Baseline-Ergebnis (Termin 4)** | `Nordwerk-Industrie-Service-Website` (`origin/experiment/r-01-baseline`) | `18d222b` (`R-BASE`) | **`ad7d304`** (isoliert vom Kunden-Release `main`) |
| **Factory-Baseline (`F-BASE`, Termin 4)** | `https://github.com/BohdanBerlev/agentic_ai_peppe` (`main`) | `6da5414` | **`5a146a3`** (Tag: **`F-BASE`**) |
| **Factory-Verbesserung (`F-NEW-v1.0`, Termin 5)** | `https://github.com/BohdanBerlev/agentic_ai_peppe` (`main`) | `5a146a3` (`F-BASE`) | Code-Commit `f803ece` / `0da8ba0` + Test `test_factory_fnew_t5.py` (Tag: **`F-NEW-v1.0`**) |

---

## 2. Kundenänderung `CR-01`: Englische Einstiegsseite & Zielgruppen-Erweiterung (`A1`–`A3`, `B1`–`B3`, `L5.1`)

### 2.1 Änderungs-Issue & Auswirkungsanalyse (`A1`)
- **Spezifikation im Produkt-Repo:** [`client-01-website/issue_cr01.md`](../client-01-website/issue_cr01.md) (Commit `316b5d4`, ausgehend vom Termin-4-Release-Candidate `7805e3b` / `v0.2.0-rc1`).
- **Auswirkungsanalyse:**
  - **Neu:** `index_en.html` (`<html lang="en">`) mit allen wörtlichen Pflichtinhalten aus dem Aufgabenblatt Termin 5 (*Nordwerk Industrie-Service*, *Practical support for your technical operations.*, *Maintenance planning*, *Spare parts coordination*, *Operational documentation*, *Technical purchasing departments*, *Request information* $\rightarrow$ `mailto:kontakt@nordwerk.example`, *Fictional company – HAW Hamburg course project. No real offers or contact.*, Rücklink `Deutsch` auf `index.html`).
  - **Geändert:** `index.html` erhält die zusätzliche Zielgruppe *„Technische Einkaufsabteilungen“* unter `#zielgruppen` sowie den Sprachwechsel-Link `<a href="index_en.html" hreflang="en" lang="en">English</a>` in der `<nav>`.
  - **Unverändert / Regressionsschutz:** Alle bestehenden deutschen Pflichtinhalte (`N-01` bis `N-09`, `AC-01` bis `AC-08`) bleiben unverändert und werden durch `test_website.py` (`F1`–`F4`) und `test_cr01.py` automatisch geschützt.

### 2.2 Echte Factory-Läufe für `CR-01` (`A2`, `A3`)

Beide Läufe wurden mit derselben zentralen Factory (`src.workflows.feature_pipeline --full-company --use-backend-agent`, 8 kooperierende Agentenrollen: `product_owner_requirements`, `project_manager`, `agent_engineer`, `software_architect`, `backend_api_engineer`, `qa_test_engineer`, `ai_safety_security_engineer`, `integration_engineer`) und aktivem Qualitätsgate ausgeführt:

| Lauf | Zieldatei | Workflow-ID & Trace | Agenten-Laufzeit | Menschliche Gate-Zeit | Agenten-Kosten | Automatisierter Test im Gate | Produkt-Commit & Freigabe |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lauf A (EN)** | `index_en.html` | [`52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl`](session-05/52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl) | `43,53 s` | `39,06 s` | `8,6905 Credits` | `python test_cr01_en.py` $\rightarrow$ `Exit-Code 0` (`F1`–`F4` + `CR-01 EN` PASSED) | Commit **`5227307`** · Freigabe: **Mehrose Farooq** (`approved`) |
| **Lauf B (DE)** | `index.html` | [`c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl`](session-05/c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl) | `42,45 s` | `39,94 s` | `8,7329 Credits` | `python test_cr01.py` $\rightarrow$ `Exit-Code 0` (`F1`–`F4` + `CR-01 EN` + `CR-01 DE` PASSED) | Commit **`263d007`** · Freigabe: **Mehrose Farooq** (`approved`) |

### 2.3 Dokumentierte menschliche Eingriffe (`A2`)
1. **Vorbereitung vor dem Agentenlauf (Commit `316b5d4`, Lars Boos):** Erstellung von `issue_cr01.md`, `test_cr01.py`, `test_cr01_en.py` und einem leeren Starter-Gerüst `index_en.html` (`<title>TODO</title>`).
2. **Interaktive Gate-Entscheidungen (Mehrose Farooq):** Prüfung und Freigabe von Lauf A (`39,06 s`) und Lauf B (`39,94 s`) am Human Approval Gate. **Am HTML-Output des `backend_agent` (`index_en.html` in `5227307` und `index.html` in `263d007`) wurde keine Zeile manuell nachbearbeitet.**
3. **CSS-Selektor-Aliase & Release-Dokumentation (Commit `f2feebb`, David Pisarkiewicz):** Ergänzung von Selektor-Aliasen (`.logo`, `.lead`, `.card`, `.audiences`, `.btn`) in `styles.css` sowie Ablage von `SR-01-response.md` und `HANDOVER.md` im Produkt-Repo.

### 2.4 Automatisierte Regression & Manuelles Browser-/Tastatur-Review (`A3`, `B1`–`B3`)
- **Automatisierte Prüfungen (`Exit-Code 0`, 0 Regressionen):**
  ```text
  PASSED       F1 Pflichtinhalt (AC-01..AC-04)
  PASSED       F2 Kontakt & Navigation (AC-04, AC-05)
  PASSED       F3 Lokale Verweise & Assets / PHP-frei (AC-05, AC-08)
  PASSED       F4 Bedienbarkeit statisch (AC-06/AC-07)
  PASSED       CR-01 EN Englische Ansicht
  PASSED       CR-01 DE Zielgruppe & Sprachwechsel
  ERGEBNIS CR-01: BESTANDEN (0 Regressionen)
  ```
- **Manuelles Browser-Review bei `375 px` und `1280 px` sowie per Tastatur (`Tab` / `:focus-visible`) für beide Ansichten (`index.html` & `index_en.html`):**
  Vollständig durchgeführt und bestanden am `2026-11-09` durch **Lars Boos** und **David Pisarkiewicz** – dokumentiert in **[`docs/customer-01/browser_review_t5.md`](../docs/customer-01/browser_review_t5.md)**.

---

## 3. Sicherheitsanfrage `SR-01` & Komponentenübersicht (`B4`, `B5`, `D1`, `L5.3`)

- **Kundenantwort (max. 1 Seite, inkl. Komponentenübersicht):** **[`evidence/SR-01-response.md`](SR-01-response.md)** (identisch im Produkt-Repo unter [`client-01-website/SR-01-response.md`](../client-01-website/SR-01-response.md)).
- **Technische Detailanalyse:** **[`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md)**.
- **Abgedeckte Pflichtpunkte gemäß Bewertungsraster `B4`, `B5` & `L5.3`:**
  1. **Primärquelle mit Datum:** ENISA-Mitteilung vom **21.10.2026** (*Joint Statement on Critical PHP Vulnerabilities*, `CVE-2026-109618` & `CVE-2026-109619`) inkl. verlinkter PHP-Quelle und Abrufdatum (`2026-11-08` / `2026-11-09`, Kurs-Primärquellenauszug).
  2. **Differenzierung Altsystem (Stand `23.10.2026`) vs. Neusystem:** Erklärt, warum die pauschale Betreiberangabe **„PHP 8.2“ beim bisherigen Auftritt (mit CMS & Kontaktformular) weder Betroffenheit noch Behebung belegt** (ungeklärter Patch-/Backport-Stand, kein Admin-Zugang), während unsere neue statische Lieferung (`CR-01-v1.0`) kein PHP, kein CMS und kein Server-Formular enthält (`F3 PASSED`).
  3. **Keine unbelegte Garantie „statisch = sicher“:** Explizite Klarstellung, dass statisches HTML zwar PHP-/CMS-Lücken im Anwendungscode ausschließt, aber Webserver-Härtung, Deaktivierung des PHP-Interpreters im Webroot, TLS/HTTPS und sichere Hoster-Zugänge weiterhin zwingend sind.
  4. **Konkrete Hoster-Rückfragen & Vergleich Update vs. Isolation vs. statischer Ersatz:** Vollständig tabellarisch gegenübergestellt.
  5. **Funktionsverlust & Wartungsverantwortung:** Wegfall des Redaktions-CMS und des serverseitigen Kontaktformulars (Ersatz durch `mailto:kontakt@nordwerk.example`) sowie klare Aufteilung der Wartungsverantwortung zwischen Hoster/Nordwerk und Entwicklungsteam.
  6. **Komponentenübersicht (`B4`):** Trennt sauber zwischen (1) ungeklärtem Altsystem (`PHP 8.2`, CMS), (2) ausgelieferten Laufzeitkomponenten (`HTML5`, `CSS3`; PHP/JS/CMS/DB = `nicht verwendet`) und (3) Build-/Test-/Factory-Komponenten (`Python 3.11+`, `pytest`, `langgraph`, `langchain-google-genai`).
  7. **Menschliche Faktenprüfung & Freigabe (`D1` / `L5.3`):** Geprüft und freigegeben durch **David Pisarkiewicz** und **Lars Boos** (`2026-11-09`).

---

## 4. Gezielte Factory-Verbesserung `F-NEW-v1.0` & Empirischer `R-01`-Vergleich (`A4`, `C1`–`C3`, `L5.2`)

- **Implementierte Änderung:** [`src/llm/factory.py`](../src/llm/factory.py) (Tag **`F-NEW-v1.0`**): `@lru_cache(maxsize=4)` auf `resolve_google_model()` (reduziert Modell-Discovery von 8 auf 1 HTTP-GET pro Lauf) sowie Anpassung des `InMemoryRateLimiter` (`requests_per_second: 0.08 -> 0.25`, `max_retries: 6 -> 2`) bei **identischem Modell** (`gemini-3.5-flash-lite`).
- **Deterministischer Unit-Test (`A4`):** [`tests/test_factory_fnew_t5.py`](../tests/test_factory_fnew_t5.py) (`test_resolve_google_model_lru_cache_prevents_redundant_http_calls` $\rightarrow$ `PASSED`; gesamter Testbericht: `76 passed, 2 skipped` in [`evidence/session-05/pytest.xml`](session-05/pytest.xml)).
- **Vollständige Vergleichsanalyse:** **[`evidence/R01-comparison.md`](R01-comparison.md)**
- **Live-Trace `R-NEW`:** [`evidence/session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl`](session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl) (ausgeführt auf frischer Kopie von `R-BASE` = `18d222b`).

| Messgröße | `R-BASE` (`0cef313b`, Termin 4) | `R-NEW` (`24b3bc4f`, Termin 5) | $\Delta$ relativ | Bewertung gegen T4-Hypothese |
| :--- | :--- | :--- | :--- | :--- |
| **Fehlläufe vor Erfolg (`429`)** | `2` (`cc5362a3`, `1b7f1382`) | **`0`** (1. Versuch erfolgreich) | $-100\,\%$ | ✅ Keine Rate-Limit-Abbrüche |
| **Agenten-Laufzeit (`duration_seconds`)** | `118,40 s` | **`44,48 s`** | **$-62,4\,\%$** | ✅ **Ziel ($\ge 40\,\%$ Reduktion) klar übertroffen** |
| **Kosten erfolgreicher Einzellauf** | `9,4473 Credits` | **`8,7024 Credits`** | **$-7,9\,\%$** | ❌ **Ziel ($\ge 30\,\%$ pro Einzellauf) verfehlt** *(da weiterhin 8 Calls)* |
| **Kosten inkl. Fehlläufen** | `22,6063 Credits` | **`8,7024 Credits`** | **$-61,5\,\%$** | ✅ Hohe Gesamtersparnis durch Wegfall der Fehlläufe |
| **Qualität & Regression (`test_r01.py`)** | `Exit-Code 0` (`0` Regressionen) | **`Exit-Code 0` (`0` Regressionen)** | unverändert | ✅ Volle Prüfqualität erhalten |

- **Empirische Entscheidung (`C3`):** **`F-NEW-v1.0` beibehalten (`retain`) und künftig um einen `--lean`-Modus ergänzen (`adapt`)**, da die Laufzeit stabil um $>60\,\%$ sinkt (bestätigt in allen 3 Session-5-Läufen: `44,48 s`, `43,53 s`, `42,45 s`), während für eine $\ge 30\,\%$-Kostensenkung pro Einzellauf die Anzahl der aufgerufenen Agentenrollen bei Kleinständerungen von 8 auf 5 reduziert werden muss.

---

## 5. Abnahme (`AC-01` bis `AC-10`), Technische Freigabe & Übergabe (`B6`, `D1`, `D2`, `L5.4`)

- **Detaillierte Abnahmetabelle (`AC-01` bis `AC-10`):** **[`docs/customer-01/acceptance.md`](../docs/customer-01/acceptance.md)**
- **Übergabeprotokoll:** **[`evidence/hand-over.md`](hand-over.md)** (sowie [`client-01-website/HANDOVER.md`](../client-01-website/HANDOVER.md))
- **Start-, Test- und Wartungsanleitung:** **[`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md)** (sowie [`client-01-website/README.md`](../client-01-website/README.md))
- **Klare Trennung von technischer Freigabe und Kundenstatus (`D1` / `B6`):**
  - **Technischer Freigabestatus (Team 3):** ✅ **Technisch freigegeben** (`approved` durch **Mehrose Farooq**, **David Pisarkiewicz**, **Lars Boos** und **Maxim Bers** am `2026-11-09`; alle Tests `F1`–`F4`, `CR-01 EN`, `CR-01 DE` sowie Browser-Review bestanden).
  - **Kundenabnahme-Status:** ⬜ **Ausstehend (offene Kundenentscheidung durch den Dozenten in Termin 5)** – es wird ausdrücklich **keine** Selbstbehauptung *„vom Kunden akzeptiert“* aufgestellt.

---

## 6. Gesamtkosten-Bilanz T3–T5, CI-Läufe & Budgetabweichungs-Analyse (`C4`, `L5.4`)

Vollständige Rohdaten ohne doppelte Stunden: **[`costs/usage.csv`](../costs/usage.csv)**

### 6.1 Kumulierte Kosten T3–T5 (getrennt nach Kundenlieferung, Experiment `R-01` und Factory-Entwicklung)

| Termin | Aufgabenblock / Kategorie | Menschliche Zeit & Kosten (`100 Cr./h`) | Agenten-Läufe (Erfolg + Fehlläufe) | Agenten-Kosten (`Credits`) | Summe Block (`Credits`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Termin 3** | **Kundenlieferung `TASK-001`** (`v0.1.0-t3`) | `12,5 h` = `1.250,00 Cr.` | 1 Lauf (`bf81352d`) | `30,9069 Cr.` | `1.280,9069 Cr.` |
| **Termin 3** | **Factory-Entwicklung (`FACTORY-DEV`)** | `7,5 h` = `750,00 Cr.` | — | `0,0000 Cr.` | `750,0000 Cr.` |
| **Termin 4** | **Kundenlieferung `TASK-002`** (`v0.2.0-rc1`) | `8,0 h` = `800,00 Cr.` | 1 Lauf (`cb3bcea8`) | `9,5938 Cr.` | `809,5938 Cr.` |
| **Termin 4** | **Experiment `R-01` Baseline** (`R-BASE`) | `5,0 h` = `500,00 Cr.` | 3 Läufe (`0cef313b` + 2 Fehlläufe `cc5362a3`, `1b7f1382`) | `22,6063 Cr.` | `522,6063 Cr.` |
| **Termin 4** | **Factory-Entwicklung (`FACTORY-DEV`)** | `7,0 h` = `700,00 Cr.` | 2 lokale Fault-Injection-Runs (`557714eb`, `0210bc84`) | `0,0000 Cr.` | `700,0000 Cr.` |
| **Termin 5** | **Kundenlieferung `CR-01` + `SR-01`** (`CR-01-v1.0`) | `12,0 h` = `1.200,00 Cr.` *(8,0 h `CR-01` + 4,0 h `SR-01`)* | 2 Läufe (`52b69365` [8,6905 Cr.] + `c0ee2cc3` [8,7329 Cr.]) | `17,4234 Cr.` | `1.217,4234 Cr.` |
| **Termin 5** | **Experiment `R-01` Nachher (`R-NEW`)** | `4,0 h` = `400,00 Cr.` | 1 Lauf (`24b3bc4f`) | `8,7024 Cr.` | `408,7024 Cr.` |
| **Termin 5** | **Factory-Entwicklung (`FACTORY-DEV` `F-NEW-v1.0`)** | `4,0 h` = `400,00 Cr.` | — | `0,0000 Cr.` | `400,0000 Cr.` |
| **Gesamt T3–T5** | **1. Reine Kundenlieferung (`TASK-001` + `TASK-002` + `CR-01` + `SR-01`)** | **`32,5 h` = `3.250,00 Cr.`** | **4 erfolgreiche Produkt-Läufe (0 Fehlläufe)** | **`57,9241 Cr.`** | **`3.307,9241 Cr.`** |
| **Gesamt T3–T5** | **2. Referenzexperiment `R-01` (`R-BASE` + `R-NEW`)** | **`9,0 h` = `900,00 Cr.`** | **2 Erfolge + 2 Fehlläufe (`429`)** | **`31,3087 Cr.`** | **`931,3087 Cr.`** |
| **Gesamt T3–T5** | **3. Übergreifende Factory-Entwicklung (`FACTORY-DEV`)** | **`18,5 h` = `1.850,00 Cr.`** | **76 `pytest`-Tests lokal + 111 GitHub-Actions-Runs** | **`0,0000 Cr.`** | **`1.850,0000 Cr.`** |
| **GESAMT T3–T5** | **Alle Aktivitäten T3–T5 (4 Mitglieder × 3 Termine × 5 h = 60,0 h)** | **`60,0 h` = `6.000,00 Cr.`** | **8 Pipeline-Läufe (6 Erfolge, 2 Fehlläufe)** | **`89,2328 Cr.`** | **`6.089,2328 Cr.`** |

*(Hinweis zu GitHub Actions T2–T5 aus [`costs/usage.csv`](../costs/usage.csv): Insgesamt **111 GitHub-Actions-Workflows** auf GitHub Free-Tier [0 Credits Zusatzkosten], davon **53 `CI`-Testläufe** [`51 success`, `2 failure`] und **58 `Agentic Issue Reviewer`-Webhook-Läufe** [`11 success`, `47 failure` bei Issue-Edits vor/während T4]).*

### 6.2 Budgetabweichungs-Analyse (Geplantes Kundenbudget vs. Ist-Aufwand T3–T5)
- **Geplantes Kunden-Lieferbudget aus Termin 3:** `1.200,00 Credits` Basis-Lieferbudget (T3/T4) + `400,00 Credits` Änderungsreserve (T5) = **`1.600,00 Credits` Gesamtbudget**.
- **Tatsächlicher Kunden-Lieferaufwand (`TASK-001` + `TASK-002` + `CR-01` + `SR-01`):** **`3.307,92 Credits`** (`3.250,00 Credits` menschliche Arbeit [`32,5 h`] + `57,92 Credits` LLM-Agentenläufe).
- **Budgetabweichung:** **`+1.707,92 Credits` (`+106,7 %` über Zielbudget)**.
- **Ursachenanalyse der Abweichung:**
  1. **Menschliche Stunden dominieren zu 98,2 % die Lieferkosten (`3.250,00` von `3.307,92 Credits`):** Die reinen LLM-Agentenkosten für alle 4 produktiven Kundenläufe (`TASK-001`, `TASK-002`, `CR-01 A`, `CR-01 B`) betrugen zusammen nur **`57,92 Credits`** (`3,6 %` des 1.600-Credit-Budgets!). Die Überschreitung entstand ausschließlich dadurch, dass 4 Teammitglieder bei jedem Termin die Pflicht-Sichtprüfungen (375/1280 px, Tastatur), Issue-/Test-Spezifikationen (`issue_t3.md`, `issue_t4.md`, `issue_cr01.md`), Sicherheitsanalysen (`SR-01`) und Evidenz-Dokumentationen erstellt haben.
  2. **Deutlicher Produktivitätsgewinn der Factory von T3 zu T5:** Während der erste Kundenlauf `TASK-001` in T3 noch `2.239,75 s` (`30,91 Credits`) benötigte, liefen `TASK-002` in T4 in `94,24 s` (`9,59 Credits`) und die beiden `CR-01`-Läufe in T5 dank `F-NEW-v1.0` in nur noch **`43,53 s` bzw. `42,45 s`** (`8,69` bzw. `8,73 Credits`).

---

## 7. Drei belegte, übertragbare Factory-Erkenntnisse aus T3–T5 (`C4`, `L5.4`)

| # | Übertragbare Erkenntnis (Lesson Learned) | Empirischer Beleg im Projekt (T3–T5) | Konsequenz für zukünftige Kundenprojekte |
| :--- | :--- | :--- | :--- |
| **1** | **Vorab-Review-Stände (Pre-Implementation) dürfen nach erfolgreicher Code-Generierung und grünem QA-Test das Release-Gate nicht dauerhaft blockieren.** | In **Termin 3** (`bf81352d`) markierte der `software_architect` das leere Starter-Template vor dem `backend_agent`-Lauf korrekt mit `changes_requested`; obwohl `backend_agent` und `qa_test_engineer` (`test_website.py`) danach bestanden, blieb die Gesamtempfehlung auf `changes_requested`. Durch den Fix in [`_compute_agent_recommendation`](../src/workflows/feature_pipeline.py) (Commit `b112623`) wurde dieses Fehlverhalten behoben – in **Termin 5 Lauf A** (`52b69365`) meldete der Architect am leeren `index_en.html`-Gerüst erneut `changes_requested`, das Gate de-eskalierte nach grünem `test_cr01_en.py` jedoch vollautomatisch und korrekt auf `agent_recommendation: "approved"`. | In mehrstufigen Agenten-Graphen müssen Vorab-Befunde als *Input-Auftrag* für den Implementierungs-Agenten modelliert werden, während das Freigabe-Gate strikt am *Post-Implementation-Artefakt* hängt. |
| **2** | **Deterministische, domänenspezifische Prüffamilien am Gate schlagen reine LLM-Selbstbewertungen und müssen durch gezielte Fault-Injection validiert werden.** | In **Termin 4** haben wir die Produktprüfung in 4 deterministische Prüffamilien (`F1`–`F4` in [`test_website.py`](../client-01-website/test_website.py)) plus `enforce_quality_gate()` in [`feature_pipeline.py`](../src/workflows/feature_pipeline.py) überführt. Die beiden kontrollierten Fehlerinjektionen ([`557714eb.json`](session-04/fault-injection/557714eb-efba-4260-af95-46ee17d95e22.json) Kontaktfehler & [`0210bc84.json`](session-04/fault-injection/0210bc84-e836-4066-adc5-c6bf7fcfe032.json) defekter Ankerlink) bewiesen, dass `quality_gate_blocked=True` jede Freigabe technisch verhindert, bis der Fehler behoben ist. In **Termin 5** schützten dieselben 4 Familien `index.html` bei `CR-01` ohne jede Regression. | Für jedes neue Kundenprojekt zuerst einen schnellen, deterministischen Akzeptanz- & Security-Check (`F1`–`F4`) schreiben und diesen technisch erzwingend ans Human Gate koppeln. |
| **3** | **Infrastruktur-Optimierungen (Caching & Rate-Limiting) halbieren die Durchlaufzeit, aber echte Token-/Credit-Einsparungen erfordern aufgabenabhängiges Überspringen redundanter Agentenrollen.** | Im **`R-01`-Experiment (Termin 4 vs. Termin 5, [`R01-comparison.md`](R01-comparison.md))** senkte `F-NEW-v1.0` (`@lru_cache` auf `resolve_google_model()` + Rate-Limiter `0.08 -> 0.25`) die Agenten-Laufzeit drastisch um **$-62,4\,\%$** (`118,40 s` $\rightarrow$ `44,48 s`), die Einzellauf-Credits jedoch nur um **$-7,9\,\%$** (`9,45` $\rightarrow$ `8,70 Credits`), weil weiterhin alle 8 Agentenrollen aufgerufen wurden. Zudem zeigten **47 fehlgeschlagene GitHub-Actions-Issue-Reviewer-Triggers**, dass ungedrosselte Event-Webhooks ohne Vorfilterung (`Intended actor = Agent`, PR #57) unnötige Fehlversuche erzeugen. | Kleine Änderungs-Tasks (`R-01`, `CR-01`) sollten über ein leichtgewichtiges Routing (`--lean`: nur PO $\rightarrow$ Backend $\rightarrow$ QA/Security $\rightarrow$ Gate) laufen, statt bei jeder 2-Zeilen-Änderung alle 8 Rollen aufzurufen. |

---

## 8. Vollständigkeits-Checkliste nach Bewertungsraster Termin 5 (100 Punkte & L5.1–L5.4)

| Kriterium / Lernziel | Status | Beleg / Fundstelle |
| :--- | :--- | :--- |
| **A1–A3 & L5.1 (Kundenänderung durch Factory & Regression)** | ✅ Erfüllt | [`client-01-website/issue_cr01.md`](../client-01-website/issue_cr01.md), Traces [`52b69365`](session-05/52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl) & [`c0ee2cc3`](session-05/c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl), Produkt-Commits `5227307` & `263d007` (Tag `CR-01-v1.0`) |
| **A4, C1–C3 & L5.2 (Factory-Änderung `F-NEW` & ehrlicher `R-01`-Vergleich)** | ✅ Erfüllt | [`src/llm/factory.py`](../src/llm/factory.py) (Tag `F-NEW-v1.0`), Unit-Test [`tests/test_factory_fnew_t5.py`](../tests/test_factory_fnew_t5.py), Trace [`24b3bc4f`](session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl), [`evidence/R01-comparison.md`](R01-comparison.md) |
| **B1–B3 (Englischer Einstieg, Zielgruppe, Sprachwechsel, Browser-Review)** | ✅ Erfüllt | [`client-01-website/index_en.html`](../client-01-website/index_en.html), [`client-01-website/index.html`](../client-01-website/index.html), [`client-01-website/test_cr01.py`](../client-01-website/test_cr01.py), [`docs/customer-01/browser_review_t5.md`](../docs/customer-01/browser_review_t5.md) |
| **B4–B5, D1 & L5.3 (Komponentenübersicht, `SR-01`-Antwort & Faktenprüfung)** | ✅ Erfüllt | [`evidence/SR-01-response.md`](SR-01-response.md), [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md), [`client-01-website/SR-01-response.md`](../client-01-website/SR-01-response.md) |
| **B6, C4, D2 & L5.4 (Übergabe, Gesamtkosten T3–T5, 3 Erkenntnisse, Abschluss)** | ✅ Erfüllt | [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md), [`evidence/hand-over.md`](hand-over.md), [`docs/customer-01/acceptance.md`](../docs/customer-01/acceptance.md), [`costs/usage.csv`](../costs/usage.csv), dieses Dokument |
