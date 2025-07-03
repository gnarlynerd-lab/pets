#!/bin/bash
# DKS Digital Pet System - Quick Start Script

echo "===== Setting up DKS Digital Pet System ====="

# Create virtual environment if it doesn't exist
if [ ! -d "dks_env" ]; then
    echo "Creating virtual environment..."
    python -m venv dks_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source dks_env/bin/activate

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
echo "PYTHONPATH set to: $PYTHONPATH"

# Install dependencies
echo "Installing Mesa package directly..."
pip install mesa --no-build-isolation

echo "Installing remaining dependencies..."
pip install -r requirements.txt

echo "===== Setup complete ====="
echo ""
echo "To start the backend server:"
echo "  python -m uvicorn backend.main:app --reload"
echo ""
echo "To start the frontend (in a different terminal):"
echo "  cd next && npm install && npm run dev"
echo ""
echo "For more information, see RUNNING_INSTRUCTIONS.md"
