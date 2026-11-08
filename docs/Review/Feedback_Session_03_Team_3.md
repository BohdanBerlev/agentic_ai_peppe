# Team 3 – Session 3: Feedback

**80/100 Punkte – solider Tagesstand; Factory-Lernziele teilweise erreicht.**

Ihr habt einen anspruchsvollen agentischen Entwicklungsworkflow realisiert: mehrere Fähigkeiten arbeiten mit strukturierten Übergaben zusammen, der Backend-Agent erstellt eine Kundenwebsite, QA führt einen echten Produktcheck aus, und ein Mensch entscheidet am Freigabe-Gate. Die Nordwerk-Website erfüllt die Anforderungen von Session 3; der Produkttest wurde bei der Evaluation erfolgreich wiederholt.

Besonders gut ist eure Analyse eines konkreten Factory-Engpasses: Eine frühe negative Architekturprüfung bleibt im Workflow bestehen, obwohl Implementierung und QA später erfolgreich waren. Eure Hypothese zur Verbesserung der Gate-Entscheidung ist messbar und damit ein guter Ausgangspunkt für Session 4.

**Drei Punkte solltet ihr jetzt klären:**

1. **Eindeutige Release-Evidenz:** Der SHA-256-Wert eurer eingereichten `index.html` stimmt nicht mit dem freigegebenen Laufartefakt überein; der verlinkte Produkt-Commit ist für die Evaluation nicht zugänglich. Bitte stellt einen überprüfbaren Stand samt Test und menschlicher Freigabe bereit.
2. **Tatsächliche Tool-Sicherheit und Provider:** Euer Backend-Agent verwendet nicht den vollständig gehärteten Schreib-Helper. Übernehmt die `.git`-/Workspace-Schutzregeln in den wirklich ausgeführten Code. Dokumentiert außerdem die offizielle Freigabe für Google Gemini oder verwendet den vorgesehenen Modellzugang.
3. **Saubere Messung:** Der eingereichte Factory-Testbericht enthält 67 bestandene und zwei übersprungene Tests, darunter den PostgreSQL-Lifecycle-Test. Korrigiert die abweichende Manifest-Aussage und trennt Kundenlieferkosten von Factory-Entwicklungszeit.

**Insgesamt eine technisch starke Leistung.** Für Session 4 ist der wichtigste Fortschritt, dass eure Factory nicht nur funktionierende Software erzeugt, sondern ihre Ergebnisse **reproduzierbar, sicher und eindeutig freigegeben** ausliefert.
