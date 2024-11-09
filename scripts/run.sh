#!/bin/bash

# Run the first script
./secret_encrypt.sh

# Check if the first script executed successfully
if [ $? -eq 0 ]; then
    echo "secret_encrypt.sh executed successfully."
else
    echo "secret_encrypt.sh failed."
    exit 1
fi

# Run the second script
./server_init.sh

# Check if the second script executed successfully
if [ $? -eq 0 ]; then
    echo "server_init.sh executed successfully."
else
    echo "server_init.sh failed."
    exit 1
fi

# Run the third script
./run_docker_compose.sh

# Check if the third script executed successfully
if [ $? -eq 0 ]; then
    echo "run_docker_compose.sh executed successfully."
else
    echo "run_docker_compose.sh failed."
    exit 1
fi

# Run the fourth script
./server_monitoring.sh

# Check if the third script executed successfully
if [ $? -eq 0 ]; then
    echo "server_monitoring.sh executed successfully."
else
    echo "server_monitoring.sh failed."
    exit 1
fi

# Run the fifth script
./server_backup.sh

# Check if the third script executed successfully
if [ $? -eq 0 ]; then
    echo "server_backup.sh executed successfully."
else
    echo "server_backup.sh failed."
    exit 1
fi

# Run the sixth script


# Run the seventh script


# Run the eighth script
