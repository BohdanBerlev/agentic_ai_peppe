# Sicherheitsanalyse & Komponentenübersicht SR-01 (CVE-2026-109618 / CVE-2026-109619)

**Erstellt / Aktualisiert:** 2026-11-09  
**Team:** PepeGroup (Team 3: David Pisarkiewicz, Maxim Bers, Lars Boos, Mehrose Farooq)  
**Kunde:** Nordwerk Industrie-Service (Hamburg)  
**Referenz:** Sicherheitsanfrage `SR-01` (Bereitgestelltes Systemprofil, Stand `23.10.2026`)  
**Primärquelle:** ENISA-Mitteilung vom **21.10.2026** (*Joint Statement on Critical PHP Vulnerabilities*, `https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities`) inkl. verlinkter PHP-Primärquelle zu **`CVE-2026-109618`** und **`CVE-2026-109619`** (Abrufdatum: `2026-11-08` / `2026-11-09`, datierter Kurs-Auszug im geschützten Lehrprojektkontext).  
**Menschliche Faktenprüfung & Freigabe (D1 / L5.3):** Geprüft und freigegeben durch **David Pisarkiewicz** und **Lars Boos** (`2026-11-09`).

---

## 1. Ausgangslage & Systemprofil des Kunden (Stand 23.10.2026)

| Merkmal | Bisheriger Auftritt (Altsystem beim Hoster) | Neue Lieferung (`client-01-website`, Release `CR-01-v1.0`) |
| :--- | :--- | :--- |
| **Technischer Aufbau** | Dynamische Website mit **CMS** und serverseitigem **Kontaktformular** | Rein statische Website (`index.html`, `index_en.html`, `styles.css`) |
| **PHP-Einsatz** | Betreiberangabe **„PHP 8.2“** *(genaue Paket-/Patchversion unbekannt)* | **Nicht verwendet** *(0 PHP-Dateien, automatisch geprüft durch `F3`)* |
| **Admin-Zugang & Patch-Nachweis** | Kein Administratorzugang; keine belastbare Aussage des Hosters zu Korrekturen | Vollständiger Quellcode- und Release-Zugriff im Git-Repository |
| **Angriffsindikatoren** | Kein Hinweis auf konkret nachgewiesenen Angriff *(aber auch keine Log-Prüfung)* | Kein serverseitiger Interpreter im Produktcode |

---

## 2. Differenzierte Betroffenheitsanalyse (L5.3 / B5)

1. **Bisheriger Auftritt (Altsystem mit „PHP 8.2“, CMS und Formular):**
   - **Betroffenheit ist offen / ungeklärt (potenzielles Risiko):** Die pauschale Angabe **„PHP 8.2“ belegt weder Betroffenheit noch Behebung**. Ob die Installation für `CVE-2026-109618` bzw. `CVE-2026-109619` verwundbar ist, hängt von der exakten Patchversion (`8.2.x`), etwaigen Security-Backports der Linux-Distribution des Hosters, der PHP-SAPI-Konfiguration sowie der CMS- und Formular-Plugin-Version ab.
   - Das Fehlen eines bereits bemerkten Angriffs ersetzt keinen Patch-Nachweis.
2. **Neue Kurswebsite (`client-01-website`, Release `CR-01-v1.0`):**
   - **Im eigenen Code nicht von PHP-CVEs betroffen:** Das ausgelieferte Produkt nutzt ausschließlich statisches HTML5 und CSS3. Unser automatisierter Test `python test_website.py` (Prüffamilie `F3`) stellt bei jedem Lauf sicher, dass keine `.php`/`.phtml`/`.phar`-Dateien, keine `<?php`-Tags und keine externen Skripte im Checkout existieren.
3. **Keine Aussage „statisch = sicher“:**
   - Eine statische Website schließt zwar Schwachstellen im PHP-Interpreter oder CMS aus, garantiert aber **nicht pauschal absolute Sicherheit**.
   - Wenn das alte CMS oder ein aktiver PHP-Interpreter im selben Webverzeichnis bzw. auf einem unzureichend isolierten Shared-Hosting-System weiterläuft, bleibt das Serverrisiko bestehen. Zudem sind Webserver-Konfiguration, HTTPS/TLS, DNS-Sicherheit und Zugangsdaten-Schutz weiterhin erforderlich.

---

## 3. Pflichtrückfragen an den externen Hoster

Vor einer Weiterverwendung des Altsystems oder Bereitstellung auf demselben Webspace muss der Hoster beantworten:
1. Welche **exakte PHP-Paket-/Patchversion** (`php -v` / Distributionspaket inkl. Security-Backports für `CVE-2026-109618` & `CVE-2026-109619`) ist installiert und wann wurde gepatcht?
2. Welche **CMS- und Kontaktformular-Versionen** laufen aktuell und sind alle Sicherheitsupdates eingespielt?
3. Wurden die **Server- und Access-Logs** seit dem 21.10.2026 auf Ausnutzungsversuche untersucht?
4. Kann für die Auslieferung der neuen statischen Website das alte CMS vollständig entfernt und die **PHP-Ausführung für die Domain komplett deaktiviert** werden?

---

## 4. Handlungsoptionen, Funktionsverlust & Wartungsverantwortung

### Vergleich: Update vs. vorübergehende Isolation vs. statischer Ersatz

| Option | Maßnahme | Bewertung & Konsequenz |
| :--- | :--- | :--- |
| **Update** | Hoster spielt PHP-8.2-Security-Patch sowie CMS-/Formular-Updates ein. | Erhält CMS & Formular, erfordert aber verlässliche Hoster-Mitwirkung und dauerhafte künftige Patch-Überwachung. |
| **Vorübergehende Isolation** | Sofortige Deaktivierung der PHP-Ausführung / des Formulars bzw. Vorschalten einer Wartungs-/Zugriffssperre bis zur Hoster-Bestätigung. | **Gebotene Sofortmaßnahme** für das Altsystem, solange keine belastbare Hoster-Auskunft vorliegt. |
| **Statischer Ersatz (`CR-01-v1.0`)** | Ablösung des PHP/CMS-Altsystems durch die statische HTML/CSS-Lieferung (`index.html`, `index_en.html`, `styles.css`) bei deaktiviertem PHP. | **Empfohlene Ziellösung** für Nordwerk: eliminiert PHP- und CMS-Angriffsfläche dauerhaft, bringt jedoch den unten genannten Funktionsverlust mit sich. |

### Funktionsverlust gegenüber dem bisherigen CMS & Kontaktformular
1. **Wegfall des Redaktions-CMS:** Inhaltsänderungen erfolgen nicht mehr im Browser-Backend, sondern durch Änderung der HTML-Dateien und Ausführung der Prüfskripte (`test_website.py`, `test_cr01.py`).
2. **Wegfall des serverseitigen Kontaktformulars:** Die Kontaktaufnahme erfolgt über `mailto:kontakt@nordwerk.example` (*„Anfrage stellen“* / *„Request information“*), wofür beim Website-Besucher ein E-Mail-Client eingerichtet sein muss (bzw. die Adresse manuell kopiert wird).

### Wartungsverantwortung
- **Hoster / Nordwerk:** Webserver-Grundbetrieb, TLS-Zertifikate, Domain/DNS sowie vollständige Deaktivierung von PHP im Auslieferungsverzeichnis.
- **PepeGroup (bzw. Nordwerk nach Übergabe):** Pflege der statischen HTML/CSS-Inhalte und Ausführung der Regressionstests (`test_website.py`, `test_cr01.py`) vor jedem neuen Release gemäß [`docs/DEPLOYMENT.md`](DEPLOYMENT.md).

---

## 5. Vollständige Komponentenübersicht (Kriterium B4)

### A. Ausgelieferte Laufzeitkomponenten des Kundenprodukts (`client-01-website`)

| Komponente | Version / Bezugsstand | Status im Kundenprodukt |
| :--- | :--- | :--- |
| `index.html` (Deutsche Ansicht) | HTML5, Release `CR-01-v1.0` (`263d007`) | ✅ **Verwendet (Laufzeit)** |
| `index_en.html` (Englische Ansicht) | HTML5, Release `CR-01-v1.0` (`5227307` / `263d007`) | ✅ **Verwendet (Laufzeit)** |
| `styles.css` (Layout & Fokus-Stile) | CSS3, lokal eingebunden | ✅ **Verwendet (Laufzeit)** |
| PHP (`PHP 8.2` o. ä.) | — | ❌ **Nicht verwendet** *(im Altsystem ungeklärt)* |
| CMS & Server-Kontaktformular | — | ❌ **Nicht verwendet** *(im Altsystem ungeklärt)* |
| Clientseitiges JavaScript / externe CDNs / Tracker | — | ❌ **Nicht verwendet** |

### B. Build-, Test- und Factory-Komponenten (nur Entwicklungsumgebung, nicht auf Kundenserver)

| Komponente | Version / Bezugsstand | Zweck |
| :--- | :--- | :--- |
| Python Laufzeit & `http.server` | Python `3.11+` / `3.14` (Standardbibliothek) | Lokale Vorschau (`localhost:8000`) & Testausführung |
| `test_website.py`, `test_cr01.py`, `test_r01.py` | Commit `263d007` (Stdlib `html.parser`, `pathlib`, `re`) | Deterministische Produkt- & Regressionsprüfung (`F1`–`F4`, `CR-01`, `R-01`) |
| `pytest` | `>= 8.3.0` (`requirements.txt`) | Test-Runner für Produkt- und Factory-Gate-Tests |
| `langgraph` / `langchain` / `langchain-core` | `>= 1.1.0` / `>= 1.2.0` (`requirements.txt`) | Orchestrierung der Agentic AI Software Factory (`F-NEW-v1.0`) |
| `langchain-google-genai` & `httpx` | `>= 4.0.0` / `>= 0.28.1` (`gemini-3.5-flash-lite`) | LLM-Anbindung mit `@lru_cache` und `InMemoryRateLimiter` |
| `pydantic` & `pydantic-settings` | `>= 2.11.0` / `>= 2.8.0` (`requirements.txt`) | Strukturierte Handover-Artefakte & Konfiguration |

---

*Kurzfassung für den Kunden (max. 1 Seite): [`evidence/SR-01-response.md`](../evidence/SR-01-response.md)*
