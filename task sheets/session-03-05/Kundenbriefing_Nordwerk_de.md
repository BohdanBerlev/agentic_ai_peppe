# Kundenprojekt 01 – Nordwerk Industrie-Service

**Verbindliches Kundenbriefing · Termine 3–5 · Version 1.0, 23.10.2026**

## Auftrag und Ausgangslage

Wir sind Nordwerk Industrie-Service, ein fiktiver kleiner B2B-Dienstleister in Hamburg. Bisher gewinnen wir Aufträge durch Empfehlungen. Potenzielle Kunden sollen nun online verstehen, was wir leisten, für wen wir arbeiten und wie sie uns erreichen. Sie sollen eine unverbindliche Anfrage per E-Mail stellen können. Der Dozent übernimmt die Kundenrolle und dokumentiert verbindliche Klarstellungen für alle Teams.

Unser bisheriger, extern betriebener PHP-Auftritt kann redaktionell bearbeitet werden und besitzt ein Kontaktformular. Für den ersten neuen Auftritt akzeptieren wir eine statische Lösung und einen E-Mail-Link. CMS und Formular gehören nicht zum Auftrag. Die spätere Sicherheitsanfrage ist eine separate Beratung innerhalb dieses Projekts.

## Verbindliche Inhalte für den ersten Release Candidate

| Kennung | Inhalt |
|---|---|
| N-01 | Firmenname: **Nordwerk Industrie-Service** |
| N-02 | Hauptaussage: **Praktische Unterstützung für Ihren technischen Betrieb.** |
| N-03 | Wartungsplanung: **Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.** |
| N-04 | Ersatzteilkoordination: **Wir unterstützen bei der Abstimmung von Ersatzteilbedarfen und Lieferterminen.** |
| N-05 | Betriebsdokumentation: **Wir bringen technische Unterlagen in eine nachvollziehbare und nutzbare Struktur.** |
| N-06 | Zielgruppen: **Kleine Produktionsbetriebe** und **Technische Serviceunternehmen** |
| N-07 | Arbeitsweise: **Ein fester Ansprechpartner, ein gemeinsam vereinbarter Leistungsumfang und nachvollziehbare Ergebnisse.** |
| N-08 | Kontakt: **Anfrage stellen** mit `mailto:kontakt@nordwerk.example` |
| N-09 | Übungshinweis: **Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.** |

Die `.example`-Adresse ist ein Platzhalter; keine Nachricht versenden. Keine erfundenen Kundenlogos, Zertifizierungen, Referenzen, Reaktionszeiten oder Erfolgszahlen ergänzen. Die Pflichttexte dürfen mit Layout und Überschriften ergänzt werden, ihr sachlicher Gehalt bleibt erhalten. Ein Logo ist optional; Bilder und externe Schrift-/Trackingdienste sind nicht erforderlich.

## Akzeptanzkriterien

| ID | Prüfung | Fällig |
|---|---|---|
| AC-01 | Firmenname und Hauptaussage sind auf der Startansicht auffindbar. | T3 |
| AC-02 | Alle drei Leistungen mit zugehörigem Inhalt sind erkennbar. | T4 |
| AC-03 | Beide Zielgruppen und die Arbeitsweise sind enthalten; keine erfundenen Leistungsversprechen. | T4 |
| AC-04 | Klar benannter Kontaktlink öffnet `mailto:kontakt@nordwerk.example`; Übungshinweis ist sichtbar. | T3 |
| AC-05 | Navigation führt zu Leistungen und Kontakt; interne Links und lokale Assets funktionieren. | T4 |
| AC-06 | Bei 375 px und 1280 px Breite kein horizontaler Inhaltsüberlauf; Text und Kontakt sind nutzbar. | T4 |
| AC-07 | Dokumenttitel, deutsche Sprachkennzeichnung, sinnvolle Überschriften und erkennbare Tastaturfokusse; Bilder, falls vorhanden, mit passendem Alternativtext. | T4 |
| AC-08 | Frischer Produkt-Checkout startet mit dokumentiertem Befehl ohne Factory/LLM/Factory-Datenbank; Produkttests laufen separat. | T4 |
| AC-09 | CR-01 aus Termin 5 erfüllt; deutsche Inhalte, Navigation und Kontakt funktionieren weiterhin. | T5 |
| AC-10 | Komponentenübersicht, abgegrenzte Antwort auf SR-01 und dokumentierte Kundenabnahme liegen vor. | T5 |

T3 verlangt außerdem eine erste Leistung aus AC-02. T4 verlangt AC-01 bis AC-08. Eine einzelne Seite mit Sprungmarken genügt. T5 ergänzt ausschließlich die im Aufgabenblatt angegebene Änderung CR-01 und Sicherheitsanfrage SR-01. Keine Zahlung, Registrierung, Analytics, echte personenbezogene Daten oder öffentliche Bereitstellung erforderlich. Die Abnahme ist eine Kursabnahme, keine Bestätigung rechtlicher Produktionsreife.

## Liefer- und Evidenzvertrag

Das bestehende Team-Repo ist die **Factory**; ein neues Repo `client-01-website` enthält ausschließlich das Kundenprodukt einschließlich Produkttests und Lieferdokumentation. Namen dürfen abweichen. Der Factory-Pflichtstack aus Termin 1/2 bleibt bestehen. Für das Produkt sind HTML/CSS, wenig JavaScript und ein einfacher lokaler Webserver ohne Zusatzfreigabe zulässig. Kein PHP/CMS-Neubau erforderlich. Weitere Frameworks nur nach bisheriger Kursregel. Keine neuen Agentenzahl-Quoten in diesem Projekt; bestehende organisatorische Rollenregeln bleiben bestehen.

Ein realer Durchlauf umfasst: Kunden-Task → mindestens zwei strukturierte, technisch zusammenarbeitende Agentenfähigkeiten → echter LLM-Aufruf über die vorhandene Provider-Abstraktion → reales Tool auf dem Produkt-Checkout → Produktartefakt/Patch → Prüfung → menschliche Freigabe oder Ablehnung. Der Agentenanteil muss eine substanzielle, überprüfbare Anforderung, Produktänderung oder Prüfung erzeugen; bloßes Umschreiben der README reicht nicht. Mindestens ein Agent muss selbst eine Produktdatei bearbeiten oder einen anwendbaren Patch erzeugen. Manuelle Umsetzung, Patch-Anwendung und Korrektur sind erlaubt und werden protokolliert. Ein externer Chat oder Editor-Assistent allein ist kein Factory-Nachweis.

Pro Lauf eindeutige `run_id`; projektbezogene Ablage, beispielsweise `runs/website-01/<run_id>/`. Eingabe-/Ergebnis-Commit, Factory-Commit, Issue/Task, Akzeptanzkriterien, Modell/Einstellungen, Agentenrollen, Tool-Aktionen, Ergebnis, Prüfbericht, Freigabe sowie Kosten sind verknüpft. Eingabe-Commit wird vor Start fixiert; Laufmanifest und zugehörige Nachweisdateien werden anschließend in einem eigenen Evidenz-Commit abgelegt. So entsteht kein zirkulärer Commit-Verweis. Rohtraces separat oder als zugängliches CI-Artefakt mit dauerhafter Zusammenfassung; keine Überschreibung gemeinsamer Logs. Ein Trace muss keine internen Modellgedanken enthalten: Inputs/Outputs, Aktionen und Ergebnisse genügen.

Geheimnisse bleiben außerhalb der Repos. Laufende Agenten dürfen nur den freigegebenen Produktbereich ändern; getrennte Run-Verzeichnisse bleiben beschreibbar. Beispieltest für abgewiesene Schreibzugriffe ausschließlich in einer temporären Testumgebung. Änderungen an der Factory selbst erfolgen als menschlich verantwortete Engineering-Arbeit.

## Kosten und Tagesabschluss

Das vorhandene Kostenmodell gilt: Mensch 100 Credits pro Personenstunde; Agentenaufruf 1 Credit plus 0,01/s, Input 0,02/1.000 Tokens, Output 0,04/1.000 Tokens; CI-Lauf 1 Credit. Tokens, falls nicht verfügbar, als unbekannt kennzeichnen, bekannte Kosten als Teilkosten ausweisen. Keine fiktiven Nullwerte. Menschliche Tätigkeiten exklusiv als Factory-Entwicklung, Lieferung, Review oder Nacharbeit erfassen; nicht zusätzlich dieselbe Zeit als allgemeine Arbeitszeit addieren. Fehlversuche und verworfene Ergebnisse zählen. Modellkredits sind keine Euro-Kalkulation.

Zu Beginn von T3 vereinbart jedes Team mit dem Dozenten ein dokumentiertes Planbudget für die Lieferung T3/T4, getrennt von Factory-Entwicklung, sowie eine Reserve für T5. Ohne Vorgabe gilt die begründete Teamplanung als Ausgangswert; es gibt kein verborgenes einheitliches Kostenlimit und keine Punkte für das kleinste Budget. Abweichungen erklären, nicht Daten anpassen.

Pro Termin wird im Factory-Repo `evidence/session-0N.md` abgegeben: Factory-/Produkt-Repo und Commitstände, relevante Tasks/PRs, Run-IDs, AC-Prüfung, Kosten, Freigaben, maximal drei nächste Schritte. Kein umfangreicher zusätzlicher Tagesbericht nötig.
