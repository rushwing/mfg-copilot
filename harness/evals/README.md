# Agent Evals

Recommended primary framework:
- DeepEval

Recommended supporting tools:
- LangSmith for trace correlation and experiment visibility
- OpenEvals for targeted evaluator composition where useful

Current selection guidance:
- use DeepEval as the default CI-facing regression framework
- keep evaluator datasets and golden cases here
- keep run linkage with `langsmith_run_id` and `harness_run_id`
- avoid introducing Langfuse as a second primary observability platform unless the team explicitly replaces LangSmith

