#!/usr/bin/env bash
# Run the benchmark suite — auto-detects Docker or falls back to standalone.
#
# Usage:
#   ./run_benchmarks.sh                     # auto-detect
#   ./run_benchmarks.sh --docker            # force Docker
#   ./run_benchmarks.sh --standalone        # force standalone (venv)
#   ./run_benchmarks.sh --docker -- --sites fastapi-docs --iterations 1
#
# Any arguments after -- are passed to benchmark_all_tools.py.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
IMAGE_NAME="llm-crawler-bench"

MODE=""
BENCH_ARGS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --docker)    MODE="docker"; shift ;;
        --standalone) MODE="standalone"; shift ;;
        --)          shift; BENCH_ARGS=("$@"); break ;;
        *)           BENCH_ARGS+=("$1"); shift ;;
    esac
done

# ---------------------------------------------------------------------------
# Docker helpers
# ---------------------------------------------------------------------------

docker_is_installed() {
    command -v docker &>/dev/null
}

docker_is_running() {
    docker info &>/dev/null 2>&1
}

start_docker_desktop() {
    echo "Docker daemon not running — attempting to start Docker Desktop..."

    case "$(uname -s)" in
        Darwin)
            open -a Docker 2>/dev/null || open "/Applications/Docker.app" 2>/dev/null || {
                echo "ERROR: Could not open Docker Desktop. Install it from https://docker.com/products/docker-desktop"
                return 1
            }
            ;;
        Linux)
            if command -v systemctl &>/dev/null; then
                sudo systemctl start docker 2>/dev/null || true
            fi
            if ! docker_is_running; then
                nohup /opt/docker-desktop/bin/docker-desktop &>/dev/null &
            fi
            ;;
        MINGW*|MSYS*|CYGWIN*)
            cmd.exe /c "start \"\" \"C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe\"" 2>/dev/null || {
                echo "ERROR: Could not start Docker Desktop on Windows."
                return 1
            }
            ;;
    esac

    echo -n "Waiting for Docker daemon"
    for i in $(seq 1 60); do
        if docker_is_running; then
            echo " ready."
            return 0
        fi
        echo -n "."
        sleep 1
    done
    echo " timed out."
    echo "ERROR: Docker daemon did not start within 60 seconds."
    return 1
}

ensure_docker() {
    if ! docker_is_installed; then
        echo "ERROR: Docker is not installed. Install from https://docker.com/products/docker-desktop"
        exit 1
    fi
    if ! docker_is_running; then
        start_docker_desktop || exit 1
    fi
}

run_docker() {
    ensure_docker
    cd "$REPO_ROOT"

    # Build image if it doesn't exist or Dockerfile changed
    if ! docker image inspect "$IMAGE_NAME" &>/dev/null; then
        echo "Building benchmark Docker image (first time — may take a few minutes)..."
        docker build -t "$IMAGE_NAME" .
    fi

    # Collect env vars to pass through
    ENV_ARGS=()
    [[ -n "${FIRECRAWL_API_KEY:-}" ]]  && ENV_ARGS+=(-e FIRECRAWL_API_KEY)
    [[ -n "${FIRECRAWL_API_URL:-}" ]]  && ENV_ARGS+=(-e FIRECRAWL_API_URL)
    [[ -n "${FIRECRAWL_TIER:-}" ]]     && ENV_ARGS+=(-e FIRECRAWL_TIER)
    [[ -n "${OPENAI_API_KEY:-}" ]]     && ENV_ARGS+=(-e OPENAI_API_KEY)

    if [[ -f "$REPO_ROOT/.env" ]]; then
        _clean_env=$(mktemp)
        sed -e 's/^export //' \
            -e 's/="\(.*\)"$/=\1/' \
            -e "s/='\(.*\)'$/=\1/" \
            "$REPO_ROOT/.env" > "$_clean_env"
        ENV_ARGS+=(--env-file "$_clean_env")
    fi

    # Run preflight smoke test first
    echo "Running pre-flight smoke test in Docker..."
    docker run --rm \
        "${ENV_ARGS[@]}" \
        -v "$REPO_ROOT/reports:/app/reports" \
        -v "$REPO_ROOT/runs:/app/runs" \
        --entrypoint python \
        "$IMAGE_NAME" \
        preflight.py --smoke-test

    echo ""
    echo "Running benchmarks in Docker..."
    docker run --rm \
        "${ENV_ARGS[@]}" \
        -v "$REPO_ROOT/reports:/app/reports" \
        -v "$REPO_ROOT/runs:/app/runs" \
        "$IMAGE_NAME" \
        "${BENCH_ARGS[@]}"
}

# ---------------------------------------------------------------------------
# Standalone (venv) helpers
# ---------------------------------------------------------------------------

run_standalone() {
    cd "$REPO_ROOT"

    if [[ -f ".venv/bin/python3" ]]; then
        PYTHON=".venv/bin/python3"
    elif [[ -f ".venv/Scripts/python.exe" ]]; then
        PYTHON=".venv/Scripts/python.exe"
    else
        PYTHON="python3"
    fi

    echo "Running pre-flight check..."
    if ! "$PYTHON" preflight.py; then
        echo ""
        echo "Pre-flight failed. Run:  $PYTHON preflight.py --install"
        exit 1
    fi

    echo ""
    echo "Running benchmarks (standalone)..."
    "$PYTHON" benchmark_all_tools.py "${BENCH_ARGS[@]}"
}

# ---------------------------------------------------------------------------
# Auto-detect mode
# ---------------------------------------------------------------------------

if [[ -z "$MODE" ]]; then
    if docker_is_installed; then
        MODE="docker"
    else
        MODE="standalone"
    fi
fi

case "$MODE" in
    docker)     run_docker ;;
    standalone) run_standalone ;;
esac
