#!/bin/bash

# Script to purge the CKPool log file
# Usage: sudo ./purge_ckpool_log.sh

# Configuration
LOG_FILE="/home/ckpool/ckpool-solo/ckpool.log"
USER="ckpool"
GROUP="ckpool"
SERVICE_NAME="ckpool"

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root (use sudo)."
    exit 1
fi

# Check if the log file exists
if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file $LOG_FILE does not exist."
    exit 1
fi

# Check if the ckpool user exists
if ! id "$USER" >/dev/null 2>&1; then
    echo "Error: User $USER does not exist."
    exit 1
fi

# Check if the ckpool group exists
if ! getent group "$GROUP" >/dev/null; then
    echo "Error: Group $GROUP does not exist."
    exit 1
fi

# Notify about the purging process
echo "Purging CKPool log file: $LOG_FILE"

# Truncate the log file (safer than deleting, keeps file handle intact)
if ! : > "$LOG_FILE"; then
    echo "Error: Failed to truncate $LOG_FILE. Check permissions."
    exit 1
fi

# Restore ownership and permissions
chown "$USER:$GROUP" "$LOG_FILE"
chmod 640 "$LOG_FILE"

# Optional: Signal CKPool to reopen log file (if it doesn't use journald)
# CKPool may need to be signaled to release the file handle
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Reloading CKPool service to ensure log file is reopened..."
    if ! systemctl reload "$SERVICE_NAME" 2>/dev/null; then
        echo "Warning: Reload not supported; consider restarting CKPool if needed."
        echo "To restart manually: sudo systemctl restart $SERVICE_NAME"
    fi
fi

echo "Successfully purged $LOG_FILE."

exit 0
