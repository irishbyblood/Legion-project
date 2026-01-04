# Legion-project

A Flask-based web server with search and scraping capabilities, designed to run on Termux with Cloudflare Tunnel support.

## Features

- 🔍 Web search functionality using DuckDuckGo
- 🌐 Web scraping capabilities with BeautifulSoup4
- 🚀 Flask-based REST API
- 🔒 Cloudflare Tunnel integration for secure remote access
- 📱 Termux-compatible

## Installation

### 1. Install Python Dependencies

```bash
pip install flask requests duckduckgo-search beautifulsoup4
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Install Termux API (Termux only)

If running on Termux, install the Termux API package:

```bash
pkg install termux-api
```

### 3. Install Cloudflare Tunnel (Optional)

For remote access via Cloudflare Tunnel:

```bash
# Download and install cloudflared
# Visit: https://github.com/cloudflare/cloudflared/releases
# Or on Termux:
pkg install cloudflared
```

## Usage

### Running the Web Server

Start the web server in the background:

```bash
python interface/web_server.py &
```

The server will run on `http://0.0.0.0:5000` by default.

### Accessing the Web Interface

Once the server is running, you can access:

- **Main Interface**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/health`

### API Endpoints

#### Search API
```bash
POST /api/search
Content-Type: application/json

{
  "query": "your search query"
}
```

#### Scrape API
```bash
POST /api/scrape
Content-Type: application/json

{
  "url": "https://example.com"
}
```

### Using Cloudflare Tunnel

To expose your server through Cloudflare Tunnel:

```bash
# First, authenticate (one-time setup)
cloudflared tunnel login

# Create a tunnel named "legion"
cloudflared tunnel create legion

# Run the tunnel
cloudflared tunnel run legion
```

Or in Termux with chroot:

```bash
termux-chroot cloudflared tunnel run legion
```

**Note**: You'll need to configure your tunnel to route to `localhost:5000`. Create a `config.yml` file for cloudflared:

```yaml
tunnel: <your-tunnel-id>
credentials-file: /path/to/credentials.json

ingress:
  - hostname: your-domain.com
    service: http://localhost:5000
  - service: http_status:404
```

## Complete Setup Example

Here's the complete setup process:

```bash
# 1. Install Dependencies
pip install flask requests duckduckgo-search beautifulsoup4
pkg install termux-api

# 2. Run Server
python interface/web_server.py &

# 3. Connect to Domain (with configured tunnel)
termux-chroot cloudflared tunnel run legion
```

## Development

### Project Structure

```
Legion-project/
├── interface/
│   └── web_server.py      # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

### Testing the Server

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

Test the search API:

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'
```

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, you can modify the port in `interface/web_server.py`:

```python
app.run(host='0.0.0.0', port=8080, debug=False)  # Change port to 8080
```

### Cloudflare Tunnel Not Connecting

1. Ensure cloudflared is properly authenticated: `cloudflared tunnel login`
2. Verify tunnel configuration in `config.yml`
3. Check that the local server is running: `curl http://localhost:5000/health`

### DuckDuckGo Search Issues

If search is not working, ensure you have internet connectivity and the `duckduckgo-search` package is properly installed:

```bash
pip install --upgrade duckduckgo-search
```

## License

See LICENSE file for details.
