# Bewertungsraster Termin 5 / Assessment rubric Session 5

**Änderungsfähigkeit und empirisches Factory-Lernen / Change delivery and empirical Factory learning**

Verbindliche Aufgaben / Required tasks: [DE](Aufgabenblatt_Termin_05_de.md) · [EN](Task_Sheet_Session_05_en.md)

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
| A1 | 10 | Versionierte Änderung / Versioned change | CR-01 ausgehend vom T4-Candidate adressiert; gleiche zentrale Factory, strukturiertes Änderungstask und bestehender Produktkontext. / CR-01 starts from the S4 candidate; same central Factory, structured change task and existing product context. | Input-Commit, Issue, Konfiguration / Input commit, issue, config |
| A2 | 10 | Agentischer Änderungsbeitrag / Agent change contribution | CR-01 enthält echten LLM-/Tool-Lauf mit mindestens zwei kooperierenden Fähigkeiten, agentischem Produktdiff und dokumentierten menschlichen Eingriffen. / CR-01 includes real LLM/tool run with two cooperating capabilities, agent product diff and recorded human interventions. | Trace, Diff, Beiträge / Trace, diff, contributions |
| A3 | 10 | Regression und Freigabe / Regression and approval | Neue Kriterien und AC-01–08 prüfen konkreten Release; Testergebnisse beeinflussen Gate; menschliche Freigabe oder begründetes Zurückhalten. / New criteria and AC-01–08 check the specific release; results influence gate; human approves or justifiably withholds it. | Prüfung, Gate-State, Review / Checks, gate state, review |
| A4 | 10 | Gezielte Factory-Änderung / Targeted Factory change | Begründete Verbesserung in Factory implementiert, sinnvoll getestet, als F-NEW versioniert und auf R-01 tatsächlich ausgeführt; keine gleichzeitige unkontrollierte Modelländerung. / Justified improvement implemented in Factory, meaningfully tested, versioned as F-NEW and actually run on R-01; no simultaneous uncontrolled model change. | Factory-Diff, Test, Experiment-Run / Factory diff, test, experiment run |
| B1 | 5 | Englischer Einstieg / English entry | Vorgegebener englischer Inhalt aus CR-01 vollständig, passende Sprache/Titel. / All required English CR-01 content, appropriate language/title. | Produkt, automatisierte Checks / Product, automated checks |
| B2 | 5 | Zielgruppe und Sprachwechsel / Audience and language switching | Zusätzliche deutsche Zielgruppe, Sprachwechsel und korrekter Kontakt in beiden Ansichten. / Additional German audience, language switching and correct contact in both views. | Produkt, Links / Product, links |
| B3 | 5 | Erhalt des Bestands / Preserve existing behaviour | AC-01–08 weiterhin erfüllt, automatische Regression und erneutes Browser-/Tastaturreview durchgeführt. / AC-01–08 still met, automated regression and repeated browser/keyboard review performed. | Tests, Review / Tests, review |
| B4 | 5 | Komponentenübersicht / Component inventory | Eigene Laufzeit- und Build-/Testkomponenten mit Version/Bezugsstand oder Nichtverwendung getrennt vom unsicheren Altsystem erfasst. / Own runtime and build/test components with version/reference or non-use distinguished from the uncertain old system. | Inventar / Inventory |
| B5 | 5 | Sicherheitsantwort / Security response | SR-01 beantwortet bekannte/unklare Betroffenheit, Hoster-Rückfragen, angemessene Optionen, Funktionsverlust und Wartung; Primärquelle/Datum, keine unbelegte Sicherheitsgarantie. / SR-01 addresses known/unknown exposure, host questions, appropriate options, lost functionality and maintenance; primary source/date, no unsupported guarantee. | Kundenantwort mit Quellen / Customer response with sources |
| B6 | 5 | Übergabefähiger Release / Handover-ready release | Release eindeutig versioniert, unabhängig start-/testbar, Wartungshinweis und Abnahmestatus mit Restmängeln bzw. offener Kundenentscheidung korrekt. / Release clearly versioned, independently runnable/testable, maintenance note and accurate acceptance status with defects or pending customer decision. | Release, Anleitung, Protokoll / Release, instructions, record |
| C1 | 5 | Vergleichbarkeit / Comparability | Vorher/nachher auf demselben R-BASE, identischem R-01 und Kriterien, gleichem Modell und dokumentierten Einstellungen; getrennte Runs ohne Lösungsübernahme. / Before/after use same R-BASE, R-01 and criteria, same model and recorded settings; isolated runs without solution leakage. | Versuchsmanifest, Inputstände / Experiment manifest, input versions |
| C2 | 5 | Messwerte und Rohdaten / Measurements and raw records | Mindestens ein vollständiger Lauf je Variante mit Akzeptanz/Regression, Review-/Nacharbeitszeit, Fehlern und bekannten Kosten; fehlende Tokens transparent. / At least one full run per variant with acceptance/regression, review/rework time, faults and known costs; missing tokens transparent. | Rohdaten, Läufe, Prüfergebnisse / Raw records, runs, checks |
| C3 | 5 | Empirische Entscheidung / Empirical decision | Ergebnis inklusive Streuungs-/Stichprobenlimits interpretiert; beibehalten/anpassen/zurücknehmen begründet; kein Zwang zum positiven Effekt. / Result interpreted with variability/sample limits; retaining/adapting/reverting justified; no positive effect required. | Kurze Auswertung / Short analysis |
| C4 | 5 | Gesamtkosten und Übertragbarkeit / Total costs and transfer | T3–5-Bilanz ohne doppelte Stunden, Fehlläufe enthalten, Factory-Entwicklung separat, Budgetabweichung und drei belegte übertragbare Erkenntnisse. / S3–5 totals without duplicate hours, including failures, Factory development separate, budget deviation and three evidenced transferable lessons. | Bilanz, Lernpunkte / Totals, lessons |
| D1 | 5 | Verantwortete Freigaben / Accountable approvals | Benannte Menschen prüfen Produkt und Sicherheitsfakten; technische Freigabe und tatsächliche Kundenentscheidung klar unterschieden. / Named humans review product and security facts; technical approval and actual customer decision clearly distinguished. | Review-/Abnahmeprotokoll / Review/acceptance record |
| D2 | 5 | Nachvollziehbarer Abschluss / Traceable closure | Session-05-Index verlinkt Repos/Commits, Kundenänderung, Runs, Vergleich und Übergabe; offene Aufgaben sichtbar. / Session-05 index links repos/commits, change, runs, comparison and handover; open tasks visible. | evidence/session-05.md |

**A Factory 40 · B Kundenprodukt / Customer product 30 · C Messung und Lernen / Measurement and learning 20 · D Verantwortung und Übergabe / Accountability and handover 10 = 100.**

## Lernzielentscheidung / Learning-objective decision

| Lernziel / Objective | Mindestwerte / Required scores | Zusätzlich zu prüfen / Additional checks |
|---|---|---|
| L5.1 | A1 = 10, A2 = 10 und A3 mindestens 5 / A1 = 10, A2 = 10 and A3 at least 5 | Reale versionierte Kundenänderung durch dieselbe Factory mit Prüf-/Freigabeschritt belegt. / Real versioned customer change through the same Factory with check/approval step evidenced. |
| L5.2 | A4 mindestens 5, C1 = 5, C2 = 5 und C3 mindestens 3 / A4 at least 5, C1 = 5, C2 = 5 and C3 at least 3 | Implementierte Änderung und vergleichbarer ehrlicher Versuch; kein positiver Effekt vorausgesetzt. / Implemented change and comparable honest experiment; no positive effect required. |
| L5.3 | B4 mindestens 3, B5 = 5 und D1 mindestens 3 / B4 at least 3, B5 = 5 and D1 at least 3 | Zusätzlich zwingend: menschlich geprüfte Sicherheitsfakten und keine unbelegte Betroffenheits-/Sicherheitsgarantie. / Additionally mandatory: human-checked security facts and no unsupported exposure/security guarantee. |
| L5.4 | B6 = 5, C4 mindestens 3 und D2 mindestens 3 / B6 = 5, C4 at least 3 and D2 at least 3 | Übergabe und wahrer Abnahmestatus, Gesamtaufwand und wiederverwendbare Erkenntnisse belegt. Eine dokumentiert ausstehende Kundenentscheidung ist zulässig. / Handover and true acceptance status, total effort and reusable lessons evidenced. A documented pending customer decision is acceptable. |

## Abgrenzung / Scope boundary

Nicht verlangen / Not required: positiver Optimierungseffekt, volle Autonomie, komplette englische Detailübersetzung, Live-Exploit, öffentliche Bereitstellung, tatsächliche Euro-Rentabilität. / Positive optimisation effect, full autonomy, full English translation, live exploit, public deployment or actual euro profitability.

## Kurzes Bewertungsprotokoll / Short assessment record

1. Team, Termin/Session, Factory- und Produkt-Commit / Factory and product commit.
2. Je Kriterium Punkte, Status beobachtet/unbekannt und konkrete Datei/Run/PR als Beleg / Per criterion: score, observed/unknown status and specific file/run/PR.
3. A–D-Summen und Gesamt / A–D subtotals and total.
4. Je Lernziel Status, Beleg und gegebenenfalls genau die fehlende Bedingung / Per objective: status, evidence and exact unmet condition if any.
5. Tagesziel erreicht/teilweise/nicht erreicht/offen, Stärken, kritische Befunde und höchstens drei nächste Schritte / Overall achieved/partial/not achieved/pending, strengths, critical findings and at most three next actions.

Automatisierte Checks unterstützen die Bewertung; sichtbare Nutzbarkeit, Kundenentscheidung, Sicherheitsargumentation und ehrliche Interpretation erfordern gezielten menschlichen Review. / Automated checks support assessment; visible usability, customer decisions, security reasoning and honest interpretation require targeted human review.
