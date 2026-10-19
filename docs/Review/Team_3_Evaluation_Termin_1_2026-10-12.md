# Team 3 – Evaluation nach Termin 1
**Firma:** PepeGroup  
**Team:** 6 Studierende  
**Termin:** 12. Oktober 2026  
**Bewertung erstellt:** 13. Oktober 2026  
**Status:** Vorläufiger Bewertungsvorschlag; Abgabezeitpunkt nicht verbindlich bestätigt, keine unabhängige Runtime-Verifikation.

## Ergebnis
**69/100 Punkte – Tagesziel teilweise erreicht.**

Das Team hat einen eigenen LangGraph-Cost-Agenten und drei eigene Tests erstellt, die Rollen vollständig zugeordnet und einen gut nachvollziehbaren Issue-/PR-Prozess aufgebaut. Es fehlen die für Termin 1 geforderten tatsächlichen Ausführungs- und Kostennachweise. Architektur und Firmenentscheidungen beschreiben noch nicht den tatsächlich implementierten Cost-Agenten.

Der Score ist ein Engineering Health Indicator, keine Note. 69 liegt unmittelbar unter der Tageszielspanne von 70–84; daraus folgt keine Aussage über eine fehlende technische Fähigkeit der Studierenden. Maßgeblich ist die vorliegende Repository-Evidenz.

## Snapshot und Methode
- Repository: https://github.com/BohdanBerlev/agentic_ai_peppe
- Baseline: `2685668b92bf5afb8a7886876ba00a6585057006` vom 07.10.2026; dieselbe Kursversion wie bei Teams 1 und 2.
- Vorläufiger Freeze: 12.10.2026, 15:00 Uhr Europe/Berlin.
- Bewerteter Commit: `c65485f3b7cf64e25eab779a2ccd033b494c708d` von 14:55:02 Uhr.
- Aktueller main-Commit bei Prüfung: `68ab9d24c7d7185888e4020aecfa2f539cc3f609` von 15:05:47 Uhr; enthält einen README-Nachtrag und wird separat eingeordnet.
- Delta: https://github.com/BohdanBerlev/agentic_ai_peppe/compare/2685668b92bf5afb8a7886876ba00a6585057006...c65485f3b7cf64e25eab779a2ccd033b494c708d
- Vollständiger rekursiver Dateibaum für den bewerteten SHA geprüft; nicht abgeschnitten.
- Angehängtes v3.2-Termin-1-Raster und dieselbe Bewertungslogik wie für Teams 1/2. Starterbeispiele, Startertests, pytest.ini und unveränderte Basis werden nicht als Eigenleistung gewertet.
- Git-Zeitstempel rekonstruieren die Historie, beweisen allein aber keinen Push-Zeitpunkt. Der Dozent hat noch keinen verbindlichen Abgabe-SHA bestätigt.
- Issues/PRs und Actions am 13.10. gelesen. Alle erfassten Issues/PRs wurden am 12.10. vor 15:00 Uhr angelegt. Historische Issue-Inhalte zum exakten Freeze nicht rekonstruiert.
- Keine Punkte für unnötige Komplexität, reine Anzahl an Agenten/Commits oder Dokumentationsumfang. Keine Termin-2-Anforderungen abgezogen.

## Punkteübersicht
| Bereich | Punkte | Maximum |
|---|---:|---:|
| A. Company & Roles | 17 | 20 |
| B. Technical Platform | 10 | 15 |
| C. First Own Agent | 31 | 35 |
| D. Testing & Evidence | 6 | 15 |
| E. Cost Measurement | 0 | 10 |
| F. Engineering Process | 5 | 5 |
| **Gesamt** | **69** | **100** |

## Einzelbewertung
| Kriterium | Punkte | Evidenz | Begründung |
|---|---:|---|---|
| A1 | 8/8 | organization/roles.yaml | Alle zwölf Rollen haben current_actor_type, target_actor_type und einen benannten accountable_human. |
| A2 | 4/6 | organization/roles.yaml; organization/company.md; src/agents/cost_agent.py | Plausibles Human-Agent-Zielbild, keine Schein-operational-Markierung. Zielakteure vielfach TBD; Architekturfreigabe laut company.md erforderlich, laut Rollenfeld false. Erste QA-Rolle passt nicht zur Cost-Implementierung. |
| A3 | 3/3 | organization/company.md | Rollenentscheidungen, übergreifende Teamentscheidungen, menschliche Freigabe, Eskalation und Budget-Stopp konkret beschrieben. Rollenwechsel können ergänzt werden. |
| A4 | 2/3 | organization/company.md | QA als erste Rolle begründet, Managing Director bewusst menschlich, Security/Release-Gate benannt. Tatsächlicher erster implementierter Agent ist Cost statt QA. |
| B1 | 4/4 | README.md, Team setup vor 15:00 | OS/Umgebung, Python, Ollama, Portabweichung 5433 und lokale Konfigurationsgrenzen dokumentiert. Referenzlauf ohne Trace transparent angegeben; Testbehauptung nicht unabhängig verifiziert. |
| B2 | 1/6 | docs/architecture.md; Baseline-Diff | Minimale Anpassung durch Entfernen von ICC-/LangSmith-Diagrammpfaden; kein konkreter Cost-Agent, kein Log-Lesetool und kein Human Gate. Abschnitt Team changes bleibt Template. |
| B3 | 3/3 | src/agents/cost_agent.py; Baseline-Diff | Provider-, Trace- und Plattformbasis sinnvoll wiederverwendet. Keine parallele Ersatzinfrastruktur im gewählten Snapshot. |
| B4 | 2/2 | Baseline-Diff; requirements.txt | Pflichtstack im gewählten Snapshot eingehalten; späterer oMLX-Nachtrag separat behandelt. |
| C1 | 15/15 | src/agents/cost_agent.py | Eigenständiger, plausibel ausführbarer StateGraph mit load_logs, analyze und bedingtem Fehlerende. Kein unabhängiger Lauf; benötigt vorhandene Eingabetraces. |
| C2 | 5/5 | src/agents/cost_agent.py | Echter llm.invoke-Aufruf über get_chat_model technisch nachvollziehbar. Live-Erfolg nicht unabhängig nachgewiesen. |
| C3 | 3/5 | src/agents/cost_agent.py; Snapshot-Dateibaum | Reales Dateilesetool implementiert; tatsächliche Nutzung in einem Agentenlauf mangels Trace nicht belegt. |
| C4 | 5/5 | src/agents/cost_agent.py | CostState als TypedDict und CostReport/CostInsight als Pydantic-Modelle definieren Input-State und Output. |
| C5 | 3/5 | src/agents/cost_agent.py | Fehlende Datei wird behandelt, ungültiges LLM-JSON führt zu unparseable, Graph terminiert. Unbegrenzte Dateipfade, ungesicherter LLM-Fehlerpfad und success-Trace auch bei unparseable begrenzen die Robustheit. |
| D1 | 4/6 | tests/test_cost_agent.py; pytest.ini | Drei eigene sinnvolle Tests für fehlende Datei sowie gültiges/ungültiges JSON. Standard-Erfassung plausibel, erfolgreicher vollständiger Testlauf ohne Protokoll/CI nicht bestätigt. Wie bei Team 1 vorläufig 4/6. |
| D2 | 0/5 | Vollständiger Snapshot-Dateibaum; logs/ | Nur logs/.gitkeep vorhanden; kein eigener Execution Trace. |
| D3 | 2/4 | src/agents/cost_agent.py; README.md | Modulaufruf möglich, Funktion nimmt Logpfad an. Default logs/agent-runs.jsonl fehlt; README erklärt keinen reproduzierbaren eigenen Lauf mit Eingabedaten. Keine CLI-Pfadoption. |
| E1 | 0/3 | costs/usage.csv | Nur Header, keine tatsächlichen Menschenstunden. |
| E2 | 0/4 | costs/usage.csv; Snapshot-Dateibaum | Keine tatsächlichen Agentennutzungsdaten gespeichert. Ein Cost-Agent allein ist kein Nutzungsnachweis. |
| E3 | 0/3 | costs/usage.csv; costs/cost-model.yaml; src/agents/cost_agent.py | Raten unverändert vorhanden, aber keine tatsächlichen Credits berechnet/dokumentiert. Eigener Agent loggt keine estimated_cost_credits seiner Analyse. |
| F1 | 3/3 | GitHub Issues #1–#7 | Sieben relevante echte Issues für bearbeitete bzw. zu bearbeitende Termin-1-Themen; Issues getrennt von PRs #8–#10. |
| F2 | 2/2 | Commit-Historie; PRs #8–#10 | Rollen, Firma, Setup und Code/Tests nachvollziehbar; PRs enthalten zuordenbare Änderungen, #8 verweist auf Issue #2. Keine Punkte für reine Anzahl. |

## Harte Caps
- Kein eigener Execution Trace: Gesamtscore höchstens 75.
- Keine tatsächlichen Nutzungsdaten, nur Cost-Template: Gesamtscore höchstens 75.
- Eigener Agent und eigene Tests sind vorhanden. Daher keine Caps für fehlenden Agenten, fehlende eigene Tests oder nur Starter plus Dokumentation.
- Kein fehlgeschlagener Standard-Testlauf nachgewiesen. Daher kein vorsorglicher 8/15-Cap für Testing & Evidence.

Die strengste nachgewiesene Gesamtkappung ist 75/100. Der Rohscore 69 liegt darunter; die Caps ändern den Score nicht. Es handelt sich um Obergrenzen, nicht um zusätzliche abzuziehende Strafpunkte.

## Fachliche Befunde
### Organisation gut angelegt, Ist-Zustand noch nicht synchronisiert
Alle sechs Teammitglieder sind im Firmendokument benannt. Verantwortlichkeit für alle zwölf Rollen ist vergeben. Besonders positiv: company.md stellt ausdrücklich klar, dass ein LLM-approved keine menschliche Freigabe ersetzt.

Es gibt allerdings Widersprüche:
- company.md nennt QA & Test als ersten Agenten, Code enthält Cost & Observability.
- company.md verlangt Architekturfreigabe und menschliche Ergebnisprüfung, während roles.yaml für Software Architect human_approval_required=false setzt.
- Die Cost-Rolle bleibt planned/human. Ohne echten Ausführungsnachweis ist planned konservativ und zulässig; der Status sollte nach einem belegten Lauf aktualisiert werden.
- Zielakteure bleiben oft TBD. Für A1 sind die verlangten Actor-Typen und accountable humans vollständig; für das konkrete Mixed-Team-Zielbild fehlt dennoch die Umsetzungsperspektive.

### Cost-Agent ist eine eigene technische Leistung
src/agents/cost_agent.py implementiert:
1. Einlesen einer JSONL-Datei über ein reales Tool.
2. Reduktion auf Agent, Status, Dauer, Tokens und bereits aufgezeichnete Credits.
3. Analyse mit LLM über die Starter-Provider-Abstraktion.
4. Pydantic-Validierung des Ergebnisses.
5. LangGraph-State und Fehlerabbruch bei nicht lesbarer Datei.
6. Schreiben eines Traces über die gemeinsame Hilfsfunktion.

Das ist ein sinnvoller eigener Agent und keine bloß umbenannte Starterdatei. Ein Cost-Agent kann grundsätzlich als erster Agent dienen; ein QA-Agent ist dafür nicht zwingend. Problematisch ist die Abweichung zwischen Entscheidung/Dokumentation und Implementierung.

### Der Cost-Agent ersetzt die Messpipeline noch nicht
Der Agent liest vorhandene Messdaten, aber im Snapshot gibt es keine Eingabetraces. Die voreingestellte Datei logs/agent-runs.jsonl fehlt. usage.csv enthält nur den Header.

Der eigene Trace enthält weder model noch estimated_cost_credits. Die Kosten der Analyse selbst werden somit nicht vollständig erfasst. Die Software besitzt Ansatzpunkte für Beobachtbarkeit, aber es gibt noch keinen abgegebenen Nutzungsnachweis.

Zählung, Summen und Credit-Berechnung sollten deterministisch aus validierten Datensätzen erfolgen. Das LLM kann Ergebnisse erklären und Optimierungsideen vorschlagen. Aktuell wird total_runs_analyzed vom LLM erzeugt und nicht mit der tatsächlichen Zahl eingelesener Datensätze abgeglichen.

### Konkrete Robustheits- und Sicherheitslücken
- read_log_file löst den Pfad auf, prüft jedoch nicht, ob er innerhalb des erlaubten Verzeichnisses liegt. Absolute Pfade und ../ können Dateien außerhalb des Repositories erreichen. Inhalte mit passenden JSON-Feldern könnten dadurch an das LLM gelangen. Eine explizite Pfadgrenze und erlaubte Log-Verzeichnisse sind erforderlich.
- Ungültige JSON-Zeilen werden still verworfen. Ein nicht objektförmiger JSON-Wert kann beim Zugriff data.get scheitern. Gültige Datensätze sollten validiert und verworfene Zeilen gezählt werden.
- Fehlende Token-/Kostenfelder werden teilweise als 0 interpretiert. Unbekannte Messwerte müssen als unbekannt erkennbar bleiben, damit Kosten nicht unterschätzt werden.
- LLM-Ausnahmen können graph.invoke verlassen, bevor run_cost_analysis einen Fehlertrace schreibt.
- Ein unparseable-Ergebnis wird im äußeren Erfolgszweig dennoch als status=success protokolliert. Trace-Status und fachlicher Ergebnisstatus müssen übereinstimmen.
- Der Graph selbst ist endlich; ein Gesamtzeitlimit des eigenen Workflows ist nicht explizit implementiert. Provider-Timeouts aus dem Starter ersetzen keine vollständige eigene Fehler-/Trace-Behandlung.
- Die untrusted Inhalte der Logs dürfen keine Reviewer-Instruktionen überschreiben.

Die fehlende Pfadgrenze ist ein konkreter hoher Sicherheitsbefund. Ein geleaktes Secret oder eine tatsächliche Datenabgabe wurde nicht festgestellt. Das Raster-Security-Critical-Finding für committed Secrets wird daher nicht behauptet.

### Drei sinnvolle Tests, aber kein Standardlaufnachweis
tests/test_cost_agent.py prüft:
- Fehlende Datei führt zu FileNotFoundError.
- Gültiges JSON wird in einen strukturierten CostReport umgesetzt.
- Ungültiger Text erzeugt unparseable statt eines Parsing-Absturzes.

Diese Tests sind eigene Leistung. Sie prüfen noch nicht den ganzen Graph, einen echten erfolgreichen Toollauf, einen LLM-Fehler oder die Traces. Das README meldet 4 passed; der Starter enthält bereits vier Tests, und hinzu kommen drei eigene Tests. Die Aussage bestätigt daher nicht den vollständigen aktuellen Testumfang. Sie kann sich auf einen früheren Starter-Testlauf beziehen; ein Testfehler oder Täuschung wird daraus nicht abgeleitet.

Die Actions-API liefert 0 Workflow-Runs. Ein Standardlaufprotokoll für den bewerteten Commit fehlt. Wie bei Team 1 wird D1 deshalb vorläufig mit 4/6 bewertet, ohne fehlende Evaluator-Abhängigkeiten als Teamfehler zu behandeln.

### Issue-/PR-Prozess ist eine Stärke
Issues #1–#7 decken Setup, Firma/Rollen, Architektur, eigenen Agenten, Tests, Trace und Kosten ab. PRs #8–#10 sind getrennt identifiziert und tragen Rollen-, Firmen- und Setupänderungen bei; PR #8 referenziert Issue #2.

Offene Checklisten sollten nach erfolgreicher Umsetzung mit konkreten Nachweisen aktualisiert werden. Aufgabentexte in Issues allein beweisen keine Implementierung; die Punkte für Prozess beziehen sich auf relevante Planung und nachvollziehbare Änderungen.

## README-Nachtrag nach 15:00 Uhr
Der Commit von 15:05:47 Uhr ergänzt eine Tabelle für alle sechs Menschen und deren OS/IDE, Python, Modell und gemeldete Testergebnisse. Das ist hilfreiche zusätzliche Setup-Dokumentation.

Er nennt unter anderem:
- Leon: oMLX statt Ollama, Modellbezeichnung Qwen3.8 27B.
- Lars: anderes Modell statt des Starter-Beispiels.
- Bohdan: Linux, während der frühere Abschnitt nur macOS/Windows nennt.

Die Modellbezeichnungen sind Teamangaben und wurden nicht extern verifiziert. Größere Modelle erzeugen keine Zusatzpunkte. Ein abweichendes Modell allein ist keine zentrale zusätzliche Technologie; oMLX als zusätzliche Runtime muss hinsichtlich Absprache und Integration in den vorgeschriebenen Provider-Pfad geklärt werden.

Der Nachtrag liegt außerhalb des vorläufigen Freeze und ändert den primären Score nicht. Würde der Dozent ihn zulassen, bleibt B1 bereits bei 4/4; B4 wäre bei tatsächlich zentraler, nicht abgesprochener oMLX-Nutzung erneut zu prüfen. Ein solcher Verstoß wird hier weder unterstellt noch rückwirkend auf den früheren Snapshot übertragen.

## Drei priorisierte Aufgaben für den nächsten Termin
1. **Echten Lauf und Evidenz erzeugen:** Eingabetraces nachvollziehbar bereitstellen, Cost-Agent mit vorhandenem Log ausführen, Ergebnis und eigenen Trace in einem eingecheckten evidence-Verzeichnis sichern. Trace um Modell, tatsächliche Toolnutzung, Ergebnisstatus, Kosten und Code-Commit ergänzen.
2. **Messfähigkeit vervollständigen:** grobe tatsächliche Arbeitszeiten aller sechs Menschen, Agentenläufe, Laufzeiten, verfügbare Tokens und tatsächliche CI-Runs in usage.csv erfassen; gemeinsame Raten erhalten und Credits per Python berechnen. Unbekannte Tokenwerte nicht als kostenlos behandeln.
3. **Qualität und Projektakte synchronisieren:** Cost statt QA als derzeitige Fähigkeit abbilden, konkreten Tool-/LLM-/Gate-Pfad zeichnen, Freigaberegeln harmonisieren; Pfadgrenzen und LLM-Fehlertraces reparieren, sinnvolle Tests ergänzen und python -m pytest mit Protokoll durchführen.

## Ausblick Termin 2
Bei sechs Menschen müssen Ende Termin 2 mindestens **12 − 6 = 6 operative agentische/hybride Rollen** technisch belegt sein. Geplante Actor-Typen allein zählen nicht. Ein Agent darf mehrere unterscheidbare Rollen unterstützen.

Hinzu kommen mindestens drei unterscheidbare Fähigkeiten, gemeinsames Task-/State-Modell, Agent-to-Agent-Workflow, Human Gate und der persistente Work-Item-Dry-Run mit Tests. Diese späteren Anforderungen führen hier zu keinem Abzug.

## Prüfgrenzen
Statischer Code-/Testreview, Baseline-Diff, komplette Snapshot-Struktur, Issue-/PR- und Actions-Abfrage durchgeführt. Kein unabhängiger Python-, DB- oder Ollama-/ICC-Lauf; der Evaluator-Umgebung fehlen Projektabhängigkeiten und ein LLM-Dienst. Keine vollständige Secrets-Prüfung aller historischen Inhalte durchgeführt. In den bewerteten Teamdateien wurde kein konkretes committed Secret festgestellt. Keine Security-Freigabe.

## Kurzes Teamfeedback
Ihr habt die Rollen vollständig zugeordnet, einen eigenen Cost-Agenten samt drei Tests gebaut und Eure Arbeit gut über Issues und PRs organisiert. Für das Tagesziel fehlen noch ein tatsächlich belegter Agentenlauf und ausgefüllte Nutzungs-/Kostendaten. Bringt außerdem Architektur und Firmenentscheidungen auf den Stand des Cost-Agenten. Priorität hat jetzt ein reproduzierbarer Lauf mit Trace, Testprotokoll und vollständiger Messung.

