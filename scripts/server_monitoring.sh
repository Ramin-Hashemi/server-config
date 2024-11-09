#!/bin/bash

# Enable strict mode for better error handling
set -euo pipefail

# Server details
server_url="http://ime-agent.com"
email_recipient="ramin.hashemi@usa.com"

# Function to send email alerts
send_alert() {
  local message=$1
  echo "$message" | mail -s "Server Down Alert" "$email_recipient"
}

# Check server status
response=$(curl -s -o /dev/null -w "%{http_code}" "$server_url")

if [ "$response" -ne 200 ]; then
  send_alert "Server is down! HTTP status code: $response"
else
  echo "Server is up and running."
fi