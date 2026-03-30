# Testing And Evals Strategy

This repository should use a layered testing strategy instead of one framework for everything.

## Recommended stack

### Frontend UI and browser E2E

- Primary: Playwright

Why:
- strong browser automation and isolation
- built-in traces, screenshots, retries, and parallelization
- can combine browser actions with API setup and verification in the same test run

Use it for:
- login, approval inbox, task execution, and audit-visible user flows
- full-stack browser E2E against deployed or preview environments
- smoke coverage for production-like paths

### Backend unit and API tests

- Primary: `pytest`
- API client layer: FastAPI `TestClient` for straightforward sync tests
- Async API and service tests: `httpx.AsyncClient` with `ASGITransport`

Why:
- FastAPI officially supports `pytest` with `TestClient`
- `httpx` provides direct ASGI calling for async service tests
- `pytest` fits Python service code, fixtures, parametrization, and CI workflows naturally

Use it for:
- unit tests for domain logic
- service tests for FastAPI routes
- orchestrator state machine tests
- adapter tests with stubs and fixtures

### Backend integration tests

- Primary: `pytest` + `testcontainers-python`

Why:
- integration tests should exercise real PostgreSQL, MySQL-compatible dependencies, and Elasticsearch-like services where practical
- Testcontainers keeps those environments reproducible in CI without hand-maintained shared test infrastructure

Use it for:
- database migrations
- repository / persistence tests
- service integration against real backing services

### API contract and fuzz testing

- Primary: Schemathesis

Why:
- it generates tests from OpenAPI automatically
- it catches status-code, schema, and edge-case failures that hand-written tests usually miss

Use it for:
- contract validation of FastAPI OpenAPI specs
- regression checks for externally exposed APIs
- stateful API workflow testing where OpenAPI links are defined

### End-to-end workflow tests

Use two layers, not one:

- Playwright for user-visible E2E
- `pytest` workflow tests for non-UI service-to-service scenarios

Examples:
- Playwright: approver opens inbox, reviews deployment plan, approves execution
- `pytest` E2E: router -> orchestrator -> rag-service -> toolhub flow without browser overhead

This split keeps browser E2E focused and fast enough, while still giving deep workflow coverage.

### Tests versus Harness

Keep `tests/` and `harness/` separate on purpose.

- `tests/` is for service and application correctness
- `harness/` is for agent behavior replay, evaluation, and regression over realistic datasets

Use `tests/` for:
- unit, integration, contract, browser E2E, and load testing
- validating code behavior, route behavior, persistence behavior, and API contracts

Use `harness/` for:
- DeepEval or similar agent evaluations
- golden dataset replay
- prompt, retrieval, planning, and agent-trajectory regression checks
- benchmark-style comparisons across model routing or agent strategies

Practical rule:
- if the test is asserting software behavior of a service, it belongs in `tests/`
- if the test is judging quality or regression of agent behavior over scenarios or datasets, it belongs in `harness/`

### Load testing

- Primary: `k6`

Why:
- strong fit for API, workflow, and adapter concurrency testing
- simple scripting model for CI and containerized execution
- good match for load risks around `toolhub`, approval APIs, and orchestrator fan-out paths

Use it for:
- `tests/load/`
- FastAPI endpoint throughput and latency baselines
- toolhub adapter concurrency checks for MES / SFC style integrations
- pre-release performance smoke tests in shared environments

## Agent eval recommendation

### Recommended default

- Primary eval framework: DeepEval
- Keep LangSmith as the tracing / observability system already reflected in this repo
- Use OpenEvals selectively for targeted LLM-as-judge or trajectory-style evaluations when it provides a better fit
- Do not add Langfuse as a second primary observability system unless the team explicitly decides to replace LangSmith

### Why DeepEval as the primary eval runner

- strong fit for code-first CI and Harness Engineering
- native pytest-oriented workflow
- supports LLM-as-judge and multi-turn evaluation patterns
- works well as an offline regression gate for agent behavior

Best fit in this repo:
- `harness/evals/`
- CI regression runs
- golden dataset evaluation against task classes such as retrieval QA, plan generation, and operational triage

### Why not make Langfuse the primary choice right now

Langfuse is strong, especially for integrated tracing, prompt management, and evals. But this repo already established LangSmith as the trace correlation layer.

Running both as first-class platforms too early would create:
- duplicated instrumentation
- split dashboards
- unclear source of truth for runs and feedback

If the team later decides to standardize on Langfuse instead of LangSmith, that is a reasonable architecture choice, but it should be an explicit platform decision.

### Where OpenEvals fits

OpenEvals is useful as a focused evaluator library, especially for:
- LLM-as-judge checks
- agent trajectory and multiturn evaluation
- targeted evaluator composition around specific outputs

Use it when:
- a team needs a narrow evaluator quickly
- a task needs built-in evaluator patterns not worth re-implementing
- LangGraph- or LangSmith-adjacent evaluation workflows benefit from its integrations

Do not treat it as the only evaluation system for the whole platform unless the team wants a thinner, library-first approach.

## Practical recommendation for this repo

### Testing

- Frontend and browser E2E: Playwright
- Backend unit, integration, and workflow tests: pytest
- Async API coverage: httpx AsyncClient
- Infra-backed integration: testcontainers-python
- API contract and fuzz: Schemathesis
- Load testing: k6

### Agent evaluation

- Primary: DeepEval
- Optional targeted helper: OpenEvals
- Observability and run correlation: LangSmith
- Not recommended right now: adding Langfuse in parallel with LangSmith as another primary platform
