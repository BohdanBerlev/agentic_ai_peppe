# Feedback für Team 3 – Session 2

**PepeGroup · vorläufig 60/100 Punkte – Tagesziel teilweise erreicht.**  
**Rohscore: 63/100; Obergrenze 60 wegen fehlender Rollenabdeckung bei vier Mitgliedern laut eurer aktuellen Teamdokumentation.** Der Score ist ein Engineering Health Indicator und keine Note.

**Teamgröße bitte abgleichen:** Eure aktuelle Firmenbeschreibung nennt vier Mitglieder, die frühere Kursangabe und die Session-1-Kostenzeile nennen sechs. Die Bewertung legt vier zugrunde und verlangt deshalb acht operativ unterstützte Rollen. Bei weiterhin sechs Mitgliedern wäre diese Obergrenze neu zu bewerten; mit unverändert vier anerkannten Rollen ergäben sich 67/100 Punkte.

Ihr habt vier eigene Fähigkeiten für Requirements, Architektur, QA/Security und Kostenanalyse aufgebaut. Positiv ist die echte Übergabe des Architekturberichts an den QA-/Security-Agenten. Alle **24 eigenen Tests bestanden**; insgesamt waren es 35 bestandene Tests und ein übersprungener Starter-DB-Test. Eure manuell bereinigten **16,5785 Credits** lassen sich aus den eingereichten Einzeltraces bestätigen.

Für Session 3 sind drei Punkte besonders wichtig:

1. **Menschliche Freigaben technisch absichern.** Ohne interaktives Terminal erzeugt eure Pipeline bei positiven Modellantworten automatisch `approved` unter dem Namen eines Teammitglieds. Das darf nicht als menschliche Freigabe gelten. Headless muss die Entscheidung ausstehend lassen. Der GitHub-Runner kann außerdem Issues trotz `changes_requested` oder `invalid_output` als erledigt schließen. Prüft die tatsächliche Freigabeentscheidung und ergänzt Tests für diese negativen Fälle. Im ersten Dry-Run-Trace steht `approved`, während euer Bericht „Changes Requested“ beschreibt; klärt diesen Widerspruch transparent.
2. **Rollen und Provider mit den Kursvorgaben abgleichen.** Operational-Markierungen allein genügen nicht. Der Requirements-Agent zeigt bisher keine getrennten Fähigkeiten für Project Manager, Agent Engineer und Integration Engineer. QA und Security sind in einem gemeinsamen Review kombiniert. Mehrere Rollen dürfen denselben Agenten nutzen, benötigen aber unterscheidbares Verhalten und Evidenz. Verwendet außerdem den vorgesehenen lokalen/ICC-Zugang oder belegt eine ausdrückliche Absprache zur Google-Nutzung. Der Google-Pfad ist derzeit mit den deklarierten Abhängigkeiten nicht reproduzierbar.
3. **Einen realen, getesteten Dry Run mit korrekten Kosten sichern.** Eure API-Tests ersetzen die Datenbank vollständig durch Mocks; sie belegen keine PostgreSQL-Persistenz. Der QA-/Security-Agent liest und bewertet Code, führt jedoch keine Tests aus. Ergänzt einen echten DB-Lifecycle und verknüpft ihn mit gespeicherten Testergebnissen. Behebt das Double-Counting im Cost-Agenten tatsächlich im Code und prüft es mit einem Regressionstest. Trennt menschliche Review-/Korrekturzeit von Implementierung und Wartezeit.

Zusätzlich sollten fehlende Kontextdateien vor dem nächsten LLM-Aufruf zur Eskalation führen. Eure Pipeline ruft das Modell derzeit trotz Lesefehler noch auf. Das Architekturdiagramm sollte außerdem zeigen, dass eine Nachbesserung einen neuen Lauf benötigt; eine automatische Rückschleife ist im Code nicht vorhanden.

Die technische Basis ist vorhanden. Konzentriert euch nun auf einen gemeinsamen Ablauf, dessen Rollen, Tests, Kosten und Freigaben durchgehend nachweisbar sind.
