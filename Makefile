.PHONY: test lint invariants preflight check check-invariants check-consistency check-lint review smoke readme

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

# Regenerate README.md from report data
readme:
	$(PYTHON) generate_readme.py

# Graduated smoke test: 5/30/100 pages per tool
smoke:
	$(PYTHON) benchmark_all_tools.py --smoke-only

# Full self-improvement review: validate + show what changed
review: check
	@echo ""
	@echo "══ Changes ══════════════════════════════════════════"
	@if git diff --quiet && git diff --cached --quiet; then \
		echo "No changes detected."; \
	else \
		git diff --stat; \
		echo ""; \
		git diff; \
	fi
