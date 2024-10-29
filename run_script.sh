#!/bin/bash

# Install python3-tqdm
if sudo apt-get install -y python3-tqdm; then
    echo "python3-tqdm installed successfully."
else
    echo "Failed to install python3-tqdm." >&2
    exit 1
fi

# Run the Python script
if python3 server_config.py "run"; then
    echo "Python script executed successfully."
else
    echo "Failed to execute Python script." >&2
    exit 1
fi

# Keep the shell open
exec "$SHELL"