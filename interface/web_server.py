#!/usr/bin/env python3
"""
Legion Project Web Server
A Flask-based web server for the Legion project with search capabilities.
"""

from flask import Flask, request, jsonify, render_template_string
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
REQUEST_TIMEOUT = 10  # Timeout for HTTP requests in seconds
MAX_CONTENT_LENGTH = 5000  # Maximum content length for scraped text
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

app = Flask(__name__)

# Simple HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legion Project</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .search-container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        #results {
            margin-top: 20px;
        }
        .result-item {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            border-left: 4px solid #007bff;
        }
        .result-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .result-link {
            color: #007bff;
            text-decoration: none;
            font-size: 14px;
        }
        .result-snippet {
            color: #666;
            margin-top: 5px;
            font-size: 14px;
        }
        .status {
            text-align: center;
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>🔍 Legion Project</h1>
    <div class="search-container">
        <h2>Search Engine</h2>
        <input type="text" id="searchQuery" placeholder="Enter your search query...">
        <button onclick="performSearch()">Search</button>
        <div id="results"></div>
    </div>

    <script>
        async function performSearch() {
            const query = document.getElementById('searchQuery').value;
            const resultsDiv = document.getElementById('results');
            
            if (!query.trim()) {
                resultsDiv.innerHTML = '<p class="status">Please enter a search query.</p>';
                return;
            }
            
            resultsDiv.innerHTML = '<p class="status">Searching...</p>';
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    resultsDiv.innerHTML = `<p class="status">Error: ${data.error}</p>`;
                    return;
                }
                
                if (data.results && data.results.length > 0) {
                    let html = '<h3>Search Results:</h3>';
                    data.results.forEach(result => {
                        html += `
                            <div class="result-item">
                                <div class="result-title">${result.title}</div>
                                <a href="${result.url}" class="result-link" target="_blank">${result.url}</a>
                                <div class="result-snippet">${result.snippet || ''}</div>
                            </div>
                        `;
                    });
                    resultsDiv.innerHTML = html;
                } else {
                    resultsDiv.innerHTML = '<p class="status">No results found.</p>';
                }
            } catch (error) {
                resultsDiv.innerHTML = `<p class="status">Error: ${error.message}</p>`;
            }
        }
        
        // Allow Enter key to trigger search
        document.getElementById('searchQuery').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page route"""
    logger.info("Home page accessed")
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/search', methods=['POST'])
def search():
    """API endpoint for searching using DuckDuckGo"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        logger.info(f"Search query received: {query}")
        
        # Perform DuckDuckGo search
        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=10)
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', '')
                })
        
        logger.info(f"Found {len(results)} results")
        return jsonify({'results': results})
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape', methods=['POST'])
def scrape():
    """API endpoint for scraping web pages"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        logger.info(f"Scraping URL: {url}")
        
        # Fetch and parse the webpage
        headers = {
            'User-Agent': USER_AGENT
        }
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic information
        title = soup.title.string if soup.title else 'No title'
        
        # Extract text content
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return jsonify({
            'title': title,
            'url': url,
            'content': text[:MAX_CONTENT_LENGTH]  # Limit content size
        })
    
    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Legion Web Server'})

if __name__ == '__main__':
    logger.info("Starting Legion Web Server...")
    # Run on all interfaces to be accessible via Cloudflare Tunnel
    app.run(host='0.0.0.0', port=5000, debug=False)
