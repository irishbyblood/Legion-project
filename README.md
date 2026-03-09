# Legion Project

## Setup
Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Run
Start the Flask interface:
```bash
python interface/web_server.py
```

For Termux usage, the original instructions include:
```bash
pkg install termux-api
termux-chroot cloudflared tunnel run legion
```
