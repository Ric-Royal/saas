#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if generate_secrets.py exists
if [ ! -f "scripts/generate_secrets.py" ]; then
    echo "Error: Required script generate_secrets.py is missing."
    exit 1
fi

echo "Setting up environment files..."
python3 scripts/generate_secrets.py

if [ $? -eq 0 ]; then
    echo -e "\n✅ Environment setup completed successfully!"
    echo "Note: Make sure to securely store the generated secrets and never commit them to version control."
else
    echo -e "\n❌ Environment setup failed. Please check the errors above and fix them."
    exit 1
fi 