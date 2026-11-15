# Bewertungsraster Termin 8 / Assessment rubric Session 8

**Änderungslieferung und wirtschaftliches Factory-Lernen / Change delivery and economic Factory learning · Version 1.0 · 08.11.2026**

Verbindliche Aufgaben / Binding tasks: [DE](Aufgabenblatt_Termin_08_de.md) · [EN](Task_Sheet_Session_08_en.md)

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
| A1 | 10 | Versionierte Kundenänderung / Versioned customer change | CR-02 aus T7-Candidate durch dieselbe zentrale Factory bearbeitet; Projektkontext, Ausgangsstand und Auswirkungsanalyse klar. / CR-02 handled from S7 candidate through same central Factory; project context, base and impact analysis clear. | Issue, Commits, Konfiguration / Issue, commits, config |
| A2 | 10 | Agentischer Änderungsbeitrag / Agent change contribution | Realer LLM-/Tool-Lauf mit zwei kooperierenden Fähigkeiten, agentischem Produktdiff und benannten menschlichen Eingriffen. / Real LLM/tool run with two cooperating capabilities, agent product diff and identified human interventions. | Trace, Produktdiff / Trace, product diff |
| A3 | 10 | Regressionsgate / Regression gate | Versionsrichtige Q-/E-Prüfungen beeinflussen Freigabe; konkrete menschliche Entscheidung; keine ungeprüfte Übernahme. / Version-correct Q/E checks affect approval; specific human decision; no unchecked adoption. | Testergebnisse, Gate / Test results, gate |
| A4 | 10 | Gezielte Factory-Änderung / Targeted Factory change | Eine begründete kleine Intervention zentral implementiert, sinnvoll getestet, versioniert und tatsächlich auf R-02 angewendet. / One justified small intervention centrally implemented, meaningfully tested, versioned and actually applied to R-02. | Factory-Diff, Test, Run / Factory diff, test, run |
| B1 | 5 | Neue Versandregel / New shipping rule | Q01–Q14 unter HP-V2 korrekt, Schwelle nach Rabatt und inklusive Gleichheit; Versand/Gesamt und Regelversion angepasst. / Q01–Q14 correct under HP-V2, post-discount inclusive threshold; shipping/total and rule version updated. | Fachtests, besonders Q06/Q10/Q11 / Business tests, especially Q06/Q10/Q11 |
| B2 | 5 | Bestand fachlich erhalten / Preserve business behaviour | Positionswerte/Rabatte unverändert, E01–E10 abgewiesen; alte V1-Versandwerte nicht als V2-Soll verwendet. / Line values/discounts preserved, E01–E10 rejected; obsolete V1 shipping not used as V2 expectation. | Regressionstests, historische V1-Evidenz / Regression tests, historical V1 evidence |
| B3 | 5 | UI und Export konsistent / Consistent UI and export | Neuer Versand und Gesamt in Anzeige/JSON identisch, Pflichtfelder und Nettokennzeichnung erhalten; menschlicher Review. / Updated shipping/total identical in UI/JSON, required fields/net notice retained; human review. | Export-/UI-Test, Review / Export/UI check, review |
| B4 | 5 | Unabhängiger Produktbetrieb / Independent product runtime | Release aus frischem Checkout ohne Factory/LLM start-/testbar, Anleitung aktuell. / Release starts/tests from fresh checkout without Factory/LLM, instructions current. | Start-/Testnachweis / Startup/test record |
| B5 | 5 | Kundentrennung erhalten / Customer isolation retained | Nordwerk-Stand unverändert und separat zugänglich; Experiment/Fehlerstand nicht Kundenrelease. / Nordwerk unchanged and separately accessible; experiment/fault state not customer release. | Commits/Status, Branch-Zuordnung / Commits/status, branch mapping |
| B6 | 5 | Übergabe und Abnahmestatus / Handover and acceptance status | Versionierter Release, Regel-/Start-/Testhinweise, Restmängel sowie wahrer technischer und Kundenstatus. Ausstehende Dozentenentscheidung erlaubt. / Versioned release, rules/start/test notes, defects and true technical/customer status. Pending instructor decision allowed. | Release, Übergabe, Status / Release, handover, status |
| C1 | 5 | Kontrollierter Vergleich / Controlled comparison | Beide Varianten gleiches HP-V1-Q-BASE, R-02, Modell/Provider/Einstellungen und unabhängige Kriterien; frische getrennte Runs ohne Lösungstransfer. / Both variants use same HP-V1-Q-BASE, R-02, model/provider/settings and independent criteria; fresh isolated runs without solution transfer. | Versuchsmanifest, Inputstände / Experiment manifest, inputs |
| C2 | 5 | Vollständige Versuchsdaten / Complete experiment data | Mindestens ein Vorher-/Nachher-Lauf; Qualität, Fehler, menschliche Zeit und bekannte Agenten-/CI-Kosten erfasst; Verbesserungsentwicklung getrennt. / At least one before/after run; quality, faults, human time and known agent/CI costs recorded; improvement development separate. | Run-Daten, Kosten / Run records, costs |
| C3 | 5 | Ehrliche Interpretation / Honest interpretation | Ergebnis mit Stichprobenlimits diskutiert; Entscheidung beibehalten/anpassen/zurücknehmen begründet, kein Zwang zu positivem Effekt. / Result discussed with sample limits; retain/adapt/revert justified, no positive effect required. | Kurze Auswertung / Short analysis |
| C4 | 5 | Bilanz und Wiederverwendung / Totals and reuse | T6–8-Kosten ohne doppelte Stunden inkl. Fehlläufen/CI; Budgetabweichung, reuse-/kundenspezifischer Aufwand und dritte-Kunden-Entscheidung mit Belegen. / S6–8 costs without duplicate hours including failures/CI; budget deviation, reuse/customer-specific effort and third-customer decision evidenced. | Bilanz, drei Antworten / Totals, three answers |
| D1 | 5 | Menschliche Verantwortung / Human accountability | Review mit Name/Zeitpunkt an konkretem Commit; technische Freigabe von Kundenabnahme unterschieden. / Review with name/time on specific commit; technical approval distinguished from customer acceptance. | Review/Abnahmeprotokoll / Review/acceptance record |
| D2 | 5 | Prüfbarer Abschluss / Inspectable closure | Session-08-Index zugänglich, Produkt-/Factory-Commits, Runs, Tests, Experiment, Kosten und offene Arbeit verknüpft. / Accessible session-08 index links product/Factory commits, runs, tests, experiment, costs and open work. | evidence/session-08.md |

**A Factory 40 · B Kundenprodukt / Customer product 30 · C Messung und Lernen / Measurement and learning 20 · D Verantwortung und Übergabe / Accountability and handover 10 = 100.**

## Vier Lernziele / Four objectives

| Lernziel / Objective | Mindestpunkte / Required scores | Zusatzbedingungen / Additional conditions |
|---|---|---|
| L8.1 | A1 = 10; A2 = 10 | Reale versionierte CR-02-Lieferung durch bestehende Factory. / Real versioned CR-02 delivery through existing Factory. |
| L8.2 | A3 ≥ 5; B1 = 5; B2 = 5; B3 ≥ 3 | Zusätzlich ausgeführte Regression und konkrete menschliche Freigabe oder begründetes Zurückhalten. / Additionally executed regression and concrete human approval or justified withholding. |
| L8.3 | A4 ≥ 5; C1 = 5; C2 = 5; C3 ≥ 3 | Identischer Produkt-Ausgangspunkt, belegte Änderung und ehrlicher Versuch; positiver Effekt nicht nötig. / Identical product base, evidenced intervention and honest experiment; positive effect unnecessary. |
| L8.4 | B6 = 5; C4 ≥ 3; D2 ≥ 3 | Übergabe, Gesamtaufwand und belegte Reuse-Erkenntnisse; keine kausalen Sparbehauptungen aus verschiedenen Produkten. / Handover, total effort and evidenced reuse lessons; no causal savings claims from different products. |

## Abgrenzung / Scope

Keine Pflicht zu zusätzlichen Agenten, ERP/PDF, Euro-Rentabilität, gleichzeitiger V1/V2-Unterstützung oder positivem Optimierungseffekt. / No requirement for more agents, ERP/PDF, euro profitability, simultaneous V1/V2 support or positive optimisation effect.

## Bewertungsprotokoll / Assessment record

Team, Termin, tatsächliche Factory-/Produkt-Commits; je Kriterium Punkte, Fundstelle und beobachtet/unbekannt; A–D und Gesamtsumme; je Lernziel Status/Begründung; Gesamttagesziel; Stärken, kritische Befunde und höchstens drei nächste Schritte. / Team, session, actual Factory/product commits; per criterion score, reference and observed/unknown; A–D/total; each objective status/reason; overall daily target; strengths, critical findings and at most three next actions.

Automatische Checks unterstützen die Bewertung. Gezielter menschlicher Review bleibt für reale Beiträge, UI-Nutzbarkeit, Kundenstatus und empirische Interpretation nötig. / Automated checks support assessment. Targeted human review remains necessary for real contributions, UI usability, customer status and empirical interpretation.
