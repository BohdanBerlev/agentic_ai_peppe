# SR-01: Kundenantwort zur Sicherheitsanfrage (CVE-2026-109618 & CVE-2026-109619)

**An:** Geschäftsführung / Technischer Betrieb, Nordwerk Industrie-Service (Hamburg)  
**Von:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Datum:** 2026-11-09  
**Referenz:** Sicherheitsanfrage `SR-01` (Systemprofil Stand 23.10.2026)  
**Primärquelle:** ENISA-Mitteilung vom **21.10.2026** (*Joint Statement on Critical PHP Vulnerabilities*, `https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities`) sowie die dort verlinkten offiziellen PHP-Sicherheitsadvisories zu **`CVE-2026-109618`** und **`CVE-2026-109619`**.  
**Abrufdatum / Quellenhinweis:** Abgerufen am `2026-11-08` / `2026-11-09` auf Basis des im Kurs bereitgestellten datierten Primärquellen-Auszugs (da es sich um kursdefinierte Referenz-CVEs im geschützten Lehrprojektkontext handelt).  
**Menschliche Faktenprüfung & Freigabe (D1 / L5.3):** Geprüft und freigegeben durch **David Pisarkiewicz** und **Lars Boos** am `2026-11-09` (Abgleich gegen Systemprofil vom `23.10.2026`, ENISA-Quellenangabe und Produkttests `test_website.py` / `test_cr01.py`).

---

## 1. Was ist bekannt und was bleibt offen? (Altsystem vs. neue Website)

### A. Ihr bisheriger Webauftritt (Altsystem beim externen Hoster, Stand 23.10.2026)
- **Status:** **Potenziell betroffen – tatsächliche Betroffenheit und Patch-Status sind derzeit ungeklärt (offen).**
- **Warum „PHP 8.2“ allein weder Betroffenheit noch Behebung belegt:**  
  Laut Systemprofil läuft Ihr bisheriger Auftritt mit einem CMS, einem serverseitigen Kontaktformular und der pauschalen Betreiberangabe **„PHP 8.2“**, ohne dass Ihnen die genaue Paket-/Patchversion (z. B. `8.2.x` bzw. Distributions-Backports), die CMS-/Plugin-Versionen oder eine belastbare Korrekturaussage des Hosters vorliegen.  
  Die Angabe *„PHP 8.2“* nennt lediglich den Versionszweig (Major.Minor). Sie zeigt **nicht**, ob eine für `CVE-2026-109618` / `CVE-2026-109619` verwundbare Unterversion aktiv ist oder ob der Hoster bereits gepatchte Pakete eingespielt hat. Auch dass bisher **kein Angriff nachgewiesen** wurde, bedeutet keine Entwarnung, da ohne Administratorzugang und ohne Log-Auswertung weder eine Ausnutzung noch eine Verwundbarkeit ausgeschlossen werden kann.

### B. Unsere neue Website-Lieferung (`client-01-website`, Release `CR-01-v1.0`)
- **Status bezüglich `CVE-2026-109618` / `CVE-2026-109619`:** **Im Anwendungscode nicht betroffen.**  
  Unsere neue Lieferung besteht ausschließlich aus statischem **HTML5** (`index.html`, `index_en.html`) und **CSS3** (`styles.css`). Sie verwendet **kein PHP**, **kein CMS**, **keine Datenbank** und **kein serverseitiges Formularskript** (automatisiert verifiziert durch `python test_website.py`, Prüffamilie `F3`).
- **Wichtige Abgrenzung – „statisch“ bedeutet nicht pauschal „sicher“:**  
  Der Verzicht auf PHP schließt zwar Schwachstellen im PHP-Interpreter und CMS aus, ist aber **kein Selbstläufer („statisch = sicher“ gilt nicht)**. Wenn auf demselben Webspace oder Shared-Hosting-Server weiterhin ein ungepatchter PHP-Interpreter oder das alte CMS erreichbar bleibt, besteht das Serverrisiko fort. Zudem müssen Webserver-Härtung, TLS/HTTPS, DNS und Hosting-Zugangsdaten weiterhin regulär abgesichert werden.

---

## 2. Welche Angaben muss Ihr Hoster zwingend liefern?

Bitte fordern Sie vor einer Weiterverwendung des Altsystems bzw. vor dem Live-Gang auf demselben Hosting-Paket schriftlich folgende vier Auskünfte vom Hoster an:
1. **Exakte PHP-Paket- und Patchversion:** Vollständige Versionskennung (`php -v` bzw. Distributionspaket inkl. Backport-Status zu `CVE-2026-109618` und `CVE-2026-109619`) sowie Einspieldatum des Updates.
2. **CMS- und Formular-Versionsstand:** Genaue Version des eingesetzten CMS und des Kontaktformular-Plugins sowie Status ausstehender Sicherheitsupdates.
3. **Prüfung auf Kompromittierung:** Wurden Server- und Zugriffsprotokolle im Zeitraum vor/seit dem **21.10.2026** auf Ausnutzungsversuche geprüft?
4. **Abschaltbarkeit von PHP für den neuen Auftritt:** Bestätigung, dass das alte CMS/Formular vollständig entfernt und die PHP-Skriptausführung für das Webverzeichnis der neuen statischen Website komplett deaktiviert werden kann.

---

## 3. Angemessene Sofortmaßnahme & Vergleich der Handlungsoptionen

**Sofortige Empfehlung:** Da Sie keinen Administratorzugang haben und keine belastbare Patch-Bestätigung des Hosters vorliegt, sollten Sie sich **nicht** auf den ungeklärten Zustand des Altsystems verlassen. Verlangen Sie sofort die Hoster-Auskunft und lassen Sie bis zur Klärung entweder die **PHP-/CMS-Ausführung vorübergehend isolieren/deaktivieren** oder schalten Sie direkt auf den **statischen Ersatz (`CR-01-v1.0`)** bei deaktiviertem PHP-Interpreter um.

| Handlungsoption | Vorgehen | Wann sinnvoll? | Vor- und Nachteile für Nordwerk |
| :--- | :--- | :--- | :--- |
| **1. Update (In-Place-Patching)** | Hoster patcht PHP 8.2 auf die fehlerbereinigte Patchversion und aktualisiert CMS + Kontaktformular. | Nur wenn CMS und Webformular zwingend weiterbetrieben werden müssen **und** der Hoster zeitnah belastbar patcht. | **+** Kein Funktionsverlust.<br>**−** Volle Abhängigkeit vom Hoster; dauerhafter laufender Patch- und Wartungsaufwand für PHP & CMS bleibt bestehen. |
| **2. Vorübergehende Isolation** | Abschalten des PHP-Interpreters / Sperren des CMS & Kontaktformulars (z. B. Wartungsseite / `.htaccess`-Sperre) bis zur Hoster-Nachweisführung. | **Als sofortige Akutmaßnahme**, solange der Hoster keine Patch-Bestätigung liefert. | **+** Unterbindet sofort die potenzielle RCE-Angriffsfläche.<br>**−** Website bzw. Formular ist vorübergehend eingeschränkt; löst noch nicht die langfristige Wartungsfrage. |
| **3. Statischer Ersatz (`CR-01-v1.0`)** | Vollständiges Abschalten/Entfernen des alten CMS + PHP-Interpreters und Auslieferung unserer statischen HTML/CSS-Website (`index.html`, `index_en.html`, `styles.css`). | **Empfohlene Ziellösung** für den klar abgegrenzten Informationsauftritt von Nordwerk. | **+** Eliminiert PHP-, CMS- und Formular-Angriffsfläche dauerhaft; sofort einsatzbereit.<br>**−** **Bewusster Funktionsverlust** gegenüber CMS & Formular (siehe Abschnitt 4). |

---

## 4. Funktionsverlust gegenüber CMS/Formular & künftige Wartungsverantwortung

- **Funktionsverlust beim Wechsel auf die statische Website:**
  1. **Kein Redaktions-CMS:** Inhalte können nicht mehr über ein Browser-Login geändert werden; Textänderungen erfolgen kontrolliert an den HTML-Dateien (`index.html`, `index_en.html`) mit anschließendem Testlauf (`test_website.py`, `test_cr01.py`).
  2. **Kein serverseitiges Kontaktformular:** Statt eines direkt im Browser absendbaren Formulars nutzt die neue Website `mailto:kontakt@nordwerk.example` (*„Anfrage stellen“* / *„Request information“*). Dies setzt beim Besucher ein eingerichtetes E-Mail-Programm voraus (oder das Kopieren der E-Mail-Adresse).
- **Wartungsverantwortung im Betrieb:**
  - **Hosting-Infrastruktur, Webserver-Updates, TLS-Zertifikate & Deaktivierung von PHP:** Liegt beim **externen Hoster** (Überwachung/Beauftragung durch **Nordwerk**).
  - **Inhaltliche Pflege & geprüfte HTML/CSS-Releases:** Erfolgt bei Änderungswünschen durch das Entwicklungsteam (**PepeGroup**) bzw. nach Übergabe anhand der dokumentierten Start-/Testanleitung (`docs/DEPLOYMENT.md`). Da das ausgelieferte Produkt keine Laufzeit-Abhängigkeiten (kein PHP, kein CMS, kein JS-Framework) besitzt, fallen für die Website selbst keine laufenden Sprach-/Framework-Security-Patches an.

---

## 5. Komponentenübersicht (Kriterium B4: Altsystem vs. neue Lieferung vs. Build/Test)

| Systembereich | Komponente | Version / Bezugsstand | Einsatzstatus |
| :--- | :--- | :--- | :--- |
| **1. Altsystem beim Hoster**<br>*(Stand 23.10.2026 – abzulösen / ungeklärt)* | PHP-Laufzeitumgebung | Betreiberangabe `PHP 8.2` *(exakte Patchversion unbekannt)* | ⚠️ **Ungeklärt / im neuen Produkt nicht verwendet** |
| | Content-Management-System (CMS) & Kontaktformular | Version unbekannt *(kein Admin-Zugang)* | ⚠️ **Ungeklärt / im neuen Produkt nicht verwendet** |
| **2. Neue Kundenwebsite (`client-01-website`)**<br>*(Ausgelieferte Laufzeitkomponenten, Release `CR-01-v1.0`)* | Statisches Markup (`index.html`, `index_en.html`) | HTML5 (Living Standard, Commit `263d007`) | ✅ **Verwendet (Produktiv-Auslieferung)** |
| | Statisches Stylesheet (`styles.css`) | CSS3 (lokal ohne externe Fonts/CDNs) | ✅ **Verwendet (Produktiv-Auslieferung)** |
| | PHP / Server-Skripte / CMS / Datenbank / Webformular | — | ❌ **Nicht verwendet** *(automatisch geprüft durch `F3`)* |
| | Clientseitiges JavaScript / externe Tracker / CDNs | — | ❌ **Nicht verwendet** *(automatisch geprüft durch `F1` & `F3`)* |
| **3. Build-, Test- & Factory-Komponenten**<br>*(Nur Entwicklungsumgebung – nicht auf Kundenserver)* | Python & Lokaler Prüfserver (`http.server`) | Python `3.11+` / `3.14` (Stdlib `html.parser`, `pathlib`) | 🔧 **Nur für lokale Vorschau & automatisierte Tests** |
| | Produkt- & Regressions-Testsuite (`test_website.py`, `test_cr01.py`, `pytest`) | `pytest >= 8.3.0`, deterministische Prüffamilien `F1`–`F4` + `CR-01` | 🔧 **Nur für Build-/Gate-Prüfung** |
| | Agentic AI Factory (`langgraph`, `langchain-google-genai`, `pydantic`) | `F-NEW-v1.0`, Modell `gemini-3.5-flash-lite` | 🔧 **Nur zur Entwicklung/Generierung in der Factory** |
