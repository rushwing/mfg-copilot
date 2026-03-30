# PostgreSQL Migrations

This directory contains platform-owned migrations only.

Subdirectories:
- `platform/`: users, sessions, approvals, audit, RBAC
- `agents/`: task ledger, checkpoints, execution state
- `rag/`: platform-owned retrieval metadata, KB release metadata

Rule:
- every real migration managed by this repository belongs under one of these PostgreSQL subdirectories

