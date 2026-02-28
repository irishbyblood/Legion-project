import os
import subprocess
import requests
import shutil
import socket
import re
import sys
from urllib.parse import urlparse, urlunparse
from flask import Flask, render_template_string, request, jsonify
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

app = Flask(__name__)

# Security: Add security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com https://fonts.gstatic.com; img-src 'self' data: https:;"
    return response

# Security: Input validation function
def validate_search_query(query):
    """Validate and sanitize search query"""
    if not query or not isinstance(query, str):
        return None
    # Remove potentially dangerous characters while allowing normal search queries
    query = query.strip()
    if len(query) > 500:  # Limit query length
        return None
    # Basic validation - allow alphanumeric, spaces, and basic safe punctuation only
    # Removed quotes, semicolons, and other potentially dangerous characters
    if not re.match(r'^[\w\s\-.,!?()]+$', query):
        return None
    return query

# --- MODULE 1: DARK WEB GATEWAY ---
def real_dark_web_search(query):
    """Access Tor Network via Clearnet Gateway"""
    try:
        # Security: Validate query
        query = validate_search_query(query)
        if not query:
            return [{"title": "INVALID QUERY", "snippet": "Query contains invalid characters", "link": "#"}]
        
        url = f"https://ahmia.fi/search/?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for item in soup.select('li.result'):
            try:
                title = item.select_one('a').text.strip()
                link = item.select_one('a')['href']
                # Security: Properly parse and replace .onion domains
                if link:
                    try:
                        parsed = urlparse(link)
                        if parsed.netloc.endswith('.onion'):
                            # Replace .onion TLD with .onion.ly
                            new_netloc = parsed.netloc[:-6] + '.onion.ly'  # Remove '.onion' and add '.onion.ly'
                            link = urlunparse((parsed.scheme, new_netloc, parsed.path, 
                                             parsed.params, parsed.query, parsed.fragment))
                    except Exception:
                        pass  # Keep original link if parsing fails
                snippet = item.select_one('p').text.strip()
                results.append({"title": title, "link": link, "snippet": snippet})
            except (AttributeError, KeyError, TypeError):
                continue
        return results[:10]
    except Exception as e:
        return [{"title": "GATEWAY ERROR", "snippet": str(e), "link": "#"}]

# --- MODULE 2: HUNTRESS THREAT SCANNER ---
def real_security_scan():
    """Scans PIDs for Persistence/Spyware - Cross-platform support"""
    try:
        # Cross-platform process listing
        if sys.platform.startswith('win'):
            # Windows: use tasklist
            output = subprocess.check_output(["tasklist", "/v"], universal_newlines=True)
        else:
            # Unix-like: use ps
            output = subprocess.check_output(["ps", "-ef"], universal_newlines=True)
        
        lines = output.split('\n')
        threats = []
        safe_count = 0
        for line in lines:
            if "termux" in line or "python" in line: continue
            if any(x in line for x in ["keylog", "monitor", "trace", "exploit", "metasploit"]):
                threats.append(f"⚠️ SUSPICIOUS PID: {line[:60]}...")
            safe_count += 1
        status = f"SCANNED {safe_count} PROCESSES."
        return {"status": status, "threats": threats}
    except subprocess.CalledProcessError as e:
        return {"status": f"SCAN FAILED: {str(e)}", "threats": []}
    except FileNotFoundError:
        return {"status": "SCAN FAILED: Process listing command not available", "threats": []}
    except Exception as e:
        return {"status": f"SCAN FAILED: {str(e)}", "threats": []}

# --- MODULE 3: CLEARNET & SYSTEM ---
def real_web_search(query):
    """Search clearnet with validation"""
    try:
        # Security: Validate query
        query = validate_search_query(query)
        if not query:
            return [{"title": "INVALID QUERY", "body": "Query contains invalid characters", "href": "#"}]
        return DDGS().text(query, max_results=5)
    except Exception as e:
        return [{"title": "SEARCH ERROR", "body": str(e), "href": "#"}]

def system_stats():
    total, used, free = shutil.disk_usage("/")
    return f"STORAGE: {free // (2**30)} GB FREE | IP: {socket.gethostbyname(socket.gethostname())}"

# --- MODULE 4: THE ALIVE INTERFACE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    body { background: #000; color: #00ff41; font-family: 'Share Tech Mono', monospace; margin: 0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
    
    /* ANIMATIONS */
    @keyframes breathe { 0% { opacity: 0.9; } 50% { opacity: 1; box-shadow: inset 0 0 50px #002200; } 100% { opacity: 0.9; } }
    @keyframes scan { 0% { background-position: 0 0; } 100% { background-position: 0 100%; } }
    
    body::after {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        background-size: 100% 2px, 3px 100%; pointer-events: none; z-index: 10;
    }
    
    #container { flex: 1; display: flex; flex-direction: column; z-index: 20; animation: breathe 4s infinite; }
    
    /* NAV */
    .nav { display: flex; border-bottom: 2px solid #333; background: #050505; }
    .nav div { flex: 1; padding: 15px; text-align: center; border-right: 1px solid #333; cursor: pointer; font-weight: bold; }
    .nav div.active { background: #00ff41; color: #000; }
    #t-dark.active { background: #ff0000; color: #fff; }

    /* CONTENT */
    .section { display: none; flex: 1; padding: 20px; overflow-y: auto; }
    .section.active { display: block; }
    
    .result { border-left: 2px solid #333; padding-left: 10px; margin-bottom: 15px; }
    .result a { color: #fff; text-decoration: none; font-size: 1.1em; font-weight: bold; }
    .result p { color: #aaa; font-size: 0.9em; margin: 5px 0 0 0; }
    
    .dark-mode .result { border-left-color: #ff0000; }
    .dark-mode a { color: #ffaaaa; }
    
    /* CONTROLS */
    .bar { padding: 15px; background: #111; border-top: 1px solid #333; }
    input { width: 100%; padding: 15px; background: #000; border: 1px solid #333; color: #00ff41; font-family: inherit; box-sizing: border-box; }
    button { width: 100%; padding: 15px; margin-top: 10px; background: #00ff41; border: none; font-weight: bold; font-family: inherit; font-size: 1.1em; cursor: pointer; }
    .red-btn { background: #ff0000; color: #fff; }
</style>
</head>
<body>
<div id="container">
    <div class="nav">
        <div onclick="tab('surface')" id="t-surface" class="active">SURFACE</div>
        <div onclick="tab('dark')" id="t-dark" style="color:#ff0000">DARK WEB</div>
        <div onclick="tab('secure')" id="t-secure">HUNTRESS</div>
    </div>

    <div id="surface" class="section active">
        <div id="r-surface"></div>
    </div>

    <div id="dark" class="section dark-mode">
        <div style="color:red; text-align:center; margin-bottom:10px;">⚠️ ENCRYPTED GATEWAY ACTIVE</div>
        <div id="r-dark"></div>
    </div>

    <div id="secure" class="section">
        <div id="r-secure">SYSTEM READY.</div>
    </div>

    <div class="bar">
        <input id="query" placeholder="ENTER COMMAND OR SEARCH...">
        <button id="actionBtn" onclick="runAction()">EXECUTE</button>
        <button onclick="toggleMic()" style="background:#333; color:#fff; margin-top:5px;">🎙️ VOICE COMMAND</button>
    </div>
</div>

<script>
    let currentTab = 'surface';
    
    function tab(t) {
        currentTab = t;
        document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
        document.querySelectorAll('.nav div').forEach(e => e.classList.remove('active'));
        document.getElementById(t).classList.add('active');
        document.getElementById('t-'+t).classList.add('active');
        
        const btn = document.getElementById('actionBtn');
        if(t === 'dark') { btn.className = 'red-btn'; btn.innerText = "SEARCH DARK WEB"; }
        else if(t === 'secure') { btn.className = ''; btn.innerText = "SCAN SYSTEM"; }
        else { btn.className = ''; btn.innerText = "SEARCH WEB"; }
    }

    async function runAction() {
        const q = document.getElementById('query').value;
        const resDiv = document.getElementById('r-'+currentTab);
        resDiv.innerHTML = "PROCESSING...";
        
        if (currentTab === 'secure') {
            const res = await fetch('/scan');
            const data = await res.json();
            resDiv.innerHTML = data.status + "<br><br>" + data.threats.join("<br>");
            return;
        }
        
        const res = await fetch('/search', {
            method: 'POST', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({type: currentTab, query: q})
        });
        const data = await res.json();
        
        resDiv.innerHTML = "";
        data.results.forEach(r => {
            resDiv.innerHTML += `<div class='result'><a href='${r.link || r.href}'>${r.title || 'Result'}</a><p>${r.snippet || r.body}</p></div>`;
        });
    }

    // REAL VOICE API - with feature detection
    let recognition = null;
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = (e) => {
            document.getElementById('query').value = e.results[0][0].transcript;
            runAction();
        };
    }
    
    function toggleMic() {
        if (recognition) {
            recognition.start();
        } else {
            alert('Speech recognition is not supported in your browser.');
        }
    }
</script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    if not data or 'query' not in data or 'type' not in data:
        return jsonify(results=[{"title": "ERROR", "body": "Invalid request", "href": "#"}])
    
    if data['type'] == 'dark': 
        return jsonify(results=real_dark_web_search(data['query']))
    return jsonify(results=real_web_search(data['query']))

@app.route('/scan')
def scan(): return jsonify(real_security_scan())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
