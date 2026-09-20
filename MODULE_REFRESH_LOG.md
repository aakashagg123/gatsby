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
| ai-engineering | content/ | scripts/build_html.py | 2026-09-20 |
| harness-engineering | harness-engineering/ | scripts/build_site.py | 2026-09-20 |
| flowable | flowable/ | scripts/build_site.py | 2026-09-20 |
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

- 2026-09-20 — ai-engineering — verified, no changes needed. Checked the
  one genuinely time-sensitive, verifiable claim in the module
  (`content/02-reliable-outputs/model-routing.md`'s description of GPT-5's
  real-time router shipping as the default architecture, August 2025)
  against a live web search — accurate as stated. No pricing figures,
  benchmark numbers, or fragile superlatives elsewhere in the module's 28
  lesson files to go stale; historical/technical references (DeepSeek-V2's
  MLA, the "DeepSeek moment," the GPT-4 drift debates) are correctly
  framed as dated history, not current-state claims.
- 2026-09-20 — harness-engineering — fixed: the course's "defaults to the
  latest model" claim was stale across 24 files (prose + runnable code
  examples). Every reference to Claude Opus 4.8 (`claude-opus-4-8`) as
  "the latest model" updated to Opus 5 (`claude-opus-5`); the two files
  framing a model-family overview ("the Claude 4.x family") updated to
  "the Claude 5 family," including Sonnet 4.6 -> Sonnet 5 and
  Fable 5 -> Fable 5.1. Haiku 4.5 references left as-is — that generation
  is still current. Scope: `phases/00-setup-and-tooling/`,
  `01-llm-io-foundations/`, `02-the-agent-loop/`, `03-tool-engineering/`,
  `04-context-engineering/`, `16-observability-and-cost/`,
  `18-production-and-deployment/`, `19-capstone-coding-agent/`.
- 2026-09-20 — flowable — fixed: two Camunda references were stale.
  (1) Camunda 7's landscape-table "tax" said only "end-of-life path," but
  Camunda 7 Community Edition is now fully EOL (no more updates since
  October 2025; Enterprise stays on LTS support to 2030) — updated in
  Phase 0's landscape lesson and its quadrant-chart label. (2) Camunda 8's
  "exporter-based history" description is outdated since the 8.8 release
  unified history into the Orchestration Cluster (no more separate,
  pluggable exporter pipeline) — updated in Phase 0's landscape lesson,
  Phase 10's competitive-landscape rematch lesson, and its
  `competitive-matrix.md` output. Left unchanged after verification:
  Flowable's `asyncLeave` "6.7+" version-floor claim (still a valid
  minimum, not a "latest version" claim), Temporal's "no business-facing
  artifact" characterization, and BPMN 2.0/DMN/CMMN spec-currency claims.
  Sources checked (8): Camunda's Feb 2025 Camunda 7 Enterprise EOL-extension
  announcement (camunda.com/blog/2025/02/camunda-7-enterprise-end-of-life-extension);
  Camunda's Nov 2025 "What's different: Orchestration Cluster in Camunda 8.8"
  post (camunda.com/blog/2025/11/whats-different-orchestration-cluster-camunda-88);
  Camunda 8.8 release notes and docs on the Orchestration Cluster
  architecture; Camunda's official product lifecycle/EOL policy page;
  Camunda 7 vs 8 migration guidance docs; Flowable's GitHub releases/changelog
  for the 6.7+ `asyncLeave` flag; Temporal's public docs on its
  code-first workflow model; the OMG BPMN 2.0.2 / DMN 1.5 / CMMN 1.1
  specification pages confirming no newer ratified major version has
  superseded them.
- 2026-09-20 — ai-engineering — re-verified under the stricter two-pass
  methodology (retroactive; the original run above used Pass A fragile-fact
  grep only). Pass B picked 3 load-bearing substantive claims and
  researched each independently, seeking disconfirming evidence: (1)
  `model-routing.md`'s GPT-5-router claim — still accurate; GPT-5's router
  architecture is documented as shipped in its August 2025 system card,
  and the claim is correctly framed as a past-tense historical fact, not
  a "current latest" claim, even though GPT-5.5/5.6 have since shipped.
  (2) `inference-stack-tradeoffs.md`'s "DeepSeek moment" open-weight-wave
  framing (R1, Qwen3, Kimi K2 "kept frontier-adjacent capability within
  reach ... ever since") — the named models are now a superseded
  generation (Kimi K3, Qwen3.8, DeepSeek V4, GLM-5.3 have since shipped),
  but the claim itself — that this wave marked open-weight models
  becoming commodity-budget-competitive — is still true and, if anything,
  more true today; left unchanged as a correctly-dated historical
  reference, not a "current SOTA" claim. (3)
  `finetune-vs-icl-vs-rag.md`'s citation of Google's *Agents* whitepaper
  "targeted learning" taxonomy (in-context learning / retrieval-based ICL
  / fine-tuning) — confirmed accurate against the whitepaper's actual
  content. No changes needed. Sources checked (8): OpenAI's GPT-5 system
  card (openai.com/index/gpt-5-system-card); Wikipedia's GPT-5.5 entry;
  a Sept 2026 GPT-5 overview (botpress.com/blog/everything-you-should-know-about-gpt-5);
  a 2026 open-weight-model comparison (wavect.io/blog/open-weight-llm-comparison-2026);
  a Kimi K2/DeepSeek-R1/Qwen3/GLM-4.5 2026 guide (turingpost.com/p/chinesemodels);
  Artificial Analysis's tracker of recent open-weight launches
  (artificialanalysis.ai/articles/recent-open-weights-model-launches);
  a summary of Google's *Agents* whitepaper (hyperbolic.ai/blog/summary-of-google-ai-white-paper-agents);
  and a second independent summary of the same whitepaper
  (medium.com/@sayantann7 — "Unpacking Google's Vision for AI Agents").
- 2026-09-20 — harness-engineering — re-verified under the stricter
  two-pass methodology beyond the model-name fix already shipped above
  (retroactive). Pass A: grepped for pricing/context-window/benchmark
  numbers beyond model ids — found only two pre-hedged "illustrative —
  verify current pricing" placeholders in the cost-accounting lesson,
  already correctly caveated. Pass B: checked whether Phase 12 (MCP &
  extensibility) teaches anything affected by MCP's real 2026-07-28 spec
  revision — the largest since the protocol launched, deprecating Roots,
  Sampling, Logging, and Dynamic Client Registration (DCR to CIMD).
  Confirmed none of those four deprecated capabilities are covered by the
  course's MCP lessons, which teach only the wire protocol fundamentals,
  tools/resources/prompts, servers/clients, skills, and plugins — so the
  deprecations don't affect this module's content. Also checked Phase 8's
  permission-modes lesson and Phase 11's plan-mode lesson against current
  product behavior descriptions — both are from-scratch conceptual
  implementations (not claims about a specific product's current UI), so
  nothing to update. No further changes needed. Sources checked (6): the
  MCP spec blog's 2026-07-28 release announcement
  (blog.modelcontextprotocol.io/posts/2026-07-28); the MCP 2026 roadmap
  post (blog.modelcontextprotocol.io/posts/2026-mcp-roadmap); Wikipedia's
  Model Context Protocol entry; a 2026 MCP adoption/update report
  (tech-insider.org/ie/model-context-protocol-mcp-update-2026); an MCP
  spec version-timeline reference (hidekazu-konishi.com/entry/mcp_specification_version_timeline);
  and a Claude Code features/settings reference for 2026
  (hidekazu-konishi.com/entry/claude_code_features_settings_reference_2026).
