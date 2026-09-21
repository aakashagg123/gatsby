# Daily module refresh log

Tracks a recurring automated job (a Routine, fired daily at 9am IST /
03:30 UTC) that picks one module per day — the one with the oldest
`last_refreshed` date, `never` outranking any date — and grounds it in
real, current, expert-level knowledge on two axes: **accuracy** (every
checkable claim, not a sampled subset, is still true) and
**comprehensiveness** (the module covers what a current expert
practitioner would expect for this topic, at this depth, today — a
missing framework or superseded technique is as real a defect as a wrong
fact). Every run reads the full module before researching, not a grep
sweep. Scope stays conservative on structure — it corrects and fills
within existing lessons; it does not add new lessons or restructure a
module, flagging anything that large instead. Every run advances the
table below, whether or not it found something to fix, so the rotation
always moves forward.

| id | path | build script | last_refreshed |
|---|---|---|---|
| ai-engineering | content/ | scripts/build_html.py | 2026-09-20 |
| harness-engineering | harness-engineering/ | scripts/build_site.py | 2026-09-20 |
| flowable | flowable/ | scripts/build_site.py | 2026-09-20 |
| first-principles | first-principles/ | scripts/build_first_principles.py | 2026-09-21 |
| product-sense | product-sense/ | scripts/build_product_sense.py | 2026-09-21 |
| technical-product-sense | technical-product-sense/ | scripts/build_technical_product_sense.py | 2026-09-21 |
| technical-product-management | technical-product-management/ | scripts/build_technical_product_management.py | 2026-09-21 |
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
- 2026-09-21 — first-principles — fixed: one substantive-content issue found
  after checking 4 load-bearing claims. `traps-and-limits.md`'s
  Dunning-Kruger bullet stated the effect as settled fact ("the less you
  know... the more confident you feel"), but a real, ongoing academic
  dispute (Gignac & Zajenkowski 2020; Blair Fix's 2022 autocorrelation
  critique; continuing through 2024-2025 replication work) argues the
  original effect is substantially a statistical artifact of noisy
  self-assessment rather than a distinct cognitive bias. Reframed the
  bullet as "Overconfidence from thin knowledge (popularly Dunning-Kruger)"
  with an honest note on the dispute, keeping the practical teaching point
  intact — the underlying caution (a little knowledge is dangerous for
  first-principles thinking) holds regardless of the statistical mechanism.
  Left unchanged after verification: the SpaceX "~2% of price is raw
  materials" figure (`what-is-first-principles.md`, `recap.md`) — widely
  and consistently corroborated; the "10,000 hours" correction
  (`recap.md`) — already correctly hedges toward Ericsson's actual
  "deliberate practice, not raw hours" finding, consistent with current
  scholarship; Charlie Munger's "80-90 important models" quote
  (`mental-models-latticework.md`) — verified as an accurate quotation.
  Sources checked (8): Blair Fix's "The Dunning-Kruger effect is
  autocorrelation" (myhub.ai/items/the-dunning-kruger-effect-is-autocorrelation-economics-from-the-top-down);
  Gignac & Zajenkowski (2020), "The Dunning-Kruger effect is (mostly) a
  statistical artefact" (researchgate.net/publication/340361120); a 2024
  discussion of the ongoing statistical debate
  (benjamintseng.com/2024/03/nope-the-dunning-kruger-effect-is-just-bad-statistics);
  a philosophy-of-science discussion of the dispute, including Kruger's own
  2002 rebuttal (dailynous.com/2022/04/25/dunning-kruger-discussion); a
  breakdown of Musk's SpaceX raw-material-cost analysis
  (medium.com/@ahmet_celebi's "Elon Musk's First Principles in the
  Factory"); a sourced list of Charlie Munger's mental models confirming
  the "80 or 90" quote (sourcesofinsight.com/charlie-munger-mental-models);
  Scott Young's 2024 "The 10,000-Hour Rule Is a Myth"
  (scotthyoung.com/blog/2024/01/23/10000-hr-rule-myth); and a retrospective
  on Ericsson's own objections to the popularized rule
  (davidepstein.com/father-of-the-10000-hours-rule-passes-away).
- 2026-09-21 — product-sense — fixed: `product-sense-for-ai.md`'s "patterns
  users now expect" section named ChatGPT's "Pulse" morning-digest feature
  as a live example of proactive AI — OpenAI sunset Pulse on June 17, 2026,
  folding the capability into general-purpose "scheduled tasks." Updated
  the parenthetical to note the rename/sunset explicitly, keeping the
  underlying teaching point (proactive AI needs consent and restraint)
  intact, since the pattern itself didn't go away, only the branded
  feature name did. Left unchanged after verification: the broader "2025
  reset [user reference points]" framing and its four named patterns
  (deep-research modes, proactive AI, persistent memory, visible
  thinking) — all four are still the current standard as of 2026, per
  live research, and "2025" is correctly used as a historical origin
  point, not a "current state" claim; the Air Canada chatbot
  refund-policy incident (`recap.md`) — verified accurate down to the
  ruling date (Feb 14, 2024) and refund amount (CAD $650.88); the PM
  Handbook interview attributions naming PMs' employers as "Google,
  Twitter, Facebook, Yammer" (`recap.md`) — correctly reflects where
  those interviewees worked *at the time*, not a claim about current
  company names (Twitter/X, Facebook/Meta) that needs updating; and
  `communication.md`'s "60% of 200 surveyed users" figure — a labeled
  illustrative example, not a live statistic. Sources checked (7): OpenAI
  ChatGPT Pulse launch coverage (techcrunch.com/2025/09/25/openai-launches-chatgpt-pulse-to-proactively-write-you-morning-briefs);
  a 2026 report on Pulse's sunset into scheduled tasks
  (justinmckelvey.com/blog/chatgpt-pulse); a 2026 AI-agent-memory research
  survey (mem0.ai/blog/state-of-ai-agent-memory-2026); a roundup of 2026
  personal-AI-assistant memory products (vellum.ai/blog/best-personal-ai-assistants-with-memory);
  a 2026 UX design-trends report confirming transparency/multimodal as
  *additional* trends, not a replacement for the four named patterns
  (designlab.com/blog/ai-in-ux-product-design-trends-2026); the American
  Bar Association's analysis of the Air Canada tribunal ruling
  (americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot);
  and The Hill's report confirming the CAD $650.88 refund figure
  (thehill.com/business/4476307-air-canada-must-pay-refund-promised-by-ai-chatbot-tribunal-rules).
- 2026-09-21 — technical-product-sense — expanded: first run under the
  strengthened accuracy-and-comprehensiveness standard. Read all 9 lessons
  plus README and recap in full (not a grep sweep) before researching.
  Found and closed 3 genuine comprehensiveness gaps, all source-confirmed
  before writing: (1) `apis-and-contracts.md` covered only REST-shaped
  contracts, with no mention of GraphQL or gRPC despite hybrid
  REST+GraphQL+gRPC architectures being the confirmed 2026 enterprise
  norm — added a "REST isn't the only shape" section. (2)
  `security-and-privacy.md` listed HIPAA/PCI/GDPR as the regulated
  categories to know but never mentioned the EU AI Act, despite this
  being an AI-PM-focused curriculum and the Act reaching active
  enforcement in August 2026 — added a bullet with the current
  enforcement timeline and cross-linked to `ai-security-and-guardrails`'s
  deeper treatment. (3) `data-and-the-data-model.md` never mentioned
  eventual consistency or the CAP theorem, even though the site's own
  `eventual-consistency` glossary entry already claimed this lesson as
  its `see` link — a real, pre-existing broken promise to readers, not a
  hypothetical gap. Added a "Consistency is a spectrum, not a given"
  section, a failure mode, a checklist item, and a cross-link to
  `system-design/core-building-blocks.md`'s deeper mechanics, closing the
  glossary's dangling reference. Accuracy pass: verified the "nines"
  downtime math (8.7 hrs/yr at 99.9%, 52 min/yr at 99.99%) by
  calculation; the Air Canada chatbot incident in `recap.md` reuses
  facts already verified with primary sources in the 2026-09-21
  product-sense run (Feb 14, 2024 ruling, CAD $650.88); Redis and
  HIPAA/PCI/GDPR/DPDP references are generic, still-current regime/tool
  names, not specific claims needing a source. **Flagged, not fixed**
  (out of this module's scope): `ai-security-and-guardrails/governance-audit-and-compliance.md`
  states EU AI Act obligations "phasing in through 2026-27," which is
  now imprecise — the July 2026 Digital Omnibus (Regulation (EU)
  2026/1744) pushed the high-risk tier to Dec 2027 (stand-alone systems)
  and Aug 2028 (embedded systems). Recommend fixing this the next time
  `ai-security-and-guardrails` comes up in rotation. Sources checked
  (9): a 2026 API-architecture adoption report confirming REST's ~83%
  share and gRPC/GraphQL's specialized enterprise roles
  (askantech.com/graphql-vs-rest-vs-grpc-api-architecture-microservices-2026);
  a second 2026 API-pattern comparison confirming the hybrid-architecture
  norm (apiscout.dev/guides/rest-vs-graphql-vs-grpc-vs-trpc-2026); the
  European Commission's official AI Act policy page
  (digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai); a
  2026 EU AI Act compliance guide confirming the August 2026 enforcement
  date and GPAI fine powers (secureprivacy.ai/blog/eu-ai-act-2026-compliance);
  a second 2026 guide confirming the Digital Omnibus's revised high-risk
  timeline (decodethefuture.org/en/eu-ai-act-explained); IBM's CAP
  theorem explainer confirming continued relevance and the
  availability/consistency tradeoff (ibm.com/think/topics/cap-theorem); a
  distributed-systems consistency-tradeoffs writeup covering the PACELC
  extension (hazelcast.com/blog/navigating-consistency-in-distributed-systems-choosing-the-right-trade-offs);
  Google's SRE book chapter on distributed consensus and CAP
  (sre.google/sre-book/managing-critical-state); and this repo's own
  `system-design/core-building-blocks.md` and
  `ai-security-and-guardrails/governance-audit-and-compliance.md`,
  cross-checked to confirm no duplication and to source the flagged
  finding above.
- 2026-09-21 — technical-product-management — fixed: 2 accuracy corrections
  and 3 comprehensiveness fills, all within existing lessons. Read all 9
  lessons plus README and recap in full before researching. (1) Accuracy:
  `recap.md`'s Knight Capital war story claimed the ~$440M loss was "more
  than its market cap" — Knight's pre-incident market cap was ~$681M, so
  the loss was roughly two-thirds, not more; corrected. (2) Accuracy:
  `prioritization-and-roadmaps.md`'s Kano description listed only 3 of
  the original model's 5 categories — added the missing "indifferent" and
  "reverse" categories. (3) Comprehensiveness: `working-with-engineering.md`
  never mentioned velocity or throughput — core agile execution vocabulary
  a PM needs; added a section explaining both, the difference between
  them, and why they're diagnostic not motivational. (4) Comprehensiveness:
  `metrics-and-experimentation.md` didn't distinguish data-informed from
  data-driven decision-making — a standard PM concept; added the
  distinction with guidance on when to use each mode. (5) Comprehensiveness:
  `launches-rollouts-and-migrations.md`'s feature-flag cleanup bullet was
  thin on governance; expanded with flag lifecycle management (cleanup
  dates, inventory tracking, audits). Left unchanged after verification:
  RICE formula (confirmed as Intercom's standard formulation), WSJF
  (confirmed as Reinertsen/SAFe's cost-of-delay/duration), Cagan's four
  risks (confirmed accurate to SVPG/Inspired), "vibe coding" coinage
  (confirmed Karpathy Feb 2 2025, Collins word of the year 2025), and 5
  Whys attribution. Sources checked (6): SEC Knight Capital enforcement
  action and 10-K filing (~$461M pre-tax loss, market cap ~$681M);
  Forbes's Knight Capital reporting; Kano's original model documentation
  (5 categories: must-be, one-dimensional, attractive, indifferent,
  reverse); Intercom's RICE framework documentation; Reinertsen's
  "Principles of Product Development Flow" WSJF formulation; SAFe's
  official WSJF guidance.
