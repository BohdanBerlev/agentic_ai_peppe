# Customer project 01 – Nordwerk Industrie-Service

**Binding customer brief · Sessions 3–5 · Version 1.0, 23 October 2026**

## Commission and starting point

We are Nordwerk Industrie-Service, a fictional small B2B service provider in Hamburg. So far, referrals generate our business. Prospective customers should now be able to understand our services, target groups and contact options online, and request information by email without commitment. The instructor acts as the customer and records binding clarifications for all teams.

Our previous externally hosted PHP website provides content editing and a contact form. For the initial replacement, we accept a static site and an email link. A CMS and a form are outside scope. The later security enquiry is a separate advisory task within this project.

## Required content for the first release candidate

The initial website is in German, including for the international team. Use the supplied German strings; do not spend time inventing copy.

| ID | Content |
|---|---|
| N-01 | Company name: **Nordwerk Industrie-Service** |
| N-02 | Main statement: **Praktische Unterstützung für Ihren technischen Betrieb.** |
| N-03 | Wartungsplanung: **Wir strukturieren Wartungsaufgaben und dokumentieren Zuständigkeiten für kleine technische Betriebe.** |
| N-04 | Ersatzteilkoordination: **Wir unterstützen bei der Abstimmung von Ersatzteilbedarfen und Lieferterminen.** |
| N-05 | Betriebsdokumentation: **Wir bringen technische Unterlagen in eine nachvollziehbare und nutzbare Struktur.** |
| N-06 | Target groups: **Kleine Produktionsbetriebe** and **Technische Serviceunternehmen** |
| N-07 | Working approach: **Ein fester Ansprechpartner, ein gemeinsam vereinbarter Leistungsumfang und nachvollziehbare Ergebnisse.** |
| N-08 | Contact: **Anfrage stellen**, linking to `mailto:kontakt@nordwerk.example` |
| N-09 | Course notice: **Fiktives Unternehmen – Lehrprojekt der HAW Hamburg. Keine realen Angebote oder Kontaktaufnahme.** |

The `.example` address is a placeholder; do not send messages. Do not invent customer logos, certifications, references, response times or success statistics. Layout and headings may supplement the required content without changing its factual meaning. A logo is optional; images and external font/tracking services are unnecessary.

## Acceptance criteria

| ID | Check | Due |
|---|---|---|
| AC-01 | Company name and main statement are easy to find on the initial view. | S3 |
| AC-02 | All three services and their descriptions are identifiable. | S4 |
| AC-03 | Both target groups and the working approach are included; no invented promises. | S4 |
| AC-04 | Clearly labelled contact link targets `mailto:kontakt@nordwerk.example`; the course notice is visible. | S3 |
| AC-05 | Navigation reaches services and contact; internal links and local assets work. | S4 |
| AC-06 | At widths of 375 px and 1280 px there is no horizontal content overflow; text and contact remain usable. | S4 |
| AC-07 | Document title, German language metadata, meaningful headings and visible keyboard focus; appropriate alternative text if images exist. | S4 |
| AC-08 | A fresh product checkout starts with a documented command without the Factory, LLM or Factory database; product tests run separately. | S4 |
| AC-09 | CR-01 from Session 5 is met; German content, navigation and contact continue to work. | S5 |
| AC-10 | Component inventory, a properly scoped SR-01 response and recorded customer acceptance are provided. | S5 |

S3 also requires one service from AC-02. S4 requires AC-01–AC-08. S5 adds only CR-01 and SR-01 as specified in its task sheet. A single page with anchors is sufficient. No payment, accounts, analytics, real personal data or public deployment required. Acceptance is for the course; it does not certify legal readiness for production.

## Delivery and evidence contract

The existing team repository is the **Factory**; a new `client-01-website` repository contains the customer product, product tests and delivery documentation. Other names are acceptable. The Factory retains the mandatory stack from Sessions 1/2. For the product, HTML/CSS, a little JavaScript and a simple local web server are pre-approved. No PHP/CMS implementation required. Other frameworks follow the existing course approval rule. This project adds no new agent-count quota; existing organisational role requirements continue to apply.

A real run includes: customer task → at least two technically cooperating agent capabilities exchanging structured data → a real LLM call through the existing provider abstraction → a real tool operating on the product checkout → product artifact/patch → checks → human approval or rejection. Agent contributions must produce a substantial, verifiable requirement, product change or check; merely rewriting a README is insufficient. At least one agent must edit a product file or produce an applicable patch. Manual implementation, patch application and correction are allowed and recorded. An external chat or editor assistant alone is not evidence of your Factory.

Each run has a unique `run_id` and project-specific storage, for example `runs/website-01/<run_id>/`. Link input/output commits, Factory commit, issue/task, acceptance criteria, model/settings, agent roles, tool actions, result, checks, approval and costs. Freeze the input commit before starting; store the manifest and supporting files afterwards in a separate evidence commit. This avoids circular commit references. Raw traces may be separate files or accessible CI artifacts with a durable summary; do not overwrite shared logs. Traces need not contain internal model reasoning: inputs/outputs, actions and results suffice.

Keep secrets outside repositories. Running agents may modify only the approved product area; separate run directories remain writable. Test rejected write access only in a temporary test environment. Changes to the Factory itself remain human-accountable engineering work.

## Costs and end-of-session handover

Use the existing model: human work 100 credits per person-hour; agent call 1 credit plus 0.01/s, input 0.02/1,000 tokens, output 0.04/1,000 tokens; CI run 1 credit. Mark unavailable token counts as unknown and label known costs as partial costs. Do not enter fictitious zeroes. Assign human work exclusively to Factory development, delivery, review or rework; do not add the same time again as general work. Include failed attempts and discarded results. Course credits are not euro estimates.

At the start of S3, agree and record a delivery plan budget for S3/S4 with the instructor, separately from Factory development, plus a reserve for S5. If no instructor amount is specified, the justified team estimate is the baseline. There is no hidden common cost ceiling and no reward for the smallest budget. Explain deviations rather than altering data.

For each session, submit `evidence/session-0N.md` in the Factory repo: Factory/product repository and commit references, relevant tasks/PRs, run IDs, AC checks, costs, approvals and at most three next actions. No lengthy additional daily report is needed.
