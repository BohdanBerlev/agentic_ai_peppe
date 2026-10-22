# Session 3 evaluation rubric – CUST-001

**100 points · ungraded engineering health indicator.** All teams use the same customer contract. German and English are equivalent. Assess evidenced customer delivery and work since the previous submission; unchanged previously assessed work and supplied infrastructure do not create new achievement points. Integrating reused own components may contribute to the working customer result.

## Criteria

Award partial credit in proportion to evidenced fulfilment, with reasons. Cite files, tests, run IDs or GitHub artifacts for every criterion. Do not infer functionality from documentation alone.

| Criterion | Max. | Full-credit evidence |
|---|---:|---|
| **A. Customer understanding** | **10** | |
| A1. Acceptance matrix | 4 | AC-01 to AC-08 linked to tests/artifacts and results. |
| A2. Clarifications | 2 | Questions/assumptions documented; a reasoned statement that no questions remain is acceptable. |
| A3. Scope and accepted requirements | 4 | Small agreed delivery; unreviewed model suggestions not presented as customer requirements; reviewed version saved. |
| **B. Functionality and data** | **25** | |
| B1. Creation and defaults | 5 | AC-01 supported by own code and actually executed API behaviour. |
| B2. Filtering | 7 | AC-03 individual and combined filters work. |
| B3. State logic | 7 | AC-04, including repeated state and rejected transitions without unintended changes. |
| B4. Data preservation/migration | 6 | AC-02 and existing-data mapping documented and technically evidenced; no destructive reset. |
| **C. Tests and reproducibility** | **20** | |
| C1. Success cases | 5 | Own API/workflow success tests execute in the standard run. |
| C2. Negative cases | 5 | AC-05/06/07 cover 422/404/503, unknown fields and unchanged state after invalid transitions. |
| C3. Actual DB test | 7 | Own `tests/test_customer_persistence.py` test passes against PostgreSQL using a new connection/process; no mock/memory/skip. |
| C4. Repeatability | 3 | Commands, migration, dependencies, tested source version and saved JUnit agree. |
| **D. Agent contribution** | **15** | |
| D1. Two capabilities | 4 | Two distinguishable own capabilities contribute to the customer task; human and agent contributions identified. |
| D2. Substantive handover | 5 | Earlier structured output influences subsequent processing, shown by code and execution evidence. |
| D3. Actual run and evidence | 4 | At least one actual local/ICC LLM run with tool, IDs, provider/model, status and artifact; mock tests separate. |
| D4. Errors and termination | 2 | Bounded execution and escalation; missing required input stops before model invocation. |
| **E. Human responsibility** | **10** | |
| E1. Explicit decision | 4 | Actual review of customer result with reviewer, time and rationale. |
| E2. No automatic human approval | 3 | Negative tests for headless/invalid reports pass; no automatic customer/issue completion without approval. |
| E3. Source binding | 3 | Reviewed artifacts bound to source commit or hash; changes require renewed review. |
| **F. Costs and learning** | **10** | |
| F1. Task costs | 4 | Actual calls/runtime/tokens/credits including failures, deduplicated without rollup duplication; unknown values explicit. |
| F2. Human effort | 3 | Implementation, review and correction estimated/recorded separately per task; waiting time distinct. |
| F3. Next experiment | 3 | Evidence-based optimisation hypothesis combining costs and quality. |
| **G. Engineering process** | **10** | |
| G1. Issue → PR → review | 4 | Concrete issues, feature PR and human review traceable; ZIP includes necessary references/exports. |
| G2. Session 2 remediation and roles | 4 | Confirmed team size, key findings fixed/prioritised with reasons; role status backed by evidence or an explicit gap. |
| G3. Delivery record | 2 | Architecture, acceptance/delivery notes and reproduction instructions match the submission. |
| **Total** | **100** | |

## Caps

Add criterion points first, then apply the lowest applicable overall cap. Report raw score, caps and final score separately. Apply category caps before overall caps.

| Finding | Limit |
|---|---:|
| No own plausibly executable customer feature | Overall maximum 50 |
| No actual PostgreSQL implementation; memory/mock-only storage | Overall maximum 60 |
| No actually executed own PostgreSQL customer test | Overall maximum 70 |
| No substantive technical agent handover | Overall maximum 65 |
| No evidenced actual own local/ICC LLM customer run | Overall maximum 75 |
| No explicit human gate, or automatic consent represented as human approval | Overall maximum 60 |
| Relevant own tests fail in the correctly configured standard run | C maximum 10/20 |

Missing evaluator infrastructure is not proof of team failure. A saved, traceable actual DB run tied to the tested source version can substitute for a live DB rerun. A README claim or passing mock tests cannot. Distinguish skipped from executed tests. For ZIP-only assessment, report unavailable GitHub history as uncertainty and consider concrete references/exports.

Session 2 role caps are **not automatically carried over** into Session 3. Role coverage remains a project requirement and is assessed here in G2; previous assessments remain unchanged. This rubric evaluates customer delivery alongside remediation.

## Interpretation and output

| Final score | Interpretation |
|---:|---|
| 85–100 | Clearly above the session goal |
| 70–84 | Session goal achieved |
| 55–69 | Partially achieved |
| 40–54 | Major gaps |
| Below 40 | Customer delivery not yet reliable |

70 points are fully satisfactory. Complexity, number of agents, model size, call count and text length earn no bonus. Exclude `examples/**`, `tests/starter/**`, `pytest.ini` and unchanged course templates. Report actual published secrets as Critical Findings without repeating their values. Explicitly report provider deviations, unsupported claims and serious gate problems; do not invent additional penalties.

Produce: short verdict; all 24 criterion scores with evidence; raw score/caps/final score; tests and execution limits; strengths; key findings; three next actions. Add feedback in the team's language. Optional JSON: `company`, `session=3`, `source_commit`, `raw_score`, `applied_caps`, `score`, `dimensions`, `evidence`, `missing_evidence`, `top_3_actions`, `confidence`.
