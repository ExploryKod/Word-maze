#!/bin/bash
# Entrypoint script for Ollama container
# Automatically pulls tinyllama model on first start

# Start Ollama in background
ollama serve &

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama is ready!"
        break
    fi
    sleep 1
done

# Pull tinyllama model if not already present
echo "Checking for tinyllama model..."
if ! ollama list | grep -q "tinyllama"; then
    echo "Pulling tinyllama:latest model..."
    ollama pull tinyllama:latest
    echo "tinyllama model downloaded successfully!"
else
    echo "tinyllama model already exists, skipping download."
fi

# Pre-warm the model by making a test request (loads model into memory)
echo "Pre-warming tinyllama model..."
ollama run tinyllama "test" > /dev/null 2>&1 || true
echo "Model pre-warming complete!"

# Keep container running
wait

