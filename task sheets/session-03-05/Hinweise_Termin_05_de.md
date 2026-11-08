# Termin 5 – Durchführungshinweise für alle Teams (DE)

**Wahlpflichtprojekt Agentic AI · 9. November 2026 · Ergänzung zur Durchführung, keine neue Aufgabenstellung**

**Verbindlich bleiben** das bestehende [Aufgabenblatt für Termin 5](https://github.com/MARS-Group-HAW/agentic_ai/blob/main/task%20sheets/session-03-05/Aufgabenblatt_Termin_05_de.md), das [Kundenbriefing Nordwerk](https://github.com/MARS-Group-HAW/agentic_ai/blob/main/task%20sheets/session-03-05/Kundenbriefing_Nordwerk_de.md) und das unveränderte [Bewertungsraster](https://github.com/MARS-Group-HAW/agentic_ai/blob/main/task%20sheets/session-03-05/Bewertungsraster_Termin_05_Factory.md). Es gibt **keine neuen Anforderungen, Punkte oder zusätzlichen Agentenquoten**. Diese Hinweise präzisieren bereits bestehende Vorgaben aufgrund der Erfahrungen aus Termin 4.

## 1. R-01: Vergleichbarkeit vor Optimierung sichern

- Prüft **vor jeder Factory-Änderung**, ob F-BASE und R-BASE als konkrete Git-Commits identifizierbar sind. Ein Tag allein genügt nur, wenn er tatsächlich auf den ausgeführten Commit zeigt.
- Erstellt einen sauberen Ausgangs-Checkout. Dokumentiert `git status`, Factory-/Produkt-Commit, Modell/Provider, Einstellungen, identische R-01-Aufgabe und Akzeptanztests sowie die eindeutige Run-ID.
- Ist die T4-Baseline unvollständig oder nicht wiederherstellbar, darf sie **vor der Änderung** mit der unveränderten Factory nachgeholt werden. Kennzeichnet sie als **T5-Nachholung**; dies ändert die T4-Bewertung nicht.
- Führt R-01 danach mit F-NEW auf einer **frischen Kopie desselben R-BASE** aus. Keine R-01-Ergebnisdateien oder vorgefertigten Patches aus dem ersten Lauf übernehmen. Nur die gezielt untersuchte Factory-Änderung variieren; dasselbe Modell und dieselben Einstellungen verwenden.
- Dokumentiert auch gescheiterte, aber vollständig protokollierte Versuche. Ein positiver Optimierungseffekt ist **keine** Bestehensvoraussetzung. Schon ein Vorher-/Nachher-Paar ist nur eine vorläufige Beobachtung.

## 2. Kosten vollständig und ohne Doppelzählung

- Erfasst für T5 und die T3–T5-Bilanz **alle zugehörigen** Agentenläufe, Fehlversuche und CI-Workflow-Runs (auch fehlgeschlagene GitHub-Actions-Läufe) nach dem Kurs-Creditmodell. Nicht zum Kundenauftrag gehörende Läufe sind als Factory-Entwicklung oder sonstige interne Tätigkeit kenntlich zu machen.
- Ordnet menschliche Zeit **exklusiv** einer Kategorie zu: Factory-Entwicklung, Kundenlieferung, Review oder Nacharbeit. Dieselbe Zeit darf nicht doppelt erscheinen.
- Trennt die **operativen Kosten des R-01-Vergleichs** vom einmaligen Aufwand für die Entwicklung von F-NEW. Fehlende Token-/Messwerte bleiben ausdrücklich `unknown`, nicht automatisch `0`.
- Prüft, ob `costs/usage.csv` technisch korrekt einlesbar ist und Summen/CI-Zählung zu den Rohdaten passen.

## 3. Nachweisbare Produktfreigabe und Experimenttrennung

- Verknüpft Kunden-Task/Issue, Ausgangs-Commit, Run-ID, agentischen Diff, Produkttestergebnis, konkreten Ergebnis-Commit, menschlichen Reviewer, Freigabeentscheidung und Zeitpunkt.
- Haltet **drei Zustände auseinander**: (a) veröffentlichungsfähiger Nordwerk-Candidate, (b) isoliertes R-01-Experiment, (c) absichtlich fehlerhafter Teststand. R-01 ist **keine** neue Kundenanforderung.
- Das Produkt muss für die Bewertung zugänglich sein: öffentliche Git-Commits oder vollständiger überprüfbarer ZIP-/Commit-/Diff-Nachweis. Ein privater, für die Evaluation nicht einsehbarer Link genügt nicht allein.
- Eine technische Teamfreigabe ist **nicht** die Kundenabnahme. Die Dozentenentscheidung wird gesondert dokumentiert; ausstehende Abnahme ist nach Aufgabenblatt zulässig.

## 4. Umfang begrenzen und Zeit gezielt einsetzen

- **CR-01:** Eine kurze englische Einstiegsseite reicht. Keine vollständige Übersetzung der Detailtexte und keine zusätzlichen Frameworks nötig. Bestehende deutsche Inhalte und AC-01–08 müssen erhalten bleiben.
- **SR-01:** Höchstens ca. eine Seite faktengeprüfte Kundenantwort, plus knappe Komponentenübersicht. Bekannte Tatsachen von Unbekanntem unterscheiden, Quellen und Abrufdatum nennen. Kein Penetrationstest erforderlich.
- **Factory-Experiment:** Eine gezielte Verbesserung und mindestens ein nachvollziehbarer Vorher-/Nachher-Lauf statt neuer Agentenfunktionen. Qualität, Review-/Nacharbeit und Gesamtkosten vergleichen.
- **Evidenz:** Ein prägnanter `evidence/session-05.md` mit Links, Status, Kostenbilanz und drei überprüfbaren Erkenntnissen. Keine zusätzliche umfangreiche Dokumentation.

**Quellen SR-01:** [ENISA, 21.10.2026](https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities) und [PHP-Projekt, Sicherheitsmitteilung 2026](https://www.php.net/archive/2026.php). Die Quellen sind verfügbar. Eine bloße Angabe „PHP 8.2“ belegt weder die konkrete Verwundbarkeit noch eine erfolgte Behebung.

**Didaktischer Maßstab:** Nicht die Zahl der Agenten oder eine schönere Website zählt, sondern nachweisbare Änderungslieferung, wirksame menschliche Qualitätskontrolle und ein nachvollziehbarer empirischer Verbesserungsversuch.
