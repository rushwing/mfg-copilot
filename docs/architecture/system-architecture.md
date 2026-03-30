+--------------------------------------------------------------------------------------+
|                               NVIDIA MFG COPILOT                                     |
|                          Product Scope / High-Level Architecture                     |
+--------------------------------------------------------------------------------------+

Users
  |
  |  Web / Chat / API
  v
+--------------------------------------------------------------------------------------+
|                                Unified Portal / API Gateway                          |
|--------------------------------------------------------------------------------------|
| SSO / Login | Role Resolver | Session Context | Audit Trail | Approval Inbox         |
+--------------------------------------------------------------------------------------+
  |
  | user role + intent + phase + checkpoint + station + site
  v
+--------------------------------------------------------------------------------------+
|                                   Agent Router                                       |
|--------------------------------------------------------------------------------------|
| Routing Policy                                                                        |
| - Role-based routing                                                                  |
| - Intent classification                                                               |
| - Phase / checkpoint awareness                                                        |
| - Safety policy (read-only / approval-needed / execute)                              |
+--------------------------------------------------------------------------------------+
  |
  +----------------------------+----------------------------+---------------------------+
                               |                            |
                               v                            v
                     +-------------------+        +-------------------+        +-------------------+
                     |   Doc Copilot     |        |  Deploy Agent     |        |   Ops Agent       |
                     |   (Phase Prep)    |        | (Station Bringup) |        | (Build / MP Ops)  |
                     +-------------------+        +-------------------+        +-------------------+
                     | - Doc Q&A         |        | - IQ/OQ workflow  |        | - Triage          |
                     | - Template fill   |        | - Deploy plan     |        | - Log analysis    |
                     | - Gap detection   |        | - MES/SFC checks  |        | - Env diagnosis   |
                     | - Summary reports |        | - SW distribution |        | - Network diag    |
                     +-------------------+        | - Approval gates  |        | - FA assist       |
                               |                  +-------------------+        | - Daily/weekly rpt|
                               |                            |                  +-------------------+
                               +-------------+--------------+---------------------------+
                                             |
                                             v
+--------------------------------------------------------------------------------------+
|                              Shared Agent Runtime Layer                              |
|--------------------------------------------------------------------------------------|
| LangGraph Orchestrator | Tool Registry | Prompt/Policy Layer | Memory | Observability|
| Retry/Timeout          | Human-in-loop | Task State Machine  | Trace  | Cost Control |
+--------------------------------------------------------------------------------------+
                                             |
                        +--------------------+---------------------+--------------------+
                        |                    |                     |                    |
                        v                    v                     v                    v
+-------------------+  +-------------------+  +--------------------------------+  +------------------+
|    RAG Layer      |  |  Model Gateway    |  |         Enterprise Tools        |  |  Data Products    |
+-------------------+  +-------------------+  +--------------------------------+  +------------------+
| KB retriever      |  | Local model route |  | MES / SFC                       |  | Project master   |
| DB retriever      |  | API LLM route     |  | Software distribution platform  |  | Product / SKU    |
| Hybrid search     |  | Policy by task    |  | CMDB / asset inventory          |  | Build records    |
| Reranker          |  | PII / export ctrl |  | Log / metrics / alerts          |  | Yield / UPH      |
| Citation builder  |  | Fallback / quota  |  | Ticketing / bug tracker         |  | Failure history  |
+-------------------+  +-------------------+  | Git / CI for bug-fix agent      |  | FA / repair data |
                        | Local: SGLang     |  +--------------------------------+  +------------------+
                        | Remote: Commercial|
                        +-------------------+

--------------------------------------------------------------------------------------------------------
Repo Boundary
--------------------------------------------------------------------------------------------------------

Repo 1: mfg-project-lifecycle-kb
  |
  +-- phase/checkpoint templates
  +-- glossary
  +-- i18n
  +-- frontmatter schema
  +-- checkpoint index
  +-- doc index
  +-- versioned KB release artifacts

Repo 2: mfg-copilot-monorepo
  |
  +-- apps/
  |    +-- portal-web
  |    +-- agent-router
  |    +-- doc-copilot
  |    +-- deploy-agent
  |    +-- ops-agent
  |
  +-- packages/
       +-- agent-core
       +-- rag-core
       +-- kb-client
       +-- model-gateway
       +-- auth-rbac
       +-- approval-engine
       +-- tool-mes
       +-- tool-distribution
       +-- tool-observability
       +-- shared-schemas

--------------------------------------------------------------------------------------------------------
Primary Flows
--------------------------------------------------------------------------------------------------------

1. Document Copilot Flow
   User -> Portal -> Router -> Doc Copilot
        -> KB Retriever + Project/Product DB
        -> Structured generation
        -> Validation against template schema / required sections
        -> Output document / summary / checklist draft

2. Deployment Agent Flow
   User -> Portal -> Router -> Deploy Agent
        -> Read site/station context
        -> Generate deployment plan
        -> Approval gate
        -> Execute tools via MES / distribution platform
        -> Collect results
        -> Produce IQ/OQ evidence + audit log

3. Ops Agent Flow
   User / alert -> Router -> Ops Agent
                -> Gather logs / metrics / build data / known issues
                -> Multi-agent triage
                -> Suggest fix or escalate
                -> Optional bug-fix branch via commercial LLM
                -> Summary / RCA / FA input

--------------------------------------------------------------------------------------------------------
Recommended Scope by Phase
--------------------------------------------------------------------------------------------------------

Phase 1
  - Portal + Router
  - Doc Copilot
  - KB integration
  - Project DB integration
  - Daily/weekly/monthly summaries

Phase 2
  - Deploy Agent
  - Approval workflow
  - MES / SFC / software distribution adapters

Phase 3
  - Ops Agent team
  - Triage + diagnostics + FA + bug-fix workflow
  - Stronger observability and guardrails

