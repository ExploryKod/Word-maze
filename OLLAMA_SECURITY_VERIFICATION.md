# Ollama Security Verification Guide

## Snap vs Install Script: Security Comparison

### Snap Package (More Secure for Isolation)

**Advantages:**
- ✅ **Sandboxed**: Runs in isolated environment (AppArmor confinement)
- ✅ **Auto-updates**: Secure, verified updates from Snap store
- ✅ **Verified source**: Canonical verifies packages in Snap store
- ✅ **No root execution**: Install script doesn't need sudo
- ✅ **Reproducible**: Same package for everyone
- ✅ **Audit trail**: Snap store maintains package history

**Disadvantages:**
- ⚠️ **Less control**: Can't easily customize installation
- ⚠️ **Snap overhead**: Slightly more resource usage
- ⚠️ **Snap daemon**: Requires snapd service

### Install Script (More Flexible)

**Advantages:**
- ✅ **Direct control**: You see exactly what it does
- ✅ **Customizable**: Can modify installation
- ✅ **No Snap dependency**: Doesn't require snapd
- ✅ **Faster**: No sandboxing overhead

**Disadvantages:**
- ⚠️ **Requires verification**: Must verify script before running
- ⚠️ **Manual updates**: You must update manually
- ⚠️ **Root access**: Requires sudo (security risk if compromised)

## Recommendation: **Use Snap for Better Security**

For most users, **Snap is more secure** because:
1. Canonical verifies packages
2. Sandboxed execution
3. Automatic security updates
4. No need to verify scripts manually

## How to Verify the Install Script (If You Use It)

### Method 1: Check Official Source

```bash
# 1. Verify you're on the official site
# Check SSL certificate
openssl s_client -connect ollama.ai:443 -showcerts | grep -A 2 "CN="

# 2. Check DNS (ensure you're not being redirected)
nslookup ollama.ai

# 3. Download from official GitHub (more trustworthy)
curl -fsSL https://raw.githubusercontent.com/ollama/ollama/main/scripts/install.sh -o /tmp/ollama-install.sh
```

### Method 2: Review the Script Before Running

```bash
# Download without executing
curl -fsSL https://ollama.ai/install.sh -o /tmp/ollama-install.sh

# Review the entire script
cat /tmp/ollama-install.sh

# Or use a pager
less /tmp/ollama-install.sh

# Check what it does
grep -E "(curl|wget|apt|dpkg|systemctl|sudo|chmod|chown)" /tmp/ollama-install.sh

# Look for suspicious patterns
grep -i "rm -rf\|format\|delete\|password\|key" /tmp/ollama-install.sh
```

### Method 3: Verify Checksums (If Available)

```bash
# Download script
curl -fsSL https://ollama.ai/install.sh -o /tmp/ollama-install.sh

# Calculate SHA256
sha256sum /tmp/ollama-install.sh

# Compare with official checksum (if published)
# Check: https://github.com/ollama/ollama/releases
```

### Method 4: Check GitHub Source

The most secure way is to get the script from GitHub:

```bash
# Get from official GitHub repository
curl -fsSL https://raw.githubusercontent.com/ollama/ollama/main/scripts/install.sh -o /tmp/ollama-install.sh

# Verify it's from the official repo
# Check: https://github.com/ollama/ollama
```

### Method 5: Use GPG Signature (If Available)

```bash
# Download script and signature
curl -fsSL https://ollama.ai/install.sh -o /tmp/ollama-install.sh
curl -fsSL https://ollama.ai/install.sh.asc -o /tmp/ollama-install.sh.asc

# Import Ollama's GPG key (if they publish one)
# gpg --keyserver keyserver.ubuntu.com --recv-keys <OLLAMA_GPG_KEY>

# Verify signature
# gpg --verify /tmp/ollama-install.sh.asc /tmp/ollama-install.sh
```

## What the Install Script Typically Does (Safe Operations)

A legitimate Ollama install script should:

1. **Download the binary** from official source
2. **Install to `/usr/local/bin/ollama`**
3. **Create systemd service** at `/etc/systemd/system/ollama.service`
4. **Set proper permissions** (chmod +x)
5. **Start the service**

**Red flags to watch for:**
- ❌ Downloads from unknown URLs
- ❌ Executes arbitrary code without verification
- ❌ Modifies files outside expected locations
- ❌ Requests passwords or API keys
- ❌ Connects to unknown servers
- ❌ Deletes files unnecessarily

## Secure Installation Methods (Ranked by Security)

### 1. Snap Package (Most Secure) ⭐ RECOMMENDED

```bash
# Install via Snap (most secure)
sudo snap install ollama

# Verify installation
snap info ollama
snap list | grep ollama

# Check security confinement
snap connections ollama
```

**Why it's most secure:**
- Canonical verifies all Snap packages
- Sandboxed with AppArmor
- Automatic security updates
- No manual verification needed

### 2. Manual Binary Download (Good Security)

```bash
# 1. Download from official GitHub releases
cd /tmp
wget https://github.com/ollama/ollama/releases/download/v<VERSION>/ollama-linux-amd64

# 2. Verify checksum from GitHub release page
sha256sum ollama-linux-amd64
# Compare with checksum on GitHub release page

# 3. Install manually
sudo mv ollama-linux-amd64 /usr/local/bin/ollama
sudo chmod +x /usr/local/bin/ollama

# 4. Create service manually (see OLLAMA_INSTALL_LINUX.md)
```

### 3. Verified Install Script (Moderate Security)

```bash
# 1. Download from GitHub (more trustworthy than direct domain)
curl -fsSL https://raw.githubusercontent.com/ollama/ollama/main/scripts/install.sh -o /tmp/install.sh

# 2. Review the script
cat /tmp/install.sh | less

# 3. Verify it matches what you expect
# Check: Does it download from official source?
# Check: Does it install to expected locations?
grep -E "ollama.ai|github.com/ollama" /tmp/install.sh

# 4. Only then execute
chmod +x /tmp/install.sh
sudo /tmp/install.sh
```

## Recommended Secure Installation Process

### Option A: Snap (Easiest & Most Secure)

```bash
# 1. Install Snap (if not already installed)
sudo apt update
sudo apt install snapd

# 2. Install Ollama via Snap
sudo snap install ollama

# 3. Verify
snap info ollama
ollama --version

# 4. Start service
sudo snap start ollama

# 5. Download model
ollama pull llama2
```

### Option B: Verified Manual Installation

```bash
# 1. Go to official GitHub releases
# https://github.com/ollama/ollama/releases
# Note the latest version number

# 2. Download binary
VERSION="v0.1.0"  # Replace with latest version
cd /tmp
wget https://github.com/ollama/ollama/releases/download/${VERSION}/ollama-linux-amd64

# 3. Download checksum from GitHub
wget https://github.com/ollama/ollama/releases/download/${VERSION}/checksums.txt

# 4. Verify checksum
sha256sum -c checksums.txt

# 5. Install
sudo mv ollama-linux-amd64 /usr/local/bin/ollama
sudo chmod +x /usr/local/bin/ollama

# 6. Create service (see OLLAMA_INSTALL_LINUX.md)
```

## Additional Security Measures

### 1. Verify SSL Certificate

```bash
# Check the website's SSL certificate
echo | openssl s_client -connect ollama.ai:443 2>/dev/null | openssl x509 -noout -subject -issuer

# Should show valid certificate from trusted CA
```

### 2. Check DNS Resolution

```bash
# Ensure you're resolving to correct IP
nslookup ollama.ai
dig ollama.ai

# Compare with known IPs (check GitHub or official docs)
```

### 3. Use HTTPS Only

```bash
# Always use https:// (never http://)
# The install script should use https://
grep -i "http://" /tmp/ollama-install.sh  # Should be minimal or none
```

### 4. Verify GitHub Repository

```bash
# Check the official repo
# https://github.com/ollama/ollama
# Verify:
# - Number of stars (should be high)
# - Recent activity
# - Official organization/owner
# - Verified badge (if available)
```

## Comparison Table

| Method | Security | Ease | Verification Needed | Updates |
|--------|----------|------|---------------------|----------|
| **Snap** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | None (Canonical verifies) | Automatic |
| **Manual Binary** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Checksum verification | Manual |
| **Install Script (GitHub)** | ⭐⭐⭐ | ⭐⭐⭐⭐ | Code review | Manual |
| **Install Script (Direct)** | ⭐⭐ | ⭐⭐⭐⭐⭐ | Full verification | Manual |

## Final Recommendation

**For Pop!_OS (Ubuntu-based): Use Snap**

```bash
sudo snap install ollama
```

**Why:**
1. ✅ Highest security (Canonical verification + sandboxing)
2. ✅ Easiest installation
3. ✅ Automatic security updates
4. ✅ No manual verification needed
5. ✅ Works perfectly with your Docker setup

**If you can't use Snap:**
- Use manual binary download from GitHub releases
- Always verify checksums
- Review install script if you must use it

## Quick Security Checklist

Before installing any software:

- [ ] Verify source (official website/GitHub)
- [ ] Check SSL certificate
- [ ] Review script/binary if possible
- [ ] Verify checksums
- [ ] Use package manager when available (Snap/Apt)
- [ ] Check for GPG signatures
- [ ] Review what the software does
- [ ] Install in isolated environment first (VM/test machine)

## Resources

- **Official GitHub**: https://github.com/ollama/ollama
- **Snap Store**: https://snapcraft.io/ollama
- **Security Advisories**: Check GitHub security tab
- **Releases**: https://github.com/ollama/ollama/releases

