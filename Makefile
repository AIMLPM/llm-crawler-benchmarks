.PHONY: test lint invariants preflight check check-invariants check-consistency check-lint

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

# Self-assessment targets
check: check-invariants check-consistency check-lint

check-invariants:
	$(PYTHON) self_improvement/check_invariants.py

check-consistency:
	$(PYTHON) self_improvement/check_cross_report_consistency.py

check-lint:
	$(PYTHON) lint_reports.py
