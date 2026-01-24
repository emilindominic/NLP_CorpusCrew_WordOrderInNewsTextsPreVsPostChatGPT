#!/usr/bin/env bash
# Convenience runner for rule-based baselines and evaluation.
# - Ensures spaCy language models are available (downloads if missing, unless skipped)
# - Runs simple heuristic baseline, POS-pattern baseline, then evaluation report.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="python"
SKIP_DOWNLOAD=false

show_help() {
    cat <<'HELP'
Usage: ./run.sh [--skip-download]

Options:
  --skip-download   Do not attempt to download spaCy language models.
  -h, --help        Show this help message.

Behavior:
  1) If .venv exists, it is activated.
  2) Ensures spaCy models en_core_web_sm, de_core_news_sm, ru_core_news_sm exist
     (unless --skip-download is set).
  3) Runs:
        python scripts/simple_heuristic_baseline.py
        python scripts/pos_pattern_baseline.py
        python scripts/evaluate_baselines.py
HELP
}

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-download)
            SKIP_DOWNLOAD=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Activate venv if present
if [[ -d ".venv" ]]; then
    echo "Using existing virtual environment (.venv)"
    source .venv/bin/activate
    PYTHON_BIN="python"
else
    echo "No virtual environment found, using system Python"
fi

ensure_model() {
    local model="$1"
    if "$PYTHON_BIN" - <<PY
import sys
try:
    import spacy
    spacy.load("$model")
except Exception:
    sys.exit(1)
sys.exit(0)
PY
    then
        echo "spaCy model '$model' already installed"
    else
        if [[ "$SKIP_DOWNLOAD" == true ]]; then
            echo "Skipping download of '$model' (not installed)"
        else
            echo "Downloading spaCy model '$model'..."
            "$PYTHON_BIN" -m spacy download "$model"
        fi
    fi
}

if [[ "$SKIP_DOWNLOAD" != true ]]; then
    ensure_model "en_core_web_sm"
    ensure_model "de_core_news_sm"
    ensure_model "ru_core_news_sm"
fi

echo ""
echo "Running simple heuristic baseline..."
"$PYTHON_BIN" scripts/simple_heuristic_baseline.py

echo ""
echo "Running POS-pattern baseline..."
"$PYTHON_BIN" scripts/pos_pattern_baseline.py

echo ""
echo "Generating rule-based evaluation report..."
"$PYTHON_BIN" scripts/evaluate_baselines.py

echo ""
echo "Done. Reports are in reports/, predictions in data/."
