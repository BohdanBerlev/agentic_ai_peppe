# Feedback – Team 3 (PepeGroup), Session 4

**92/100 Punkte – sehr starker Tagesstand; Tagesziel nach Lernzielmatrix teilweise erreicht.**

Ihr habt die Nordwerk-Website überzeugend zu einem Release Candidate weiterentwickelt. Alle vier Produkt-Prüffamilien konnte ich unabhängig erfolgreich ausführen. Besonders positiv sind der dokumentierte echte Folgeauftrag durch eure Factory, die wirksame Erkennung von Kontakt- und Navigationsfehlern mit anschließender Korrektur sowie die transparente Erfassung von zwei fehlgeschlagenen R-01-Läufen. Auch eure konkrete Hypothese zur Reduktion unnötiger Agentenaufrufe ist ein sinnvoller Ansatz für Session 5.

**Drei Punkte sind für den nächsten Termin wichtig:**

1. **R-01 reproduzierbar machen:** In eurem Bericht steht `F-BASE = 6da5414`, der GitHub-Tag zeigt jedoch auf `5a146a3`. Dazwischen wurde relevanter Factory-Code geändert. Stellt den tatsächlich ausgeführten Ausgangsstand und den separaten R-01-Produkt-Commit eindeutig bereit.
2. **Freigabe an den Produktstand binden:** Verknüpft menschliches Review, Testergebnis und den konkreten freigegebenen Commit/Diff in einer gemeinsamen T4-Evidenz. Das Produkt-Repository war bei der Evaluation nicht zugänglich.
3. **Kosten und Betrieb vollständig erfassen:** Eure menschlichen Zeiten und Agentenläufe sind gut aufgeschlüsselt. Die GitHub-Actions-Läufe fehlen jedoch, darunter zahlreiche gescheiterte Issue-Reviewer-Läufe. Klärt außerdem die formale Freigabe eures Gemini-Providers.

**Insgesamt eine technisch starke Weiterentwicklung.** Der wichtigste nächste Schritt ist jetzt, die bereits funktionierende Factory und ihren wirtschaftlichen Verbesserungsprozess exakt reproduzierbar und überprüfbar zu machen – nicht zusätzliche Komplexität aufzubauen.
