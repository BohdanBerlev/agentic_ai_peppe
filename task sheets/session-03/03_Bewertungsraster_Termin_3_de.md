# Bewertungsraster Termin 3 – Kundenauftrag CUST-001

**100 Punkte · unbenoteter Engineering Health Indicator.** Für alle Teams gilt derselbe Kundenvertrag. Deutsch und Englisch sind gleichwertig. Maßgeblich sind die nachweisbare Kundenlieferung und die Arbeit seit der letzten Abgabe; bereits bewertete unveränderte Funktionen und Starter-Infrastruktur erzeugen keine neuen Eigenleistungspunkte. Die Integration wiederverwendeter Teamkomponenten darf zum funktionierenden Kundenergebnis beitragen.

## Kriterien

Teilpunkte sind proportional zur belegten Erfüllung zu vergeben, mit konkreter Begründung. Für jedes Kriterium Dateien, Testfälle, Run-IDs bzw. GitHub-Referenzen nennen. Erfüllung darf aus Dokumentation allein nicht unterstellt werden.

| Kriterium | Max. | Volle Punkte bei |
|---|---:|---|
| **A. Kundenverständnis** | **10** | |
| A1. Akzeptanzmatrix | 4 | AC-01 bis AC-08 jeweils mit Test/Artefakt und Ergebnis verknüpft. |
| A2. Klärungen | 2 | Fachliche Rückfragen/Annahmen nachvollziehbar; „keine offenen Fragen“ mit kurzer Begründung ist zulässig. |
| A3. Scope und freigegebene Anforderungen | 4 | Kleine vereinbarte Lieferung; ungeprüfte Modellvorschläge nicht als Kundenvorgabe ausgegeben; geprüfte Fassung vorhanden. |
| **B. Funktion und Daten** | **25** | |
| B1. Erstellung und Defaults | 5 | AC-01 im eigenen Code und an tatsächlich ausgeführtem API-Verhalten belegt. |
| B2. Filter | 7 | AC-03 einzeln und kombiniert erfüllt. |
| B3. Statuslogik | 7 | AC-04 einschließlich Wiederholung und Ablehnung ungültiger Übergänge, ohne unerwünschte Zustandsänderung. |
| B4. Datenerhalt/Migration | 6 | AC-02 und Mapping bestehender Daten dokumentiert und technisch belegt; kein destruktiver Reset. |
| **C. Tests und Reproduzierbarkeit** | **20** | |
| C1. Erfolgsfälle | 5 | Eigene erfolgreiche API-/Workflowtests im Standardlauf ausgeführt. |
| C2. Negative Fälle | 5 | AC-05/06/07 mit 422/404/503, unbekannten Feldern und unverändertem Zustand nach ungültigem Übergang getestet. |
| C3. Echter DB-Test | 7 | Eigener Kundentest in `tests/test_customer_persistence.py` mit PostgreSQL und neuer Verbindung/Prozess tatsächlich bestanden; kein Mock/Memory/Skip. |
| C4. Wiederholbarkeit | 3 | Befehle, Migration, Abhängigkeiten, geprüfter Quellstand und gespeicherte JUnit-Ergebnisse passen zusammen. |
| **D. Agentischer Kundenbeitrag** | **15** | |
| D1. Zwei Fähigkeiten | 4 | Zwei unterscheidbare eigene Fähigkeiten tragen zum Kunden-Task bei; Menschen-/Agentenbeiträge getrennt ausgewiesen. |
| D2. Fachlicher Handover | 5 | Vorheriger strukturierter Output beeinflusst nachfolgende Verarbeitung; Code und Ausführungsevidenz zeigen dies. |
| D3. Echter Lauf und Evidenz | 4 | Mindestens ein echter lokaler/ICC-LLM-Lauf samt Tool, IDs, Modell/Provider, Status und Artefakt; Mocktests separat. |
| D4. Fehler und Terminierung | 2 | Begrenzte Ausführung und nachvollziehbare Eskalation; fehlender Pflichtinput stoppt vor LLM-Nutzung. |
| **E. Menschliche Verantwortung** | **10** | |
| E1. Explizite Entscheidung | 4 | Reale Reviewentscheidung zu Kundenergebnis, Reviewer, Zeit und Begründung dokumentiert. |
| E2. Kein automatisches Human Approval | 3 | Headless-/ungültiger-Report-Negativtests bestehen; kein automatischer Kunden-/Issueabschluss ohne Freigabe. |
| E3. Bindung an Quellstand | 3 | Geprüfte Artefakte mit Code-Commit oder Hash gebunden; Änderungen lösen neuen Review aus. |
| **F. Kosten und Lernen** | **10** | |
| F1. Taskkosten | 4 | Reale Calls/Laufzeit/Tokens/Credits inkl. Fehlversuchen, dedupliziert ohne Rollup-Doppelzählung, unbekannte Werte ausgewiesen. |
| F2. Humanaufwand | 3 | Implementierung, Review und Korrektur getrennt geschätzt/erfasst und dem Task zugeordnet; Wartezeit separat. |
| F3. Folgerung | 3 | Begründete nächste Optimierung aus Daten und Qualitätsbefunden, mit prüfbarer Hypothese. |
| **G. Engineering-Prozess** | **10** | |
| G1. Issue → PR → Review | 4 | Konkrete Issues, Feature-PR und menschlicher Review nachvollziehbar; ZIP-Abgabe enthält die erforderlichen Referenzen/Exporte. |
| G2. Session-2-Nacharbeit und Rollen | 4 | Bestätigte Teamgröße; wichtigste Befunde bearbeitet oder begründet priorisiert; Status pro Rolle mit Evidenz/Gap statt Etiketten. |
| G3. Lieferakte | 2 | Architektur, Abnahme-/Lieferbericht und Reproduktionshinweise spiegeln den abgegebenen Stand. |
| **Gesamt** | **100** | |

## Obergrenzen

Erst Teilpunkte addieren, dann die niedrigste zutreffende Gesamtobergrenze anwenden. Rohscore, Cap und Endscore getrennt ausgeben. Teilbereichsgrenze vor Gesamtcap anwenden.

| Befund | Grenze |
|---|---:|
| Keine eigene plausibel ausführbare Kundenfunktion | Gesamt maximal 50 |
| Keine tatsächliche PostgreSQL-Implementierung, nur Memory/Mock-Speicher | Gesamt maximal 60 |
| Kein tatsächlich ausgeführter eigener PostgreSQL-Kundentest | Gesamt maximal 70 |
| Kein technischer fachlicher Agenten-Handover | Gesamt maximal 65 |
| Kein echter team-eigener lokaler/ICC-LLM-Kundenlauf belegt | Gesamt maximal 75 |
| Kein explizites menschliches Gate oder automatische Zustimmung wird als menschliche Freigabe behandelt | Gesamt maximal 60 |
| Relevante eigene Tests scheitern im korrekt eingerichteten Standardlauf | C maximal 10/20 |

Fehlende Infrastruktur der Bewertungsumgebung ist kein nachgewiesener Teamfehler. Ein gespeicherter, nachvollziehbarer echter DB-Lauf am zugeordneten Quellstand kann einen nicht wiederholbaren Live-DB-Lauf ersetzen. Ein bloßes README-„DB funktioniert“ oder grüne Mocktests genügen nicht. Ob ein Testfall übersprungen oder tatsächlich ausgeführt wurde, muss sichtbar sein. Wenn nur ZIP-Evidenz vorliegt, fehlende GitHub-Historie als Unsicherheit ausweisen und konkrete Exporte/Referenzen berücksichtigen.

Die früheren Rollen-Caps aus Termin 2 werden **nicht automatisch zusätzlich** auf Termin 3 übertragen. Rollenabdeckung bleibt Projektanforderung und wird hier in G2 mitbewertet; frühere Bewertungen bleiben bestehen. So wird Kundenlieferung nicht durch eine erneut gezählte historische Lücke ersetzt.

## Interpretation und Ausgabe

| Endscore | Interpretation |
|---:|---|
| 85–100 | Deutlich über Tagesziel |
| 70–84 | Tagesziel erreicht |
| 55–69 | Teilweise erreicht |
| 40–54 | Wesentliche Lücken |
| Unter 40 | Kundenlieferung noch nicht belastbar |

70 Punkte sind vollständig zufriedenstellend. Komplexität, Anzahl Agenten, Modellgröße, Aufrufzahl und Textmenge erzeugen keine Zusatzpunkte. Keine Punkte für `examples/**`, `tests/starter/**`, `pytest.ini` oder unveränderte Kursvorlagen. Reale veröffentlichte Secrets als Critical Finding ausweisen, ohne Werte zu wiederholen. Providerabweichungen, unbewiesene Aussagen und schwerwiegende Gatefehler ausdrücklich benennen; keine zusätzlichen unvereinbarten Scoreabzüge erfinden.

Bewertungsbericht: Kurzurteil; 24 Einzelkriterien mit Evidenz und Punkten; Rohscore/Caps/Endscore; Tests und Ausführungsgrenzen; Stärken; wesentliche Befunde; drei nächste Schritte. Zusätzlich Feedback in der Teamsprache. Optional strukturiertes JSON mit `company`, `session=3`, `source_commit`, `raw_score`, `applied_caps`, `score`, `dimensions`, `evidence`, `missing_evidence`, `top_3_actions` und `confidence`.
