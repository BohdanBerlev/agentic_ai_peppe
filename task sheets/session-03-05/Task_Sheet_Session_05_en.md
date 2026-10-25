# Session 5 – Customer change, security enquiry and Factory experiment

**10:00–15:00 · Customer project 01 · Required: [Customer brief](Client_Brief_Nordwerk_en.md)**  
Assessment: [Session 5 rubric](Bewertungsraster_Termin_05_Factory.md).

## Daily target and learning objectives

Deliver a limited change to the existing website, respond to a security enquiry and test one targeted Factory improvement against the S4 baseline.

- **L5.1:** Deliver a change from a versioned product baseline using the same Factory.
- **L5.2:** Assess the effect of a Factory change honestly under comparable conditions.
- **L5.3:** Distinguish exposure, assumptions and response options in a security enquiry.
- **L5.4:** Connect product acceptance, costs and reusable Factory lessons.

## 1. Customer change CR-01

> We want to enable international enquiries and also address technical purchasing departments. Please add a short English landing page or clearly labelled English view. Preserve the existing German website.

Create a change issue and short impact analysis. Use your Factory to make the product change. The English view must include:

| Element | Required content |
|---|---|
| Title | **Nordwerk Industrie-Service** |
| Main statement | **Practical support for your technical operations.** |
| Services | **Maintenance planning**, **Spare parts coordination**, **Operational documentation** |
| Additional target group | **Technical purchasing departments** |
| Contact | **Request information**, `mailto:kontakt@nordwerk.example` |
| Notice | **Fictional company – HAW Hamburg course project. No real offers or contact.** |

Also add **“Technische Einkaufsabteilungen”** as a target group on the German view. Both views provide access to language switching and contact; the English view has appropriate language metadata and document title. A brief English entry page is sufficient; a full translation of all detailed copy is unnecessary. Check new content automatically and run AC-01–08 as regression checks; repeat browser review at 375/1280 px and using the keyboard. Do not invent figures or service promises.

## 2. Security enquiry SR-01

> We have heard about critical PHP vulnerabilities. Is our existing site affected? Can we safely use your new website, and who will handle updates?

**Supplied system profile, dated 23 October 2026:** Old site externally hosted; operator says “PHP 8.2”, exact package/patch and CMS versions unknown; CMS and contact form present; no admin access and no reliable hosting-provider statement about fixes. No evidence of a confirmed attack. The new course website uses only the components you actually chose.

Read the [ENISA statement dated 21 October 2026](https://www.enisa.europa.eu/news/joint-statement-on-critical-php-vulnerabilities) concerning CVE-2026-109618 and CVE-2026-109619. Use the linked PHP source for detailed claims. Record source and access date. If access is unavailable during class, the instructor supplies a dated extract of that same primary source; state this limitation.

Write a short customer response, approximately one page maximum: what is known, what is uncertain, what information must the host provide, what immediate action is appropriate, and how do updating, temporary isolation and static replacement differ? “PHP 8.2” alone proves neither exposure nor remediation. Do not claim “static = secure”. Explain lost CMS/form functionality and maintenance responsibility. Inventory the runtime and build/test components of your new delivery with version/reference or “not used”. An agent may prepare the response; a human checks facts and approves it. No live attack or vulnerable server is required.

## 3. Evaluate one Factory change

Implement the small improvement justified in S4. Repeat R-01 with **F-NEW** on a fresh copy of the same **R-BASE**; use the identical task and acceptance criteria, same model and recorded settings. Isolate run state and experimental outputs. Do not reuse the completed baseline solution as hidden input. Do not change the model and workflow at the same time.

At least one complete before and after run is required; two per variant are recommended if time permits. Compare acceptance/regressions, review/rework time, faults and known delivery costs. Report Factory development effort separately. A single pair supports only a preliminary observation. An unsuccessful optimisation is a valid outcome of a sound experiment: justify retaining, adapting or reverting it.

If the S4 baseline is missing, run it before making the change using the unchanged Factory and label it an S5 catch-up. Never reconstruct it from memory. This does not retroactively replace the S4 evidence.

## 4. Acceptance and handover

Deliver a release commit/tag, start/test instructions and maintenance note. The instructor accepts against AC-01–10 or records outstanding defects. If no customer decision is possible by 15:00, distinguish technical approval from pending customer acceptance. Do not self-declare customer acceptance.

| Location | Required submission |
|---|---|
| Product repo | CR-01 change with review diff, regression results, SR-01 response/component inventory, release and handover |
| Factory repo | Real change run, implemented improvement, R-01 comparison with raw data, costs and decision |
| `evidence/session-05.md` | Commit/run references, AC-01–10, technical approval and customer status, S3–5 totals and three transferable lessons |

## Schedule

10:00–10:20 impact analysis; 10:20–11:20 Factory change and comparison; 11:20–12:00 customer change; 12:00–12:30 break; 12:30–13:30 finish change/regression; 13:30–14:10 security response; 14:10–14:35 acceptance; 14:35–15:00 evidence and review.

**Definition of Done:** Versioned customer product, traceable change delivery, properly scoped security response and honest Factory comparison. A positive optimisation effect is not required to meet the learning objective.
