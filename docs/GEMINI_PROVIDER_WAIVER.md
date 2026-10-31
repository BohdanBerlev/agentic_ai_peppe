# Antrag und Dokumentation zur Ausnahmegenehmigung: Nutzung der Google Gemini API

**Projekt:** Agentic AI Software Factory (HAW Hamburg, WS 2026/2027)  
**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Kunde:** Nordwerk Industrie-Service (Kundenprojekt 01)  
**Datum:** 31. Oktober 2026  
**Status:** Dokumentarische Ausnahmegenehmigung beantragt & implementiert  

---

## 1. Gegenstand des Antrags

Das Team 3 (PepeGroup) beantragt hiermit die offizielle Genehmigung zum Einsatz der **Google Gemini API** (`gemini-3.8-flash` bzw. `gemini-2.5-flash`) als primäres Flaggschiff-Modell für die agentische Software Factory im Rahmen von Termin 3, Termin 4 und Termin 5.

---

## 2. Fachliche Begründung & Notwendigkeit

1. **Komplexität der 8-Rollen-Unternehmensarchitektur:**  
   Die Factory bildet eine vollwertige Agenten-Organisation ab:
   - `product_owner_requirements` (strukturierte Akzeptanzkriterien)
   - `project_manager` (Work Packages mit Abhängigkeiten)
   - `agent_engineer` (LangGraph-Knotenspezifikation und Tool-Verträge)
   - `software_architect` (Code- und Layout-Architekturprüfung)
   - `backend_api_engineer` (vollständige HTML/CSS-Codegenerierung & TDD-Loop)
   - `qa_test_engineer` (Ausführung und Analyse realer Testsuiten)
   - `ai_safety_security_engineer` (Guardrail-Prüfung, Path-Traversal- & CVE-Audits)
   - `integration_engineer` (Handover-Validierung zwischen allen Phasen)

   Lokale Edge-Modelle (wie `qwen3:4b` oder `llama3.2:3b` auf Studierenden-Notebooks) weisen bei dieser Tiefe von Pydantic-Schemas und sequentiellen Handovers eine hohe Fehlerquote bei JSON-Formatierungen auf (`unparseable`), was zu künstlichen Eskalationen führt. `gemini-3.8-flash` liefert verlässliche, fehlerfreie Strukturtreue und hohe semantische Qualität.

2. **Latenz und Zuverlässigkeit:**  
   Die Ausführung des vollständigen 8-Rollen-Graphs erfordert sequentiell bis zu 8 reale Modellaufrufe. Lokale CPU/GPU-Inferenz auf Entwickler-Laptops führte in Session 2 zu Laufzeiten von über 45 Minuten pro Durchlauf mit thermischem Drosseln. Die Gemini-API ermöglicht stabile Durchläufe bei gleichzeitiger Trace-Aufzeichnung aller Zwischenschritte.

3. **Interoperabilität der Provider-Abstraktion bleibt gewahrt:**  
   Die Factory-Architektur in [`src/llm/factory.py`](../src/llm/factory.py) ist nicht proprietär an Google gebunden. Über die zentrale Factory-Funktion `get_chat_model()` unterstützt die Plattform unverändert:
   - `ollama` (für autarken Offline-Betrieb)
   - `openai_compatible` (für den HAW ICC-Endpunkt gemäß [`docs/ICC_CONFIGURATION.md`](ICC_CONFIGURATION.md))
   - `google` (für Gemini 3.8 Flash / 2.5 Flash)
   Ein Wechsel auf ICC oder lokales Ollama kann jederzeit durch bloßes Setzen der Umgebungsvariable `LLM_PROVIDER=openai_compatible` ohne Quellcode-Änderung erfolgen.

---

## 3. Kosten-, Token- und Governance-Modell

Die Nutzung von Gemini erfolgt unter strikter Einhaltung des Kurs-Kostenmodells ([`costs/cost-model.yaml`](../costs/cost-model.yaml)):

| Kostenart | Modellannahme / Kursmodell | Erfassung in der Factory |
|---|---|---|
| **Aufrufpauschale** | 1,00 Credit pro Aufruf | Exakt erfasst in jedem Run-Trace (`calls`) |
| **Laufzeit** | 0,01 Credits pro Sekunde Inferenz | Über `duration_seconds` im Trace erfasst |
| **Input-Tokens** | 0,02 Credits pro 1.000 Tokens | Über LangChain Token-Usage exakt gezählt |
| **Output-Tokens** | 0,04 Credits pro 1.000 Tokens | Über LangChain Token-Usage exakt gezählt |

* **Keine fiktiven Nullwerte:** Tokens und Inferenzzeiten werden aus den HTTP-Metadaten ausgelesen und in [`costs/usage.csv`](../costs/usage.csv) verbucht.
* **Separation von Human- und Agentenkosten:** Menschliche Wartezeiten und interaktive Gate-Reviews werden explizit von den Agentenkosten getrennt ausgewiesen (kein Double-Counting).

---

## 4. Datenschutz, Secrets & Sicherheits-Compliance

* **Secrets Management:** Der API-Schlüssel (`GOOGLE_API_KEY` / `GEMINI_API_KEY`) wird ausschließlich über lokale `.env`-Dateien injiziert. Die `.env`-Datei ist in [`.gitignore`](../.gitignore) verankert und befindet sich zu keinem Zeitpunkt im Git-Verlauf.
* **Keine Übertragung personenbezogener Daten:** Im Kundenprojekt 01 werden ausschließlich synthetische Daten des fiktiven Lehrprojekts *Nordwerk Industrie-Service* verarbeitet. Es werden keine realen Kundendaten, IP-Adressen oder vertraulichen Hochschuldaten an externe Endpunkte übermittelt.
* **Tool-Sicherheit:** Alle Agenten-Dateizugriffe sind durch gehärtete Sicherheits-Helper (`write_target_text_file` / Path-Traversal-Schutz / `.git`-Sperre) isoliert.

---

## 5. Antrag auf Freigabe

Wir bitten die Kursleitung um förmliche Bestätigung der Ausnahmegenehmigung zur Nutzung der Google Gemini API im Rahmen der Evaluationen der Termine 3 bis 5.
