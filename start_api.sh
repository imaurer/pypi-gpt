#!/bin/bash

# script for running on prod using systemd
source /mnt/data/pypi-gpt/env/bin/activate
export PYTHONPATH=/mnt/data/pypi-gpt/src
exec uvicorn pypi_gpt:app --host 0.0.0.0 --port 8000
