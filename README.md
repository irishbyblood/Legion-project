# Legion AI (Legion Prime)

**High-Tech Cyberpunk AI Interface**

Domain: https://horizen-network.com  
Platform: Android (Termux + Flask + Cloudflare Tunnel)  
Theme: Neon Green (#00ff41) Cyberpunk Interface

## Features

- 🔍 Real-time web search using DuckDuckGo
- 🌐 Web scraping with BeautifulSoup4
- 💻 Terminal-style cyberpunk interface
- ⚡ Flask-based REST API
- 🎨 Neon green glitch effects
- 📱 Mobile-responsive design
- 🔒 Real functionality (no simulations)

## Installation

### 1. Install Dependencies

```bash
pip install flask requests duckduckgo-search beautifulsoup4
```

On Termux (Android):
```bash
pkg install python termux-api
pip install flask requests duckduckgo-search beautifulsoup4
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Run Server

```bash
python interface/web_server.py &
```

The server will start on `http://0.0.0.0:5000` by default.

### 3. Connect to Domain (Optional - Cloudflare Tunnel)

On Termux:
```bash
termux-chroot cloudflared tunnel run legion
```

This connects your local server to the Cloudflare tunnel for public access.

## Usage

### Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. You'll see the Legion Prime neural interface
3. Enter your query in the terminal-style input
4. Click "EXECUTE" or press Enter
5. View search results in the cyberpunk-themed interface

### API Endpoints

#### Query Endpoint
```bash
POST /query
Content-Type: application/json

{
  "query": "your search query"
}
```

Response:
```json
{
  "status": "success",
  "query": "your search query",
  "results": [
    {
      "title": "Result title",
      "url": "https://example.com",
      "snippet": "Result description..."
    }
  ]
}
```

#### Status Endpoint
```bash
GET /status
```

Response:
```json
{
  "status": "online",
  "ai_name": "Legion Prime",
  "domain": "https://horizen-network.com",
  "version": "1.0.0"
}
```

#### Fetch Webpage Content
```bash
POST /fetch
Content-Type: application/json

{
  "url": "https://example.com"
}
```

## Project Structure

```
Legion-project/
├── interface/
│   ├── web_server.py         # Flask server and Legion AI core
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # Cyberpunk styling
│   │   └── js/
│   │       └── main.js       # Frontend JavaScript
│   └── templates/
│       └── index.html        # Main HTML template
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Customization

### Change Theme Color

Edit `interface/web_server.py`:
```python
self.theme_color = "#00ff41"  # Change to your color
```

Edit `interface/static/css/style.css`:
```css
--neon-green: #00ff41;  /* Change to your color */
```

### Change Port

```bash
PORT=8080 python interface/web_server.py
```

## Security Notes

- The server binds to `0.0.0.0` to allow external connections
- Input is sanitized to prevent XSS attacks
- Use behind a reverse proxy (like Cloudflare Tunnel) for production

## Troubleshooting

### Dependencies Not Installing

Make sure you have pip updated:
```bash
pip install --upgrade pip
```

### Server Not Accessible

Check if port 5000 is available:
```bash
netstat -tulpn | grep 5000
```

### Search Not Working

Verify DuckDuckGo search is working:
```python
from duckduckgo_search import DDGS
with DDGS() as ddgs:
    results = ddgs.text("test query", max_results=5)
    print(list(results))
```

## License

See LICENSE file for details.

## Credits

- Flask Framework
- DuckDuckGo Search API
- BeautifulSoup4
- Cloudflare Tunnel