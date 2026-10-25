# Termin 5 – Kundenänderung, Sicherheitsanfrage und Factory-Experiment

**10:00–15:00 Uhr · Kundenprojekt 01 · Pflichtlektüre: [Kundenbriefing](Kundenbriefing_Nordwerk_de.md)**  
Bewertung: [Raster Termin 5](Bewertungsraster_Termin_05_Factory.md).

## Tagesziel und Lernziele

Ihr liefert eine begrenzte Kundenänderung am vorhandenen Website-Stand, beantwortet eine Sicherheitsanfrage und prüft eine gezielte Factory-Verbesserung gegen die Baseline aus T4.

- **L5.1:** Eine Änderung ausgehend von einem versionierten Produktstand durch dieselbe Factory liefern.
- **L5.2:** Die Wirkung einer Factory-Änderung unter vergleichbaren Bedingungen ehrlich prüfen.
- **L5.3:** Betroffenheit, Annahmen und Handlungsoptionen einer Sicherheitsanfrage unterscheiden.
- **L5.4:** Produktabnahme, Kosten und wiederverwendbare Factory-Erkenntnisse zusammenführen.

## 1. Kundenänderung CR-01

> Wir möchten internationale Anfragen ermöglichen und künftig auch technische Einkaufsabteilungen ansprechen. Bitte ergänzen Sie eine kurze englische Einstiegsseite bzw. klar bezeichnete englische Ansicht. Die bisherige deutsche Website soll erhalten bleiben.

Erstellt ein Änderungs-Issue und eine kurze Auswirkungsanalyse. Nutzt eure Factory für die Produktänderung. Die englische Ansicht muss enthalten:

| Element | Verbindlicher Inhalt |
|---|---|
| Titel | **Nordwerk Industrie-Service** |
| Hauptaussage | **Practical support for your technical operations.** |
| Leistungen | **Maintenance planning**, **Spare parts coordination**, **Operational documentation** |
| Zusätzliche Zielgruppe | **Technical purchasing departments** |
| Kontakt | **Request information**, `mailto:kontakt@nordwerk.example` |
| Hinweis | **Fictional company – HAW Hamburg course project. No real offers or contact.** |

Die deutsche Ansicht erhält zusätzlich **„Technische Einkaufsabteilungen“** als Zielgruppe. Von beiden Ansichten sind Sprachwechsel und Kontakt erreichbar; die englische Ansicht besitzt passende Sprachkennzeichnung und Dokumenttitel. Ein kurzer englischer Einstieg reicht, keine vollständige Übersetzung aller Detailtexte. Prüft neue Inhalte automatisiert und AC-01–08 als Regression; Browserreview erneut bei 375/1280 px sowie per Tastatur. Verbindliche Zahlen oder Leistungsversprechen werden nicht ergänzt.

## 2. Sicherheitsanfrage SR-01

> Wir haben von kritischen PHP-Lücken gehört. Ist unser bisheriger Auftritt betroffen? Können wir Ihre neue Website sicher einsetzen, und wer kümmert sich künftig um Updates?

**Bereitgestelltes Systemprofil, Stand 23.10.2026:** Alter Auftritt bei externem Hoster; Betreiberangabe „PHP 8.2“, genaue Paket-/Patchversion und CMS-Version unbekannt; CMS und Kontaktformular vorhanden; kein Administratorzugang und keine belastbare Aussage des Hosters zu den Korrekturen. Kein Hinweis auf einen konkret nachgewiesenen Angriff. Die neue Kurswebsite besitzt nur die tatsächlich von euch verwendeten Komponenten.

Lest die [ENISA-Mitteilung vom 21.10.2026](https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities) zu CVE-2026-109618 und CVE-2026-109619. Nutzt die dort verlinkte PHP-Quelle bei Detailaussagen. Dokumentiert Quelle und Abrufdatum. Wenn der Zugriff im Kurs nicht möglich ist, stellt der Dozent einen datierten Auszug derselben Primärquelle bereit; die Einschränkung wird genannt.

Erstellt eine kurze Kundenantwort, maximal ca. eine Seite: Was ist bekannt, was bleibt offen, welche Angaben muss der Hoster liefern, welche sofortige Maßnahme ist angemessen, wie unterscheiden sich Update, vorübergehende Isolation und statischer Ersatz? PHP 8.2 allein belegt weder Betroffenheit noch Behebung. Keine Aussage „statisch = sicher“. Benennt Funktionsverlust gegenüber CMS/Formular und Wartungsverantwortung. Dokumentiert für eure neue Lieferung Laufzeit- und Build-/Testkomponenten mit Version/Bezugsstand oder „nicht verwendet“. Die Antwort darf agentisch vorbereitet werden; ein Mensch prüft Fakten und gibt sie frei. Kein Live-Angriff und kein verwundbarer Server erforderlich.

## 3. Eine Factory-Änderung überprüfen

Implementiert die in T4 begründete kleine Verbesserung. Wiederholt R-01 mit **F-NEW** auf einer frischen Kopie desselben **R-BASE**; identische Aufgabe und Akzeptanzkriterien, gleiches Modell und dokumentierte Einstellungen. Laufzustände/Versuchsausgaben getrennt halten. Keine Nachnutzung der fertigen R-01-Lösung aus der Baseline als versteckter Input. Untersucht nicht gleichzeitig Modellwechsel und Workflow-Änderung.

Mindestens ein vollständiger Vorher- und Nachher-Lauf; zwei je Variante sind bei Zeit empfohlen. Vergleicht Akzeptanz/Regressionen, Review-/Nacharbeitszeit, Fehler und bekannte Lieferkosten. Factory-Entwicklungsaufwand separat ausweisen. Ein einzelnes Paar erlaubt nur eine vorläufige Beobachtung. Eine erfolglose Optimierung ist bei sauberem Versuch ein gültiges Ergebnis: beibehalten, anpassen oder zurücknehmen begründen.

Falls T4 die Baseline fehlt: vor der Änderung noch mit der unveränderten Factory nachholen und als T5-Nachholung kennzeichnen; keine Baseline aus Erinnerung erfinden. Das ersetzt nicht rückwirkend den T4-Nachweis.

## 4. Abnahme und Übergabe

Liefert einen Release-Commit/Tag, Start-/Testanleitung und Wartungshinweis. Der Dozent nimmt anhand AC-01–10 ab oder protokolliert Restmängel. Falls keine Kundenentscheidung bis 15 Uhr möglich ist: technischen Freigabestand und ausstehende Kundenabnahme getrennt kennzeichnen. Keine Selbstbehauptung „vom Kunden akzeptiert“.

| Ablage | Pflichtabgabe |
|---|---|
| Produkt-Repo | CR-01-Änderung mit Review-Diff, Regressionsergebnisse, SR-01-Antwort/Komponentenübersicht, Release und Übergabe |
| Factory-Repo | realer Änderungslauf, implementierte Verbesserung, R-01-Vergleich mit Rohdaten, Kosten und Entscheidung |
| `evidence/session-05.md` | Commit-/Run-Verweise, AC-01–10, technische Freigabe und Kundenstatus, Gesamtbilanz T3–5 und drei übertragbare Erkenntnisse |

## Zeitrahmen

10:00–10:20 Änderungsanalyse; 10:20–11:20 Factory-Änderung und Vergleich; 11:20–12:00 Kundenänderung; 12:00–12:30 Pause; 12:30–13:30 Änderung/Regression abschließen; 13:30–14:10 Sicherheitsantwort; 14:10–14:35 Abnahme; 14:35–15:00 Evidenz und Bilanz.

**Definition of Done:** Versioniertes Kundenprodukt, nachvollziehbar bearbeitete Änderung, abgegrenzte Sicherheitsantwort und ehrlicher Factory-Vergleich. Positiver Optimierungseffekt ist keine Voraussetzung für das Lernziel.
