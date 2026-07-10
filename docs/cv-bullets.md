# Evidence-Safe CV Bullets

Use two or three projects per application. Do not list all seven at equal
weight, and do not present local benchmark numbers as production results.

Use a bullet only after you can explain the implementation, reproduce its
evidence, and modify the relevant code without relying on a prepared script.
AI-assisted scaffolding is compatible with honest ownership; claiming behavior
you have not personally verified is not.

## Portfolio Summary

- Built and tested seven local-first data and ML engineering projects covering
  analytical pipelines, temporal features, model governance, data reliability,
  RAG evaluation, event-time processing, and incremental ELT; implemented 48
  deterministic domain tests and documented production boundaries.

Use this only when a broad portfolio summary is useful. A role-specific CV is
usually stronger with one flagship and one supporting project.

## Lakehouse Data Platform

- Built a local-first analytical pipeline with raw, bronze, silver, gold, and
  serving layers, including dimensional models, source-to-mart reconciliation,
  lineage artifacts, run metadata, and deterministic backfills.
- Implemented idempotent event ingestion using source fingerprints and event
  keys, with schema drift detection, dead-letter records, freshness checks,
  duplicate detection, and recovery tests.

## Feature Store And Inference

- Implemented point-in-time feature joins and offline/online parity checks for
  an account-risk workflow, with versioned feature state, simulated streaming
  updates, idempotent writes, late-event handling, and rollback tests.
- Built a local inference path with online-store fallback, request validation,
  model/version logging, feature freshness and drift reports, and batch scoring;
  documented the Redis/Feast/MLflow production migration boundary.

Do not call the current implementation a production real-time feature store or
quote its in-process latency on a CV.

## MLOps Lifecycle

- Built a deterministic model lifecycle workflow with data validation,
  train/validation/test splits, artifact tracking, candidate registration,
  champion promotion, batch scoring, monitoring, and rollback.
- Implemented eight blocking evaluation gates spanning data quality, accuracy,
  AUC, F1, RMSE, segment disparity, model size, and latency; tested that failed
  candidates cannot replace the champion.

Describe tracking and registry behavior as local or file-backed unless the
external MLflow path has been exercised.

## Data Observability And Lineage

- Built a local data reliability control plane that evaluates dataset contracts,
  freshness, schema drift, nulls, uniqueness, volume, and upstream health, then
  creates deduplicated incidents with likely cause and next action.
- Implemented transitive lineage impact analysis across datasets and business
  assets, with dbt/OpenLineage-shaped metadata, structured evidence, and tests
  for duplicate incident prevention.

## RAG Evaluation Pipeline

- Built a versioned RAG data pipeline with document loading, content hashing,
  deduplication, configurable chunking, deterministic embeddings, hybrid
  retrieval, metadata filters, citations, and incremental index artifacts.
- Implemented a retrieval regression harness covering recall, precision, MRR,
  nDCG, citation coverage, faithfulness heuristics, fallback behavior, latency,
  and cost estimates, with a runnable HTTP query path.

Do not claim production RAG quality from the current small fixture corpus. Lead
with the evaluation architecture and tests.

## Streaming Fraud And Anomaly

- Built a deterministic event-time risk simulator with transaction generation,
  schema validation, sliding/tumbling/session features, watermarks, late-event
  handling, deduplication, checkpointing, DLQ, replay, and explainable alerts.
- Tested at-least-once failure behavior including duplicate delivery, poison
  records, late events, idempotent scoring, and alert suppression; documented
  the Kafka/Flink production path and exactly-once tradeoffs.

Use **simulator** until a broker-backed path is part of the verified demo.

## ELT Connector Framework

- Built a reusable connector framework with full-refresh, incremental, append,
  and upsert semantics; implemented cursor checkpoints, pagination, bounded
  retry, rate-limit handling, schema inference, drift policy, and quarantine.
- Added connector contract tests proving checkpoint advancement, idempotent
  destination writes, pagination, schema-change handling, and recovery from
  transient source failures.

## Recommended Pairings

| Target Role | Project Bullets |
| --- | --- |
| Data Engineer | Lakehouse plus ELT or Observability |
| Analytics Engineer | Lakehouse plus Observability |
| ML Engineer | Feature Store plus MLOps Lifecycle |
| MLOps Engineer | MLOps Lifecycle plus Feature Store or Observability |
| AI/LLM Engineer | RAG Evaluation plus Lakehouse or Observability |
| Streaming/Data Platform | Streaming Fraud plus Lakehouse |
| Solution Architect | Lakehouse plus Feature Store and one reliability project |

## Language Rules

Prefer:

- built, implemented, tested, designed, documented
- local-first, production-style, deterministic simulator
- maps to, migration path, integration boundary

Avoid unless directly proven:

- production-grade, enterprise-ready, internet-scale
- real-time when processing local files in one process
- fully automated CI/CD when only one repository has CI
- MLflow-, Feast-, Airflow-, Kafka-, or Qdrant-based when the core demo does not
  execute that system
