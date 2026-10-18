#!/usr/bin/env bash
#
# Check Ollama Setup
# This script verifies that Ollama is properly configured and ready to use.

set -e

echo "=============================================="
echo "Checking Ollama Setup for Local Claude Agent"
echo "=============================================="
echo ""

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed"
    echo ""
    echo "To install Ollama:"
    echo "  curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  # or visit: https://ollama.ai"
    exit 1
fi

echo "✓ Ollama is installed: $(ollama --version 2>/dev/null || echo 'unknown version')"
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null 2>&1; then
    echo "⚠ Ollama server is not running"
    echo ""
    echo "To start Ollama:"
    echo "  ollama serve"
    echo ""
    echo "Or check if it's running on a different port"
else
    echo "✓ Ollama server is running"
fi
echo ""

# Check available models
echo "Checking available models..."
if ollama list &> /dev/null; then
    MODELS=$(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}' | grep -v "NAME")
    if [ -z "$MODELS" ]; then
        echo "⚠ No models installed"
        echo ""
        echo "Recommended models for Claude-like experience:"
        echo "  ollama pull llama3.2   # Lightweight, fast"
        echo "  ollama pull llama3.1   # More capable"
        echo "  ollama pull qwen2.5    # Strong reasoning"
    else
        echo "✓ Installed models:"
        echo "$MODELS" | while read -r model; do
            echo "  - $model"
        done
    fi
else
    echo "⚠ Could not list models"
fi
echo ""

# Test connection
BASE_URL="${ANTHROPIC_BASE_URL:-http://localhost:11434}"
echo "Testing connection to $BASE_URL..."
if curl -s "$BASE_URL/api/tags" > /dev/null 2>&1; then
    echo "✓ Connection successful"
else
    echo "❌ Cannot connect to Ollama at $BASE_URL"
    echo ""
    echo "Make sure Ollama is running:"
    echo "  ollama serve"
    exit 1
fi
echo ""

echo "=============================================="
echo "Setup Complete!"
echo "=============================================="
echo ""
echo "To use the Ollama-based Claude agent:"
echo ""
echo "1. Set environment variables:"
echo "   export ANTHROPIC_BASE_URL=http://localhost:11434"
echo "   export ANTHROPIC_API_KEY=ollama"
echo "   export ANTHROPIC_MODEL=llama3.2  # or your preferred model"
echo ""
echo "2. Install Python dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "3. Run the agent:"
echo "   python ollama_agent.py"
echo ""
