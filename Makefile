.PHONY: bootstrap test docs-check verify-submodules tree

PROJECTS := \
	01-lakehouse-data-platform \
	02-feature-store-inference \
	03-mlops-lifecycle-platform \
	04-data-observability-lineage \
	05-rag-evaluation-pipeline \
	06-streaming-fraud-anomaly \
	07-elt-connector-framework

bootstrap:
	git submodule update --init --recursive

test: docs-check verify-submodules
	python3 scripts/run_all_tests.py

docs-check:
	python3 scripts/check_portfolio_docs.py

verify-submodules:
	@for project in $(PROJECTS); do \
		test -f "$$project/Makefile" || { \
			echo "Missing $$project. Run: make bootstrap" >&2; \
			exit 1; \
		}; \
	done

tree:
	find . -maxdepth 3 -type f | sort
