# Secure Ollama Installation on Ubuntu Pop!_OS

This guide covers secure installation and configuration of Ollama on Linux.

## Method 1: Snap Package (Most Secure - Recommended) ⭐

**This is the most secure method** because:
- Canonical verifies all Snap packages
- Sandboxed execution (AppArmor)
- Automatic security updates
- No manual verification needed

```bash
# Install Snap (if not already installed)
sudo apt update
sudo apt install snapd

# Install Ollama via Snap
sudo snap install ollama

# Verify installation
snap info ollama
ollama --version

# Start the service
sudo snap start ollama

# Download a model
ollama pull llama2
```

**Note**: Snap is the most secure option. See `OLLAMA_SECURITY_VERIFICATION.md` for security comparison.

## Method 2: Official Install Script

### Step 1: Download and Verify the Install Script

```bash
# Download the official install script
curl -fsSL https://ollama.ai/install.sh -o /tmp/ollama-install.sh

# Verify the script (optional but recommended)
cat /tmp/ollama-install.sh | head -20  # Review what it does
```

### Step 2: Review the Script (Security Best Practice)

Before running any install script, it's good practice to review it:

```bash
# View the script
less /tmp/ollama-install.sh

# Or check what it will do
grep -E "(curl|wget|apt|dpkg|systemctl)" /tmp/ollama-install.sh
```

The official script typically:
- Downloads the Ollama binary
- Installs it to `/usr/local/bin/ollama`
- Creates a systemd service
- Sets up proper permissions

### Step 3: Run the Installation

```bash
# Make it executable
chmod +x /tmp/ollama-install.sh

# Run with sudo (required for system installation)
sudo /tmp/ollama-install.sh
```

### Step 4: Verify Installation

```bash
# Check if Ollama is installed
which ollama
ollama --version

# Check if the service is running
systemctl status ollama
```

## Method 3: Manual Installation (More Control)

If you prefer more control over the installation:

### Step 1: Download the Binary

```bash
# Create a directory for Ollama
sudo mkdir -p /usr/local/bin

# Download the latest Linux binary
curl -L https://ollama.ai/download/ollama-linux-amd64 -o /tmp/ollama

# Verify it's executable
chmod +x /tmp/ollama

# Move to system location
sudo mv /tmp/ollama /usr/local/bin/ollama
```

### Step 2: Create Systemd Service (Secure Service)

Create a service file for secure, managed execution:

```bash
sudo nano /etc/systemd/system/ollama.service
```

Add this content:

```ini
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_ORIGINS=*"

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/usr/share/ollama /home/ollama/.ollama

[Install]
WantedBy=default.target
```

### Step 3: Create Dedicated User (Security Best Practice)

```bash
# Create a dedicated user for Ollama (more secure)
sudo useradd -r -s /bin/false -d /home/ollama -m ollama

# Create directory for Ollama data
sudo mkdir -p /usr/share/ollama
sudo chown ollama:ollama /usr/share/ollama
sudo chown ollama:ollama /home/ollama/.ollama
```

### Step 4: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (starts on boot)
sudo systemctl enable ollama

# Start service
sudo systemctl start ollama

# Check status
sudo systemctl status ollama
```


## Security Configuration

### 1. Restrict Network Access (Recommended)

By default, Ollama listens on `0.0.0.0:11434` (all interfaces). For security, bind to localhost only:

Edit the service file:
```bash
sudo systemctl edit ollama
```

Add:
```ini
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
```

Or create override:
```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo nano /etc/systemd/system/ollama.service.d/override.conf
```

Add:
```ini
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
```

Restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

### 2. Configure Firewall (UFW)

```bash
# If you need external access (not recommended for local dev)
sudo ufw allow 11434/tcp

# For localhost only (recommended), no firewall rule needed
# Ollama will only be accessible from your machine
```

### 3. Set Up CORS Origins (If Needed)

If you need to access from Docker containers:

```bash
sudo systemctl edit ollama
```

Add:
```ini
[Service]
Environment="OLLAMA_ORIGINS=http://localhost:*,http://127.0.0.1:*"
```

### 4. Verify Security Settings

```bash
# Check what ports Ollama is listening on
sudo netstat -tlnp | grep ollama
# or
sudo ss -tlnp | grep ollama

# Should show: 127.0.0.1:11434 (localhost only)
```

## Post-Installation Setup

### 1. Download Your First Model

```bash
# Test with a small model first
ollama pull llama2

# Or a faster model
ollama pull phi

# Or Mistral (good balance)
ollama pull mistral
```

### 2. Test the Installation

```bash
# Test Ollama is working
ollama list

# Test a simple query
ollama run llama2 "Hello, how are you?"
```

### 3. Verify Docker Can Access (For Your Use Case)

Since you're using Option B (Docker app + host Ollama):

```bash
# Test from host
curl http://localhost:11434/api/tags

# Test from Docker (after starting your container)
docker exec -it <your-container> curl http://host.docker.internal:11434/api/tags
```

## Troubleshooting

### Ollama Service Won't Start

```bash
# Check logs
sudo journalctl -u ollama -n 50

# Check permissions
ls -la /usr/local/bin/ollama
ls -la /home/ollama/.ollama

# Restart service
sudo systemctl restart ollama
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R ollama:ollama /home/ollama/.ollama
sudo chown -R ollama:ollama /usr/share/ollama
```

### Port Already in Use

```bash
# Check what's using port 11434
sudo lsof -i :11434

# Kill the process if needed
sudo kill <PID>
```

### Can't Access from Docker

Make sure Ollama is bound to `0.0.0.0` or `127.0.0.1` (not just localhost):

```bash
# Check binding
sudo ss -tlnp | grep 11434

# If you see 127.0.0.1:11434, Docker can access via host.docker.internal
# If you see 0.0.0.0:11434, it's accessible from anywhere (less secure)
```

## Security Checklist

- ✅ Ollama installed in system location (`/usr/local/bin`)
- ✅ Running as dedicated user (not root)
- ✅ Service configured with systemd
- ✅ Bound to localhost only (`127.0.0.1:11434`)
- ✅ Firewall configured (if needed)
- ✅ Regular updates (check with `ollama --version`)
- ✅ Models stored in user directory (`~/.ollama`)

## Updating Ollama

```bash
# Check current version
ollama --version

# Update (re-run install script)
curl -fsSL https://ollama.ai/install.sh | sh

# Or if using Snap
sudo snap refresh ollama
```

## Uninstallation

If you need to remove Ollama:

```bash
# Stop and disable service
sudo systemctl stop ollama
sudo systemctl disable ollama

# Remove service file
sudo rm /etc/systemd/system/ollama.service

# Remove binary
sudo rm /usr/local/bin/ollama

# Remove user (optional)
sudo userdel ollama

# Remove data (optional - this deletes all models!)
rm -rf ~/.ollama
```

## Recommended Configuration for Your Use Case

For your Docker setup (Option B), use this configuration:

```bash
# 1. Install Ollama (Method 1 or 2)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Configure to listen on localhost
sudo systemctl edit ollama
# Add: Environment="OLLAMA_HOST=127.0.0.1:11434"

# 3. Restart
sudo systemctl daemon-reload
sudo systemctl restart ollama

# 4. Download a model
ollama pull llama2

# 5. Verify
curl http://localhost:11434/api/tags
```

Your Docker container will access it via `http://host.docker.internal:11434`.

## Additional Security Tips

1. **Keep Ollama Updated**: Regularly check for updates
2. **Monitor Logs**: `sudo journalctl -u ollama -f`
3. **Use Firewall**: If exposing to network, use UFW
4. **Limit Origins**: Set `OLLAMA_ORIGINS` if needed
5. **Regular Backups**: Backup `~/.ollama` if you have custom models

## Resources

- Official Docs: https://ollama.ai/docs
- GitHub: https://github.com/ollama/ollama
- Models: https://ollama.ai/library

