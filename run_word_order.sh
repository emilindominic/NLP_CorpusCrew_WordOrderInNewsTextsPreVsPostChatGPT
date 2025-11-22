#!/usr/bin/env bash
# Run word order extraction with flexible options
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default values
LANG=""
TEST_MODE=""
INPUT="data/conllu"
OUTPUT="data/word_order_labeled.csv"

# Help message
show_help() {
    cat << HELP
Word Order Extraction Script

Usage: ./run_word_order.sh [OPTIONS]

Options:
    --lang LANG         Process only specific language (eng|deu|rus)
    --test N            Test mode: process only N sentences per file
    --input PATH        Input CoNLL-U file or directory (default: data/conllu)
    --output PATH       Output CSV file (default: data/word_order_labeled.csv)
    -h, --help          Show this help message

Examples:
    # Test on 100 sentences from English
    ./run_word_order.sh --lang eng --test 100

    # Process all English files (full dataset)
    ./run_word_order.sh --lang eng

    # Process all languages (full dataset)
    ./run_word_order.sh

    # Process single file
    ./run_word_order.sh --input data/conllu/eng_news_2019_10K.conllu --test 50

Environment:
    The script will use the existing .venv if present, or system Python.
HELP
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --lang)
            LANG="$2"
            shift 2
            ;;
        --test)
            TEST_MODE="$2"
            shift 2
            ;;
        --input)
            INPUT="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
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

# Check if venv exists and activate it
if [ -d ".venv" ]; then
    echo "Using existing virtual environment (.venv)"
    source .venv/bin/activate
else
    echo "No virtual environment found, using system Python"
fi

# Build command
CMD="python scripts/extract_word_order.py --input $INPUT --output $OUTPUT"

if [ -n "$TEST_MODE" ]; then
    CMD="$CMD --test $TEST_MODE"
    echo "Running in TEST mode: $TEST_MODE sentences per file"
fi

# If language specified, filter input
if [ -n "$LANG" ]; then
    if [ -d "$INPUT" ]; then
        INPUT_PATTERN="$INPUT/${LANG}_*.conllu"
        # Check if any files match
        if ls $INPUT_PATTERN 1> /dev/null 2>&1; then
            echo "Processing language: $LANG"
            # Process each matching file
            for file in $INPUT_PATTERN; do
                CMD="python scripts/extract_word_order.py --input $file --output $OUTPUT"
                if [ -n "$TEST_MODE" ]; then
                    CMD="$CMD --test $TEST_MODE"
                fi
                echo "Running: $CMD"
                eval $CMD
            done
            exit 0
        else
            echo "No files found for language: $LANG"
            exit 1
        fi
    fi
fi

# Run the command
echo "Running: $CMD"
eval $CMD

echo ""
echo "Done! Output saved to: $OUTPUT"
