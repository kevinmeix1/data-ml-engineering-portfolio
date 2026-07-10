# Portfolio Improvement Roadmap

The next milestone is not more scope. It is turning three promising local demos
into repositories whose public claims, CI, containers, metrics, and screenshots
all agree.

## Priority 0: Correct The Public Story

Complete before pinning repositories on GitHub.

1. Replace `production-grade` and unqualified `real-time` language in repository
   descriptions and READMEs.
2. Add a local/integrated/production-mapping matrix to every README.
3. Move unused Compose dependencies to a `reference` profile or wire them into a
   smoke test.
4. Rename finite `serve` commands to `serve-smoke`, or make them run a real
   long-lived API.
5. Stop using local latency, throughput, drift, or three-question retrieval
   metrics as performance evidence.
6. Pin only the projects that have cleared the flagship gate.

**Exit criterion:** a reviewer cannot find a material mismatch between a README
claim and the command it references.

## Priority 1: Establish The Shared Baseline

Apply to all seven repositories:

- add the standard Make targets
- add Ruff and a real type checker
- add exact dependency locks and separate integration extras
- add GitHub Actions with read-only permissions, concurrency, tests, demo smoke,
  package build, and Docker validation
- pin container image versions and remove `latest`
- add health checks and `service_healthy` dependencies
- add one structured run summary and low-cardinality metric contract
- regenerate screenshots from clean current demos

**Exit criterion:** `make demo`, `make test`, `make lint`, `make typecheck`, and
the documented container smoke all pass in CI on the default branch.

## Priority 2: Make Lakehouse The Data Flagship

1. Wire one ELT connector output into the actual raw ingestion contract.
2. Exercise MinIO or a filesystem-compatible object-store adapter in an
   integration test.
3. Run the transformation graph with real dbt Core rather than only executing
   dbt-shaped SQL files.
4. Make the Airflow asset DAG call the package entry points and test DAG parsing.
5. Feed real quality and lineage artifacts into the incident/impact logic from
   the Observability repo.
6. Add a failed partition backfill, retry, and idempotent recovery walkthrough.
7. Redesign the dashboard around run status, freshness SLO, failed assets,
   backfill progress, and source-to-mart impact.

**Exit criterion:** a Compose smoke ingests through the object-store adapter,
runs dbt, publishes serving tables, emits lineage, opens an incident for a
broken partition, recovers it, and proves no duplicate facts.

## Priority 3: Make Feature Store The ML Flagship

1. Fix synthetic event ordering so the watermark scenario produces a credible
   mix of on-time and late events rather than marking most events late.
2. Make feature freshness deterministic and make the dashboard agree with the
   current report.
3. Add candidate quality gates or stop presenting the baseline model as a
   promoted success when its metrics are weak.
4. Start a real FastAPI service in Docker and smoke-test it over HTTP.
5. Exercise Redis in the integrated path, then kill Redis and prove the defined
   fallback and recovery behavior.
6. Run Feast materialization and historical retrieval, or label the Feast files
   as a reference adapter.
7. Merge the useful MLOps lifecycle controls: evaluation gate, model/feature
   compatibility, champion/challenger state, deployment decision, and rollback.
8. Add a controlled latency test with environment metadata and confidence
   bounds; keep it separate from production SLO claims.

**Exit criterion:** tests prove point-in-time correctness and parity; Compose
proves Redis-backed online retrieval, HTTP inference, degraded fallback,
promotion gating, and rollback with explicit model and feature versions.

## Priority 4: Make RAG The AI Flagship

1. Expand to at least dozens of realistic documents with sections, duplicates,
   updates, metadata ACLs, and malformed files.
2. Build a separate golden set with at least dozens of questions, hard
   negatives, unanswerable questions, and multi-document questions.
3. Add dataset splits so retrieval settings are not tuned and reported on the
   same examples.
4. Run one real vector backend, preferably Qdrant or pgvector, in Compose and
   compare it with the deterministic local index.
5. Add top-k, chunk-size, overlap, hybrid-weight, and reranker experiments with
   versioned reports.
6. Add answer abstention, citation entailment checks, and explicit hallucination
   categories.
7. Produce a before/after regression showing one failed question, its root
   cause, the data/index change, and the measured improvement.
8. Add query-log redaction, document-level authorization tests, retention, and
   threat-model notes.

**Exit criterion:** a held-out eval report demonstrates a reproducible retrieval
improvement on a non-trivial corpus, and the API returns cited answers or an
explicit abstention through a real vector backend.

## Priority 5: Decide The Supporting Repositories

### ELT and Observability

After their strongest capabilities run inside the Lakehouse flow:

- keep standalone repos only if they remain useful reusable components
- otherwise archive them with a README pointing to the integrated flagship
- do not leave duplicate active repos with the same generated dashboard story

### MLOps Lifecycle

After promotion and rollback controls are integrated into the ML flagship:

- retain it only if it becomes a distinct orchestration/governance project
- otherwise archive or unpin it to avoid competing registry and serving stories

### Streaming Fraud

Choose one of two paths:

- **Standalone flagship:** add real Kafka/Redpanda consumption, durable state,
  consumer-group replay, and a credible event-time engine or processor.
- **ML platform scenario:** keep the semantics tests and make fraud the streaming
  use case for online features and model serving.

**Exit criterion:** every public repo owns a distinct problem that can be stated
without repeating another repository's pitch.

## Priority 6: Product And UI Pass

- Give each dashboard a different workflow and visual hierarchy.
- Replace long record dumps with summary, trend, exception, and drill-down views.
- Keep one primary action or decision visible per screen.
- Show healthy, degraded, failed, and recovered states.
- Test desktop and mobile overflow with Playwright.
- Commit one current desktop screenshot per repository.

**Exit criterion:** screenshots are recognizable by domain even with the project
title hidden.

## Priority 7: Interview And Publishing

1. Record a three-minute walkthrough for each flagship.
2. Prepare one failure story and one tradeoff story per featured repo.
3. Create role-specific GitHub pin sets and CV variants.
4. Publish the shared portfolio README only after links, CI, and screenshots are
   current.
5. Keep the default branch clean and use small PRs with visible test evidence.

## Recommended Order

1. Public claim corrections
2. CI and command consistency
3. Lakehouse integration
4. Feature Store plus lifecycle integration
5. RAG corpus and evaluation depth
6. Supporting-repo consolidation
7. UI and interview polish

Do not start another project until the first three flagships meet their exit
criteria.
