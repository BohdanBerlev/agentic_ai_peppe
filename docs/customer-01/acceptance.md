# CUST-001 / TASK-001, TASK-002 & CR-01 – Acceptance / Abnahme (Termine 3, 4 & 5)

**Kunde:** Nordwerk Industrie-Service  
**Projekt-ID:** `client-01` (`target_dir: "client-01-website"`)  
**Produkt-Repository:** `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website`  
**LLM-Provider-Genehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../GEMINI_PROVIDER_WAIVER.md)  

---

## 1. Abnahmestand Termin 5 – Kundenänderung `CR-01`, Sicherheitsantwort `SR-01` & Übergabe (Tag `CR-01-v1.0` / `v0.3.0`)

- **Eingabe-Commit:** `7805e3b` (`v0.2.0-rc1` + README) / `316b5d4` (`issue_cr01.md` & `test_cr01.py`)
- **Geprüfte Factory-Produkt-Commits:** `5227307` (`index_en.html`, Lauf A) $\rightarrow$ **`263d007`** (`index.html`, Lauf B; gemergt auf `main`, Tag **`CR-01-v1.0`**)
- **Workflow-IDs (`CR-01`):**
  - Lauf A (`index_en.html`): `52b69365-3d49-4bcd-9c4d-f51ab8c136e7` ([`evidence/session-05/52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl`](../../evidence/session-05/52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl))
  - Lauf B (`index.html`): `c0ee2cc3-4031-4ce9-8188-d37da99a1583` ([`evidence/session-05/c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl`](../../evidence/session-05/c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl))
- **Browser-Review (375 px / 1280 px & Tastaturfokus für DE + EN):** [`docs/customer-01/browser_review_t5.md`](browser_review_t5.md)
- **Technischer Freigabestatus (Team 3):** **Technisch freigegeben** (`approved` durch Mehrose Farooq, David Pisarkiewicz & Lars Boos am `2026-11-08` / `2026-11-09`)
- **Kundenabnahme-Status (Dozent / Kunde):** **Ausstehend** (Abnahme durch Dozenten in Termin 5; keine Selbstbehauptung *„vom Kunden akzeptiert“*)

| AC | Anforderung / Prüfkriterium | Technisches Prüfergebnis (Termin 5) | Run / Commit / Artefakt | Technische Freigabe vs. Kundenstatus |
|---|---|---|---|---|
| **AC-01** | Firmenname (`N-01`: „Nordwerk Industrie-Service“) und Hauptaussage (`N-02`) auf Startansicht auffindbar | `Passed` (`test_website.py` & `test_cr01.py` Familie `F1`: 0 Regressionen) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Team 3) · Kundenabnahme: **Ausstehend** |
| **AC-02** | Alle drei Leistungen erkennbar: `N-03` (Wartungsplanung), `N-04` (Ersatzteilkoordination), `N-05` (Betriebsdokumentation) | `Passed` (`test_website.py` & `test_cr01.py` Familie `F1`) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Team 3) · Kundenabnahme: **Ausstehend** |
| **AC-03** | Zielgruppen (`N-06`) und Arbeitsweise (`N-07`) enthalten; keine erfundenen Leistungsversprechen | `Passed` (`test_website.py` Familie `F1`: 0 verbotene Zusagen) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Team 3) · Kundenabnahme: **Ausstehend** |
| **AC-04** | Kontaktlink (`Anfrage stellen`, `N-08`) öffnet `mailto:kontakt@nordwerk.example`; Übungshinweis (`N-09`) sichtbar | `Passed` (`test_website.py` Familien `F1` & `F2`) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Team 3) · Kundenabnahme: **Ausstehend** |
| **AC-05** | Navigation führt zu Leistungen, Zielgruppen, Arbeitsweise und Kontakt; lokale Verweise und Assets funktionieren | `Passed` (`test_website.py` Familien `F2` & `F3`) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Team 3) · Kundenabnahme: **Ausstehend** |
| **AC-06** | Bei `375 px` und `1280 px` Breite kein horizontaler Inhaltsüberlauf (`scrollWidth <= clientWidth`) in DE & EN | `Passed` ([`browser_review_t5.md`](browser_review_t5.md) für `index.html` & `index_en.html`) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Lars Boos / David Pisarkiewicz) · Kundenabnahme: **Ausstehend** |
| **AC-07** | Dokumenttitel, `lang="de"` / `lang="en"`, sinnvolle Überschriften (`h1 -> h2 -> h3`), erkennbare Tastaturfokusse (`:focus-visible`) | `Passed` (`test_website.py` `F4`, `test_cr01.py` + [`browser_review_t5.md`](browser_review_t5.md)) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (Lars Boos / David Pisarkiewicz) · Kundenabnahme: **Ausstehend** |
| **AC-08** | Frischer Produkt-Checkout startet ohne Factory/LLM/DB; Produkttests (`test_website.py`, `test_cr01.py`) laufen separat | `Passed` ([`docs/DEPLOYMENT.md`](../DEPLOYMENT.md)) | Commit `263d007` (`CR-01-v1.0`) | Technisch freigegeben (David Pisarkiewicz) · Kundenabnahme: **Ausstehend** |
| **AC-09** | **`CR-01` (Termin 5):** Englische Einstiegsseite (`index_en.html`, `lang="en"`) mit allen Pflichtinhalten (*Nordwerk Industrie-Service*, *Practical support for your technical operations.*, *Maintenance planning*, *Spare parts coordination*, *Operational documentation*, *Technical purchasing departments*, *Request information* $\rightarrow$ `mailto:kontakt@nordwerk.example`, englischer Kurshinweis); DE-Ansicht mit *„Technische Einkaufsabteilungen“*; beidseitiger Sprachwechsel erreichbar | `Passed` (`python test_cr01.py` Exit-Code 0 + Browser-Review in [`browser_review_t5.md`](browser_review_t5.md)) | Commits `5227307` & `263d007`, Workflows `52b69365` & `c0ee2cc3` | Technisch freigegeben (Mehrose Farooq) · Kundenabnahme: **Ausstehend** |
| **AC-10** | **`SR-01` & Übergabe (Termin 5):** Abgegrenzte Kundenantwort zu `CVE-2026-109618` / `CVE-2026-109619` (ENISA-Quelle `21.10.2026`, ungeklärtes PHP-8.2-Altsystem vs. statischer Ersatz, keine „statisch = sicher“-Garantie, Funktionsverlust CMS/Formular, Hoster-Rückfragen, Komponentenübersicht, Wartungsverantwortung) | `Passed` ([`evidence/SR-01-response.md`](../../evidence/SR-01-response.md), [`docs/SECURITY_SR-01.md`](../SECURITY_SR-01.md), [`evidence/hand-over.md`](../../evidence/hand-over.md)) | Menschliche Faktenprüfung: David Pisarkiewicz & Lars Boos (`2026-11-09`) | Technisch freigegeben (David Pisarkiewicz / Lars Boos) · Kundenabnahme: **Ausstehend** |

---

## 2. Abnahmestand Termin 4 – Vollständiger Release Candidate (`TASK-002`, Tag `v0.2.0-rc1` / `R-BASE`)

- **Eingabe-Commit:** `3e6121b` (`v0.1.0-t3`) / `fef6a55` (mit `issue_t4.md` & 4-Familien-`test_website.py`)
- **Geprüfter Release-Candidate-Commit:** **`18d222b`** (Tags: **`v0.2.0-rc1`**, **`R-BASE`**)
- **Workflow-ID:** `cb3bcea8-4a03-4cc9-82cc-759136472b92` ([`evidence/session-04/cb3bcea8-4a03-4cc9-82cc-759136472b92.jsonl`](../../evidence/session-04/cb3bcea8-4a03-4cc9-82cc-759136472b92.jsonl))
- **Browser-Review (375 px / 1280 px & Tastaturfokus):** [`docs/customer-01/browser_review_t4.md`](browser_review_t4.md)
- **Datum der Abnahme:** 02. November 2026

| AC | Test / Artifact | Actual Result / Ergebnis (Termin 4) | Run / Source Commit | Reviewer / Decision |
|---|---|---|---|---|
| **AC-01** | Firmenname (`N-01`: „Nordwerk Industrie-Service“) und Hauptaussage (`N-02`: „Praktische Unterstützung für Ihren technischen Betrieb.“) auf Startansicht auffindbar | `Passed` (`test_website.py` Prüffamilie `F1 Pflichtinhalt` + Sichtprüfung im Browser) | Produkt-Commit `18d222b` (`v0.2.0-rc1`), Workflow `cb3bcea8-4a03-4cc9-82cc-759136472b92` | David Pisarkiewicz / Lars Boos: **Approved** |
| **AC-02** | Alle drei Leistungen erkennbar: `N-03` (Wartungsplanung), `N-04` (Ersatzteilkoordination), `N-05` (Betriebsdokumentation) | `Passed` (`test_website.py` Prüffamilie `F1 Pflichtinhalt`; durch `backend_agent` Run `cf08875b-7b67-41b2-9796-84f118d20108` als 3 `<article class="service-card">` generiert) | Produkt-Commit `18d222b` (`v0.2.0-rc1`), Workflow `cb3bcea8-4a03-4cc9-82cc-759136472b92` | David Pisarkiewicz / Mehrose Farooq: **Approved** |
| **AC-03** | Beide Zielgruppen (`N-06`: „Kleine Produktionsbetriebe“, „Technische Serviceunternehmen“) und Arbeitsweise (`N-07`) enthalten; keine erfundenen Leistungsversprechen | `Passed` (`test_website.py` Prüffamilie `F1 Pflichtinhalt`: alle Pflichttexte exakt vorhanden, 0 verbotene Werbeaussagen/Zertifikate) | Produkt-Commit `18d222b` (`v0.2.0-rc1`), Workflow `cb3bcea8-4a03-4cc9-82cc-759136472b92` | Mehrose Farooq / Lars Boos: **Approved** |
| **AC-04** | Klar benannter Kontaktlink (`Anfrage stellen`, `N-08`) öffnet `mailto:kontakt@nordwerk.example`; Übungshinweis (`N-09`) im Footer sichtbar | `Passed` (`test_website.py` Prüffamilien `F1` & `F2` + Klicktest im Browser) | Produkt-Commit `18d222b` (`v0.2.0-rc1`), Workflow `cb3bcea8-4a03-4cc9-82cc-759136472b92` | David Pisarkiewicz / Mehrose Farooq: **Approved** |
| **AC-05** | Navigation führt zu Leistungen (`#leistungen`), Zielgruppen (`#zielgruppen`), Arbeitsweise (`#arbeitsweise`) und Kontakt (`#kontakt`); interne `#`-Links und lokale Assets (`styles.css`) funktionieren | `Passed` (`test_website.py` Prüffamilien `F2 Kontakt & Navigation` & `F3 Lokale Verweise & Assets` + Klicktest im Browser) | Produkt-Commit `18d222b` (`v0.2.0-rc1`) | Lars Boos: **Approved** |
| **AC-06** | Bei `375 px` und `1280 px` Breite kein horizontaler Inhaltsüberlauf (`scrollWidth <= clientWidth`); Text und Kontakt nutzbar | `Passed` (Manuelles Browser-Review in [`browser_review_t4.md`](browser_review_t4.md) bei 375 px und 1280 px bestanden) | Produkt-Commit `18d222b` (`v0.2.0-rc1`) | David Pisarkiewicz / Lars Boos: **Approved** |
| **AC-07** | Dokumenttitel, `lang="de"`, sinnvolle Überschriften (`h1 -> h2 -> h3`), erkennbare Tastaturfokusse (`:focus-visible`), Bildalternativen | `Passed` (`test_website.py` Prüffamilie `F4 Bedienbarkeit statisch` + `Tab`-Fokus-Prüfung in [`browser_review_t4.md`](browser_review_t4.md)) | Produkt-Commit `18d222b` (`v0.2.0-rc1`) | David Pisarkiewicz / Lars Boos: **Approved** |
| **AC-08** | Frischer Produkt-Checkout startet mit dokumentiertem Befehl ohne Factory/LLM/DB; Produkttests laufen separat | `Passed` (`python -m http.server 8000` und `python test_website.py` laufen vollständig eigenständig) | Produkt-Commit `18d222b` (`v0.2.0-rc1`) | David Pisarkiewicz: **Approved** |

---

## 3. Historischer Abnahmestand Termin 3 (`TASK-001`, Tag `v0.1.0-t3`)

- **Produkt-Repository:** `client-01-website` (Eingabe-Commit: `cbbf7a9` -> Geprüfter Release-Commit: `3e6121b`, Tag `v0.1.0-t3`)  
- **Workflow-ID:** `bf81352d-f7cb-4628-ad10-475cad888f73` ([`evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`](../../evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl))  
- **Verifizierte SHA-256 Hashes (Stand `v0.1.0-t3`):**
  - `client-01-website/index.html`: `b3cf793ce3a1ee7b3eda042f4a9a17e5abde88c1abb7336d962f8e3fb3bfb7cf`
  - `client-01-website/styles.css`: `d7ac76b8b3015f6fb9e9bcd648d71bc54ce8cea023935672f8f0005612e85a40`
  - `client-01-website/test_website.py`: `41a920b54603ae70f1eefc47d58ff9018315216b3af05313db73280461b910cb`
  - Nachrechnen im Produkt-Repo: `git show v0.1.0-t3:index.html | shasum -a 256` (Werte aus dem Git-Objekt, LF-Zeilenenden; ein Windows-Checkout mit CRLF ergibt andere Werte)
