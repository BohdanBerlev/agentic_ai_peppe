# Termin 6 – Zweiter Kunde, dieselbe Factory

**10:00–15:00 Uhr · Kundenprojekt 02 HansePack · Version 1.0, 08.11.2026**  
Verbindliche Anlagen: [Kundenbriefing mit Rechenregeln und Abnahmekriterien](Kundenbriefing_HansePack_de.md), [Katalog](HansePack_Katalog.json), [Referenzfälle](HansePack_Referenzfaelle.json). Bewertung: [Raster T6 DE/EN](Bewertungsraster_Termin_06_Factory.md).

## Was ihr heute konkret tut

Ihr stellt eure bestehende Factory auf einen zweiten Kunden ein und liefert einen kleinen, korrekt rechnenden Angebotsfall. Ihr baut keine neue Factory und erweitert nicht die Nordwerk-Website um fremde Kundenfunktionen.

**Lernziele:** L6.1 Projektwechsel und Wiederverwendung nachweisen; L6.2 einen echten agentischen Produktbeitrag liefern; L6.3 Fachregeln durch unabhängige Referenzwerte prüfen; L6.4 Projektstartaufwand und Grenzen der Wiederverwendung erfassen.

## 1. Auftrag klären und Produkt-Repo anlegen

Lest das Kundenbriefing, besonders die Rabatt- und Rundungsregeln. Erstellt `client-02-quotation` oder ein gleichwertiges separates Repo. Übernehmt Katalog und Referenzfälle unverändert als Kundenfixtures; Prüfsumme oder unveränderter Git-Stand genügt als Herkunftsnachweis. Notiert offene Fragen und explizite Annahmen im Kunden-Issue. Plant Lieferung T6/T7 und eine Reserve für T8. Dozent übernimmt die Kundenrolle; verbindliche Antworten gelten für alle Teams.

Sichert den letzten Nordwerk-Produktcommit. Konfiguriert in der vorhandenen Factory Kundenkennung, Checkout, Aufgaben und Prüfpfad für HansePack. Zeigt, welche Agenten/Tools unverändert bleiben und wo Anpassungen nötig sind. Neue generische Fähigkeit bei Bedarf zentral in der Factory implementieren; keine hartcodierte zweite Agentenkopie. Testet die Projektzuordnung deterministisch: Ein HansePack-Auftrag darf keine Nordwerk-Produktdatei ändern. In temporären Testverzeichnissen arbeiten, keine echten fremden Daten beschädigen.

## 2. Einen vollständigen Angebotsfall liefern

Gebt eurer Factory einen Task, etwa: „Implementiere die Python-Berechnung für HP-BOX mit Menge 1 und 50 einschließlich Rabatt, Versand und Gesamt. Weise Menge 0 zurück.“ Mindestens zwei Agentenfähigkeiten müssen strukturierte Daten tatsächlich übergeben; ein Agent erzeugt eine Produktänderung oder einen anwendbaren Patch. Reale Modell-/Tool-Nutzung und menschlichen Review belegen. Manuelle Ergänzungen bleiben erlaubt, zählen aber als menschliche Arbeit.

Heute genügen eine Python-Funktion mit reproduzierbarem Aufruf, CLI oder API. Die fertige Weboberfläche und der Download sind erst T7 fällig. Das Produkt läuft ohne Factory/LLM. Verwendet deterministische Rechenlogik, keine Preisberechnung durch einen LLM-Aufruf.

## 3. Konkrete Prüfungen ausführen

| Prüfung heute | Erwartetes Ergebnis |
|---|---|
| Q01: HP-BOX × 1 | Warenwert 250, Versand 1200, Gesamt 1450 Cent |
| Q03: HP-BOX × 50 | Listenbetrag 12500, Rabatt 625, Warenwert 11875, Versand 1200, Gesamt 13075 Cent |
| E01: Menge 0 | Verständlicher Fehler, kein gültiges Angebot |
| Projekttrennung | HansePack-Lauf verändert keine Nordwerk-Datei; letzter Nordwerk-Stand bleibt separat startbar |

Diese Tagesanforderungen konkretisieren HP-AC01/02 und den ersten Teil von HP-AC04. Erstellt eigene automatisierte Produktchecks gegen die gelieferten Werte und führt sie aus; eine Aussage des generierenden Agenten ist kein Fachtest. Ein Mensch prüft Ergebnis und Code-Diff. Factory-Test für Projektzuordnung im Standardlauf `python -m pytest`; separaten Produkt-Testbefehl dokumentieren. Tests dürfen Modelle mocken, der echte Produktlauf muss zusätzlich belegt sein.

## 4. Evidenz und Kosten sichern

Verknüpft Kunden-Issue, Eingabe-Commit, Run-ID, Factory-Commit, Agentenbeitrag, Produkttest, Ergebnis-Commit, Reviewer und Entscheidung. Schätzt/erfasst die Einrichtungszeit für den zweiten Kunden separat. Notiert kurz: Was ließ sich wiederverwenden? Was war noch kundenspezifisch? Welche eine Schwäche soll im nächsten Schritt untersucht werden? Noch keine kausale Ersparnis gegenüber Nordwerk behaupten: Es sind verschiedene Aufträge.

**Abgabe 15 Uhr:** neues eigenständig ausführbares Produkt, bestandene Q01/Q03/E01-Tests, echter Factory-Lauf, Projekttrennungstest, überprüfbarer Nordwerk-Stand sowie `evidence/session-06.md` mit Kosten, Verweisen und höchstens drei nächsten Schritten. Keine vollständige Angebotsanwendung heute erforderlich.

## Tagesrhythmus

10:00–10:20 Auftrag/Plan; 10:20–11:15 Repos und Projektwechsel; 11:15–12:00 erster Lauf; 12:00–12:30 Pause; 12:30–14:00 Berechnung/Prüfung/Korrektur; 14:00–14:35 Demo und Review; 14:35–15:00 Snapshot/Kosten.
