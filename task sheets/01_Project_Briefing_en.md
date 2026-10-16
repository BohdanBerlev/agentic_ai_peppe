# Agentic AI Elective Project – Project Briefing

**HAW Hamburg – Faculty of Computer Science**  
**Instructor:** Prof. Dr. Thomas Clemen  
**Format:** ungraded elective project  
**Duration:** 12 sessions, Mondays, 10:00–15:00  
**Participants:** approximately 17 students  
**Organisation:** 3 software companies with approximately 5–6 students each  
**Updated:** 7 October 2026

---

## 1. Scenario

As a team, you will establish a small software development company.

Your company has more designated roles than human team members. You must therefore support some roles with AI agents or hybrid human–agent solutions.

After a setup phase of two sessions, each company will receive a customer assignment.

From that point onwards, you will work like a small software company:

- understand requirements,
- plan tasks,
- develop software,
- test,
- deploy,
- use agents,
- monitor costs,
- respond to change requests and disruptions.

The project is ungraded. Nevertheless, each company's technical progress will be evaluated automatically after every project day, based on its GitHub repository.

---

## 2. Central Question

The goal is not to build as many agents as possible.

The goal is to find out:

> **How can a mixed team of humans and AI agents develop software reliably and cost-effectively?**

This includes, in particular:

- appropriate delegation to agents,
- human oversight,
- technical integration of agents,
- software quality,
- reproducibility,
- error handling,
- cost engineering,
- adapting the organisation throughout the semester.

---

## 3. Mandatory Roles

Each company must cover all twelve roles below.

| Role | Main Responsibility |
|---|---|
| **1. Managing Director / Customer Lead** | Customer communication, priorities, company decisions |
| **2. Product Owner / Requirements Engineer** | Requirements, user stories, acceptance criteria |
| **3. Project Manager** | Planning, task assignment, dependencies, delivery risks |
| **4. Software Architect** | System architecture, interfaces, ADRs, technical standards |
| **5. Backend / API Engineer** | FastAPI, business logic, API contracts |
| **6. Data & RAG Engineer** | PostgreSQL, pgvector, ingestion, retrieval, embeddings |
| **7. Agent Engineer** | LangGraph workflows, LangChain, agent state, tools |
| **8. Integration Engineer** | Agent-to-agent and agent-to-system interfaces |
| **9. QA & Test Engineer** | pytest, regression tests, agent evaluation |
| **10. DevOps Engineer** | Docker, GitHub Actions, build, deployment |
| **11. AI Safety & Security Engineer** | Tool permissions, guardrails, secrets, agent risks |
| **12. Cost & Observability Engineer** | Traces, execution times, token usage, cost engineering |

### Role Assignment Rules

One person may be responsible for multiple roles.

For each role, distinguish between two states:

- **current_actor_type** – how the role is currently performed,
- **target_actor_type** – how the role is intended to be performed in the future.

Possible values:

- `human`
- `agent`
- `hybrid`

Each role must also have an **accountable human**.

### Session 1

During the first session, a role intended for an agent may still be performed by a human.

Example:

```yaml
current_actor_type: human
target_actor_type: agent
implementation_status: planned
```

### End of Session 2

By the end of Session 2, at least

```text
12 - number of human team members
```

roles must have **operational support from agents or hybrid human–agent solutions**.

For 6 students, this means at least 6 roles; for 5 students, at least 7 roles.

A role counts as operationally supported by agents or a hybrid solution only if there is technically verifiable behaviour to demonstrate it.

One agent may support multiple roles if:

- its role-specific behaviour can be distinguished,
- different inputs/outputs or policies exist,
- its execution can be followed in traces.

---

## 4. Mandatory Technology Stack

All companies start with the same starter repository.

### Software Engineering

- GitHub
- GitHub Issues
- GitHub Actions
- Git
- Python 3.12
- FastAPI
- Pydantic
- pytest
- Docker
- Docker Compose

### Agentic AI

- LangGraph
- LangChain
- LLM access through the provider abstraction defined in the starter
- locally via Ollama **or**
- via an ICC endpoint provided by HAW

Agent code should not depend directly on a specific LLM installation.

### Data / RAG

- PostgreSQL
- pgvector
- `langchain-postgres`
- psycopg 3

PostgreSQL serves as:

- the relational application database,
- the metadata database,
- the foundation for RAG / vector retrieval.

### Observability and Cost Engineering

Local, machine-readable project artefacts are mandatory:

- agent execution traces,
- execution times,
- model / agent / task,
- success or failure,
- token usage, where available,
- cost records.

### LangSmith

LangSmith is **optional** and is not part of the evaluation basis.

If you use LangSmith, it does not replace local traces in the repository.

### Additional Tools

Additional frameworks, databases, vector stores, workflow engines or observability platforms may only be used after prior consultation with the instructor.

---

## 5. The Starter Repository

The starter repository provides a shared technical foundation.

It includes, among other things:

- a basic FastAPI service,
- PostgreSQL + pgvector,
- Docker configuration,
- a basic GitHub Actions workflow,
- basic pytest tests,
- `pytest.ini` for consistent test imports and test paths,
- an LLM provider abstraction,
- local trace helper functions,
- a cost model template,
- a role template,
- an architecture template,
- a LangGraph reference agent.

### Setup Guides and Assignments

The setup guides explain how to install and configure Python, Docker and Ollama or access the HAW ICC endpoint:

- German: [SETUP_LOCAL_DE.md](../docs/SETUP_LOCAL_DE.md)
- English: [SETUP_LOCAL_EN.md](../docs/SETUP_LOCAL_EN.md)

The detailed assignments and submission checklists are in [Tasks Sessions 1 and 2 – English](Tasks_Session_1_and_2_en.md) and [Aufgaben Termin 1 und 2 – German](Aufgaben_Termin_1_und_2_de.md). The evaluation criteria are in the [Session 1 and 2 evaluation rubric (German)](Evaluation_Rubric_Sessions_1_and_2_en.md).

### Standard Test Command

The standard command for this project is:

```bash
python -m pytest
```

Use this command both locally and in CI. It ensures that `pytest` runs in the same Python environment as the project.

### Distinguish Tests from Real Execution

The starter tests use a simulated LLM. Passing these tests therefore does not demonstrate a real LLM call or a working PostgreSQL connection. Check the database separately via `/db/health` and run the reference agent with your configured LLM. The reference run verifies the starter; your submission also requires a real run of your own agent with an attributable trace.

### Execution Time and Termination

Your own workflows should have explicit limits on execution time, LLM calls and possible loops. Timeouts and other errors must produce a defined error result. The unchanged starter does not consistently enforce these limits; setting a timeout variable alone is not sufficient evidence. The reference run can take several minutes on local hardware. See the setup guide for further details.

### Important

The starter does **not count as student work**.

In particular, the following areas do not count as evidence of your own agents or tests:

```text
examples/**
tests/starter/**
pytest.ini
```

Templates count as student work only after they have been meaningfully adapted to your company.

The exact boundary is described in:

```text
docs/STARTER_BOUNDARY.md
```

---

## 6. GitHub Is the Central Project Record

After every project day, a snapshot of the company's repository will be evaluated.

Only verifiable repository evidence will be considered.

### Good Evidence

- your own executable code,
- your own tests,
- GitHub Issues,
- pull requests from the customer project onwards,
- agent execution traces,
- structured outputs,
- cost records,
- Architecture Decision Records,
- an updated architecture,
- verifiable customer deliverables.

### Insufficient Evidence

A statement such as

> “Our QA agent handles quality assurance.”

is not sufficient.

An example of evidence would be:

```text
Task
   ↓
QA agent under src/agents/
   ↓
Execution trace
   ↓
Structured QA report
   ↓
Test / human review
```

### Human Approval

An LLM-generated status such as `approved` is a model assessment, not human approval. A human approval gate requires an explicit human decision that can be linked to the task and the agent's result. A structurally valid result still needs to be checked for substantive correctness.

In Session 1, a manual review artefact may document the decision. By the end of Session 2, at least one workflow must include an explicit human approval or escalation point; the decision must be traceable in the workflow state or the generated artefact.

Basic rule:

> **Evidence over claims.**

---

## 7. Cost Engineering from the Start

Even a locally running LLM is not treated as “free” in this project.

All companies use an abstract credit model.

From Session 1 onwards, record at least:

- human working time,
- agent runs,
- the model used,
- agent execution time,
- tokens, where available,
- CI runs.

From Session 2 onwards, also record costs per task and human review/correction effort.

The key question is not:

> Which team uses the most agents?

It is:

> Which human–agent configuration delivers good quality with the most reasonable level of effort?

---

## 8. Working Practices

Teams will work largely independently.

A useful daily schedule is:

### 10:00–10:20 – Company Stand-up

- daily goal
- blockers
- current roles
- planned division of tasks between humans and agents

### 10:20–12:30 – Engineering

### 12:30–13:00 – Break

### 13:00–14:30 – Engineering

### 14:30–15:00 – Repository Freeze

Before the end of the project day:

- run tests with `python -m pytest`,
- update open issues,
- save execution traces,
- update cost records,
- bring documentation into line with the actual implementation.

---

## 9. What You Should Not Optimise For

The project does not automatically reward:

- large numbers of agents,
- complex multi-agent systems,
- very large models,
- many LLM calls,
- maximum autonomy,
- many commits,
- extensive documentation without implementation.

A simple solution may be the better solution.

What matters is:

- functionality,
- technical quality,
- traceability,
- appropriate use of agents,
- costs,
- learning progress.

---

## 10. Goal After Session 1

After the first project day:

> **The company is established. The platform runs. Your first agent works, is tested, produces evidence, and its usage can be measured.**

A complete agent organisation is not yet expected.

The submission must include at least one of your own LangGraph agents with a real tool, structured input/output and meaningful error handling, one of your own pytest tests, a real execution trace for your own agent, and recorded usage with calculated credits. Adapt your company description, role model, architecture and team setup. At least three meaningful GitHub Issues and a traceable commit history are required; pull requests are optional in Session 1.

---

## 11. Goal After Session 2

After Session 2, each company should have a small but functional **Agentic Development Platform**.

It should demonstrate at least that:

- all twelve roles are covered organisationally,
- at least `12 - number of human team members` roles have operational support from agents or hybrid solutions,
- at least three distinguishable agent capabilities / role implementations of your own exist; these do not necessarily require three separate agents,
- LangGraph/LangChain are actually used,
- each agent capability has a clear input, structured output, at least one real tool, error handling and trace evidence,
- at least two agents use a shared task/state model,
- at least one LangGraph workflow connects at least two agents through a technical handoff using state / structured data; manual copy/paste does not count,
- at least one workflow includes an explicit human approval gate or escalation point,
- structured traces provide evidence of a real workflow run,
- tests cover a success case, an error case, structured state / output and termination or loop limits,
- costs are recorded per task, including human review/correction effort,
- the software foundation is tested with `python -m pytest` and is reproducible.

### Mandatory Internal Dry Run

Before the customer assignment, extend the starter service with a persistent **work-item feature**:

- create a work item,
- list work items,
- mark a work item as completed or delete it,
- store data in PostgreSQL,
- provide your own automated API tests.

At least part of the implementation must be handled through your Agentic Development Workflow. The chain from GitHub Issue through task and agent/human contribution to code, test and review must be traceable.

Document the dry run in `docs/dry-run-01.md`, on no more than one page: implementation, people and agents involved, required corrections/approvals, costs per task, and one concrete improvement to try on the next task.

The first customer assignment begins in Session 3.

