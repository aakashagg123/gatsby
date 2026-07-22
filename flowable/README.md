<div align="center">

# Flowable — from scratch

**Understand process automation by building a tiny process engine by hand — then run the
same processes on the real Flowable engine.** Concept-first for PMs and architects, with a
technical build layer for engineers.

![Phases](https://img.shields.io/badge/phases-12-d97757?style=flat-square&labelColor=181818)
![Track](https://img.shields.io/badge/track-build%20it%20%2F%20use%20it-d97757?style=flat-square&labelColor=181818)

**[🗺️ Roadmap](./ROADMAP.md)** · **[🧭 Methodology](./METHODOLOGY.md)** · **[✍️ Authoring](./AUTHORING.md)** · **[📐 Ten Principles](./foundations/process-automation-principles.md)**

</div>

> This is a **separate track** from the Harness Engineering module. *Flowable* is an
> open-source business process automation platform (a 2016 fork of Activiti): a BPMN 2.0
> engine for structured processes, a CMMN engine for case management, a DMN engine for
> decisions, and an event registry for event-driven flows. Banks and fintechs run loan
> origination, KYC, and approval workflows on it. Here you learn the *execution model*
> underneath — tokens, wait states, transactions, jobs — by building it yourself, so the
> real engine is transparent when you use it.

## Audience — two layers, one track

- **PM / architect layer:** the `foundations/` spine and every **Concept** beat explain
  *when* and *why* — BPMN vs CMMN vs DMN, embed vs standalone, Flowable vs Camunda vs
  Temporal — with no code required.
- **Engineer layer:** every **Build It** implements the idea from scratch (Python
  standard library, ~80–150 lines), and every **Use It** runs the same thing on a real
  Flowable engine (Docker + REST, or embedded in Spring Boot).

Read only the Concept beats and you get a complete architecture course. Do the builds
and you can reason about the engine's behaviour from first principles.

## How it works

Each lesson runs the same six beats: **Motto → Problem → Concept → Build It → Use It →
Ship It**, then a short self-quiz. See [`METHODOLOGY.md`](./METHODOLOGY.md).

## Start here

- **Read the spine first:** [The Ten Principles of Process Automation](./foundations/process-automation-principles.md).
- **First worked lessons:**
  - [Tokens & sequence flow: a process engine in 100 lines](./phases/01-bpmn-and-the-token-model/01-tokens-and-sequence-flow/docs/en.md)
  - [Wait states & persistence: why the engine sleeps](./phases/02-the-engine-state-and-transactions/01-wait-states-and-persistence/docs/en.md)

## Status

Phases **1 (BPMN & the Token Model)**, **2 (The Engine: State & Transactions)**,
**4 (Service Integration & Error Handling)** and **5 (DMN: Decisions as Tables)** are
complete; the rest are scaffolded in the [Roadmap](./ROADMAP.md).

## Run the code

```bash
python3 flowable/phases/01-bpmn-and-the-token-model/01-tokens-and-sequence-flow/code/token_engine.py
```

To run the **Use It** beats you need a local Flowable instance:

```bash
docker run -p 8080:8080 flowable/flowable-rest
# REST API at http://localhost:8080/flowable-rest/service, default user rest-admin/test
```

<div align="center"><sub>Educational content. Use it, fork it, teach from it.</sub></div>
