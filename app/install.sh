#!/bin/bash

echo "===================================="
echo "Satisfactory Production Calculator"
echo "Installation Script (Linux/macOS)"
echo "===================================="
echo ""

echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 4: Checking Graphviz installation..."
if command -v dot &> /dev/null; then
    echo "[OK] Graphviz is installed at: $(which dot)"
else
    echo "[WARNING] Graphviz is NOT installed"
    echo "Please install Graphviz:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install graphviz"
    echo ""
    echo "Fedora:"
    echo "  sudo dnf install graphviz"
    echo ""
    echo "macOS:"
    echo "  brew install graphviz"
fi

echo ""
echo "===================================="
echo "Installation complete!"
echo "===================================="
echo ""
echo "To start the application, run:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  streamlit run streamlit_app.py"
echo ""
