# SR-01 Sicherheitsantwort an Nordwerk Industrie-Service

**Betreff:** Sicherheitsanfrage zu PHP-Schwachstellen CVE-2026-109618 / CVE-2026-109619  
**An:** Nordwerk Industrie-Service (Hamburg)  
**Von:** PepeGroup (Team 3)  
**Datum:** 2026-11-08  
**Referenz:** SR-01

---

## Kurzantwort (max. 1 Seite)

Sehr geehrte Damen und Herren,

wir haben Ihre Anfrage bezüglich der von ENISA gemeldeten PHP-Schwachstellen CVE-2026-109618 und CVE-2026-109619 geprüft und können Ihnen folgende Einschätzung geben:

### Was ist (potenziell) betroffen?

**Ihre Nordwerk-Website: Nicht betroffen.**

Die Website von Nordwerk Industrie-Service ist eine **vollständig statische HTML/CSS-Seite** – sie enthält keinerlei PHP-Code, keine serverseitige Skript-Ausführung und keine Datei-Upload-Funktionalität. Die gemeldeten Schwachstellen betreffen ausschließlich Systeme, die PHP aktiv ausführen (CVE-2026-109618: PHP File-Upload-RCE; CVE-2026-109619: PHP-Deserialisierungs-RCE). Da Ihre Website keine dieser Eigenschaften aufweist, besteht kein direktes Angriffsrisiko durch diese CVEs.

**Automatisch verifiziert** durch unsere Testsuite (`python test_website.py`, F3-Prüffamilie): Keine PHP-Dateien, kein PHP-Marker (`<?php`), keine serverseitigen Endpunkte vorhanden.

### Welche Informationen wir vom Hoster noch benötigen

Damit wir eine vollständige Entwarnung geben können, benötigen wir folgende Bestätigung Ihres Hosting-Anbieters:

1. **Ist PHP auf dem Server installiert und/oder aktiv?** (auch wenn Ihre Website es nicht nutzt, könnten andere Anwendungen auf demselben Server betroffen sein)
2. **Welche PHP-Version wird betrieben** (falls vorhanden)?
3. **Betreiben andere Mieter/Anwendungen PHP auf derselben Server-Instanz?**
4. **Ist ein WAF (Web Application Firewall) oder eine Sandbox-Isolation aktiv?**

### Sofortige Maßnahmen

| Maßnahme | Priorität | Zuständig | Status |
|---------|-----------|-----------|--------|
| Automatischen PHP-Angriffsflächentest ausführen (`python test_website.py`) | 🔴 Sofort | PepeGroup | ✅ Bereits erledigt – Ergebnis: PASSED |
| Hoster nach PHP-Aktivierung befragen | 🟡 Diese Woche | Nordwerk | ⬜ Ausstehend |
| PHP im Hosting-Panel deaktivieren (falls aktiv) | 🟡 Nach Hoster-Auskunft | Nordwerk / Hoster | ⬜ Ausstehend |
| Reinen Static-Hoster in Betracht ziehen (z. B. GitHub Pages, Netlify) | 🟢 Mittelfristig | Nordwerk | ⬜ Optional |

### Unterschied zwischen den Optionen: Update, Isolation, Ersatz

| Option | Beschreibung | Empfehlung für Nordwerk |
|--------|-------------|------------------------|
| **Update** | PHP auf eine nicht-anfällige Version patchen | Nur relevant, falls PHP aktiv genutzt wird – bei Nordwerk nicht der Fall |
| **Isolation** | PHP-Interpreter deaktivieren oder in einem separaten Container isolieren; Website bleibt auf statischem Server | **Empfohlen**, falls Hoster PHP-Sharing betreibt |
| **Ersatz** | PHP-Anwendung vollständig durch statische Alternative ersetzen | **Bereits umgesetzt** – Nordwerk-Website ist bereits statisches HTML |

---

> **Zusammenfassung:** Ihre Website ist durch CVE-2026-109618 / CVE-2026-109619 nicht direkt gefährdet. Bitte klären Sie mit Ihrem Hoster, ob PHP auf der Server-Infrastruktur aktiv ist (Shared-Hosting-Risiko). Wir empfehlen, PHP auf Ihrem Hosting-Account zu deaktivieren oder einen rein statischen Hosting-Dienst zu nutzen.

Für Rückfragen stehen wir jederzeit zur Verfügung.

Mit freundlichen Grüßen,  
**PepeGroup (Team 3)**  
David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq

---

*Vollständige technische Analyse: [`docs/SECURITY_SR-01.md`](../docs/SECURITY_SR-01.md)*  
*Automatisierter Nachweis: `python test_website.py` → F3-Familie PASSED*
