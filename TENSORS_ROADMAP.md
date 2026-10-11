# Tensors: module plan

> **Status:** built and registered; fact-check in progress. Plan written 2026-10. See the status table at the end.

The second foundation module, after [machine learning](./MACHINE_LEARNING_ROADMAP.md) and before convolutional networks. It follows the same dual altitude: a leader briefing in every lesson, plus one runnable standard-library example that ends in `assert` lines.

## Decisions

| Decision | Choice |
| --- | --- |
| Audience | Product and technology leaders. Engineers get the Under the hood sections. |
| Shape | 5 lessons and a recap. Each lesson has a worked example, an Under the hood section with code that runs, a diagram, a checklist and Sources. |
| Code | Python standard library only. A small `Tensor` class teaches the mechanics. An optional NumPy check runs only when NumPy is installed. |
| Running thread | The churn data and `TinyNet` from the machine learning module. The tensor code rebuilds its forward pass as matrix multiplications and its gradients with a small autograd. |
| Out of scope | Transformers and serving (`llms`, `content/01-inference-internals`), convolutions (next module), writing PyTorch. |

## The overlap gate

Per `CONTENT_FRAMEWORK.md` section 7.

| Neighbour | What it already covers | Delta in this module |
| --- | --- | --- |
| `content/01-inference-internals` (quantization, KV cache, batching, prefill vs. decode) | Serving memory and speed. | The vocabulary underneath (shape, rank, dtype, bytes) and training memory by pile. Links out for serving. |
| `machine-learning` lessons 3 and 6 | The training loop and a hand-written backward pass. | How a library does it: matrix multiplication as the layer, then automatic differentiation. |
| `llms/what-is-an-llm` | What an LLM is. | Where the numbers live. One link, no model internals. |
| `first-principles`, `generative-ai` | Not tensors. | None. |

## The lessons

| # | Lesson | The question it answers | Runnable file |
| --- | --- | --- | --- |
| 1 | What a tensor is: shape, rank and dtype | What is the object every model works on, and how big is it in bytes? | `lesson1_shapes.py` |
| 2 | Operations and broadcasting | Why do shape errors cause most framework bugs? | `lesson2_broadcasting.py` |
| 3 | Matrix multiplication: the workhorse | What does a layer cost, and why does one big multiply beat many small ones? | `lesson3_matmul.py` |
| 4 | Batching, memory and precision | Will it fit, and what do the number formats trade? | `lesson4_memory.py` |
| 5 | Automatic differentiation | How does a library get the gradient with no hand-written rules? | `lesson5_autograd.py` |

## Sources to use

Primary sources only, each with an "as of" date: the NumPy and PyTorch documentation (broadcasting, copies and views, autograd mechanics); Micikevicius et al., *Mixed Precision Training* (ICLR 2018); Rajbhandari et al., *ZeRO* (2020); Kalamkar et al. on bfloat16 (2019) and Google's bfloat16 description; NVIDIA's Matrix Multiplication Background guide; Kaplan et al., *Scaling Laws for Neural Language Models* (2020); Baydin et al., *Automatic differentiation in machine learning: a survey* (JMLR 2018); Goodfellow, Bengio and Courville, *Deep Learning* (2016). Numbers in worked examples come from the code and are labelled invented. No unsourced statistics.

## Wiring

- Track build: `scripts/build_tensors.py`, output `tensors-html/`.
- Registration: `build_site.py` (constant, copy, landing card, link rewrite), `build_html.py` FLAT, `check_links.py` SCAN_DIRS, `build_graph.py` TRACKS and FLAT_TRACKS, `build_glossary.py`, `check_module.py` VOLATILITY (medium), `CONTENT_FRAMEWORK.md` freshness table, `SUMMARY.md`, `README.md`, `SITE_QUALITY_ROADMAP.md`.
- Glossary: about 25 terms.
- Diagrams: one hand-built figure per lesson, plus the README opener.
- Forward links: the machine learning module now links here.
- Learning paths: the AI Engineer path reads all five lessons. The AI Engineering Lead path reads lessons 1, 3 and 4.

## Verification

`check_links.py` and `check_design_system.py` pass. `check_module.py tensors` passes. `python3 tensors/code/test_examples.py` passes, and `numpy_check.py` agrees with NumPy when it is installed. The pages render in light and dark at 390 and 1280 px. An independent agent fact-checks the lessons (claim, location, primary source, verdict). Every `WRONG` or `STALE` row is fixed, and the agent is run again on the fixed files.

## Status

| Step | State |
| --- | --- |
| Plan | Done |
| Code and tests | Done: 5 lesson files, a shared `tensor.py`, an optional NumPy check, one test runner |
| Lessons, README, recap | Done: 5 lessons, README, recap with 12 test-yourself questions |
| Diagrams and glossary | Pending |
| Registration and learning paths | In progress |
| Independent fact-check | Pending |
