#!/bin/bash

echo "Starting Satisfactory Production Calculator..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./install.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run streamlit_app.py
