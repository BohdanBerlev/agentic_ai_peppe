# Internal Dry Run 01: Work-Item API (Session 2)

**Datum:** 19. Oktober 2026  
**Task-ID:** DRYRUN-002  
**Ziel:** Implementierung und Überprüfung einer persistenten CRUD-API für Work-Items (FastAPI + PostgreSQL).

## 1. Umsetzung & Agenten-Orchestrierung
Die Backend-Endpunkte (POST, GET, PATCH, DELETE) wurden implementiert und durch die autonome **Agentic Feature Pipeline** validiert. Die Pipeline orchestriert die Agenten `requirements_agent`, `architect_agent` und `qa_security_agent`, gefolgt von einem interaktiven Human Gate.

## 2. Iterationen & Human Gate Entscheidungen

**Durchlauf 1 (Trace: `a4c5e5d8-6163-4b0f-a5e1-dcbaaefc0821`)**
* **Findings:** Die Agenten detektierten fehlendes Connection-Pooling (Gefahr von Resource Exhaustion), ungeschützte Exceptions (Information Disclosure) und fehlende Pydantic-Längenvalidierung (`architect_agent`: `changes_requested`, `qa_security_agent`: `changes_requested`).
* **Entscheidung (Human Gate):** Fachlich *Changes Requested* mit der Notiz *"Bitte die Vorschläge umsetzen."*, woraufhin der Code für Durchlauf 2 überarbeitet wurde.
* **Transparenz-Hinweis / Erratum zum Trace `a4c5e5d8-6163-4b0f-a5e1-dcbaaefc0821`:** Im Roh-Trace der Orchestrator-Zeile steht im Feld `human_approval.decision` fälschlicherweise `"approved"`, obwohl die menschliche Freigabe-Notiz (`"Bitte die Vorschläge umsetzen."`) sowie die Sub-Agenten-Reports (`changes_requested`) klar eine Nachbesserung forderten und im Anschluss auch Durchlauf 2 durchgeführt wurde. Ursache war eine Fehleingabe (`a` statt `c`) im interaktiven Terminal-Prompt ohne Rückfrage/Konsistenzprüfung. Um die Integrität der historischen Evidenz zu wahren, wurde die JSONL-Datei nicht nachträglich editiert; stattdessen wurde das Human Gate in `src/workflows/feature_pipeline.py` für Session 3 gehärtet (striktes Eingabeschema, explizite Rückfrage bei Abweichung von Agenten-Findings und kein Auto-Approve im Headless-Modus).

**Durchlauf 2 (Trace: `ec9367ce-8be8-46e3-ab56-8d8132e8ff71`)**
* **Findings:** Nach Behebung der kritischen Fehler (Einführung von `psycopg_pool`, Fehler-Masking, `max_length`) forderten Architect und QA Agent tiefgreifende Strukturänderungen (Separation of Concerns in Repository-Layer, Pagination für GET-Requests).
* **Entscheidung (Human Gate):** *Approved (Accepted Risk).* Die Architektur- und QA-Findings sind valide, überschreiten jedoch den Scope des Session 2 MVPs. Basis-Anforderungen (CRUD, grundlegendes Pooling, Error-Masking) sind vollständig erfüllt. Offene Punkte werden als Technical Debt ins Backlog übernommen. 

## 3. Kosten des Workflows & Observability-Fix
Die initial ausgewiesenen Gesamtkosten von 37.57 Credits (Trace: 6ccda690-8a96-471a-8673-340dd4a81029) wiesen einen Observability-Bug (Double-Counting) auf. Der Cost Agent summierte fälschlicherweise die Traces der Sub-Agenten *und* den zusammenfassenden Trace des Orchestrators. Zudem inkludierte die Pipeline-Laufzeit die menschliche Wartezeit am Human Gate (ca. 24 Minuten im zweiten Lauf).

**Bereinigte, reale Metriken (ohne Orchestrator-Overhead):**
* **Analysierte LLM-Calls:** 7 Aufrufe (Sub-Agenten + Cost Agent)
* **Reine Agenten-Laufzeit:** 919.5 Sekunden (~15 Minuten)
* **Reale Gesamtkosten:** 16.5785 Credits
* **Maßnahme fürs Backlog:** Anpassung der `cost_agent.py`, um Orchestrator-Zeilen (`feature_pipeline_workflow`) zukünftig aus der Token-Summierung auszuschließen.

## 4. Fazit
Die Multi-Agenten-Architektur funktioniert zuverlässig und deckt reale Schwachstellen auf. Das Human Gate hat sich als essenzielle Kontrollinstanz erwiesen, um die Balance zwischen theoretischer Code-Perfektion (LLM-Pedanterie) und pragmatischer MVP-Lieferung zu wahren.