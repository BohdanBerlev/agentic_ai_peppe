# Customer project 02: HansePack quotation calculator

**Binding brief for Sessions 6–8 · Version 1.0 · 8 November 2026**

## The commission

HansePack Handelsgesellschaft is a fictional B2B packaging supplier. Three sales staff currently prepare quotations using spreadsheets and manually correct discount/shipping errors. Build a small local web application: select items and quantities, calculate a quotation, inspect it and download JSON. The UI may be German or English; all teams share identical rules and mandatory scope.

Create a new product repo, for example `client-02-quotation`, and develop it through your existing Factory. **Reuse the Factory; do not turn the Nordwerk website into the calculator.** Changing only a project name while retaining hardcoded Nordwerk paths is not reuse.

## Scope and technology

A simple page for items, quantities, lines, calculation and download is sufficient. Implement deterministic business logic in Python; FastAPI and basic HTML/CSS/JavaScript are pre-approved. Existing course rules apply to other frameworks. A product JSON catalogue is sufficient; no database required. Runtime must work without Factory or LLM. Document Python/dependencies, startup and test commands. No login, ERP, PDF, payments, real customer data, public deployment or AI in the product required.

## Catalogue and binding business rules

The binding input [HansePack_Katalog.json](HansePack_Katalog.json) defines prices per sales unit:

| SKU | Product | Price cents | Display EUR |
|---|---|---:|---:|
| HP-BOX | Shipping box | 250 | 2.50 |
| HP-TAPE | Packing tape | 400 | 4.00 |
| HP-FILM | Stretch film | 1250 | 12.50 |

1. A quotation contains 1–3 lines. Each SKU occurs at most once. Quantities are integers from 1 to 10,000. Unknown items, duplicate SKUs, empty lists, missing values, strings instead of numbers, fractional and Boolean quantities are invalid. Do not silently coerce, round or aggregate invalid input.
2. Per line, list amount = quantity × unit price. Quantity discount applies to the **entire list amount of that line**, not marginal tiers and not quantities summed across SKUs: 1–49 units 0%, 50–99 units 5%, 100+ units 10%.
3. Round each line's discount amount to whole cents using **ROUND_HALF_UP**. Line net = list amount minus rounded discount. Use integer cents or Decimal, not binary floating-point rounding. For integer rates, `(list_amount_cents * discount_percent + 50) // 100` is one possible calculation.
4. Goods net = sum of line net amounts. **Rule version HP-V1, S6/S7:** shipping is 1,200 cents below 50,000 cents goods net, otherwise zero. Evaluate the inclusive threshold after discounts and before shipping. Total = goods net + shipping.
5. All amounts are simulated net EUR amounts; no VAT calculation. Show “Net amounts – course project, not a binding quotation”. This course rule is not tax advice.
6. Invalid input produces understandable errors and no apparently valid quotation. No exact HTTP status is prescribed; distinguish error and success clearly. Client-side checks do not replace validation in the Python business logic.
7. Display and JSON export include SKU, quantity, unit price, list amount, discount rate, discount amount and line net for each line, plus goods net, shipping, total, currency and rule version. Export money as integer cents. Export and visible calculation agree exactly. Timestamps/quotation numbers are optional and excluded from reference totals.

## Reference cases and expected results

These are customer-provided results, not outputs from your generating agent. Complete inputs and line values are in [HansePack_Referenzfaelle.json](HansePack_Referenzfaelle.json). Tests may load them; product logic must not simply return stored answers by case ID.

| Case | Lines | Goods net cents | Shipping HP-V1 | Total HP-V1 | Shipping HP-V2 | Total HP-V2 |
|---|---|---:|---:|---:|---:|---:|
| Q01 | BOX × 1 | 250 | 1200 | 1450 | 1500 | 1750 |
| Q02 | BOX × 49 | 12250 | 1200 | 13450 | 1500 | 13750 |
| Q03 | BOX × 50 | 11875 | 1200 | 13075 | 1500 | 13375 |
| Q04 | BOX × 99 | 23512 | 1200 | 24712 | 1500 | 25012 |
| Q05 | BOX × 100 | 22500 | 1200 | 23700 | 1500 | 24000 |
| Q06 | BOX × 200 | 45000 | 1200 | 46200 | 0 | 45000 |
| Q07 | FILM × 40 | 50000 | 0 | 50000 | 0 | 50000 |
| Q08 | FILM × 39 | 48750 | 1200 | 49950 | 0 | 48750 |
| Q09 | TAPE × 100 | 36000 | 1200 | 37200 | 1500 | 37500 |
| Q10 | FILM × 32 | 40000 | 1200 | 41200 | 0 | 40000 |
| Q11 | FILM × 31 | 38750 | 1200 | 39950 | 1500 | 40250 |
| Q12 | BOX × 50; TAPE × 10 | 15875 | 1200 | 17075 | 1500 | 17375 |
| Q13 | FILM × 51 | 60562 | 0 | 60562 | 0 | 60562 |
| Q14 | BOX × 53 | 12587 | 1200 | 13787 | 1500 | 14087 |

BOX/TAPE/FILM abbreviate the full SKUs. Q04 rounds a 1,237.5-cent discount to 1,238; Q13 rounds 3,187.5 to 3,188. Q06 checks the shipping threshold after discount. Q14 requires a 662.5 → 663-cent discount, distinguishing HALF_UP from rounding to the nearest even integer.

## Acceptance criteria: what must work, and when?

**HP-AC** means HansePack acceptance criterion, independent of Nordwerk AC-01–10.

| ID | Specific requirement | Due |
|---|---|---|
| HP-AC01 | Separate product repo, documented independent startup and test command, no Factory runtime dependency. | S6 initial version; S7 fresh checkout |
| HP-AC02 | Python business logic calculates Q01 and Q03 completely correctly; output includes lines, discount, shipping and total. | S6 |
| HP-AC03 | All Q01–Q14 under HP-V1 correct including line amounts; discount boundaries, rounding and shipping correct. | S7 |
| HP-AC04 | All invalid E01–E10 cases rejected in business logic; no valid quotation produced. | S7; S6 at least E01 |
| HP-AC05 | Simple web UI supports entering lines, calculating, showing results and understandable errors; net-amount notice visible. | S7 |
| HP-AC06 | JSON export includes required fields and matches calculation/display. | S7 |
| HP-AC07 | Fresh checkout, reproducible product checks, human usage review and release candidate recorded. | S7 |
| HP-AC08 | CR-02 delivered: all Q01–Q14 correct under HP-V2, discounts/validation preserved, UI/export consistent. | S8 |
| HP-AC09 | Versioned release, handover notes and true technical approval/customer acceptance status recorded. | S8 |

## Announced change CR-02 – Session 8 only

“Change shipping terms: below EUR 400.00 goods net after discount, charge EUR 15.00 shipping; from exactly EUR 400.00 shipping is free. Everything else remains unchanged.” This is **HP-V2**. No retroactive recalculation of saved quotations is required because storage is outside scope. Final runtime need not offer a V1/V2 selector; historical V1 versions remain inspectable through Git. Tests target the relevant rule version; V2 must not be assessed against obsolete V1 shipping expectations.

## Factory evidence and costs

Each session includes at least one real customer task with two cooperating agent capabilities, structured handovers, real LLM through the existing provider abstraction, real tool use and agent-edited product code or applicable patch. Manual application/correction is allowed and recorded. External chat/editor use alone does not replace your Factory. No new agent quotas. Retain course stack, local/HAW ICC models and no cloud tokens.

Link run ID, project ID, task, actual Factory commit, product input/output commits, model/settings, tool actions, checks, reviewer, decision and timestamp. Record clean input states with `git status`. Store manifests in a later evidence commit to avoid circular hash requirements. Separate project workspaces/logs; new customer context must not overwrite Nordwerk. Freeze the Nordwerk product commit and keep it independently runnable after the switch; no rebuild of the previous project required.

Existing credit model: human 100/person-hour; agent call 1 plus 0.01/s, input 0.02/1,000 tokens, output 0.04/1,000; CI workflow run 1, including failed runs. Assign human time exclusively to Factory development, customer delivery, review or rework. Include failures, mark missing values `unknown`, label known totals as partial costs where needed. Agree S6/S7 delivery budget and S8 change reserve with instructor or use justified team estimates; no hidden ceiling. Identify project-switch effort. Separate operational experiment costs from one-off improvement effort. Credits are not euro estimates.

Submit one concise Factory-repo index per session, `evidence/session-06.md`, `session-07.md` or `session-08.md`, with evidence links and at most three next actions. Provide accessible repos or inspectable ZIP/commit/diff evidence; inaccessible private URLs alone are insufficient. Distinguish technical team approval from instructor/customer acceptance; mark pending decisions.
