# Termin 8 – Versandänderung liefern und Factory-Wirkung prüfen

**10:00–15:00 Uhr · Kundenprojekt 02 · Version 1.0, 08.11.2026**  
Pflichtanlagen: [Kundenbriefing](Kundenbriefing_HansePack_de.md), [Referenzfälle](HansePack_Referenzfaelle.json). Bewertung: [Raster T8 DE/EN](Bewertungsraster_Termin_08_Factory.md).

## Was ihr heute konkret tut

Ihr setzt die neue Versandregel im vorhandenen Angebotsrechner um, liefert einen geprüften Release und prüft eine gezielte Factory-Verbesserung am gleichen Versuch wie in T7. Kundenänderung und Factory-Experiment bleiben getrennt.

**Lernziele:** L8.1 eine fachliche Änderung durch dieselbe Factory liefern; L8.2 unveränderte Fachregeln durch Regressionen absichern; L8.3 die Wirkung einer Factory-Änderung unter vergleichbaren Bedingungen untersuchen; L8.4 Aufwand und Wiederverwendung über zwei Kundenprojekte begründet beurteilen.

## 1. Kundenänderung CR-02 umsetzen

> Ab jetzt: Unter 400,00 Euro Warenwert nach Rabatt kostet der Versand 15,00 Euro. Ab einschließlich 400,00 Euro ist er frei. Rabatte, Rundung, Artikel und Validierung bleiben unverändert.

Dokumentiert Auswirkung und betroffene Tests im Änderungs-Issue. Nutzt eure Factory, um den T7-Produktstand auf Regelversion **HP-V2** zu ändern. Mindestens zwei Agentenfähigkeiten, realer Modell-/Tool-Lauf und agentischer Produktdiff müssen belegt sein. Menschen prüfen und entscheiden am konkreten Ergebnis-Commit. Mindestens Q06, Q10 und Q11 im Review erläutern: Rabatt vor Versandschwelle, genau an der neuen Schwelle, knapp darunter.

## 2. Fachregression und Lieferung prüfen

Alle Q01–Q14 unter HP-V2 sowie E01–E10 müssen geprüft werden; Positionswerte und Rabatte bleiben identisch zu HP-V1. Nur Versand, davon abhängiges Gesamt und Regelversionskennzeichnung ändern sich. Falsche alte Versand-Erwartungen nicht als V2-Regression behandeln. Keine Pflicht zu parallelem Betrieb beider Regeln: V1-Commit und alte Prüfergebnisse erhalten, V2-Tests für den neuen Stand nutzen.

Ein Mensch erstellt eine Mehrpositionsanfrage in der Oberfläche, kontrolliert Versand/Gesamt und den heruntergeladenen JSON-Export. Frischen Checkout und Produkt-Testaufruf ohne Factory nachweisen. HP-AC01–07 bleiben sinngemäß mit neuen Versandwerten gültig, HP-AC08/09 kommen hinzu. Nordwerk-Dateien bleiben unverändert; letzter Nordwerk-Stand ist weiter separat verfügbar.

## 3. Eine Factory-Verbesserung gegen R-02 prüfen

Vor der geplanten Änderung vollständige T7-Baseline und echte **F-BASE/Q-BASE**-Commits prüfen. Falls nötig vorher mit unveränderter Factory nachholen und als **T8-Nachholung** markieren; T7-Bewertung ändert sich dadurch nicht.

Implementiert genau eine kleine begründete Factory-Änderung und kennzeichnet sie als **F-NEW**. Führt exakt R-02 aus T7 auf einer frischen isolierten Kopie desselben **HP-V1-Q-BASE** aus, nicht auf dem inzwischen geänderten HP-V2-Produkt. Gleiches Modell/Provider/Einstellungen und gleiche Akzeptanzprüfungen verwenden; keine fertige Vorher-Lösung, Patches oder ausgangsverändernde Caches übernehmen. Geänderte Factory-Policies dürfen Teil der benannten Intervention sein.

R-02: Feld `calculation_note` im JSON-Export mit Text `Net amounts; shipping shown separately.`, Test dafür, bisherige Werte/Anzeige/Fehlerbehandlung erhalten. Experimentergebnis nicht in die Kundenlieferung mergen. Die gleichen unabhängigen Abnahmetests in beiden Varianten verwenden; Agenten dürfen zusätzliche Tests erzeugen, aber nicht die verbindlichen Kriterien verändern.

Mindestens ein vollständiger Vorher-/Nachher-Lauf, zwei je Variante bei Zeit empfohlen. Vergleicht Qualität, Fehler, menschliche Liefer-/Review-/Nacharbeitszeit und bekannte Agenten-/CI-Kosten; einmaligen Verbesserungsaufwand getrennt angeben. Bericht maximal etwa eine Seite plus Rohdaten. Kein positiver Effekt vorgeschrieben; Beibehalten, Anpassen oder Zurücknehmen begründen. Ein Versuchspaar liefert eine vorläufige Beobachtung, keine belastbare allgemeine Überlegenheit.

## 4. Abnehmen und wirtschaftliche Bilanz ziehen

Versioniert den Kundenrelease und übergebt Start, Tests und Regelbeschreibung. Der Dozent entscheidet als Kunde; ausstehende Entscheidung gesondert markieren. In `evidence/session-08.md` stehen Produkt-/Factory-Commits, Run-IDs, Prüfergebnisse, Freigaben, Experiment und Kostenbilanz T6–8.

Beantwortet mit konkreten Nachweisen drei Fragen: Welche Fähigkeit aus Nordwerk wurde tatsächlich wiederverwendet? Welcher Aufwand blieb kundenspezifisch? Welche Factory-Investition würdet ihr für einen dritten Kunden beibehalten? Unterschiedliche Aufträge nicht ungeprüft als Vorher-/Nachher-Benchmark vergleichen. Keine Kosten-pro-akzeptiertem-Task berechnen, wenn kein Task akzeptiert wurde: Misserfolg und Aufwand nennen. Kleine Fallzahl/Teamgröße beachten, kein Euro-Gewinn ableiten.

**Abgabe 15 Uhr:** geprüfter HP-V2-Release, realer Änderungslauf, R-02-Vergleich mit Rohdaten, bilanzierte Kosten und wahrer Kundenstatus. Kein neuer Agent und kein zusätzliches Produktfeature allein für mehr Komplexität nötig.

## Tagesrhythmus

10:00–10:20 Änderungsanalyse; 10:20–11:20 Factory-Änderung/Versuch; 11:20–12:00 CR-02; 12:00–12:30 Pause; 12:30–13:30 CR-02/Regression abschließen; 13:30–14:10 Produktreview/Bilanz; 14:10–14:35 Kundendemo; 14:35–15:00 Evidenz sichern.
