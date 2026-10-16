# Wahlpflichtprojekt Agentic AI – Aufgaben für Termin 1 und Termin 2

Infrastrukturupdate, verteilte Traces und DB-Tests: [Hinweise für Termin 2](../docs/SESSION_02_DE.md).

## Ausgangspunkt

Ihr arbeitet **nicht** auf einem leeren Repository.

Alle Firmen erhalten dasselbe Starter Repository.

Der Starter liefert bereits:

- Python 3.12,
- FastAPI,
- Docker / Docker Compose,
- PostgreSQL + pgvector,
- pytest,
- GitHub-Actions-Basisworkflow,
- LangChain / LangGraph,
- LLM-Provider-Abstraktion für Ollama bzw. HAW ICC,
- Trace-Hilfsfunktionen,
- Cost-Model-Template,
- Rollen- und Architektur-Templates,
- einen Referenzagenten unter `examples/`.

### Wichtig

Starter-Code ist keine studentische Leistung.

Insbesondere:

```text
examples/**
tests/starter/**
```

werden bei der Bewertung nicht als eigene Agenten- oder Testleistung gezählt.

---

# Termin 1 – Firma steht, erster Agent arbeitet

## Tagesziel

Am Ende von Termin 1 soll gelten:

> **Firma steht. Plattform läuft. Ein erster eigener Agent arbeitet, wird getestet, hinterlässt Evidenz und seine Nutzung ist messbar.**

Mehr wird an diesem Tag nicht verlangt.

---

## Aufgabe 1 – Entwicklungsumgebung einrichten und Starter verifizieren

Diese Anleitung beschreibt den empfohlenen Einstieg: **Python und FastAPI laufen direkt auf eurem Rechner, PostgreSQL/pgvector läuft in Docker, das lokale LLM läuft über Ollama auf eurem Rechner.** Alternativ verwendet ihr einen vom Kurs bereitgestellten HAW-ICC-Endpunkt.

Alle Projektbefehle werden im Stammverzeichnis des Repositories ausgeführt, also in dem Ordner mit `requirements.txt`, `docker-compose.yml` und `.env.example`.

### 1.1 Voraussetzungen vorbereiten

Installiert bzw. prüft vor dem ersten Projekttag:

| Software | Zweck | Bezugsquelle / Prüfung |
|---|---|---|
| Git | Repository und Versionsverwaltung | [Git](https://git-scm.com/downloads); `git --version` |
| Python **3.12** | Gemeinsame Python-Laufzeit | [Python](https://www.python.org/downloads/); macOS/Linux: `python3.12 --version`, Windows: `py -3.12 --version` |
| Docker Desktop (macOS/Windows) bzw. Docker Engine mit Compose (Linux) | PostgreSQL/pgvector | [Docker](https://docs.docker.com/get-started/get-docker/); `docker info` und `docker compose version` |
| Ollama, sofern ihr lokal arbeitet | LLM-Laufzeit und Modellverwaltung | Installation siehe Abschnitt 1.6 |
| Editor / IDE | Code und Konfiguration bearbeiten | Eure vorhandene Entwicklungsumgebung |

Eine andere installierte Python-Version ersetzt Python 3.12 für diesen Starter nicht. Klärt fehlende Voraussetzungen vorab. Ein erfolgreicher `python3.12 --version`- bzw. `py -3.12 --version`-Aufruf muss `Python 3.12.x` anzeigen.

**Docker muss laufen.** Öffnet auf macOS/Windows zuerst Docker Desktop und wartet, bis die Engine gestartet ist. `docker info` muss anschließend ohne Verbindungsfehler durchlaufen. Auf Linux muss der Docker-Dienst laufen und euer Benutzer Zugriff darauf haben.

### 1.2 Firmen-Repository öffnen

Verwendet das GitHub-Repository eurer Firma auf Basis des bereitgestellten Starters:

```bash
git clone <URL-EURES-FIRMEN-REPOSITORIES>
cd <ORDNER-EURES-FIRMEN-REPOSITORIES>
```

Ersetzt die Platzhalter durch eure tatsächliche Repository-URL und den entstandenen Ordnernamen. Für einen lokalen Probelauf könnt ihr zunächst das Starter-ZIP entpacken und in dessen Projektordner wechseln. Das ZIP allein enthält aber noch keine GitHub-Issues oder nachvollziehbare Firmen-Commit-Historie.

### 1.3 Python-Umgebung erstellen

**macOS / Linux:**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Falls PowerShell die Aktivierung blockiert, könnt ihr die Python-Befehle stattdessen über den Interpreter der virtuellen Umgebung ausführen:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

Bei den weiteren `python`-Aufrufen verwendet ihr dann ebenfalls `.\.venv\Scripts\python.exe`.

Wenn `.venv` bereits korrekt mit Python 3.12 eingerichtet wurde, aktiviert sie und verwendet sie weiter. Prüft nach der Aktivierung:

```bash
python --version
python -m pip --version
```

Erwartet: Python 3.12.x; der von pip angezeigte Installationspfad verweist auf eure `.venv`.

### 1.4 Projektkonfiguration anlegen und Starter-Tests ausführen

Legt beim ersten Setup die lokale Konfiguration an.

**macOS / Linux:**

```bash
cp .env.example .env
```

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

Existiert bereits eine konfigurierte `.env`, bearbeitet sie weiter, statt sie zu überschreiben. Zugangsdaten gehören nur in die lokale `.env`; diese Datei wird vom Starter aus Git ausgeschlossen.

Führt dann aus:

```bash
python -m pytest
```

**Erwartet:** Im unveränderten Starter werden vier Tests erfolgreich ausgeführt. Die Referenzagenten-Tests verwenden ein simuliertes LLM; außerdem wird der `/health`-Endpunkt getestet. Dieser Testlauf bestätigt noch keine echte LLM-Verbindung oder Datenbankverbindung. Diese prüft ihr in den folgenden Schritten separat.

### 1.5 PostgreSQL und pgvector starten

```bash
docker info
docker compose up -d db
docker compose ps
```

**Erwartet:** Der Service `db` läuft und meldet nach seiner Startphase `healthy`. Die Datenbank ist für lokal ausgeführtes Python über `localhost:5432` erreichbar. Der Starter initialisiert die pgvector-Erweiterung.

Wenn Port 5432 bereits belegt ist, prüft, ob eine andere lokale PostgreSQL-Instanz oder ein anderer Container läuft. Dokumentiert eine notwendige Portänderung; passt dann auch `DATABASE_URL` und `LANGCHAIN_POSTGRES_URL` in `.env` an.

### 1.6 Ollama installieren und das lokale LLM herunterladen

**Nur bei lokalem LLM-Zugang. Bei HAW ICC geht ihr direkt zu Abschnitt 1.7.**

Ollama ist die Laufzeit, das Sprachmodell wird anschließend separat heruntergeladen. `pip install -r requirements.txt` installiert die Python-Anbindung, aber weder die Ollama-Anwendung noch das Sprachmodell.

#### macOS

1. Öffnet [Ollama für macOS](https://ollama.com/download/mac).
2. Ladet die aktuelle Anwendung herunter und öffnet das Disk-Image.
3. Zieht `Ollama.app` in den Ordner **Programme / Applications**.
4. Startet Ollama aus diesem Ordner.
5. Falls Ollama die Einrichtung des Terminalbefehls anbietet, bestätigt sie.
6. Öffnet ein neues Terminal und prüft:

```bash
ollama --version
```

Die aktuell dokumentierte macOS-Version von Ollama setzt macOS 14 oder neuer voraus. Prüft die [offizielle macOS-Anleitung](https://docs.ollama.com/macos), falls euer Rechner abweicht.

#### Windows

1. Öffnet [Ollama für Windows](https://ollama.com/download/windows).
2. Ladet den Installer herunter und führt ihn aus.
3. Startet Ollama, falls es nach der Installation noch nicht läuft.
4. Öffnet ein neues PowerShell-Fenster und prüft:

```powershell
ollama --version
```

Weitere Voraussetzungen stehen in der [offiziellen Windows-Anleitung](https://docs.ollama.com/windows).

#### Linux

Die [offizielle Linux-Anleitung](https://docs.ollama.com/linux) verwendet:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

Auf Systemen mit systemd könnt ihr den Dienst prüfen und bei Bedarf starten:

```bash
systemctl status ollama
sudo systemctl start ollama
```

#### Modell herunterladen und ausprobieren – alle Betriebssysteme

Für den lokalen Standardpfad dieses Starters verwendet ihr `qwen3:4b`:

```bash
ollama pull qwen3:4b
ollama list
ollama run qwen3:4b
```

Der erste Befehl lädt die Modellgewichte herunter und benötigt eine Internetverbindung sowie freien Speicherplatz. Der aktuell angebotene Modell-Download ist etwa 2,5 GB groß; für die Ausführung wird zusätzlich Arbeitsspeicher benötigt. Siehe [Modellseite](https://ollama.com/library/qwen3:4b). Die Modell-Dateigröße ist keine Aussage über den gesamten RAM-Bedarf.

Gebt in der interaktiven Sitzung beispielsweise ein:

```text
Erkläre in zwei Sätzen, was ein Softwaretest prüft.
```

**Erwartet:** Das Modell erzeugt eine Antwort. Beendet die Sitzung mit `/bye`. Dies beendet den interaktiven Chat; der Ollama-Dienst soll für den anschließenden Agentenlauf weiterlaufen.

Prüft außerdem im Browser oder per HTTP-Aufruf:

```text
http://localhost:11434/api/tags
```

**Erwartet:** Eine JSON-Antwort, deren Modellliste `qwen3:4b` enthält.

Wenn kein Ollama-Dienst läuft, startet ihn in einem separaten Terminal:

```bash
ollama serve
```

Lasst dieses Terminal geöffnet. Wenn die Desktop-Anwendung oder ein Dienst Ollama bereits gestartet hat, ist `ollama serve` nicht zusätzlich nötig. Eine Meldung, dass Port 11434 bereits belegt ist, kann auf den bereits laufenden Dienst hinweisen; prüft dann `/api/tags`.

Bei einem Fehler wie `pull model manifest: 412` mit dem Hinweis auf eine neuere erforderliche Ollama-Version: Ollama aktualisieren, neu starten und `ollama pull qwen3:4b` wiederholen.

Für diesen Probelauf benötigt ihr kein Embedding-Modell. `nomic-embed-text` wird erst benötigt, wenn ihr die Embedding-/RAG-Funktionen verwendet; dann separat mit `ollama pull nomic-embed-text` herunterladen.

### 1.7 LLM-Zugang in `.env` konfigurieren

#### Option A – Ollama auf eurem Rechner

Öffnet `.env` im Editor und setzt:

```dotenv
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:4b
LLM_BASE_URL=http://localhost:11434
EMBEDDING_BASE_URL=http://localhost:11434
```

Die aktuelle `.env.example` verwendet bereits `http://localhost:11434` für beide URLs. Das passt zum empfohlenen Einstieg mit Python auf eurem Rechner. Prüft diese Werte auch in einer bereits vorhandenen `.env`. Nur wenn die Anwendung im Container läuft und Ollama auf dem Rechner bleibt, verwendet ihr für beide URLs `http://host.docker.internal:11434`. Die Datenbank läuft weiterhin in Docker.

#### Option B – HAW ICC

Die Kursleitung muss euch die konkrete URL, den Modellnamen und gegebenenfalls ein Token bereitstellen. Bei einem OpenAI-kompatiblen ICC-Endpunkt konfiguriert ihr:

```dotenv
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://<ICC-ENDPOINT>/v1
LLM_MODEL=<BEREITGESTELLTER-MODELLNAME>
LLM_API_KEY=<TOKEN-FALLS-ERFORDERLICH>
```

Ersetzt die Platzhalter durch die bereitgestellten Werte. Weitere Hinweise stehen im Starter unter `docs/ICC_CONFIGURATION.md`. Ohne diese Angaben ist der ICC-Pfad noch nicht ausführbar. Chat- und Embedding-Endpunkte können unterschiedlich sein; der erste Referenzlauf benötigt nur den Chat-Zugang.

### 1.8 FastAPI starten und Verbindung prüfen

Im Projektordner mit aktiver Python-Umgebung:

```bash
python -m uvicorn src.app.main:app --reload
```

Lasst dieses Terminal geöffnet. Öffnet im Browser:

| URL | Erwartetes Ergebnis |
|---|---|
| `http://localhost:8000/docs` | Interaktive API-Dokumentation |
| `http://localhost:8000/health` | JSON mit `status: "ok"` und konfiguriertem LLM-Provider |
| `http://localhost:8000/db/health` | `database: "ok"`; `pgvector` enthält die installierte Erweiterungsversion |

Der `/health`-Endpunkt zeigt die Konfiguration, führt aber keinen echten LLM-Aufruf aus. Diesen prüft ihr im nächsten Schritt.

### 1.9 Mitgelieferten Referenzagenten ausführen

Öffnet ein zweites Terminal, wechselt ebenfalls in den Projektordner und aktiviert dort erneut die Python-Umgebung:

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Führt dann aus:

```bash
python -m examples.file_review_agent --input src/app/main.py
```

**Erwartet:** Der Agent liest die Datei mit seinem Tool, ruft das konfigurierte LLM auf und gibt ein strukturiertes Review mit `status`, `summary` und `findings` aus. Zusätzlich entsteht ein Eintrag in `logs/<run_id>.jsonl` (`TRACE_FILE=logs/RUN_ID.jsonl`).

Ein Ergebnis `unparseable` bedeutet, dass ein Review nicht als gültiges Ergebnis geparst werden konnte. Es ist noch kein erfolgreicher fachlicher Review. Prüft die Ausgabe und dokumentiert diesen Befund.

Der Referenzagent dient ausschließlich als Stack-Test. Er ist **kein eigener Firmenagent**; auch sein Trace zählt nicht als team-eigene Execution Evidence.

### 1.10 Typische Fehler eingrenzen

| Beobachtung | Nächster Prüfschritt |
|---|---|
| `python3.12` bzw. `py -3.12` nicht gefunden | Python-3.12-Installation und Terminal-Pfad prüfen |
| `No module named pytest` oder anderes fehlendes Modul | Richtige `.venv` aktivieren; Installation mit `python -m pip install -r requirements.txt` prüfen |
| pip kann eine festgelegte Version nicht installieren | Vollständige Fehlermeldung, Python-Version und Plattform festhalten; Kursleitung informieren, statt einzelne Pakete willkürlich zu aktualisieren |
| Docker-Daemon nicht erreichbar | Docker Desktop bzw. Docker-Dienst starten; `docker info` wiederholen |
| Datenbank nicht erreichbar | `docker compose ps`, `docker compose logs db`, Port 5432 und `.env` prüfen |
| Datenbank meldet `healthy`, aber `/db/health` meldet `password authentication failed` | Abschnitt 1.10.1 durchführen; ein laufender Container bestätigt nicht das Passwort der Anwendung |
| `ollama` nicht gefunden | Installation/CLI-Einrichtung abschließen und Terminal neu öffnen |
| Ollama-Verbindung verweigert | Ollama-Anwendung/Dienst starten; `/api/tags` prüfen |
| Ollama-Modell nicht gefunden | `ollama list` prüfen und `ollama pull qwen3:4b` ausführen |
| Agent verwendet `host.docker.internal`, obwohl Python lokal läuft | `LLM_BASE_URL` in `.env` auf `http://localhost:11434` ändern |
| API-Port 8000 belegt | Bestehenden Prozess identifizieren oder für den Probelauf `--port 8001` verwenden und Browser-URLs entsprechend anpassen |

#### 1.10.1 Datenbank-Passwortfehler bei laufendem Container

Ein `healthy`-Status bestätigt die Bereitschaft des Datenbankdienstes. Er beweist nicht, dass die Anwendung sich mit ihrem konfigurierten Passwort anmelden kann. Bei einem bereits initialisierten Datenvolume ändert ein neuer Wert für `POSTGRES_PASSWORD` in `.env` das gespeicherte Rollenpasswort nicht automatisch.

1. Prüft in eurer lokalen `.env`, dass Datenbankbenutzer, Datenbankname, Port und Passwort zusammenpassen. Der Starter verwendet `agentic`, `agentic_company` und Port 5432. Das Passwort in `DATABASE_URL` und `LANGCHAIN_POSTGRES_URL` muss zum Rollenpasswort passen. Bei Sonderzeichen in einer URL ist URL-Kodierung erforderlich.
2. Prüft, dass ihr im richtigen Projektordner arbeitet und Uvicorn diese `.env` verwendet. Bereits extern gesetzte Umgebungsvariablen können die Werte aus `.env` übersteuern. Gebt keine vollständigen Verbindungs-URLs mit Passwort in Issues oder Chatnachrichten weiter.
3. Öffnet für die lokale Starter-Datenbank die psql-Sitzung im Container:

```bash
docker compose exec db psql -U agentic -d agentic_company
```

Die Befehle verwenden die Starter-Standardnamen. Habt ihr diese verändert, verwendet eure tatsächlichen Namen. In der psql-Sitzung eingeben:

```text
\password agentic
```

4. Gebt bei beiden Passwortabfragen das in eurer lokalen Konfiguration verwendete Passwort ein. Die Eingabe wird nicht angezeigt. Verlasst anschließend psql mit:

```text
\q
```

5. Beendet Uvicorn mit `Ctrl+C` und startet es erneut, damit geänderte Einstellungen übernommen werden:

```bash
python -m uvicorn src.app.main:app --reload
```

6. Prüft im zweiten Terminal die Verbindung über die tatsächlich verwendete Anwendung:

```bash
curl -i --max-time 10 http://127.0.0.1:8000/db/health
```

Unter Windows PowerShell verwendet ihr dafür `curl.exe` statt `curl`. Erwartet sind HTTP 200, `database: "ok"` und die installierte pgvector-Version. Der Probelauf mit diesem Starter meldete PostgreSQL 17.11 und pgvector 0.8.6; verwendet in eurer Dokumentation eure tatsächlich angezeigten Versionen.

**Wichtig:** Ein `psql -W`-Aufruf innerhalb des Containers erzwingt eine Passwortabfrage auch dann, wenn die dortige Authentifizierung das Passwort gar nicht verwendet. Ein erfolgreicher Aufruf allein beweist deshalb nicht, dass die Anwendung über den veröffentlichten Port mit ihrem Passwort zugreifen kann. Für den Nachweis verwendet ihr `/db/health`.

Für diese Korrektur müssen keine Datenvolumes gelöscht werden. Insbesondere ist `docker compose down -v` kein erforderlicher Schritt: Es würde die Datenvolumes entfernen.

Quellen: [PostgreSQL: psql und Passwortverwaltung](https://www.postgresql.org/docs/17/app-psql.html), [Docker: PostgreSQL-Leitfaden](https://docs.docker.com/guides/postgresql/).

#### 1.10.2 Ein HTTP-Aufruf zeigt nichts an

Verwendet zur Fehlersuche `curl -i --max-time 10` statt nur `curl -s`. So seht ihr HTTP-Status, Antwort und mögliche Verbindungsfehler. Unter Windows PowerShell verwendet ihr `curl.exe`.

Uvicorn muss in einem separaten Terminal weiterlaufen. Wenn der Server nach `Ctrl+C` beendet wurde, ist Port 8000 über diese Anwendung nicht erreichbar. Das Terminal mit Uvicorn zeigt Zugriffe auf `/db/health` und den jeweiligen Statuscode.

#### 1.10.3 Referenzlauf dauert sehr lange

Im Probelauf dauerte ein erfolgreicher Referenzlauf rund 12 Minuten und 38 Sekunden. Dies ist eine beobachtete Laufzeit, keine Soll-Laufzeit. Aus dem Trace allein ist die Ursache nicht bekannt. Ein laufender Prozess ohne Ausgabe ist noch kein abgeschlossener Lauf.

Der Ollama-Adapter setzt jetzt einen HTTP-Client-Timeout über `LLM_TIMEOUT_SECONDS` (Standard: 120 Sekunden) und eine Ausgabegrenze über `LLM_MAX_OUTPUT_TOKENS` (Standard: 768). Ein HTTP-Timeout ist keine harte Grenze für die Gesamtlaufzeit des Workflows. Wiederholt lange Läufe nicht parallel. Fehler und `Ctrl+C` werden im Referenzlauf als Trace erfasst; ein harter Prozessabbruch kann dies verhindern.

Für euren eigenen Agenten plant ihr ein explizites Ausgabe- und Zeitbudget sowie ein strukturiertes Fehlerergebnis bei Überschreitung. Die spätere eigene Implementierung wird getrennt vom mitgelieferten Referenzagenten bewertet.

Ein Referenzergebnis mit `status: "approved"` ist die Modellausgabe des Dateireviews. Es ersetzt keine menschliche Freigabe im Firmenworkflow.

### Deliverable – Team Setup dokumentieren

Ergänzt im `README.md`:

```text
## Team setup
```

mit:

- verwendeten Betriebssystemen / Entwicklungsumgebungen,
- Python-Version,
- LLM-Zugang: Ollama oder HAW ICC, einschließlich Modellname,
- notwendigen Setup-Abweichungen,
- bekannten Einschränkungen,
- Ergebnis der Starter-Tests, der Datenbankprüfung und des Referenzlaufs.

Dokumentiert beobachtete Ergebnisse; tragt bei einem noch blockierten Schritt den tatsächlichen Fehler ein.

**Hinweis für die spätere eigene Execution Evidence:** Der Starter ignoriert `logs/*.jsonl` in Git. Speichert ausgewählte, bereinigte Traces eures eigenen Agenten beispielsweise unter `evidence/session-01/`, damit sie im Repository-Snapshot nachvollziehbar sind. Schreibt dort keine Zugangsdaten oder geschützten Daten hinein.

Die Installationshinweise wurden anhand der offiziellen Ollama-Dokumentation am 5. Oktober 2026 geprüft. Für veränderte Betriebssystem-Voraussetzungen gelten die oben verlinkten Herstellerangaben.

---

## Aufgabe 2 – Firma und Rollenmodell festlegen

Bearbeitet:

```text
organization/roles.yaml
```

Alle zwölf Rollen müssen geplant und einem accountable human zugeordnet sein.

Für jede Rolle legt ihr fest:

- `current_actor_type`
- `current_actor`
- `target_actor_type`
- `target_actor`
- `accountable_human`
- `human_approval_required`
- `implementation_status`

Beispiel:

```yaml
- id: qa_test_engineer
  current_actor_type: human
  current_actor: Lisa
  target_actor_type: agent
  target_actor: qa-agent
  accountable_human: Lisa
  human_approval_required: true
  implementation_status: planned
```

Wenn euer erster eigener Agent bereits funktioniert:

```yaml
current_actor_type: hybrid
target_actor_type: hybrid
implementation_status: operational
```

### Zusätzlich

Bearbeitet:

```text
organization/company.md
```

Maximal ca. 1 Seite.

Beschreibt:

- Firmenname,
- kurze Mission,
- Entscheidungsregel,
- Eskalationsregel für Agenten,
- Regeln für spätere Rollenwechsel.

### Drei Pflichtentscheidungen

Begründet kurz:

1. Welche Rolle wird zuerst technisch durch einen Agenten unterstützt?
2. Welche Rolle bleibt zunächst bewusst menschlich?
3. Wo ist ein Human Approval Gate notwendig?

---

## Aufgabe 3 – Architektur an eure Firma anpassen

Bearbeitet:

```text
docs/architecture.md
```

Eure Version muss mindestens zeigen:

- euren ersten eigenen Agenten,
- dessen Tool,
- LLM-Zugang,
- Human Gate bzw. Eskalationspunkt,
- lokale Traces,
- Kostenpfad,
- Verbindung zur vorhandenen FastAPI-/PostgreSQL-Basis, soweit relevant.

Ein unverändertes Starter-Diagramm gilt nicht als Deliverable.

### Stack-Abweichungen

Wenn ihr eine zusätzliche Technologie benötigt, legt ein GitHub Issue an mit:

- Problem,
- gewünschter Technologie,
- Begründung,
- möglichem Nutzen,
- möglichen Kompatibilitätsrisiken.

Nutzung erst nach Absprache.

---

## Aufgabe 4 – Ersten eigenen Agenten implementieren

Implementiert unter

```text
src/agents/
```

mindestens **einen eigenen LangGraph-Agenten**.

Geeignete Rollen sind beispielsweise:

- QA & Test Engineer,
- Product Owner / Requirements Engineer,
- Software Architect,
- Cost & Observability Engineer.

Der Agent muss:

1. LangGraph tatsächlich verwenden,
2. das LLM über die vorhandene Provider-Abstraktion beziehen,
3. einen klar definierten Input besitzen,
4. ein strukturiertes Ergebnis erzeugen,
5. mindestens ein reales Tool verwenden,
6. einen sinnvollen Fehlerfall behandeln,
7. einen lokalen Execution Trace erzeugen.

### Mögliche Tools

- Repository-Datei lesen,
- pytest ausführen,
- API-Endpunkt aufrufen,
- Datenbank abfragen,
- Ergebnisdatei schreiben.

Eine reine LLM-Anfrage ohne Tool-Nutzung genügt nicht.

---

## Aufgabe 5 – Eigenen Agententest schreiben

Erstellt mindestens einen sinnvollen Test außerhalb von:

```text
tests/starter/**
```

Geeignete Tests:

- Output erfüllt ein Pydantic-Schema,
- ungültiger Input wird abgelehnt,
- Toolzugriff ist eingeschränkt,
- Workflow terminiert,
- erwartetes Artefakt wird erzeugt.

---

## Aufgabe 6 – Execution Evidence erzeugen

Führt euren eigenen Agenten mindestens einmal aus.

Im Repository muss mindestens ein team-eigener Trace nachvollziehbar sein.

Mindestens:

```text
run_id
task_id
agent
model
duration
status
tools
```

Tokenzahlen werden erfasst, wenn der Provider sie liefert.

---

## Aufgabe 7 – Nutzung und Kosten messen

Termin 1 dient zunächst dem **Aufbau der Messpipeline**, nicht der Kostenoptimierung.

Erfasst mindestens:

- menschliche Arbeitszeit des Teams,
- Anzahl eigener Agentenläufe,
- Modell,
- Laufzeit,
- Tokens, soweit verfügbar,
- Anzahl CI-Läufe,
- berechnete Credits nach dem Kurs-Kostenmodell.

Noch keine umfassende ROI-Analyse.

### Deliverable

Aktualisiert die vorgesehenen Dateien unter:

```text
costs/
```

mit tatsächlichen Daten für Termin 1.

---

## Aufgabe 8 – GitHub sinnvoll nutzen

Legt mindestens drei sinnvolle Issues für die wichtigsten Arbeiten an.

Empfohlen:

- erster eigener Agent,
- Firmen-/Rollenmodell,
- Architektur / technisches Setup.

Eine nachvollziehbare Commit-Historie ist Pflicht.

Pull Requests sind am ersten Termin **empfohlen, aber noch nicht verpflichtend**.

---

# Abgabezustand Termin 1

- [ ] Starter verifiziert
- [ ] Team Setup im README
- [ ] 12 Rollen geplant
- [ ] accountable human für jede Rolle
- [ ] current/target actor sinnvoll eingetragen
- [ ] `organization/company.md` angepasst
- [ ] `docs/architecture.md` angepasst
- [ ] mindestens 1 eigener LangGraph-Agent unter `src/agents/`
- [ ] mindestens 1 reales Tool
- [ ] strukturierter Input/Output
- [ ] sinnvoller Fehlerfall
- [ ] mindestens 1 eigener pytest-Test
- [ ] team-eigener Execution Trace
- [ ] Human Hours erfasst
- [ ] Agent Usage erfasst
- [ ] Credits berechnet
- [ ] mindestens 3 sinnvolle GitHub Issues
- [ ] nachvollziehbare Commit-Historie

---

# Termin 2 – Agentic Development Platform

## Tagesziel

Am Ende von Termin 2 besitzt eure Firma eine kleine, aber funktionierende interne Agentenplattform.

Leitfrage:

> **Können Agenten zu operativen Mitgliedern einer Engineering-Organisation werden?**

---

## Aufgabe 1 – Operative Rollenabdeckung herstellen

Bis Ende Termin 2 müssen mindestens

```text
12 - Anzahl menschlicher Teammitglieder
```

Rollen operativ durch Agenten oder hybride Lösungen unterstützt werden.

Bei:

- 6 Studierenden → mindestens 6 Rollen
- 5 Studierenden → mindestens 7 Rollen

Das bedeutet **nicht zwingend einen eigenen Agenten pro Rolle**.

Ein Agent darf mehrere Rollen unterstützen, wenn das Rollenverhalten technisch unterscheidbar und tracebar ist.

Aktualisiert:

```text
organization/roles.yaml
```

`implementation_status: operational` ist nur zulässig, wenn technische Evidenz existiert.

---

## Aufgabe 2 – Mindestens drei eigene Agentenfähigkeiten

Unter

```text
src/agents/
```

müssen mindestens drei unterscheidbare Agentenfähigkeiten / Rollenimplementierungen vorhanden sein.

Empfohlene Kombination:

1. Product Owner / Requirements
2. Developer oder Architect
3. QA & Test

Jede Fähigkeit benötigt:

- klaren Input,
- strukturierten Output,
- mindestens ein Tool,
- Fehlerbehandlung,
- Trace-Evidenz.

---

## Aufgabe 3 – Gemeinsames Task-/State-Modell

Definiert ein gemeinsames technisches Task-Modell, bevorzugt mit Pydantic.

Beispiel:

```python
class EngineeringTask(BaseModel):
    task_id: str
    task_type: str
    description: str
    assigned_role: str
    input_files: list[str] = []
```

Mindestens zwei Agenten müssen dieses Modell tatsächlich verwenden.

---

## Aufgabe 4 – Agent-to-Agent-Workflow

Implementiert einen LangGraph-Workflow mit mindestens zwei Agenten.

Beispiel:

```text
Engineering Task
      ↓
Developer Agent
      ↓
Artifact
      ↓
QA Agent
      ↓
Review
      ↓
Human Gate
```

oder:

```text
Requirement
      ↓
Requirements Agent
      ↓
Architect Agent
      ↓
Human Approval
```

Die Übergabe muss technisch über State / strukturierte Daten erfolgen.

Manuelles Copy/Paste zählt nicht.

---

## Aufgabe 5 – Human Gate integrieren

Mindestens ein Workflow muss eine explizite menschliche Freigabe oder Eskalation vorsehen.

Beispiele:

- `approved`
- `changes_requested`
- `escalate_to_human`

Die Entscheidung muss im Workflow-State oder im erzeugten Artefakt nachvollziehbar sein.

---

## Aufgabe 6 – Workflow testen

Erstellt Tests für:

- mindestens einen Erfolgsfall,
- mindestens einen Fehlerfall,
- strukturierten State / Output,
- Terminierung oder Schleifenbegrenzung.

Externe LLM-Aufrufe dürfen in Unit Tests sinnvoll gemockt werden.

---

## Aufgabe 7 – Interner Dry Run

Vor dem ersten Kundenauftrag führt ihr einen kleinen internen Engineering-Auftrag durch.

### Auftrag

Erweitert den Starter-Service um eine persistente **Work-Item-Funktion**.

Mindestens:

- Work Item anlegen,
- Work Items auflisten,
- Work Item als erledigt markieren oder löschen,
- Speicherung in PostgreSQL,
- automatisierte API-Tests.

Mindestens ein Teil der Umsetzung muss über euren Agentic Development Workflow bearbeitet werden.

### Nachweis

```text
GitHub Issue
   ↓
Engineering Task
   ↓
Agent / Human
   ↓
Artifact / Code
   ↓
Test
   ↓
Review
```

---

## Aufgabe 8 – Task-bezogenes Cost Engineering

Für den Dry Run muss mindestens nachvollziehbar sein:

- Task,
- beteiligter Agent,
- Modell,
- Calls,
- Laufzeit,
- Tokens, soweit verfügbar,
- Credits,
- menschlicher Review-/Korrekturaufwand.

### Mini-Auswertung

Erstellt:

```text
docs/dry-run-01.md
```

Maximal 1 Seite.

Beantwortet:

1. Was wurde umgesetzt?
2. Welche Menschen und Agenten waren beteiligt?
3. Wo musste ein Mensch korrigieren oder freigeben?
4. Was kostete der Workflow?
5. Welche konkrete Änderung würdet ihr beim nächsten Task ausprobieren?

---

# Abgabezustand Termin 2

Zusätzlich zu Termin 1:

- [ ] Mindestanzahl operativer agentischer/hybrider Rollen erreicht
- [ ] mindestens 3 unterscheidbare eigene Agentenfähigkeiten
- [ ] gemeinsames Task-/State-Modell
- [ ] mindestens 1 technischer Agent-to-Agent-Workflow
- [ ] mindestens 1 Human Gate
- [ ] Tests für Erfolgs- und Fehlerfall
- [ ] persistente Work-Item-Funktion mit PostgreSQL
- [ ] API-Tests
- [ ] Execution Trace für den Workflow
- [ ] Task-bezogene Agentenkosten
- [ ] Human Review-/Korrekturaufwand
- [ ] `docs/dry-run-01.md`

---

# Leitlinie

Termin 1:

> **Can we build and observe an agent?**

Termin 2:

> **Can agents become part of an engineering organization?**

Ab Termin 3:

> **Can this organization deliver value to a customer?**

