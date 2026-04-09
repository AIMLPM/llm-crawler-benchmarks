.PHONY: test lint invariants preflight

PYTHON ?= .venv/bin/python

test:
	$(PYTHON) -m pytest tests/ -q

lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) lint_reports.py

invariants:
	$(PYTHON) self_improvement/check_invariants.py
	$(PYTHON) self_improvement/check_cross_report_consistency.py

preflight: lint test invariants
