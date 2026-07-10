# Recruiter Guide

## The Portfolio In One Sentence

I built a local-first portfolio of data and ML systems that demonstrates the
engineering guarantees behind production platforms: idempotency, temporal
correctness, data contracts, model gates, lineage, evaluation, replay, and
failure recovery.

These are production-style portfolio projects built with deterministic
synthetic data. They are not claims of operating production workloads.

## What To Review First

The portfolio should be read as three flagship stories and four supporting
labs, not seven equal products.

| Story | Repository | What It Proves | Current Boundary |
| --- | --- | --- | --- |
| Analytics Data Platform | [Lakehouse Data Platform](https://github.com/kevinmeix1/lakehouse-data-platform) | Medallion modeling, dimensional marts, idempotent ingestion, reconciliation, lineage, and backfills | The core path is local; Compose services are not yet the verified runtime |
| ML Feature Delivery | [Feature Store and Inference](https://github.com/kevinmeix1/feature-store-inference) | Point-in-time joins, offline/online parity, streaming update semantics, inference, and rollback | Redis, Feast, and MLflow are migration targets rather than the default exercised path |
| RAG Quality System | [RAG Evaluation Pipeline](https://github.com/kevinmeix1/rag-evaluation-pipeline) | Versioned ingestion, hybrid retrieval, citations, retrieval evaluation, and an HTTP query path | The evaluation corpus is intentionally small and does not establish production RAG quality |

The supporting projects isolate reusable concerns:

- **MLOps Lifecycle:** evaluation gates, promotion, registry state, and rollback.
- **Data Observability:** contracts, incident deduplication, lineage impact, and
  root-cause classification.
- **ELT Connector Framework:** pagination, incremental state, retry, schema
  drift, and quarantine.
- **Streaming Fraud:** event-time windows, watermarks, DLQ, replay, scoring, and
  alert deduplication in a deterministic simulator.

## Thirty-Second Explanation

> I built these projects to show practical engineering judgment across the data
> and ML lifecycle. The strongest examples are a Lakehouse pipeline, a temporal
> feature and inference system, and a RAG evaluation pipeline. Each has
> deterministic tests for hard guarantees such as idempotency, point-in-time
> correctness, parity, rollback, and retrieval regression. I explicitly label
> local implementations, service-backed integrations, and production migration
> designs so the repositories do not claim operational scale they have not run.

## Role-Specific Framing

| Role | Lead Project | Supporting Project | Positioning |
| --- | --- | --- | --- |
| Data Engineer | Lakehouse | ELT or Observability | Reliable ingestion through modeled serving tables, with recovery and data contracts |
| Analytics Engineer | Lakehouse | Observability | Dimensional modeling, reconciliation, tests, lineage, and downstream impact |
| ML Engineer | Feature Store | MLOps Lifecycle | Temporal feature correctness through governed model delivery and rollback |
| MLOps Engineer | Feature Store plus MLOps as one story | Observability | Promotion gates, version compatibility, serving behavior, monitoring, and incidents |
| AI/LLM Engineer | RAG Evaluation | Lakehouse or Observability | RAG quality as a versioned data and evaluation problem, not only a prompt problem |
| Solution Architect | Lakehouse | Feature Store and Observability | Boundaries, contracts, failure modes, migration paths, and operational tradeoffs |

Do not list all seven on one CV. Choose one flagship and one or two supporting
projects that match the role.

## Public Evidence

- All repositories are public and linked from the
  [portfolio index](https://github.com/kevinmeix1/data-ml-engineering-portfolio).
- The index runs 48 deterministic domain tests across all seven repositories in
  a public GitHub Actions workflow.
- Every project produces a local dashboard artifact and documents its generated
  evidence.
- Only one child repository currently has its own CI, and none yet proves a full
  service-backed Compose transaction in CI. Those are roadmap items, not hidden
  claims.

## Suggested GitHub Pins

For a general data and ML profile, pin these in order:

1. `data-ml-engineering-portfolio`
2. `lakehouse-data-platform`
3. `feature-store-inference`
4. `rag-evaluation-pipeline`

Use `streaming-fraud-anomaly` as an additional pin for streaming roles. Keep the
MLOps, Observability, and ELT repositories linked from the index until their best
capabilities are integrated into the flagships.

## What A Technical Interviewer Can Ask

The portfolio is strongest when the conversation focuses on one guarantee and
one failure path:

- How does an ingestion retry avoid duplicate facts?
- How does a point-in-time join prevent training leakage?
- What prevents a failed model candidate from becoming champion?
- How is one upstream failure separated from many downstream symptoms?
- How does an index or corpus change become a measurable RAG regression?
- How do event deduplication and alert deduplication differ during replay?
- When is a connector checkpoint safe to advance?

The detailed answers and project-specific tradeoffs are in the
[Interview Guide](interview-guide.md).

## Language That Preserves Credibility

Use:

- local-first
- production-style portfolio project
- deterministic simulator
- service-backed integration when it is actually exercised
- production mapping or migration path for design-only components

Avoid:

- production-grade
- enterprise-ready
- internet-scale
- real-time for a local file loop
- tool-based labels when the named service is not executed by the demo

The portfolio's senior signal is the ability to define a guarantee, prove it,
show its failure behavior, and state what remains before production.
