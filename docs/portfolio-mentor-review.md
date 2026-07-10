# Portfolio Mentor Review

## Executive Assessment

The portfolio contains real, reviewable engineering logic. All 46 domain tests
pass, and each local workflow generates the documented artifacts. The strongest
tests cover meaningful properties: point-in-time correctness, offline/online
parity, idempotent ingestion, failed promotion gates, duplicate incidents, late
events, alert deduplication, and incremental checkpoints.

The portfolio is nevertheless over-presented. Seven similarly styled
"platforms," broad dependency lists, and Compose files containing unused
services make the work look generated before a reviewer reaches the good code.
The remedy is evidence and consolidation, not more tools.

No project should be called production-grade. Three are promising flagship
candidates; none has yet cleared the full portfolio standard.

## Audit Method

This review used the repositories as they exist, not their project briefs.

- Ran all 46 tests through the portfolio test runner.
- Ran every documented local workflow from a clean `.local` directory.
- Inspected each README, Makefile, Compose file, Dockerfile, CI workflow, source
  layout, test suite, and screenshot.
- Checked all seven public GitHub repositories and their descriptions.
- Distinguished executable integrations from SDK-shaped or file-backed
  simulations.

Audit date: 10 July 2026.

## Current Scorecard

| Project | Local Workflow | Tests | Public CI | Integrated Runtime | Mentor Verdict |
| --- | --- | ---: | --- | --- | --- |
| Lakehouse | Pass | 5 | No | App runs locally; MinIO, Redpanda, Postgres, dbt, and Airflow are not the core executed path | Best Data Engineering candidate; harden next |
| Feature Store | Pass | 6 | No | Core uses SQLite/JSON; FastAPI exists, but the container command runs a finite demo | Strong correctness tests; demo and serving path block flagship status |
| MLOps Lifecycle | Pass | 7 | Yes | File-backed tracking/registry; `serve` is a scoring smoke, not a long-running API | Useful governance module; merge into ML platform story |
| Observability | Pass with intentional incidents | 6 | No | SQLite/JSON metadata; Marquez/Postgres are reference services | Good reliability logic; integrate with Lakehouse |
| RAG Evaluation | Pass | 8 | No | Long-running local HTTP API; Qdrant/pgvector are not exercised | Best AI candidate; evaluation set is far too small |
| Streaming Fraud | Pass | 7 | No | JSONL topic simulator; no Kafka/Flink runtime | Good streaming semantics lab; not yet a real-time platform |
| ELT Connector | Pass | 7 | No | Fake API and local files/SQLite; MinIO/Postgres are reference services | Clean supporting framework; connect it to Lakehouse |

## Material Findings

### 1. Compose overstates integration

Every repository has a Compose file, but most core workflows still use local
files or SQLite. In several repos, external services start without being used;
in Feature Store and MLOps, the app container runs a finite command instead of
the API implied by its service name and exposed port.

This is the highest credibility risk because an interviewer can discover it in
minutes. Either wire a service into an integration test or move it behind a
`reference` profile and label it as production mapping.

### 2. Public proof is inconsistent

Only MLOps Lifecycle has GitHub Actions. Local tests are valuable, but a public
reviewer cannot see that the other six are continuously passing. Add the same
small, reliable CI contract everywhere before adding new architecture.

The existing MLOps workflow also calls `py_compile` both linting and type
checking. Use a real linter and type checker or call the step a compile check.

### 3. Flagship demo evidence is too easy

- Feature Store marks 259 of 300 simulated stream records late, reports stale
  features, and promotes a synthetic model with 0.50 accuracy and 0.125
  precision. Those outputs weaken rather than strengthen the story.
- RAG evaluates three tiny documents with three questions. Perfect recall and
  MRR are fixture checks, not meaningful retrieval-quality evidence.
- MLOps drift compares a batch distribution with one online prediction. The
  resulting alert demonstrates code execution, not statistical monitoring.
- Fraud throughput above 20,000 events/second is an in-process file-loop number,
  not a Kafka or end-to-end benchmark.

Keep these values in tests if they prove determinism, but do not use them as CV
or production performance claims.

### 4. The dashboards look related by template, not by product

The seven screenshots repeat the same dark header, metric tiles, pale tables,
and long static page. Specific issues include a wrapped timestamp in Lakehouse,
a `FAIL / n/a` panel in the Feature Store screenshot, dense incident cards in
Observability, and tiny demo counts in RAG and ELT.

Each UI should answer one domain question. A screenshot should fit in one useful
viewport and show a decision or incident, not every generated record.

### 5. Dependency lists imply paths the demos do not run

Several `pyproject.toml` files list Airflow, MLflow, Feast, Evidently, Ragas,
Qdrant, and other heavy integrations while the fast path uses the standard
library. This is acceptable only when extras are separated and the README says
which dependency set each command exercises.

## Overlap And Ownership

| Shared Concern | Repositories | Clear Owner |
| --- | --- | --- |
| Source extraction, pagination, and cursors | ELT, Lakehouse | ELT owns connector mechanics; Lakehouse consumes landed data |
| Schema and data quality | ELT, Lakehouse, Observability, RAG | Each enforces a domain contract; Observability aggregates failures into incidents |
| Lineage | Lakehouse, Observability | Lakehouse emits lineage; Observability consumes it for impact analysis |
| Streaming and late events | Lakehouse, Feature Store, Fraud | Fraud owns event-time processing; others consume domain streams |
| Model registration and rollback | Feature Store, MLOps, Fraud | MLOps owns promotion governance; serving systems consume approved versions |
| Drift and monitoring | Feature Store, MLOps, Observability, RAG | Each owns its domain signal; Observability owns cross-system incidents |
| Dashboards | All seven | Each dashboard must expose its system's unique operational decision |

## Flagship Recommendation

Treat these as flagship candidates, in this order:

1. **Lakehouse Data Platform** for Data Engineering and Solution Architecture.
   It has the broadest coherent data model and the strongest documentation.
2. **Feature Store and Inference** for ML Engineering and MLOps. Its temporal
   correctness and parity tests are valuable, but the demo and API path must be
   repaired before it is featured.
3. **RAG Evaluation Pipeline** for AI/LLM Systems. Keep the data/evaluation
   framing, but expand the evidence enough that retrieval metrics mean
   something.

Use Streaming Fraud as a fourth, role-specific project after it runs against an
actual broker and stream processor. Until then, call it an event-time simulator.

## Simplify And Merge

Do not create duplicate replacement repositories. Move capabilities into the
existing strongest repo, then archive or unpin the old source repo after links
and history are preserved.

### Data platform consolidation

- Keep `lakehouse-data-platform` as the public anchor.
- Integrate one real ELT connector so its checkpoint becomes the Lakehouse raw
  ingestion checkpoint.
- Integrate Observability's incidents and impact analysis against actual
  Lakehouse run, quality, and lineage artifacts.
- Keep the standalone ELT and Observability repos as labs only until that
  integration is complete; then archive or clearly mark them as extracted
  components.

### ML platform consolidation

- Keep Feature Store responsible for temporal feature correctness and serving.
- Move the useful MLOps controls into the same portfolio story: candidate
  evaluation, promotion, model/feature compatibility, deployment, and rollback.
- Do not maintain two separate file-backed registries and two near-identical
  prediction dashboards as equal projects.

### Streaming decision

- Keep Fraud standalone only if the next iteration uses Kafka/Redpanda and a
  real event-time engine or a credible consumer implementation.
- Otherwise, use it as the streaming use case inside the ML platform and retain
  a focused semantics test suite.

### RAG remains standalone

RAG has a distinct data model and evaluation problem. Do not merge it with the
structured feature platform. Share only observability conventions and incident
interfaces.

## Target Public Portfolio

The cleanest long-term portfolio is four systems, with only three pinned for a
given role:

1. **Analytics Data Platform**: connector ingestion, Lakehouse modeling, data
   quality, lineage, incidents, backfills, and serving marts.
2. **ML Feature and Delivery Platform**: point-in-time features, training,
   evaluation gates, registry, online inference, monitoring, and rollback.
3. **RAG Quality System**: versioned corpus, indexing, retrieval, evaluation,
   citations, error analysis, and cost/latency telemetry.
4. **Streaming Risk System**: broker-backed event-time processing, scoring,
   DLQ, replay, alerts, and operational metrics.

## What To Say In Interviews

Use this framing:

> These are local-first, production-style systems built with deterministic
> synthetic data. I use them to demonstrate specific guarantees and failure
> handling. Where a dependency is not exercised, I label it as production
> mapping rather than an implemented integration.

Avoid these claims:

- "production-grade" or "enterprise-ready"
- "real-time" for an in-process JSONL simulator
- "MLflow/Feast/Airflow-based" when the default workflow writes compatible
  local files but does not run the platform
- latency, throughput, drift, or retrieval numbers produced by tiny local
  fixtures as production benchmarks

## Decision

Do not add an eighth project. First make one Data Engineering flagship, one ML
platform flagship, and one AI flagship indisputably runnable. The portfolio will
look more senior when three repositories have deep evidence than when seven
repositories list every fashionable tool.
