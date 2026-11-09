# Abnahme- & Übergabeprotokoll – Termin 5 (`CR-01-v1.0` & `SR-01`)

**Produkt:** Nordwerk Industrie-Service Website (`client-01-website`)  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-09  
**Session:** `session-05`

---

## 1. Technische Freigabe (Factory-Läufe, Regression & Browser-Review)

### A. Kundenänderung `CR-01`: Englische Einstiegsseite (`index_en.html`) + Zielgruppen-Erweiterung (`index.html`)

| Prüfung / Nachweis | Ergebnis | Beleg / Artefakt |
| :--- | :--- | :--- |
| **Factory-Lauf A (`index_en.html`)** | ✅ `approved` (8 Calls, `43,53 s`, `8,6905` Credits) | Trace [`52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl`](session-05/52b69365-3d49-4bcd-9c4d-f51ab8c136e7.jsonl), Commit `5227307`, Freigabe: **Mehrose Farooq** |
| **Factory-Lauf B (`index.html`)** | ✅ `approved` (8 Calls, `42,45 s`, `8,7329` Credits) | Trace [`c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl`](session-05/c0ee2cc3-4031-4ce9-8188-d37da99a1583.jsonl), Commit `263d007`, Freigabe: **Mehrose Farooq** |
| **`python test_website.py` (Regression F1–F4, AC-01..AC-08)** | ✅ `PASSED` (Exit-Code 0, 0 Fehler) | Prüffamilien `F1`, `F2`, `F3`, `F4` vollständig grün |
| **`python test_cr01.py` (`CR-01 EN` & `CR-01 DE`)** | ✅ `PASSED` (Exit-Code 0, 0 Regressionen) | Alle wörtlichen Pflichtinhalte (*Maintenance planning*, *Spare parts coordination*, *Operational documentation*, *Technical purchasing departments*, *Request information*, *Fictional company – HAW Hamburg course project. No real offers or contact.*) + *„Technische Einkaufsabteilungen“* in DE + beidseitiger Sprachwechsel |
| **Manuelles Browser- & Tastatur-Review (`375 px` / `1280 px`)** | ✅ `PASSED` (beide Ansichten DE & EN) | Protokoll: [`docs/customer-01/browser_review_t5.md`](../docs/customer-01/browser_review_t5.md), Prüfer: **Lars Boos** & **David Pisarkiewicz** |

### B. Gezielte Factory-Verbesserung `F-NEW-v1.0` & `R-01`-Vergleich

| Prüfung / Nachweis | Ergebnis | Beleg / Artefakt |
| :--- | :--- | :--- |
| **`@lru_cache(maxsize=4)` auf `resolve_google_model()` & Rate-Limiter-Tuning** | ✅ Implementiert & getestet | [`src/llm/factory.py`](../src/llm/factory.py), Unit-Test [`tests/test_factory_fnew_t5.py`](../tests/test_factory_fnew_t5.py) (`76 passed, 2 skipped` in [`evidence/session-05/pytest.xml`](session-05/pytest.xml)) |
| **Live-Vergleichslauf `R-NEW` auf `R-BASE` (`18d222b`)** | ✅ `PASSED` (`44,48 s` vs. `118,40 s` = **−62,4 %** Laufzeit, 0 Regressionen) | Trace [`24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl`](session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl), Auswertung [`evidence/R01-comparison.md`](R01-comparison.md), Freigabe: **Mehrose Farooq** |

---

## 2. Abgrenzung: Technische Freigabe vs. Kundenabnahme (D1 / B6 / L5.4)

| Status-Ebene | Status | Verantwortlich / Bemerkung |
| :--- | :--- | :--- |
| **1. Technische Freigabe (PepeGroup)** | ✅ **Technisch freigegeben** (`2026-11-09`) | Freigegeben durch **Mehrose Farooq** (Human Approval Gate `CR-01` & `R-NEW`), **David Pisarkiewicz** und **Lars Boos** (Browser-Review & `SR-01`-Faktenprüfung) sowie **Maxim Bers** (Tests & Kostenbilanz). |
| **2. Formale Kundenabnahme (`AC-01`–`AC-10`)** | ⬜ **Ausstehend (offene Kundenentscheidung)** | Die formale Abnahme erfolgt durch den Dozenten im Rahmen von Termin 5 anhand von [`docs/customer-01/acceptance.md`](../docs/customer-01/acceptance.md). Es wird ausdrücklich **keine** Selbstbehauptung *„vom Kunden akzeptiert“* aufgestellt. |

**Offene Punkte für das Kundengespräch (Nordwerk):**
1. **Entscheidung zum Altsystem (`SR-01`):** Einholen der schriftlichen Hoster-Auskunft zu PHP 8.2 / CMS-Patchstand bzw. endgültige Abschaltung des PHP-Interpreters und des alten CMS zugunsten des statischen Releases `CR-01-v1.0`.
2. **Akzeptanz des bewussten Funktionsverlusts:** Bestätigung durch Nordwerk, dass der Wegfall des Redaktions-CMS und des serverseitigen Kontaktformulars (Ersatz durch `mailto:kontakt@nordwerk.example`) für den Betrieb akzeptiert wird.
3. **Abnahme der englischen Einstiegsseite (`index_en.html`):** Formale Abnahme der kompakten englischen Einstiegsansicht durch den Kunden/Dozenten.

---

## 3. Sicherheitsanfrage `SR-01` (Zusammenfassung & Freigabe)

- **Kundenantwort (max. 1 Seite):** [`evidence/SR-01-response.md`](SR-01-response.md)
- **Technische Detailanalyse & Komponentenübersicht:** [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md)
- **Menschliche Faktenprüfung:** Geprüft und freigegeben durch **David Pisarkiewicz** und **Lars Boos** am `2026-11-09` anhand der ENISA-Mitteilung vom `21.10.2026` (`CVE-2026-109618` / `CVE-2026-109619`) und des Systemprofils vom `23.10.2026`.

---

## 4. Versionierte Release-Stände & Tags (B6 / D2)

| Repository | Release-Tag | Ziel-Commit | Inhalt |
| :--- | :--- | :--- | :--- |
| **Produkt-Repo** (`client-01-website`) | **`CR-01-v1.0`** & **`v0.3.0`** | `main` (inkl. Factory-Commits `5227307` & `263d007`) | Deutsche & englische Website (`index.html`, `index_en.html`, `styles.css`), Produkttests (`test_website.py`, `test_cr01.py`), `SR-01`-Antwort & Übergabe-Doku |
| **Factory-Repo** (`agentic_ai_peppe`) | **`F-NEW-v1.0`** | `main` (inkl. `src/llm/factory.py` & `tests/test_factory_fnew_t5.py`) | Factory mit `@lru_cache` & Rate-Limiter-Optimierung, `R-01`-Vergleich, `SR-01`-Analyse, `pytest.xml` & Gesamtkostenbilanz T3–T5 |

---

## 5. Übergabe, Start-/Test-Anleitung & Wartungsverantwortung

- **Vollständige Start-, Test- und Deployment-Anleitung:** [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md)
- **Schnellstart ohne Factory:**
  ```powershell
  cd client-01-website
  python test_website.py
  python test_cr01.py
  python -m http.server 8000
  ```
- **Wartungsverantwortung:**
  - **Hoster / Nordwerk:** Webserver-Grundbetrieb, TLS-Zertifikate, Domain/DNS sowie vollständige Deaktivierung von PHP im Auslieferungsverzeichnis.
  - **PepeGroup (bzw. Nordwerk nach Übergabe):** Pflege der statischen HTML/CSS-Inhalte und Ausführung der Regressionstests (`test_website.py`, `test_cr01.py`) vor jedem Release.
