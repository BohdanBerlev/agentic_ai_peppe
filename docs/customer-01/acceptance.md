# CUST-001 – Acceptance / Abnahme

**Kunde:** Nordwerk Industrie-Service  
**Task-ID:** CUST-001  
**Geprüfter Release-Stand:** Release Candidate 01 (Termin 3)  
**Produkt-Repository:** `client-01-website` (Commit: `2f5e4a5`)  

**Factory-Repository:** `agentic_ai_peppe`  
**Datum der Abnahme:** 24. Oktober 2026

| AC | Test / artifact | Actual result / Ergebnis | Run / source commit | Reviewer / decision |
|---|---|---|---|---|
| **AC-01** | Firmenname (N-01: „Nordwerk Industrie-Service“) und Hauptaussage (N-02: „Praktische Unterstützung für Ihren technischen Betrieb.“) auf Startseite sichtbar | Passed (`test_website.py`: Checks 1 & 2 bestanden; im Browser unter `http://localhost:8000` visuell verifiziert) | Commit `2f5e4a5`, Run `website-run-001` | Lars Boos / Mehrose Farooq: **Approved** |
| **AC-02 (T3-Teil)** | Erste Leistung vorhanden (N-03 Wartungsplanung: „Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.“) | Passed (`test_website.py`: Check 3 bestanden; Überschrift und Fließtext vorhanden) | Commit `2f5e4a5`, Run `website-run-001` | Lars Boos: **Approved** |
| **AC-04** | Kontaktlink öffnet `mailto:kontakt@nordwerk.example` mit Buttontext „Anfrage stellen“; Übungshinweis (N-09: „Fiktives Unternehmen – Lehrprojekt der HAW Hamburg...“) sichtbar | Passed (`test_website.py`: Checks 4, 5 & 6 bestanden; Linkziel und Hinweistext exakt) | Commit `2f5e4a5`, Run `website-run-001` | Lars Boos / Mehrose Farooq: **Approved** |

| **AC-02 (Rest)** | Ersatzteilkoordination (N-04) und Betriebsdokumentation (N-05) | Geplant für Termin 4 (laut Aufgabenblatt in T3 noch nicht fällig) | Backlog T4 | Offen für T4 |
| **AC-03** | Zielgruppen und Arbeitsweise vollständig integriert | Geplant für Termin 4 | Backlog T4 | Offen für T4 |
| **AC-05** | Navigation mit Sprungmarken zu allen Leistungen | Geplant für Termin 4 | Backlog T4 | Offen für T4 |
| **AC-06** | Responsive Prüfung bei 375px und 1280px ohne horizontalen Überlauf | Vorab im CSS angelegt (`@media (max-width: 600px)`), formale Abnahme in T4 | Backlog T4 | Offen für T4 |
| **AC-07** | Barrierefreiheit, Tastaturfokusse, Alt-Attribute | Geprüft (valides HTML5, `lang="de"`, sichtbare Fokus-Outlines) | Commit `2f5e4a5` | Vorläufig erfüllt, formal fällig in T4 |
| **AC-08** | Autonomer Start und isolierte Produkttests ohne Factory | Passed (`python -m http.server 8000` und `python test_website.py` laufen isoliert) | Commit `2f5e4a5` | Lars Boos: **Approved** |

## Reviewed requirements / Geprüfte Anforderungen

- **Freigegebene Fassung:** `client-01-website/index.html` (Commit `2f5e4a5`)

- **Prüfcode:** `client-01-website/test_website.py`
- **Menschliche Sichtprüfung:** Durchgeführt von Lars Boos und Mehrose Farooq am lokalen Webserver `http://localhost:8000`.
- **Verworfene Modellvorschläge:** Ein initialer Entwurf des Agenten enthielt ein JavaScript-Kontaktformular mit externem CDN-Script; dies wurde durch den Architektur- und Sicherheitsagenten abgewiesen und durch einen reinen `mailto:`-Link ohne externe Abhängigkeiten ersetzt.

## Open acceptance items / Offene Abnahmepunkte

- **AC-02 (vollständig):** Integration der beiden weiteren Leistungsbausteine N-04 (Ersatzteilkoordination) und N-05 (Betriebsdokumentation) in Termin 4.
- **AC-03:** Vollständige Zielgruppenansprache und Arbeitsweise in Termin 4.
- **AC-06:** Umfassender responsiver Testnachweis auf mehreren realen Viewports in Termin 4.
