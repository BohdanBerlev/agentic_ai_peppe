# Session 3 – Customer assignment CUST-001: RequestBoard

**Monday, 26 October 2026 · 10:00–15:00**
**Fictional customer:** CampusService, a university's internal IT support team.
**Customer representative:** instructor. The assignment is identical for all teams.

## The customer's request

“Our small service team receives requests through several channels. We lose track of urgent requests and work already in progress. We need a simple, reliable service that stores requests, filters them by priority and status, and updates their progress. Today we want a demonstrable first version.”

Extend your existing Session 2 work-item implementation. Reuse your platform. Assessment recognises the evidenced customer contribution and closure of relevant gaps rather than rewarding a rewrite.

## Required MVP and API contract

A request has `id`, `title`, optional `description`, `priority` and `status`. Use synthetic examples, not personal data. Existing extra fields such as timestamps may remain.

| Operation | Required behaviour |
|---|---|
| `POST /work-items` | Accept title and optional description/priority; return 201 and the stored request. |
| `GET /work-items` | Return a JSON array; optional `status` and `priority` filters. Combined filters use AND. |
| `PATCH /work-items/{id}` | Update exactly the `status` field; return 200 and the updated request. |

| Field | Rule |
|---|---|
| `title` | String, trimmed, 1–100 characters after trimming. |
| `description` | Optional string, at most 1,000 characters; omitted means empty string. |
| `priority` | `low`, `normal`, `high`; default `normal`. |
| `status` | `open`, `in_progress`, `done`; creation always uses `open`. POST cannot set a different status. |
| Transitions | `open → in_progress → done`; repeating the same state is allowed and does not change it. Backward transitions and `open → done` are invalid. |

Invalid inputs, unknown filter values and invalid transitions return **422** without changing state. PATCH of an unknown ID returns **404**. Database unavailability returns **503**, without credentials, SQL or raw exception details. POST allows only `title`, `description`, `priority`; PATCH allows only `status`. Unknown JSON fields return 422. Error wording may vary within this contract. Sorting and DELETE are not additional customer requirements today.

The API paths are fixed for comparability. Existing additional endpoints may remain. Existing data must survive a documented migration: missing priority becomes `normal`, previous `done=true` becomes `done`, and other previous states use a documented mapping. Do not delete submitted/existing data or use `docker compose down -v` as a migration procedure.

## Acceptance criteria

| ID | Verifiable acceptance |
|---|---|
| AC-01 | Valid POST returns 201, a new ID, trimmed title, priority and status `open`. Defaults follow the contract. |
| AC-02 | After closing/reopening a database connection or restarting the API process, the same request remains readable. Use actual PostgreSQL. |
| AC-03 | Unfiltered GET returns stored requests. Individual and combined filters return only matching entries. |
| AC-04 | Status follows the allowed transitions and persists across new DB connections. Repeating the same state returns 200. |
| AC-05 | Empty/blank/oversized title, oversized description, invalid values/filters/transitions and unknown JSON fields return 422. |
| AC-06 | PATCH of a missing ID returns 404. |
| AC-07 | Simulated DB unavailability returns 503 and a generic error. A separate actual DB test proves AC-02; simulation does not replace it. |
| AC-08 | An agent handover uses a previously produced artifact substantively. A human reviews the result and records explicit acceptance tied to an unambiguous source version. |

Example requests: “Check projector in room A” (`high`), “Create a test account for the lab” (`normal`), “Update documentation link” (`low`). Demonstrate at least three requests, filtering and status transitions.

## Boundaries

The required stack and course rates remain unchanged: Python, FastAPI/Pydantic, PostgreSQL, LangGraph/LangChain, pytest, Docker and GitHub; LLM via local Ollama or HAW ICC. No external cloud LLM tokens or transmission of customer data. Extra frameworks require prior agreement. Authentication, UI, email integration, RAG, full-text search and deployment are outside today's acceptance scope.

Ask the instructor business questions in the opening phase. Record binding answers in `docs/customer-01/clarifications.md`. Changes to the API contract require a documented customer decision communicated to all teams. Your team decides implementation details.
