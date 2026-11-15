# Bewertungsraster Termin 6 / Assessment rubric Session 6

**Projektwechsel und erster fachlicher Durchlauf / Project switching and first business delivery · Version 1.0 · 08.11.2026**

Verbindliche Aufgaben / Binding tasks: [DE](Aufgabenblatt_Termin_06_de.md) · [EN](Task_Sheet_Session_06_en.md)

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
| A1 | 10 | Wiederverwendete Factory / Reused Factory | Bestehende Factory adressiert neues separates Produkt-Repo über Konfiguration; wiederverwendete Fähigkeiten und nötige Anpassungen konkret gezeigt. / Existing Factory addresses separate new product through config; reused capabilities and required adaptations identified. | Konfiguration, Code, Repo-Verweise / Config, code, repos |
| A2 | 10 | Agentischer Produktbeitrag / Agent product contribution | Realer Provider-/LLM- und Tool-Lauf erzeugt substanziellen Python-Produktcode oder anwendbaren Patch; manueller Anteil markiert. / Real provider/LLM and tool run produces substantial Python product code or applicable patch; manual work identified. | Trace, Produktdiff / Trace, product diff |
| A3 | 10 | Zusammenarbeit und Freigabe / Cooperation and approval | Zwei Fähigkeiten übergeben strukturierte Daten; Ergebnis mit ausgeführten Produktchecks und konkreter menschlicher Entscheidung verbunden, Schleifen begrenzt. / Two capabilities exchange structured data; output linked to executed product checks and concrete human decision, loops bounded. | State, Trace, Gate / State, trace, gate |
| A4 | 10 | Kundentrennung / Customer isolation | Projektzuordnung und Produkt-Schreibbereich technisch begrenzt; eigener ausgeführter Factory-Test zeigt keine Nordwerk-Änderung durch HansePack-Auftrag. / Project assignment/product write scope technically bounded; executed own Factory test shows no Nordwerk change from HansePack task. | Factory-Test, Status/Diff / Factory test, status/diff |
| B1 | 5 | Deterministische Produktlogik / Deterministic product logic | Python berechnet Preise ohne LLM und verwendet verbindlichen Katalog; Produkt unabhängig aufrufbar. / Python calculates without LLM using binding catalogue; product independently invocable. | Fachcode, Startnachweis / Logic, startup |
| B2 | 5 | Einfachfall Q01 / Basic Q01 | Vollständige Positionswerte und Summen Q01 unter HP-V1 korrekt, automatisch gegen Kundenwerte geprüft. / Full Q01 line values/totals correct under HP-V1, automatically checked against customer values. | Produkttest, Ergebnis / Product test, result |
| B3 | 5 | Rabattfall Q03 / Discount Q03 | Listenbetrag, 5%-Rabatt, Warenwert, Versand und Gesamt Q03 korrekt, automatisch geprüft. / Q03 list, 5% discount, goods net, shipping and total correct and automatically checked. | Produkttest, Ergebnis / Product test, result |
| B4 | 5 | Ungültige Menge E01 / Invalid E01 | Menge 0 wird in Python-Fachlogik zurückgewiesen; Fehler statt gültigem Angebot; automatisierter Test. / Python business logic rejects quantity 0; error instead of valid quote; automated test. | Validierung, Test / Validation, test |
| B5 | 5 | Produktstart und Altprodukt / Product startup and previous product | Neuer Produkt-Start-/Testaufruf dokumentiert; Nordwerk-Commit gesichert und separat startbar, Dateistand unverändert. / New product start/test commands documented; Nordwerk commit frozen and separately runnable, file state unchanged. | READMEs, Commit/Status, Startbeleg / READMEs, commit/status, startup |
| B6 | 5 | Kundenauftrag verstanden / Commission understood | Kunden-Issue benennt Tagesumfang, unabhängige Fixtures, Fragen/Annahmen und benannte Verantwortung; kein erfundener Zusatzumfang. / Issue identifies daily scope, independent fixtures, questions/assumptions and accountability; no invented extra scope. | Issue, Fixtures / Issue, fixtures |
| C1 | 5 | Run-Evidenz / Run evidence | Run-ID, Projekt, tatsächliche Eingabe-/Ergebnis-/Factory-Commits, Modell/Einstellungen, Tests und Reviewer verknüpft. / Run ID, project, actual input/output/Factory commits, model/settings, tests and reviewer linked. | Runmanifest, Index / Manifest, index |
| C2 | 5 | Vollständige Messung / Complete measurement | Menschliche Zeit exklusiv kategorisiert; Agenten-/CI-Fehlläufe enthalten, unbekannte Werte markiert; Kostenrechnung konsistent. / Human time assigned exclusively; failed agent/CI runs included, unknown values marked; calculation consistent. | Zeit-/Nutzungsdaten / Time/usage records |
| C3 | 5 | Planung / Planning | Lieferplan T6/T7, T8-Reserve und tatsächlicher Projektstartaufwand dokumentiert; Factory-Entwicklung getrennt. / S6/S7 plan, S8 reserve and actual project-start effort recorded; Factory development separate. | Budget, Zeitdaten / Budget, time records |
| C4 | 5 | Reuse-Lernen / Reuse learning | Konkreter wiederverwendeter Teil und kundenspezifischer Aufwand mit Belegen sowie eine überprüfbare Schwäche benannt; keine unbelegte Kausalbehauptung. / Evidenced reused component and customer-specific effort plus testable weakness; no unsupported causal claim. | Kurze Analyse mit Verweisen / Short referenced analysis |
| D1 | 5 | Menschliche Verantwortung / Human accountability | Benannte Person prüft Produktdiff/Fachresultat und entscheidet über konkreten Ergebnisstand. / Named person reviews product diff/business result and decides on specific output. | Review/Gate / Review/gate |
| D2 | 5 | Tagesübergabe / Daily handover | Session-06-Index erreichbar, beide Produkte und Factory zuordenbar, Tests/Run/Kosten und höchstens drei nächste Schritte verlinkt. / Accessible session-06 index identifies both products/Factory and links checks/run/costs, at most three next actions. | evidence/session-06.md |

**A Factory 40 · B Kundenprodukt / Customer product 30 · C Messung und Lernen / Measurement and learning 20 · D Verantwortung und Übergabe / Accountability and handover 10 = 100.**

## Vier Lernziele / Four objectives

| Lernziel / Objective | Mindestpunkte / Required scores | Zusatzbedingungen / Additional conditions |
|---|---|---|
| L6.1 | A1 = 10; A4 ≥ 5; B5 = 5 | Zwingend: neues adressiertes Kunden-Repo und unverändertes separat startbares Nordwerk. / Mandatory: addressed new customer repo and unchanged separately runnable Nordwerk. |
| L6.2 | A2 = 10; A3 = 10 | Realer Code-/Patchbeitrag, zwei Fähigkeiten und konkrete menschliche Entscheidung vollständig belegt. / Full evidence of real code/patch contribution, two capabilities and human decision. |
| L6.3 | B2 = 5; B3 = 5; B4 = 5 | Drei eigene ausgeführte Prüfungen gegen unveränderte Kundenwerte. / Three executed own checks against unchanged customer expectations. |
| L6.4 | C1, C2, C3, C4 jeweils / each ≥ 3 | Zusätzlich echter Projektstartaufwand und belegte Wiederverwendung benannt. / Additionally actual project-start effort and evidenced reuse identified. |

## Abgrenzung / Scope

T6 verlangt keine vollständige Weboberfläche, keinen Export, keine vollständige Q-/E-Suite und kein Optimierungsexperiment. / S6 does not require full web UI, export, complete Q/E suite or optimisation experiment.

## Bewertungsprotokoll / Assessment record

Team, Termin, tatsächliche Factory-/Produkt-Commits; je Kriterium Punkte, Fundstelle und beobachtet/unbekannt; A–D und Gesamtsumme; je Lernziel Status/Begründung; Gesamttagesziel; Stärken, kritische Befunde und höchstens drei nächste Schritte. / Team, session, actual Factory/product commits; per criterion score, reference and observed/unknown; A–D/total; each objective status/reason; overall daily target; strengths, critical findings and at most three next actions.

Automatische Checks unterstützen die Bewertung. Gezielter menschlicher Review bleibt für reale Beiträge, UI-Nutzbarkeit, Kundenstatus und empirische Interpretation nötig. / Automated checks support assessment. Targeted human review remains necessary for real contributions, UI usability, customer status and empirical interpretation.
