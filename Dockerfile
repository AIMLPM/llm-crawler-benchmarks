# Benchmark environment for LLM crawler head-to-head comparison.
#
# Bundles Python, Go, Playwright browsers, and all 7 benchmark tools so
# results are reproducible across machines.
#
# Build:
#   docker build -t llm-crawler-benchmarks .
#
# Run (pass API keys for firecrawl / answer-quality benchmarks):
#   docker run --rm \
#     -e FIRECRAWL_API_KEY \
#     -e OPENAI_API_KEY \
#     -v $(pwd)/reports:/app/reports \
#     -v $(pwd)/runs:/app/runs \
#     llm-crawler-benchmarks
#
# The volume mount lets results write back to your host.

FROM python:3.13-slim AS base

# System deps for Playwright browsers and lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget curl gnupg ca-certificates \
        # Playwright/patchright system deps (Chromium)
        libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
        libcups2 libdrm2 libxkbcommon0 libatspi2.0-0 libxcomposite1 \
        libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
        libasound2 libwayland-client0 libcairo2 \
        # lxml build deps
        libxml2-dev libxslt1-dev \
        # General
        git \
    && rm -rf /var/lib/apt/lists/*

# ---------- Go (for Colly binary) ----------
FROM base AS go-builder
ARG GO_VERSION=1.24.4
RUN wget -q "https://go.dev/dl/go${GO_VERSION}.linux-$(dpkg --print-architecture).tar.gz" -O /tmp/go.tar.gz \
    && tar -C /usr/local -xzf /tmp/go.tar.gz \
    && rm /tmp/go.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

COPY tools/colly_crawler /build/colly_crawler
WORKDIR /build/colly_crawler
RUN go build -o colly_crawler .

# ---------- Final image ----------
FROM base

WORKDIR /app

# Copy the Go binary
COPY --from=go-builder /build/colly_crawler/colly_crawler /usr/local/bin/colly_crawler

# Install benchmark dependencies (includes markcrawl from PyPI)
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir ".[dev]"

# Install Playwright Chromium to a shared path accessible by non-root user.
# crawl4ai uses patchright (a Playwright fork) with its own browser binaries.
# Without the patchright install, crawl4ai imports fine but fails at runtime
# with "BrowserType.launch: Executable doesn't exist".
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/browsers
RUN python -m playwright install chromium && \
    python -m patchright install chromium && \
    chmod -R o+rx /opt/browsers && \
    # patchright may cache to /root — make accessible too
    chmod -R o+rx /root/.cache 2>/dev/null && chmod o+x /root || true

# Copy benchmark scripts and reports
COPY benchmark_*.py quality_scorer.py crawlee_worker.py lint_reports.py preflight.py test_crawl4ai_graduated.py generate_readme.py report_utils.py ./
COPY runners/ runners/
COPY reports/ reports/
COPY self_improvement/ self_improvement/
COPY tests/ tests/
COPY tools/ tools/

# Non-root user — owns /app so benchmarks can write caches and results
RUN groupadd -r bench && useradd -r -g bench -d /app bench && \
    chown -R bench:bench /app
USER bench

# Default: run the head-to-head comparison
ENTRYPOINT ["python", "benchmark_all_tools.py"]
