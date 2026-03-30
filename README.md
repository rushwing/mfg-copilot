# MFG Copilot

Multi-agent aggregation and management platform for manufacturing workflows.

This repo now follows a strict progressive-disclosure model inspired by `deer-flow`:
- root docs stay short and orienting
- directory `README.md` files act as navigation hubs
- deep design only appears one layer down, when a reader actually needs it

## Start Here

- New to the repo: [Docs Home](./docs/README.md)
- Need the fastest architecture brief: [Architecture Overview](./docs/architecture/overview.md)
- Need implementation scope and backlog shape: [Tasks Home](./tasks/README.md)

## Repo Shape

- `apps/` for user-facing React applications
- `services/` for FastAPI-based platform and agent services
- `packages/` for shared Python and TypeScript libraries
- `infra/` for Docker and Kubernetes assets
- `observability/` for Prometheus, LangSmith, and Elasticsearch integrations
- `harness/` for evals, standards, and repeatable system checks
- `docs/` for architecture, ADRs, and operating guidance
- `tasks/` for repo-native phase and feature requirements
