# Bewertungsraster Termin 3 / Assessment rubric Session 3

**Erster nachgewiesener Factory-Durchlauf / First evidenced Factory run**

Verbindliche Aufgaben / Required tasks: [DE](Aufgabenblatt_Termin_03_de.md) · [EN](Task_Sheet_Session_03_en.md)

## Einheitliche Anwendung / Consistent use

**Unbenotetes Projekt: 100 Punkte als formatives Feedback, keine Note. / Ungraded project: 100 points for formative feedback, not a grade.**

Bewertet den Stand des jeweiligen Tages einschließlich weiterverwendeter Teamleistungen. Starter-Code, Starter-Tests und unveränderte Vorlagen sind keine eigene Leistung. Kein Bonus für Agentenzahl, Autonomie, Frameworks, Codeumfang oder optische Effekte. Menschliche Umsetzung ist zulässig; sie ersetzt keinen geforderten Factory-Nachweis. Keine rückwirkende Anforderung späterer Termine. / Assess the current daily state including reused team work. Supplied code/tests and unchanged templates are not student achievements. No bonus for agent count, autonomy, frameworks, code volume or visual effects. Human implementation is allowed but cannot replace required Factory evidence. Do not apply future requirements early.

**Punkte je Kriterium / Per-criterion scoring:**

| Maximum | Voll / Full | Teilweise / Partial | Fehlend / Absent |
|---:|---:|---:|---:|
| 10 | 10 | 5 | 0 |
| 5 | 5 | 3 | 0 |

Voll: alle genannten Merkmale durch passende Evidenz belegt. Teilweise: ein sinnvoller Kern ist belegt, aber ein ausdrücklich benanntes Merkmal fehlt oder ist unvollständig. Fehlend: kein belastbarer Kernnachweis, reine Behauptung oder widersprechende Ausführung. Teilpunkte konkret begründen; keine frei interpolierten Zwischenwerte. / Full: all listed features evidenced. Partial: meaningful core evidenced but a specifically identified feature is missing or incomplete. Absent: no reliable core evidence, assertion alone or contradictory execution. Explain partial credit; do not interpolate other scores.

Ein Live-Run ist nicht bei jeder Bewertung nötig: verknüpfte Traces, Commit-Diff und Prüfergebnisse können genügen. Tests mit Mock-LLM belegen deterministische Logik, keinen realen Modelllauf. Unzugängliche oder nicht ausführbare Evidenz als **unbekannt / unknown** markieren und vorläufig nur belegte Punkte vergeben; kein erfundenes Bestehen oder technisches Scheitern. Ein negativer Test ist nur dann positiv als Testleistung zu werten, wenn das erwartete Scheitern korrekt erkannt wird. / A live rerun is not always necessary: linked traces, commit diffs and check results can suffice. Mock-LLM tests establish deterministic logic, not a real model run. Mark inaccessible/unexecutable evidence unknown and award provisional points only for demonstrated evidence; do not invent success or failure. A negative test counts positively only when the expected failure is detected correctly.

## Ergebnisdarstellung / Reporting

| Gesamt / Total | Interpretation |
|---:|---|
| 85–100 | Sehr starker Tagesstand / Strong daily result |
| 70–84 | Solider Tagesstand / Solid daily result |
| 55–69 | Teilweise erreicht / Partially achieved |
| 0–54 | Wesentliche Lücken / Major gaps |

**Der Punktestand allein entscheidet nicht über die Factory-Lernziele.** Je Lernziel ausgeben: `erreicht / achieved`, `teilweise / partial`, `nicht erreicht / not achieved` oder `unbekannt / unknown`, mit Evidenz. Die nachfolgende Matrix definiert „erreicht“. „Teilweise“ bedeutet belegter Teilfortschritt unter diesen Bedingungen; „nicht erreicht“ bedeutet fehlendes Verhalten bei prüfbarer Evidenz. Unbekannt bleibt offen und wird nicht als erreicht gezählt. / **The score alone does not determine Factory learning outcomes.** Report each objective as achieved, partial, not achieved or unknown, with evidence. The matrix below defines achieved. Partial means demonstrated progress below those conditions; not achieved means missing behaviour with inspectable evidence. Unknown remains open and does not count as achieved.

**Tagesziel insgesamt erreicht / Overall daily target achieved:** mindestens 70/100, A mindestens 28/40, C mindestens 10/20 und alle vier Lernziele erreicht. Sonst „teilweise“ bei belegtem Teilfortschritt oder „nicht erreicht“ ohne solchen; bei entscheidender unbekannter Evidenz „offen“. Die Einzelwerte bleiben sichtbar; keine verdeckten Punktabzüge oder zusätzlichen Caps. / At least 70/100, A at least 28/40, C at least 10/20 and all four objectives achieved. Otherwise partial if progress is evidenced, not achieved if it is not; pending if decisive evidence is unknown. Keep raw scores visible; no hidden deductions or extra caps.

Committed Secrets als kritischen Befund nennen und konkrete Abhilfe verlangen; daraus keine hypothetischen zusätzlichen Bewertungsregeln erfinden. / Report committed secrets as a critical finding requiring remediation; do not invent extra hypothetical scoring rules.

## Kriterien / Criteria

| ID | Max. | Kriterium / Criterion | Vollständiger Nachweis / Full evidence | Fundstelle / Evidence source |
|---|---:|---|---|---|
| A1 | 10 | Trennung und Adressierung / Separation and addressing | Zwei Repos; konfigurierter Produkt-Checkout/Projektkennung; Factory-Code bleibt zentral. / Two repos; configured product checkout/project ID; Factory code stays central. | Repo-Struktur, Konfiguration, Run-Input / Repo structure, config, run input |
| A2 | 10 | Echte agentische Produktarbeit / Real agentic product work | Realer LLM-Aufruf über Provider, reales Tool und agentisch geänderte Produktdatei oder anwendbarer Patch; Ergebnis zuordenbar. / Real LLM through provider, real tool and agent-edited product file or applicable patch; attributable result. | Trace plus Produkt-Diff/Patch / Trace plus product diff/patch |
| A3 | 10 | Technische Zusammenarbeit / Technical cooperation | Mindestens zwei Agentenfähigkeiten tauschen strukturierte Daten tatsächlich aus; Task, Übergabe und Artefakt verknüpft. / At least two agent capabilities actually exchange structured data; task, handover and artifact linked. | State/Schema, Code, Trace / State/schema, code, trace |
| A4 | 10 | Kontrollierter Ablauf / Controlled workflow | Menschliches Gate entscheidet über konkreten Stand; Schleifenlimit/Eskalation und zulässiger Produkt-Arbeitsbereich implementiert. / Human gate decides on a specific version; loop limit/escalation and allowed product workspace implemented. | Gate-Entscheidung, Workflow/Tool-Code / Gate decision, workflow/tool code |
| B1 | 5 | Identität / Identity | AC-01 sichtbar erfüllt. / AC-01 visibly met. | Produktstand, Review / Product version, review |
| B2 | 5 | Erste Leistung / First service | Eine Leistung aus AC-02 einschließlich zugehörigem Pflichttext vorhanden. / One AC-02 service with its required description. | Produktstand / Product version |
| B3 | 5 | Kontakt und Übungshinweis / Contact and notice | AC-04 vollständig erfüllt. / AC-04 fully met. | Linkziel, sichtbarer Hinweis / Link target, visible notice |
| B4 | 5 | Eigener Produktcheck / Own product check | Sinnvoller automatisierter Check prüft einen Tagesinhalt/ein Linkziel und ist erfolgreich ausführbar; sichtbares Ergebnis zusätzlich menschlich geprüft. / Meaningful automated check verifies daily content/link target and runs successfully; visible output also human-reviewed. | Testcode, Ergebnis, Prüfer / Test code, result, reviewer |
| B5 | 5 | Unabhängiger Start / Independent startup | Kleiner Website-Stand ohne Factory-Prozess vorführbar; Start und separater Produkttest dokumentiert. / Small website demonstrable without a Factory process; startup and separate product test documented. | README, Startnachweis / README, startup evidence |
| B6 | 5 | Scope und Kunden-Task / Scope and customer task | Task referenziert Tageskriterien, Pflichtinhalte und explizite Annahmen/Klärungen; keine erfundenen Kundenversprechen. / Task refers to daily criteria, required content and explicit assumptions/clarifications; no invented promises. | Issue, AC-Prüfliste / Issue, AC checklist |
| C1 | 5 | Run-Zuordnung / Run linkage | Eindeutige Run-ID; Eingabe-/Ergebnis-/Factory-Commit, Task, Modell und Ergebnisse verknüpft; keine überschriebenen Logs. / Unique run ID; input/output/Factory commits, task, model and results linked; no overwritten logs. | Manifest, Trace / Manifest, trace |
| C2 | 5 | Vollständiger Aufwand / Complete effort | Menschliche Kategorien, Agenten-/CI-Daten, Review, Nacharbeit und Fehlläufe erfasst; Unbekanntes transparent. / Human categories, agent/CI data, review, rework and failures recorded; unknowns transparent. | Nutzungsdaten, Zeitdaten / Usage and time records |
| C3 | 5 | Planung und Berechnung / Planning and calculation | Planbudget Lieferung und T5-Reserve begründet; Factory-Entwicklung getrennt; Credits konsistent berechnet. / Delivery plan budget and S5 reserve justified; Factory development separate; credits calculated consistently. | Kostenmodell, Rechnung, Planung / Cost model, calculation, plan |
| C4 | 5 | Lernhypothese / Learning hypothesis | Ein konkreter Engpass aus dem echten Lauf und überprüfbare Verbesserungshypothese mit erwarteter Messgröße. / Concrete bottleneck from the real run and testable improvement hypothesis with an intended measure. | Run-Beleg, kurze Hypothese / Run reference, short hypothesis |
| D1 | 5 | Verantwortung und eigene Factory-Prüfung / Accountability and own Factory check | Accountable humans benannt; Reviewentscheidungen zugeordnet; eigener sinnvoller Factory-Test besteht im Standardlauf. / Accountable humans named; review decisions attributed; own meaningful Factory test passes in standard run. | Rollen, Gate, pytest / Roles, gate, pytest |
| D2 | 5 | Nachvollziehbarer Tagesstand / Traceable daily state | Session-03-Index verlinkt beide Repos/Commits, Tasks/Runs, Beiträge und höchstens drei nächste Schritte. / Session-03 index links both repos/commits, tasks/runs, contributions and at most three next actions. | evidence/session-03.md |

**A Factory 40 · B Kundenprodukt / Customer product 30 · C Messung und Lernen / Measurement and learning 20 · D Verantwortung und Übergabe / Accountability and handover 10 = 100.**

## Lernzielentscheidung / Learning-objective decision

| Lernziel / Objective | Mindestwerte / Required scores | Zusätzlich zu prüfen / Additional checks |
|---|---|---|
| L3.1 | A1 mindestens 5 und B5 = 5 / A1 at least 5 and B5 = 5 | Zwei Repos und adressierter Produkt-Checkout belegt; kleiner Produktstand ohne Factory vorführbar. / Two repos and addressed checkout evidenced; small product runs without Factory. |
| L3.2 | A2 = 10 und A3 = 10 / A2 = 10 and A3 = 10 | Reale Modell-/Tool-Nutzung, agentischer Produktbeitrag und Zusammenarbeit zweier Fähigkeiten vollständig nachgewiesen. / Real model/tool use, agent product contribution and two-capability cooperation fully evidenced. |
| L3.3 | A4 mindestens 5 und B4 mindestens 3 / A4 at least 5 and B4 at least 3 | Zusätzlich zwingend: menschliche Entscheidung über konkreten Stand und ausgeführter Produktcheck. / Additionally mandatory: human decision on a specific version and an executed product check. |
| L3.4 | C1, C2 und C4 jeweils mindestens 3 / C1, C2 and C4 each at least 3 | Run, tatsächlicher Aufwand und beobachtungsbasierte Hypothese sind miteinander verknüpft. / Run, actual effort and observation-based hypothesis are linked. |

## Abgrenzung / Scope boundary

Noch nicht verlangen / Not due yet: AC-02 vollständig, AC-03/05–08 vollständig, Englisch, Sicherheitsantwort, Vorher-Nachher-Experiment. / Full AC-02, full AC-03/05–08, English view, security response or before/after experiment.

## Kurzes Bewertungsprotokoll / Short assessment record

1. Team, Termin/Session, Factory- und Produkt-Commit / Factory and product commit.
2. Je Kriterium Punkte, Status beobachtet/unbekannt und konkrete Datei/Run/PR als Beleg / Per criterion: score, observed/unknown status and specific file/run/PR.
3. A–D-Summen und Gesamt / A–D subtotals and total.
4. Je Lernziel Status, Beleg und gegebenenfalls genau die fehlende Bedingung / Per objective: status, evidence and exact unmet condition if any.
5. Tagesziel erreicht/teilweise/nicht erreicht/offen, Stärken, kritische Befunde und höchstens drei nächste Schritte / Overall achieved/partial/not achieved/pending, strengths, critical findings and at most three next actions.

Automatisierte Checks unterstützen die Bewertung; sichtbare Nutzbarkeit, Kundenentscheidung, Sicherheitsargumentation und ehrliche Interpretation erfordern gezielten menschlichen Review. / Automated checks support assessment; visible usability, customer decisions, security reasoning and honest interpretation require targeted human review.
