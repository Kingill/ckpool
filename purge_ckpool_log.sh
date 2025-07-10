#!/bin/bash

# Script to purge the CKPool log file

# Configuration
LOG_FILE="/home/ckpool/ckpool-solo/logs/ckpool.log"

# Check if the log file exists
if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file $LOG_FILE does not exist."
    exit 1
fi

# Notify about the purging process
echo "Purging CKPool log file $LOG_FILE"

# Truncate the log file
if [ ! -w "$(dirname "$LOG_FILE")" ] || { [ -f "$LOG_FILE" ] && [ ! -w "$LOG_FILE" ]; }; then
    echo "Error: Cannot write to or create $LOG_FILE"
else
    : > "$LOG_FILE"  # Truncate or create the file
fi

echo "Successfully purged"
echo "sudo systemctl restart hashrate.service"

