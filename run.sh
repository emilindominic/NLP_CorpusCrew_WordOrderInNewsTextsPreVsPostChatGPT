#!/usr/bin/env bash
set -euo pipefail

#for repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

#for python
if command -v python3.12 >/dev/null 2>&1; then PY=python3.12; else PY=python3; fi

#create venv if no, activate
if [ ! -d ".venv" ]; then "$PY" -m venv .venv; fi
source .venv/bin/activate

#install requirements
pip install -r requirements.txt

#config check
[ -f config/m1_config.yaml ] || { echo "Missing config/m1_config.yaml"; exit 1; }

#run preprocessing
python scripts/clean_news.py --config config/m1_config.yaml

#run report
python scripts/m1_summaries.py --in_dir data/clean --report_path reports/m1_stats.md
echo "Done. Outputs in data/clean/ and reports/m1_stats.md"
