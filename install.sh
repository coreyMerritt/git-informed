#!/usr/bin/env bash

set -euo pipefail

script_dir="$(dirname "$(readlink -f "$0")")"
binary_dir="/usr/bin"
binary_name="giti"

# Execute
rm -rf "./.venv"
python -m venv "./.venv"
./.venv/bin/pip install -e .[dev]
if [[ ! -L "${binary_dir}/${binary_name}" ]]; then
  sudo ln -s "${script_dir}/start.sh" "${binary_dir}/${binary_name}"
fi
