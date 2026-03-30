# API Gateway

This service owns the user-facing FastAPI boundary.

Early Phase 1 expectation:
- reserve approval-facing request and response contracts now
- expose approval inbox and decision surfaces against shared schemas
- avoid inventing approval payloads independently in frontend and backend

Primary contracts should align with:
- `packages/py/shared-schemas/approval-envelope.schema.yaml`

