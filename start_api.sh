#!/bin/bash
source /mnt/data/pypi-gpt/env/bin/activate
export PYTHONPATH=/mnt/data/pypi-gpt/src
exec uvicorn clepy:app --host 0.0.0.0 --port 8000
