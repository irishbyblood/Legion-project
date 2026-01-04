# Legion-project

A Flask-based web application featuring dark web search gateway, system security scanning, and clearnet search capabilities.

## Features

- **Surface Web Search**: DuckDuckGo-powered clearnet search
- **Dark Web Gateway**: Access Tor network via Ahmia clearnet gateway
- **Huntress Scanner**: System process security scanner
- **Voice Commands**: Speech recognition for hands-free operation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/irishbyblood/Legion-project.git
cd Legion-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Security Notes

- This application is for educational and research purposes only
- The dark web search uses a clearnet gateway (Ahmia) and does not provide true anonymity
- System scanning requires appropriate permissions
- Use responsibly and in accordance with applicable laws

## Requirements

- Python 3.7+
- Flask
- requests
- beautifulsoup4
- duckduckgo-search

## License

See LICENSE file for details.