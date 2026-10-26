# Bewertungsraster Termin 4 / Assessment rubric Session 4

**Wiederholbare Lieferung und wirksame Qualitätsgates / Repeatable delivery and effective quality gates**

Verbindliche Aufgaben / Required tasks: [DE](Aufgabenblatt_Termin_04_de.md) · [EN](Task_Sheet_Session_04_en.md)

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
| A1 | 10 | Factory wiederverwenden / Reuse the Factory | Weiterer echter Kunden-Task nutzt dieselbe zentrale Factory und konfigurierte Produktzuordnung; keine eingebettete Factory im Produkt. / Another real customer task uses the same central Factory and configured product assignment; no embedded Factory in product. | Zwei Tagesstände, Konfiguration / Daily versions, config |
| A2 | 10 | Realer Folgelauf / Real subsequent run | Mindestens zwei kooperierende Fähigkeiten, realer LLM-/Tool-Einsatz, substanzieller agentischer Produktdiff und Human Gate im neuen Task belegt. / New task evidences two cooperating capabilities, real LLM/tool use, substantial agent product diff and human gate. | Trace, Diff, Entscheidung / Trace, diff, decision |
| A3 | 10 | Wirksames Qualitätsgate / Effective quality gate | Produktergebnisse gehen technisch in Freigabe/Korrektur ein; kontrollierter Kontakt-/Linkfehler wird erkannt und blockiert, Korrektur besteht. / Product results technically drive approval/correction; controlled contact/link fault is detected and blocked, corrected version passes. | Negativ-/Positivlauf, Gate-State / Negative/positive run, gate state |
| A4 | 10 | Factory-Tests und Begrenzung / Factory tests and bounds | Eigene Tests für positiven und abgelehnten/eskalierten Gate-Zustand bestehen; Schleifen und Produkt-Schreibbereich begrenzt. / Own tests for positive and rejected/escalated gate states pass; loops and product write scope bounded. | pytest, Workflow/Tool-Code / pytest, workflow/tool code |
| B1 | 5 | Inhalte / Content | AC-01–03 vollständig erfüllt. / AC-01–03 fully met. | Produkt, AC-Prüfliste / Product, AC checklist |
| B2 | 5 | Kontakt und Navigation / Contact and navigation | AC-04–05 vollständig erfüllt. / AC-04–05 fully met. | Produkt, Linkprüfung / Product, link checks |
| B3 | 5 | Responsive Nutzung / Responsive use | AC-06 an beiden Breiten tatsächlich geprüft. / AC-06 actually checked at both widths. | Browserreview mit Breiten/Prüfer / Browser review with widths/reviewer |
| B4 | 5 | Bedienbarkeit / Usability | AC-07 geprüft, einschließlich Tastaturfokus und Bildalternativen soweit anwendbar. / AC-07 checked, including keyboard focus and image alternatives where applicable. | Browserreview, Markup / Browser review, markup |
| B5 | 5 | Eigenständiger Candidate / Independent candidate | AC-08 belegt: frischer Checkout, dokumentierter Start und separate Tests ohne Factory; Candidate eindeutig versioniert. / AC-08 evidenced: fresh checkout, documented startup and separate tests without Factory; candidate clearly versioned. | Commit/Tag, Startnachweis / Commit/tag, startup record |
| B6 | 5 | Automatisierte Produktprüfung / Automated product checks | Drei verschiedene Prüffamilien Inhalt, Kontakt/Navigation, lokale Verweise/Assets prüfen echte Anforderungen und bestehen am Candidate. / Three distinct families check content, contact/navigation, local references/assets against real requirements and pass on candidate. | Testcode und Ergebnis / Test code and result |
| C1 | 5 | Baseline reproduzierbar / Reproducible baseline | R-01 auf R-BASE mit F-BASE ausgeführt; Modell/Einstellungen, Input/Output, Prüfkriterien, Run-IDs und getrennte Versuchsausgabe festgehalten. / R-01 executed on R-BASE with F-BASE; model/settings, input/output, criteria, run IDs and isolated output recorded. | Versuchsmanifest, Rohdaten / Experiment manifest, raw records |
| C2 | 5 | Kosten und Planabweichung / Costs and deviation | Tageskosten inklusive manueller Beiträge/Review/Nacharbeit und Fehlläufe; Factory-Entwicklung separat; Planabweichung erklärt. / Daily costs include manual contributions/review/rework and failures; Factory development separate; plan deviation explained. | Kosten-/Zeitdaten / Cost/time records |
| C3 | 5 | Baseline-Messwerte / Baseline measurements | R-01-Akzeptanz/Regressionen, Review-/Nacharbeitszeit und bekannte Kosten gemessen; Unbekanntes markiert. / R-01 acceptance/regressions, review/rework time and known costs measured; unknowns marked. | Messdaten und Prüfergebnis / Measurements and check result |
| C4 | 5 | Gezielte Verbesserung geplant / Targeted improvement planned | Ein belegter Engpass, konkrete geplante Factory-Änderung, erwarteter Effekt und Messkriterium; Baseline vor dieser Änderung gesichert. / Evidenced bottleneck, specific planned Factory change, expected effect and measure; baseline saved before that change. | Hypothese, Versionsfolge / Hypothesis, version sequence |
| D1 | 5 | Review und Zuständigkeit / Review and accountability | Lieferdiff/PR durch benannten Menschen geprüft; Freigabe unterscheidet Candidate und Testfehlerstand. / Delivery diff/PR reviewed by named human; approval distinguishes candidate and fault-test version. | PR/Diff, Freigabe / PR/diff, approval |
| D2 | 5 | Nachvollziehbarer Tagesstand / Traceable daily state | Session-04-Index verlinkt Repos/Commits, Runs, ACs, Fehlernachweis und R-01; höchstens drei nächste Schritte. / Session-04 index links repos/commits, runs, ACs, fault evidence and R-01; at most three next actions. | evidence/session-04.md |

**A Factory 40 · B Kundenprodukt / Customer product 30 · C Messung und Lernen / Measurement and learning 20 · D Verantwortung und Übergabe / Accountability and handover 10 = 100.**

## Lernzielentscheidung / Learning-objective decision

| Lernziel / Objective | Mindestwerte / Required scores | Zusätzlich zu prüfen / Additional checks |
|---|---|---|
| L4.1 | A1 = 10 und A2 = 10 / A1 = 10 and A2 = 10 | Weiterer echter Produkt-Task durch wiederverwendete Factory vollständig belegt. / Another real product task through the reused Factory fully evidenced. |
| L4.2 | A3 mindestens 5 und D1 = 5 / A3 at least 5 and D1 = 5 | Zusätzlich zwingend: ausgeführte Tests beeinflussen Gate und ein Mensch entscheidet am konkreten Candidate. / Additionally mandatory: executed checks affect the gate and a human decides on the specific candidate. |
| L4.3 | A3 = 10 und A4 mindestens 5 / A3 = 10 and A4 at least 5 | Erkennen, Zurückhalten und erfolgreiche Korrektur des kontrollierten Fehlers belegt. / Detection, blocking and successful correction of the controlled fault evidenced. |
| L4.4 | C1 = 5, C3 mindestens 3 und C4 mindestens 3 / C1 = 5, C3 at least 3 and C4 at least 3 | Baseline technisch reproduzierbar, Messung vorhanden und geplante Änderung zeitlich danach. / Baseline technically reproducible, measurements available and planned change subsequent to it. |

## Abgrenzung / Scope boundary

Noch nicht verlangen / Not due yet: CR-01, SR-01, endgültige Kundenabnahme oder positiver Optimierungseffekt. / CR-01, SR-01, final customer acceptance or a positive optimisation effect.

## Kurzes Bewertungsprotokoll / Short assessment record

1. Team, Termin/Session, Factory- und Produkt-Commit / Factory and product commit.
2. Je Kriterium Punkte, Status beobachtet/unbekannt und konkrete Datei/Run/PR als Beleg / Per criterion: score, observed/unknown status and specific file/run/PR.
3. A–D-Summen und Gesamt / A–D subtotals and total.
4. Je Lernziel Status, Beleg und gegebenenfalls genau die fehlende Bedingung / Per objective: status, evidence and exact unmet condition if any.
5. Tagesziel erreicht/teilweise/nicht erreicht/offen, Stärken, kritische Befunde und höchstens drei nächste Schritte / Overall achieved/partial/not achieved/pending, strengths, critical findings and at most three next actions.

Automatisierte Checks unterstützen die Bewertung; sichtbare Nutzbarkeit, Kundenentscheidung, Sicherheitsargumentation und ehrliche Interpretation erfordern gezielten menschlichen Review. / Automated checks support assessment; visible usability, customer decisions, security reasoning and honest interpretation require targeted human review.
