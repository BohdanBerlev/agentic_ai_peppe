# CUST-001 / TASK-001 – Acceptance / Abnahme

**Kunde:** Nordwerk Industrie-Service  
**Task-ID:** `TASK-001` (`project_id: "client-01"`)  
**Geprüfter Release-Stand:** Release Candidate 01 (Termin 3) – Tag `v0.1.0-t3`  
**Produkt-Repository:** `client-01-website` (Eingabe-Commit: `cbbf7a9` -> Geprüfter Release-Commit: `3e6121b`, Tag `v0.1.0-t3`)  
**Factory-Repository:** `agentic_ai_peppe` (Commit beim Lauf: `7351867`, Abgabe-Stand auf `main`)  
**Workflow-ID:** `bf81352d-f7cb-4628-ad10-475cad888f73` ([`evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl`](../../evidence/session-03/bf81352d-f7cb-4628-ad10-475cad888f73.jsonl))  
**Datum der Abnahme:** 26. Oktober 2026 (Aktualisiert mit validierten Prüfsummen am 31. Oktober 2026)  
**LLM-Provider-Genehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../GEMINI_PROVIDER_WAIVER.md)  

| AC | Test / artifact | Actual result / Ergebnis | Run / source commit | Reviewer / decision |
|---|---|---|---|---|
| **AC-01** | Firmenname (`N-01`: „Nordwerk Industrie-Service“) und Hauptaussage (`N-02`: „Praktische Unterstützung für Ihren technischen Betrieb.“) auf Startseite sichtbar | `Passed` (`test_website.py` Exit-Code 0; im Browser unter `http://localhost:8000` visuell verifiziert) | Produkt-Commit `3e6121b` (`v0.1.0-t3`), Workflow `bf81352d-f7cb-4628-ad10-475cad888f73` | David Pisarkiewicz / Lars Boos: **Approved** |
| **AC-02 (T3-Teil)** | Erste Leistung vorhanden (`N-03` Wartungsplanung: „Wartungsplanung: Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.“) | `Passed` (`test_website.py` Exit-Code 0; durch `backend_agent` Run `4e03fcfb-0d12-4a71-bd67-13e3e20a622a` in `index.html` generiert) | Produkt-Commit `3e6121b` (`v0.1.0-t3`), Workflow `bf81352d-f7cb-4628-ad10-475cad888f73` | David Pisarkiewicz / Lars Boos: **Approved** |
| **AC-04** | Kontaktlink öffnet `mailto:kontakt@nordwerk.example` mit Buttontext `Anfrage stellen` (`N-08`); Übungshinweis (`N-09`: „Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.“) im Footer sichtbar | `Passed` (`test_website.py` Exit-Code 0; Klicktest im Browser erfolgreich) | Produkt-Commit `3e6121b` (`v0.1.0-t3`), Workflow `bf81352d-f7cb-4628-ad10-475cad888f73` | David Pisarkiewicz / Mehrose Farooq: **Approved** |
| **AC-02 (Rest)** | Ersatzteilkoordination (`N-04`) und Betriebsdokumentation (`N-05`) | Geplant für Termin 4 (laut Aufgabenblatt in T3 noch nicht fällig) | Backlog T4 | Offen für T4 |
| **AC-03** | Zielgruppen (`N-06`) und Arbeitsweise (`N-07`) vollständig integriert | Geplant für Termin 4 | Backlog T4 | Offen für T4 |
| **AC-05** | Navigation mit Sprungmarken zu allen Leistungen | Sprungmarken `#leistungen` und `#kontakt` inkl. `:target`-Hervorhebung in RC1 aktiv; Vollausbau für alle Leistungen in T4 | Produkt-Commit `3e6121b` (`v0.1.0-t3`) | Vorläufig erfüllt, Vollausbau T4 |
| **AC-06** | Responsive Prüfung bei 375 px und 1280 px ohne horizontalen Überlauf | Im CSS (`@media (max-width: 600px)`, `overflow-x: hidden`) umgesetzt; formale Mehr-Viewport-Matrix in T4 | Produkt-Commit `3e6121b` (`v0.1.0-t3`) | Vorläufig erfüllt, formal fällig in T4 |
| **AC-07** | Barrierefreiheit, Tastaturfokusse, Alt-Attribute | Geprüft (valides semantisches HTML5, `lang="de"`, sichtbare `:focus-visible`-Outlines) | Produkt-Commit `3e6121b` (`v0.1.0-t3`) | Vorläufig erfüllt, formal fällig in T4 |
| **AC-08** | Autonomer Start und isolierte Produkttests ohne Factory | `Passed` (`python -m http.server 8000 --directory client-01-website` und `python client-01-website/test_website.py` laufen isoliert ohne Factory/DB) | Produkt-Commit `3e6121b` (`v0.1.0-t3`) | David Pisarkiewicz: **Approved** |

## Reviewed requirements / Geprüfte Anforderungen & Verifizierte Hashes

- **Freigegebene Fassung:**
  - `client-01-website/index.html` (SHA-256: `f65fe5984f3bc185e0979660334f766b7578fc9ad288b7703fcb3504c1e58202`)
  - `client-01-website/styles.css` (SHA-256: `d7c2e41c5314726d680e28957a4667e0c1a45c9bffb319d329902eaaaa4d1aa0`)
  - `client-01-website/test_website.py` (SHA-256: `41a920b54603ae70f1eefc47d58ff9018315216b3af05313db73280461b910cb`)
- **Prüfcode:** `client-01-website/test_website.py` (automatisch ausgeführt durch `qa_security_agent` Run `aa24b936-9994-40a7-b14e-2f4f8c12a705` mit `exit_code: 0`, 8 Checks passed).
- **Factory-Testsuite:** `evidence/session-03/pytest.xml` (67 passed, 2 skipped: Live-PostgreSQL-Test übersprungen, wenn lokaler DB-Container nicht aktiv).
- **Menschliche Sichtprüfung & Gate-Begründung:** Durchgeführt von David Pisarkiewicz (322,45 s Reviewzeit am interaktiven Human Gate) sowie im Browser unter `http://localhost:8000`. Da der `architect_agent` (`a45845d6...`) in der Pipeline *vor* dem `backend_agent` (`4e03fcfb...`) lief, bewertete der Architect noch das leere Placeholder-Skeleton mit `changes_requested`. Anschließend generierte der `backend_agent` die vollständige semantische `index.html`, woraufhin `qa_test_engineer`, `ai_safety_security_engineer` und `integration_engineer` alle Anforderungen mit `approved` bestätigten.
- **Verworfene Modellvorschläge / Guardrails:** Jegliche externen Skripte, CDNs, absoluten URLs (`http://`/`https://`) oder erfundenen Zertifikate (`ISO 9001`, `TÜV`, `24/7 Notdienst`) sind durch `test_website.py` deterministisch ausgeschlossen.
