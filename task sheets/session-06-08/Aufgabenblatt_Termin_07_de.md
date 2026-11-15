# Termin 7 – Fachlich korrekte Angebote und wirksame Fehlererkennung

**10:00–15:00 Uhr · Kundenprojekt 02 · Version 1.0, 08.11.2026**  
Pflichtanlagen: [Kundenbriefing](Kundenbriefing_HansePack_de.md), [Katalog](HansePack_Katalog.json), [Referenzfälle](HansePack_Referenzfaelle.json). Bewertung: [Raster T7 DE/EN](Bewertungsraster_Termin_07_Factory.md).

## Was ihr heute konkret tut

Ihr vervollständigt den Angebotsrechner für die ursprünglichen Regeln HP-V1. Dann zeigt ihr mit einem absichtlich eingebauten Rabattfehler, dass die Factory eine fachlich falsche Lieferung zurückhält. Schließlich sichert ihr eine Ausgangsmessung für T8.

**Lernziele:** L7.1 wiederholbare agentische Lieferung; L7.2 unabhängige Fachtests in eine wirksame Freigabe einbauen; L7.3 einen fachlichen Fehler erkennen und korrigieren; L7.4 vergleichbare Baseline für eine Factory-Verbesserung sichern.

## 1. Rechenumfang und kleine Oberfläche fertigstellen

Plant fehlende Punkte aus HP-AC01–07. Ein echter neuer Kunden-Task muss durch eure Factory laufen, etwa Rundung, Eingabevalidierung oder Export. Ergebnisdiff, reale Agenten-/Tool-Nutzung, strukturierte Übergabe mindestens zweier Fähigkeiten und menschliche Entscheidung dokumentieren.

Implementiert alle drei Artikel, Mengenstaffeln, kaufmännische Rabattrundung und ursprüngliche Versandregel. Erstellt die kleine Weboberfläche und JSON-Download gemäß Briefing. Alle ungültigen Eingaben müssen die Python-Fachlogik erreichen und dort geprüft werden. Eingaben nur in der Oberfläche zu sperren reicht nicht. Anzeige und Export mit denselben tatsächlich berechneten Daten versorgen.

## 2. Vom Kunden vorgegebene Ergebnisse testen

Führt eigene Tests für Q01–Q14 unter HP-V1 und alle ungültigen E01–E10 aus. Prüft Positionswerte und Summen. Die Referenzdatei darf nicht durch passend gemachte Agentenausgaben ersetzt werden. Bei abweichenden Ergebnissen zuerst Regel und Implementierung untersuchen, erwartete Werte nicht stillschweigend verändern. Unklare Spezifikation an den Dozenten eskalieren.

Ein Mensch führt mindestens einen Mehrpositionsfall in der Oberfläche aus, lädt JSON herunter, vergleicht Anzeige und Export und probiert eine ungültige Menge. Ein frischer Produkt-Checkout muss nach Anleitung ohne Factory starten. Tests getrennt für Factory und Produkt ausführen; bestandene Starter-Tests ersetzen keinen Fachtest.

## 3. Fachfehler kontrolliert einschleusen

In einem separaten Test-Branch/Checkout verändert ihr genau eine Bedingung: Der 5%-Rabatt beginnt fälschlich erst **oberhalb 50** statt **ab 50**. Erwartete Kundenwerte bleiben unverändert. Q03 muss dadurch fehlschlagen: falsches Gesamt 13700 statt korrekt 13075 Cent.

Lasst die Factory ihre Produktchecks ausführen. Zeigt im Workflow, dass das Testergebnis eine Freigabe verhindert oder eine Korrektur auslöst; ein Report ohne Konsequenz genügt nicht. Korrigiert den Fehler, prüft erneut und dokumentiert die menschliche Entscheidung. Factory-Tests müssen bestandenen und zurückgehaltenen Gate-Zustand abdecken; Modellaufrufe dürfen darin gemockt sein. Isolierten Fehlerstand nicht ausliefern.

## 4. Vergleichsaufgabe R-02 einmal vor der Verbesserung ausführen

Sichert den korrekten HP-V1-Candidate als Produkt-Basiscommit **Q-BASE** und die aktuelle Factory als **F-BASE**. R-02 lautet:

> Ergänze im exportierten Angebots-JSON das Feld `calculation_note` mit dem festen Text `Net amounts; shipping shown separately.`. Anzeige, Geldwerte und Fehlerbehandlung bleiben unverändert. Ergänze einen Test für das Feld; alle bisherigen Fachtests müssen weiter bestehen.

R-02 ist nur ein Experiment, keine Kundenanforderung. Führt es auf einer sauberen isolierten Kopie von Q-BASE aus. Ergebnis nicht in den Kunden-Candidate mergen. Sichert Inputstatus, echte Commits, Modell/Provider/Einstellungen, Aufgabe, Prüfungen, Run-ID, Qualität, menschlichen Review-/Korrekturaufwand und bekannte Kosten. Ein vollständiger Lauf ist Pflicht; zwei sind bei Zeit empfohlen. Auch ein gescheiterter vollständiger Lauf ist eine Baseline, sein Misserfolg muss sichtbar bleiben.

Wählt einen beobachteten Factory-Engpass und plant eine kleine Änderung für T8, etwa strukturiertere Testaufträge oder ein gezieltes deterministisches Export-Gate. Untersuchte Änderung erst nach Sicherung der Baseline implementieren. Notwendige Reparaturen für den heutigen Candidate dürfen vorher erfolgen.

**Abgabe 15 Uhr:** versionierter Candidate für HP-AC01–07, Produkt-/Factory-Tests, menschlicher UI-/Exportreview, erkannter und korrigierter Fehler, Baseline R-02 und Hypothese. In `evidence/session-07.md` alle Commit-/Run-Verweise, Kosten inklusive CI-Fehlläufen und Planabweichungen bündeln.

## Tagesrhythmus

10:00–10:20 Planung; 10:20–12:00 Anwendung vervollständigen; 12:00–12:30 Pause; 12:30–13:30 Fachtests/Fehlerfall; 13:30–14:15 R-02; 14:15–14:35 Candidate-Demo; 14:35–15:00 Evidenz/Kosten. Neue Versandregel HP-V2 erst T8.
