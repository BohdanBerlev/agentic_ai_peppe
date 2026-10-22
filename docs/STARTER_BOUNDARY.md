# Starter boundary for assessment

The repository contains supplied infrastructure and reference code so all companies begin with the same technical baseline.

## Supplied evidence that must not be scored as team achievement

Exclude from Agentic Engineering scoring:

- `examples/**`
- `tests/starter/**`

The following are templates and only count after meaningful team modification:

- `organization/company.md`
- `organization/roles.yaml`
- `docs/architecture.md`
- `costs/cost-model.yaml`

The unchanged baseline also does not count as team achievement:

- FastAPI health endpoint,
- Docker / Docker Compose,
- PostgreSQL + pgvector wiring,
- GitHub Actions baseline CI,
- LLM provider factory,
- trace helper,
- RAG helper.

## What should count

Examples of team-owned evidence:

- implementations under `src/agents/**`,
- team-created tests outside `tests/starter/**`,
- team-specific architecture changes,
- meaningful GitHub Issues,
- team-generated execution traces,
- actual cost/usage records,
- customer-project source code,
- later: Pull Requests and ADRs.

## Session 1 role staffing

The twelve roles are predefined.

During Session 1 teams distinguish between:

- `current_actor_type`
- `target_actor_type`

A planned future agent role may still have:

```yaml
current_actor_type: human
target_actor_type: agent
implementation_status: planned
```

Only roles with executable team-owned evidence may be marked:

```yaml
implementation_status: operational
```

Session 1 requires one own operational LangGraph agent, not a complete operational agent organization.

## Session 2 mixed-team rule

By the end of Session 2, at least

```text
12 - number_of_human_team_members
```

roles must be operationally supported by an agent or hybrid implementation.

A human may remain accountable for multiple roles.

One agent implementation may support multiple roles only when role-specific behavior, state, policy or outputs are technically distinguishable and the execution trace identifies the role being performed.

## Evaluation instruction

> Evaluate the delta to the starter. Do not award points merely because the starter contains working CI, FastAPI, PostgreSQL wiring, tracing utilities or a reference LangGraph agent.

## Session 2 infrastructure update (revision 4)

The updated provider limits, tracing helpers, reference runner, Docker exclusions, log mount, CI database service and all tests under `tests/starter/` remain supplied infrastructure. Do not score their adoption as team achievement. `pytest.ini` is also excluded.

Existing teams retain the starter commit/ZIP they actually used as their initial baseline and record the revision-4 update commit separately. Use both when distinguishing team work from later supplied fixes.

## Session 3 infrastructure update (revision 5)

Course documents under `task sheets/session-03/`, technical notes, unchanged templates under `docs/templates/session-03/`, CI evidence capture, generic DB-health errors, optional factory controls and `tests/starter/test_session_03_infrastructure.py` are supplied infrastructure, not student achievement. Do not overwrite team implementations when integrating this update. Customer features, migrations, own persistence tests and own human-gate logic remain team work. Session 3 uses its own announced rubric; do not retroactively rescore Sessions 1/2.
