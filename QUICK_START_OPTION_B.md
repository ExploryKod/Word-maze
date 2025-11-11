# Quick Start: Option B - Dockerized App + Ollama on Host

## Architecture

```
┌─────────────────────────────────────────┐
│         Your Host Machine               │
│                                         │
│  ┌──────────────┐                      │
│  │   Ollama     │  (Running on host)   │
│  │  Port 11434  │                      │
│  └──────┬───────┘                      │
│         │                               │
│         │ http://host.docker.internal   │
│         │                               │
│  ┌──────▼──────────────────────────┐    │
│  │   Docker Container              │    │
│  │   ┌──────────────────────┐    │    │
│  │   │  Flask App (web)     │    │    │
│  │   │  - RAG Service       │────┼────┘
│  │   │  - Connects to       │    │
│  │   │    Ollama on host   │    │
│  │   └──────────────────────┘    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Your Flask app is in Docker, Ollama is on your host machine!**

## Step-by-Step Setup

### 1. Install Ollama on Your Host Machine

```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Or download from https://ollama.ai
```

### 2. Start Ollama on Host

```bash
# In a terminal on your host machine
ollama serve
```

Keep this terminal open! Ollama needs to be running.

### 3. Download a Model on Host

```bash
# In another terminal on your host machine
ollama pull llama2
# or
ollama pull mistral
```

### 4. Configure Docker Compose

Edit `docker-compose.dev.yml` and uncomment these lines:

```yaml
web:
  environment:
    # Uncomment these lines:
    RAG_LLM_PROVIDER: "ollama"
    RAG_MODEL_NAME: "llama2"
    OLLAMA_HOST: "http://host.docker.internal:11434"
  # Uncomment this section:
  extra_hosts:
    - "host.docker.internal:host-gateway"
```

**OR** add to your `.env` file:

```bash
RAG_LLM_PROVIDER=ollama
RAG_MODEL_NAME=llama2
OLLAMA_HOST=http://host.docker.internal:11434
```

### 5. Start Your Dockerized App

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 6. Verify It Works

```bash
# Check if your app can reach Ollama
docker exec -it <your-container-name> curl http://host.docker.internal:11434/api/tags

# Or test the RAG endpoint
curl http://localhost:5000/rag/health
```

## How It Works

1. **Ollama runs on your host** at `localhost:11434`
2. **Your Flask app runs in Docker** container
3. **Docker's `host.docker.internal`** allows the container to access services on the host
4. **Your app connects** to `http://host.docker.internal:11434` to reach Ollama

## Benefits

✅ **Your app is containerized** (isolated, portable, easy to deploy)  
✅ **Ollama is on host** (better performance, shared models, easier management)  
✅ **Best of both worlds!**

## Troubleshooting

### "Connection refused" to Ollama

1. **Check Ollama is running on host:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
   If this fails, start Ollama: `ollama serve`

2. **Check Docker can reach host:**
   ```bash
   docker exec -it <container> ping host.docker.internal
   ```

3. **On Linux, you might need to add to docker-compose:**
   ```yaml
   extra_hosts:
     - "host.docker.internal:host-gateway"
   ```
   (This is already in the config, just make sure it's uncommented)

### "host.docker.internal" not working (Linux)

On Linux, Docker might not support `host.docker.internal` by default. Use:

```yaml
extra_hosts:
  - "host.docker.internal:172.17.0.1"  # Docker bridge IP
```

Or find your Docker bridge IP:
```bash
ip addr show docker0 | grep inet
```

## Summary

**Yes, you can absolutely use Option B!** Your Flask app runs in Docker, Ollama runs on your host, and they communicate via `host.docker.internal`. This is the recommended setup for development.

