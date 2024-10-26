#!/bin/bash

# Run the Python script
python server_config.py "$1"

# Run this command (will execute "sudo python3 server_config.py prepare_server")
# sudo ./run_script.sh prepare_server

# Keep the shell open
exec "$SHELL"