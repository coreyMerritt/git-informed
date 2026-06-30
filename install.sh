#!/usr/bin/env bash

set -euo pipefail

script_dir="$(dirname "$(readlink -f "$0")")"

sudo ln -s "${script_dir}/start.sh" "/usr/bin/gitbs"
