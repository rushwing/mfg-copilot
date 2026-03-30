# Model Routing

This directory owns versioned routing rules from task type to model profile.

Early rule:
- all task-to-model routing must be declared here before it is hardcoded in services

Why this exists:
- rollout gets messy quickly when each agent service picks models ad hoc
- approval-heavy, retrieval-heavy, and coding-heavy tasks often need different model profiles
- SGLang and remote commercial models should be selected by policy, not by scattered conditionals

Recommended flow:
1. define task classes in the schema file
2. map each class to a model profile
3. let services consume the resolved policy instead of embedding vendor-specific decisions

See `task-routing.schema.yaml`.

