#!/bin/bash
# Legion AI Setup Script

echo "==============================================="
echo "  Legion AI (Legion Prime) Setup"
echo "  Cyberpunk Interface Installation"
echo "==============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo ""

if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dependencies installed successfully!"
else
    echo ""
    echo "❌ Failed to install dependencies."
    exit 1
fi

echo ""
echo "==============================================="
echo "  Installation Complete!"
echo "==============================================="
echo ""
echo "To start the server, run:"
echo "  python3 interface/web_server.py"
echo ""
echo "Or run in background:"
echo "  python3 interface/web_server.py &"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:5000"
echo ""
echo "==============================================="
