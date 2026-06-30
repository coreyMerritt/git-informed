#!/usr/bin/env bash

set -euo pipefail

script_dir="$(dirname "$(readlink -f "$0")")"

${script_dir}/.venv/bin/python "${script_dir}/src/main.py" "$@"
