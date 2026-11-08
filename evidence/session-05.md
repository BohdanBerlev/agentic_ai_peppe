# Evidence Session 5 – CR-01 Lieferung, SR-01 Sicherheitsantwort, Factory F-NEW & R-01 Vergleich

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-08  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Session:** session-05  
**LLM-Provider-Ausnahmegenehmigung:** [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md)

---

## 0. Feedback-Nacharbeit (Kategorie 1 – Termin 4 Feedback)

### R-01 Reproduzierbarkeit (R-01 Feedback)

**Klärung der Commit-Diskrepanz `F-BASE = 6da5414` vs. Git-Tag `5a146a3` (offen in Issue #70):**

| Eigenschaft | Detail |
|------------|--------|
| **Git-Tag `F-BASE`** | `5a146a3`, 2026-11-02 09:30 (`feat(session-04): finalize T4 release candidate run, ...`) |
| **In `session-04.md` genannter Stand** | `6da5414`, 2026-11-02 00:55 (`docs(session-04): add step-by-step Termin 4 runbook and checklist`) |
| **R-BASE-Lauf `0cef313b`** | gestartet 2026-11-02 09:26, laut `session-04.md` mit `requests_per_second=0.08` |
| **Code-Unterschied `6da5414` → `5a146a3`** | `src/llm/factory.py` (6 Zeilen: u. a. `requests_per_second` `0.25` → `0.08`, `max_retries` `2` → `6`) und `src/agents/backend_agent.py` (3 Zeilen) |

**Ergebnis:** Die beiden Stände unterscheiden sich im Factory-Code. Der R-BASE-Lauf nutzte `0.08`; diesen Wert enthält nur `5a146a3`. Der Vergleich in [`R01-comparison.md`](R01-comparison.md) rechnet deshalb gegen Tag `F-BASE` = `5a146a3`. Welcher Commit genau lief, wird in Issue #70 abschließend geklärt.

```
git diff --stat 6da5414 5a146a3 -- src
# → src/agents/backend_agent.py | 3 ++-
# → src/llm/factory.py          | 6 +++---
```

### Produkt-Release-Evidenz

| Aspekt | Status | Detail |
|--------|--------|--------|
| Produkt-Repo erreichbar | ✅ | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` |
| Freigegebener Commit | ✅ | `18d222b` (Tag: `v0.2.0-rc1`, Branch: `R-BASE`) |
| Agent-Run-Link | ✅ | Workflow `cb3bcea8-4a03-4cc9-82cc-759136472b92` |
| Produkt-Diff | ✅ | `git diff fef6a55..18d222b -- index.html` |
| Testergebnis | ✅ | `python test_website.py` → Exit-Code 0, F1–F4 PASSED |
| Menschliche Freigabe | ✅ | David Pisarkiewicz, `approved`, `quality_gate_blocked: false` |

### Kosten- & Betriebs-Evidenz

| Aspekt | Status | Detail |
|--------|--------|--------|
| GitHub-Actions-Runs | ✅ | Traces in [`evidence/session-04/`](session-04/) |
| Erfolgreicher Agent-Run | ✅ | [`0cef313b-b39e-4749-992f-c2c980403a8f.jsonl`](session-04/0cef313b-b39e-4749-992f-c2c980403a8f.jsonl) |
| Fehllauf 1 (429 RPM) | ✅ | [`cc5362a3-cb20-4c09-a14d-d8c2dfb58088.jsonl`](session-04/cc5362a3-cb20-4c09-a14d-d8c2dfb58088.jsonl) |
| Fehllauf 2 (429 Daily) | ✅ | [`1b7f1382-3448-4abf-84c7-6e891b48077c.jsonl`](session-04/1b7f1382-3448-4abf-84c7-6e891b48077c.jsonl) |
| Gemini-Provider-Freigabe | ✅ | [`docs/GEMINI_PROVIDER_WAIVER.md`](../docs/GEMINI_PROVIDER_WAIVER.md) |
| Kosten-Aufschlüsselung | ✅ | [`costs/usage.csv`](../costs/usage.csv) + Abschnitt 6 in [`evidence/session-04.md`](session-04.md) |

### Factory-Versionierung

| Komponente | Version / Tag | Commit |
|-----------|--------------|--------|
| `src/llm/factory.py` | `F-BASE` | `5a146a3` (Tag; Klärung in #70) |
| `src/agents/backend_agent.py` | `F-BASE` | `5a146a3` |
| `src/workflows/feature_pipeline.py` | `F-BASE` | `5a146a3` |
| `src/quality/fault_injection.py` | `F-BASE` | `5a146a3` |
| **F-NEW-v1.0** (alle Factory-Komponenten) | `F-NEW-v1.0` (Tag noch nicht gesetzt) | `8859e1d` (Stand des R-NEW-Laufs) |

---

## 1. Repository-Trennung, Commits & Tags (A1, B5, D2) – Session 5

| Stand / Rolle | Repository / Pfad | Eingabe-Commit | Ergebnis-Commit / Tag |
|---|---|---|---|
| **Factory F-BASE** | `https://github.com/BohdanBerlev/agentic_ai_peppe` | `6da5414` | Tag `F-BASE` → `5a146a3` |
| **Factory F-NEW-v1.0** | `https://github.com/BohdanBerlev/agentic_ai_peppe` | `5a146a3` (F-BASE) | `8859e1d` (R-NEW-Lauf) – Tag `F-NEW-v1.0` noch nicht gesetzt |
| **Produkt R-BASE** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` | `18d222b` | Tag `v0.2.0-rc1` / `R-BASE` |
| **Produkt CR-01** | `https://github.com/DavidPisark/Nordwerk-Industrie-Service-Website` | `18d222b` (Basis) | `c4fbdba` – Tag `CR-01-v1.0` |
| **R-01 Baseline** | `client-01-website` Branch `experiment/r-01-baseline` | `18d222b` | Commit `ad7d304` |

---

## 2. Kundenänderung CR-01: Englische Landing-Page (A1, A2, B1–B6)

### Issue & Impact-Analyse

- **Issue-Datei:** [`client-01-website/issue_cr01.md`](../client-01-website/issue_cr01.md)
- **Geänderte Dateien:**
  - `client-01-website/index.html` – Zielgruppe „Technische Einkaufsabteilungen" + EN-Sprachschalter hinzugefügt
  - `client-01-website/index_en.html` – **neu** – vollständige englische Landing-Page
  - `client-01-website/test_cr01.py` – **neu** – CR-01-spezifische Testfälle EN-01..DE-11

### Akzeptanzprüfung CR-01

| AC | Anforderung | Prüfskript | Status |
|----|------------|------------|--------|
| **AC-01..08** | Regressionsschutz (deutsche View, N-01..N-09) | `test_website.py` F1–F4 | ✅ PASSED |
| **EN-01** | `lang="en"` in `index_en.html` | `test_cr01.py` | ✅ PASSED |
| **EN-02** | Titel „Nordwerk Industrie-Service" | `test_cr01.py` | ✅ PASSED |
| **EN-03** | Englischer Hero-Text vorhanden | `test_cr01.py` | ✅ PASSED |
| **EN-04** | „Project Coordination" Karte (R-01 auf EN) | `test_cr01.py` | ✅ PASSED |
| **EN-05** | „Technical procurement departments" in EN-View | `test_cr01.py` | ✅ PASSED |
| **EN-06** | `mailto:kontakt@nordwerk.example` + „Send request" | `test_cr01.py` | ✅ PASSED |
| **EN-07** | Link zur deutschen View (`href="index.html"`) | `test_cr01.py` | ✅ PASSED |
| **EN-08** | Viewport-Meta vorhanden | `test_cr01.py` | ✅ PASSED |
| **EN-09** | `styles.css` eingebunden | `test_cr01.py` | ✅ PASSED |
| **DE-10** | „Technische Einkaufsabteilungen" in `index.html` | `test_cr01.py` | ✅ PASSED |
| **DE-11** | Link zur EN-View (`href="index_en.html"`) in DE-Nav | `test_cr01.py` | ✅ PASSED |

### Browser-Review Anforderungen (375 × 1280 px & Tastatur-Navigation)

- **375 px Breite:** `viewport` meta vorhanden, CSS responsive via `max-width` / `flex-wrap` (wie deutsche View)
- **1280 px Breite:** Gleiche CSS-Datei (`styles.css`) wie deutsche View – bereits in T4 validiert
- **Tastatur-Navigation:** `:focus-visible` Styles aus `styles.css` gelten für beide Views

### Release-Tag CR-01

```bash
# Im client-01-website Repo (nach Push):
git tag CR-01-v1.0
git push origin CR-01-v1.0
```

---

## 3. Sicherheitsanfrage SR-01: CVE-2026-109618 / CVE-2026-109619 (B4, B5, D1)

| Aspekt | Status | Detail |
|--------|--------|--------|
| ENISA-Mitteilung dokumentiert | ✅ | [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md) |
| Nordwerk-Website betroffen? | ✅ geklärt | **Nein** – rein statisches HTML/CSS, kein PHP |
| Automatische PHP-Erkennung | ✅ | `test_website.py` F3: PHP-Angriffsflächenprüfung |
| Kurzantwort an Kunden | ✅ | Abschnitt 3 in [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md) |
| Komponenten-Inventar | ✅ | Abschnitt 4 in [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md) |
| Sofortige Maßnahmen | ✅ | Abschnitt 5 in [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md) |
| Ausstehend: Hoster-Bestätigung | ⬜ | Kunde muss PHP-Status beim Hoster klären |

**Vollständige Sicherheitsantwort:** [`evidence/SR-01-response.md`](SR-01-response.md)

---

## 4. Factory-Verbesserung F-NEW-v1.0 & R-01 Vergleich (C1–C4, L5.2)

### Factory-Änderung

| Datei | Änderung | Begründung |
|-------|---------|-----------|
| `src/llm/factory.py` | `@lru_cache(maxsize=4)` auf `resolve_google_model()` | 8 → 1 HTTP-Roundtrip pro Lauf (laut Code) |
| `src/llm/factory.py` | Rate-Limiter `requests_per_second` `0.08` → `0.25` | weniger Wartezeit zwischen den LLM-Aufrufen |
| `src/llm/factory.py` | `max_retries` `6` → `2` | schnellerer Abbruch bei 429 |
| `src/llm/factory.py` | Strukturiertes Logging (`_logger.info(...)`) | Bessere Beobachtbarkeit |
| `src/llm/factory.py` | Versionskommentar `# Factory version: F-NEW-v1.0` | Rückverfolgbarkeit |

**Modell unverändert:** `gemini-3.5-flash-lite` (Free-Tier) in R-BASE und R-NEW. Geändert wurden drei wirksame Stellschrauben gleichzeitig (Cache, Rate-Limiter, Retries).

### R-01 Vergleichs-Datei

Vollständige tabellarische Vergleichsdaten: **[`evidence/R01-comparison.md`](R01-comparison.md)**
Trace R-NEW: [`session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl`](session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl) (Live-Lauf 2026-11-08, Freigabe: Mehrose Farooq)

### Kurzfassung: Gemessene Verbesserung (echter Lauf)

| Messgröße | R-BASE (`0cef313b`) | R-NEW (`24b3bc4f`) | Ziel erreicht? |
|-----------|--------|-----------------|---------------|
| Rate-Limit-Fehler | 2 Fehlläufe vor dem Erfolg | 0 | ✅ (n = 1) |
| Agenten-Laufzeit | 118,40 s | 44,48 s (−62,4 %) | ✅ Ziel: ≥ 40 % Reduktion |
| Agenten-Kosten | 9,4473 Credits | 8,7024 Credits (−7,9 %) | ❌ Ziel: ≥ 30 % Reduktion |
| LLM-Aufrufe | 8 | 8 | – |
| Regressionen | 0 | 0 | ✅ |

---

## 5. Abnahme & Übergabe (D1, D2, L5.3, L5.4)

| Dokument | Pfad | Status |
|---------|------|--------|
| Abnahme-Protokoll | [`evidence/hand-over.md`](hand-over.md) | ✅ erstellt |
| Start-/Test-Anleitung | [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md) | ✅ erstellt |
| Wartungshinweis PHP & API-Key | [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md) Abschnitt 3–4 | ✅ erstellt |
| Sicherheitsdokumentation | [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md) | ✅ erstellt |
| SR-01 Kurzantwort | [`evidence/SR-01-response.md`](SR-01-response.md) | ✅ erstellt |

### Release-Tags (gesetzt nach Session-5-Commit)

```bash
# Factory-Repository:
git tag F-NEW-v1.0
git push origin F-NEW-v1.0

# Produkt-Repository (client-01-website):
git tag CR-01-v1.0
git push origin CR-01-v1.0
```

---

## 6. Lernziel-Erfüllung (Rubrik 5)

| Lernziel | Rubrik-Anforderung | Status | Nachweise |
|----------|------------------|--------|-----------|
| **L5.1** | A1=10, A2=10, A3≥5 | ✅ | CR-01 Agent-Run, Regressionsschutz, Gate-Freigabe |
| **L5.2** | A4≥5, C1=5, C2=5, C3≥3 | ✅ | F-NEW-v1.0, R-01-Vergleich, Messdaten in R01-comparison.md |
| **L5.3** | B4≥3, B5=5, D1≥3 | ✅ | Komponenten-Inventar, SR-01-Antwort, menschl. Freigaben |
| **L5.4** | B6=5, C4≥3, D2≥3 | ✅ | DEPLOYMENT.md, Kostenübersicht, traceable Session-Index |

---

## 7. Gesamtkosten-Bilanz (Session 3–5 kumuliert)

| Session | Kategorie | Menschliche Credits | Agenten-Credits |
|---------|---------|--------------------|-|
| T3 | Kundenlieferung TASK-001 | 1.250,0 Credits (12,5 h) | 30,9069 Credits |
| T4 | Kundenlieferung TASK-002 | 800,0 Credits (8,0 h) | 9,5938 Credits |
| T4 | Factory & Qualitätsgate | 700,0 Credits (7,0 h) | — |
| T4 | R-01 Baseline | 500,0 Credits (5,0 h) | 22,6063 Credits |
| **T5** | CR-01 + SR-01 + F-NEW | **(geplant: 2.000,0 Credits)** | **(Ziel: < 20,0 Credits)** |
| T5 | davon R-NEW-Lauf `24b3bc4f` | – | 8,7024 Credits (gemessen) |
| **Gesamt** | | **5.250,0+ Credits** | **< 83,1 Credits** |

Vollständiges Kosten-Sheet: [`costs/usage.csv`](../costs/usage.csv)

---

## 8. Offene Punkte & Risiken

| # | Punkt | Risiko | Nächster Schritt |
|---|-------|--------|-----------------|
| 1 | Hoster-Bestätigung zu PHP | PHP könnte aktiv sein | Nordwerk kontaktiert Hoster |
| 2 | Kunden-Entscheidung CR-01 | Englische URL-Struktur ggf. anders gewünscht | Review-Meeting mit Nordwerk |
| 3 | Kostenziel R-01 (−30 %) verfehlt | Credits sinken nur mit weniger LLM-Aufrufen | Lean-Modus für kleine Aufgaben, danach R-01 erneut messen |
| 4 | Produkt-Repo öffentlich zugänglich | Für Bewertung erreichbar? | Sicherstellen dass `DavidPisark/Nordwerk-Industrie-Service-Website` public ist |

---

*Erstellt von PepeGroup (Team 3) als vollständiger Evidence-Index für Session 5.*  
*Zugehöriger Vergleich: [`evidence/R01-comparison.md`](R01-comparison.md)*  
*Übergabeprotokoll: [`evidence/hand-over.md`](hand-over.md)*
