#!/usr/bin/env bash

set -euo pipefail

script_dir="$(dirname "$(readlink -f "$0")")"

# Execute
python -m venv .venv
./.venv/bin/pip install -e .[dev]
if [[ ! -L "/usr/bin/gitbs" ]]; then
  sudo ln -s "${script_dir}/start.sh" "/usr/bin/gitbs"
fi
