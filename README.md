## Team setup

Die folgende Übersicht dokumentiert die Entwicklungsumgebungen und die vom
Team gemeldeten Setup-Ergebnisse für Termin 1.

| Teammitglied | Betriebssystem | Entwicklungsumgebung | Python | LLM-Zugang | Modell | Testergebnisse |
|---|---|---|---|---|---|---|
| Leon | macOS | VS Code | 3.12 | oMLX |  `Qwen3.8 27B` | Erfolgreich |
| Maxim | macOS | PyCharm | 3.12 | Ollama | `qwen3:4b` | Erfolgreich |
| Mero | macOS | PyCharm | 3.12 | Ollama | `qwen3:4b` | Erfolgreich |
| David | macOS | PyCharm | 3.12 | Ollama | `qwen3:4b` | Erfolgreich |
| Lars | Windows 11 | IntelliJ IDEA | 3.12.0 | Ollama |  `Qwen 3.5 9B` | Erfolgreich |
| Bohdan | Linux | PyCharm | 3.12 | Ollama | `qwen3:4b` | Erfolgreich |

### Abweichungen vom Starter-Setup

- **Leon:** oMLX mit Qwen3.8 27B statt Ollama mit `qwen3:4b`
- **Lars:** Qwen 3.5 9B statt des Starter-Modells `qwen3:4b`


# Agentic AI Software Company – Starter Repository

Starter repository for the HAW Hamburg elective project **Agentic AI / Human–Agent Software Company**.

The repository provides a deliberately small, common technical baseline so that teams can focus on engineering a mixed human–agent software company instead of spending the first sessions resolving incompatible frameworks.

## Course Documents / Kursunterlagen

- Project briefing: [English](task%20sheets/01_Project_Briefing_en.md) / [Deutsch](task%20sheets/01_Projektbriefing_de.md)
- Tasks for Sessions 1 and 2: [English](task%20sheets/Tasks_Session_1_and_2_en.md) / [Deutsch](task%20sheets/Aufgaben_Termin_1_und_2_de.md)
- Evaluation rubric: [English](task%20sheets/Evaluation_Rubric_Sessions_1_and_2_en.md) / [Deutsch](task%20sheets/03_Bewertungsraster_GitHub_Termin_1_und_2.md)
- Session 2 guide and update instructions: [English](docs/SESSION_02_EN.md) / [Deutsch](docs/SESSION_02_DE.md)
- Setup instructions: [English](docs/SETUP_LOCAL_EN.md) / [Deutsch](docs/SETUP_LOCAL_DE.md)

The sessions run on Mondays from **10:00 to 15:00**. Assessment evaluates the team's changes to the starter, not the supplied examples and tests.

## What is fixed

- GitHub + GitHub Issues + GitHub Actions
- Python **3.12**
- LangChain + LangGraph
- FastAPI + Pydantic
- Docker + Docker Compose
- pytest
- PostgreSQL + pgvector
- LLM via either
  - local Ollama, or
  - an OpenAI-compatible HAW ICC endpoint
- structured local trace and cost data

Additional frameworks, databases, vector stores, workflow engines, or observability platforms require prior approval.

## Important: starter code does not count as team work

Code under `examples/` and tests under `tests/starter/` are reference implementations supplied with the course.
They exist to verify that the stack is wired correctly.

For project evaluation:

> **Do not count files under `examples/` or `tests/starter/` as evidence for an implemented company agent.**

Teams must implement their own agents under `src/agents/`.

Role staffing is also part of the project. During Session 1, teams distinguish `current_actor_type` from `target_actor_type`: a role can still be performed by a human while an agent implementation is planned. Session 1 requires one own operational LangGraph agent. By the end of Session 2, at least `12 - number of human team members` roles must be operationally supported by an agent or hybrid implementation. One agent implementation may support multiple roles only when role-specific behavior and outputs are technically distinguishable and traceable.

See [`docs/STARTER_BOUNDARY.md`](docs/STARTER_BOUNDARY.md).

---

## Repository structure

```text
.
├── .github/
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── costs/
│   ├── cost-model.yaml
│   └── usage.csv
├── db/
│   └── init.sql
├── docs/
│   ├── architecture.md
│   ├── ICC_CONFIGURATION.md
│   ├── STARTER_BOUNDARY.md
│   ├── SETUP_LOCAL_DE.md
│   └── SETUP_LOCAL_EN.md
├── examples/
│   └── file_review_agent.py
├── organization/
│   ├── company.md
│   └── roles.yaml
├── src/
│   ├── agents/
│   ├── app/
│   ├── llm/
│   ├── observability/
│   └── rag/
├── task sheets/
│   ├── project briefings (German / English)
│   ├── assignments (German / English)
│   └── evaluation rubric (German)
├── tests/
│   └── starter/
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# Quick start: local Python + Docker database + native Ollama

## 1. Prerequisites

- Git
- Python 3.12
- Docker Desktop / Docker Engine with Compose
- Ollama if you want to run the LLM locally

> **Docker must be running before you use `docker compose`.**  
> On macOS and Windows, start **Docker Desktop** first. On Linux, make sure the Docker Engine/daemon is running.
>
> Verify Docker before continuing:
>
> ```bash
> docker info
> ```
>
> If this command cannot connect to the Docker daemon, `docker compose up` will fail as well.

The recommended local setup is:

- run **Ollama natively on the host machine**, and
- use **Docker Compose for PostgreSQL/pgvector** and, if desired later, application services.

This is particularly useful on macOS, where native Ollama can use Apple Metal acceleration while Docker Desktop does not provide the same GPU access to Ollama containers.

## 2. Clone and configure

```bash
git clone <YOUR-REPOSITORY-URL>
cd <YOUR-REPOSITORY>
cp .env.example .env
```

## 3. Create a Python environment

macOS / Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Start PostgreSQL + pgvector

Make sure Docker is running first:

```bash
docker info
```

Then start the database:

```bash
docker compose up -d db
```

Check it:

```bash
docker compose ps
```

## 5. Check and start Ollama locally

The starter assumes a **recent Ollama version**. Before pulling the course model, check your installed version:

```bash
ollama --version
```

Then pull the example model used by `.env.example`:

```bash
ollama pull qwen3:4b
```

### If `ollama pull` fails with HTTP 412

A message such as:

```text
Error: pull model manifest: 412:
The model you are attempting to pull requires a newer version of Ollama.
```

means that the locally installed Ollama version is too old for the current model manifest. Update Ollama using the official installer for your operating system, restart Ollama, and verify the installed version again:

```bash
ollama --version
ollama pull qwen3:4b
```

Do not work around this error by changing the project dependencies or Docker configuration. It is an Ollama client/runtime version issue.

After the model has been downloaded successfully, verify that it can be started:

```bash
ollama run qwen3:4b
```

Exit the interactive model session with `Ctrl+D` or `/bye`.

Ollama usually starts its background service automatically when the desktop application is running. If no Ollama service is active, start it manually:

```bash
ollama serve
```

If Ollama is already running, `ollama serve` is unnecessary and may report that port `11434` is already in use.

## 6. Start FastAPI locally

For local Python execution, set the Ollama URL in `.env` to:

```text
LLM_BASE_URL=http://localhost:11434
EMBEDDING_BASE_URL=http://localhost:11434
```

Then:

```bash
python -m uvicorn src.app.main:app --reload
```

Open:

- API docs: `http://localhost:8000/docs`
- service health: `http://localhost:8000/health`
- database health: `http://localhost:8000/db/health`

## 7. Run the starter tests

Run the tests through the active Python interpreter:

```bash
python -m pytest
```

The repository contains a `pytest.ini` that adds the repository root to Python's import path. This allows the starter tests to import `src` and `examples` consistently. Using `python -m pytest` is recommended because it also ensures that pytest is executed from the same Python environment in which the project dependencies were installed.

## 8. Run the supplied LangGraph reference example

This verifies LangGraph + LangChain + LLM + local trace logging:

```bash
python -m examples.file_review_agent --input src/app/main.py
```

The example writes a separate trace to `logs/<run_id>.jsonl` using `TRACE_FILE=logs/RUN_ID.jsonl`. Existing `.env` files must be updated manually. See the Session 2 guide for evidence export and costs.

Remember: this supplied example does **not** count as a team agent.

---

# Quick start: application in Docker

Copy `.env.example` to `.env` and keep:

```text
LLM_BASE_URL=http://host.docker.internal:11434
EMBEDDING_BASE_URL=http://host.docker.internal:11434
```

Then:

```bash
docker compose up --build
```

Docker Compose maps `host.docker.internal` to the Docker host also on Linux through `host-gateway`.

---

# Switching to HAW ICC

If the provided ICC service exposes an OpenAI-compatible API, configure:

```text
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://<ICC-ENDPOINT>/v1
LLM_API_KEY=<TOKEN-IF-REQUIRED>
LLM_MODEL=<ICC-MODEL-NAME>
```

The agent code should not need to change. The same principle is used for embeddings.

The exact ICC URL, model name and authentication method must be supplied by the course before use.
See [`docs/ICC_CONFIGURATION.md`](docs/ICC_CONFIGURATION.md).

---

# LangSmith

LangSmith is **not required** by this repository and is not part of the assessment baseline.

If a team has permission to use it, LangChain/LangGraph tracing can be enabled through standard LangSmith environment variables. Local JSONL tracing remains mandatory for comparable project evidence.

Do not send customer data, secrets, or protected data to an external tracing service.

---

## Detailed Setup Instructions

Installing Python, Docker, and Ollama, as well as connection tests
and troubleshooting: [Lokales Setup](docs/SETUP_LOCAL_DE.md) / [Local setup](docs/SETUP_LOCAL_EN.md).

---

# First team tasks

The starter deliberately leaves these areas incomplete:

1. complete `organization/company.md`
2. assign all roles in `organization/roles.yaml`
3. adapt `docs/architecture.md` to the team's real architecture
4. use the common course rates in `costs/cost-model.yaml` and record actual usage
5. implement at least one **team-owned** agent under `src/agents/`
6. add meaningful tests outside `tests/starter/`
7. create GitHub Issues for the work
8. produce team-owned execution traces and cost evidence

---

# Compatibility policy

The core dependency versions are pinned in `requirements.txt` to create the same baseline for all teams.
Teams should not upgrade individual LangChain/LangGraph packages independently.

If a package change is necessary:

1. create an Issue,
2. explain why the baseline is insufficient,
3. document compatibility implications,
4. request approval before merging the change.

