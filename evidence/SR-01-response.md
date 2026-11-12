# SR-01: Kundenantwort zur Sicherheitsanfrage (CVE-2026-109618 & CVE-2026-109619)

**An:** Geschäftsführung & Technischer Betrieb, Nordwerk Industrie-Service (Hamburg)  
**Von:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-09 · **Status:** Menschlich geprüft & freigegeben (David Pisarkiewicz, Lars Boos)  
**Referenz:** ENISA Joint Statement vom 21.10.2026 (*Critical PHP Vulnerabilities* zu `CVE-2026-109618` & `CVE-2026-109619`); abgerufen am 08./09.11.2026 auf Basis des Kurs-Primärquellenauszugs; Abgleich mit Systemprofil vom 23.10.2026.

---

### 1. Bewertung: Altsystem vs. Neulieferung
- **Bisheriger Webauftritt (Altsystem beim Hoster, Stand 23.10.2026):**  
  Die pauschale Betreiberangabe **„PHP 8.2“ belegt weder Betroffenheit noch Behebung**. Sie nennt nur den Versionszweig, nicht aber den konkreten Patchstand (behoben erst ab PHP 8.2.35 bzw. Distributions-Backports). Da Ihnen Administratorzugang und Log-Dateien fehlen, bedeutet auch das Fehlen bekannter Angriffe **keine Entwarnung**. Das Altsystem bleibt potenziell verwundbar.
- **Neue Website-Lieferung (`CR-01-v1.0`):**  
  Unsere Auslieferung besteht ausschließlich aus statischem **HTML5 und CSS3**. Sie enthält **kein PHP, kein CMS, keine Datenbank und kein serverseitiges Skript** (automatisiert verifiziert durch Testfamilie `F3`). Im Anwendungscode besteht daher **keine Betroffenheit**.  
  *Wichtiger Hinweis:* **„Statisch“ bedeutet nicht automatisch „rundum sicher“:** Wenn der Hoster auf dem Webspace weiterhin einen ungepatchten PHP-Interpreter aktiv lässt, bleibt die Serverangriffsfläche bestehen. Webserver-Härtung, TLS/HTTPS und Zugangsabsicherung sind weiterhin zwingend erforderlich.

---

### 2. Dringende Rückfragen an Ihren Hoster
Fordern Sie vor Weiterbetrieb oder Bereitstellung schriftlich folgende Nachweise an:
1. **Exakte PHP-Paketversion:** Vollständige Versionskennung (`php -v`) inkl. Backport-Status zu den genannten CVEs und Einspieldatum.
2. **CMS- & Plugin-Patchstand:** Version des CMS sowie des Kontaktformulars und Status ausstehender Sicherheitsupdates.
3. **Log-Audit:** Prüfung der Webserver- und Zugriffsprotokolle im Zeitraum um den 21.10.2026 auf auffällige Ausnutzungsmuster.
4. **PHP-Deaktivierung:** Bestätigung, dass für das Webverzeichnis der neuen statischen Website die PHP-Skriptausführung serverseitig vollständig abgeschaltet werden kann.

---

### 3. Handlungsoptionen & Sofortempfehlung

| Option | Vorgehen | Vor- und Nachteile |
| :--- | :--- | :--- |
| **1. Update (In-Place)** | Hoster patcht PHP $\ge$ 8.2.35 und aktualisiert CMS/Formular. | **+** Voller Erhalt von CMS/Formular.<br>**−** Abhängig vom Hoster; dauerhafter Patchaufwand bleibt. |
| **2. Isolation (Akut)** | Vorübergehendes Abschalten des PHP-Interpreters / Wartungsseite. | **+** Stoppt RCE-Angriffsfläche sofort.<br>**−** Auftritt vorübergehend eingeschränkt. |
| **3. Statischer Ersatz (`CR-01-v1.0`)** | **Empfohlen:** CMS entfernen, PHP deaktivieren, statische HTML/CSS-Lieferung live schalten. | **+** Eliminiert PHP-/CMS-Schwachstellen dauerhaft; sofort startklar.<br>**−** Funktionsverlust bei CMS und Formular. |

---

### 4. Funktionsverlust & Wartungsverantwortung
- **Funktionsverlust:** Kein browserbasiertes CMS-Login mehr (Änderungen erfolgen versionskontrolliert am HTML-Quellcode); kein serverseitiges Webformular (Anfragen laufen robust über `mailto:kontakt@nordwerk.example`).
- **Verantwortung:** Hoster und Nordwerk verantworten Webserver, TLS-Zertifikate und die serverseitige PHP-Deaktivierung. PepeGroup verantwortet die inhaltliche Pflege und qualitätsgesicherte HTML/CSS-Releases.

---

### 5. Komponentenübersicht (Kriterium B4)

| Bereich | Komponente & Version | Einsatzstatus |
| :--- | :--- | :--- |
| **1. Altsystem beim Hoster** | Unbekannte Version `PHP 8.2` (Patchstand ungeklärt); CMS & Kontaktformular ohne Admin-Zugang | ⚠️ **Ungeklärt / im neuen Produkt nicht verwendet** |
| **2. Neue Kundenwebsite (`CR-01-v1.0`)** | HTML5 (`index.html`, `index_en.html`) & CSS3 (`styles.css`); PHP/JS/CMS/DB: *nicht vorhanden* | ✅ **Produktiv verwendet** (getestet mit `F1`–`F4`, `CR-01`) |
| **3. Build/Test & Factory** | Python 3.11+, `pytest`, Factory `F-NEW-v1.0` (`gemini-3.5-flash-lite`, `langgraph`) | 🔧 **Nur Entwicklungsumgebung** (nicht auf Kundenserver) |
