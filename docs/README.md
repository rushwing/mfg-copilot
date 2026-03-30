# Docs Home

This directory is the documentation entry point for the repo.

The rule is simple: start with the smallest useful doc first, then drill down only when needed.

## Read In This Order

1. [Architecture Overview](./architecture/overview.md) for the 2-minute system picture.
2. [Tasks Home](../tasks/README.md) for active phases and feature-story scope.
3. [Architecture Index](./architecture/README.md) for implementation and design deep dives.
4. [ADR Index](./adr/README.md) for durable architectural decisions.

## Directory Map

- `architecture/` for overview, layouts, patterns, and detailed design
- `adr/` for accepted or proposed architecture decisions
- `runbooks/` for operator-facing procedures as they are added

## Navigation Rule

- root `README.md` files should link to indexes, not to every deep document
- detailed docs should assume the reader intentionally navigated there
- requirement content belongs in `tasks/`, not duplicated across architecture docs
