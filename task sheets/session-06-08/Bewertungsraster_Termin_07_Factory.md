# Bewertungsraster Termin 7 / Assessment rubric Session 7

**Fachtests, Fehlererkennung und Baseline / Business tests, fault detection and baseline · Version 1.0 · 08.11.2026**

Verbindliche Aufgaben / Binding tasks: [DE](Aufgabenblatt_Termin_07_de.md) · [EN](Task_Sheet_Session_07_en.md)

## Anwendung / Use

Unbenotetes Projekt, 100 Punkte formatives Feedback pro Termin. / Ungraded project, 100 formative feedback points per session.

Bewertet Teamleistung gegenüber dem Starter und den Stand des jeweiligen Tages. Wiederverwendung eigener früherer Fähigkeiten zählt als nachgewiesene Wiederverwendung, nicht als neu erfundene Fähigkeit. Starter-Tests und unveränderte Vorlagen ersetzen keine eigene Leistung. Kein Bonus für Agentenzahl, Autonomie, UI-Schmuck oder zusätzliche Frameworks. / Assess team work beyond the supplied starter and the current daily state. Evidenced reuse of earlier team capabilities counts as reuse, not as newly invented functionality. Supplied tests/unchanged templates do not replace own work. No bonus for agent count, autonomy, UI decoration or extra frameworks.

| Maximum | Vollständig / Full | Teilweise / Partial | Fehlend / Absent |
|---:|---:|---:|---:|
| 10 | 10 | 5 | 0 |
| 5 | 5 | 3 | 0 |

Vollständig: alle Merkmale der Zeile belegt. Teilweise: sinnvoller Kern belegt, konkretes fehlendes Merkmal benennen. Fehlend: kein belastbarer Kern oder Widerspruch zur Ausführung. Nur diese Werte verwenden. Unzugängliche Evidenz als unbekannt markieren; Punkte vorläufig nur für Belegtes. Kein Lauf aus einer README-Behauptung unterstellen. / Full: all features evidenced. Partial: meaningful core evidenced; name the missing feature. Absent: no reliable core or execution contradicts it. Use only these scores. Mark inaccessible evidence unknown and award provisional points only for demonstrated work. Do not infer execution from a README claim.

Reale Traces mit passenden Diffs/Testergebnissen können einen Live-Neulauf ersetzen. Mock-Tests belegen Workflow-Logik, keinen realen LLM-Aufruf. Erwartete Negativtests zählen als bestanden, wenn der Fehler erkannt wird. Unbekannte Kosten sind keine Nullkosten. / Real traces with matching diffs/test results can replace live reruns. Mock tests establish workflow logic, not real LLM use. Expected negative tests pass when the error is detected. Unknown costs are not zero costs.

## Punktestand und Lernziele getrennt ausweisen / Separate scores and objectives

85–100 sehr starker Stand / strong; 70–84 solider Stand / solid; 55–69 teilweise / partial; 0–54 wesentliche Lücken / major gaps. Keine Noten. / Not grades.

Je Lernziel: **erreicht / achieved**, **teilweise / partial**, **nicht erreicht / not achieved**, **unbekannt / unknown**, jeweils mit Datei/Run/Commit-Beleg. „Erreicht“ erfordert die unten genannten Punktwerte und Zusatzbedingungen. Teilweise bedeutet belegten Teilfortschritt; unbekannt bleibt offen. / For each objective report achieved, partial, not achieved or unknown, with file/run/commit evidence. Achieved requires the scores and additional conditions below. Partial means evidenced progress; unknown stays pending.

**Tagesziel insgesamt erreicht:** mindestens 70/100, Factory A mindestens 28/40, Messung C mindestens 10/20 und alle vier Lernziele erreicht. Sonst bei Teilfortschritt teilweise, ohne solchen nicht erreicht; entscheidende unbekannte Evidenz ergibt offen. Alle Einzelwerte sichtbar lassen, keine weiteren Caps oder geheimen Abzüge. / **Overall achieved:** at least 70/100, A at least 28/40, C at least 10/20 and all four objectives achieved. Otherwise partial if progress exists, not achieved without progress; decisive unknown evidence means pending. Keep raw values visible; no extra caps or hidden deductions.

Committed Secrets als kritischen Befund mit Abhilfe nennen. Keine Anforderungen späterer Termine vorwegnehmen. Kundenprodukt und Factory-Lernen separat erklären. / Flag committed secrets with remediation. Do not apply later requirements early. Explain product result separately from Factory learning.

## Kriterien und Evidenz / Criteria and evidence

| ID | Max. | Kriterium / Criterion | Vollständiger Nachweis / Full evidence | Belege / Evidence |
|---|---:|---|---|---|
| A1 | 10 | Factory wiederholt einsetzen / Repeat Factory use | Neuer substanzieller HansePack-Task verwendet bestehende Factory/Projektkonfiguration; Produkt und Factory bleiben getrennt. / New substantial HansePack task uses existing Factory/project config; product/Factory remain separate. | Task, Konfiguration / Task, config |
| A2 | 10 | Realer Folgelauf / Real subsequent run | Realer LLM-/Tool-Lauf, strukturierte Kooperation zweier Fähigkeiten, agentischer Produktdiff und Eingriffsprotokoll belegt. / Real LLM/tool run, structured two-capability cooperation, agent product diff and intervention record evidenced. | Trace, Diff / Trace, diff |
| A3 | 10 | Fachfehler wirksam blockieren / Effectively block business fault | Absichtlich falsche Rabattgrenze löst Q03-Fehler aus; unveränderte Tests verhindern Freigabe/erzwingen Korrektur; korrekter Stand besteht und wird menschlich entschieden. / Injected discount boundary fault fails Q03; unchanged checks block approval/trigger correction; corrected version passes with human decision. | Fehler-/Korrekturlauf, Gate / Fault/correction run, gate |
| A4 | 10 | Factory-Gate getestet / Tested Factory gate | Eigene Tests für bestandenen/zurückgehaltenen Zustand erfolgreich; Schleifen-/Projektgrenzen bestehen weiter. / Own tests for passed/blocked states succeed; loop/project boundaries retained. | pytest, Workflow-Code / pytest, workflow code |
| B1 | 5 | Rabatte und Rundung / Discounts and rounding | Alle Positionswerte Q01–Q14 nach HP-V1 korrekt, einschließlich Q04/Q13 und Staffelgrenzen. / All Q01–Q14 line values correct under HP-V1, including Q04/Q13 and tier boundaries. | Fachtests, Fixture-Abgleich / Business tests, fixtures |
| B2 | 5 | Versand und Summen / Shipping and totals | Alle Warenwerte/Versand/Gesamtsummen Q01–Q14 HP-V1 korrekt, Q06 nach Rabatt und Q07 an Schwelle. / All Q01–Q14 goods net/shipping/totals correct for HP-V1; Q06 after discount and Q07 at threshold. | Fachtests / Business tests |
| B3 | 5 | Validierung / Validation | E01–E10 in Python zurückgewiesen, kein gültiges Angebot; keine stille Typumwandlung oder SKU-Zusammenfassung. / E01–E10 rejected in Python, no valid quote; no silent type coercion or SKU aggregation. | Validierungstests / Validation tests |
| B4 | 5 | Kleine nutzbare Oberfläche / Small usable UI | Positionen erfassbar, Berechnung/Fehler sichtbar, Nettokennzeichnung; menschlicher Mehrpositions-/Fehlerreview dokumentiert. / Lines enterable, calculation/errors visible, net notice; human multi-line/error review recorded. | UI, Review / UI, review |
| B5 | 5 | Konsistenter JSON-Export / Consistent JSON export | Pflichtfelder mit Integer-Cent und Regelversion vorhanden; Download stimmt mit Anzeige/Ergebnis überein, menschlich geprüft. / Required fields with integer cents/rule version; download matches display/result, human checked. | Export, Test, Review / Export, test, review |
| B6 | 5 | Eigenständiger Candidate / Independent candidate | Versionierter korrekter Candidate startet/testet aus frischem Checkout ohne Factory; unabhängige Kundenfixtures unverändert. / Versioned correct candidate starts/tests from fresh checkout without Factory; independent customer fixtures unchanged. | Commit, Start-/Testprotokoll / Commit, startup/test record |
| C1 | 5 | Reproduzierbare R-02-Baseline / Reproducible R-02 baseline | Sauberer Q-BASE/F-BASE, identisches benanntes R-02, Modell/Einstellungen, Kriterien, echte Commits/Run und getrennte Versuchsausgabe gesichert. / Clean Q-BASE/F-BASE, specified R-02, model/settings, criteria, actual commits/run and isolated output preserved. | Manifest, git status / Manifest, git status |
| C2 | 5 | Tageskosten / Daily costs | Alle zugehörigen menschlichen/Agenten-/CI-Aufwände inkl. Fehlläufen erfasst; Factory-Entwicklung getrennt, Budgetabweichung erklärt. / All relevant human/agent/CI effort including failures recorded; Factory development separate, budget deviation explained. | Kosten und Rohdaten / Costs and raw records |
| C3 | 5 | Baseline gemessen / Baseline measured | Mindestens ein vollständiger R-02-Lauf mit Qualität, Review-/Nacharbeit und bekannten Kosten; Scheitern/Unbekanntes ehrlich gekennzeichnet. / At least one full R-02 run with quality, review/rework and known costs; failure/unknowns honestly marked. | Versuchsdaten, Prüfbericht / Experiment records, checks |
| C4 | 5 | Gezielte Hypothese / Targeted hypothesis | Belegter Engpass, kleine geplante Factory-Änderung und erwartete Messgröße; Baseline vor untersuchter Intervention. / Evidenced bottleneck, small planned Factory change and expected measure; baseline before investigated intervention. | Hypothese, Versionsfolge / Hypothesis, version sequence |
| D1 | 5 | Verantworteter Review / Accountable review | Benannter Mensch prüft Diff und Fach-/UI-/Exportresultat; Candidate-Freigabe und absichtlicher Fehlerstand klar unterschieden. / Named human reviews diff/business/UI/export result; candidate approval distinguished from injected-fault state. | Review, Entscheidung / Review, decision |
| D2 | 5 | Nachvollziehbarer Tagesstand / Traceable daily state | Session-07-Index verlinkt Candidate, Tests, Fehlernachweis, Baseline, Kosten und nächste Schritte. / Session-07 index links candidate, tests, fault evidence, baseline, costs and next actions. | evidence/session-07.md |

**A Factory 40 · B Kundenprodukt / Customer product 30 · C Messung und Lernen / Measurement and learning 20 · D Verantwortung und Übergabe / Accountability and handover 10 = 100.**

## Vier Lernziele / Four objectives

| Lernziel / Objective | Mindestpunkte / Required scores | Zusatzbedingungen / Additional conditions |
|---|---|---|
| L7.1 | A1 = 10; A2 = 10 | Weiterer echter Produkt-Task durch dieselbe Factory. / Another real product task through the same Factory. |
| L7.2 | A3 = 10; D1 = 5 | Unabhängige Kundenerwartungen beeinflussen technische Freigabe; Mensch entscheidet konkret. / Independent customer expectations affect technical approval; human decides on specific result. |
| L7.3 | A3 = 10; A4 ≥ 5 | Erkanntes Scheitern, Zurückhalten und erfolgreiche Korrektur belegt. / Detected failure, blocking and successful correction evidenced. |
| L7.4 | C1 = 5; C3 = 5; C4 ≥ 3 | Technisch wiederholbarer Ausgangsversuch mit Messung und nachgelagerter Hypothese. / Technically repeatable baseline with measurements and subsequent hypothesis. |

## Abgrenzung / Scope

HP-V2/CR-02 und positiver Optimierungseffekt sind noch nicht fällig. R-02 bleibt isoliert und gehört nicht in die Kundenabnahme. / HP-V2/CR-02 and positive optimisation effect not due yet. R-02 remains isolated, outside customer acceptance.

## Bewertungsprotokoll / Assessment record

Team, Termin, tatsächliche Factory-/Produkt-Commits; je Kriterium Punkte, Fundstelle und beobachtet/unbekannt; A–D und Gesamtsumme; je Lernziel Status/Begründung; Gesamttagesziel; Stärken, kritische Befunde und höchstens drei nächste Schritte. / Team, session, actual Factory/product commits; per criterion score, reference and observed/unknown; A–D/total; each objective status/reason; overall daily target; strengths, critical findings and at most three next actions.

Automatische Checks unterstützen die Bewertung. Gezielter menschlicher Review bleibt für reale Beiträge, UI-Nutzbarkeit, Kundenstatus und empirische Interpretation nötig. / Automated checks support assessment. Targeted human review remains necessary for real contributions, UI usability, customer status and empirical interpretation.
