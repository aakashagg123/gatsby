"""The landing page: four sequenced pillars with a Start-here row.

Card copy lives in CARDS (one entry per track, keyed by its site folder). PILLARS says where
each track sits. Pillar II cards also carry a depth badge that the build measures from the
markdown, so the label cannot drift from the content:

  Deep spec     runnable Python in at least half of the track's lessons
  PM summary    concepts and decisions, no runnable code (or very little)

build_site.py calls render() with the live graph counts.
"""
import html as htmllib
import os
import re

import design_system as ds

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEEP_SHARE = 0.5   # share of lessons with a ```python block that makes a track a deep spec

CARDS = {'ai': {'title': 'AI engineering',
        'blurb': 'The engineering discipline under production LLM systems — inference, retrieval, evals, '
                 'observability, safety, cost. Designed reading editions.'},
 'harness': {'title': 'Harness engineering',
             'blurb': "Build a coding agent's harness from scratch — loop, tools, context, permissions, "
                      'subagents — then use the real SDK. 10 phases, 41 lessons, one tested capstone.'},
 'flowable': {'title': 'Flowable',
              'blurb': 'Process automation from scratch — build a token engine, wait states, and a job '
                       'executor by hand, then run real BPMN on the Flowable engine. Concept-first for PMs, '
                       'with a build layer for engineers.'},
 'first-principles': {'title': 'First principles',
                      'blurb': 'Reason from fundamentals and build range across disciplines — the method, a '
                               'latticework of mental models, becoming a polymath, and learning how to '
                               'learn.'},
 'product-sense': {'title': 'Product sense',
                   'blurb': 'The instinct for what makes a product succeed, for APMs & PMs moving into AI PM '
                            '— motivation, empathy, creativity, communication, domain expertise, and product '
                            'sense for AI.'},
 'technical-product-sense': {'title': 'Technical product sense',
                             'blurb': 'Read systems like an engineer — architecture, APIs, data, latency, '
                                      'reliability, and tech debt — with a diagram in every lesson. For APMs '
                                      '& PMs moving into AI PM.'},
 'technical-product-management': {'title': 'Technical product management',
                                  'blurb': 'The operating discipline of shipping — the role, specs, '
                                           'prioritization, execution, metrics, and releases — with a '
                                           'diagram in every lesson. For APMs & PMs moving into AI PM.'},
 'agentic-ai': {'title': 'Agentic AI',
                'blurb': 'What agents actually are — the loop, tools, memory, planning — plus reliability, '
                         'security, and economics. Opens with a knowledge graph; a diagram in every lesson.'},
 'knowledge-graphs': {'title': 'Knowledge graphs',
                      'blurb': 'Treat what the company knows as a product — entities and ontologies, the '
                               'construction pipeline, GraphRAG, governance, and the business case, in '
                               'product leader language.'},
 'machine-learning': {'title': 'Machine learning',
                      'blurb': 'What a learned system is, what it learns from, how it learns, how to trust '
                               'its score, which model family to pick, and how to keep it working after '
                               'launch. Runnable code in every lesson.'},
 'tensors': {'title': 'Tensors',
             'blurb': 'What the objects every model works on are, what they cost in memory and compute, why '
                      'shape errors are silent, and how a library gets the gradient for free. Runnable code '
                      'in every lesson.'},
 'cnns': {'title': 'Convolutional networks',
          'blurb': 'How a vision model sees, what resolution and depth cost, when to reuse a pre-trained or '
                   'foundation model, and why vision features break in production. Runnable code in three '
                   'lessons.'},
 'transformers': {'title': 'Transformers',
                  'blurb': 'The stack behind almost every language model: attention, the block, position and '
                           'the cost of context, the KV cache, and reading a model card as memory, compute '
                           'and cost. Runnable code in every lesson.'},
 'ai-assisted-development': {'title': 'AI-assisted development for leaders',
                             'blurb': 'What changes when a coding agent writes the code: specifying, '
                                      'verifying, controlling and measuring the work. Runnable code in every '
                                      'lesson, including a real Stop-hook script.'},
 'fine-tuning': {'title': 'Fine-tuning and post-training',
                 'blurb': 'How a base model becomes an assistant, what supervised tuning, LoRA and '
                          'preference tuning change, why the dataset is the product, and how to test the '
                          'break-even and gate the release. Runnable code in every lesson.'},
 'generative-ai': {'title': 'Generative AI: the big picture',
                   'blurb': 'What makes AI "generative," the five modalities, why output is probabilistic, '
                            'the four-layer product stack, and build vs. buy vs. fine-tune. Opens the '
                            'Generative AI family.'},
 'llms': {'title': 'LLMs',
          'blurb': 'Tokens, the context window, the jagged frontier, prompting, sampling, choosing a model, '
                   'and the order to reach for prompting, RAG, or fine-tuning.'},
 'api-integrations': {'title': 'APIs & integrations',
                      'blurb': 'The request/response contract, authentication, rate limits, streaming, '
                               'retries, structured output, webhooks, and fitting a model call into a real '
                               'system.'},
 'rag-vector-databases': {'title': 'RAG & vector databases',
                          'blurb': 'Grounding models in your data — when to use RAG and when not to, '
                                   'embeddings, vector databases, chunking, retrieval quality, and a '
                                   'hands-on build with Claude Code and pgvector.'},
 'memory-and-context': {'title': 'Memory & context',
                        'blurb': 'Memory as a product decision, the three shapes it takes, how memories are '
                                 'written and kept, the designs for reading them back, and the trust '
                                 'failures it has to be designed against.'},
 'tool-calling': {'title': 'Tool calling',
                  'blurb': 'The line where an AI product stops talking and starts doing: designing a tool '
                           'worth trusting, and keeping the permission boundary around it real.'},
 'ai-agents': {'title': 'AI agents',
               'blurb': 'The loop behind every agent, how much autonomy a task needs, what keeps it reliable '
                        'across many steps, when not to build one, how to run one safely, and how to choose '
                        'one.'},
 'agentic-workflows': {'title': 'Agentic workflows',
                       'blurb': 'Choosing a workflow pattern, when more than one agent earns its cost, and '
                                'what it takes to make a workflow durable enough to own end to end.'},
 'evaluation-and-observability': {'title': 'Evaluation & observability',
                                  'blurb': 'Why the eval set is the product spec for a non-deterministic '
                                           'system, and the order to actually build the eval and '
                                           'observability stack in.'},
 'ai-security-and-guardrails': {'title': 'AI security & guardrails',
                                'blurb': 'Jailbreak, injection, extraction, and poisoning are four different '
                                         'attacks. How to test your defenses, and how governance becomes '
                                         'compliance evidence a regulator or buyer can check.'},
 'cost-optimization': {'title': 'Cost optimization',
                       'blurb': 'Which lever fixes which cost driver, the build-vs-buy breakeven done as '
                                'arithmetic, and the FinOps practice that turns attribution into governance '
                                'before the invoice, not after.'},
 'system-design': {'title': 'System design',
                   'blurb': 'How real systems are designed at scale — from rate limiters to stock exchanges '
                            '— with the architecture, tradeoffs, and failure modes that shape product '
                            'decisions. 28 systems plus lessons on distributed data, caching, ML and GenAI '
                            'systems, social media and reliability, a question bank and runnable code, '
                            'diagrams included.'},
 'access-control': {'title': 'Access control',
                    'blurb': 'Who may do what, and where that is decided: authentication vs authorization, '
                             'OAuth and tokens, RBAC, ABAC, relationship-based access, Keycloak, and access '
                             'control for AI agents. 8 lessons.'},
 'context-engineering': {'title': 'Context engineering',
                         'blurb': 'Treat what the model gets to see as a product decision — instructions, '
                                  "retrieval, memory, and live state, spec'd, governed, and evaluated with "
                                  'the same rigor as the output it produces.'},
 'prompt-engineering': {'title': 'Prompt engineering',
                        'blurb': 'The craft of writing input a model will reliably act on — from ChatGPT '
                                 'productivity patterns, through few-shot and chain-of-thought, into the '
                                 'prompts that drive Claude Code and other coding agents. 10 lessons.'},
 'business-acumen': {'title': 'Business acumen',
                     'blurb': 'Money, markets, organizations and influence for Group PMs, Heads of Product '
                              'and VPs — grounded in FinTech, Payments, Lending, eCommerce, InsurTech and '
                              'Retail. 15 lessons and an interactive self-assessment with a radar chart and '
                              'an improvement plan.'},
 'graph': {'title': 'Knowledge graph',
           'blurb': 'Every page across all __TRACKS__ tracks as one interactive map — __NODES__ pages, __LINKS__ '
                    'cross-references. Search it, filter by track, click any node to jump in.'}}

START = [
    ("Engineer", "I build AI systems", "harness/index.html",
     "Start with Harness engineering and write a coding agent's loop, tools and permissions by hand. "
     "Then take the AI Engineer path for retrieval, evals and cost.",
     "learning-paths/ai-engineer.html", "AI Engineer path"),
    ("Product leader", "I own AI features", "learning-paths/senior-product-manager.html",
     "Start with the Senior PM path. Read the PM summaries in Pillar II first, "
     "and open a deep spec when your engineers say something you cannot check.",
     "learning-paths/ai-product-lead.html", "AI Product Lead path"),
]

# (pillar number, title, lede, [(group title or None, note, [track keys])], compact?)
PILLARS = [
    ("I", "Build from scratch",
     "Three tracks you cannot get from a slide deck. You write the code, run it, and read the tests.",
     [(None, [("harness", "Flagship build"), ("flowable", "Flagship build"), ("ai", "Reading edition")])], False),
    ("II", "Core LLM and agent architecture",
     "The reference for how models, agents, context and guardrails fit together. "
     "Several topics appear twice on purpose: once as a PM summary, once as a deep spec. "
     "Each card says which.",
     [("Model foundations", ["generative-ai", "llms", "transformers", "fine-tuning", "machine-learning", "tensors", "cnns"]),
      ("Agents and workflows", ["agentic-ai", "ai-agents", "agentic-workflows", "tool-calling", "ai-assisted-development"]),
      ("Context and knowledge", ["context-engineering", "memory-and-context", "knowledge-graphs", "rag-vector-databases"]),
      ("Ship it safely", ["ai-security-and-guardrails", "evaluation-and-observability", "cost-optimization", "api-integrations"])],
     False),
    ("III", "Distributed systems foundations",
     "The systems knowledge every AI design review leans on: scale, latency, reliability and access.",
     [(None, ["system-design", "technical-product-sense", "access-control"])], False),
    ("IV", "Product craft and mental models",
     "General product and thinking skills. Useful, but not AI-specific, so they sit last.",
     [(None, ["first-principles", "product-sense", "technical-product-management", "prompt-engineering", "business-acumen"])], True),
]


def lesson_files(key):
    d = os.path.join(ROOT, key)
    if not os.path.isdir(d):
        return []
    return [f for f in sorted(os.listdir(d))
            if f.endswith(".md") and f not in ("README.md", "recap.md")]


def depth(key):
    """(label, evidence) for a flat track, measured from its lessons."""
    files = lesson_files(key)
    if not files:
        return None
    n_code = 0
    for f in files:
        with open(os.path.join(ROOT, key, f), encoding="utf-8") as fh:
            if re.search(r"```python", fh.read()):
                n_code += 1
    if n_code / len(files) >= DEEP_SHARE:
        return ("Deep spec", "info", f"Runnable code in {n_code} of {len(files)} lessons")
    return ("PM summary", "secondary", "Concepts and decisions, little or no runnable code")


def _esc(s):
    return htmllib.escape(s, quote=False)


def card(key, tag=None, tag_color="secondary", foot=""):
    c = CARDS[key]
    href = "graph/index.html" if key == "graph" else f"{key}/index.html"
    badge = ds.badge(_esc(tag), color=tag_color, size="md", pill=True) if tag else ""
    foot_html = f'<span class="card-iw">{_esc(foot)}</span>' if foot else ""
    return (f'<a class="card" href="{href}">{badge}<h3>{_esc(c["title"])} →</h3>'
            f'<p>{_esc(c["blurb"])}</p>{foot_html}</a>')


def _pillar_head(num, title, lede):
    return (f'<section class="pillar" id="pillar-{num.lower()}" aria-labelledby="pillar-{num.lower()}-h">'
            f'<div class="group pillar-title"><span class="pillar-num">Pillar {num}</span>'
            f'<h2 id="pillar-{num.lower()}-h">{_esc(title)}</h2></div>'
            f'<p class="pillar-lede">{_esc(lede)}</p>')


def _twin_note(keys, depths):
    """One sentence per group that says which cards are the PM summary and which the deep spec."""
    pm = [CARDS[k]["title"] for k in keys if depths.get(k) and depths[k][0] == "PM summary"]
    deep = [CARDS[k]["title"] for k in keys if depths.get(k) and depths[k][0] == "Deep spec"]
    if not pm or not deep:
        return ""
    return f"PM summary: {', '.join(pm)}. Deep spec: {', '.join(deep)}."


def render(n_nodes, n_links, n_tracks):
    out = ['<main class="index landing">',
           "<h1>Supercharge your AI learning</h1>",
           '<p class="lede">Hands-on tracks for PMs and engineers moving into AI — from first principles to production.</p>',
           f'<div class="group">Start here {ds.text_link("Compare all four role paths →", "learning-paths/index.html", primary=True)}</div>',
           '<div class="cards start-here">']
    for tag, title, href, blurb, alt_href, alt_label in START:
        out.append(f'<a class="card" href="{href}">{ds.badge(_esc(tag), color="discovery", size="md", pill=True)}'
                   f'<h3>{_esc(title)} →</h3><p>{_esc(blurb)}</p>'
                   f'<span class="card-iw">Also: {_esc(alt_label)}</span></a>')
    out.append("</div>")

    depths = {}
    for num, title, lede, groups, compact in PILLARS:
        out.append(_pillar_head(num, title, lede))
        if num == "II":
            out.append('<p class="pillar-legend">'
                       f'{ds.badge("Deep spec", color="info", size="md", pill=True)} runnable code in at least half the lessons. '
                       f'{ds.badge("PM summary", color="secondary", size="md", pill=True)} concepts and decisions, little or no code.</p>')
        for group, items in groups:
            if group:
                keys = list(items)
                depths.update({k: depth(k) for k in keys})
                note = _twin_note(keys, depths)
                out.append(f'<h3 class="pillar-group">{_esc(group)}</h3>')
                if note:
                    out.append(f'<p class="pillar-note">{_esc(note)}</p>')
            if compact:
                out.append('<ul class="pillar-list">')
                for k in items:
                    out.append(f'<li><a class="TextLink" data-underline="" href="{k}/index.html">{_esc(CARDS[k]["title"])}</a>'
                               f' — <span>{_esc(CARDS[k]["blurb"])}</span></li>')
                out.append("</ul>")
                continue
            out.append('<div class="cards">')
            for it in items:
                if isinstance(it, tuple):                      # Pillar I: fixed tag
                    out.append(card(it[0], tag=it[1], tag_color="discovery" if "Flagship" in it[1] else "secondary"))
                    continue
                d = depths.get(it)
                if d:
                    out.append(card(it, tag=d[0], tag_color=d[1], foot=d[2]))
                else:
                    out.append(card(it, tag="Module"))
            out.append("</div>")
        out.append("</section>")

    out.append('<div class="group">Explore</div><div class="cards">')
    graph = dict(CARDS["graph"])
    blurb = graph["blurb"].replace("__NODES__", str(n_nodes)).replace("__LINKS__", str(n_links)).replace("__TRACKS__", str(n_tracks))
    CARDS["graph"] = {"title": graph["title"], "blurb": blurb}
    out.append(card("graph", tag="Explore"))
    CARDS["graph"] = graph
    out.append("</div>")
    out.append('<footer class="foot">Educational content. Use it, fork it, teach from it.</footer></main>')
    return "\n".join(out)
