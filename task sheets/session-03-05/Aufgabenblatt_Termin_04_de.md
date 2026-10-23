# Termin 4 – Lieferfähige Website und belastbare Factory-Prüfung

**10:00–15:00 Uhr · Kundenprojekt 01 · Pflichtlektüre: [Kundenbriefing](Kundenbriefing_Nordwerk_de.md)**  
Bewertung: [Raster Termin 4](Bewertungsraster_Termin_04_Factory.md).

## Tagesziel und Lernziele

Ihr liefert einen eigenständig startbaren Release Candidate für AC-01 bis AC-08. Die Factory bearbeitet weitere Kunden-Tasks und unterscheidet zuverlässig zwischen bestandenem Ergebnis und notwendiger Korrektur. Ihr sichert die Ausgangsmessung für die Verbesserung in Termin 5.

- **L4.1:** Die Factory wiederholt auf demselben Kundenprojekt einsetzen, ohne die Agenten in das Produkt zu kopieren.
- **L4.2:** Automatisierte Prüfungen und menschliches Review zu einer wirksamen Freigabe verbinden.
- **L4.3:** Eine kontrollierte Fehlersituation erkennen und die Lieferung verhindern oder korrigieren.
- **L4.4:** Einen reproduzierbaren Ausgangsversuch für eine spätere Factory-Änderung sichern.

## 1. Stand prüfen und Arbeit planen

Öffnet die Evidenz aus T3. Prüft Engpass, offene ACs und Aufwand. Priorisiert die fehlenden Pflichtinhalte. Macht keine optionale Funktion zum Pflichtumfang. Behandelt jede Produktänderung als Task mit verantwortlicher Person und erwartetem Ergebnis.

## 2. Release Candidate mit der Factory fertigstellen

Bearbeitet die fehlenden Leistungen, Zielgruppen, Arbeitsweise und Navigation über eure Factory. Mindestens ein weiterer substanzieller Produkt-Task muss einen realen Agentenlauf einschließlich Tool-Nutzung, Prüfung und menschlicher Entscheidung durchlaufen. Wiederverwendet Konfiguration und Workflow; dokumentiert erforderliche Anpassungen. Manuelle Arbeit bleibt zulässig und wird sichtbar erfasst.

Erstellt einen Review-PR oder einen gleichwertigen überprüfbaren Diff mit zugehöriger Freigabe. Automatisches Mergen ist keine Anforderung. Markiert den Candidate mit Tag oder eindeutigem Commit und dokumentiert den Start aus einem frischen Produkt-Checkout ohne laufende Factory.

## 3. Qualitätsgate tatsächlich prüfen

Automatisiert mindestens drei unterschiedliche Produktprüfungen: Pflichtinhalt, Kontakt-/Navigationsziel und lokale Verweise/Assets. Eine sinnvolle Zusammenfassung pro Prüffamilie genügt. Prüft 375/1280 px sowie Tastaturnavigation/Fokus zusätzlich im Browser und dokumentiert Ergebnis und Prüfer. Browserautomation ist optional; ein Screenshot allein belegt keine funktionierende Navigation.

In einer isolierten Testkopie verändert ihr genau einen Fehler: Kontaktadresse auf einen falschen Wert setzen oder einen internen Link brechen. Zeigt, dass die Prüfung fehlschlägt und der Workflow den Stand nicht als freigegeben ausweist. Korrigiert den Fehler und prüft erneut. Keine absichtlich defekte finale Lieferung. Factory-Tests müssen den positiven und den abgelehnten/eskalierten Zustand des Gates prüfen; reale LLM-Läufe und deterministische Tests getrennt ausweisen.

## 4. Ausgangsversuch R-01 sichern

Der gleiche Versuch wird in T5 nach einer Factory-Änderung wiederholt. Erstellt dafür aus eurem Candidate einen eingefrorenen Basis-Commit **R-BASE**. Aufgabe R-01 lautet:

> Ergänze unter den Leistungen die Karte **„Projektkoordination“** mit dem Text **„Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.“** Alle bisherigen Inhalte, Kontaktziele und Navigation müssen erhalten bleiben.

R-01 ist eine isolierte Referenzaufgabe, keine zusätzliche Kundenanforderung. Führt sie mit der aktuellen Factory **F-BASE** auf einem eigenen Branch/Checkout von R-BASE aus. Mischt das Versuchsergebnis nicht in den Kundenrelease. Haltet Input, Kriterien, Modell/Einstellungen, Factory-/Produkt-Commits, Run-IDs, Prüfqualität, Review-/Nacharbeitszeit und bekannte Kosten fest. Ein vollständiger Versuch ist Pflicht; zwei Wiederholungen sind bei verfügbarer Zeit empfohlen. Fehlversuche mit ausweisen.

Wählt aus T3/T4 einen Engpass und formuliert eine kleine Verbesserung für T5, die sich an R-01 überprüfen lässt. Beispiel: fehlende Pflichttexte vor dem Human Gate deterministisch prüfen. Notwendige Reparaturen für den heutigen Candidate dürfen vorher erfolgen; die bewusst zu untersuchende Änderung beginnt erst nach gesicherter Baseline.

## 5. Abgabe

| Ablage | Pflichtabgabe |
|---|---|
| Produkt-Repo | Candidate-Commit/Tag, AC-01–08-Prüfliste, Produkttests, Browserreview, Start-/Testanleitung, überprüfbarer Lieferdiff |
| Factory-Repo | weiterer echter Task-Lauf, Gate-Tests, kontrollierter Fehlernachweis, R-01-Baseline und Hypothese |
| `evidence/session-04.md` | Commit-/Run-Verweise, Freigabe, Kosten inklusive Fehlläufen, Abweichung vom Planbudget und nächste Änderung |

## Zeitrahmen

10:00–10:20 Planung; 10:20–12:00 Fertigstellung; 12:00–12:30 Pause; 12:30–13:30 Tests und Fehlerfall; 13:30–14:15 Baseline R-01; 14:15–14:35 Candidate-Demo; 14:35–15:00 Snapshot und Kosten.

**Definition of Done:** Ein prüfbarer Candidate erfüllt AC-01–08, ein fehlerhafter Teststand wurde tatsächlich zurückgehalten und die Baseline für T5 ist reproduzierbar. Eine neue Kundenänderung und die Sicherheitsantwort werden heute noch nicht verlangt.
