# Shared Engineering Standard

This is the minimum public quality bar for every project. It favors truthful,
repeatable evidence over a large architecture diagram.

It is deliberately a target standard. As audited on 10 July 2026, the current
portfolio has `make test` in 7/7 repositories, `make demo` in 5/7, a real linter
in 0/7, a real type checker in 0/7, child-repository CI in 1/7, and a verified
service-backed Compose smoke path in 0/7. Compliance must be earned by an
executable check, not inferred from a file or dependency name.

## 1. Three Execution Modes

Every README must include an implementation matrix like this:

| Capability | Local | Integrated | Production Mapping |
| --- | --- | --- | --- |
| Example: event storage | SQLite/files, exercised by `make demo` | Postgres/MinIO, exercised by `make compose-smoke` | S3 and warehouse design notes |

The labels have strict meanings:

- **Local:** runs without external paid or hosted services and is covered by
  tests.
- **Integrated:** starts real dependencies and proves behavior against them.
  Starting an unused container does not count.
- **Production mapping:** architecture or migration guidance only.

If an external service is not integrated, put it behind a Compose `reference`
profile or remove it from the default stack.

## 2. Command Contract

Every repository exposes these targets:

```bash
make demo
make test
make lint
make typecheck
make compose-config
make compose-up
make compose-smoke
make compose-down
make clean
```

Required behavior:

| Command | Contract |
| --- | --- |
| `make demo` | Starts from deterministic inputs, runs the core local workflow, and prints a concise artifact summary. |
| `make test` | Runs unit, contract, failure, and workflow tests without paid services. |
| `make lint` | Runs a real linter such as Ruff. |
| `make typecheck` | Runs a real type checker such as mypy or Pyright; it is not an alias for compilation. |
| `make compose-config` | Validates the Compose model. |
| `make compose-up` | Starts the integrated path and waits for health. |
| `make compose-smoke` | Calls running services and proves at least one domain behavior. |
| `make compose-down` | Removes containers and test volumes predictably. |
| `make clean` | Removes only generated state under `.local/`. |

Domain commands such as `make backfill`, `make replay`, `make train`,
`make evaluate`, `make rollback`, `make reindex`, and `make sync` remain useful.

## 3. Repository Layout

Use this layout when the contents are real:

```text
project-name/
  README.md
  LICENSE
  Makefile
  pyproject.toml
  pylock.toml                 # or a documented, exact lock format
  Dockerfile
  compose.yaml
  src/<package_name>/
  tests/
    unit/
    contract/
    integration/
  configs/
  contracts/
  orchestration/
  infra/
  docs/
    architecture.md
    runbooks/
    adr/
    screenshots/
  .github/workflows/ci.yml
```

Do not create empty folders to look complete. Keep generated databases, logs,
reports, models, indexes, and screenshots under `.local/` unless a curated
artifact is intentionally committed.

Public repository names use lowercase kebab case. Python packages use lowercase
snake case. Keep the current names:

| Repository | Python Package |
| --- | --- |
| `lakehouse-data-platform` | `lakehouse_platform` |
| `feature-store-inference` | `feature_store_system` |
| `mlops-lifecycle-platform` | `mlops_platform` |
| `data-observability-lineage` | `observability_platform` |
| `rag-evaluation-pipeline` | `rag_pipeline` |
| `streaming-fraud-anomaly` | `fraud_streaming` |
| `elt-connector-framework` | `elt_framework` |

The portfolio index uses numbered submodule paths for a stable review order;
the independent GitHub repository names do not include those prefixes:

```text
data-ml-engineering-portfolio/
  README.md
  Makefile
  scripts/
  docs/
  01-lakehouse-data-platform/
  02-feature-store-inference/
  03-mlops-lifecycle-platform/
  04-data-observability-lineage/
  05-rag-evaluation-pipeline/
  06-streaming-fraud-anomaly/
  07-elt-connector-framework/
```

The numbers are navigation order, not maturity scores. Capability consolidation
should happen inside the strongest repositories; do not create new duplicate
repositories merely to rename a project.

## 4. Docker And Compose

Use `compose.yaml` and `docker compose`, not legacy orchestration language.

Minimum standard:

- pin application base images and service image versions; avoid `latest`
- build a non-root application image
- use a read-only root filesystem where practical
- drop Linux capabilities and disable privilege escalation
- store mutable state in named volumes or explicit mounts
- add health checks to every long-running service
- use long-form `depends_on` with `service_healthy` when readiness matters
- give finite setup jobs `service_completed_successfully` semantics
- set stop grace periods and deterministic cleanup
- document ports and avoid common collisions across the portfolio
- add a live HTTP or protocol smoke test; container build alone is insufficient

Docker documents that short-form `depends_on` waits only for startup, while
`service_healthy` waits for a declared health check. Compose profiles are useful
for optional debug, observability, or reference services.

## 5. Dependencies And Reproducibility

- Define project metadata and dependency groups in `pyproject.toml`.
- Keep the fast local dependency group small.
- Put Airflow, Feast, MLflow, Ragas, Qdrant, or cloud SDKs in named integration
  extras when the default path does not import them.
- Commit an exact lock for application and CI environments. The current Python
  packaging specification defines `pylock.toml` for reproducible installs; a
  tool-specific lock is acceptable when documented.
- Build a wheel in CI and run `pip check`.
- Record Python and tool versions in generated evidence.

## 6. Test Architecture

Each project needs four test layers:

1. **Unit:** deterministic domain logic.
2. **Contract:** schemas, feature signatures, API payloads, manifests, and
   generated artifact shapes.
3. **Failure:** retries, duplicates, bad schemas, stale data, rollback, DLQ,
   or missing dependencies.
4. **Integration:** the real Compose service path.

Critical property by project:

| Project | Property That Must Be Proved |
| --- | --- |
| Lakehouse | Idempotent ingestion, source-to-mart reconciliation, and deterministic backfill |
| Feature Store | Point-in-time correctness, offline/online parity, and fallback semantics |
| MLOps Lifecycle | Failed candidates cannot become champion and rollback restores a known version |
| Observability | Duplicate incident prevention and transitive impact analysis |
| RAG | Retrieval regression on a non-trivial golden set and citation grounding |
| Streaming Fraud | Event-time handling, dedupe, replay, poison records, and alert dedupe |
| ELT | Checkpoint atomicity, pagination, rate limiting, schema drift, and idempotent destination writes |

Never treat a tiny fixture metric as evidence of model or retrieval quality. A
fixture can prove behavior; a benchmark needs enough data, uncertainty, and a
documented environment.

## 7. CI/CD

Every public repository has a small GitHub Actions workflow with:

- explicit `permissions: contents: read`
- workflow concurrency with stale runs cancelled
- supported Python version and dependency cache
- exact dependency installation and `pip check`
- lint and type-check jobs
- unit and contract tests
- deterministic demo smoke test
- package and Docker build
- Compose integration smoke test where Docker is part of the claim
- uploaded reports or diagnostics on failure

Pin third-party actions to reviewed full commit SHAs for immutable workflow
dependencies. Keep deployment credentials out of pull-request workflows and use
least-privilege environment protection for real deployments.

## 8. Logging

Emit one JSON object per line. Every operational event includes:

- timestamp in UTC
- event name and severity
- run, request, event, sync, or incident identifier
- component and environment
- dataset, model, feature, schema, or index version where relevant
- duration and outcome
- bounded error category

Do not log raw features, document contents, prompts, emails, account IDs, or
other sensitive values by default. Use OpenTelemetry semantic conventions when
instrumenting HTTP, database, messaging, and object-store operations so logs,
metrics, and traces correlate consistently.

## 9. Metrics

Metrics must expose the main operational risk, not simply fill a dashboard.

| Project | Primary Metrics |
| --- | --- |
| Lakehouse | freshness, reconciliation, failed runs, backfill progress, rows by layer |
| Feature Store | feature age, null rate, parity, online-store hit rate, inference latency |
| MLOps Lifecycle | gate outcomes, candidate/champion version, deployment and batch status |
| Observability | open incidents, stale assets, failed checks, mean time to detect/recover |
| RAG | recall and nDCG, failed retrieval rate, citation coverage, latency, cost estimate |
| Streaming Fraud | input rate, event-time lag, consumer lag, DLQ, score and alert volume |
| ELT | extracted/loaded/quarantined rows, retry count, lag, checkpoint age, schema version |

Prometheus labels must be low-cardinality. Never use customer, request, event,
document, or incident IDs as metric labels.

## 10. README Structure

Use the same order in every repository:

1. One-sentence problem and scope
2. Screenshot
3. Three-minute quick start
4. Implementation matrix: local, integrated, production mapping
5. Architecture diagram
6. Core guarantees and how they are tested
7. Commands and generated artifacts
8. Failure demo and recovery
9. Observability
10. Limitations and production hardening
11. Interview talking points

The first screen should explain what is executable. Avoid long lists of tools
before the reader understands the problem.

## 11. Architecture And ADRs

Mermaid diagrams must distinguish solid implemented paths from dashed migration
paths. Show state stores, failure paths, ownership boundaries, and recovery
loops. Do not show a service merely because it appears in `pyproject.toml`.

Write ADRs only for real decisions, such as:

- local fast path versus integrated service path
- at-least-once plus idempotency versus exactly-once
- point-in-time materialization strategy
- file-backed registry versus external registry
- vector database and hybrid retrieval choice
- incident deduplication key and retention

## 12. Runbooks

At least one runnable incident per project must answer:

- What failed and how was it detected?
- What user or downstream asset is affected?
- Which logs, metrics, state, and versions should be inspected?
- What is the safe local recovery command?
- Is replay/backfill idempotent?
- What is the production recovery and rollback path?
- How is recurrence prevented?

## 13. Demo Data

Demo data must be deterministic, documented, and include both healthy and broken
cases. Use enough data to exercise logic, but do not imply scale. Record the seed
and scenario mix in the output.

Model and retrieval projects need separate fixture and evaluation datasets. Do
not tune against the same three examples used to report quality.

## 14. UI And Screenshots

- Give each project a domain-specific information architecture.
- Show one decision-oriented viewport, not an endless table dump.
- Use charts only where a trend or distribution matters.
- Show failure and recovery states intentionally.
- Prevent wrapping identifiers and timestamps from breaking metric tiles.
- Verify desktop and mobile overflow before committing screenshots.
- Retake screenshots from a clean, current demo in CI or a documented release
  process.

## Definition Of Done

A project becomes flagship-ready only when:

- local and Compose smoke paths both pass
- CI is green on the default branch
- dependencies and images are reproducible
- the core correctness property has a direct test
- one failure/recovery scenario is runnable
- metrics and logs are generated from the real path
- README claims match the implementation matrix
- the screenshot is current and readable
- limitations name the missing production controls

## References

- [Docker Compose startup order and health conditions](https://docs.docker.com/compose/how-tos/startup-order/)
- [Docker Compose profiles](https://docs.docker.com/compose/how-tos/profiles/)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Actions concurrency](https://docs.github.com/en/actions/concepts/workflows-and-actions/concurrency)
- [Python `pylock.toml` specification](https://packaging.python.org/en/latest/specifications/pylock-toml/)
- [OpenTelemetry semantic conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/)
- [Prometheus client instrumentation guidance](https://prometheus.io/docs/instrumenting/writing_clientlibs/)
