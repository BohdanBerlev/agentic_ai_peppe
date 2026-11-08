# Deployment & Start-Anleitung

**Produkt:** Nordwerk Industrie-Service Website  
**Factory:** PepeGroup Agentic-AI-System  
**Version:** CR-01-v1.0 / F-NEW-v1.0  
**Datum:** 2026-11-08

---

## 1. Website-Deployment (client-01-website)

### Voraussetzungen
- Beliebiger statischer HTTP-Server (kein PHP benötigt!)
- Python 3.8+ (nur für Tests)

### Lokaler Start
```bash
cd client-01-website
python -m http.server 8000
# → http://localhost:8000 (Deutsch)
# → http://localhost:8000/index_en.html (Englisch)
```

### Tests ausführen
```bash
cd client-01-website
python test_website.py     # Regressionstests F1–F4
python test_cr01.py        # CR-01-spezifische Tests (EN-View + DE-Erweiterung)
# oder mit pytest:
python -m pytest test_website.py test_cr01.py -v
```

### Produktiv-Deployment
Die Website besteht ausschließlich aus:
- `index.html` (deutsche View)
- `index_en.html` (englische View – CR-01)
- `styles.css` (Stylesheet)

Einfach alle drei Dateien auf einen Webserver hochladen. **Kein PHP, kein Node.js, kein Backend nötig.**

---

## 2. Factory-Deployment (Agentic-AI-System)

### Voraussetzungen
- Python 3.11+
- Gemini API-Key (siehe Abschnitt 3)
- `.env`-Datei (Vorlage: `.env.example`)

### Setup
```bash
git clone https://github.com/BohdanBerlev/agentic_ai_peppe.git
cd agentic_ai_peppe
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# GEMINI_API_KEY in .env eintragen
```

### Factory-Run (CR-01 Beispiel)
```bash
python -m src.workflows.feature_pipeline \
  --task-id CR-01 \
  --project-id client-01 \
  --target-dir client-01-website \
  --input-file index.html \
  --test-target test_cr01.py \
  --issue-file client-01-website/issue_cr01.md \
  --desc "Add English landing page and extend German target groups per CR-01" \
  --full-company \
  --use-backend-agent \
  --session session-05
```

---

## 3. Wartungshinweis: Gemini API-Key

Der Gemini API-Key (`GEMINI_API_KEY`) wird ausschließlich von der **Factory** benötigt, **nicht** von der Website.

### Key-Erneuerung
1. Google AI Studio: https://aistudio.google.com/app/apikey
2. Neuen Key erstellen oder bestehenden rotieren
3. `.env`-Datei aktualisieren: `GEMINI_API_KEY=AIza...`
4. GitHub Repository Secrets aktualisieren (für CI/CD): `Settings → Secrets → GEMINI_API_KEY`

### Key-Validierung
```bash
python check_env.py   # Prüft alle Umgebungsvariablen
```

---

## 4. Wartungshinweis: PHP-Versionen (Sicherheit)

Die Nordwerk-Website nutzt **kein PHP**. Bei Hosting-Providern, die PHP standardmäßig aktivieren:

1. **PHP im Hosting-Panel deaktivieren** (empfohlen)
2. **Oder:** Reinen Static-File-Hoster verwenden (z.B. GitHub Pages, Netlify)
3. **Automatische Prüfung:** `python test_website.py` erkennt PHP-Dateien via F3-Familie

Bei CVE-Meldungen zu PHP: Diese betreffen die Nordwerk-Website **nicht direkt** (siehe `docs/SECURITY_SR-01.md`).

---

*Erstellt von PepeGroup (Team 3), Session 5.*
