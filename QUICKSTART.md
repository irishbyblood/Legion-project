# Quick Start Guide - Legion AI

Get Legion AI up and running in 3 minutes!

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/irishbyblood/Legion-project.git
cd Legion-project

# Run setup script
bash setup.sh

# Start the server
bash run.sh bg
```

### Option 2: Manual Setup
```bash
# Clone the repository
git clone https://github.com/irishbyblood/Legion-project.git
cd Legion-project

# Install dependencies
pip install -r requirements.txt

# Start the server
python interface/web_server.py
```

## 📱 Access the Interface

Once the server is running, open your browser:
```
http://localhost:5000
```

Or from another device on the same network:
```
http://<your-ip>:5000
```

## ✅ Verify Installation

Test the API endpoint:
```bash
curl http://localhost:5000/status
```

Expected response:
```json
{
  "status": "online",
  "ai_name": "Legion Prime",
  "domain": "https://horizen-network.com",
  "version": "1.0.0"
}
```

## 🔍 Try a Search

In your terminal:
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence"}'
```

Or use the web interface:
1. Open `http://localhost:5000` in your browser
2. Type your query in the terminal-style input
3. Click "EXECUTE" or press Enter
4. View results in the cyberpunk interface

## 🛑 Stop the Server

If running in background:
```bash
# Find the process
ps aux | grep web_server.py

# Kill it (replace PID with actual process ID)
kill <PID>
```

## 📱 Termux Quick Start

On Android with Termux:

```bash
# Install required packages
pkg update && pkg upgrade
pkg install python git

# Clone and setup
git clone https://github.com/irishbyblood/Legion-project.git
cd Legion-project
pip install -r requirements.txt

# Start server
python interface/web_server.py &

# Open in browser
termux-open-url http://localhost:5000
```

## 🌐 Public Access (Optional)

To make Legion AI accessible from the internet:

1. Install Cloudflare Tunnel (see TERMUX_SETUP.md)
2. Configure tunnel to point to localhost:5000
3. Access via your custom domain

## 🔧 Common Issues

### Port Already in Use
```bash
# Use a different port
PORT=8080 python interface/web_server.py
```

### Dependencies Not Found
```bash
# Upgrade pip and reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

### Can't Access from Another Device
- Make sure both devices are on the same network
- Check firewall settings
- Verify server is running on 0.0.0.0 (it should be by default)

## 📚 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API usage
- See [TERMUX_SETUP.md](TERMUX_SETUP.md) for Android setup
- Review [SECURITY_SUMMARY.md](SECURITY_SUMMARY.md) for security info

## 🎨 Interface Features

- **Terminal-style Console**: Real-time output with neon green theme
- **Web Search**: Powered by DuckDuckGo
- **Cyberpunk Theme**: Glitch effects and animations
- **Mobile Responsive**: Works on phones and tablets
- **Real-time Results**: No simulations, real functionality

## 💡 Pro Tips

1. Use `bash run.sh bg` to run in background
2. Set `SECRET_KEY` environment variable for production
3. Deploy behind Cloudflare Tunnel for public access
4. Check logs at `/tmp/legion_server.log` if issues occur
5. Press Ctrl+L to clear the console in the web interface

## 🎯 That's It!

You're now running Legion AI! Start exploring the cyberpunk interface and enjoy the real-time search capabilities.

---

**Need Help?** Check the documentation or open an issue on GitHub.
