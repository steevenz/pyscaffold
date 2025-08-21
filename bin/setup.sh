#!/bin/bash
# PyScaffold Setup Script for Linux/macOS
# This script sets up the development environment for PyScaffold

set -e  # Exit on any error

# Parse command line arguments
CLEAN_MODE=false
SHOW_HELP=false

for arg in "$@"; do
    case $arg in
        --clean)
            CLEAN_MODE=true
            shift
            ;;
        --help)
            SHOW_HELP=true
            shift
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

if [ "$SHOW_HELP" = true ]; then
    echo "🚀 PyScaffold Setup Script"
    echo
    echo "Usage: ./bin/setup.sh [options]"
    echo
    echo "Options:"
    echo "  --clean    Clean setup: remove existing venv, clear pip cache, force reinstall"
    echo "  --help     Show this help message"
    echo
    exit 0
fi

if [ "$CLEAN_MODE" = true ]; then
    echo "🧹 Clean setup mode enabled"
    echo "🚀 Setting up PyScaffold development environment (CLEAN MODE)..."
else
    echo "🚀 Setting up PyScaffold development environment..."
fi
echo

# Check if Python 3.8+ is installed
echo "📋 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION found, but Python $REQUIRED_VERSION or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"
echo

# Handle clean setup - remove existing venv and clear cache
if [ "$CLEAN_MODE" = true ]; then
    echo "🧹 Cleaning up existing environment..."
    if [ -d "venv" ]; then
        echo "Removing existing virtual environment..."
        rm -rf venv
        echo "✅ Existing virtual environment removed"
    fi
    
    echo "Clearing pip cache..."
    python3 -m pip cache purge 2>/dev/null || true
    echo "✅ Pip cache cleared"
    echo
fi

# Create virtual environment
echo "🔧 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"
echo

# Install dependencies
INSTALL_FLAGS=""
if [ "$CLEAN_MODE" = true ]; then
    INSTALL_FLAGS="--force-reinstall --no-cache-dir"
    echo "📚 Installing dependencies (clean mode: force reinstall, no cache)..."
else
    echo "📚 Installing dependencies..."
fi

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt $INSTALL_FLAGS
    echo "✅ Dependencies installed from requirements.txt"
else
    echo "⚠️  requirements.txt not found, installing basic dependencies..."
    pip install textual rich pyyaml $INSTALL_FLAGS
fi
echo

# Install development dependencies if available
if [ -f "requirements-dev.txt" ]; then
    echo "🛠️  Installing development dependencies..."
    pip install -r requirements-dev.txt
    echo "✅ Development dependencies installed"
fi
echo

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p outputs
mkdir -p caches
echo "✅ Directories created"
echo

# Set executable permissions
echo "🔐 Setting executable permissions..."
chmod +x bin/setup.sh
chmod +x bin/setup.bat
chmod +x bin/setup.ps1
echo "✅ Permissions set"
echo

echo "🎉 Setup completed successfully!"
echo
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run PyScaffold: python run.py"
echo "  3. Or use CLI mode: python run.py --cli"

echo
echo "Happy coding! 🐍✨"