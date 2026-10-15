# GitHub snapshot evaluation rubric — Sessions 1 and 2

English translation of [the German rubric](03_Bewertungsraster_GitHub_Termin_1_und_2.md). Criteria, points and caps are identical.

## 1. Purpose

After Sessions 1 and 2, each company's GitHub snapshot is evaluated automatically. The project is ungraded. The score is an **Engineering Health Indicator** and concrete feedback for the next project day. Maximum: **100 points per session**.

## 2. Assess only the team's delta

All companies start with the same starter repository. Distinguish supplied baseline from student achievement.

Never count these as team achievement:

```text
examples/**
tests/starter/**
pytest.ini
```

Do not automatically award points for the supplied FastAPI health endpoint, PostgreSQL/pgvector wiring, unchanged GitHub Actions CI, unchanged Docker Compose, unchanged trace helpers or unchanged templates. Templates count only after meaningful team adaptation.

Use `docs/STARTER_BOUNDARY.md` and `STARTER_MANIFEST.json` as references.

> Assess the delta to the starter, not the starter itself.

## 3. Evidence over claims

Preferred evidence, in order:

1. Team-owned executable code.
2. Team-owned automated tests.
3. Execution traces.
4. Structured outputs / measurements.
5. GitHub Issues / commit history.
6. Team-specific configuration.
7. Technical documentation.

A README claim is insufficient when functionality can be checked technically.

The standard local and CI test command is:

```bash
python -m pytest
```

`pytest.ini` is supplied infrastructure. Team-owned tests must be included and executable through this standard command.

## 4. Session 1 rubric

### A. Company & Roles — 20 points

**A1. Complete role model — 8 points.** Check `organization/roles.yaml`.

- **8:** all 12 roles contain `current_actor_type`, `target_actor_type` and `accountable_human`.
- **5:** 9–11 roles complete.
- **2:** 6–8 roles complete.
- **0:** fewer than 6 complete.

**A2. Human–agent target organization — 6 points.** Assess plausible current/target assignments, recognizable planning for mixed-team work and absence of nominal agents falsely marked `operational`. Do not score the number of planned agents.

**A3. Decision and escalation rules — 3 points.** Check `organization/company.md`.

**A4. Three required decisions justified — 3 points.** Look for the first role supported by an agent, a role deliberately kept human and a human approval gate.

### B. Technical Platform — 15 points

**B1. Reproducible team setup — 4 points.** The README contains team-specific development environment, Ollama/ICC access, setup deviations and known limitations.

**B2. Team-specific architecture — 6 points.** `docs/architecture.md` shows the team's agent, tool, LLM path, human gate/escalation and trace/cost path. Unchanged starter architecture: **0 points**.

**B3. Sensible reuse of starter — 3 points.** No unnecessary parallel replacement infrastructure for components already supplied.

**B4. Stack discipline — 2 points.** **2:** required stack followed or requested deviation justified in an Issue. **0:** central additional technology introduced without agreement.

### C. First Own Agent — 35 points

**C1. Own executable LangGraph agent — 15 points.** Only team-owned implementations, e.g. `src/agents/**`.

- **15:** independently implemented and plausibly executable.
- **10:** largely implemented, minor gaps.
- **5:** fragment / limited executability.
- **0:** no own agent.

`examples/**` never counts.

**C2. Real LLM call through provider abstraction — 5 points.** **5:** technically traceable. **2:** partial implementation / unjustified direct provider-specific coupling. **0:** no real LLM use.

**C3. Real tool — 5 points.** **5:** actually used in the evidenced run. **3:** implemented, but use not evidenced. **0:** text generation only.

**C4. Structured input/output — 5 points.** Prefer Pydantic, TypedDict, JSON Schema or a defined LangGraph state.

**C5. Meaningful error handling — 5 points.** Examples: invalid input, tool error, missing file, LLM error, defined termination.

### D. Testing & Evidence — 15 points

**D1. Own meaningful pytest test — 6 points.** Only tests outside `tests/starter/**`. Full points require execution through `python -m pytest`.

**D2. Team-owned execution trace — 5 points.** Must be attributable to the team's own agent run.

**D3. Reproducible agent invocation — 4 points.** Repository/README explains how to execute the agent.

### E. Cost Measurement — 10 points

Session 1 assesses measurement capability, not cost optimization.

**E1. Human hours — 3 points.** Actual team effort recorded approximately.

**E2. Agent usage — 4 points.** At least own agent, model, runtime, runs and tokens if available.

**E3. Credits calculated — 3 points.** Actual usage translated into credits using the course cost model.

### F. Engineering Process — 5 points

**F1. Meaningful GitHub Issues — 3 points.** At least three relevant Issues for work actually undertaken.

**F2. Traceable commit history — 2 points.** Do not assess commit count. Pull Requests are optional in Session 1.

### Session 1 total

| Dimension | Points |
|---|---:|
| A. Company & Roles | 20 |
| B. Technical Platform | 15 |
| C. First Own Agent | 35 |
| D. Testing & Evidence | 15 |
| E. Cost Measurement | 10 |
| F. Engineering Process | 5 |
| **Total** | **100** |

## 5. Session 1 interpretation

| Score | Meaning |
|---:|---|
| 85–100 | Clearly exceeds the day's objective |
| 70–84 | Day's objective achieved |
| 55–69 | Partially achieved |
| 40–54 | Substantial gaps |
| <40 | Technical foundation not yet operational |

**70 points represent a fully satisfactory project day.** The score is explicitly not a grade.

## 6. Session 1 hard caps

- **No own executable agent:** total at most **50/100**.
- **No own test:** if only `tests/starter/**` exists, total at most **75/100**.
- **Team tests not executable through the standard command:** if team tests exist but `python -m pytest` fails, Testing & Evidence at most **8/15**.
- **No team-owned execution trace:** total at most **75/100**.
- **No actual usage data:** if only the unchanged cost template exists, total at most **75/100**.
- **Starter plus documentation only:** if technical implementation is largely unchanged and mainly Markdown was edited, total at most **40/100**.

## 7. Session 2 rubric

Session 2 assesses the current state after two sessions.

### A. Operational Mixed Team — 20 points

**A1. Minimum operational agent/hybrid-supported roles — 10 points.** Required: `12 - number of human team members`.

- **10:** minimum reached and technically evidenced.
- **7:** one role below minimum.
- **4:** two roles below minimum.
- **0:** substantially below minimum.

A role counts only when technically evidenced behavior exists.

**A2. Consistent accountable humans / human gates — 5 points.**

**A3. Role model matches actual implementation — 5 points.** No `operational` designation without evidence.

### B. Agent Platform — 25 points

**B1. At least three distinguishable agent capabilities — 10 points.** **10:** at least 3. **7:** 2. **3:** 1. **0:** none. One agent may support multiple roles if behavior and traces are distinguishable.

**B2. Shared task/state model — 5 points.** Actually used by at least two agents.

**B3. Agent-to-agent workflow — 7 points.** Technical handover through LangGraph state / structured data.

**B4. Human gate — 3 points.** Explicit approval or escalation point.

### C. Workflow Quality & Tests — 20 points

**C1. Structured outputs — 4 points.**

**C2. Success case tested — 5 points.** Full points require inclusion in `python -m pytest`.

**C3. Failure case tested — 5 points.** Full points require inclusion in `python -m pytest`.

**C4. Termination / loop bounds — 3 points.**

**C5. Reproducible workflow run — 3 points.**

### D. Internal Dry Run — 20 points

**D1. Persistent Work-Item feature — 8 points.** At least create, list, complete or delete, and PostgreSQL persistence.

**D2. API tests — 4 points.** Team-owned tests executable through `python -m pytest`.

**D3. Agentic contribution traceability — 5 points.** Traceable chain: `Issue → Task → Agent/Human → Artifact → Test/Review`.

**D4. `docs/dry-run-01.md` — 3 points.** Brief, concrete and tied to actual evidence.

### E. Cost Engineering — 10 points

**E1. Agent costs per task — 4 points.**

**E2. Human review / correction effort — 3 points.**

**E3. Concrete optimization idea from measurements — 3 points.** A reasoned hypothesis for the next task is sufficient.

### F. Engineering Discipline — 5 points

**F1. Issues / commits reflect the dry run — 3 points.**

**F2. Architecture / role model updated — 2 points.**

### Session 2 total

| Dimension | Points |
|---|---:|
| A. Operational Mixed Team | 20 |
| B. Agent Platform | 25 |
| C. Workflow Quality & Tests | 20 |
| D. Internal Dry Run | 20 |
| E. Cost Engineering | 10 |
| F. Engineering Discipline | 5 |
| **Total** | **100** |

## 8. Session 2 interpretation

| Score | Meaning |
|---:|---|
| 85–100 | Clearly exceeds the day's objective |
| 70–84 | Day's objective achieved |
| 55–69 | Partially achieved |
| 40–54 | Substantial gaps |
| <40 | Agentic Development Platform not yet operational |

## 9. Session 2 hard caps

- **Operational role minimum substantially missed:** more than two missing roles, total at most **60/100**.
- **Fewer than two own capabilities:** total at most **55/100**.
- **No technical agent-to-agent workflow:** total at most **65/100**.
- **No own workflow/API tests:** total at most **65/100**.
- **Team tests not executable through the standard command:** if relevant team tests cannot successfully run through `python -m pytest`, Workflow Quality & Tests at most **10/20**.
- **Mock-only dry run / no persistence:** total at most **75/100**.

## 10. Both sessions: security critical finding

Committed secrets such as API keys, passwords, tokens or private keys are always reported as a **Critical Finding**.

## 11. No points for unnecessary complexity

Do not reward more agents than needed, more frameworks, larger models, more LLM calls or unnecessary multi-agent layers. Technical simplicity is not a disadvantage when the solution is reliable and traceable.

## 12. Automated evaluation output

```json
{
  "company": "NAME",
  "session": 1,
  "score": 78,
  "interpretation": "Day's objective achieved",
  "dimensions": {
    "company_roles": 16,
    "technical_platform": 12,
    "first_own_agent": 27,
    "testing_evidence": 11,
    "cost_measurement": 8,
    "engineering_process": 4
  },
  "evidence": [
    {
      "criterion": "C1",
      "score": 13,
      "files": ["src/agents/qa_agent.py"],
      "reason": "..."
    }
  ],
  "strengths": ["..."],
  "critical_findings": ["..."],
  "missing_evidence": ["..."],
  "top_3_actions_next_session": ["...", "...", "..."],
  "confidence": 0.9
}
```

For Session 2, adapt dimension keys to the Session 2 rubric.

## 13. Instruction to the evaluation model

> Compare the repository state with the supplied starter and assess only team-owned changes and execution evidence. Exclude `examples/**`, `tests/starter/**` and `pytest.ini` entirely from student achievement. Unchanged starter infrastructure must not earn student-achievement points. Do not infer functionality from documentation; seek code, tests, traces or structured data for technically verifiable claims. Team tests must be included and executable in `python -m pytest`. Cite specific files or GitHub artifacts for each substantial assessment. Do not penalize simplicity or reward extra frameworks. Do not deduct points for functionality not yet required in the relevant session. A score of 70–84 means the day's objective was achieved; do not treat 70 as weak performance. Explicitly report uncertainty when a static repository snapshot cannot reliably verify functionality.
