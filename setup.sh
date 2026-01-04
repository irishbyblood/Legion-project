#!/bin/bash
# Legion AI Setup Script for Termux on Android

echo "======================================"
echo "  Legion AI (Legion Prime) Setup"
echo "======================================"
echo ""

# Update packages
echo "[*] Updating Termux packages..."
pkg update -y
pkg upgrade -y

# Install Python and dependencies
echo "[*] Installing Python..."
pkg install python python-pip -y

# Install required Python packages
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install cloudflared for tunnel
echo "[*] Installing cloudflared..."
pkg install wget -y
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64 -O cloudflared
chmod +x cloudflared
mv cloudflared $PREFIX/bin/

# Create .cloudflared directory
mkdir -p ~/.cloudflared

echo ""
echo "======================================"
echo "  Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Authenticate cloudflared:"
echo "   cloudflared tunnel login"
echo ""
echo "2. Create a tunnel:"
echo "   cloudflared tunnel create legion-prime-tunnel"
echo ""
echo "3. Configure DNS for your domain (horizen-network.com)"
echo ""
echo "4. Start Legion AI:"
echo "   ./start.sh"
echo ""
