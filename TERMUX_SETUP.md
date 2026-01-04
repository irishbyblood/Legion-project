# Termux Setup Guide for Legion AI

This guide is specifically for running Legion AI on Android using Termux.

## Prerequisites

1. Install Termux from F-Droid (recommended) or Google Play
2. Update Termux packages:
   ```bash
   pkg update && pkg upgrade
   ```

## Installation Steps

### 1. Install Required Packages

```bash
# Install Python and required system packages
pkg install python git termux-api

# Upgrade pip
pip install --upgrade pip
```

### 2. Clone the Repository

```bash
cd ~
git clone https://github.com/irishbyblood/Legion-project.git
cd Legion-project
```

### 3. Install Python Dependencies

```bash
pip install flask requests duckduckgo-search beautifulsoup4
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

### 4. Run the Server

Start the server in the background:
```bash
python interface/web_server.py &
```

Check if it's running:
```bash
curl http://localhost:5000/status
```

### 5. Access the Interface

Open Termux browser or any browser on your Android device:
```bash
termux-open-url http://localhost:5000
```

Or access from another device on the same network:
```
http://<your-android-ip>:5000
```

To find your IP address:
```bash
ifconfig wlan0 | grep inet
```

## Cloudflare Tunnel Setup (Optional)

To make your Legion AI accessible from the internet:

### 1. Install Cloudflared

```bash
# Download cloudflared for ARM64
pkg install wget
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
chmod +x cloudflared-linux-arm64
mv cloudflared-linux-arm64 $PREFIX/bin/cloudflared
```

### 2. Authenticate with Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser for authentication.

### 3. Create a Tunnel

```bash
cloudflared tunnel create legion
```

### 4. Configure the Tunnel

Create a config file at `~/.cloudflared/config.yml`:

```yaml
tunnel: legion
credentials-file: /data/data/com.termux/files/home/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: horizen-network.com
    service: http://localhost:5000
  - service: http_status:404
```

Replace `<tunnel-id>` with your actual tunnel ID.

### 5. Run the Tunnel

```bash
cloudflared tunnel run legion &
```

Now your Legion AI will be accessible at `https://horizen-network.com`

## Running on Startup

To automatically start Legion AI when Termux starts:

1. Create a startup script:

```bash
mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-legion.sh
```

2. Add the following content:

```bash
#!/data/data/com.termux/files/usr/bin/bash

cd ~/Legion-project
python interface/web_server.py > ~/legion.log 2>&1 &

# Optional: Start Cloudflare tunnel
# cloudflared tunnel run legion > ~/cloudflare.log 2>&1 &
```

3. Make it executable:

```bash
chmod +x ~/.termux/boot/start-legion.sh
```

## Troubleshooting

### Server Won't Start

Check if port 5000 is already in use:
```bash
netstat -tulpn | grep 5000
```

Use a different port:
```bash
PORT=8080 python interface/web_server.py
```

### Dependencies Won't Install

Update pip and try again:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Can't Access from Other Devices

1. Make sure you're on the same WiFi network
2. Check Android's firewall settings
3. Verify the server is running on 0.0.0.0:
   ```bash
   netstat -tulpn | grep python
   ```

### Permission Denied

Some operations might require storage permission:
```bash
termux-setup-storage
```

## Performance Tips

1. **Keep Termux awake**: Acquire a wakelock to prevent Termux from being killed:
   ```bash
   termux-wake-lock
   ```

2. **Increase memory**: If you experience crashes, try:
   ```bash
   ulimit -s unlimited
   ```

3. **Monitor resources**:
   ```bash
   top
   ```

## Stopping the Server

Find the process:
```bash
ps aux | grep web_server.py
```

Kill it:
```bash
kill <PID>
```

Or use pkill:
```bash
pkill -f web_server.py
```

## Updating

Pull the latest changes:
```bash
cd ~/Legion-project
git pull origin main
pip install -r requirements.txt --upgrade
```

## Additional Resources

- Termux Wiki: https://wiki.termux.com
- Cloudflare Tunnel Docs: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- Flask Documentation: https://flask.palletsprojects.com/

## Support

For issues specific to Termux setup, check the Termux community forums or the project's GitHub issues page.
