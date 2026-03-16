# ⚡ Legion AI (Legion Prime) ⚡

**High-Tech Cyberpunk AI Assistant with Dark Web Access**

Legion AI is a powerful, real-time AI assistant designed for Android (via Termux) with cyberpunk aesthetics, voice control, and advanced capabilities including dark web search and security scanning.

## 🎯 Features

### Core Capabilities
- **🌐 Web Search Agent**: Real-time search using DuckDuckGo API
- **🕵️ Dark Web Agent**: Access .onion sites via Ahmia gateway with onion.ly proxy
- **🔒 Security Agent**: Huntress-style threat hunting and process scanning
- **📊 System Monitoring**: Real-time storage, memory, and network information
- **🎤 Voice Interface**: Continuous speech recognition for hands-free operation

### Visual Experience
- **Cyberpunk UI**: Neon green (#00ff41) theme with red alerts for dark web
- **Breathing Backgrounds**: Animated grid with scaling effects
- **CRT Scanlines**: Authentic retro-futuristic display effect
- **Glitch Effects**: Dynamic animations during active operations
- **Terminal Console**: Real-time operation logging

### Platform Support
- **Android**: Full support via Termux
- **Cloudflare Tunnel**: Public HTTPS access to your local instance
- **Domain**: Configured for horizen-network.com

## 📋 Requirements

### Android (Termux)
- Android device (5.0+)
- [Termux](https://f-droid.org/en/packages/com.termux/) installed from F-Droid
- Internet connection
- Microphone access for voice commands

### Permissions
The APK requires "God Mode" permissions:
- 🎤 Microphone (voice commands)
- 📷 Camera
- 📍 Location
- 💾 Storage (read/write)
- 📱 SMS (read/send)
- 👥 Contacts (read/write)
- 🌐 Internet & Network

## 🚀 Installation

### 1. Install Termux
Download from F-Droid (NOT Google Play):
```bash
https://f-droid.org/en/packages/com.termux/
```

### 2. Clone Repository
```bash
pkg install git
git clone https://github.com/irishbyblood/Legion-project.git
cd Legion-project
```

### 3. Run Setup
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Update Termux packages
- Install Python 3 and pip
- Install all Python dependencies
- Download and install cloudflared

### 4. Configure Cloudflare Tunnel (Optional)
For public HTTPS access:

```bash
# Login to Cloudflare
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create legion-prime-tunnel

# Copy credentials to expected location
cp ~/.cloudflared/*.json ~/.cloudflared/credentials.json

# Configure DNS
# Point horizen-network.com to your tunnel
cloudflared tunnel route dns legion-prime-tunnel horizen-network.com
```

## 🎮 Usage

### Start Legion AI
```bash
./start.sh
```

This starts:
1. Flask web server on `http://localhost:5000`
2. Cloudflare tunnel (if configured)

### Access the Interface

**Local Access:**
```
http://localhost:5000
```

**Public Access (with tunnel):**
```
https://horizen-network.com
```

### Voice Commands

Click "🎤 ACTIVATE VOICE INTERFACE" or use these voice commands:
- "Search web [query]" - Web search
- "Dark web [query]" - Dark web search
- "Security scan" - Run security scan
- "System info" - Display system information

### API Endpoints

#### Web Search
```bash
POST /api/search/web
Content-Type: application/json

{
  "query": "artificial intelligence"
}
```

#### Dark Web Search
```bash
POST /api/search/darkweb
Content-Type: application/json

{
  "query": "privacy tools"
}
```

#### Security Scan
```bash
GET /api/security/scan?type=processes
```

#### System Information
```bash
GET /api/system/info
```

#### Agent Status
```bash
GET /api/agents/status
```

### Stop Legion AI
```bash
./stop.sh
```

## 🔧 Configuration

### Web Server
Edit `web_server.py` to customize:
- Port (default: 5000)
- Agent behavior
- Security keywords
- API endpoints

### Cloudflare Tunnel
Edit `cloudflared-config.yml` to configure:
- Tunnel name
- Domain routing
- Service endpoints

### Android Manifest
`AndroidManifest.xml` defines all required permissions for the APK build.

## 🏗️ Architecture

### Agent Swarm
Legion AI uses a modular agent architecture:

```python
# Base Agent
class LegionAgent:
    - name
    - description
    - status
    - execute()

# Specialized Agents
- WebSearchAgent: DuckDuckGo API integration
- DarkWebAgent: Ahmia + onion.ly proxy
- SecurityAgent: Process scanning & threat detection
```

### Tech Stack
- **Backend**: Python 3 + Flask
- **Frontend**: HTML5 + CSS3 + JavaScript
- **APIs**: DuckDuckGo, Ahmia, ipify
- **System**: psutil for process/system monitoring
- **Tunnel**: Cloudflare cloudflared

## 🔒 Security

### Security Scanner
Scans running processes for suspicious keywords:
- keylog, trace, attack, exploit
- malware, trojan, backdoor, rootkit
- inject, spy

### Dark Web Access
- Uses Ahmia search engine for .onion indexing
- Proxies .onion sites via onion.ly for clearnet access
- ⚠️ **Warning**: Use Tor Browser for true anonymity

### Privacy
- No telemetry or tracking
- All searches use privacy-focused DuckDuckGo
- Local processing of system data

## 📱 Building APK

To build as Android APK (requires additional setup):

1. Install Buildozer:
```bash
pip install buildozer
```

2. Create buildozer.spec:
```bash
buildozer init
```

3. Configure buildozer.spec with AndroidManifest.xml permissions

4. Build:
```bash
buildozer android debug
```

## 🎨 UI Theme

### Color Scheme
- **Primary**: Neon Green (#00ff41)
- **Background**: Dark (#0a0a0a)
- **Alerts**: Red (#ff0000)
- **Accents**: Cyan (#00ffff)

### Animations
- Breathing backgrounds (4s cycle)
- Pulsing headers (2s cycle)
- Blinking status indicators (1s cycle)
- Glitch effects on active states

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
pkill -f "python web_server.py"
```

### Speech Recognition Not Working
- Ensure microphone permissions are granted
- Use HTTPS (required for Web Speech API)
- Check browser compatibility (Chrome/Edge recommended)

### Cloudflare Tunnel Issues
```bash
# Check tunnel status
cloudflared tunnel list

# View logs
cloudflared tunnel run legion-prime-tunnel --loglevel debug
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📄 License

See [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

Legion AI is for educational and research purposes. Users are responsible for:
- Complying with local laws regarding security scanning
- Ethical use of dark web search capabilities
- Proper handling of system permissions
- Respecting privacy and security policies

Dark web access should only be used for legitimate research purposes.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

## 🎯 Roadmap

Future enhancements:
- [ ] Natural language processing
- [ ] Additional agent types
- [ ] Machine learning integration
- [ ] Enhanced threat detection
- [ ] Mobile app build automation
- [ ] Multi-language support

---

**⚡ Legion AI - Neural Network Online ⚡**

*Built with Python, powered by cyberpunk aesthetics*