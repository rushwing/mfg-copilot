# Tests

Repository-level tests live here.

- `unit/`: pure unit tests
- `integration/`: service and database integration tests
- `contract/`: API and gRPC compatibility tests
- `e2e/`: user-flow and workflow tests
- `load/`: throughput and concurrency tests

Recommended tooling:
- `pytest` for backend unit, integration, and workflow tests
- Playwright for browser-facing E2E
- Schemathesis for OpenAPI contract and fuzz testing
- `testcontainers-python` for infra-backed integration tests
- `k6` for load and concurrency testing

Practical split:
- `tests/e2e/` should include browser E2E driven by Playwright
- non-UI service-to-service workflows should stay in pytest-based integration or workflow suites
- `tests/load/` should hold k6 scenarios for API, orchestrator, and toolhub concurrency checks
