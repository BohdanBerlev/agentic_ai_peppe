# Session 6 – Second customer, same Factory

**10:00–15:00 · Customer project 02 HansePack · Version 1.0, 8 November 2026**  
Binding attachments: [Customer brief with calculation rules and acceptance criteria](Client_Brief_HansePack_en.md), [catalogue](HansePack_Katalog.json), [reference cases](HansePack_Referenzfaelle.json). Assessment: [S6 rubric DE/EN](Bewertungsraster_Termin_06_Factory.md).

## What you actually do today

Configure your existing Factory for a second customer and deliver a small correct quotation case. Do not build another Factory or add unrelated customer features to Nordwerk.

**Objectives:** L6.1 evidence project switching/reuse; L6.2 deliver a real agent product contribution; L6.3 check business rules against independent reference values; L6.4 record project-start effort and reuse limits.

## 1. Clarify the commission and create a product repo

Read the brief, especially discount and rounding rules. Create `client-02-quotation` or equivalent separate repo. Copy catalogue and reference cases unchanged as customer fixtures; a checksum or unchanged Git version establishes provenance. Record questions and explicit assumptions in the customer issue. Plan S6/S7 delivery and an S8 reserve. The instructor is the customer; binding answers apply to all teams.

Freeze the latest Nordwerk product commit. Configure customer ID, checkout, tasks and check path for HansePack in the existing Factory. Show which agents/tools remain unchanged and which adaptations are needed. Implement new generic capabilities centrally when necessary, not as hardcoded agent duplicates. Test project assignment deterministically: a HansePack task must not change Nordwerk product files. Use temporary test directories and do not damage real unrelated data.

## 2. Deliver one complete quotation case

Give your Factory a task such as: “Implement Python calculation for HP-BOX quantities 1 and 50, including discount, shipping and total. Reject quantity 0.” At least two agent capabilities actually exchange structured data; an agent produces a product change or applicable patch. Evidence real model/tool use and human review. Manual additions remain allowed but count as human work.

Today a Python function with reproducible invocation, CLI or API is sufficient. A complete web UI and download are due in S7. Product runtime works without Factory/LLM. Use deterministic calculation logic, not an LLM call to determine prices.

## 3. Run concrete checks

| Today's check | Expected result |
|---|---|
| Q01: HP-BOX × 1 | Goods net 250, shipping 1200, total 1450 cents |
| Q03: HP-BOX × 50 | List 12500, discount 625, goods net 11875, shipping 1200, total 13075 cents |
| E01: quantity 0 | Understandable error; no valid quotation |
| Project isolation | HansePack run changes no Nordwerk file; last Nordwerk version remains independently runnable |

These requirements specify HP-AC01/02 and the first part of HP-AC04. Write and run your own automated product checks against supplied values; a generating agent's assertion is not a business test. A human checks output and code diff. Run a Factory project-assignment test with `python -m pytest`; document a separate product test command. Tests may mock models; evidence the real product run separately.

## 4. Preserve evidence and costs

Link customer issue, input commit, run ID, Factory commit, agent contribution, product test, output commit, reviewer and decision. Identify setup time for the second customer separately. Briefly record what was reused, what remained customer-specific and which one weakness to investigate next. Do not yet claim causal savings over Nordwerk: these are different commissions.

**Submission by 15:00:** new independently runnable product, passing Q01/Q03/E01 checks, real Factory run, project-isolation test, inspectable Nordwerk version and `evidence/session-06.md` with costs, references and at most three next actions. A complete quotation app is not required today.

## Schedule

10:00–10:20 commission/plan; 10:20–11:15 repos and project switch; 11:15–12:00 first run; 12:00–12:30 break; 12:30–14:00 calculation/checks/correction; 14:00–14:35 demo/review; 14:35–15:00 snapshot/costs.
