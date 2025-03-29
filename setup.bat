#!/bin/bash

echo "Setting up the environment..."

if ! command -v python3 &>/dev/null; then
    echo "Error: Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

if ! command -v pip &>/dev/null; then
    echo "Error: pip is not installed. Please install pip and try again."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! You can now use the tools."

exit 0
