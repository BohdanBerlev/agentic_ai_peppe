# Termin 3 – Erster Kundenauftrag durch eure Software Factory

**10:00–15:00 Uhr · Kundenprojekt 01 · Pflichtlektüre: [Kundenbriefing](Kundenbriefing_Nordwerk_de.md)**  
Bewertung: [Raster Termin 3](Bewertungsraster_Termin_03_Factory.md). Die Vorgaben im Briefing sind Bestandteil dieses Aufgabenblatts.

## Tagesziel und Lernziele

Am Tagesende hat eure bestehende Factory in einem separaten Kunden-Repository einen kleinen, ausführbaren Teil des Web-Auftritts erzeugt. Ihr könnt zeigen, welche Beiträge von Agenten stammen, welche von Menschen und wie das Ergebnis geprüft wurde.

- **L3.1:** Factory und Produkt technisch trennen und einen Kundenauftrag explizit adressieren.
- **L3.2:** Mindestens zwei Agentenfähigkeiten mit strukturierten Übergaben an einem echten Produktartefakt zusammenarbeiten lassen.
- **L3.3:** Prüfungen und menschliche Entscheidung tatsächlich in den Ablauf einbauen.
- **L3.4:** Aufwand einschließlich Fehlversuchen messen und daraus einen konkreten Engpass ableiten.

## 1. Kundenauftrag verstehen und eingrenzen

Lest das Briefing gemeinsam. Legt im Produkt-Repo ein Kunden-Issue mit Tagesumfang, AC-01, AC-04 und einer Leistung aus AC-02 an. Übernehmt die verbindlichen Inhalte. Notiert offene Fragen und dokumentiert Kundenantworten. Aufgabenblatt und Briefing bilden den freigegebenen Ausgangsumfang; offene Entscheidungen dürfen als explizite Annahmen dokumentiert werden.

Legt accountable humans für Auftrag, technische Lieferung, Prüfung und Freigabe fest. Mehrere Rollen pro Person bleiben möglich. Plant Lieferaufwand T3/T4 und Reserve T5 nach dem Kostenvertrag. Vollständige Autonomie ist kein Tagesziel.

## 2. Repositories und Arbeitsbereiche trennen

Verwendet das existierende Team-Repo als Factory weiter. Erstellt ein eigenständiges Produkt-Repo, etwa `client-01-website`. Richtet einen separaten Checkout ein. Die Factory erhält konfigurierbar Projektkennung, Pfad und Task. Produktdateien werden dort erzeugt; Agenten, Policies und allgemeine Tools bleiben in der Factory.

Prüft, dass das Produkt ohne Factory-Prozess lokal geöffnet oder über einen einfachen dokumentierten Webserver ausgeliefert werden kann. Geheimnisse gehören in keine Abgabe. Die Factory darf den vorgegebenen Stack behalten, ohne ihn dem Produkt aufzuzwingen.

## 3. Einen echten Factory-Durchlauf ausführen

Verwendet eure Fähigkeiten aus Termin 2. Beispiel: Requirements/Planung übergibt strukturierte Tasks an Implementierung; QA erhält Artefaktpfade und Kriterien. Namen und konkrete Aufteilung sind frei.

Ein Lauf muss mindestens zwei Agentenfähigkeiten, einen realen LLM-Aufruf und eine reale Tool-Aktion auf dem Kunden-Checkout belegen. Ein Agent bearbeitet mindestens eine Produktdatei oder erzeugt einen anwendbaren Patch. Baut einen sichtbaren menschlichen Review-Schritt ein. Ein abgelehnter Zwischenstand mit anschließender Korrektur ist zulässig; er darf nicht als akzeptiert ausgewiesen werden. Wiederholungen werden begrenzt, z. B. maximal zwei Korrekturschleifen, danach menschliche Eskalation.

Sichert vor Start die Eingabe-Commits und verknüpft anschließend Ergebnisstand und Evidenz. Rohlogs mit eindeutigen Run-IDs sichern. Manuelle Eingriffe, nicht ausgeführte Vorschläge und verworfene Änderungen kennzeichnen.

## 4. Kleinen Website-Ausschnitt prüfen

Zeigt Firmenname, Hauptaussage, eine Leistung, Kontaktlink und Übungshinweis. Ein einfaches Layout genügt. Erstellt mindestens einen sinnvollen eigenen automatisierten Produktcheck und einen eigenen Factory-Test für strukturierten Übergabezustand oder Projektzuordnung. Factory-Tests laufen mit `python -m pytest`; Produkttests besitzen einen separaten dokumentierten Aufruf. Tests dürfen für reproduzierbare Logik Mock-LLMs verwenden; der reale Durchlauf wird separat nachgewiesen.

Ein Mensch prüft die sichtbaren Inhalte und den Kontaktlink. Erst danach wird der Stand freigegeben oder mit konkretem Grund abgelehnt.

## 5. Bilanz und Abgabe

Erfasst menschliche Liefer-, Review-, Nacharbeits- und Factory-Zeit separat, Agenten-/CI-Kosten und Fehlläufe. Notiert den wichtigsten Engpass mit Run-/Artefaktbeleg sowie eine überprüfbare Verbesserungshypothese für T4/T5. Noch kein Vorher-Nachher-Experiment erforderlich.

| Ablage | Pflichtabgabe |
|---|---|
| Produkt-Repo | Kunden-Issue, kleiner lauffähiger Website-Stand, eigener Produktcheck, Start-/Testbefehl |
| Factory-Repo | Projektkonfiguration, eigener Factory-Test, Run-Evidenz, Human-Gate-Entscheidung, Kosten |
| `evidence/session-03.md` | Verweise auf beide Commitstände, Run-IDs, geprüfte Tageskriterien, Beiträge, Engpass und Hypothese |

## Zeitrahmen

10:00–10:20 Auftrag und Planung; 10:20–12:00 Repo-Trennung und erster Lauf; 12:00–12:30 Pause; 12:30–14:00 Produkt, Tests und Korrektur; 14:00–14:35 Demo/Review; 14:35–15:00 Evidenz und Kosten sichern.

**Definition of Done:** Der kleine Produktstand ist vorführbar, sein Agentenbeitrag ist technisch belegt, die menschliche Prüfung ist dokumentiert und Aufwand/Lücken sind ehrlich ausgewiesen. Eine vollständige Website wird erst in T4 verlangt.
