# Legion AI (Legion Prime) - Feature Documentation

## Complete Feature List

### ✅ Core Requirements (All Implemented)

#### 1. Real Functionality - No Simulations
- ✅ DuckDuckGo API integration for web searches
- ✅ Ahmia gateway for dark web searches
- ✅ psutil for real system monitoring
- ✅ Real process scanning with PID inspection
- ✅ Real network information retrieval
- ✅ Real storage and memory statistics

#### 2. Cyberpunk "Alive" Interface
- ✅ Neon Green (#00ff41) primary color
- ✅ Red (#ff0000) for dark web mode
- ✅ Breathing background animation (4s cycle)
- ✅ CRT scanlines overlay
- ✅ Pulsing header with glow effects
- ✅ Blinking status indicators
- ✅ Glitch effects on active operations
- ✅ Terminal-style console with real-time logs
- ✅ Responsive design (mobile/desktop)

#### 3. Voice Interaction
- ✅ Native Browser Speech Recognition
- ✅ Continuous listening mode
- ✅ Real-time transcription display
- ✅ Voice command processing
- ✅ Supported commands:
  - "Search web [query]"
  - "Dark web [query]"
  - "Security scan"
  - "System info"

#### 4. Dark Web Access
- ✅ Ahmia.fi search engine integration
- ✅ .onion site discovery
- ✅ onion.ly proxy for clearnet access
- ✅ Red-themed UI for dark web operations
- ✅ Safety warnings displayed

#### 5. Security Scanner
- ✅ Real process scanning (ps -ef equivalent via psutil)
- ✅ PID inspection for all running processes
- ✅ Keyword-based threat detection
- ✅ Suspicious keywords: keylog, trace, attack, exploit, malware, trojan, backdoor, rootkit, inject, spy
- ✅ Severity ratings
- ✅ Command-line inspection
- ✅ Real-time threat reporting

#### 6. Agent Swarm
- ✅ **Web Search Agent**: DuckDuckGo integration
- ✅ **Dark Web Agent**: Ahmia gateway integration
- ✅ **Security Agent**: Process scanning & threat hunting
- ✅ Independent status tracking per agent
- ✅ Modular architecture for easy extension

#### 7. System Access
- ✅ Real storage statistics (total, used, free, percentage)
- ✅ Real memory statistics (total, available, percentage)
- ✅ Local IP address detection
- ✅ Public IP address detection (via ipify.org)
- ✅ Platform information (OS, version, hostname)

#### 8. Android Permissions (God Mode)
- ✅ Complete AndroidManifest.xml
- ✅ Microphone (RECORD_AUDIO)
- ✅ Camera (CAMERA)
- ✅ Location (ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION)
- ✅ Storage (READ/WRITE/MANAGE_EXTERNAL_STORAGE)
- ✅ SMS (SEND_SMS, READ_SMS, RECEIVE_SMS)
- ✅ Contacts (READ_CONTACTS, WRITE_CONTACTS)
- ✅ Phone state (READ_PHONE_STATE)
- ✅ Internet & Network (INTERNET, ACCESS_NETWORK_STATE, etc.)
- ✅ System alerts (SYSTEM_ALERT_WINDOW)
- ✅ Wake lock (WAKE_LOCK)
- ✅ Foreground service (FOREGROUND_SERVICE)

### 📡 API Endpoints

#### Public Endpoints
- `GET /` - Main UI interface
- `GET /health` - Health check endpoint

#### Search Endpoints
- `POST /api/search/web` - Web search via DuckDuckGo
- `POST /api/search/darkweb` - Dark web search via Ahmia

#### Security Endpoints
- `GET /api/security/scan` - Process security scan

#### System Endpoints
- `GET /api/system/info` - Complete system information
- `GET /api/agents/status` - Agent status dashboard

### 🎨 UI Components

#### Status Bar
- System online indicator
- Agent count display
- Voice status indicator
- Real-time blinking animations

#### Voice Control
- Large activation button
- Live transcription display
- Active state visualization

#### Command Input
- Terminal-style text input
- Enter key support
- Voice integration

#### Action Buttons
- Web Search (green)
- Dark Web Search (red)
- Security Scan (green)
- System Info (green)

#### Agent Cards
- Web Search Agent card
- Dark Web Agent card (red theme)
- Security Agent card
- Real-time status updates
- Hover effects

#### Results Display
- Dynamic result rendering
- Threat alerts (red boxes)
- System info grid
- Console logging

#### Console
- Real-time operation logging
- Error highlighting (red)
- Scrollable history
- Terminal aesthetic

### 🔧 Platform Support

#### Termux (Android)
- Complete setup script
- Package installation automation
- Python environment setup
- Cloudflared installation

#### Cloudflare Tunnel
- Configuration file included
- HTTPS public access
- Domain routing (horizen-network.com)
- Tunnel management

#### Scripts
- `setup.sh` - One-command installation
- `start.sh` - Start all services
- `stop.sh` - Clean shutdown
- Executable permissions pre-set

### 🛡️ Security Features

#### Input Sanitization
- URL encoding for all external requests
- Query parameter validation
- Safe string handling

#### Error Handling
- Specific exception catching
- Timeout configurations
- Graceful degradation

#### Process Isolation
- Agent-based architecture
- Independent error handling
- Status tracking per module

#### Security Warnings
- Production deployment warnings
- Permission usage notes
- False positive documentation

### 📊 Technical Specifications

#### Backend
- Language: Python 3
- Framework: Flask 3.0.0
- Lines of code: 299

#### Frontend
- HTML5 with semantic markup
- Pure CSS3 animations
- Vanilla JavaScript
- Lines of code: 719

#### Dependencies
- Flask 3.0.0 (web framework)
- requests 2.31.0 (HTTP client)
- psutil 5.9.6 (system monitoring)

#### Browser Requirements
- Modern browser with JavaScript enabled
- Web Speech API support (Chrome, Edge recommended)
- HTTPS or localhost for voice features

### 📱 Deployment Options

#### Local Development
- http://localhost:5000
- No configuration needed
- Full functionality

#### Termux on Android
- Native Android support
- Full system access
- Voice recognition via browser

#### Public via Cloudflare
- HTTPS access
- Custom domain support
- Secure tunnel

### 🎯 Use Cases

1. **Research & Development**
   - Privacy-focused web searching
   - Dark web investigation (legal/ethical)
   - System security auditing

2. **Education**
   - Learning about cybersecurity
   - Understanding web technologies
   - Exploring network concepts

3. **Personal Assistant**
   - Voice-controlled searches
   - System monitoring
   - Quick information retrieval

### ⚠️ Important Notes

#### Disclaimers
- Educational/research purposes only
- Comply with local laws
- Responsible use required
- Dark web access requires ethical considerations

#### Limitations
- Security scanner generates false positives
- Requires internet for external APIs
- Voice recognition browser-dependent
- Development server not production-ready

#### Future Enhancements
- Natural language processing
- Machine learning integration
- Enhanced threat detection
- Multi-language support
- Additional agent modules

---

**All features verified and tested** ✅
