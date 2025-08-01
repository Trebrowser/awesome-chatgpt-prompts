#!/bin/bash

# Deskhog App Launcher Script
# This script ensures dependencies are installed and launches the Deskhog app

echo "🖥️  Starting Deskhog - Zoom Disconnect Tool"
echo "==========================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ Error: pip is not available"
    echo "Please install pip for Python 3 and try again."
    exit 1
fi

echo "✅ pip found"

# Install dependencies if they don't exist
echo "📦 Checking dependencies..."

# Check if psutil is installed
if ! python3 -c "import psutil" &> /dev/null; then
    echo "📦 Installing psutil..."
    if command -v pip3 &> /dev/null; then
        pip3 install psutil --user
    else
        python3 -m pip install psutil --user
    fi
else
    echo "✅ psutil is already installed"
fi

# Check if tkinter is available (usually comes with Python)
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ Error: tkinter is not available"
    echo "On Ubuntu/Debian, install it with: sudo apt-get install python3-tk"
    echo "On CentOS/RHEL, install it with: sudo yum install tkinter"
    echo "On Fedora, install it with: sudo dnf install python3-tkinter"
    exit 1
else
    echo "✅ tkinter is available"
fi

# Optional: Install xdotool for better Zoom integration on Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v xdotool &> /dev/null; then
        echo "⚠️  Optional: xdotool not found. Installing for better Zoom integration..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y xdotool
        elif command -v yum &> /dev/null; then
            sudo yum install -y xdotool
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y xdotool
        elif command -v pacman &> /dev/null; then
            sudo pacman -S xdotool
        else
            echo "⚠️  Could not install xdotool automatically. Please install it manually for better functionality."
        fi
    else
        echo "✅ xdotool found"
    fi
fi

echo ""
echo "🚀 Launching Deskhog..."
echo ""

# Launch the application
cd "$SCRIPT_DIR"
python3 deskhog_app.py

echo ""
echo "👋 Deskhog has been closed. Thanks for using it!"