# ADR 0002: PostgreSQL Platform Ownership with MySQL Enterprise Integration

## Status

Accepted

## Context

The platform needs a durable operational store for users, approvals, audit, orchestration state, and agent metadata. At the same time, enterprise or factory systems may already use MySQL and remain outside this repository's ownership.

Running the platform as a long-term dual-write system across PostgreSQL and MySQL would increase:
- migration complexity
- operational risk
- consistency bugs
- ownership ambiguity

## Decision

Use PostgreSQL as the platform system-of-record.

Treat external MySQL systems as upstream enterprise sources, not as peer write targets for platform features.

### PostgreSQL owns

- users and sessions
- approvals and audit trail
- task ledger and orchestration checkpoints
- agent metadata and platform configuration
- RAG metadata that belongs to the platform

### MySQL owns

- enterprise or factory source data managed by upstream systems
- schemas that this repository does not control

### Integration rule

- platform services never dual-write business state to PostgreSQL and MySQL
- access to enterprise MySQL data is isolated behind `services/toolhub/`
- if mirrored access is required, prefer one-way sync into PostgreSQL or Elasticsearch over direct platform ownership of MySQL schema

## Migration convention

- `data/migrations/postgresql/` contains real platform migrations
- `data/migrations/mysql/` does not contain platform-managed migrations
- `data/migrations/mysql/` may contain snapshots or documentation only
- enterprise sync assets live under `data/sync/`

## Consequences

Benefits:
- one primary transactional platform database
- cleaner ownership of schema changes
- easier approvals, audit, and task-state modeling
- enterprise integration remains replaceable behind adapters

Costs:
- mirrored enterprise data needs sync or adapter infrastructure
- some upstream query needs may require staged replication before performance is acceptable

## Follow-up

- define adapter contracts in `services/toolhub/`
- add sync docs or configs under `data/sync/` when enterprise mirroring begins
- keep agent code unaware of whether enterprise data originated in MySQL, PostgreSQL mirror tables, or search indexes

