# Agentic AI Elective Project – Tasks for Sessions 1 and 2

Infrastructure update, distributed traces and DB tests: [Session 2 guide](../docs/SESSION_02_EN.md).

## Starting point

You are **not** starting with an empty repository.

All companies receive the same starter repository.

The starter already provides:

- Python 3.12,
- FastAPI,
- Docker / Docker Compose,
- PostgreSQL + pgvector,
- pytest,
- a basic GitHub Actions workflow,
- LangChain / LangGraph,
- an LLM provider abstraction for Ollama or HAW ICC,
- trace helper functions,
- a cost model template,
- role and architecture templates,
- a reference agent under `examples/`.

### Important

Starter code does not count as student work.

In particular:

```text
examples/**
tests/starter/**
```

do not count as evidence of your own agent implementations or tests in the assessment.

---

# Session 1 – The company is established and the first agent works

## Goal for the day

By the end of Session 1:

> **The company is established. The platform runs. A first agent of your own works, is tested, produces evidence, and its usage can be measured.**

No more than this is required on the first day.

---

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

---

## Task 2 – Define the company and role model

Edit:

```text
organization/roles.yaml
```

All twelve roles must be planned and assigned to an accountable human.

For each role, define:

- `current_actor_type`
- `current_actor`
- `target_actor_type`
- `target_actor`
- `accountable_human`
- `human_approval_required`
- `implementation_status`

Example:

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

If your first agent of your own already works:

```yaml
current_actor_type: hybrid
target_actor_type: hybrid
implementation_status: operational
```

### Also

Edit:

```text
organization/company.md
```

Maximum length: approximately one page.

Describe:

- company name,
- brief mission,
- decision rule,
- escalation rule for agents,
- rules for subsequent role changes.

### Three required decisions

Briefly explain:

1. Which role will first receive technical support from an agent?
2. Which role will deliberately remain human initially?
3. Where is a human approval gate necessary?

---

## Task 3 – Adapt the architecture to your company

Edit:

```text
docs/architecture.md
```

Your version must show at least:

- your first agent of your own,
- its tool,
- LLM access,
- human gate or escalation point,
- local traces,
- cost tracking path,
- connection to the existing FastAPI/PostgreSQL baseline, where relevant.

An unchanged starter diagram does not count as a deliverable.

### Stack deviations

If you need an additional technology, create a GitHub issue containing:

- the problem,
- the proposed technology,
- justification,
- potential benefits,
- possible compatibility risks.

Use it only after consultation with the course instructor.

---

## Task 4 – Implement your first agent

Under:

```text
src/agents/
```

implement at least **one LangGraph agent of your own**.

Suitable roles include:

- QA & Test Engineer,
- Product Owner / Requirements Engineer,
- Software Architect,
- Cost & Observability Engineer.

The agent must:

1. actually use LangGraph,
2. obtain the LLM through the existing provider abstraction,
3. have a clearly defined input,
4. produce a structured result,
5. use at least one real tool,
6. handle a meaningful error case,
7. generate a local execution trace.

### Possible tools

- read a repository file,
- run pytest,
- call an API endpoint,
- query the database,
- write a result file.

A plain LLM request without tool use is insufficient.

---

## Task 5 – Write your own agent test

Create at least one meaningful test outside:

```text
tests/starter/**
```

Suitable tests include:

- output conforms to a Pydantic schema,
- invalid input is rejected,
- tool access is restricted,
- the workflow terminates,
- the expected artifact is generated.

---

## Task 6 – Generate execution evidence

Run your own agent at least once.

At least one team-owned trace must be available and traceable in the repository.

Include at least:

```text
run_id
task_id
agent
model
duration
status
tools
```

Record token counts if the provider supplies them.

---

## Task 7 – Measure usage and costs

Session 1 initially focuses on **building the measurement pipeline**, not cost optimization.

Record at least:

- the team's human working time,
- number of runs of your own agents,
- model,
- runtime,
- tokens, where available,
- number of CI runs,
- credits calculated using the course cost model.

A comprehensive ROI analysis is not yet required.

### Deliverable

Update the designated files under:

```text
costs/
```

with actual data for Session 1.

---

## Task 8 – Use GitHub meaningfully

Create at least three meaningful issues for the most important work.

Recommended topics:

- your first agent,
- company / role model,
- architecture / technical setup.

A traceable commit history is mandatory.

Pull requests are **recommended but not yet mandatory** in the first session.

---

# Submission checklist for Session 1

- [ ] Starter verified
- [ ] Team setup in README
- [ ] 12 roles planned
- [ ] Accountable human for every role
- [ ] Current/target actor entries are meaningful
- [ ] `organization/company.md` adapted
- [ ] `docs/architecture.md` adapted
- [ ] At least 1 LangGraph agent of your own under `src/agents/`
- [ ] At least 1 real tool
- [ ] Structured input/output
- [ ] Meaningful error case
- [ ] At least 1 pytest test of your own
- [ ] Team-owned execution trace
- [ ] Human hours recorded
- [ ] Agent usage recorded
- [ ] Credits calculated
- [ ] At least 3 meaningful GitHub issues
- [ ] Traceable commit history

---

# Session 2 – Agentic Development Platform

## Goal for the day

By the end of Session 2, your company has a small but functioning internal agent platform.

Guiding question:

> **Can agents become operational members of an engineering organization?**

---

## Task 1 – Establish operational role coverage

By the end of Session 2, at least:

```text
12 - number of human team members
```

roles must receive operational support from agents or hybrid solutions.

For example:

- 6 students → at least 6 roles
- 5 students → at least 7 roles

This does **not necessarily mean a separate agent for every role**.

An agent may support multiple roles if its role-specific behavior is technically distinguishable and traceable.

Update:

```text
organization/roles.yaml
```

`implementation_status: operational` is permitted only when technical evidence exists.

---

## Task 2 – At least three agent capabilities of your own

Under:

```text
src/agents/
```

there must be at least three distinguishable agent capabilities / role implementations.

Recommended combination:

1. Product Owner / Requirements
2. Developer or Architect
3. QA & Test

Each capability requires:

- clear input,
- structured output,
- at least one tool,
- error handling,
- trace evidence.

---

## Task 3 – Shared task/state model

Define a shared technical task model, preferably using Pydantic.

Example:

```python
class EngineeringTask(BaseModel):
    task_id: str
    task_type: str
    description: str
    assigned_role: str
    input_files: list[str] = []
```

At least two agents must actually use this model.

---

## Task 4 – Agent-to-agent workflow

Implement a LangGraph workflow with at least two agents.

Example:

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

or:

```text
Requirement
      ↓
Requirements Agent
      ↓
Architect Agent
      ↓
Human Approval
```

The handover must be implemented technically through state / structured data.

Manual copy/paste does not count.

---

## Task 5 – Integrate a human gate

At least one workflow must provide for explicit human approval or escalation.

Examples:

- `approved`
- `changes_requested`
- `escalate_to_human`

The decision must be traceable in the workflow state or the generated artifact.

---

## Task 6 – Test the workflow

Create tests for:

- at least one success case,
- at least one error case,
- structured state / output,
- termination or loop limits.

External LLM calls may be meaningfully mocked in unit tests.

---

## Task 7 – Internal dry run

Before the first customer assignment, carry out a small internal engineering task.

### Assignment

Extend the starter service with a persistent **work item feature**.

At minimum:

- create a work item,
- list work items,
- mark a work item as completed or delete it,
- store data in PostgreSQL,
- automated API tests.

At least part of the implementation must be handled through your agentic development workflow.

### Evidence

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

## Task 8 – Task-based cost engineering

For the dry run, it must be possible to trace at least:

- task,
- participating agent,
- model,
- calls,
- runtime,
- tokens, where available,
- credits,
- human review / correction effort.

### Brief evaluation

Create:

```text
docs/dry-run-01.md
```

Maximum length: one page.

Answer:

1. What was implemented?
2. Which humans and agents were involved?
3. Where did a human need to correct or approve something?
4. What did the workflow cost?
5. What specific change would you try for the next task?

---

# Submission checklist for Session 2

In addition to Session 1:

- [ ] Required minimum number of operational agent-supported/hybrid roles achieved
- [ ] At least 3 distinguishable agent capabilities of your own
- [ ] Shared task/state model
- [ ] At least 1 technical agent-to-agent workflow
- [ ] At least 1 human gate
- [ ] Tests for success and error cases
- [ ] Persistent work item feature with PostgreSQL
- [ ] API tests
- [ ] Execution trace for the workflow
- [ ] Task-based agent costs
- [ ] Human review / correction effort
- [ ] `docs/dry-run-01.md`

---

# Guiding principle

Session 1:

> **Can we build and observe an agent?**

Session 2:

> **Can agents become part of an engineering organization?**

From Session 3 onwards:

> **Can this organization deliver value to a customer?**

