#!/bin/bash
set -e

echo "🗑️  AI-as-Me Uninstall Script"
echo "============================"

# Stop and disable service if exists
if systemctl --user is-active --quiet ai-as-me 2>/dev/null; then
    echo "🛑 Stopping service..."
    systemctl --user stop ai-as-me
    echo "✓ Service stopped"
fi

if systemctl --user is-enabled --quiet ai-as-me 2>/dev/null; then
    echo "🔓 Disabling service..."
    systemctl --user disable ai-as-me
    echo "✓ Service disabled"
fi

# Remove service file
SERVICE_FILE="$HOME/.config/systemd/user/ai-as-me.service"
if [ -f "$SERVICE_FILE" ]; then
    echo "🗑️  Removing service file..."
    rm "$SERVICE_FILE"
    systemctl --user daemon-reload
    echo "✓ Service file removed"
fi

echo ""
echo "✅ Uninstall complete!"
echo ""
echo "Note: Project files and data are preserved."
echo "To remove completely, delete the project directory."
