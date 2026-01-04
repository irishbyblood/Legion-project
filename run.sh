#!/bin/bash
# Legion AI Run Script

echo "Starting Legion AI (Legion Prime)..."
echo ""

# Check if server is already running
if pgrep -f "web_server.py" > /dev/null; then
    echo "⚠️  Legion AI is already running!"
    echo ""
    echo "To stop it, run: pkill -f web_server.py"
    echo "Or check the process: ps aux | grep web_server.py"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to project directory
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if dependencies are installed
echo "Checking dependencies..."
python3 -c "import flask" 2>/dev/null || { echo "❌ flask not installed"; exit 1; }
python3 -c "import requests" 2>/dev/null || { echo "❌ requests not installed"; exit 1; }
python3 -c "from duckduckgo_search import DDGS" 2>/dev/null || { echo "❌ duckduckgo-search not installed"; exit 1; }
python3 -c "from bs4 import BeautifulSoup" 2>/dev/null || { echo "❌ beautifulsoup4 not installed"; exit 1; }

if [ $? -ne 0 ]; then
    echo ""
    echo "Run: pip install -r requirements.txt"
    echo "Or: bash setup.sh"
    exit 1
fi

echo "✅ Dependencies OK"
echo ""

# Get port from environment or use default
PORT=${PORT:-5000}

# Start the server
echo "🚀 Starting server on port $PORT..."
echo ""

# Run in background or foreground based on argument
if [ "$1" == "background" ] || [ "$1" == "bg" ] || [ "$1" == "-b" ]; then
    python3 interface/web_server.py > /tmp/legion_server.log 2>&1 &
    SERVER_PID=$!
    sleep 2
    
    if ps -p $SERVER_PID > /dev/null; then
        echo "✅ Server started successfully in background!"
        echo "   PID: $SERVER_PID"
        echo "   Logs: /tmp/legion_server.log"
    else
        echo "❌ Failed to start server. Check logs: /tmp/legion_server.log"
        exit 1
    fi
else
    echo "Starting in foreground mode..."
    echo "Press Ctrl+C to stop"
    echo ""
    python3 interface/web_server.py
fi

echo ""
echo "==============================================="
echo "  Legion AI is running!"
echo "==============================================="
echo ""
echo "Access the interface at:"
echo "  http://localhost:$PORT"
echo ""
echo "Check status:"
echo "  curl http://localhost:$PORT/status"
echo ""
echo "To stop (if running in background):"
echo "  pkill -f web_server.py"
echo ""
echo "==============================================="
