# MFG Copilot

Monorepo scaffold for a multi-agent aggregation and management platform.

This layout follows a pragmatic community-style split:
- `apps/` for user-facing React applications
- `services/` for FastAPI-based platform and agent services
- `packages/` for shared Python and TypeScript libraries
- `infra/` for Docker and Kubernetes delivery assets
- `observability/` for Prometheus, LangSmith, and Elasticsearch integrations
- `harness/` for Harness Engineering scenarios, evals, and repeatable system checks
- `docs/architecture/` for architecture source docs and diagrams

Start reading here:
- [Architecture Index](./docs/architecture/README.md)
- [Project Layout](./docs/architecture/project-layout.md)
- [System Architecture Source](./docs/architecture/system-architecture.md)
- [System Architecture Diagram](./docs/architecture/diagrams/system-architecture.svg)
