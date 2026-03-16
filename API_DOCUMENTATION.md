# Legion AI API Documentation

## Base URL

```
http://localhost:5000
```

For production (with Cloudflare Tunnel):
```
https://horizen-network.com
```

## Endpoints

### 1. Health Check

Check if the server is online and get basic information.

**Endpoint:** `GET /status`

**Response:**
```json
{
  "status": "online",
  "ai_name": "Legion Prime",
  "domain": "https://horizen-network.com",
  "version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:5000/status
```

---

### 2. Web Interface

Access the main Legion AI web interface.

**Endpoint:** `GET /`

**Response:** HTML page with cyberpunk interface

**Example:**
```bash
# Open in browser
http://localhost:5000
```

---

### 3. Search Query

Perform a web search using DuckDuckGo.

**Endpoint:** `POST /query`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "your search query"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "query": "your search query",
  "ai_name": "Legion Prime",
  "domain": "https://horizen-network.com",
  "results": [
    {
      "title": "Result Title",
      "url": "https://example.com",
      "snippet": "Brief description of the result..."
    }
  ]
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Error description"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence"}'
```

**Python Example:**
```python
import requests

response = requests.post(
    'http://localhost:5000/query',
    json={'query': 'artificial intelligence'}
)

data = response.json()
if data['status'] == 'success':
    for result in data['results']:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}\n")
```

**JavaScript Example:**
```javascript
fetch('http://localhost:5000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({query: 'artificial intelligence'})
})
.then(response => response.json())
.then(data => {
  if (data.status === 'success') {
    data.results.forEach(result => {
      console.log('Title:', result.title);
      console.log('URL:', result.url);
      console.log('Snippet:', result.snippet);
    });
  }
});
```

---

### 4. Fetch Webpage Content

Fetch and parse the content of a specific webpage.

**Endpoint:** `POST /fetch`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response (Success):**
```json
{
  "status": "success",
  "url": "https://example.com",
  "content": "Extracted text content from the webpage (first 1000 characters)..."
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "Failed to fetch content"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/fetch \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Python Example:**
```python
import requests

response = requests.post(
    'http://localhost:5000/fetch',
    json={'url': 'https://example.com'}
)

data = response.json()
if data['status'] == 'success':
    print(f"Content from {data['url']}:")
    print(data['content'])
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request (missing parameters, etc.)
- `500 Internal Server Error` - Server error

Error responses include a JSON body with details:
```json
{
  "status": "error",
  "message": "Description of what went wrong"
}
```

---

## Rate Limiting

The server uses DuckDuckGo for search, which has its own rate limiting. If you make too many requests in a short time, you may receive empty results or errors.

**Best Practices:**
- Add delays between requests (recommended: 1-2 seconds)
- Cache results when possible
- Handle errors gracefully

---

## CORS

The server does not currently implement CORS headers. If you need to access the API from a web application on a different domain, you'll need to:

1. Set up a proxy
2. Run the client and server on the same domain
3. Modify `web_server.py` to add CORS headers

**Adding CORS (if needed):**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

---

## Security Considerations

1. **Input Validation**: All user input is sanitized to prevent XSS attacks
2. **HTTPS**: Use Cloudflare Tunnel for encrypted connections in production
3. **Authentication**: Not implemented - add if needed for production
4. **Rate Limiting**: Not implemented - consider adding for production

---

## Integration Examples

### cURL Integration
```bash
#!/bin/bash
# Search and save results

QUERY="cybersecurity news"
RESPONSE=$(curl -s -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$QUERY\"}")

echo "$RESPONSE" | jq '.results[] | .title'
```

### Python Integration
```python
import requests
import json

class LegionAIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def search(self, query):
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query}
        )
        return response.json()
    
    def fetch_page(self, url):
        response = requests.post(
            f"{self.base_url}/fetch",
            json={"url": url}
        )
        return response.json()
    
    def status(self):
        response = requests.get(f"{self.base_url}/status")
        return response.json()

# Usage
client = LegionAIClient()
results = client.search("machine learning")
print(json.dumps(results, indent=2))
```

### Node.js Integration
```javascript
const axios = require('axios');

class LegionAIClient {
  constructor(baseURL = 'http://localhost:5000') {
    this.client = axios.create({ baseURL });
  }

  async search(query) {
    const response = await this.client.post('/query', { query });
    return response.data;
  }

  async fetchPage(url) {
    const response = await this.client.post('/fetch', { url });
    return response.data;
  }

  async status() {
    const response = await this.client.get('/status');
    return response.data;
  }
}

// Usage
const legion = new LegionAIClient();
legion.search('artificial intelligence')
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

---

## WebSocket Support

Currently not implemented. If you need real-time updates, consider:
1. Using long polling
2. Implementing Server-Sent Events (SSE)
3. Adding WebSocket support with Flask-SocketIO

---

## Future Enhancements

Planned features:
- [ ] Authentication system
- [ ] Rate limiting
- [ ] Caching layer
- [ ] WebSocket support
- [ ] Multiple search engine support
- [ ] Advanced AI processing
- [ ] User sessions
- [ ] Search history
- [ ] API key management

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/irishbyblood/Legion-project/issues
- Documentation: See README.md

---

## License

See LICENSE file for details.
