# LangSmith

LangSmith integration should be wired early, not after workflows are already in production.

Minimum trace correlation contract:
- `task_id`
- `workflow_id`
- `agent_id`
- `plan_id`
- `approval_id`
- `langsmith_run_id`
- `harness_run_id`

Rule:
- every harness execution should either create or attach a `langsmith_run_id`
- reports in `harness/reports/` should retain the matching `harness_run_id` and `langsmith_run_id`

This keeps replay, debugging, and regression analysis joinable across harness outputs and agent traces.

