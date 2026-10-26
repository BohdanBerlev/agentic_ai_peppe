# CUST-001 – Delivery / Lieferbericht (Termin 3)

**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Auftrag:** Kundenprojekt 01 – Initialer Webauftritt Release Candidate  
**Lieferdatum:** 24. Oktober 2026  
**Erstellt durch:** PepeGroup (Team 3)

---

### 1. Kundennutzen & Scope
Nordwerk Industrie-Service erhält einen schnellen, modernen und barrierefreien Webauftritt (Release Candidate), der potenziellen B2B-Kunden sofort Identität, Hauptaussage und die Kernleistung der Wartungsplanung vermittelt. Über einen standardisierten `mailto:`-Link können Interessenten direkt unverbindliche Anfragen stellen, ohne dass ein komplexes oder wartungsintensives CMS/PHP-System erforderlich ist.

### 2. Commit-Stände & Nachvollziehbarkeit
- **Geprüfter Produkt-Code-Commit:** `7b1206f` (Repository: `client-01-website`)
- **Factory-Commit vor Lauf:** `f3b346f` (Repository: `agentic_ai_peppe`)
- **Liefer-/Evidenz-Commit:** nachgelagert zur Vermeidung zirkulärer Verweise.
- **Workflow & Run-ID:** Task `CUST-001`, Run `website-run-001` (Trace: `evidence/session-03/runs/website-run-001.jsonl`).

### 3. Startbefehle & Ausführung
Das Kundenprodukt benötigt weder Factory-Prozesse noch Datenbanken:
```bash
# Lokaler Start im Produktverzeichnis:
cd client-01-website
python -m http.server 8000
# URL im Browser: http://localhost:8000
```

### 4. Tests & Prüfungsergebnisse
- **Eigener automatisierter Produktcheck (`test_website.py`):**
  - Befehl: `python test_website.py`
  - Ergebnis: **8 von 8 Checks bestanden (0 Fehler)**.
  - Geprüft: Firmenname (N-01), Hauptaussage (N-02), Wartungsplanung (N-03), Kontaktlink `mailto:kontakt@nordwerk.example` (N-08), Übungshinweis Lehrprojekt HAW Hamburg (N-09), UTF-8 / `lang="de"`, keine Tracker/Script-Injections.
- **Factory-Tests (Pytest):**
  - Befehl: `python -m pytest`
  - Ergebnis: Alle eigenen Factory-Tests und Regressionstests (inkl. `test_session_03_infrastructure.py` und `test_work_items_real_postgres_lifecycle`) erfolgreich ausgeführt.

### 5. Ablaufkette (Traceability)
1. **Kunden-Issue:** `TASK-001` (definiert in `client-01-website/issue_t3.md`)
2. **Requirements Agent:** Extrahiert N-01 bis N-09 und strukturiert Akzeptanzkriterien (`RequirementsReport`).
3. **Software Architect Agent:** Prüft Barrierefreiheit, HTML5-Struktur und lokale Asset-Bindung (`ArchitectureReport`).
4. **Backend Implementation Agent:** Generiert/aktualisiert `client-01-website/index.html` und bindet Stylesheets ein.
5. **QA & Test Agent:** Führt den automatisierten Produktcheck aus und validiert Exit-Code 0.
6. **AI Safety & Security Agent:** Verifiziert, dass keine Path Traversals, externen Tracker oder CDN-Skripte eingeschleust wurden.
7. **Human Approval Gate:** Menschliche Sichtprüfung im Browser (`http://localhost:8000`) und Klickprüfung des Kontaktlinks.

### 6. Menschliche vs. Agenten-Arbeit
- **Agenten:** Erstellung der Anforderungsanalyse, Architekturprüfung, HTML-Strukturierung, Sicherheitsaudit und Testauswertung.
- **Menschen:**
  - *Lieferung/Setup:* Maxim Bers & David Pisarkiewicz (Repo-Trennung, Server-Dokumentation, Pipeline-Konfiguration).
  - *Review & Abnahme:* Lars Boos & Mehrose Farooq (Sichtprüfung im Browser, Klicktest des Mailto-Links, finale Freigabeentscheidung am Human Gate).

### 7. Freigabeentscheidung (Human Gate)
- **Reviewer:** Lars Boos & Mehrose Farooq
- **Entscheidung:** **Approved** (alle Pflichtkriterien AC-01, AC-02 Teil, AC-04 erfüllt)
- **Datum/Zeit:** 2026-10-24 16:30 UTC
- **Notiz:** „Release Candidate erfüllt die Kriterien für T3 vollständig. Layout ist sauber, Kontaktlink öffnet E-Mail-Client wie gefordert.“

### 8. Kosten & Aufwand
- **Planbudget T3/T4:** 1.200 Credits (Lieferung) + 400 Credits (T5 Reserve).
- **Menschlicher Gesamtaufwand T3:**
  - Implementierung/Setup: 2,5 h (250 Credits)
  - Review: 1,5 h (150 Credits)
  - Meeting/Planung: 0,5 h (50 Credits)
- **Agenten-Kosten T3:** ~2,85 Credits (2 reale LLM-Aufrufe, 1 Pipeline-Lauf ohne Double-Counting).
- **Setup-Kosten:** Getrennt erfasst.

### 9. Engpass & Verbesserungshypothese für T4
- **Beobachteter Engpass:** Die manuelle Übertragung von Attributen im Agenten-Prompt führte beim ersten Entwurf zu ungeschützten Sonderzeichen im Mailto-Betreff.
- **Hypothese für T4:** Durch Bereitstellung einer Pydantic-Komponentenvalidierung für HTML-Komponenten vor dem Schreib-Tool lässt sich die Korrekturzeit um 100 % eliminieren und die Tokenanzahl um ca. 20 % senken.

### 10. Vereinbarter Scope & nächste Schritte
- Keine offenen Defekte für den T3-Scope.
- **Nächste Schritte für T4:**
  1. Hinzufügen der beiden weiteren Leistungsbausteine N-04 (Ersatzteilkoordination) und N-05 (Betriebsdokumentation).
  2. Zielgruppenansprache N-06 und Arbeitsweise N-07 integrieren.
  3. Vollständige responsive Prüfung bei 375 px und 1280 px.
