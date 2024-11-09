#!/bin/bash

# Enable strict mode for better error handling
set -euo pipefail

# Set the backup directory
backup_dir="/path/to/backup"

# Create the backup directory if it doesn't exist
mkdir -p "$backup_dir"

# List of files and directories to back up
backup_items=("/home/user/documents" "/etc" "/var/log")

# Timestamp for the backup file
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
backup_file="$backup_dir/backup_$timestamp.tar.gz"

# Function to log messages
log_message() {
  local message=$1
  echo "$(date +"%Y-%m-%d %H:%M:%S") - $message"
}

# Perform the backup
log_message "Starting backup..."
if tar -czf "$backup_file" "${backup_items[@]}"; then
  log_message "Backup complete: $backup_file"
else
  log_message "Backup failed!"
  exit 1
fi