# CUST-001 / TASK-001 & TASK-002 – Acceptance / Abnahme (Termine 3 & 4)

**Kunde:** Nordwerk Industrie-Service  
**Projekt-ID:** `client-01` (`target_dir: "client-01-website"`)  
**Produkt-Repository:** `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website`  
**LLM-Provider-Genehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../GEMINI_PROVIDER_WAIVER.md)  

---

## 1. Abnahmestand Termin 4 – Vollständiger Release Candidate (`TASK-002`, Tag `v0.2.0-rc1` / `R-BASE`)

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

## 2. Historischer Abnahmestand Termin 3 (`TASK-001`, Tag `v0.1.0-t3`)

- **Produkt-Repository:** `client-01-website` (Eingabe-Commit: `cbbf7a9` -> Geprüfter Release-Commit: `3e6121b`, Tag `v0.1.0-t3`)  
- **Workflow-ID:** `bf81352d-f7cb-4628-ad10-475cad888f73` ([`evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`](../../evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl))  
- **Verifizierte SHA-256 Hashes (Stand `v0.1.0-t3`):**
  - `client-01-website/index.html`: `b3cf793ce3a1ee7b3eda042f4a9a17e5abde88c1abb7336d962f8e3fb3bfb7cf`
  - `client-01-website/styles.css`: `d7ac76b8b3015f6fb9e9bcd648d71bc54ce8cea023935672f8f0005612e85a40`
  - `client-01-website/test_website.py`: `41a920b54603ae70f1eefc47d58ff9018315216b3af05313db73280461b910cb`
  - Nachrechnen im Produkt-Repo: `git show v0.1.0-t3:index.html | shasum -a 256` (Werte aus dem Git-Objekt, LF-Zeilenenden; ein Windows-Checkout mit CRLF ergibt andere Werte)
