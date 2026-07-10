# Interview Guide

The goal is to show judgment, not recite a tool list. Use this answer structure
for every project:

1. **Problem:** the failure or guarantee the project addresses.
2. **Decision:** the design choice you made and why.
3. **Evidence:** the test, artifact, or runnable failure scenario.
4. **Boundary:** what is local or simulated.
5. **Production change:** the first thing you would harden.

## Portfolio Pitch

### 30 seconds

I built local-first data and ML systems around the guarantees that usually make
production platforms difficult: temporal correctness, idempotency, contracts,
evaluation gates, lineage, replay, and observability. I use deterministic
synthetic data so a reviewer can run the workflows quickly. I distinguish the
local implementation from service-backed integrations and production migration
options instead of claiming the projects are production systems.

### When asked whether they are production-ready

No. They are production-style portfolio systems. The local guarantees are
implemented and tested, but most have not been operated under multi-tenant
traffic, real sensitive data, security review, load, cost pressure, or on-call
conditions. I can explain exactly which components are real, which are
simulated, and what I would harden first.

## 1. Lakehouse Data Platform

**Scope:** local event ingestion through raw, bronze, silver, gold, and serving
tables, with quality, backfill, lineage, and run metadata.

**Best story:** source fingerprints and event IDs make ingestion idempotent;
row-count and revenue reconciliation then prove that the model graph did not
silently lose or duplicate facts.

**Evidence:** six tests cover the happy path, source idempotency, dead-letter
handling, schema evolution, and multi-partition backfill. `make demo` builds 11
models and a serving SQLite database.

**Tradeoff:** the local SQL runner and SQLite path make review fast. MinIO,
Redpanda, Postgres, dbt, and Airflow are currently migration or orchestration
examples, not one integrated runtime.

**Questions to prepare for:**

- How would a backfill avoid double counting?
- Which checks should block publication versus only alert?
- Why use both medallion layers and a dimensional model?
- How would you partition files and tables at larger scale?
- How would the design map to S3 plus Snowflake or Databricks?

## 2. Feature Store And Inference

**Scope:** historical feature materialization, point-in-time training joins,
online feature state, parity checks, simulated streaming updates, scoring, and
rollback.

**Best story:** a label row may only see feature events at or before its event
time. The point-in-time test injects future data and proves the join excludes it;
the parity test compares offline and materialized online values.

**Evidence:** seven tests cover temporal correctness, parity, streaming
idempotency, late events, prediction logging, and registry rollback.

**Tradeoff:** the default store is SQLite/JSON with optional Redis access. The
current container executes a finite demo rather than serving the FastAPI app,
and local sub-millisecond latency is not a production benchmark.

**Known demo issue:** the current scenario makes most stream events late and
promotes a weak synthetic model. Fix the event ordering, freshness scenario, and
promotion boundary before using this as a flagship demo.

**Questions to prepare for:**

- What exactly causes point-in-time leakage?
- How do you version feature definitions independently of models?
- What is the fallback behavior when Redis is unavailable?
- How do you make online writes idempotent across consumers?
- What compatibility check happens before model promotion?

## 3. MLOps Lifecycle

**Scope:** deterministic data splits, training, validation, candidate
registration, evaluation gates, champion promotion, batch/online scoring,
monitoring, and rollback.

**Best story:** registration and promotion are separate state transitions. A
candidate remains available for audit even when one gate fails, but the
champion pointer cannot move unless every required gate passes.

**Evidence:** seven tests cover reproducible splits, promotion blocking,
successful promotion, rollback, batch scoring, online scoring, and monitoring
artifacts. Eight gates cover data quality, model quality, segment gap, size, and
latency.

**Tradeoff:** experiment tracking and registry semantics are file-backed. The
FastAPI module exists, but `make serve` is a scoring smoke rather than a
long-running server. Say this plainly.

**Questions to prepare for:**

- Which gates are blocking, advisory, or manually approved?
- How do you prevent test-set overfitting through repeated promotion?
- What is the difference between rollback and retraining?
- How would MLflow aliases and deployment state remain consistent?
- Why is drift based on one online prediction statistically meaningless?

## 4. Data Observability And Lineage

**Scope:** contracts, freshness and schema checks, incident deduplication,
root-cause categories, transitive lineage impact, and alert-ready artifacts.

**Best story:** a deterministic incident key prevents the same failed check from
creating repeated incidents, while lineage separates the upstream cause from
all downstream datasets and business assets it affects.

**Evidence:** six tests cover freshness, schema drift, duplicate incident
prevention, downstream tables, downstream assets, and report generation. The
demo intentionally produces a mixed healthy/broken estate.

**Tradeoff:** dbt and OpenLineage metadata are ingested from local files;
Marquez/Postgres in Compose are not yet the live metadata backend.

**Questions to prepare for:**

- How is incident severity derived and routed?
- How do you avoid blaming every downstream table independently?
- What happens when lineage is incomplete or stale?
- How would you measure mean time to detect and recover?
- Which checks belong inline versus in a scheduled observability sweep?

## 5. RAG Evaluation Pipeline

**Scope:** versioned document ingestion, hashing and deduplication, chunking,
deterministic embeddings, hybrid retrieval, cited answers, and evaluation.

**Best story:** dataset and embedding versions become part of the index identity,
so retrieval regressions can be attributed to a specific corpus, chunking, or
embedding change rather than an untraceable prompt edit.

**Evidence:** eight tests cover versioned ingestion, indexing, filters, retrieval,
evaluation artifacts, citations/logging, retrieval fallback, and a live HTTP
smoke path.

**Tradeoff:** the answer generator and faithfulness checks are deterministic
heuristics. Qdrant/pgvector and hosted models are production mappings. The
current three-document, three-question corpus only proves the harness works; it
does not establish RAG quality.

**Questions to prepare for:**

- How would you create hard negatives and prevent evaluation leakage?
- Why can recall rise while answer quality falls?
- How do chunk size, overlap, hybrid weighting, and reranking interact?
- How would document ACLs propagate to chunks and citations?
- What signals should trigger abstention rather than generation?

## 6. Streaming Fraud And Anomaly

**Scope:** deterministic transaction generation, schema validation,
event-time windows, watermarks, deduplication, heuristic scoring, DLQ, replay,
and alert suppression.

**Best story:** at-least-once delivery is converted into effectively-once
business alerts by separating event deduplication from alert deduplication and
using stable identifiers at both boundaries.

**Evidence:** seven tests cover duplicates, late events, bad schemas, poison
messages, explainable scoring, alert deduplication, and metric generation.

**Tradeoff:** local JSONL files are Kafka-shaped topics, and scoring is a rule
plus deterministic heuristic rather than a validated fraud model. Local loop
throughput is not an end-to-end streaming benchmark.

**Questions to prepare for:**

- Why use event time rather than processing time?
- How do watermark and allowed lateness affect correctness and latency?
- When should a late event go to correction rather than DLQ?
- What state must survive a consumer rebalance or replay?
- What would exactly-once require across Kafka and the alert sink?

## 7. ELT Connector Framework

**Scope:** source abstraction, cursor state, pagination, retry and rate-limit
handling, schema inference, drift policy, quarantine, destination writes, and
run metadata.

**Best story:** checkpoint advancement is part of the destination commit
boundary. If validation or loading fails, the prior cursor remains durable so a
retry cannot skip source records.

**Evidence:** seven tests cover full and incremental behavior, pagination,
retry/rate limits, schema drift, quarantine, idempotent upsert, and checkpoint
advancement.

**Tradeoff:** sources are fake APIs and local CSV; there is no OAuth, CDC,
distributed scheduler, or warehouse destination. That is why it is a connector
mechanics lab, not an Airbyte replacement.

**Questions to prepare for:**

- What consistency boundary includes the destination and checkpoint?
- How do append and upsert change idempotency?
- How should breaking versus additive drift be handled?
- How do you resume a paginated source after a mid-page failure?
- When would you choose managed Airbyte or Fivetran instead?

## Closing Rule

Never defend breadth by listing more tools. Pick one tested guarantee, walk
through the state transition and failure mode, then explain the production
boundary. That is the most senior version of each project.
