# Session 3 – First customer delivery through your Software Factory

**10:00–15:00 · Customer project 01 · Required: [Customer brief](Client_Brief_Nordwerk_en.md)**  
Assessment: [Session 3 rubric](Bewertungsraster_Termin_03_Factory.md). The brief is part of this task sheet.

## Daily target and learning objectives

By the end of the session, your existing Factory has produced a small runnable part of the website in a separate customer repository. You can identify agent and human contributions and show how the result was checked.

- **L3.1:** Separate Factory and product technically and address a customer task explicitly.
- **L3.2:** Make at least two agent capabilities cooperate through structured handovers on a real product artifact.
- **L3.3:** Integrate checks and an actual human decision into the workflow.
- **L3.4:** Measure effort including failed attempts and identify a concrete bottleneck.

## 1. Understand and scope the commission

Read the brief together. Create a customer issue in the product repo identifying today's scope: AC-01, AC-04 and one service from AC-02. Use the required content. Record open questions and customer answers. This sheet and the brief define the approved initial scope; unresolved choices may be recorded as explicit assumptions.

Assign accountable humans for the commission, technical delivery, checks and approval. A person may hold multiple roles. Plan the S3/S4 delivery effort and S5 reserve according to the cost contract. Full autonomy is not today's target.

## 2. Separate repositories and workspaces

Continue using the existing team repo as the Factory. Create a separate product repository, for example `client-01-website`, with its own checkout. Supply project ID, path and task as configuration to the Factory. Generate product files there; agents, policies and general tools remain in the Factory.

Verify that the product can be opened locally or served through a simple documented web server without a Factory process. No submission may contain secrets. Keep the mandatory stack in the Factory without imposing it on the product.

## 3. Execute a real Factory run

Use your capabilities from Session 2. For example, requirements/planning passes structured tasks to implementation; QA receives artifact paths and acceptance criteria. Names and exact responsibilities are your choice.

A run must demonstrate at least two agent capabilities, a real LLM call and a real tool action on the customer checkout. An agent must edit at least one product file or produce an applicable patch. Include a visible human review step. A rejected intermediate result followed by a correction is acceptable; do not label it accepted. Bound repetitions, for example at most two correction loops before human escalation.

Freeze input commits before starting, then link the output version and evidence. Save raw logs under unique run IDs. Identify manual interventions, unexecuted suggestions and discarded changes.

## 4. Check a small website slice

Show company name, main statement, one service, contact link and course notice. A simple layout is sufficient. Create at least one meaningful automated product check and one own Factory test for structured handover state or project assignment. Run Factory tests with `python -m pytest`; document a separate product test command. Tests may mock LLMs for reproducible logic; provide the real run separately.

A human checks visible content and the contact link. Only then approve the version or reject it with a specific reason.

## 5. Review and submit

Record human delivery, review, rework and Factory development time separately, agent/CI costs and failed runs. Identify the main bottleneck with a run/artifact reference and a testable improvement hypothesis for S4/S5. A before/after experiment is not yet required.

| Location | Required submission |
|---|---|
| Product repo | Customer issue, small runnable website version, own product check, start/test command |
| Factory repo | Project configuration, own Factory test, run evidence, human gate decision, costs |
| `evidence/session-03.md` | Both commit references, run IDs, checks against today's criteria, contributions, bottleneck and hypothesis |

## Schedule

10:00–10:20 commission and planning; 10:20–12:00 repo separation and first run; 12:00–12:30 break; 12:30–14:00 product, tests and correction; 14:00–14:35 demo/review; 14:35–15:00 save evidence and costs.

**Definition of Done:** The small product version can be demonstrated, its agent contribution is technically evidenced, human review is recorded, and effort/gaps are reported honestly. The complete website is due in S4.
