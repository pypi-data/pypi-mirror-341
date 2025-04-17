#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install uv if not already installed
pip install uv

# Install the package with uv
uv pip install -e .

echo "Installation complete. You can now run the server with 'python run_server.py'" 