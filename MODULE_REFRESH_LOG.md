# Daily module refresh log

Tracks a recurring automated job (a Routine, fired daily at 9am IST /
03:30 UTC) that picks one module per day — the most overdue module in the
highest-priority tier (see `tier` and `cadence_days` below) — and grounds it in
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

`tier` ranks priority for the AI-PM curriculum (1 is picked first): tier 1 is PM craft and
AI foundations, tier 2 is core agent and infrastructure topics, tier 3 is engineer build tracks
and stable fundamentals. `cadence_days` is how many days may pass before a module is due
again. A module is due when `last_refreshed` is `never` or older than its cadence. The job
picks the lowest tier number among due modules.

| id | path | build script | tier | cadence_days | last_refreshed |
|---|---|---|---|---|---|
| technical-product-management | technical-product-management/ | scripts/build_technical_product_management.py | 1 | 45 | 2026-09-21 |
| technical-product-sense | technical-product-sense/ | scripts/build_technical_product_sense.py | 1 | 45 | 2026-09-21 |
| product-sense | product-sense/ | scripts/build_product_sense.py | 1 | 45 | 2026-09-21 |
| business-acumen | business-acumen/ | scripts/build_business_acumen.py | 1 | 45 | 2026-10-16 |
| ai-assisted-development | ai-assisted-development/ | scripts/build_ai_assisted_development.py | 1 | 45 | 2026-10-17 |
| fine-tuning | fine-tuning/ | scripts/build_fine_tuning.py | 1 | 45 | 2026-10-17 |
| transformers | transformers/ | scripts/build_transformers.py | 1 | 45 | 2026-10-17 |
| knowledge-graphs | knowledge-graphs/ | scripts/build_knowledge_graphs.py | 1 | 45 | 2026-10-24 |
| ai-engineering | content/ | scripts/build_html.py | 1 | 45 | 2026-09-20 |
| agentic-ai | agentic-ai/ | scripts/build_agentic_ai.py | 2 | 30 | 2026-10-23 |
| generative-ai | generative-ai/ | scripts/build_generative_ai.py | 2 | 30 | never |
| llms | llms/ | scripts/build_llms.py | 2 | 30 | 2026-10-25 |
| api-integrations | api-integrations/ | scripts/build_api_integrations.py | 2 | 30 | never |
| rag-vector-databases | rag-vector-databases/ | scripts/build_rag_vector_databases.py | 2 | 30 | 2026-10-12 |
| memory-and-context | memory-and-context/ | scripts/build_memory_and_context.py | 2 | 30 | never |
| tool-calling | tool-calling/ | scripts/build_tool_calling.py | 2 | 30 | never |
| ai-agents | ai-agents/ | scripts/build_ai_agents.py | 2 | 30 | 2026-10-30 |
| agentic-workflows | agentic-workflows/ | scripts/build_agentic_workflows.py | 2 | 30 | never |
| evaluation-and-observability | evaluation-and-observability/ | scripts/build_evaluation_and_observability.py | 2 | 30 | 2026-10-26 |
| ai-security-and-guardrails | ai-security-and-guardrails/ | scripts/build_ai_security_and_guardrails.py | 2 | 30 | 2026-10-23 |
| cost-optimization | cost-optimization/ | scripts/build_cost_optimization.py | 2 | 30 | 2026-10-29 |
| prompt-engineering | prompt-engineering/ | scripts/build_prompt_engineering.py | 2 | 30 | 2026-09-22 |
| harness-engineering | harness-engineering/ | scripts/build_site.py | 3 | 90 | 2026-09-20 |
| flowable | flowable/ | scripts/build_site.py | 3 | 90 | 2026-09-20 |
| cnns | cnns/ | scripts/build_cnns.py | 3 | 90 | 2026-10-11 |
| system-design | system-design/ | scripts/build_system_design.py | 3 | 90 | 2026-10-19 |
| first-principles | first-principles/ | scripts/build_first_principles.py | 3 | 90 | 2026-09-21 |

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

- 2026-10-14 — business-acumen — new track shipped (12 lessons, recap, and
  an interactive self-assessment). Independent blind fact-check over three
  passes. Pass 1: 1 WRONG (a SoFi bank-charter claim), 7 unsupported claims,
  13 Sources-hygiene issues. Pass 2: those cleared, web access ok, 6
  unsupported author inferences left. Pass 3: 0 WRONG / 0 STALE, inferences
  softened or re-grounded. Every company figure now cites a specific SEC
  filing document or the company's own release with an as-of date; regulatory
  claims cite law.cornell.edu, legislation.gov.uk, consumerfinance.gov,
  federalreserve.gov and uspto.gov. No book, author or person named in prose.
  check_module: avg sentence 10.8, 1% over 30 words, Flesch 67, PASS. PR #151.

- 2026-10-14 — business-acumen — expanded from 12 to 15 lessons (~66k
  words), money first. New: unit economics; business cases, capital and
  valuation; competitive advantage and strategy. Retitled: markets and
  customers; pricing and business models; products and go-to-market. The
  self-assessment grows to 60 items on 15 axes. Review stamps withdrawn from
  every lesson pending one independent fact-check before merge, so the
  last_refreshed date is unchanged. check_module: avg sentence 10.7, 0% over
  30 words, Flesch 69, WARN (no stamps).

- 2026-10-16 — business-acumen — post-merge independent fact-check of the
  15-lesson expansion: 0 WRONG / 0 STALE. Tightened six loose phrasings (US
  rate dates, Regulation B wording, a debit-cap court-challenge note, three
  quantifiers, and the reinsurance framing). Final check of the edited
  lessons: 0 WRONG / 0 STALE, web access ok. All 15 lessons stamped 2026-10
  (medium). check_module: avg sentence 10.5, 0% over 30 words, Flesch 69.

- 2026-10-23 — agentic-ai — fixed + expanded. Read all 8 lessons, README and
  recap in full. Accuracy: (1) recap's METR "19% slower" study was presented
  as current; METR's Feb/Mar 2026 follow-up estimated a speedup but called
  its own data unreliable (selection bias) — added the update. (2) Product
  lesson stated Just Walk Out's "700 human reviews per 1,000 sales vs target
  20–50" as fact; The Information's report is a 2022 figure, goal 50, and
  Amazon disputed it — reworded. (3) Protocol lesson: ACP/Instant Checkout
  was scaled back March 2026; A2A reached v1.0 March 2026; MCP moved to the
  Linux Foundation's Agentic AI Foundation Dec 2025 — updated. Coverage
  fills: Meta's Rule of Two and OWASP Agentic Top 10 (safety lesson);
  pass^k vs pass@k (reliability); Anthropic's multi-agent 90.2%/15x-token
  tradeoff (multi-agent); context rot (context lesson). Verified unchanged:
  EchoLeak CVE-2025-32711 (June 2025), Replit/SaaStr incident, Cursor "Sam"
  bot, Project Vend details, compounding-error table (recomputed
  arithmetically). Not verified: GitHub MCP exploit (May 2025) and the
  Chevy Tahoe incident were left as written, no fresh source opened.
  Flagged, not built: no new-lesson gaps; a dedicated agent-identity /
  authorization lesson could be a future recommendation.
  Sources: metr.org/blog/2026-02-24-uplift-update/;
  linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation;
  aaif.io/blog/aaifs-first-quarter-success-story-new-members-technical-wins-and-open-governance;
  opensource.googleblog.com/2026/04/a-year-of-open-collaboration-celebrating-the-anniversary-of-a2a.html;
  linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year;
  forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back;
  forkast.news (OpenAI Instant Checkout walk-back); simonwillison.net/2025/nov/2/new-prompt-injection-papers
  (Rule of Two); genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026;
  arxiv.org/pdf/2406.12045 (τ-bench pass^k); anthropic.com/engineering/multi-agent-research-system;
  trychroma.com/research/context-rot; anthropic.com/research/project-vend-1;
  thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html (EchoLeak);
  eweek.com/news/replit-ai-coding-assistant-failure; incidentdatabase.ai/cite/1039 (Cursor);
  asiae.co.kr / hrgrapevine (Just Walk Out reporting and Amazon response).

- 2026-10-23 (follow-up, same module) — agentic-ai — expanded. Added four
  items from a parallel run's notes, each re-verified first: IBM's ACP merged
  into A2A (Aug 2025), so the infographic "ACP" differs from the commerce ACP
  (research.ibm.com/projects/agent-communication-protocol); MCP tool poisoning
  and rug pulls (labs.cloudsecurityalliance.org MCP tool-poisoning whitepaper);
  Agent Skills as an open standard, Dec 2025 (agentskills.io); adaptive thinking
  and effort (platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost);
  Anthropic's five workflow patterns (anthropic.com/engineering/building-effective-agents).
  Not applied: Project Vend phase 2 (unverified). EU AI Act Digital Omnibus
  remains a flag for the ai-security-and-guardrails module.

- 2026-10-23 — ai-security-and-guardrails — tier 2 (log has no tier column);
  picked because it was `never` refreshed, had a flagged EU AI Act item, and
  is a topic a Senior PM is asked about in every security review. Outcome:
  fixed + expanded. Read all 3 lessons, README and recap in full. The flagged
  "phasing in through 2026-27" item is already resolved: the module already
  carries the Omnibus dates. Accuracy: (1) the public-challenge result said
  the system was "broken after about five days"; Anthropic's page says it held
  five days and four users passed all eight levels on days six and seven
  (339 people, ~3,700 hours, $55K) — fixed in lesson 1 and recap. Coverage:
  (2) next-generation Constitutional Classifiers (Jan 2026) added to lesson 1;
  (3) Excessive Agency rising to LLM03 in OWASP 2026 added; (4) adaptive
  attacks ("The Attacker Moves Second", 12 defenses, >90% ASR) added to the
  red-teaming lesson as text, failure mode and checklist item; (5) NIST Cyber
  AI Profile draft mentioned in lesson 3. Verified unchanged: many-shot
  (256 shots, 61%->2%), sleeper agents, Nasr 150x (abstract), OWASP 2026
  Hidden Context Exposure, NIST AI 100-2 E2025 (Mar 2025), Omnibus dates
  (24 Jul pub, 27 Jul in force, 2 Dec 2027 / 2 Aug 2028, 2 Dec 2026 marking).
  Sources opened: anthropic.com/research/constitutional-classifiers;
  anthropic.com/research/next-generation-constitutional-classifiers;
  anthropic.com/research/many-shot-jailbreaking;
  anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training;
  arxiv.org/abs/2311.17035; arxiv.org/abs/2510.09023;
  nist.gov AI 100-2e2025 page; github.com/OWASP/www-project-top-10-for-large-language-model-applications
  (2026 release, 4 Aug 2026); labs.cloudsecurityalliance.org OWASP 2026 research note.
  Search results only: Omnibus dates (White & Case, Mayer Brown, Cuatrecasas;
  EUR-Lex returned empty, White & Case 403); NIST Cyber AI Profile (KPMG);
  GDPR Art. 22 Omnibus status (no Council/Parliament position found).
  Not verified: SCHUFA judgment (curia redirect not followed), DPDP dates,
  SOC 2/ISO 42001 details, Greshake, DAN/CNBC, Art. 55 text, MITRE ATLAS
  (page empty). Flagged: main genai.owasp.org page still lists the 2025 top 10
  while the GitHub project page says the 2026 edition is current; re-check.
  No new-lesson gaps; an agent-security (OWASP Agentic Top 10 / Agent Control
  Standard) treatment lives in agentic-ai.

- 2026-10-24 — knowledge-graphs — tier 1; picked because it was `never`
  refreshed and the only DUE tier-1 row (all others within their 45-day
  cadence). Outcome: fixed + expanded. Read all 8 lessons, README and recap in
  full. Accuracy: (1) GQL given as ISO/IEC 39075 (Apr 2024) and SQL/PGQ named
  as the SQL:2023 route; (2) the unsourced "80% -> 60-70%" construction-share
  figure in the capstone replaced with an honest "no authoritative figure"
  (80% softened to a rule of thumb in README, lesson 3, recap). Coverage:
  (3) SQL/PGQ and its PostgreSQL 19 beta status added to the storage lesson,
  with the caveat that it rewrites to joins; (4) RDF 1.2 triple terms noted;
  (5) LazyGraphRAG and the RAG-vs-GraphRAG evaluation added to the LLM lesson;
  (6) text-to-query hardening (read-only user, timeouts, CVE-2026-35402);
  (7) temporal/bi-temporal agent memory (Graphiti) in the LLM and ontology
  lessons; (8) Google launch scale in lesson 1.
  Sources opened: blog.google/products/search/introducing-knowledge-graph-things-not
  (16 May 2012, 500M objects, 3.5B facts); microsoft.github.io/graphrag;
  microsoft.com/en-us/research/blog/lazygraphrag (0.1% indexing cost, vendor claim);
  arxiv.org/abs/2404.16130 (GraphRAG paper); arxiv.org/abs/2502.11371 (RAG vs GraphRAG);
  w3.org/TR/rdf12-concepts (CR snapshot 7 Apr 2026); github.com/getzep/graphiti;
  postgresql.org/about/news/postgresql-19-beta-1-3313 (SQL/PGQ, 4 Jun 2026);
  depesz.com/2026/07/31/waiting-for-postgresql-19-sql-property-graph-queries-sql-pgq
  (missing features; page says a change was rolled back); neo4j.com/blog/developer/production-proofing-cypher-mcp-server.
  PG19 release notes page (postgresql.org/docs/devel/release-19.html) did not list SQL/PGQ yet.
  Search results only: ISO 39075 date (SCC, Wikipedia; iso.org 403); Panama Papers
  11.5M docs and Neo4j use (neo4j.com, linkurio.us); Amazon AutoKnow KDD 2020;
  CVE-2026-35402 (NVD page returned no body).
  Not verified: LinkedIn Economic Graph, NASA lessons-learned graph, SHACL/OWL/FIBO/GS1
  details, Amazon "Product Graph 2018" framing, Zep benchmark figures.
  Flagged: re-check PG19 SQL/PGQ at GA (Sept-Oct 2026 release notes); rag-vector-databases
  GraphRAG lesson may deserve the LazyGraphRAG note too. No new-lesson gaps.

- 2026-10-25 — llms — tier 2. Picked because no tier-1 row was due (all within their
  45-day cadence) and `llms` was a tier-2 row with `never`. Outcome: fixed + expanded.
  Read all 7 lessons, README and recap first. Fixes: (1) temperature lesson now says current
  Anthropic models reject non-default `temperature`/`top_p`/`top_k` with a 400 error, and any
  value from API version 2026-10-21; effort replaces the dial; (2) determinism cause at
  temperature 0 (batch dependence); (3) context window: 1M tokens on current models, context
  rot, thinking tokens count, compaction, long-prompt pricing; (4) new reasoning-models section
  in what-is-an-llm; (5) prompting lesson: CoT now built in, 3-5 examples; (6) choosing-a-model:
  effort, default-effort trap, efficiency-first vs capability-first, dated price snapshot,
  combining models, open-weight caution. Sources opened: platform.claude.com docs — models
  overview, context-windows, choosing-a-model, effort, prompting best practices, thinking
  (sampling-parameter section), migration-2026-10-21 (only the preview opened), pricing
  (preview only); developers.openai.com/api/docs/guides/reasoning; trychroma.com/research/
  context-rot; arxiv.org/abs/2307.03172; thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference.
  Search results only, not opened: open-weight gap trackers (Epoch, Artificial Analysis
  write-ups), OpenRouter Claude 4.7 migration page. NOT verified: recap war stories (strawberry,
  Sydney/Bing limits, prompt-engineer job trend, routing savings) — the Bing blog URL 404ed and the
  HBS jagged-frontier page returned 403, so the "jagged frontier" attribution is unchecked; OpenAI/
  Google temperature behavior on reasoning models (OpenAI page is silent); top-p/top-k definitions.
  Flagged: recap.md claims need a primary-source pass; a standalone lesson on reasoning models and
  effort may be worth building (not built, scope boundary).

- 2026-10-26 — evaluation-and-observability — tier 2. Picked because no tier-1 row was due
  (all within their 45-day cadence), and among the tier-2 `never` rows this is the one a Senior PM
  is asked about in every AI launch review. Outcome: fixed + expanded. Read both lessons, README
  and recap in full first. Accuracy: (1) recap "silent weight update" story was unsourced and
  one-sided; now cites Chen et al. 2023 (GPT-4 prime accuracy 84% -> 51%) with the Narayanan/Kapoor
  critique (all-prime test set, code-format scoring) and Anthropic's Sept 2025 postmortem;
  (2) quantization story was unsourced; now cites Marchisio et al., EMNLP 2024 Findings
  (1.7% automatic vs 16.0% human drop in Japanese); (3) judge-bias story now cites Zheng et al. 2023
  and Panickssery et al. 2024; (4) trajectory-eval story marked as a common risk, not a single
  incident, and tempered with Anthropic's "grade the outcome, not the path" guidance.
  Coverage: noise and error bars, pass@k vs pass^k, offline/online/A-B layers, 20-50 starter tasks,
  generic-metric and vibe-eval anti-patterns (lesson 1); trace-reading counts (30/100), pass/fail
  over scales, per-failure-mode judges with TPR/TNR on held-out labels, judge biases, capability vs
  regression suites and saturation, pass-all gate, post-launch re-analysis, synthetic-data caveats
  (lesson 2). check_module: avg sentence 27.2 -> 20.6 (WARN threshold 20), Flesch 55 (pass).
  Sources opened: hamel.dev/blog/posts/evals-faq (first 100k of 153k chars only);
  anthropic.com/engineering/demystifying-evals-for-ai-agents;
  anthropic.com/engineering/a-postmortem-of-three-recent-issues;
  developers.openai.com/api/docs/guides/evaluation-best-practices; arxiv.org/abs/2306.05685;
  arxiv.org/abs/2404.13076; arxiv.org/abs/2307.09009; normaltech.ai/p/is-gpt-4-getting-worse-over-time;
  arxiv.org/abs/2411.00640 (abstract only); aclanthology.org/2024.findings-emnlp.935;
  arxiv.org/abs/2410.21819 (abstract only; not cited in text).
  Not verified: the "wasteful path" agent claim has no primary incident source (reworded as a risk);
  OpenTelemetry GenAI conventions status (docs moved to github.com/open-telemetry/semantic-conventions-genai;
  fetched pages gave no stability status); the linked content/04 and agentic-ai lessons were not re-audited.
  Flagged (other module): content/04-evals-observability/evals.md (~line 133) says OTel GenAI conventions
  "are standardizing trace formats" and tooling is "portable" — check stability status at the new repo
  before leaving that unqualified. recap.md still lacks a "Test yourself" section and the README a
  "Where the depth lives" map (check_module WARNs); worked-example/under-the-hood sections would need
  a structural change, not built. No new-lesson gaps.

- 2026-10-29 — cost-optimization — tier 2. Picked because no tier-1 row was due (all within their
  45-day cadence), and among the tier-2 `never` rows this one carries the most price claims that go
  stale in a roadmap review. Outcome: fixed + expanded. Read both lessons, README and recap in full
  first. Accuracy: (1) "prices fall steeply" now tied to capability tier with the Opus 4.1 -> 5.5
  change ($15/$75 -> $4/$20) and the higher Fable 5.1 tier ($10/$50); (2) worked self-hosting case
  labelled illustrative; (3) recap war stories reworded as commonly reported patterns, not sourced
  incidents. Coverage: price-sheet modifiers table (cache 0.1x/0.05x/0.025x hits, 1.25x/2x writes,
  batch 50%, fast mode, 1.1x US inference, Haiku 5.5 long-prompt tier); output-vs-input 5:1,
  thinking tokens billed as output, ~30% tokenizer inflation, effort as a lever, batch/flex timing,
  cache-hit-rate as a metric; GPU utilization as the hidden breakeven variable and the cheap-small-
  model and third-party-hosting alternatives; in-request caps (max_output_tokens, thinking_tokens
  tracking, agent turn caps); unit economics per outcome (FinOps Foundation); a tokens-per-task
  factor in the forecast. check_module: FAIL (avg sentence 26.1, Flesch 44) -> WARN (20.7, Flesch 53).
  Sources opened: platform.claude.com/docs/en/about-claude/pricing; .../build-with-claude/prompt-caching;
  .../batch-processing; .../extended-thinking; .../effort; .../about-claude/models/choosing-a-model;
  developers.openai.com/api/docs/guides/reasoning; .../flex-processing;
  finops.org/insights/token-economics-the-atomic-unit-of-ai-value/ (the tokenomics-fit-together page
  loaded but its body was not read).
  Search results only, not opened: Gartner March 2026 agentic token multiple (5-30x) — marked in the
  lesson as unopened; self-hosting breakeven blogs (Spheron, Spendark, Cohorte, GeICO tech blog 403);
  Elastic token-cost blog (opened, vendor, not cited). NOT verified: other vendors' (Google, OpenAI)
  current price tables and cache discounts — the lessons cite only Anthropic numbers and say so;
  Bedrock/Vertex prices; the 'chargeback changes behavior' claim (no primary source, reworded).
  Flagged (other module): content/04-evals-observability/cost-attribution.md and
  content/01-inference-internals/prompt-vs-semantic-caching.md may carry old cache multipliers
  (older docs said a flat 0.1x read) — check against the pricing page. Not built: a standalone lesson
  on reasoning-token and agent cost control (scope boundary). README still lacks a "Where the depth
  lives" map and recap a "Test yourself" section (structural, not built).

- 2026-10-30 — ai-agents — tier 2. Picked because no tier-1 row was due (ai-engineering is at 40 of
  45 days, the rest are newer) and `ai-agents` was a tier-2 `never` row a Senior PM meets in every
  AI roadmap review. Outcome: fixed + expanded. Read README, all 5 lessons and recap in full first.
  Accuracy: (1) METR text said the faster pace was "reported"; METR's own page now says it is no
  longer actively updated, warns above 16 hours is unreliable, and says time horizon measures human
  task time, not agent run time. Lesson and recap reworded; the 4-5 month figure is marked as
  secondary and unconfirmed. (2) "Claude 4.6 and later" thinking claim reworded to "current Claude
  models" (docs show adaptive thinking as the model behaviour). (3) 4x/15x token claim now labelled
  Anthropic internal data. (4) MCP donation: added Block and OpenAI as co-founders. Coverage: effort
  and agent loops (thinking billed as output, first request carries most reasoning, effort changes
  break the cache); long-running multi-session agent failure modes and fixes; Replit production
  database deletion as a case for code-level limits; full OWASP agentic Top 10 list.
  Sources opened: metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/;
  metr.org/time-horizons; anthropic.com/engineering/building-effective-agents;
  anthropic.com/engineering/multi-agent-research-system;
  anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation;
  cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade
  (A2A to Linux Foundation June, v0.3); platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost;
  anthropic.com/engineering/effective-harnesses-for-long-running-agents;
  genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (date only);
  incidentdatabase.ai/entities/jason-lemkin/.
  Search results only, not opened: Gartner press release (403 on fetch; figures confirmed in
  snippets and many secondary reports); OWASP ten risk names (secondary summaries); METR post-2023
  doubling estimates (buttondown, Manifold); Replit details beyond AIID (eWeek, The Stack).
  NOT verified: Moffatt v. Air Canada (CanLII 403; recap figures CA$650.88 / CA$812.02 unchecked this
  run); a possible May 2026 Gartner forecast about demoting agents (single weak source); the
  A2A/MCP current spec versions; vendor agent SDKs (OpenAI, Google) not compared.
  Flagged: recap Moffatt figures need a primary-source pass. A lesson on agent identity and
  permissions (non-human identity) may be worth building; not built (scope boundary).
