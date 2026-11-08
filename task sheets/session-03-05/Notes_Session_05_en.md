# Session 5 – Implementation Notes for All Teams (EN)

**Agentic AI elective project · 9 November 2026 · Clarifications, not a new assignment**

The existing [Session 5 task sheet](https://github.com/MARS-Group-HAW/agentic_ai/blob/main/task%20sheets/session-03-05/Task_Sheet_Session_05_en.md), [Nordwerk customer brief](https://github.com/MARS-Group-HAW/agentic_ai/blob/main/task%20sheets/session-03-05/Client_Brief_Nordwerk_en.md) and unchanged [assessment rubric](https://github.com/MARS-Group-HAW/agentic_ai/blob/main/task%20sheets/session-03-05/Bewertungsraster_Termin_05_Factory.md) remain authoritative. **No new deliverables, scoring rules or agent quotas** are introduced. These notes clarify existing expectations in light of Session 4 results.

## 1. R-01: establish comparable baselines before optimisation

- Before changing the Factory, verify that F-BASE and R-BASE identify the **actual executed Git commits**, not merely tags with mismatched targets.
- Use a clean starting checkout. Record `git status`, Factory/product commit IDs, model/provider, settings, the same R-01 task and acceptance checks, and a unique run ID.
- If the S4 baseline is incomplete or unreproducible, rerun it **before** changing the unchanged Factory; label it **S5 catch-up**. This does not change the S4 assessment.
- Run F-NEW on a **fresh copy of exactly the same R-BASE**. Do not feed the prior R-01 output or patch into the new run. Keep model and settings fixed; vary only the intended Factory improvement.
- Record failed but fully observed attempts as well. **A positive improvement is not required**; one before/after pair supports only a preliminary observation.

## 2. Complete costs without double counting

- Include all relevant agent runs, failed attempts and CI workflow runs (including failed GitHub Actions runs) for S5 and the S3–S5 totals. Identify unrelated runs separately as Factory development or internal work.
- Assign human time **exclusively** to Factory development, customer delivery, review, or rework; never count the same period twice.
- Distinguish **operational R-01 delivery costs** from the one-off engineering cost of F-NEW. Missing token or usage measurements should be marked `unknown`, not silently set to zero.
- Validate that `costs/usage.csv` parses correctly and the totals and CI counts reconcile with source evidence.

## 3. Link release approval to actual product evidence

- Link customer task/issue, starting commit, run ID, agent-created diff, product check results, resulting commit, named human reviewer, approval decision, and timestamp.
- Keep **three states separate**: (a) Nordwerk customer release candidate, (b) isolated R-01 experiment, and (c) intentionally faulty test copy. R-01 is **not** an additional customer requirement.
- Make the product accessible to evaluators: public commits or a complete inspectable ZIP/commit/diff record. A private URL alone is insufficient evidence.
- Technical team approval is **not** customer acceptance. Record the instructor's decision separately; pending customer acceptance is explicitly allowed by the task sheet.

## 4. Keep scope tight and spend time on learning

- **CR-01:** A short English landing page is sufficient. No full translation of detailed copy or new framework is needed. Preserve the German site and regression checks AC-01–08.
- **SR-01:** Approximately one page maximum for the fact-checked customer answer plus a concise component inventory. Separate known facts from uncertainties, cite sources and access dates. No penetration test is required.
- **Factory experiment:** One targeted change and at least one traceable before/after pair; compare quality, review/rework and total known cost rather than adding agent features.
- **Evidence:** A concise `evidence/session-05.md` with links, decisions, cost totals and three evidence-based transferable lessons. No additional long report is required.

**SR-01 references:** [ENISA, 21 October 2026](https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities) and the [official PHP 2026 security releases](https://www.php.net/archive/2026.php). Both sources are available. The statement “PHP 8.2” alone proves neither exposure nor remediation.

**Learning priority:** Demonstrable change delivery, effective human quality control and a reproducible empirical Factory improvement matter more than the number of agents or visual polish.
