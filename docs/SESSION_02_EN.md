# Session 2 — operational agents and an internal dry run

Monday, 19 October 2026, **10:00–15:00**.

Use the [assignment](../task%20sheets/Tasks_Session_1_and_2_en.md) and [rubric](../task%20sheets/Evaluation_Rubric_Sessions_1_and_2_en.md). This guide clarifies the common infrastructure; it does not add assessment criteria.

## Update existing team repositories

The Session 2 infrastructure fix is supplied starter code, not team achievement. Keep your original starter baseline and record the update commit separately. Do not replace your repository with a new clone.

1. Commit your current work and create a working branch.
2. Fetch the course update and inspect it before applying:

```bash
git fetch https://github.com/MARS-Group-HAW/agentic_ai.git fix/session-02-readiness
git show --stat FETCH_HEAD
git cherry-pick FETCH_HEAD
```

This branch contains one infrastructure commit based on the previous starter. Resolve conflicts by preserving your team changes and incorporating the fix. If unsure, use `git cherry-pick --abort` and ask the instructor. Record the update SHA (`git rev-parse FETCH_HEAD`).

3. Update your existing local `.env` manually (do not overwrite credentials):

```text
TRACE_FILE=logs/RUN_ID.jsonl
LLM_TIMEOUT_SECONDS=120
LLM_MAX_OUTPUT_TOKENS=768
```

`RUN_ID` is a filename placeholder replaced by the trace helper; no shell expansion is required. Legacy fixed trace paths still append. The timeout bounds HTTP operations, not total workflow time. Teams must also bound loops/calls and decide how to handle incomplete results.

## Deliver a complete path first

Implement a shared Task/State model used by two agents, a structured handover and a human approval/escalation point. Then complete the third capability, remaining role support and Work-Item dry run. Three capabilities do not automatically cover six or seven roles.

| Team size | Minimum operational agent/hybrid-supported roles |
|---|---:|
| 6 people | 6 |
| 5 people | 7 |

For every supported role, identify implementation, distinguishable behavior/output, test or trace, and accountable human. An LLM-generated `approved` is not human approval: record the human, decision, task, reviewed artifact and time in state or an artifact.

## Traces and distributed development

- The default is a separate `logs/<run_id>.jsonl` per run. Reuse a `workflow_id` across collaborating agents and a `task_id` across code, traces, review and costs; keep agent run IDs distinct. The supplied single-agent reference uses its run ID as workflow ID.
- Record `role`, `agent`, `model`, provider, tools, status, duration, calls and token usage when available. The helper accepts arbitrary record fields; teams supply their own role/workflow context.
- `logs/*.jsonl` is deliberately ignored. Copy selected, sanitized **team-owned** evidence to `evidence/session-02/<run_id>.jsonl` and commit it. Reference/mock runs are not real team execution evidence. Never include secrets or protected data.
- Docker Compose mounts `./logs` into `/workspace/logs`, retaining default logs on the host. A custom trace path outside this directory needs its own mount or export.
- The reference runner records errors, malformed results and keyboard interruptions. A hard kill or unwritable storage can still prevent logging. It records exception type, not provider error text that may contain credentials.

## Costs and review effort

The rates in `costs/cost-model.yaml` are common course rates: human 100 credits/hour; LLM call 1; runtime 0.01/second; input 0.02/1000 tokens; output 0.04/1000 tokens; CI 1/run. Do not change rates independently.

Keep the existing `costs/usage.csv` columns for compatibility. Use one row per attributable usage item. Put the matching `run_id`/`workflow_id`, model, calls, duration, token counts and activity (implementation/review/correction) in `notes`, or add a separate structured cost file with those fields. Each row must link to `task_id`; do not double-count summary and detailed rows. Separate files per person/task can avoid concurrent edits; consolidate once before the snapshot.

`estimate_cost_credits(..., calls=N)` supports an aggregate of N calls. Sum tokens and count runtime once for the period being charged. Its default `calls=1` preserves previous callers. Failed attempted calls count too. The supplied OpenAI-compatible adapter disables automatic retries so each invocation is one attempt. Missing tokens are unknown, not measured zero; recorded credits are partial estimates until usage is known. Add human and CI credits separately. Avoid counting review time again within implementation hours.

## PostgreSQL, schema and tests

The CI now supplies PostgreSQL/pgvector, runs `db/init.sql` and sets both database URLs. Its supplied persistence probe is not a team API test. Teams still implement Work-Item create/list/complete-or-delete, schema setup and API/persistence tests.

Locally:

```bash
docker compose up -d db
docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1' < db/init.sql
python -m pytest
```

To include the supplied real database probe, set `STARTER_DATABASE_TEST=1` in your shell before pytest (`export STARTER_DATABASE_TEST=1` on macOS/Linux; `$env:STARTER_DATABASE_TEST="1"` in PowerShell). Without it, that probe skips. The input-redirection example above is for Bash. In PowerShell, pipe the SQL with `Get-Content db/init.sql | docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1'`. Check `/db/health` separately with the application running.

PostgreSQL initialization scripts run automatically only for a new data directory. Document an explicit, repeatable schema/migration command for existing databases; do not delete volumes to update schema. Ensure your team tests initialize their schema before making API calls. The database account used for the supplied CI probe needs CREATE TABLE permission.

## Suggested schedule and final snapshot

| Time | Focus |
|---|---|
| 10:00–10:20 | Stand-up, blockers, update and role plan |
| 10:20–12:30 | Shared model, workflow, human gate, capabilities and tests |
| 12:30–13:00 | Break |
| 13:00–14:30 | Persistent Work Items, dry run, costs and review |
| 14:30–15:00 | Tests, evidence export, documentation and repository freeze |

Before the snapshot: run `python -m pytest`; check real PostgreSQL persistence; commit your workflow evidence and cost records; update `organization/roles.yaml` and architecture; write the one-page `docs/dry-run-01.md`. Preserve the chain **Issue → Task → Agent/Human → Artifact/Code → Test → Human Review**. Your agents and the Work-Item solution remain your own implementation.
