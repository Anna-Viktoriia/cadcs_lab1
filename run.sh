#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    command -v python3 >/dev/null 2>&1 || {
        echo "python3 is required to create .venv" >&2
        exit 1
    }
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
fi

PYTHONPATH=src .venv/bin/python -m hello
