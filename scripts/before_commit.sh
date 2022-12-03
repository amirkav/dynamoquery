#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

# vulture dynamoquery --make-whitelist > vulture_whitelist.txt
black **/*.py
isort **/*.py
flake8 dynamoquery
mypy dynamoquery
vulture dynamoquery vulture_whitelist.txt
pytest -m "not integration"
# pytest --cov-report html --cov dynamoquery

# ./scripts/docs.sh
