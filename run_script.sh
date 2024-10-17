#!/bin/bash
source .venv/bin/activate
python server_config.py
exec "$SHELL"