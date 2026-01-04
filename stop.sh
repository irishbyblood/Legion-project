#!/bin/bash
# Legion AI Stop Script

echo "Stopping Legion AI..."

# Kill Flask server
if [ -f /tmp/legion_flask.pid ]; then
    FLASK_PID=$(cat /tmp/legion_flask.pid)
    kill $FLASK_PID 2>/dev/null
    rm -f /tmp/legion_flask.pid
    echo "Flask server stopped"
fi

# Kill Cloudflare tunnel
if [ -f /tmp/legion_tunnel.pid ]; then
    TUNNEL_PID=$(cat /tmp/legion_tunnel.pid)
    kill $TUNNEL_PID 2>/dev/null
    rm -f /tmp/legion_tunnel.pid
    echo "Cloudflare tunnel stopped"
fi

# Fallback: kill by process name
pkill -f "python web_server.py" 2>/dev/null
pkill -f "cloudflared" 2>/dev/null

echo "Legion AI stopped."
