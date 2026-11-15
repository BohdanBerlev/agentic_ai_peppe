# Session 7 – Correct quotations and effective fault detection

**10:00–15:00 · Customer project 02 · Version 1.0, 8 November 2026**  
Required: [customer brief](Client_Brief_HansePack_en.md), [catalogue](HansePack_Katalog.json), [reference cases](HansePack_Referenzfaelle.json). Assessment: [S7 rubric DE/EN](Bewertungsraster_Termin_07_Factory.md).

## What you actually do today

Complete the calculator for the original HP-V1 rules. Demonstrate that the Factory blocks an incorrect delivery after an intentionally introduced discount fault. Then preserve a baseline measurement for S8.

**Objectives:** L7.1 repeatable agentic delivery; L7.2 integrate independent business tests into effective approval; L7.3 detect and correct a business fault; L7.4 preserve a comparable baseline for a Factory improvement.

## 1. Complete calculation scope and a small UI

Plan remaining HP-AC01–07 requirements. At least one real new customer task passes through your Factory, such as rounding, input validation or export. Record output diff, real agent/tool use, structured cooperation of at least two capabilities and a human decision.

Implement all three items, quantity discounts, HALF_UP discount rounding and original shipping rule. Build the small web UI and JSON download from the brief. Invalid inputs must reach and be checked by Python business logic; UI-only validation is insufficient. Supply display/export from the same actual calculation data.

## 2. Test customer-provided results

Run your own tests for Q01–Q14 under HP-V1 and all invalid E01–E10 cases. Check line values and totals. Do not replace reference data with convenient agent outputs. Investigate rule and implementation when results differ; do not silently change expected values. Escalate unclear specifications to the instructor.

A human executes at least one multi-line quotation in the UI, downloads JSON, compares display/export and tries an invalid quantity. A fresh product checkout must start according to instructions without the Factory. Run Factory/product tests separately; supplied starter tests do not replace business tests.

## 3. Introduce a controlled business fault

In a separate test branch/checkout, change exactly one condition: the 5% discount incorrectly starts **above 50** rather than **at 50**. Leave customer expectations unchanged. Q03 must fail: incorrect total 13700 instead of 13075 cents.

Have the Factory run its product checks. Show in the workflow that the result blocks approval or triggers correction; a report without a consequence is insufficient. Correct, rerun and record the human decision. Factory tests cover passed and blocked gate states; they may mock model calls. Do not release the isolated faulty version.

## 4. Run reference task R-02 once before improvement

Freeze the correct HP-V1 candidate as product base commit **Q-BASE**, and current Factory as **F-BASE**. R-02 is:

> Add `calculation_note` to exported quotation JSON with fixed text `Net amounts; shipping shown separately.`. Preserve display, money values and error handling. Add a test for the field; all existing business tests must still pass.

R-02 is an experiment, not a customer requirement. Run it from a clean isolated Q-BASE copy. Do not merge its result into the customer candidate. Record input status, actual commits, model/provider/settings, task, checks, run ID, quality, human review/rework and known costs. One full run required; two recommended if time permits. A failed full run is also a baseline; keep its failure visible.

Select an observed Factory bottleneck and plan a small S8 change, such as structured test tasks or a targeted deterministic export gate. Implement the investigated change only after preserving the baseline. Necessary repairs for today's candidate may happen first.

**Submit by 15:00:** versioned HP-AC01–07 candidate, product/Factory tests, human UI/export review, detected/corrected fault, R-02 baseline and hypothesis. In `evidence/session-07.md`, link commits/runs and costs including failed CI runs and plan deviations.

## Schedule

10:00–10:20 plan; 10:20–12:00 finish app; 12:00–12:30 break; 12:30–13:30 business tests/fault case; 13:30–14:15 R-02; 14:15–14:35 candidate demo; 14:35–15:00 evidence/costs. HP-V2 shipping change is due in S8 only.
