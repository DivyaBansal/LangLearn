#!/usr/bin/env python3
"""
Local Ollama-based Claude Agent

This module demonstrates how to use Ollama as a backend for a Claude-like agent.
It uses the Anthropic SDK with Ollama's compatibility layer.

Requirements:
    pip install anthropic

Setup:
    1. Install Ollama: https://ollama.ai
    2. Pull a model: ollama pull llama3.2
    3. Start Ollama: ollama serve

Environment Variables:
    ANTHROPIC_BASE_URL: http://localhost:11434
    ANTHROPIC_API_KEY: ollama (required but not used)
    ANTHROPIC_MODEL: llama3.2 (or your chosen model)
"""

import os
from typing import Optional


def check_ollama_connection() -> bool:
    """Check if Ollama is running and accessible."""
    import urllib.request
    import json

    base_url = os.environ.get("ANTHROPIC_BASE_URL", "http://localhost:11434")

    try:
        req = urllib.request.Request(f"{base_url}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            models = data.get("models", [])
            if models:
                print(f"✓ Ollama is running with {len(models)} model(s)")
                for model in models:
                    print(f"  - {model['name']}")
                return True
            else:
                print("✗ Ollama is running but no models are installed")
                print("  Run: ollama pull llama3.2")
                return False
    except Exception as e:
        print(f"✗ Cannot connect to Ollama at {base_url}")
        print(f"  Error: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False


def create_agent(model: Optional[str] = None):
    """
    Create an agent instance using Ollama as the backend.

    Args:
        model: The model to use (defaults to ANTHROPIC_MODEL env var or 'llama3.2')

    Returns:
        An initialized Anthropic client configured for Ollama
    """
    from anthropic import Anthropic

    base_url = os.environ.get("ANTHROPIC_BASE_URL", "http://localhost:11434")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "ollama")
    model_name = model or os.environ.get("ANTHROPIC_MODEL", "llama3.2")

    print(f"Configuring agent with:")
    print(f"  Base URL: {base_url}")
    print(f"  Model: {model_name}")

    client = Anthropic(
        base_url=base_url,
        api_key=api_key,
    )

    return client, model_name


def chat(client, model: str, message: str, system_prompt: Optional[str] = None):
    """
    Send a message to the agent and get a response.

    Args:
        client: The Anthropic client from create_agent()
        model: The model name
        message: The user's message
        system_prompt: Optional system prompt

    Returns:
        The model's response
    """
    messages = [{"role": "user", "content": message}]

    params = {
        "model": model,
        "messages": messages,
        "max_tokens": 4096,
    }

    if system_prompt:
        # Ollama's messages API doesn't support system prompt directly
        # We prepend it to the user message
        messages[0]["content"] = f"{system_prompt}\n\n{message}"

    try:
        response = client.messages.create(**params)
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"


def main():
    """Main entry point for testing the Ollama agent."""
    print("=" * 50)
    print("Local Ollama-based Claude Agent")
    print("=" * 50)
    print()

    # Check Ollama connection
    if not check_ollama_connection():
        print("\nFailed to connect to Ollama. Please ensure:")
        print("  1. Ollama is installed (https://ollama.ai)")
        print("  2. Ollama is running: ollama serve")
        print("  3. A model is installed: ollama pull llama3.2")
        return 1

    print()

    # Create agent
    client, model = create_agent()

    print()
    print("Agent ready! Type messages to chat (type 'quit' to exit)")
    print("-" * 50)

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break

            if not user_input:
                continue

            print("\nAgent: ", end="", flush=True)
            response = chat(client, model, user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

    return 0


if __name__ == "__main__":
    exit(main())
