# Team 3 (PepeGroup) – Feedback zu Session 5

**90/100 Punkte · Sehr starker Tagesstand · Formales Tagesziel teilweise erreicht (2/4 Factory-Lernziele vollständig)**

Ihr habt den ersten Nordwerk-Kundenauftrag technisch überzeugend abgeschlossen. Die deutsche Website und die neue englische Einstiegsseite erfüllen die Anforderungen von CR-01. **Alle sieben Produkttests bestanden** bei meiner unabhängigen Prüfung. Besonders positiv sind die beiden echten Agentenläufe, die nachweisbaren Produkt-Commits und die dokumentierten menschlichen Freigaben.

Auch euer **R-01-Experiment** ist ein wichtiger Fortschritt: Die gemessene Agentenlaufzeit sank von **118,40 auf 44,48 Sekunden (−62,4 %)**; die Agentenkosten eines erfolgreichen Laufs von **9,4473 auf 8,7024 Credits (−7,9 %)**. Gut ist, dass ihr das kleine Stichprobenvolumen und das noch nicht erreichte Kostenziel ausdrücklich ansprecht.

**Drei Punkte solltet ihr für die nächsten Kundenprojekte verbessern:**

1. **Experimente vollständig reproduzierbar machen.** Friert den tatsächlich verwendeten Factory-Code *vor* dem Lauf ein und speichert auch das isolierte R-01-Ergebnis als überprüfbaren Commit oder Patch. Ändert möglichst nur einen Parameter pro Vergleich – sonst lässt sich nicht erkennen, wodurch die Beschleunigung entstand.
2. **Cost Engineering korrigieren.** Im Kurs gelten **1 Credit je CI-Lauf**, unabhängig von GitHubs tatsächlichem Free-Tier. Eure 111 erfassten Actions-Läufe dürfen deshalb nicht pauschal mit 0 Credits bewertet werden. Außerdem sind 17 CSV-Zeilen wegen nicht maskierter Kommas nicht zuverlässig maschinell lesbar.
3. **Die Übergabe kundengerecht und nachweisbar machen.** Kürzt die über 1.000 Wörter lange SR-01-Kundenantwort auf etwa eine Seite, korrigiert die kaputten Factory-zu-Produkt-Links und dokumentiert, ob die beantragte Gemini-Ausnahme tatsächlich genehmigt wurde.

**Insgesamt eine technisch starke Leistung mit erkennbarer Factory-Weiterentwicklung.** Der nächste Schritt ist, nicht nur gute Resultate zu liefern, sondern Verbesserung, Wirtschaftlichkeit und Freigaben so zu belegen, dass andere die Ergebnisse zuverlässig prüfen und reproduzieren können.
