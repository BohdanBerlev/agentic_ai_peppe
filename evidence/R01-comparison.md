# R-01 Vergleichsanalyse: R-BASE (`F-BASE`) vs. R-NEW (`F-NEW-v1.0`)

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-09  
**Aufgabe:** Empirischer Vorher-/Nachher-Vergleich der Factory-Verbesserung `F-NEW-v1.0`  
**Lernziel:** L5.2 (Kriterien `A4`, `C1`, `C2`, `C3`, `C4`) – Gezielte Factory-Verbesserung unter vergleichbaren Bedingungen ehrlich prüfen

Beide Vergleichswerte stammen aus **echten Live-Läufen** gegen die Google Gemini API (je 1 vollständiger erfolgreicher Durchlauf, $n = 1$, zuzüglich 2 dokumentierter Rate-Limit-Fehlläufe in der Baseline). `R-NEW` wurde am `2026-11-08` live ausgeführt (Workflow `24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158`, Freigabe am Human Gate: **Mehrose Farooq**).

---

## 1. Experiment-Manifest & Vergleichbarkeit (Kriterium C1)

| Eigenschaft | `R-BASE` (Baseline, Termin 4) | `R-NEW` (Verbesserung, Termin 5) |
| :--- | :--- | :--- |
| **Factory-Stand** | Tag **`F-BASE`** (`5a146a3`) | Tag **`F-NEW-v1.0`** (`8859e1d` / `main`) |
| **Produkt-Basis-Commit** | **`18d222b`** (Tag: `R-BASE` / `v0.2.0-rc1`) | **`18d222b`** (frischer Checkout von Tag `R-BASE`, keine Lösungsübernahme) |
| **Modell** | `gemini-3.5-flash-lite` | `gemini-3.5-flash-lite` *(identisch, kein Modellwechsel)* |
| **LLM-Provider & Temperatur** | Google Gemini (`temperature=0.2`, `timeout=90s`) | Google Gemini (`temperature=0.2`, `timeout=90s`) |
| **Aufgaben-Spezifikation** | `issue_r01.md`: Leistungskarte *„Projektkoordination“* ergänzen | `issue_r01.md`: **identische Aufgabe & identischer CLI-Befehl** |
| **Automatisierter Produktcheck** | `python test_r01.py` (`F1`–`F4` + `R-01`) | `python test_r01.py` (`F1`–`F4` + `R-01`) |
| **Ausführungsmodus** | `--full-company --use-backend-agent` (8 Rollen) | `--full-company --use-backend-agent` (8 Rollen) |
| **Session / Workflow-Trace** | [`session-04/0cef313b-b39e-4749-992f-c2c980403a8f.jsonl`](session-04/0cef313b-b39e-4749-992f-c2c980403a8f.jsonl) | [`session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl`](session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl) |
| **Produkt-Ergebnisstand** | Branch `origin/experiment/r-01-baseline` (`ad7d304`) | Isolierter Versuchs-Checkout (getrennt vom Kunden-Release `main`) |

> [!NOTE]
> **Abschließende Klärung zum Termin-4-Feedback (`F-BASE = 6da5414` vs. Tag `5a146a3`):**  
> In Termin 4 wurde vor dem `R-01`-Baseline-Lauf `0cef313b` (Start: `2026-11-02T09:26:52Z`) lokal in `src/llm/factory.py` die Drosselung auf `requests_per_second=0.08` (`max_retries=6`) gesetzt und unmittelbar nach dem Lauf um `09:30 Uhr` als Commit `5a146a3` eingecheckt und mit dem Git-Tag **`F-BASE`** versehen. In `evidence/session-04.md` war an einer Stelle noch der vorherige Doku-Commit `6da5414` (`00:55 Uhr`) eingetragen. Der tatsächlich bei `0cef313b` ausgeführte Code entspricht exakt dem Tag **`F-BASE` (`5a146a3`)**.

---

## 2. Gezielte Factory-Änderungen in `F-NEW-v1.0` gegenüber `F-BASE` (Kriterium A4)

Quelle: `git diff F-BASE..F-NEW-v1.0 -- src/llm/factory.py` sowie Unit-Test [`tests/test_factory_fnew_t5.py`](../tests/test_factory_fnew_t5.py) (`PASSED` in [`evidence/session-05/pytest.xml`](session-05/pytest.xml)).

| Parameter in `src/llm/factory.py` | `F-BASE` (`5a146a3`) | `F-NEW-v1.0` | Technische Wirkung |
| :--- | :--- | :--- | :--- |
| **`resolve_google_model()`** | Kein Cache: Vor jedem der 8 Agenten-Aufrufe erfolgt ein synchroner HTTP-GET-Request an `/v1beta/models`. | **`@lru_cache(maxsize=4)`**: Genau **1** HTTP-GET pro Pipeline-Prozess (7 von 8 Modell-Lookups kommen direkt aus dem RAM-Cache; belegt durch `test_resolve_google_model_lru_cache_prevents_redundant_http_calls`). | Eliminiert 7 redundante Netzwerk-Roundtrips pro Workflow-Run. |
| **Rate-Limiter `requests_per_second`** | `0.08` (1 Request alle `12,5 s`) | **`0.25`** (1 Request alle `4,0 s`, exakt passend zum 15-RPM-Limit des Gemini-Free-Tiers) | Reduziert die künstliche Wartezeit zwischen den 8 Agenten-Aufrufen von ~87,5 s auf ~28,0 s. |
| **`max_retries`** | `6` | **`2`** | Verhindert minutenlange Backoff-Kaskaden bei erschöpftem Tageskontingent (`429`). |
| **Strukturiertes Logging** | `print(...)` | `_logger.info(...)` mit Cache-Hit-Status (`cached=True/False`) | Bessere Beobachtbarkeit ohne Laufzeit-Overhead. |

---

## 3. Gemessene Vorher-/Nachher-Rohdaten (Kriterium C2)

| Messgröße | `R-BASE` (`0cef313b`, mit `F-BASE`) | `R-NEW` (`24b3bc4f`, mit `F-NEW-v1.0`) | $\Delta$ absolut | $\Delta$ relativ |
| :--- | :--- | :--- | :--- | :--- |
| **Status / Fehlversuche** | `PASSED` *(zuvor 2 Abbrüche wg. 429 Quota: `cc5362a3` [6,9086 Cr.] & `1b7f1382` [6,2504 Cr.])* | **`PASSED` im 1. Versuch** *(0 Rate-Limit-Fehler)* | $-2$ Fehlläufe | $-100\,\%$ Fehlläufe |
| **Reine Agenten-Laufzeit (`duration_seconds`)** | `118,40 s` | **`44,48 s`** | **$-73,92\text{ s}$** | **$-62,4\,\%$** |
| **Agenten-Kosten erfolgreicher Lauf (`estimated_cost_credits`)** | `9,4473 Credits` | **`8,7024 Credits`** | **$-0,7449\text{ Credits}$** | **$-7,9\,\%$** |
| **Agenten-Kosten inkl. Fehlläufen** | `22,6063 Credits` *(inkl. `cc5362a3` + `1b7f1382`)* | **`8,7024 Credits`** *(0 Fehlläufe)* | **$-13,9039\text{ Credits}$** | **$-61,5\,\%$** |
| **Anzahl LLM-Aufrufe (`calls`)** | `8` | `8` | `0` | `0,0 %` |
| **Summe Input-Tokens (alle 8 Rollen)** | `9.589 Tokens` | `9.542 Tokens` | $-47\text{ Tokens}$ | $-0,5\,\%$ |
| **Summe Output-Tokens (alle 8 Rollen)** | `1.883 Tokens` | `1.669 Tokens` | $-214\text{ Tokens}$ | $-11,4\,\%$ |
| **Backend-Implementierungsversuche (`impl_attempts`)** | `1` | `1` | `0` | `0,0 %` |
| **Produkttest `python test_r01.py` (`F1`–`F4` + `R-01`)** | `Exit-Code 0` (`0` Regressionen) | `Exit-Code 0` (`0` Regressionen) | `0` Fehler | unverändert stabil |
| **Menschliche Gate-Zeit (`human_review_seconds`)** | `30,00 s` *(David Pisarkiewicz)* | `328,11 s` *(Mehrose Farooq; inkl. Terminal-Wartezeit bis zur Eingabe)* | getrennt ausgewiesen | — |
| **Menschliche Nacharbeitszeit am Produktcode** | `0,0 s` (keine manuelle Code-Nacharbeit) | `0,0 s` (keine manuelle Code-Nacharbeit) | `0,0 s` | `0,0 %` |

---

## 4. Hypothesenprüfung & Empirische Entscheidung (Kriterium C3)

### Abgleich mit den Zielwerten aus Termin 4 (`session-04.md`)

| Teilhypothese aus Termin 4 | Zielwert | Messwert `R-NEW` (`24b3bc4f`) | Status |
| :--- | :--- | :--- | :--- |
| **1. Laufzeit-Reduktion durch `@lru_cache` + Rate-Limiter-Anpassung** | $\ge 40\,\%$ Reduktion ($< 71,0\text{ s}$) | **`44,48 s` ($-62,4\,\%$)** | ✅ **Übertroffen** |
| **2. Kosten-Reduktion pro Lauf (ohne Fehlläufe)** | $\ge 30\,\%$ Reduktion ($< 6,60\text{ Credits}$) | **`8,7024 Credits` ($-7,9\,\%$)** *(bzw. $-61,5\,\%$ inkl. Wegfall der 429-Fehlläufe)* | ❌ **Verfehlt (für Einzellauf)** |
| **3. Erhalt der vollen Prüfqualität & Regressionsfreiheit** | `test_r01.py` `Exit-Code 0`, `0` Regressionen | **`Exit-Code 0`, `0` Regressionen (`F1`–`F4` + `R-01` PASSED)** | ✅ **Erreicht** |

### Ehrliche Interpretation & Methodenkritik (Streuung, Stichprobengröße & Störfaktoren)
1. **Warum sank die Laufzeit um 62,4 %, die Einzellauf-Kosten aber nur um 7,9 %?**  
   In unserer Kostenformel setzt sich jeder der 8 Agenten-Aufrufe aus einem Basispreis ($\approx 1,0\text{ Credit}$ pro Call) plus einem kleinen Laufzeit- und Token-Aufschlag zusammen. Da in `F-NEW-v1.0` weiterhin **alle 8 Rollen** durchlaufen werden (`calls = 8`), bleibt der Sockelbetrag von $\ge 8,0\text{ Credits}$ bestehen; lediglich der zeitabhängige Aufschlag sank durch die kürzere Laufzeit um `0,7449 Credits` ($-7,9\,\%$). Um die Kosten eines einzelnen erfolgreichen Laufs unter `6,60 Credits` ($-30\,\%$) zu drücken, muss zwingend die **Anzahl der LLM-Aufrufe** reduziert werden (z. B. durch einen `--lean`-Modus, der für kleine HTML-Ergänzungen `project_manager` und `agent_engineer` überspringt und von 8 auf 5 Calls reduziert).
2. **Konfundierung mehrerer Parameter in `F-NEW-v1.0`:**  
   In `src/llm/factory.py` wurden `@lru_cache(maxsize=4)` und `requests_per_second: 0.08 -> 0.25` gemeinsam aktiviert. Rechnerisch entfallen von den eingesparten `73,92 s` rund `59,5 s` auf das kürzere Rate-Limiter-Intervall ($7 \times [12,5\text{ s} - 4,0\text{ s}]$) und rund `14,4 s` auf das Einsparen der 7 synchronen HTTP-GET-Requests an `/v1beta/models` plus geringere API-Latenz.
3. **Stichprobenlimit ($n = 1$ pro erfolgreicher Variante):**  
   Ein einzelnes Laufpaar erlaubt nur eine **vorläufige empirische Beobachtung**, da Netzwerk- und Gemini-API-Antwortzeiten tageszeitabhängig schwanken. Allerdings bestätigen die beiden anschließenden `CR-01`-Läufe mit `F-NEW-v1.0` (`52b69365`: `43,53 s`, `8,6905 Credits`; `c0ee2cc3`: `42,45 s`, `8,7329 Credits`) die hohe Reproduzierbarkeit der neuen Laufzeit von **42–45 Sekunden** über insgesamt **3 aufeinanderfolgende Läufe**.

### Begründete Entscheidung (Beibehalten / Anpassen / Zurücknehmen)
- **Entscheidung:** **`F-NEW-v1.0` wird BEIBEHALTEN (`retain`) und für den weiteren Ausbau um einen `--lean`-Modus angepasst (`adapt`).**
- **Begründung:** Die Laufzeitverbesserung von ~118 s auf ~44 s ($-62,4\,\%$) bei 0 Regressionen und 7 eingesparten HTTP-Requests pro Lauf verbessert die Entwickler- und Review-Ergonomie drastisch (wie in den beiden `CR-01`-Läufen sofort praktisch genutzt). Für das noch offene Kostenziel ($-30\,\%$ Credits pro Einzellauf) ist als nächster Ausbauschritt ein expliziter `--lean`-Pipeline-Pfad (5 statt 8 Agenten-Calls für eng begrenzte Änderungs-Issues) vorgesehen.
