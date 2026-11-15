# Session 8 – Deliver shipping changes and assess Factory effects

**10:00–15:00 · Customer project 02 · Version 1.0, 8 November 2026**  
Required: [customer brief](Client_Brief_HansePack_en.md), [reference cases](HansePack_Referenzfaelle.json). Assessment: [S8 rubric DE/EN](Bewertungsraster_Termin_08_Factory.md).

## What you actually do today

Implement new shipping terms in the existing calculator, deliver a checked release and assess one targeted Factory improvement using the same experiment as S7. Keep the customer change separate from the Factory experiment.

**Objectives:** L8.1 deliver a business change using the same Factory; L8.2 protect unchanged rules with regression checks; L8.3 assess a Factory change under comparable conditions; L8.4 judge effort/reuse across two customers with evidence.

## 1. Implement customer change CR-02

> From now on, shipping costs EUR 15.00 below EUR 400.00 goods net after discount, and is free from exactly EUR 400.00. Discounts, rounding, items and validation remain unchanged.

Record impact and affected tests in the change issue. Use your Factory to change the S7 product to **HP-V2**. Evidence at least two agent capabilities, a real model/tool run and an agent product diff. Humans check and decide on the exact output commit. Explain at least Q06, Q10 and Q11 during review: discount before shipping threshold, exactly at the new threshold and just below it.

## 2. Check regression and delivery

Check all Q01–Q14 under HP-V2 and E01–E10; line values and discounts remain identical to HP-V1. Only shipping, dependent total and rule-version label change. Do not treat obsolete shipping expectations as V2 regressions. Both rule versions need not run concurrently: preserve V1 commit/results and use V2 tests for the new version.

A human enters a multi-line quotation in the UI and checks shipping/total and downloaded JSON. Demonstrate fresh checkout and product tests without Factory. HP-AC01–07 remain applicable with updated shipping values; add HP-AC08/09. Leave Nordwerk files unchanged and its last version separately available.

## 3. Evaluate one Factory improvement against R-02

Before the planned change, verify a full S7 baseline and actual **F-BASE/Q-BASE** commits. If necessary, rerun before changing the unchanged Factory and label **S8 catch-up**; this does not alter the S7 assessment.

Implement exactly one small justified Factory change as **F-NEW**. Execute precisely S7's R-02 from a fresh isolated copy of the same **HP-V1-Q-BASE**, not the changed HP-V2 product. Keep model/provider/settings and acceptance checks identical; do not reuse completed baseline output, patches or caches that alter initial conditions. Changed Factory policies may be part of the named intervention.

R-02: JSON export field `calculation_note` with `Net amounts; shipping shown separately.`, a test for it, and preserved values/display/error handling. Do not merge experimental output into the customer release. Use identical independent acceptance checks in both variants; agents may add tests but cannot change binding criteria.

At least one full before/after run is required; two per variant recommended if time permits. Compare quality, faults, human delivery/review/rework time and known agent/CI costs; show one-off improvement effort separately. Approximately one-page report maximum plus raw records. No positive effect required; justify retaining, adapting or reverting. One pair supports a preliminary observation, not general superiority.

## 4. Acceptance and economic review

Version the customer release and hand over startup, tests and rule description. The instructor decides as customer; mark pending decisions separately. `evidence/session-08.md` links product/Factory commits, run IDs, checks, approvals, experiment and S6–8 cost totals.

Answer three questions with evidence: which Nordwerk capability was actually reused, what work remained customer-specific, and which Factory investment would you retain for a third customer? Do not equate different commissions with a controlled before/after benchmark. If no task was accepted, report failure and cost rather than cost-per-accepted-task. Consider small samples/team size; do not infer euro profit.

**Submit by 15:00:** checked HP-V2 release, real change run, R-02 comparison with raw records, reconciled costs and true customer status. No extra agent or feature required merely for greater complexity.

## Schedule

10:00–10:20 impact analysis; 10:20–11:20 Factory change/experiment; 11:20–12:00 CR-02; 12:00–12:30 break; 12:30–13:30 finish CR-02/regression; 13:30–14:10 product review/totals; 14:10–14:35 customer demo; 14:35–15:00 preserve evidence.
