#!/bin/bash

# Run the Python script
python wiki_server_config.py "$1"

# Run this command (will execute "sudo python3 server_config.py wiki_server_config")
# sudo ./run_script.sh prepare_server

# Keep the shell open
exec "$SHELL"