#!/bin/bash

# Ensure the script exits if any command fails
set -e

# Define the path to your docker-compose file
COMPOSE_FILE="/home/server-config/docker-compose.yml"

# Run docker-compose up with necessary options
docker-compose -f $COMPOSE_FILE up --build --force-recreate --remove-orphans -d

# Check if the docker-compose command executed successfully
if [ $? -eq 0 ]; then
    echo "Docker Compose has successfully built and started the containers."
else
    echo "Docker Compose failed to build and start the containers."
    exit 1
fi