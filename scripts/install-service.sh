#!/bin/bash
# Install AI-as-Me as systemd service

set -e

SERVICE_NAME="ai-as-me"
WORKING_DIR="$(cd "$(dirname "$0")/.." && pwd)"
USER_NAME="$(whoami)"

# Check if running as root for system-wide install
if [ "$EUID" -eq 0 ]; then
    SERVICE_DIR="/etc/systemd/system"
    echo "Installing system-wide service..."
else
    SERVICE_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SERVICE_DIR"
    echo "Installing user service..."
fi

# Generate service file
cat > "$SERVICE_DIR/$SERVICE_NAME.service" << EOF
[Unit]
Description=AI-as-Me Personal AI Agent
After=network.target

[Service]
Type=simple
WorkingDirectory=$WORKING_DIR
Environment="PATH=$WORKING_DIR/venv/bin:/usr/local/bin:/usr/bin"
EnvironmentFile=$WORKING_DIR/.env
ExecStart=$WORKING_DIR/venv/bin/python -m ai_as_me.cli.main run --poll-interval 60
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload and enable
if [ "$EUID" -eq 0 ]; then
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    echo "✓ Service installed. Start with: sudo systemctl start $SERVICE_NAME"
else
    systemctl --user daemon-reload
    systemctl --user enable $SERVICE_NAME
    echo "✓ User service installed. Start with: systemctl --user start $SERVICE_NAME"
fi

echo "✓ View logs with: journalctl -u $SERVICE_NAME -f"
