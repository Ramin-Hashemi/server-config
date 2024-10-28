#!/bin/bash

# Run the Python script
python server_config.py "$1"

# Run below command (this will execute "sudo python3 server_config.py run")
# sudo ./run_script.sh run

# Keep the shell open
exec "$SHELL"