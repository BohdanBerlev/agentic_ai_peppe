# R-01 Vergleichsanalyse: R-BASE (F-BASE) vs. R-NEW (F-NEW)

**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-08  
**Aufgabe:** Empirischer Vorher-/Nachher-Vergleich der Factory-Verbesserung F-NEW-v1.0  
**Lernziel:** L5.2 (C1, C2, C3) – Factory-Verbesserung mit Messgrößen

Beide Werte sind **echte Läufe** (je 1 Lauf, n = 1). R-NEW wurde am 2026-11-08 live gegen die Gemini-API ausgeführt (Workflow `24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158`, Freigabe: Mehrose Farooq).

---

## 1. Experiment-Manifest

| Eigenschaft | R-BASE (Baseline, T4) | R-NEW (Verbesserung, T5) |
|-------------|----------------------|--------------------------|
| **Factory-Stand** | Tag `F-BASE` = `5a146a3` (siehe Hinweis unten) | `8859e1d` (Branch `Vorbereitung-Termin-5`, Tag `F-NEW-v1.0` noch nicht gesetzt) |
| **Produkt-Basis-Commit** | `18d222b` (Tag: `R-BASE`) | `18d222b` (Tag: `R-BASE`) |
| **Modell** | `gemini-3.5-flash-lite` | `gemini-3.5-flash-lite` (unverändert) |
| **LLM-Provider** | Google Gemini (Free-Tier) | Google Gemini (Free-Tier) |
| **Aufgabe** | R-01: Leistungskarte „Projektkoordination“ ergänzen | R-01: identische Aufgabe, identischer Befehl |
| **Test-Skript** | `test_r01.py` | `test_r01.py` |
| **Ausführungsmodus** | `--full-company --use-backend-agent` | `--full-company --use-backend-agent` |
| **Session / Workflow** | `session-04` / `0cef313b-b39e-4749-992f-c2c980403a8f` | `session-05` / `24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158` |

> [!NOTE]
> Der R-BASE-Lauf startete am 2026-11-02 um 09:26 und lief mit `requests_per_second=0.08` (siehe `session-04.md`). Diesen Stand enthält Tag `F-BASE` = `5a146a3` (Commit 09:30). Der in `session-04.md` genannte Commit `6da5414` (00:55) enthält dagegen schon `0.25`. Diese Abweichung ist offen in Issue #70.

---

## 2. Factory-Änderungen F-NEW gegenüber F-BASE

Quelle: `git diff 5a146a3 8859e1d -- src` (nur `src/llm/factory.py` geändert).

| Änderung | F-BASE (`5a146a3`) | F-NEW (`8859e1d`) | Wirkung |
|----------|--------------------|-------------------|---------|
| `resolve_google_model()` | ohne Cache: HTTP-GET an die Models-API bei jedem Agenten | `@lru_cache(maxsize=4)`: 1 HTTP-GET pro Prozess | spart laut Code 7 von 8 Abfragen (nicht separat gemessen) |
| Rate-Limiter `requests_per_second` | `0.08` (1 Anfrage alle 12,5 s) | `0.25` (1 Anfrage alle 4 s) | weniger Wartezeit zwischen den 8 LLM-Aufrufen |
| `max_retries` | `6` | `2` | bei 429-Fehlern schneller Abbruch statt langer Wiederholung |
| Logging | `print(...)` | `print(...)` + `_logger.info(...)` | keine Wirkung auf Laufzeit |

**Es wurden also drei wirksame Stellschrauben gleichzeitig geändert, nicht nur der Cache.**

---

## 3. Messwerte

| Messgröße | R-BASE (`0cef313b`) | R-NEW (`24b3bc4f`) | Δ absolut | Δ relativ |
|-----------|--------------------|--------------------|-----------|-----------|
| **Ergebnis** | PASSED (nach 2 Fehlläufen mit 429) | PASSED (1. Versuch, kein 429) | – | – |
| **Agenten-Laufzeit (`duration_seconds`)** | 118,40 s | **44,48 s** | −73,92 s | **−62,4 %** |
| **Agenten-Kosten (`estimated_cost_credits`)** | 9,4473 Credits | **8,7024 Credits** | −0,7449 Credits | **−7,9 %** |
| **LLM-Aufrufe** | 8 | 8 | 0 | 0 % |
| **Backend-Versuche (`impl_attempts`)** | – | 1 | – | – |
| **`test_r01.py` Exit-Code** | 0 | 0 | – | – |
| **Regressionen (F1–F4)** | 0 | 0 | 0 | – |
| **Menschliche Review-Zeit (`human_review_seconds`)** | 30,0 s | 328,1 s | nicht vergleichbar | – |

Die Review-Zeit von R-NEW enthält die Wartezeit, bis die Freigebende am Gate war. Sie misst nicht den Prüfaufwand und fließt nicht in den Vergleich ein.

---

## 4. Ziele aus Termin 4 vs. Ergebnis

| Ziel (aus `session-04.md`) | Zielwert | Ergebnis R-NEW | Erreicht? |
|----------------------------|----------|----------------|-----------|
| Laufzeit −40 % | < 71,0 s | 44,48 s (−62,4 %) | ✅ ja |
| Kosten −30 % | < 6,60 Credits | 8,7024 Credits (−7,9 %) | ❌ nein |
| gleiche Prüfqualität | Exit 0, 0 Regressionen | Exit 0, 0 Regressionen | ✅ ja |

---

## 5. Bewertung

1. **Laufzeit:** Das Ziel ist klar erreicht. Der größte Teil der Einsparung kommt sehr wahrscheinlich vom lockereren Rate-Limiter: Bei 8 Aufrufen mit 12,5 s Abstand entstehen allein rund 87 s Wartezeit, bei 4 s Abstand rund 28 s. Der Cache spart nur wenige kurze HTTP-Abfragen. Diese Aufteilung ist eine Abschätzung aus dem Code, keine getrennte Messung.
2. **Kosten:** Das Ziel ist verfehlt. Die Kosten hängen an der Zahl der LLM-Aufrufe und an der Laufzeit. Die Aufrufe blieben bei 8, nur der Laufzeitanteil sank. Für −30 % muss die Zahl der Aufrufe sinken, z. B. durch den in Termin 4 geplanten Lean-Modus, der bei kleinen Aufgaben Agenten überspringt.
3. **Risiko:** `requests_per_second=0.25` entspricht 15 Anfragen pro Minute und liegt damit direkt am Free-Tier-Limit. `max_retries=2` bricht bei 429 früher ab. In diesem Lauf trat kein 429 auf, bei n = 1 ist das aber kein Beleg für Stabilität.
4. **Einschränkung:** Je ein Lauf pro Seite; Schwankungen der API-Antwortzeit sind nicht herausgerechnet. F-NEW änderte drei Stellschrauben gleichzeitig, deshalb lässt sich die Wirkung nicht einer einzelnen Änderung zuordnen.

**Entscheidung:** F-NEW wird für die Laufzeit übernommen. Das Kostenziel bleibt offen und ist der nächste Verbesserungsschritt (weniger LLM-Aufrufe).

---

## 6. Akzeptanz & Regression

| Prüfung | R-BASE | R-NEW (gemessen) |
|---------|--------|------------------|
| `python test_r01.py` Exit-Code | 0 ✅ | 0 ✅ |
| F1 Pflichtinhalt | PASSED ✅ | PASSED ✅ |
| F2 Kontakt & Navigation | PASSED ✅ | PASSED ✅ |
| F3 Lokale Verweise & Assets | PASSED ✅ | PASSED ✅ |
| F4 Bedienbarkeit statisch | PASSED ✅ | PASSED ✅ |
| R-01 Zusatzleistung „Projektkoordination“ | PASSED ✅ | PASSED ✅ |

---

## 7. Gesamtkosten-Bilanz (Session 3–5 kumuliert)

| Session | Menschliche Credits | Agenten-Credits | Gesamt |
|---------|--------------------|-----------------|--------|
| T3 | 1.250,0 Credits (12,5 h) | 30,9069 Credits | 1.280,91 Credits |
| T4 | 2.000,0 Credits (20,0 h) | 22,6063 Credits | 2.022,61 Credits |
| **T5 (Stand 2026-11-08)** | offen | 8,7024 Credits (bisher nur R-NEW) | offen |
| **Kumuliert T3–T5** | offen | **62,2156 Credits** | offen |

---

*Erstellt von PepeGroup (Team 3) als Teil der Session-5-Evidenz.*  
*Zugehöriger Evidence-Index: [`evidence/session-05.md`](session-05.md)*  
*Trace R-NEW: [`evidence/session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl`](session-05/24b3bc4f-9baa-4c2a-bd9d-9ccf1cf53158.jsonl)*
