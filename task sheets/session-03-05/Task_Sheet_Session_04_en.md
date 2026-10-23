# Session 4 – Deliverable website and a dependable Factory quality gate

**10:00–15:00 · Customer project 01 · Required: [Customer brief](Client_Brief_Nordwerk_en.md)**  
Assessment: [Session 4 rubric](Bewertungsraster_Termin_04_Factory.md).

## Daily target and learning objectives

Deliver an independently runnable release candidate meeting AC-01–AC-08. The Factory handles further customer tasks and reliably distinguishes accepted results from results requiring correction. Save a baseline measurement for the improvement in Session 5.

- **L4.1:** Reuse the Factory on the same customer project without copying agents into the product.
- **L4.2:** Combine automated checks and human review into an effective release gate.
- **L4.3:** Detect a controlled fault and block or correct the delivery.
- **L4.4:** Preserve a reproducible baseline experiment for a later Factory change.

## 1. Review and plan

Open the S3 evidence. Check the bottleneck, remaining acceptance criteria and effort. Prioritise missing mandatory content. Do not promote optional features to required scope. Treat each product change as a task with an accountable person and expected result.

## 2. Complete the release candidate through the Factory

Use the Factory to address the missing services, target groups, working approach and navigation. At least one further substantial product task must pass through a real agent run with tool use, checks and a human decision. Reuse configuration and workflow; document necessary adaptations. Manual work is allowed and recorded visibly.

Create a review PR or an equivalent inspectable diff with an approval record. Automatic merging is not required. Identify the candidate by tag or exact commit and document startup from a fresh product checkout without a running Factory.

## 3. Exercise the quality gate

Automate at least three different product checks: required content, contact/navigation targets and local references/assets. One meaningful check per family is sufficient. Additionally inspect 375/1280 px layouts and keyboard navigation/focus in a browser, recording results and reviewer. Browser automation is optional; a screenshot alone does not establish working navigation.

In an isolated test copy, introduce exactly one fault: change the contact address to an incorrect value or break an internal link. Show that a check fails and the workflow does not label this version approved. Correct the fault and check again. Do not leave an intentional fault in the final delivery. Factory tests must cover positive and rejected/escalated gate states; distinguish real LLM runs from deterministic tests.

## 4. Preserve baseline experiment R-01

Repeat this same experiment after a Factory change in S5. Freeze a base commit **R-BASE** from your candidate. Reference task R-01 is:

> Add a service card headed **“Projektkoordination”** with the text **“Wir koordinieren klar abgegrenzte technische Vorhaben mit Ihrem Team.”** Preserve all previous content, contact targets and navigation.

R-01 is an isolated reference task, not an additional customer requirement. Run it using the current Factory **F-BASE** on a separate branch/checkout of R-BASE. Do not merge the experimental output into the customer release. Record input, criteria, model/settings, Factory/product commits, run IDs, check results, review/rework time and known costs. One complete run is required; two repetitions are recommended if time permits. Include failed attempts.

Choose a bottleneck from S3/S4 and formulate one small improvement for S5 that can be checked using R-01. For example, check required copy deterministically before the human gate. Necessary repairs for today's candidate may happen first; the change being investigated starts only after the baseline is saved.

## 5. Submit

| Location | Required submission |
|---|---|
| Product repo | Candidate commit/tag, AC-01–08 checklist, product tests, browser review, start/test instructions, inspectable delivery diff |
| Factory repo | Further real task run, gate tests, controlled fault evidence, R-01 baseline and hypothesis |
| `evidence/session-04.md` | Commit/run references, approval, costs including failed attempts, plan budget deviation and next change |

## Schedule

10:00–10:20 planning; 10:20–12:00 completion; 12:00–12:30 break; 12:30–13:30 tests and fault case; 13:30–14:15 R-01 baseline; 14:15–14:35 candidate demo; 14:35–15:00 snapshot and costs.

**Definition of Done:** An inspectable candidate meets AC-01–08, a faulty test version has actually been blocked, and the S5 baseline is reproducible. The new customer change and security response are not due today.
