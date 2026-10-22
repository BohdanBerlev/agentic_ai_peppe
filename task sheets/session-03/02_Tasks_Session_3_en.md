# Session 3 tasks – First customer delivery

**26 October 2026 · 10:00–15:00**
Read: customer assignment → tasks → rubric. Deliver a small accepted customer benefit with evidenced human–agent collaboration.

## Schedule

| Time | Activity / result |
|---|---|
| 10:00–10:20 | Customer briefing, questions, confirmed team size and roles. |
| 10:20–10:50 | Close the most important Session 2 gap; check human gate and DB path. |
| 10:50–11:10 | Acceptance criteria, issues and owners. |
| 11:10–12:30 | First vertical implementation, migration and tests. |
| 12:30–13:00 | Break. |
| 13:00–14:00 | Agent workflow, integration tests, error cases and costs. |
| 14:00–14:30 | Customer demos and reviews; at most 8 minutes per team. |
| 14:30–15:00 | Corrections, final tests and submission freeze. |

## 1. Stabilise and plan

Turn your three most important feedback items into issues. Confirm actual team size in `organization/company.md`; set role status according to evidence. `12 − team size` remains the organisational target. Report remaining gaps honestly. Earlier scores are not retroactively recalculated using this rubric.

Before acceptance: no automatic `approved` attributed to a human, no issue closure on changes requested/invalid output, an allowed LLM path and an executable actual DB test. Address missing role evidence alongside delivery; do not create agent programs merely to fill labels.

Create customer epic `CUST-001` and at least three actionable issues, for example contract/migration, feature/tests and workflow/acceptance. A feature PR with a brief human review is required. People may hold several roles; each task has an accountable human.

## 2. Requirements and implementation

Map AC-01 to AC-08 to `docs/customer-01/acceptance.md`: criterion, test/artifact, result and review. Add only customer-agreed criteria. Model proposals are drafts; remove invented requirements and save the accepted version.

Extend your API with priorities, filters and defined transitions. Document migration and existing-data mapping. A small working extension suffices; no login, UI, RAG or deployment.

## 3. Demonstrate the agent contribution

At least two own capabilities work on a customer task. One must substantively use another's result, such as requirements JSON → architecture review or review/test report → QA. Identical task IDs or a fixed call order alone do not suffice.

Provide at least one actual local-LLM/ICC run; unit tests may mock models. Actual tool access, structured outputs and error handling are required. Record task/workflow/run IDs, role, provider/model, tool, result status and artifact references. Technical execution, business outcome and human acceptance are separate states. Missing input files must stop processing before a model call.

A QA agent need not generate tests, but must not claim to have executed them if it only reads source. At least one actual pytest run used for acceptance must be traceable.

## 4. Test and prove persistence

Standard invocation using the active project Python:

```bash
python -m pytest -ra --junitxml=evidence/session-03/pytest.xml
```

Cover valid creation/defaults, separate/combined filters, valid/invalid transitions, unchanged state after 422, 404, generic 503 and actual PostgreSQL persistence. Parametrisation is allowed; test count alone earns no points.

Use a common own test location `tests/test_customer_persistence.py`; helpers may live elsewhere. After your documented DB/migration preparation, run:

```bash
python -m pytest tests/test_customer_persistence.py -ra --junitxml=evidence/session-03/postgres.xml
```

The test reopens a DB connection or API process and reads stored values again. Do not mock PostgreSQL, switch to memory or silently skip when the DB is missing. A separate optional local DB suite may exist; this acceptance invocation must fail if DB access is unavailable. At least one own case must actually execute and pass. Starter DB tests do not replace customer tests. Clean up only your own generated test records, never the entire data volume.

## 5. Human gate and demo

Default: pending approval, changes requested or escalation. No human input means no human approval. Record reviewer, decision, UTC time, task/workflow, reviewed artifacts and source version/hashes. Self-declared identity in a CLI/form suffices for the course; no IAM implementation is required. Hashes bind content, not identity.

Test that headless execution does not invent approval and invalid/failed reports cannot automatically complete customer work. Humans may explicitly accept a reasoned risk; that does not replace evidence for mandatory acceptance criteria. Code changes after review require new tests and review.

Demo: customer problem → three requests → filters/status → persistence → agent handover → human decision → costs/open items.

## 6. Costs and submission

Course rates: call 1.0; runtime 0.01/s; input 0.02/1,000 tokens; output 0.04/1,000; human 100/hour; CI run 1.0. Include failed attempts. Unknown tokens remain `null`, with incomplete estimates identified. Separate agent execution from human gate waiting time. Do not add orchestrator rollups as extra calls/tokens; deduplicate by run ID. Distinguish shared platform setup from the incremental cost of this task.

Submit code/tests; `docs/customer-01/acceptance.md`, `delivery.md`, `clarifications.md`, `recovery.md`; `evidence/session-03/` containing traces, JUnit and review; updated costs, roles and architecture. Copy the templates from `docs/templates/session-03/` into the customer folder. Unmodified templates and supplied infrastructure fixes are not student achievement.

In `evidence/session-03/manifest.json`, record tested source commit, commands, provider/model, IDs and evidence paths. Evidence may be added in a subsequent evidence-only commit: distinguish the tested code commit and submission commit. No source change between test and review without rerunning checks.
