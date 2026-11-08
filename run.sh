#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
  .venv/bin/python -m pip install -r requirements.txt
fi

PYTHONPATH=src .venv/bin/python -m hello
