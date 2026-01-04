#!/bin/bash
# Legion AI Start Script

echo "======================================"
echo "  Starting Legion AI (Legion Prime)"
echo "======================================"
echo ""

# Start Flask server in background
echo "[*] Starting Flask web server on port 5000..."
python web_server.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 3

# Start Cloudflare tunnel
echo "[*] Starting Cloudflare tunnel..."
cloudflared tunnel --config cloudflared-config.yml run legion-prime-tunnel &
TUNNEL_PID=$!

echo ""
echo "======================================"
echo "  Legion AI is now ONLINE"
echo "======================================"
echo ""
echo "Local Access: http://localhost:5000"
echo "Public Access: https://horizen-network.com"
echo ""
echo "Press Ctrl+C to stop..."
echo ""

# Save PIDs for cleanup
echo $FLASK_PID > /tmp/legion_flask.pid
echo $TUNNEL_PID > /tmp/legion_tunnel.pid

# Wait for user interrupt
trap 'kill $FLASK_PID $TUNNEL_PID; rm -f /tmp/legion_flask.pid /tmp/legion_tunnel.pid; echo "Legion AI stopped."; exit' INT
wait
