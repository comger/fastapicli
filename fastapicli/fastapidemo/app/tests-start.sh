#! /usr/bin/env bash
set -e

# pytest --cov /app/app/

pytest  $* /app/cms/tests/
