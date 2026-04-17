#!/usr/bin/env bash
set -euo pipefail
pip install -U pip
pip install -e ".[dev]"
alembic upgrade head
