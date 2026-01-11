#!/bin/bash
set -e

echo "🚀 AI-as-Me Setup Script"
echo "========================"

# Detect project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "📂 Project root: $PROJECT_ROOT"

# Check Python version
echo ""
echo "🐍 Checking Python version..."
PYTHON_CMD=$(command -v python3 || command -v python)
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Check if Python >= 3.10
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ Python 3.10+ required, found $PYTHON_VERSION"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -e . --user --quiet
echo "✓ Dependencies installed"

# Create runtime directories
echo ""
echo "📁 Creating runtime directories..."
mkdir -p soul kanban/{inbox,todo,doing,done} logs
echo "✓ Runtime directories created"

# Check for .env file
echo ""
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and set your DEEPSEEK_API_KEY"
else
    echo "✓ .env file exists"
fi

# Setup systemd service (optional)
echo ""
read -p "📋 Setup systemd service? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SERVICE_FILE="$HOME/.config/systemd/user/ai-as-me.service"
    mkdir -p "$HOME/.config/systemd/user"
    
    # Generate service file from template
    sed -e "s|%USER%|$USER|g" \
        -e "s|%WORKING_DIR%|$PROJECT_ROOT|g" \
        -e "s|%PATH%|$PATH|g" \
        -e "s|%PYTHON%|$PYTHON_CMD|g" \
        scripts/ai-as-me.service.template > "$SERVICE_FILE"
    
    echo "✓ Service file created: $SERVICE_FILE"
    
    # Enable and start service
    systemctl --user daemon-reload
    systemctl --user enable ai-as-me.service
    
    echo "✓ Service enabled"
    echo ""
    echo "To start the service:"
    echo "  systemctl --user start ai-as-me"
    echo ""
    echo "To check status:"
    echo "  systemctl --user status ai-as-me"
fi

# Check storage (SD card detection for RDK X5)
echo ""
echo "💾 Checking storage..."
if [ -d "/media/sdcard" ]; then
    echo "✓ SD card detected at /media/sdcard"
elif [ -d "/mnt/sdcard" ]; then
    echo "✓ SD card detected at /mnt/sdcard"
else
    echo "ℹ️  No SD card mount detected (optional)"
fi

# Final summary
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and set your DEEPSEEK_API_KEY"
echo "2. Run: ai-as-me status"
echo "3. Run: ai-as-me run"
echo ""
echo "For help: ai-as-me --help"
