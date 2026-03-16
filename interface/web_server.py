#!/usr/bin/env python3
"""
Legion AI Web Server
High-Tech Cyberpunk Interface
"""

from flask import Flask, render_template, request, jsonify
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import logging
import os
from urllib.parse import urlparse
import ipaddress

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
# Use environment variable for secret key, or generate one for development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

class LegionAI:
    """Legion Prime AI Core"""
    
    def __init__(self):
        self.name = "Legion Prime"
        self.domain = "https://horizen-network.com"
        self.theme_color = "#00ff41"  # Neon green
        
    def search_web(self, query, max_results=5):
        """Search the web using DuckDuckGo"""
        try:
            logger.info(f"Searching for: {query}")
            results = []
            
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', '')
                    })
            
            return results
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _is_safe_url(self, url):
        """Validate URL to prevent SSRF attacks"""
        try:
            parsed = urlparse(url)
            
            # Only allow http and https schemes
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Get hostname
            hostname = parsed.hostname
            if not hostname:
                return False
            
            # Resolve hostname to IP
            try:
                import socket
                ip = socket.gethostbyname(hostname)
                ip_obj = ipaddress.ip_address(ip)
                
                # Block private IP ranges
                if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
                    logger.warning(f"Blocked private IP access: {url} -> {ip}")
                    return False
                    
            except (socket.gaierror, ValueError) as e:
                logger.warning(f"Could not resolve hostname: {hostname}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"URL validation error: {e}")
            return False
    
    def fetch_page_content(self, url):
        """Fetch and parse webpage content"""
        # Validate URL first
        if not url or not isinstance(url, str):
            logger.error("Invalid URL: empty or not a string")
            return None
            
        # Check if URL is safe
        if not self._is_safe_url(url):
            logger.error(f"Unsafe URL blocked: {url}")
            return None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:1000]  # Return first 1000 characters
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return None
    
    def process_query(self, query):
        """Process user query and return response"""
        if not query:
            return {
                'status': 'error',
                'message': 'No query provided'
            }
        
        # Search the web
        search_results = self.search_web(query)
        
        return {
            'status': 'success',
            'query': query,
            'results': search_results,
            'domain': self.domain,
            'ai_name': self.name
        }

# Initialize Legion AI
legion = LegionAI()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         ai_name=legion.name,
                         domain=legion.domain,
                         theme_color=legion.theme_color)

@app.route('/query', methods=['POST'])
def query():
    """Handle AI queries"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'status': 'error', 'message': 'No query provided'}), 400
        
        response = legion.process_query(user_query)
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Query error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/status')
def status():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'ai_name': legion.name,
        'domain': legion.domain,
        'version': '1.0.0'
    })

@app.route('/fetch', methods=['POST'])
def fetch():
    """Fetch webpage content"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'No URL provided'}), 400
        
        content = legion.fetch_page_content(url)
        
        if content:
            return jsonify({
                'status': 'success',
                'url': url,
                'content': content
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to fetch content'
            }), 500
    
    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Run the server
    # Use 0.0.0.0 to allow external connections (important for Termux)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
