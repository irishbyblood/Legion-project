#!/usr/bin/env python3
"""
Legion AI (Legion Prime) - Web Server
High-Tech Cyberpunk AI Assistant with Dark Web Access
"""

from flask import Flask, render_template, jsonify, request
import requests
import subprocess
import platform
import psutil
import socket
import os
import re
from urllib.parse import quote
from datetime import datetime

app = Flask(__name__)

# Configuration
AHMIA_SEARCH_URL = "https://ahmia.fi/search/?q="
ONION_PROXY = "onion.ly"  # Proxy for accessing .onion sites on clearnet

class LegionAgent:
    """Base class for Legion AI agents"""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.status = "idle"
    
    def execute(self, query):
        raise NotImplementedError

class WebSearchAgent(LegionAgent):
    """Agent for standard web searches"""
    def __init__(self):
        super().__init__("Web Search", "Searches the clearnet for information")
    
    def execute(self, query):
        try:
            self.status = "searching"
            # Use DuckDuckGo API for privacy-focused search
            # URL encode query to prevent injection
            encoded_query = quote(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            results = []
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", "Result"),
                    "snippet": data.get("AbstractText"),
                    "url": data.get("AbstractURL", "")
                })
            
            for topic in data.get("RelatedTopics", [])[:5]:
                if "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "")[:50],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", "")
                    })
            
            self.status = "complete"
            return {
                "agent": self.name,
                "query": query,
                "results": results,
                "count": len(results),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.status = "error"
            return {
                "agent": self.name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class DarkWebAgent(LegionAgent):
    """Agent for dark web searches via Ahmia"""
    def __init__(self):
        super().__init__("Dark Web", "Searches .onion sites via Ahmia gateway")
    
    def execute(self, query):
        try:
            self.status = "searching darknet"
            # Search Ahmia for .onion sites
            # URL encode query to prevent injection
            encoded_query = quote(query)
            search_url = f"{AHMIA_SEARCH_URL}{encoded_query}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Android 10; Mobile; rv:85.0) Gecko/85.0 Firefox/85.0"
            }
            response = requests.get(search_url, headers=headers, timeout=15)
            
            # Parse results (simplified - in production would use BeautifulSoup)
            results = []
            onion_pattern = r'([a-z2-7]{16,56}\.onion)'
            onion_sites = re.findall(onion_pattern, response.text)
            
            for site in list(set(onion_sites))[:5]:
                # Provide clearnet proxy URL
                proxy_url = f"https://{site}.{ONION_PROXY}"
                results.append({
                    "title": site,
                    "snippet": f"Onion site accessible via proxy",
                    "url": proxy_url,
                    "onion": f"http://{site}"
                })
            
            self.status = "complete"
            return {
                "agent": self.name,
                "query": query,
                "results": results,
                "count": len(results),
                "warning": "Access via Tor for true anonymity",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.status = "error"
            return {
                "agent": self.name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class SecurityAgent(LegionAgent):
    """Agent for security scanning and threat hunting"""
    def __init__(self):
        super().__init__("Security", "Huntress-style threat hunting")
        # Note: These keywords will generate false positives from legitimate system processes
        # In production, use more sophisticated heuristics and whitelisting
        self.suspicious_keywords = [
            "keylog", "trace", "attack", "exploit", "malware",
            "trojan", "backdoor", "rootkit", "inject", "spy"
        ]
    
    def execute(self, scan_type="processes"):
        try:
            self.status = "scanning"
            threats = []
            
            if scan_type == "processes":
                # Scan running processes for suspicious activity
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        proc_info = proc.info
                        proc_name = proc_info['name'].lower()
                        cmdline = ' '.join(proc_info['cmdline'] or []).lower()
                        
                        # Check for suspicious keywords
                        for keyword in self.suspicious_keywords:
                            if keyword in proc_name or keyword in cmdline:
                                threats.append({
                                    "pid": proc_info['pid'],
                                    "name": proc_info['name'],
                                    "threat": keyword,
                                    "severity": "high",
                                    "cmdline": ' '.join(proc_info['cmdline'] or [])[:100]
                                })
                                break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            self.status = "complete"
            return {
                "agent": self.name,
                "scan_type": scan_type,
                "threats_found": len(threats),
                "threats": threats,
                "scanned_at": datetime.now().isoformat(),
                "status": "clean" if len(threats) == 0 else "threats_detected"
            }
        except Exception as e:
            self.status = "error"
            return {
                "agent": self.name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Initialize agents
web_agent = WebSearchAgent()
darkweb_agent = DarkWebAgent()
security_agent = SecurityAgent()

@app.route('/')
def index():
    """Main interface"""
    return render_template('index.html')

@app.route('/api/search/web', methods=['POST'])
def search_web():
    """Web search endpoint"""
    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    result = web_agent.execute(query)
    return jsonify(result)

@app.route('/api/search/darkweb', methods=['POST'])
def search_darkweb():
    """Dark web search endpoint"""
    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    result = darkweb_agent.execute(query)
    return jsonify(result)

@app.route('/api/security/scan', methods=['GET'])
def security_scan():
    """Security scan endpoint"""
    scan_type = request.args.get('type', 'processes')
    result = security_agent.execute(scan_type)
    return jsonify(result)

@app.route('/api/system/info', methods=['GET'])
def system_info():
    """System information endpoint"""
    try:
        # Get storage info
        disk = psutil.disk_usage('/')
        
        # Get network info
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        # Get public IP (with timeout)
        try:
            public_ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
            public_ip = public_ip_response.json().get('ip', 'Unknown')
        except (requests.RequestException, ValueError):
            public_ip = 'Unknown'
        
        # Memory info
        memory = psutil.virtual_memory()
        
        return jsonify({
            "platform": platform.system(),
            "platform_version": platform.version(),
            "hostname": hostname,
            "network": {
                "local_ip": local_ip,
                "public_ip": public_ip
            },
            "storage": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent_used": disk.percent
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent_used": memory.percent
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents/status', methods=['GET'])
def agents_status():
    """Get status of all agents"""
    return jsonify({
        "agents": [
            {
                "name": web_agent.name,
                "description": web_agent.description,
                "status": web_agent.status
            },
            {
                "name": darkweb_agent.name,
                "description": darkweb_agent.description,
                "status": darkweb_agent.status
            },
            {
                "name": security_agent.name,
                "description": security_agent.description,
                "status": security_agent.status
            }
        ],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Legion AI (Legion Prime)",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Run on all interfaces for Termux/Android access
    # WARNING: For production, use a proper WSGI server (gunicorn/waitress) with authentication
    # and rate limiting. This development server should only be used in trusted networks.
    app.run(host='0.0.0.0', port=5000, debug=False)
