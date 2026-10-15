# Local setup of the Agentic AI starter

This guide is intended for `docs/SETUP_LOCAL_EN.md` in the starter repository. It describes installation and verification without providing a worked company solution in advance.

## Task 1 – Set up the development environment and verify the starter

This guide describes the recommended starting configuration: **Python and FastAPI run directly on your computer, PostgreSQL/pgvector runs in Docker, and the local LLM runs through Ollama on your computer.** Alternatively, use a HAW ICC endpoint provided by the course.

Run all project commands in the repository root, which is the directory containing `requirements.txt`, `docker-compose.yml`, and `.env.example`.

### 1.1 Prepare the prerequisites

Install or check the following before the first project day:

| Software | Purpose | Download / check |
|---|---|---|
| Git | Repository and version control | [Git](https://git-scm.com/downloads); `git --version` |
| Python **3.12** | Shared Python runtime | [Python](https://www.python.org/downloads/); macOS/Linux: `python3.12 --version`, Windows: `py -3.12 --version` |
| Docker Desktop (macOS/Windows) or Docker Engine with Compose (Linux) | PostgreSQL/pgvector | [Docker](https://docs.docker.com/get-started/get-docker/); `docker info` and `docker compose version` |
| Ollama, if you work locally | LLM runtime and model management | See Section 1.6 for installation |
| Editor / IDE | Editing code and configuration | Your existing development environment |

Another installed Python version does not replace Python 3.12 for this starter. Resolve missing prerequisites in advance. A successful `python3.12 --version` or `py -3.12 --version` command must report `Python 3.12.x`.

**Docker must be running.** On macOS/Windows, open Docker Desktop first and wait until the engine has started. `docker info` must then complete without connection errors. On Linux, the Docker service must be running and your user must have access to it.

### 1.2 Open your company repository

Use your company's GitHub repository based on the supplied starter:

```bash
git clone <YOUR-COMPANY-REPOSITORY-URL>
cd <YOUR-COMPANY-REPOSITORY-DIRECTORY>
```

Replace the placeholders with your actual repository URL and the resulting directory name. For a local trial run, you can first extract the starter ZIP and change into its project directory. The ZIP alone does not include GitHub issues or a traceable company commit history.

### 1.3 Create the Python environment

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

If PowerShell blocks activation, you can instead run the Python commands through the virtual environment's interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

For subsequent `python` commands, also use `.\.venv\Scripts\python.exe` in that case.

If `.venv` has already been correctly created with Python 3.12, activate it and continue using it. After activation, check:

```bash
python --version
python -m pip --version
```

Expected: Python 3.12.x; the installation path reported by pip points to your `.venv`.

### 1.4 Create the project configuration and run the starter tests

Create the local configuration during the initial setup.

**macOS / Linux:**

```bash
cp .env.example .env
```

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

If a configured `.env` already exists, continue editing it instead of overwriting it. Credentials belong only in the local `.env`; the starter excludes this file from Git.

Then run:

```bash
python -m pytest
```

**Expected:** Four tests pass in the unmodified starter. The reference agent tests use a simulated LLM, and the `/health` endpoint is also tested. This test run does not yet confirm a real LLM connection or database connection. You will check these separately in the following steps.

### 1.5 Start PostgreSQL and pgvector

```bash
docker info
docker compose up -d db
docker compose ps
```

**Expected:** The `db` service is running and reports `healthy` after its startup phase. Python running locally can reach the database at `localhost:5432`. The starter initializes the pgvector extension.

If port 5432 is already in use, check whether another local PostgreSQL instance or container is running. Document any necessary port change and update `DATABASE_URL` and `LANGCHAIN_POSTGRES_URL` in `.env` accordingly.

### 1.6 Install Ollama and download the local LLM

**Only for local LLM access. If you use HAW ICC, proceed directly to Section 1.7.**

Ollama is the runtime; the language model is downloaded separately afterwards. `pip install -r requirements.txt` installs the Python integration, but neither the Ollama application nor the language model.

#### macOS

1. Open [Ollama for macOS](https://ollama.com/download/mac).
2. Download the current application and open the disk image.
3. Drag `Ollama.app` into the **Applications** folder.
4. Start Ollama from that folder.
5. If Ollama offers to set up the terminal command, confirm it.
6. Open a new terminal and check:

```bash
ollama --version
```

The currently documented macOS version of Ollama requires macOS 14 or later. Check the [official macOS guide](https://docs.ollama.com/macos) if your computer differs.

#### Windows

1. Open [Ollama for Windows](https://ollama.com/download/windows).
2. Download and run the installer.
3. Start Ollama if it is not already running after installation.
4. Open a new PowerShell window and check:

```powershell
ollama --version
```

Further prerequisites are listed in the [official Windows guide](https://docs.ollama.com/windows).

#### Linux

The [official Linux guide](https://docs.ollama.com/linux) uses:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

On systems using systemd, you can check the service and start it if necessary:

```bash
systemctl status ollama
sudo systemctl start ollama
```

#### Download and try the model – all operating systems

Use `qwen3:4b` for this starter's default local setup:

```bash
ollama pull qwen3:4b
ollama list
ollama run qwen3:4b
```

The first command downloads the model weights and requires an internet connection and free storage space. The currently offered model download is approximately 2.5 GB; execution requires additional RAM. See the [model page](https://ollama.com/library/qwen3:4b). The model file size does not indicate total RAM requirements.

In the interactive session, enter, for example:

```text
Explain in two sentences what a software test checks.
```

**Expected:** The model generates a response. Exit the session with `/bye`. This ends the interactive chat; the Ollama service should remain running for the subsequent agent run.

Also check in a browser or through an HTTP request:

```text
http://localhost:11434/api/tags
```

**Expected:** A JSON response whose model list includes `qwen3:4b`.

If no Ollama service is running, start it in a separate terminal:

```bash
ollama serve
```

Leave this terminal open. If the desktop application or a service has already started Ollama, an additional `ollama serve` command is unnecessary. A message that port 11434 is already in use may indicate an existing service; check `/api/tags` in that case.

If an error such as `pull model manifest: 412` states that a newer Ollama version is required, update Ollama, restart it, and repeat `ollama pull qwen3:4b`.

You do not need an embedding model for this trial run. `nomic-embed-text` is needed only when using the embedding/RAG features; download it separately with `ollama pull nomic-embed-text` at that point.

### 1.7 Configure LLM access in `.env`

#### Option A – Ollama on your computer

Open `.env` in your editor and set:

```dotenv
LLM_PROVIDER=ollama
LLM_MODEL=qwen3:4b
LLM_BASE_URL=http://localhost:11434
EMBEDDING_BASE_URL=http://localhost:11434
```

The current `.env.example` already uses `http://localhost:11434` for both URLs. This matches the recommended setup with Python running on your computer. Check these values in an existing `.env` as well. If the application runs in a container while Ollama remains on the host, use `http://host.docker.internal:11434` for both URLs instead. The database continues to run in Docker.

#### Option B – HAW ICC

The course instructor must provide the specific URL, model name, and a token if required. For an OpenAI-compatible ICC endpoint, configure:

```dotenv
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://<ICC-ENDPOINT>/v1
LLM_MODEL=<PROVIDED-MODEL-NAME>
LLM_API_KEY=<TOKEN-IF-REQUIRED>
```

Replace the placeholders with the supplied values. Further information is available in the starter under `docs/ICC_CONFIGURATION.md`. Without these details, the ICC configuration is not yet runnable. Chat and embedding endpoints may differ; the first reference run requires only chat access.

### 1.8 Start FastAPI and check the connection

In the project directory with the Python environment activated:

```bash
python -m uvicorn src.app.main:app --reload
```

Leave this terminal open. Open the following URLs in a browser:

| URL | Expected result |
|---|---|
| `http://localhost:8000/docs` | Interactive API documentation |
| `http://localhost:8000/health` | JSON with `status: "ok"` and the configured LLM provider |
| `http://localhost:8000/db/health` | `database: "ok"`; `pgvector` contains the installed extension version |

The `/health` endpoint displays the configuration but does not make a real LLM call. You will check that in the next step.

### 1.9 Run the supplied reference agent

Open a second terminal, change into the project directory there as well, and activate the Python environment again:

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Then run:

```bash
python -m examples.file_review_agent --input src/app/main.py
```

**Expected:** The agent reads the file using its tool, calls the configured LLM, and returns a structured review with `status`, `summary`, and `findings`. It also creates an entry in `logs/<run_id>.jsonl` (`TRACE_FILE=logs/RUN_ID.jsonl`).

An `unparseable` result means that the review could not be parsed as a valid result. It is not yet a successful substantive review. Check the output and document this finding.

The reference agent serves only as a stack test. It is **not your own company agent**, and its trace does not count as team-owned execution evidence.

### 1.10 Troubleshoot common errors

| Observation | Next check |
|---|---|
| `python3.12` or `py -3.12` not found | Check the Python 3.12 installation and terminal PATH |
| `No module named pytest` or another missing module | Activate the correct `.venv`; check installation with `python -m pip install -r requirements.txt` |
| pip cannot install a pinned version | Record the full error message, Python version, and platform; inform the course instructor instead of arbitrarily upgrading individual packages |
| Docker daemon unreachable | Start Docker Desktop or the Docker service; repeat `docker info` |
| Database unreachable | Check `docker compose ps`, `docker compose logs db`, port 5432, and `.env` |
| Database reports `healthy`, but `/db/health` reports `password authentication failed` | Follow Section 1.10.1; a running container does not confirm the application's password |
| `ollama` not found | Complete installation/CLI setup and reopen the terminal |
| Ollama connection refused | Start the Ollama application/service; check `/api/tags` |
| Ollama model not found | Check `ollama list` and run `ollama pull qwen3:4b` |
| Agent uses `host.docker.internal` although Python runs locally | Change `LLM_BASE_URL` in `.env` to `http://localhost:11434` |
| API port 8000 already in use | Identify the existing process or use `--port 8001` for the trial run and adjust browser URLs accordingly |

#### 1.10.1 Database password error with a running container

A `healthy` status confirms that the database service is ready. It does not prove that the application can log in with its configured password. For an already initialized data volume, a new `POSTGRES_PASSWORD` value in `.env` does not automatically change the stored role password.

1. In your local `.env`, check that the database user, database name, port, and password match. The starter uses `agentic`, `agentic_company`, and port 5432. The password in `DATABASE_URL` and `LANGCHAIN_POSTGRES_URL` must match the role password. Special characters in a URL require URL encoding.
2. Check that you are working in the correct project directory and that Uvicorn uses this `.env`. Environment variables already set externally may override `.env` values. Do not share complete connection URLs containing passwords in issues or chat messages.
3. Open a psql session inside the container for the local starter database:

```bash
docker compose exec db psql -U agentic -d agentic_company
```

These commands use the starter's default names. If you changed them, use your actual names. In the psql session, enter:

```text
\password agentic
```

4. At both password prompts, enter the password used in your local configuration. Your input is not displayed. Then exit psql with:

```text
\q
```

5. Stop Uvicorn with `Ctrl+C` and restart it so that changed settings take effect:

```bash
python -m uvicorn src.app.main:app --reload
```

6. In the second terminal, check the connection through the application actually being used:

```bash
curl -i --max-time 10 http://127.0.0.1:8000/db/health
```

In Windows PowerShell, use `curl.exe` instead of `curl`. Expected results are HTTP 200, `database: "ok"`, and the installed pgvector version. The trial run with this starter reported PostgreSQL 17.11 and pgvector 0.8.6; document the versions actually displayed in your environment.

**Important:** A `psql -W` command inside the container forces a password prompt even if authentication there does not use the password. A successful command alone therefore does not prove that the application can connect with its password through the published port. Use `/db/health` as evidence.

No data volumes need to be deleted for this correction. In particular, `docker compose down -v` is not a required step: it would remove the data volumes.

Sources: [PostgreSQL: psql and password management](https://www.postgresql.org/docs/17/app-psql.html), [Docker: PostgreSQL guide](https://docs.docker.com/guides/postgresql/).

#### 1.10.2 An HTTP request shows no output

For troubleshooting, use `curl -i --max-time 10` rather than only `curl -s`. This shows the HTTP status, response, and possible connection errors. In Windows PowerShell, use `curl.exe`.

Uvicorn must remain running in a separate terminal. If the server was stopped with `Ctrl+C`, this application is no longer reachable on port 8000. The Uvicorn terminal shows requests to `/db/health` and their status codes.

#### 1.10.3 The reference run takes a very long time

In the trial run, a successful reference run took approximately 12 minutes and 38 seconds. This is an observed runtime, not a target runtime. The trace alone does not establish the cause. A running process with no output is not yet a completed run.

The Ollama adapter now sets an HTTP client timeout through `LLM_TIMEOUT_SECONDS` (default: 120 seconds) and an output limit through `LLM_MAX_OUTPUT_TOKENS` (default: 768). An HTTP timeout is not a hard deadline for the entire workflow. Do not repeat long runs in parallel. Errors and `Ctrl+C` are traced by the reference runner; a hard process termination can prevent this.

For your own agent, plan an explicit output and time budget, and a structured error result if the budget is exceeded. Your subsequent implementation is assessed separately from the supplied reference agent.

A reference result with `status: "approved"` is the model's output from the file review. It does not replace human approval in your company workflow.

### Deliverable – Document the team setup

Add the following section to `README.md`:

```text
## Team setup
```

Include:

- operating systems / development environments used,
- Python version,
- LLM access: Ollama or HAW ICC, including the model name,
- necessary setup deviations,
- known limitations,
- results of the starter tests, database check, and reference run.

Document observed results; if a step is still blocked, record the actual error.

**Note for your subsequent execution evidence:** The starter ignores `logs/*.jsonl` in Git. Save selected, sanitized traces of your own agent under a path such as `evidence/session-01/` so they are visible in the repository snapshot. Do not include credentials or protected data.

The installation instructions were checked against the official Ollama documentation on 5 October 2026. If operating system prerequisites change, the manufacturer's documentation linked above takes precedence.


## After successful setup

Continue with the task sheet: plan the company concept and twelve roles, adapt the architecture, and develop your own agent with explicit limits. The four starter tests and the reference run verify the technical setup; Session 1 additionally requires your own code, your own tests, real execution evidence, and usage records.

For student companies, issues and commits are part of the submission. A local trial run by the course instructor can be saved separately and does not have to be incorporated into the shared starter repository as a worked example.

