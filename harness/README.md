# Harness

Harness Engineering assets live here.

- `scenarios/`: end-to-end business workflows
- `evals/`: correctness and regression evaluation suites
- `datasets/`: replayable input datasets
- `fixtures/`: stubbed dependencies
- `runners/`: harness execution entry points
- `reports/`: benchmark and eval outputs

Traceability rule:
- each harness execution should emit or attach a `harness_run_id`
- if LangSmith tracing is enabled, keep the matching `langsmith_run_id` with the harness report so replay and debugging can be joined later

PR review packet gate rule:
- packet gating examples and trace-linked gate decisions should remain reproducible from harness-visible artifacts, not only PR comments

PR review skill rule:
- `skills/review-pr/` is for explicit human-review mode only
- default LLM PR review should not automatically invoke that skill unless the user explicitly asks for human review or names `review-pr`
