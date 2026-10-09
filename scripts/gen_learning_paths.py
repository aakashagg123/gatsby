#!/usr/bin/env python3
"""Generate learning-paths/*.md from one data structure.

Every lesson link is checked against the filesystem, and every time estimate is computed
from lesson counts, so the pages cannot drift from the tracks. The generated markdown is
committed. To change a path, edit the PATHS data below and run:

    python3 scripts/gen_learning_paths.py && python3 scripts/build_learning_paths.py

When a planned module ships (machine learning, tensors, CNNs), replace its SOON(...) step
with T(...) lesson links.
"""
import glob
import importlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
OUT = os.path.join(ROOT, "learning-paths")

FLAT_MIN = 25      # minutes per flat-track or content/ lesson
HARNESS_MIN = 60   # minutes per harness-engineering lesson
SKIM_MIN = 120     # minutes to skim one harness phase

NAMES = {
    "product-sense": "Product sense", "technical-product-sense": "Technical product sense",
    "technical-product-management": "Technical product management",
    "generative-ai": "Generative AI", "llms": "LLMs", "prompt-engineering": "Prompt engineering",
    "evaluation-and-observability": "Evaluation & observability", "cost-optimization": "Cost optimization",
    "ai-security-and-guardrails": "AI security & guardrails", "agentic-ai": "Agentic AI",
    "rag-vector-databases": "RAG & vector databases", "memory-and-context": "Memory & context",
    "context-engineering": "Context engineering", "tool-calling": "Tool calling",
    "ai-agents": "AI agents", "agentic-workflows": "Agentic workflows",
    "knowledge-graphs": "Knowledge graphs", "access-control": "Access control",
    "system-design": "System design", "api-integrations": "APIs & integrations",
    "first-principles": "First principles",
}
CONTENT = {
    "00-foundations": "AI engineering: foundations", "01-inference-internals": "AI engineering: inference internals",
    "02-reliable-outputs": "AI engineering: reliable outputs", "03-rag": "AI engineering: RAG",
    "04-evals-observability": "AI engineering: evals & observability",
    "05-safety-multitenancy": "AI engineering: safety & multi-tenancy",
    "06-strategy-tradeoffs": "AI engineering: strategy & tradeoffs",
}
HARNESS = {
    1: "01-foundations-and-the-loop", 2: "02-tools", 3: "03-context-and-memory",
    4: "04-prompts-and-instructions", 5: "05-files-and-shell", 6: "06-permissions-and-security",
    7: "07-planning-and-subagents", 8: "08-extending-mcp-skills-retrieval",
    9: "09-reliability-evals-and-ops", 10: "10-capstone",
}


def h1(path):
    return open(path, encoding="utf-8").readline().strip().lstrip("# ").strip()


_cfg = {}


def flat_lessons(track):
    if track not in _cfg:
        mod = importlib.import_module("build_" + track.replace("-", "_"))
        _cfg[track] = list(mod.CFG["lessons"])
    return _cfg[track]


def content_lessons(folder):
    fs = sorted(glob.glob(f"{ROOT}/content/{folder}/*.md"))
    return [os.path.basename(f)[:-3] for f in fs if os.path.basename(f) not in ("README.md", "recap.md")]


def harness_count(n):
    return len(glob.glob(f"{ROOT}/harness-engineering/phases/{HARNESS[n]}/*/"))


class Item:
    """One group of reading inside a stage."""

    def __init__(self, kind, **kw):
        self.kind, self.kw = kind, kw
        self.minutes, self.line, self.key, self.count, self.total = 0, "", None, 0, 0
        getattr(self, "_" + kind)()

    def _t(self):  # flat track lessons
        t, ids = self.kw["track"], self.kw["ids"]
        order = flat_lessons(t)
        parts = []
        for i in ids:
            key = order[i - 1]
            p = f"{ROOT}/{t}/{key}.md"
            assert os.path.exists(p), p
            parts.append(f"[{i}. {h1(p)}](../{t}/{key}.md)")
        self.pairs, self.parts, self.prefix = [(t, i) for i in ids], parts, f"**{NAMES[t]}**: "
        self.line = self.prefix + " · ".join(parts)
        self.minutes, self.key, self.count, self.total = FLAT_MIN * len(ids), t, len(ids), len(order)

    def _c(self):  # content/ stack lessons
        f, ids = self.kw["folder"], self.kw["ids"]
        parts = []
        for k in ids:
            p = f"{ROOT}/content/{f}/{k}.md"
            assert os.path.exists(p), p
            parts.append(f"[{h1(p)}](../content/{f}/{k}.md)")
        self.line = f"**{CONTENT[f]}**: " + " · ".join(parts)
        self.minutes, self.key, self.count = FLAT_MIN * len(ids), "content", len(ids)
        self.total = sum(len(content_lessons(x)) for x in CONTENT)

    def _h(self):  # harness phase
        n, mode = self.kw["phase"], self.kw["mode"]
        p = f"{ROOT}/harness-engineering/phases/{HARNESS[n]}/README.md"
        assert os.path.exists(p), p
        c = harness_count(n)
        verb = "build it" if mode == "full" else "skim it"
        note = f"{c} lessons, {verb}"
        self.line = f"**Harness engineering**: [{h1(p)}](../harness-engineering/phases/{HARNESS[n]}/README.md) ({note})"
        self.minutes = HARNESS_MIN * c if mode == "full" else SKIM_MIN
        if self.kw.get("minutes"):
            self.minutes = self.kw["minutes"]
            self.line += f". {self.kw['note']}"
        self.key, self.count = "harness", c
        self.total = sum(harness_count(i) for i in HARNESS)

    def _f(self):  # flowable overview
        assert os.path.exists(f"{ROOT}/flowable/README.md")
        self.line = "**Flowable**: [Process automation from scratch](../flowable/README.md) (read the overview and the concept lessons)"
        self.minutes, self.key, self.count = 90, "flowable", 1
        self.total = 1

    def _soon(self):
        self.line = f"**{self.kw['name']}**: coming soon. {self.kw.get('note', '')}".strip()
        self.minutes, self.key, self.count, self.total = 0, None, 0, 0


def T(track, *ids): return Item("t", track=track, ids=list(ids))
def C(folder, *ids): return Item("c", folder=folder, ids=list(ids))
def H(phase, mode="full", minutes=None, note=""): return Item("h", phase=phase, mode=mode, minutes=minutes, note=note)
def F(): return Item("f")
def SOON(name, note=""): return Item("soon", name=name, note=note)


def hours(minutes):
    h = round(minutes / 60 * 2) / 2
    if h < 1:
        return "under an hour"
    return "about 1 hour" if h == 1 else f"about {h:g} hours"


STAMP = "*Last reviewed: 2026-10 · Volatility: medium*"
ML_NOTE = "A module on machine learning basics is planned. Skip this step until it is published."
PATHS = []

# ------------------------------------------------------------------ Senior PM
PATHS.append(dict(
    slug="senior-product-manager", title="Learning path: Senior Product Manager",
    role="senior product manager", short="Senior PM",
    who="a product manager with several years of experience who is starting to own AI features",
    outcome="You can lead an AI feature end to end. You choose the approach, set the quality bar, price it, and judge the risk.",
    prereq="Several years in product. No machine learning background is needed.",
    tldr=("This path takes a working product manager from \"AI is a black box\" to \"I can make the calls only the PM can make.\" "
          "It starts with a technical footing, adds plain-language model literacy, and then spends most of its time on four decisions: "
          "build, buy or fine-tune; the quality bar; the cost; and the risk. It skips engineering internals on purpose."),
    callout=("**Why it matters** — AI features fail in ways ordinary features do not. A PM who cannot read a quality report or a cost line cannot steer.",
             "**What it changes in your decisions** — You ask for an eval plan before a build starts. You ask for cost per task before a launch. You treat risk as a spec section.",
             "**Ask your eng team** — *\"What does a bad answer look like, how often does it happen, and how would we know?\"*",
             "**Risk if ignored** — You ship on a demo. The first real users find the failure modes, and the team has no way to measure them."),
    stages=[
        dict(name="Technical footing", why="AI products sit on ordinary systems. You need the same words your engineers use.",
             items=[T("technical-product-sense", 1, 2, 4, 5, 9)],
             ready="You can explain a request path, an API contract and where latency comes from. You can name what changes when one component is a model."),
        dict(name="AI literacy", why="Learn what a model is, what it does well, and what it does badly. Plain language, no maths.",
             items=[T("generative-ai", 1, 2, 3, 4), T("llms", 1, 2, 3, 5, 6), T("prompt-engineering", 1, 2, 7, 9)],
             ready="You can say why the same prompt gives different answers, what a context window limits, and when a bad result is a prompt problem and when it is not."),
        dict(name="The decisions only you own", why="Pick the approach, set the bar, count the cost, and accept the risk.",
             items=[T("generative-ai", 5, 6), T("llms", 7), T("product-sense", 7), T("technical-product-management", 9),
                    T("evaluation-and-observability", 1, 2), T("cost-optimization", 1, 2), T("ai-security-and-guardrails", 1, 3)],
             ready="You can write a one-page case for build, buy or fine-tune. It has an eval plan, a cost per task and the top three risks."),
        dict(name="Go deeper where your product needs it (optional)", why="Read only what your roadmap touches. Retrieval, memory and agents each change the product shape.",
             items=[T("rag-vector-databases", 1, 5, 6), T("memory-and-context", 1, 5), T("agentic-ai", 1, 8), T("tool-calling", 1),
                    SOON("Machine learning", ML_NOTE)],
             ready="You can tell when a feature needs retrieval, memory or an agent, and when it does not."),
    ],
    skip=["If you have shipped an ML-backed feature, skip stage 1 and start stage 2 at the LLMs lessons.",
          "If a launch is close, start at stage 3. Read `What an LLM actually is` and `The context window` first, because the decision lessons assume them.",
          "If your product is not agentic, skip the agent lessons in stage 4.",
          "If you already run evals with your team, read the two evaluation lessons as a check, not as new material."],
    example=[("1", "Stage 1", "Write a one-page request path for your product, marking where a model would sit."),
             ("2", "Stage 2", "Take one bad model answer from your own product and explain it using the LLM lessons."),
             ("3", "Stage 3 (decisions)", "Draft the build, buy or fine-tune case for one feature."),
             ("4", "Stage 3 (quality and cost)", "Add an eval plan and a cost per task to the draft."),
             ("5", "Stage 3 (risk)", "List the top three risks and the guardrail for each. Review with your engineering lead."),
             ("6", "Stage 4", "Pick the one deep topic your roadmap needs and read it.")],
    example_who="A senior PM with three hours a week",
    tradeoffs=["**Breadth vs. depth.** This path reads many tracks shallowly. You gain vocabulary. You do not gain engineering skill, and that is the point.",
               "**Order vs. urgency.** If a launch is close, jump to stage 3 and come back. The checkpoints tell you what you missed.",
               "**Reading vs. doing.** The decisions stage only works if you apply it to a real feature."],
    failures=["**Reading the whole library.** The path picks lessons within tracks. Do not read every lesson in every track.",
              "**Stopping at stage 2.** Literacy without the decisions stage leaves you able to talk about AI but not to steer it.",
              "**Skipping evaluation.** The most common gap is shipping with no way to measure quality.",
              "**Reading in a vacuum.** Apply each stage to a real feature or the knowledge fades."],
    checklist=["Can I explain how our feature works to a new engineer without saying \"the AI does it\"?",
               "Is there an eval plan with a named owner?",
               "Do I know the cost per task, and what happens to it at ten times the traffic?",
               "Have I listed the top three risks and a guardrail for each?",
               "Do I know which of retrieval, memory and agents our product needs?"],
    related=["ai-product-lead", "ai-engineering-lead"],
))

# ------------------------------------------------------------------ AI Product Lead
PATHS.append(dict(
    slug="ai-product-lead", title="Learning path: AI Product Lead",
    role="AI product lead", short="AI Product Lead",
    who="a product leader who owns an AI product line or a team of PMs shipping AI features",
    outcome="You set direction for how the product grounds its answers, remembers, acts, stays safe and stays affordable. You can review a design with engineering and ask informed questions.",
    prereq="This path builds on the Senior PM path, stages 1 to 3, or equivalent experience. Lessons marked ↺ repeat that path, so skip them if you did it. You have shipped or closely reviewed one AI feature.",
    repeat_from="senior-product-manager",
    tldr=("This path covers the layers between a model and a product: grounding, context, memory, tools, agents, workflows, trust and cost. "
          "It is wider and deeper than the Senior PM path. It stays at the decision level. You read enough mechanics to ask sharp questions, not to build."),
    callout=("**Why it matters** — At this level your decisions set the architecture. A weak call on grounding or autonomy is expensive to reverse.",
             "**What it changes in your decisions** — You choose retrieval, memory and agent scope on purpose. You set the autonomy dial per task. You fund evals and guardrails as roadmap items.",
             "**Ask your eng team** — *\"Which layer fails first, and how would we see it in production?\"*",
             "**Risk if ignored** — You ship an agent with the wrong autonomy or a memory that leaks. You find out from a customer."),
    stages=[
        dict(name="Model and data foundations", why="You decide how the product grounds answers. That choice drives quality and cost.",
             items=[T("llms", 1, 2, 3, 5, 6, 7), T("generative-ai", 3, 4, 5), SOON("Machine learning", ML_NOTE),
                    T("rag-vector-databases", 1, 5, 6, 7), T("knowledge-graphs", 1, 6, 8)],
             ready="You can compare prompting, retrieval and fine-tuning for a feature and pick one with reasons."),
        dict(name="Context and memory", why="What the model sees is a product decision. So is what it remembers.",
             items=[T("context-engineering", 1, 3, 4, 5, 6, 7), T("memory-and-context", 1, 2, 3, 4, 5), T("prompt-engineering", 10)],
             ready="You can write the context spec for a feature: sources, owners, freshness and how quality is measured."),
        dict(name="Action: tools, agents, workflows", why="The line between talking and doing carries the most risk and the most value.",
             items=[T("tool-calling", 1, 2, 3), T("ai-agents", 1, 2, 3, 4, 5), T("agentic-workflows", 1, 2, 3), T("agentic-ai", 6, 8)],
             ready="You can set the autonomy level for a task, justify it, and say what would make you lower it."),
        dict(name="Trust, access and cost", why="Evals, security, permissions and spend decide whether the feature survives contact with real use.",
             items=[T("evaluation-and-observability", 1, 2), T("ai-security-and-guardrails", 1, 2, 3), T("access-control", 1, 8),
                    T("cost-optimization", 1, 2), T("technical-product-sense", 8)],
             ready="You can show a reviewer your eval results, your threat model and your cost per task."),
        dict(name="Run the product", why="Turn the above into specs, launches and a response plan.",
             items=[T("technical-product-management", 3, 6, 7, 8, 9), T("product-sense", 7)],
             ready="You can write the spec, the launch gate and the incident plan for an AI feature."),
    ],
    skip=["If you ran the Senior PM path, skip the LLMs and generative AI lessons you have already read.",
          "If your product has no agents yet, read the agent lessons in stage 3 as risk reading, not as design reading.",
          "If you do not work with regulated customers, skim the governance lesson."],
    example=[("1", "Stage 1", "Pick one feature and write which of prompting, retrieval or fine-tuning it should use."),
             ("2", "Stage 2", "Write its context spec."),
             ("3", "Stage 2", "Review its memory design with a privacy owner."),
             ("4", "Stage 3", "Set its autonomy level and the trigger to lower it."),
             ("5", "Stage 4", "Run a tabletop review of its threat model, evals and cost."),
             ("6", "Stage 5", "Write the launch gate and incident plan.")],
    example_who="An AI product lead with four hours a week",
    tradeoffs=["**Coverage vs. time.** This is a long path. Each stage ends with a checkpoint, so you can stop at the layer you own.",
               "**Product depth vs. engineering depth.** You read mechanics only to ask better questions. The engineer path covers building.",
               "**Standards vs. speed.** Stage 4 slows early work and speeds later work."],
    failures=["**Treating agents as the default.** Read \"when not to build an agent\" before you commit.",
              "**Memory without a privacy owner.** Memory is a data product with a retention policy.",
              "**No eval owner.** Every layer in this path needs a quality measure and a person who owns it.",
              "**Reading without reviewing.** Take each stage to a real design review."],
    checklist=["Does every AI feature have a grounding choice with a written reason?",
               "Is there a context spec for each feature?",
               "Is the autonomy level of each agent written down?",
               "Can I show evals, a threat model and a cost per task for each feature?",
               "Is there a launch gate and an incident plan?"],
    related=["senior-product-manager", "ai-engineering-lead"],
))

# ------------------------------------------------------------------ AI Engineer
PATHS.append(dict(
    slug="ai-engineer", title="Learning path: AI Engineer",
    role="AI engineer", short="AI Engineer",
    who="a software engineer who builds AI-powered systems",
    outcome="You can build, test and run a retrieval-backed, tool-using agent, and explain how it fails.",
    prereq="Comfortable Python and one backend stack. Basic linear algebra helps. The foundations stage covers what you need.",
    tldr=("This path is build-first. It starts with how models learn, then moves through models and APIs, grounding and memory, agents and the harness, and production. "
          "It is the longest path. The harness track is the core: you build a coding agent's parts by hand and end with a tested capstone."),
    callout=("**Why it matters** — Calling an API is easy. Making the result reliable, safe and affordable is the job.",
             "**What it changes in your decisions** — You test before you tune. You put checks in code, not in prompts. You design for failure first.",
             "**Ask yourself** — *\"If this step returns garbage, what stops it from doing damage?\"*",
             "**Risk if ignored** — The demo works. Production loops, leaks or overspends, and nobody can say why."),
    stages=[
        dict(name="Foundations", why="Learn how a model is trained and what its data looks like. Everything later builds on it.",
             items=[SOON("Machine learning", ML_NOTE), SOON("Tensors", "Shapes, broadcasting and batching. Planned."),
                    SOON("CNNs", "Optional branch for vision. Planned."), T("llms", 1, 2, 5)],
             ready="You can explain what a token and a context window are, and how sampling changes the output. Until the machine learning module ships, add a training-loop primer of your own."),
        dict(name="Models and APIs", why="Call models well: contracts, streaming, retries, structured output and prompts that hold up.",
             items=[T("llms", 3, 6, 7), T("api-integrations", 1, 2, 3, 4, 5, 6), T("prompt-engineering", 2, 4, 5, 6, 7, 9, 10)],
             ready="You can call a model with retries and a typed output, and you can diagnose a failing prompt."),
        dict(name="Grounding and memory", why="Give the model the right data, in the right shape, at the right time.",
             items=[T("rag-vector-databases", 1, 2, 3, 4, 5, 7), C("03-rag", "rag-architecture", "retrieval-evals"),
                    T("memory-and-context", 3, 4), T("context-engineering", 3, 6)],
             ready="You can build a retrieval pipeline and measure its quality with a test set."),
        dict(name="Agents and the harness (build it)", why="Build the parts of an agent by hand. This is the core of the path.",
             items=[T("tool-calling", 2, 3), C("02-reliable-outputs", "function-calling"), T("ai-agents", 2), T("agentic-workflows", 1, 2, 3),
                    H(1), H(2), H(3), H(4), H(5), H(6)],
             ready="You have a working loop with tools, a permission gate and a context budget, and tests that fail when you break them."),
        dict(name="Production", why="Plan for failure: extend, test, observe, secure and scale.",
             items=[H(7), H(8), H(9), H(10, "full", 180, "Allow about 3 hours: the capstone plus your own evals, traces and cost."), T("ai-agents", 4, 5), C("01-inference-internals", "prefill-vs-decode", "batching-and-paged-attention", "kv-cache-management", "prompt-vs-semantic-caching"),
                    C("02-reliable-outputs", "model-routing", "structured-output", "agent-guardrails"), C("04-evals-observability", "evals", "observability", "cost-attribution"),
                    C("05-safety-multitenancy", "safety-engineering", "multi-tenant-isolation"),
                    T("ai-security-and-guardrails", 1, 2), T("access-control", 1, 2, 8), T("system-design", 1, 2, 7)],
             ready="Your capstone passes its tests, and you can show its evals, traces, permission rules and cost."),
    ],
    skip=["If you know machine learning, skip the foundations stage and start at models and APIs.",
          "If you only work with hosted models, read the inference lessons as background and skip the deep ones.",
          "If you want a faster tour, build harness phases 1, 2, 3 and 6 and skim the rest."],
    example=[("1", "Stage 2", "Call a model through an API with retries and a typed output."),
             ("2", "Stage 3", "Add retrieval over your own documents and measure it with ten questions."),
             ("3", "Stage 4", "Build harness phase 1: the loop. Run its asserts."),
             ("4", "Stage 4", "Build harness phases 2 and 3: tools and context."),
             ("5", "Stage 4", "Build harness phases 4 and 5: prompts, files and shell."),
             ("6", "Stage 4", "Build harness phase 6: permissions and security."),
             ("7", "Stage 5", "Build harness phases 7 and 8: planning, subagents and MCP."),
             ("8", "Stage 5", "Build phase 9 and the capstone. Break the capstone on purpose and watch it fail.")],
    example_who="An AI engineer with nine hours a week",
    tradeoffs=["**Build vs. read.** The harness lessons ask you to type the code. Skimming saves time and loses the failures you would have hit.",
               "**Depth vs. breadth.** The inference lessons go deep on serving. Read them if you run models, skim them if you call hosted ones.",
               "**Frameworks vs. from scratch.** Building by hand first makes later framework choices easier to judge."],
    failures=["**Tuning before testing.** Build the eval set first. Tuning without one is guessing.",
              "**Checks in prompts.** A rule in a prompt is a request. A rule in code is a control.",
              "**Skipping the permission gate.** An agent without one is a security incident waiting for a trigger.",
              "**No failure tests.** Break your agent on purpose and watch the tests catch it."],
    checklist=["Does every model call have a timeout, a retry rule and a typed output?",
               "Do I have a test set for retrieval and for the agent?",
               "Is every tool call behind a permission check in code?",
               "Is there a budget on steps and cost?",
               "Can I trace one request from input to answer?"],
    related=["ai-engineering-lead", "ai-product-lead"],
))

# ------------------------------------------------------------------ AI Engineering Lead
PATHS.append(dict(
    slug="ai-engineering-lead", title="Learning path: AI Engineering Lead",
    role="AI engineering lead", short="AI Engineering Lead",
    who="an engineering manager or tech lead who runs a team that builds AI systems",
    outcome="You review AI architecture, set quality and safety standards, control cost, and work well with product.",
    prereq="Years of engineering and some time running a team. You may not have shipped an AI feature yet.",
    tldr=("This path is the engineer path in short form, plus what a lead adds: economics, architecture review, governance, and working with product. "
          "You read for judgement. You skim the build lessons, so you can ask your team the right questions, and you read the decision lessons in full."),
    callout=("**Why it matters** — Your team will build what you can review. If you cannot read an architecture, an eval report or a threat model, you cannot lead the work.",
             "**What it changes in your decisions** — You set standards for evals, safety and cost before the build. You approve designs by their failure handling.",
             "**Ask your team** — *\"Show me how this fails, how we would notice, and what it costs per request.\"*",
             "**Risk if ignored** — The team ships fast and unsafe. Review happens after an incident."),
    stages=[
        dict(name="How models behave and what they cost", why="Cost and latency come from model and serving choices. Know the levers.",
             items=[T("llms", 1, 2, 3, 6, 7), SOON("Machine learning", ML_NOTE),
                    C("01-inference-internals", "prefill-vs-decode", "batching-and-paged-attention", "prompt-vs-semantic-caching"),
                    C("02-reliable-outputs", "model-routing"), C("04-evals-observability", "cost-attribution"),
                    C("06-strategy-tradeoffs", "finetune-vs-icl-vs-rag", "inference-stack-tradeoffs"), T("cost-optimization", 1, 2)],
             ready="You can explain where a request's time and money go and name the three levers that change them."),
        dict(name="Architecture you can review", why="Know the shapes: grounding, context, memory, agents, workflows. Skim the build lessons.",
             items=[T("rag-vector-databases", 1, 5, 6), T("context-engineering", 1, 3, 5), T("memory-and-context", 1, 5),
                    T("tool-calling", 2), T("knowledge-graphs", 1, 8), T("ai-agents", 1, 3, 4), T("agentic-workflows", 1, 2, 3), H(1, "skim"), H(6, "skim"), H(7, "skim"), H(9, "skim")],
             ready="You can review a design doc for an agent: its loop, tools, permissions, budgets and failure handling."),
        dict(name="Quality, safety and access", why="Set the standards. Evals, threat models and access control are yours to require.",
             items=[T("evaluation-and-observability", 1, 2), C("04-evals-observability", "evals", "observability"),
                    T("ai-security-and-guardrails", 1, 2, 3), T("access-control", 1, 2, 5, 8),
                    C("05-safety-multitenancy", "safety-engineering", "multi-tenant-isolation"), C("06-strategy-tradeoffs", "production-failure-modes")],
             ready="You can name the release gate for an AI feature, who owns it, and what evidence a buyer would ask for."),
        dict(name="Systems at scale", why="AI features still run on ordinary systems. Hold the same bar for reliability.",
             items=[T("system-design", 1, 2, 3, 7), T("technical-product-sense", 5, 8)],
             ready="You can run a design review for scale, failure and cost on any service in the stack."),
        dict(name="Work with product and run the team", why="Turn standards into process: specs, launches, incidents and how product and engineering share ownership.",
             items=[T("technical-product-management", 3, 4, 5, 6, 7, 8, 9), T("product-sense", 7)],
             ready="You and your PM share one definition of done, one quality bar and one incident process."),
    ],
    skip=["If you came from machine learning, skip the first stage's model lessons and read the cost lessons.",
          "If your team already runs evals in CI, read the evaluation lessons as a gap check.",
          "If you want hands-on depth, add the build lessons from the AI Engineer path.",
          "Flowable (process automation) is not on this path. Add it if your team builds approval or long-running workflows."],
    example_note="This plan is a fast tour: one activity per stage. The full path takes about 11 weeks at this pace.",
    example=[("1", "Stage 1", "Pull one month of cost and latency numbers for your busiest model call. Find the biggest lever."),
             ("2", "Stage 2", "Review one agent design doc against the loop, tools, permissions and budget."),
             ("3", "Stage 3", "Write the release gate for one feature and name its owner."),
             ("4", "Stage 4", "Run a failure review on one service."),
             ("5", "Stage 5", "Agree a definition of done with your PM.")],
    example_who="An AI engineering lead with three hours a week",
    tradeoffs=["**Judgement vs. hands-on skill.** Skimming the build lessons keeps you fast. It also means you rely on your team's account of how things fail.",
               "**Standards first vs. build first.** Standards slow the first feature and speed the next ten.",
               "**One path vs. two.** Pair this path with the engineer path if you still write code."],
    failures=["**Approving by demo.** Review by failure handling, not by the happy path.",
              "**No owner for the eval set.** An eval set with no owner decays.",
              "**Treating safety as a security-team task.** Product and engineering own the design that makes it hold.",
              "**Skipping the economics.** Cost surprises arrive after launch."],
    checklist=["Do we have a written release gate for each AI feature?",
               "Does every agent design show permissions, budgets and a kill switch?",
               "Do we track cost and latency per request?",
               "Do we have an incident process that covers model failures?",
               "Do product and engineering share one quality bar?"],
    related=["ai-engineer", "ai-product-lead"],
))


def minutes_of(stages):
    return sum(i.minutes for s in stages for i in s["items"])


def link_path(slug, text):
    return f"[{text}](./{slug}.md)"


def repeat_set(p):
    src = p.get("repeat_from")
    if not src:
        return set()
    return {pair for x in PATHS if x["slug"] == src for s_ in x["stages"] for it in s_["items"] if it.kind == "t" for pair in it.pairs}


def item_line(it, rep):
    if it.kind != "t" or not rep:
        return it.line
    return it.prefix + " · ".join(part + (" ↺" if pair in rep else "") for pair, part in zip(it.pairs, it.parts))


def repeat_minutes(p):
    rep = repeat_set(p)
    return FLAT_MIN * sum(1 for s_ in p["stages"] for it in s_["items"] if it.kind == "t" for pair in it.pairs if pair in rep)


def render_path(p):
    L = []
    a = L.append
    rep = repeat_set(p)
    total = minutes_of(p["stages"])
    a(f"# {p['title']}\n")
    a("*Part of [Learning paths](./README.md)*\n")
    a(f"{STAMP}\n")
    a("## TL;DR\n")
    a(p["tldr"] + "\n")
    a(f"**Who it is for:** {p['who']}.\n")
    a(f"**Outcome:** {p['outcome']}\n")
    a(f"**Before you start:** {p['prereq']}\n")
    if rep:
        a(f"**Length:** {hours(total)}, across {len(p['stages'])} stages. If you did the Senior PM path, {hours(total - repeat_minutes(p))}, because lessons marked ↺ repeat it. The time is a rough estimate (see Under the hood).\n")
    else:
        a(f"**Length:** {hours(total)}, across {len(p['stages'])} stages. The time is a rough estimate (see Under the hood).\n")
    a(f"> 🎯 **For the {p['role']}**")
    a(">")
    for i, c in enumerate(p["callout"]):
        a(f"> {c}")
        if i < len(p["callout"]) - 1:
            a(">")
    a("")
    a("## The path at a glance\n")
    a("Each stage ends with a checkpoint. Move on when you can do what the checkpoint says.\n")
    a("| Stage | Focus | About |")
    a("| --- | --- | --- |")
    for n, s in enumerate(p["stages"], 1):
        ex = " (plus planned modules)" if any(i.kind == "soon" for i in s["items"]) else ""
        a(f"| {n} | {s['name']} | {hours(sum(i.minutes for i in s['items']))}{ex} |")
    a("")
    for n, s in enumerate(p["stages"], 1):
        a(f"## Stage {n}: {s['name']}\n")
        extra = " plus the planned modules" if any(i.kind == "soon" for i in s["items"]) else ""
        a(f"{s['why']} ({hours(sum(i.minutes for i in s['items']))}{extra})\n")
        for it in s["items"]:
            a(f"- {item_line(it, rep)}")
        a("")
        a(f"**Ready to move on when:** {s['ready']}\n")
    a("## Skip-ahead rules\n")
    for r in p["skip"]:
        a(f"- {r}")
    a("")
    a("## Worked example: a week-by-week plan\n")
    a("*This example is invented, to show the method.*\n")
    a(f"{p['example_who']} spreads the path over {len(p['example'])} weeks. Each week ends with something you can show. {p.get('example_note', '')}".strip() + "\n")
    a("| Week | Stage | What you do |")
    a("| --- | --- | --- |")
    for w, st, what in p["example"]:
        a(f"| {w} | {st} | {what} |")
    a("")
    a("## Tradeoffs\n")
    for t in p["tradeoffs"]:
        a(f"- {t}")
    a("")
    a("## Failure modes\n")
    for f in p["failures"]:
        a(f"- {f}")
    a("")
    a("## Practitioner checklist\n")
    for c in p["checklist"]:
        a(f"- [ ] {c}")
    a("")
    a("## Under the hood: how this path was built\n")
    a(f"Lesson links come from the track build configs, so a renamed lesson is caught by the link check. Time is the number of lessons times {FLAT_MIN} minutes for a reading lesson, "
      f"times {HARNESS_MIN} minutes for a harness lesson that you build, and {SKIM_MIN} minutes to skim a harness phase. Add time for exercises. "
      "Modules marked \"coming soon\" are planned and not counted.\n")
    a("## Related lessons\n")
    names = {x["slug"]: x["short"] for x in PATHS}
    for r in p["related"]:
        a(f"- [{names[r]} path](./{r}.md)")
    a("- [Choose your path](./README.md)")
    a("- [Recap: paths compared](./recap.md)")
    a("")
    a("## Sources\n")
    a("Lesson counts and titles come from the track overview pages and build configs in this repository. "
      "The time estimates are this course's rule of thumb, not measured results. The week plan is invented.\n")
    text = "\n".join(L)
    defs = [("LLM", "a large language model (LLM) is a model like those behind chat assistants; the plural is large language models (LLMs)"),
            ("ML", "machine learning (ML) is the practice of training models from data"),
            ("CNN", "convolutional neural networks (CNNs) are a model type built for images"),
            ("XML", "Extensible Markup Language (XML) is a tag-based text format")]
    import re as _re
    used = [d for k, d in defs if _re.search(r"\b%ss?\b" % k, text)]
    if used:
        text = text.replace("\n> 🎯", "\n**Terms:** " + "; ".join(used) + ".\n\n> 🎯", 1)
    return text


def matrix_rows():
    rows = []
    tracks = list(NAMES) + ["content", "harness", "flowable"]
    labels = dict(NAMES, content="AI engineering stack (content/)", harness="Harness engineering", flowable="Flowable")
    for t in tracks:
        cells = []
        total = None
        any_in = False
        for p in PATHS:
            seen, tot = set(), 0
            for s in p["stages"]:
                for it in s["items"]:
                    if it.key == t:
                        seen.add((it.line, it.count)); tot = it.total
            if not seen:
                cells.append("—")
                continue
            any_in = True
            n = sum(c for _, c in seen)
            if t == "flowable":
                cells.append("Overview")
            elif t == "harness":
                skim = any("skim" in line for line, _ in seen)
                cells.append(f"{n} of {tot} lessons" + (" (part skim)" if skim else ""))
            else:
                cells.append("Full" if n >= tot else f"{n} of {tot}")
        if any_in:
            rows.append((labels[t], cells))
    return rows


def render_hub():
    L = []
    a = L.append
    a("# Learning paths\n")
    a("*Part of the [Generative AI family](../GENERATIVE_AI_ROADMAP.md)*\n")
    a(f"{STAMP}\n")
    a("This library has more than twenty tracks. You do not need all of them. "
      "A learning path picks the tracks and the lessons for one role, puts them in order, and says when to move on.\n")
    a("**A note on scope.** The paths do not teach anything new. They order and explain the lessons that already exist, "
      "and they say which lessons to skip. The lessons carry the content. Modules on machine learning, tensors and CNNs are planned. "
      "They show as \"coming soon\" until they are published.\n")
    a("## Pick your role\n")
    a("| Path | Who it is for | Outcome | Length |")
    a("| --- | --- | --- | --- |")
    for p in PATHS:
        a(f"| [{p['short']}](./{p['slug']}.md) | {p['who'][0].upper() + p['who'][1:]} | {p['outcome']} | {hours(minutes_of(p['stages']))} |")
    a("")
    a("## Where the depth lives\n")
    a("Each path page lists its lessons by stage. The tracks hold the depth. "
      "This table shows which path reads how much of each track. The [recap](./recap.md) has the full matrix.\n")
    a("| If you want the full depth on | Read |")
    a("| --- | --- |")
    a("| Models, tokens and context windows | [LLMs](../llms/README.md) |")
    a("| Grounding a model in your data | [RAG & vector databases](../rag-vector-databases/README.md) |")
    a("| Building an agent by hand | [Harness engineering](../harness-engineering/README.md) |")
    a("| Quality, safety and cost | [Evaluation & observability](../evaluation-and-observability/README.md), [AI security & guardrails](../ai-security-and-guardrails/README.md), [Cost optimization](../cost-optimization/README.md) |")
    a("| The product craft | [Technical product management](../technical-product-management/README.md) |")
    a("")
    a("## How a path works\n")
    a("- **Stages.** Each path has four or five stages. A stage has a short reason, the lessons to read, and a checkpoint.")
    a("- **Checkpoints.** A checkpoint is something you can do or explain. If you cannot, read the stage again.")
    a("- **Skip-ahead rules.** Each page says what to skip if you already know a topic.")
    a("- **Time.** Estimates are rough. A reading lesson is about 25 minutes. A harness lesson that you build is about an hour.")
    a("- **Not sure where to start?** For the harness track, the `/find-your-level` skill runs a short placement quiz. For the rest, start at stage 1 of your path and use the skip-ahead rules.")
    a("")
    a("## If you wear two hats\n")
    a("Read the path for the job you are in now. Add stages from the other path when a task needs them. "
      "A product lead working with an agent team can add the agent stage of the engineer path. An engineering lead who writes code can add the build stages.\n")
    a("**📌 Close out:** [Recap: paths compared](./recap.md), which ends with a self-test.")
    a("")
    return "\n".join(L)


def render_recap():
    L = []
    a = L.append
    a("# Learning paths: recap\n")
    a("*Part of [Learning paths](./README.md)*\n")
    a("## The paths in one view\n")
    a("| Path | Starts with | Spends the most time on | Ends with |")
    a("| --- | --- | --- | --- |")
    a("| [Senior PM](./senior-product-manager.md) | A technical footing | The decisions only the PM owns | Optional depth where the roadmap needs it |")
    a("| [AI Product Lead](./ai-product-lead.md) | Model and data foundations | Context, agents, and trust | Running the product |")
    a("| [AI Engineer](./ai-engineer.md) | LLM basics (machine learning when published) | Agents and the harness | Production |")
    a("| [AI Engineering Lead](./ai-engineering-lead.md) | Model behaviour and cost | Quality, safety and access | Working with product |")
    a("")
    a("## Which path reads how much of each track\n")
    a("\"Full\" means every lesson. A number means that many lessons out of the track's total. A dash means the path skips the track.\n")
    a("| Track | Senior PM | AI Product Lead | AI Engineer | AI Engineering Lead |")
    a("| --- | --- | --- | --- | --- |")
    for name, cells in matrix_rows():
        a(f"| {name} | " + " | ".join(cells) + " |")
    a("")
    a("## What the paths share\n")
    a("Three of the four paths read the evaluation, security and cost lessons. The PM reads them to make the call. "
      "The product lead and the engineering lead read them to set the standard. "
      "The AI engineer meets the same ideas by building them, in the harness track and the AI engineering stack.\n")
    a("## Test yourself\n")
    qs = [
        ("You are a senior PM with a launch in two weeks. Which stage do you do first, and why?",
         "Stage 3, the decisions. It covers the eval plan, cost and risk, which a launch needs. Read stage 1 and 2 later. Each stage's checkpoint shows what you missed.",
         "senior-product-manager"),
        ("What is the difference between the AI Product Lead path and the Senior PM path?",
         "The lead path is wider and deeper on the layers between a model and a product: grounding, context, memory, agents, workflows, trust and cost. It assumes the PM path or equivalent.",
         "ai-product-lead"),
        ("Why does the AI Engineer path put the harness lessons in the middle and not at the start?",
         "You need models, APIs and grounding first. The harness lessons build an agent from those parts, so they need them.",
         "ai-engineer"),
        ("An engineering lead skims the harness phases. What do they lose, and what do they keep?",
         "They lose the failures you only meet by typing the code. They keep the shape of each part: the loop, tools, permissions, budgets and failure handling, which is what a design review needs.",
         "ai-engineering-lead"),
        ("What is a checkpoint, and what do you do if you cannot meet it?",
         "A checkpoint is something you can do or explain at the end of a stage. If you cannot meet it, read the stage again before you move on.",
         "senior-product-manager"),
    ]
    for i, (q, ans, slug) in enumerate(qs, 1):
        a(f"{i}. **{q}**")
        a(f"   <details><summary>Answer</summary>{ans} (<a href=\"./{slug}.md\">Path page</a>)</details>")
    a("")
    a("## Sources\n")
    a("Lesson counts come from the track build configs in this repository. The time estimates are a rule of thumb, not measured.\n")
    a("---\n")
    a("← Back to [Learning paths](./README.md)")
    a("")
    return "\n".join(L)


def main():
    os.makedirs(OUT, exist_ok=True)
    for p in PATHS:
        open(f"{OUT}/{p['slug']}.md", "w", encoding="utf-8").write(render_path(p))
    open(f"{OUT}/README.md", "w", encoding="utf-8").write(render_hub())
    open(f"{OUT}/recap.md", "w", encoding="utf-8").write(render_recap())
    for p in PATHS:
        print(p["slug"], hours(minutes_of(p["stages"])), sum(1 for s in p["stages"] for i in s["items"] if i.kind != "soon"), "groups")


if __name__ == "__main__":
    main()
