# Deployment, Start-/Test-Anleitung & Wartungshinweise

**Produkt:** Nordwerk Industrie-Service Website (`client-01-website`)  
**Factory:** PepeGroup Agentic AI Software Factory (`agentic_ai_peppe`)  
**Release-Versionen:** Produkt `CR-01-v1.0` (`v0.3.0`) · Factory `F-NEW-v1.0`  
**Datum:** 2026-11-09

---

## 1. Kundenprodukt unabhängig starten & testen (`client-01-website`)

Das Kundenprodukt ist vollständig eigenständig und benötigt **weder die Factory noch API-Keys oder externe Dienste**.

### Voraussetzungen
- Beliebiger statischer HTTP-Server oder Python 3.8+ (nur für den lokalen Vorschau-Server und die automatisierten Tests)
- **Kein PHP, kein CMS, kein Datenbankserver, kein Node.js erforderlich**

### Lokaler Start im Browser
```powershell
cd client-01-website
python -m http.server 8000
# -> Deutsche Ansicht:  http://localhost:8000/index.html
# -> Englische Ansicht: http://localhost:8000/index_en.html
```

### Automatisierte Produkt- und Regressionstests ausführen
```powershell
cd client-01-website
python test_website.py     # Regressionstests F1-F4 (AC-01 bis AC-08)
python test_cr01.py        # CR-01-Tests (Englische Ansicht + DE-Zielgruppe + Sprachwechsel + F1-F4)
python -m pytest test_website.py test_cr01.py -v
```

### Produktiv-Bereitstellung (Static Hosting)
Die ausgelieferte Website besteht zur Laufzeit ausschließlich aus drei statischen Dateien:
- `index.html` (Deutsche Hauptansicht inkl. Zielgruppe *„Technische Einkaufsabteilungen“* & Sprachwechsel)
- `index_en.html` (Englische Einstiegsseite gemäß `CR-01` & Rücklink zur deutschen Ansicht)
- `styles.css` (Gemeinsames responsives Stylesheet für 375 px / 1280 px inkl. `:focus-visible`-Rahmen)

---

## 2. Wartungshinweise für den Kundenbetrieb (B6 / SR-01)

1. **Inhaltliche Änderungen & Funktionsumfang:**
   - Da auf ein serverseitiges CMS und ein Web-Kontaktformular bewusst verzichtet wurde (siehe [`SR-01-response.md`](../evidence/SR-01-response.md)), erfolgen Textänderungen direkt in `index.html` bzw. `index_en.html`.
   - Nach jeder Änderung sind vor dem Upload zwingend `python test_website.py` und `python test_cr01.py` auszuführen (`Exit-Code 0`).
   - Die Kontaktaufnahme läuft über `mailto:kontakt@nordwerk.example`; das Zielpostfach `kontakt@nordwerk.example` muss beim E-Mail-Provider aktiv gepflegt werden.
2. **Webserver- & PHP-Sicherheit beim Hoster (`CVE-2026-109618` / `CVE-2026-109619`):**
   - Die statische Website selbst enthält keinen PHP-Code. Dennoch gilt **nicht** pauschal *„statisch = sicher“*:
   - Stellen Sie beim Hoster sicher, dass das alte CMS/Formular vollständig entfernt und der **PHP-Interpreter für das Verzeichnis der Website deaktiviert** ist (oder nutzen Sie ein reines Static-Hosting).
   - TLS/HTTPS-Zertifikate, Webserver-Grundsicherheit und Hoster-Zugangsdaten unterliegen weiterhin der regulären Betriebswartung durch den Hoster bzw. Nordwerk.

---

## 3. Factory-Betrieb & Reproduktion der Agenten-Läufe (`agentic_ai_peppe`)

### Voraussetzungen (nur für die Factory-Entwicklungsumgebung)
- Python 3.11+ mit `.venv` (`pip install -r requirements.txt`)
- Konfigurierter `GEMINI_API_KEY` in `.env` (wird **nur** für die Factory benötigt, niemals für die Kundenwebsite)

### Reproduktion der `CR-01`-Factory-Läufe
```powershell
# Lauf A (Englische Ansicht index_en.html):
.\.venv\Scripts\python.exe -m src.workflows.feature_pipeline `
  --task-id CR-01 --project-id client-01 --target-dir client-01-website `
  --input-file index_en.html --test-target test_cr01_en.py --issue-file issue_cr01.md `
  --desc "CR-01 Run A: Create English landing page index_en.html with mandatory contents" `
  --full-company --use-backend-agent --session session-05

# Lauf B (Deutsche Ergänzung in index.html):
.\.venv\Scripts\python.exe -m src.workflows.feature_pipeline `
  --task-id CR-01 --project-id client-01 --target-dir client-01-website `
  --input-file index.html --test-target test_cr01.py --issue-file issue_cr01.md `
  --desc "CR-01 Run B: Add target group Technische Einkaufsabteilungen and language switch to index.html" `
  --full-company --use-backend-agent --session session-05
```
