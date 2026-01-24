#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Find Python
if command -v python3.12 >/dev/null 2>&1; then 
    PY=python3.12
elif command -v python3.11 >/dev/null 2>&1; then
    PY=python3.11
else 
    PY=python3
fi

# Parse arguments
LANG_FILTER=""
SKIP_CLEAN=false
SKIP_ANNOTATE=false
SKIP_REPORT=false
TEST_MODE=false

show_help() {
    cat << HELP
Usage: ./run.sh [OPTIONS]

Options:
    --lang LANG         Process only specific language (eng|deu|rus)
    --skip-clean        Skip cleaning step (use existing TSV)
    --skip-annotate     Skip annotation step
    --skip-report       Skip report generation
    --test              Test mode (process only 100 sentences per file)
    -h, --help          Show this help

Examples:
    ./run.sh                           # full pipeline, all languages
    ./run.sh --lang eng                # only English
    ./run.sh --lang deu --test         # test mode
    ./run.sh --skip-clean --lang rus   # skip cleaning
HELP
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --lang)
            LANG_FILTER="$2"
            shift 2
            ;;
        --skip-clean)
            SKIP_CLEAN=true
            shift
            ;;
        --skip-annotate)
            SKIP_ANNOTATE=true
            shift
            ;;
        --skip-report)
            SKIP_REPORT=true
            shift
            ;;
        --test)
            TEST_MODE=true
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

# Setup venv
if [ ! -d ".venv" ]; then 
    echo "Creating virtual environment..."
    "$PY" -m venv .venv
fi

source .venv/bin/activate
echo "Using Python: $PY"
echo "Installing requirements..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

# Check config
[ -f config/m1_config.yaml ] || { 
    echo "Missing config/m1_config.yaml"; 
    exit 1; 
}

# Build arguments
CLEAN_ARGS="--config config/m1_config.yaml"
ANNOTATE_ARGS="--in_dir data/clean --out_dir data/conllu"
REPORT_ARGS="--in_dir data/clean --report_path reports/m1_stats.md"

if [ -n "$LANG_FILTER" ]; then
    CLEAN_ARGS="$CLEAN_ARGS --lang $LANG_FILTER"
    ANNOTATE_ARGS="$ANNOTATE_ARGS --lang $LANG_FILTER"
    echo "Processing only: $LANG_FILTER"
fi

if [ "$TEST_MODE" = true ]; then
    ANNOTATE_ARGS="$ANNOTATE_ARGS --max_sentences 100"
    echo "Test mode: 100 sentences per file"
fi

# Step 1: Clean
if [ "$SKIP_CLEAN" = false ]; then
    echo ""
    echo "================================================"
    echo "Step 1: Text Cleaning"
    echo "================================================"
    python scripts/clean_news.py $CLEAN_ARGS
else
    echo "Skipping cleaning step"
fi

# Step 2: Annotate
if [ "$SKIP_ANNOTATE" = false ]; then
    echo ""
    echo "================================================"
    echo "Step 2: Linguistic Annotation (Stanza)"
    echo "================================================"
    python scripts/annotate_news.py $ANNOTATE_ARGS
else
    echo "Skipping annotation step"
fi

# Step 3: Report
if [ "$SKIP_REPORT" = false ]; then
    echo ""
    echo "================================================"
    echo "Step 3: Summary Report"
    echo "================================================"
    python scripts/m1_summaries.py $REPORT_ARGS
else
    echo "Skipping report generation"
fi

echo ""
echo "================================================"
echo "PIPELINE COMPLETE"
echo "================================================"
echo "Outputs:"
[ "$SKIP_CLEAN" = false ] && echo "  - Cleaned: data/clean/"
[ "$SKIP_ANNOTATE" = false ] && echo "  - Annotated: data/conllu/"
[ "$SKIP_REPORT" = false ] && echo "  - Report: reports/m1_stats.md"
echo ""
