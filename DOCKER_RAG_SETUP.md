# Docker RAG Setup Guide

This guide explains how to configure RAG (Retrieval-Augmented Generation) with your Docker setup.

## Overview

Your Docker configuration supports RAG in three ways:
1. **Ollama in Docker** (recommended for development)
2. **Ollama on host machine** (access from container)
3. **Hugging Face API** (cloud-based, no container needed)

## Option 1: Ollama in Docker

This runs Ollama as a separate service in your docker-compose setup.

### Setup Steps

1. **Uncomment Ollama service in `docker-compose.dev.yml`**:
   ```yaml
   services:
     ollama:
       image: ollama/ollama:latest
       container_name: word-maze-ollama
       ports:
         - "11434:11434"
       volumes:
         - ollama_data:/root/.ollama
   ```

2. **Uncomment dependencies and volumes**:
   ```yaml
   web:
     depends_on:
       - ollama
   ```

3. **Configure environment variables**:
   ```yaml
   web:
     environment:
       RAG_LLM_PROVIDER: "ollama"
       RAG_MODEL_NAME: "llama2"
       OLLAMA_HOST: "http://ollama:11434"  # Use service name
   ```

4. **Start services**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

5. **Download a model in Ollama container**:
   ```bash
   docker exec -it word-maze-ollama ollama pull llama2
   # or
   docker exec -it word-maze-ollama ollama pull mistral
   ```

### Advantages
- ✅ Isolated environment (no conflicts with host)
- ✅ Easy to reset/restart
- ✅ No host machine setup needed
- ✅ Consistent across team members

### Disadvantages
- ⚠️ Models need to be downloaded in container (can be large: 4-7GB per model)
- ⚠️ Slower performance (container overhead)
- ⚠️ Models not shared with other projects
- ⚠️ Uses more disk space (separate model storage)

### When to Use
- ✅ You want complete isolation
- ✅ Team members don't have Ollama installed
- ✅ You're testing different model versions
- ✅ You want to easily reset the entire environment

## Option 2: Ollama on Host Machine (Recommended for Development)

If you have Ollama running on your host machine, access it from the container. **This is often the better choice for development.**

### Setup Steps

1. **Start Ollama on your host**:
   ```bash
   ollama serve
   ```

2. **Download a model**:
   ```bash
   ollama pull llama2
   ```

3. **Configure `docker-compose.dev.yml`**:
   ```yaml
   web:
     environment:
       RAG_LLM_PROVIDER: "ollama"
       RAG_MODEL_NAME: "llama2"
       OLLAMA_HOST: "http://host.docker.internal:11434"
     extra_hosts:
       - "host.docker.internal:host-gateway"
   ```

4. **Start services**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

### Advantages
- ✅ **Reuse existing Ollama installation** (no duplicate setup)
- ✅ **Share models** between containers and projects (save disk space)
- ✅ **Better performance** (no container overhead, direct access)
- ✅ **Easier model management** (use `ollama list`, `ollama pull` directly)
- ✅ **Faster startup** (models already downloaded)
- ✅ **Less resource usage** (single Ollama instance)

### Disadvantages
- ⚠️ Requires Ollama installed on host machine
- ⚠️ Need to ensure Ollama is running before starting containers
- ⚠️ Slightly more complex networking setup

### When to Use
- ✅ **You already have Ollama installed** (most common case)
- ✅ **You want better performance** (development workflow)
- ✅ **You work with multiple projects** (share models)
- ✅ **You want to save disk space** (models are large)
- ✅ **You prefer managing models directly** (easier debugging)

## Option 3: Hugging Face API (No Container Needed)

Use Hugging Face's free API tier. No Docker service needed.

### Setup Steps

1. **Get Hugging Face API key**:
   - Sign up at https://huggingface.co/join
   - Get token from https://huggingface.co/settings/tokens

2. **Configure `docker-compose.dev.yml`**:
   ```yaml
   web:
     environment:
       RAG_LLM_PROVIDER: "huggingface"
       HUGGINGFACE_API_KEY: "your_token_here"
       HUGGINGFACE_MODEL: "mistralai/Mistral-7B-Instruct-v0.2"
   ```

3. **Or use `.env` file**:
   ```bash
   # .env
   RAG_LLM_PROVIDER=huggingface
   HUGGINGFACE_API_KEY=your_token_here
   HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
   ```

4. **Start services**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

### Advantages
- ✅ No local resources needed
- ✅ Works immediately
- ✅ No model downloads

### Disadvantages
- ⚠️ Rate limits on free tier
- ⚠️ Requires internet connection
- ⚠️ API key management

## Production Setup (`docker-compose.yml`)

For production, it's recommended to:

1. **Use Ollama on host machine** (if you have a server):
   ```yaml
   environment:
     RAG_LLM_PROVIDER: "ollama"
     RAG_MODEL_NAME: "llama2"
     OLLAMA_HOST: "http://host.docker.internal:11434"
   extra_hosts:
     - "host.docker.internal:host-gateway"
   ```

2. **Or use Hugging Face** (if you prefer cloud):
   ```yaml
   environment:
     RAG_LLM_PROVIDER: "huggingface"
     HUGGINGFACE_API_KEY: "${HUGGINGFACE_API_KEY}"
     HUGGINGFACE_MODEL: "mistralai/Mistral-7B-Instruct-v0.2"
   ```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `RAG_LLM_PROVIDER` | `ollama` or `huggingface` | `ollama` | No |
| `RAG_MODEL_NAME` | Model name (Ollama) | `llama2` | No |
| `OLLAMA_HOST` | Ollama API URL | `http://localhost:11434` | No |
| `HUGGINGFACE_API_KEY` | HF API token | - | Yes (if using HF) |
| `HUGGINGFACE_MODEL` | HF model name | `mistralai/Mistral-7B-Instruct-v0.2` | No |

## Volume Persistence

The RAG vector database is persisted in a Docker volume:
- **Development**: `rag_db` volume (mounted to `/python-docker/rag_db`)
- **Production**: `rag_db` volume (persisted across restarts)

To reset the knowledge base:
```bash
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

## Testing RAG in Docker

1. **Check RAG health**:
   ```bash
   curl http://localhost:5000/rag/health
   ```

2. **Test hint generation**:
   ```bash
   curl "http://localhost:5000/rag/hint?theme=Sens&letters=abc"
   ```

3. **Check logs**:
   ```bash
   docker-compose -f docker-compose.dev.yml logs web
   docker-compose -f docker-compose.dev.yml logs ollama  # if using Ollama service
   ```

## Troubleshooting

### "Ollama n'est pas démarré"

**If using Ollama in Docker:**
```bash
# Check if Ollama container is running
docker ps | grep ollama

# Check Ollama logs
docker logs word-maze-ollama

# Restart Ollama
docker-compose -f docker-compose.dev.yml restart ollama
```

**If using Ollama on host:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

### "Connection refused" to Ollama

- Verify `OLLAMA_HOST` is correct
- For Docker service: use `http://ollama:11434`
- For host machine: use `http://host.docker.internal:11434`
- Ensure `extra_hosts` is configured for host access

### Hugging Face API errors

- Verify API key is set: `echo $HUGGINGFACE_API_KEY`
- Check rate limits: https://huggingface.co/settings/usage
- Try a different model if current one is unavailable

### Vector database issues

- Check volume is mounted: `docker volume ls | grep rag_db`
- Reset if needed: `docker-compose -f docker-compose.dev.yml down -v`

## Recommended Setup by Environment

### Development
- **⭐ Option 2 (Recommended)**: Ollama on host - Better performance, easier model management, saves disk space
- **Option 1**: Ollama in Docker - Only if you need isolation or team members don't have Ollama
- **Option 3**: Hugging Face - If you don't want to install Ollama locally

### Production
- **Option 2**: Ollama on host/server (better resource management, shared models)
- **Option 1**: Ollama in Docker (if you prefer containerized services)
- **Option 3**: Hugging Face (if no server resources available or prefer cloud)

## GPU Support (Optional)

If you have NVIDIA GPU and want to use it with Ollama:

1. Install nvidia-docker: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

2. Uncomment GPU configuration in `docker-compose.dev.yml`:
   ```yaml
   ollama:
     deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               count: 1
               capabilities: [gpu]
   ```

3. Restart services:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

GPU acceleration significantly improves response times for larger models.

