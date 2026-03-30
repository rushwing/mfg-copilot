# MySQL Migrations

This repository does not manage upstream enterprise MySQL schema as a platform-owned migration stream.

Allowed contents here:
- schema snapshots for reference
- fixture-oriented extracts for local development
- documentation about upstream table expectations

Not allowed:
- platform feature migrations
- dual-write migration logic

Use `data/sync/` for one-way sync or mirroring assets when needed.

