# Daily module refresh log

Tracks a recurring automated job (a Routine, fired daily at 9am IST /
03:30 UTC) that picks one module per day — the one with the oldest
`last_refreshed` date, `never` outranking any date — stress-tests its
content against current industry news, fixes anything genuinely outdated,
and ships the result as a merged PR. Conservative scope only: it corrects
outdated facts, numbers, tool/model names, and recommendations; it does
not add new lessons, restructure, or rewrite sections that are still
accurate. Every run advances the table below, whether or not it found
something to fix, so the rotation always moves forward.

| id | path | build script | last_refreshed |
|---|---|---|---|
| ai-engineering | content/ | scripts/build_html.py | never |
| harness-engineering | harness-engineering/ | scripts/build_site.py | never |
| flowable | flowable/ | scripts/build_site.py | never |
| first-principles | first-principles/ | scripts/build_first_principles.py | never |
| product-sense | product-sense/ | scripts/build_product_sense.py | never |
| technical-product-sense | technical-product-sense/ | scripts/build_technical_product_sense.py | never |
| technical-product-management | technical-product-management/ | scripts/build_technical_product_management.py | never |
| agentic-ai | agentic-ai/ | scripts/build_agentic_ai.py | never |
| knowledge-graphs | knowledge-graphs/ | scripts/build_knowledge_graphs.py | never |
| generative-ai | generative-ai/ | scripts/build_generative_ai.py | never |
| llms | llms/ | scripts/build_llms.py | never |
| api-integrations | api-integrations/ | scripts/build_api_integrations.py | never |
| rag-vector-databases | rag-vector-databases/ | scripts/build_rag_vector_databases.py | never |
| memory-and-context | memory-and-context/ | scripts/build_memory_and_context.py | never |
| tool-calling | tool-calling/ | scripts/build_tool_calling.py | never |
| ai-agents | ai-agents/ | scripts/build_ai_agents.py | never |
| agentic-workflows | agentic-workflows/ | scripts/build_agentic_workflows.py | never |
| evaluation-and-observability | evaluation-and-observability/ | scripts/build_evaluation_and_observability.py | never |
| ai-security-and-guardrails | ai-security-and-guardrails/ | scripts/build_ai_security_and_guardrails.py | never |
| cost-optimization | cost-optimization/ | scripts/build_cost_optimization.py | never |
| system-design | system-design/ | scripts/build_system_design.py | never |

## Run history

(The daily job appends one line per run below, oldest first: date, module,
outcome — "fixed: <short description>" or "verified, no changes needed" —
and a link to the merged PR.)
