# Local Ollama-based Claude Agent

This directory contains the implementation of a local model-based Claude agent using Ollama as the backend.

## Overview

This agent uses Ollama to run local language models as a replacement for the cloud-based Claude API. This allows for:

- **Privacy**: All processing happens locally
- **Offline capability**: No internet connection required
- **Cost**: Free to use (no API calls)
- **Customization**: Use any model supported by Ollama

## Prerequisites

1. **Install Ollama**: https://ollama.ai
2. **Pull a model**: `ollama pull llama3.2` (or any other supported model)
3. **Ensure Ollama is running**: `ollama serve`

## Configuration

Set the following environment variables:

```bash
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_API_KEY="ollama"  # Required by the SDK but not used
export ANTHROPIC_MODEL="llama3.2"  # Your chosen Ollama model
```

## Usage

See `ollama_agent.py` for a basic implementation.

## Limitations

- Local models may have different capabilities than Claude
- Response quality depends on the chosen model
- Some Claude-specific features may not be supported
