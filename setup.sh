#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print help message
print_help() {
  echo "Usage: ./setup.sh [--help]"
  echo
  echo "This script:"
  echo "  1. Extracts dependencies from pyproject.toml"
  echo "  2. Creates requirements.txt"
  echo "  3. Creates a .venv virtual environment"
  echo "  4. Installs dependencies using pip"
  echo
  echo "Options:"
  echo "  --help        Show this help message"
}

# Check for --help flag
if [[ "$1" == "--help" ]]; then
  print_help
  exit 0
fi

echo "📦 Generating requirements.txt from pyproject.toml..."

# Check that pyproject.toml exists
if [ ! -f pyproject.toml ]; then
  echo "❌ pyproject.toml not found in current directory."
  exit 1
fi

# Check for available Python 3.10+ interpreter
PYTHON=$(command -v python3.10 || command -v python3)
if [ -z "$PYTHON" ]; then
  echo "❌ Python 3.10+ is not installed."
  exit 1
fi

# Extract dependencies from pyproject.toml using sed
REQS=$(sed -n '/^\[project\]/,/^\[.*\]/p' pyproject.toml \
  | sed -n '/dependencies = \[/,/]/p' \
  | sed -e '1d' -e '$d' -e 's/[",]//g' -e 's/^[[:space:]]*//')

if [ -z "$REQS" ]; then
  echo "⚠️ No dependencies found in pyproject.toml."
  exit 0
fi

# Write to requirements.txt
echo "$REQS" > requirements.txt
echo "✅ requirements.txt created."

# Create .venv virtual environment
echo "🐍 Creating virtual environment (.venv)..."
$PYTHON -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies using pip
echo "📥 Installing dependencies via pip..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 Setup complete!"
