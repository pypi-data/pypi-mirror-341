# llmcp

A minimal CLI for interacting with LLMs via LiteLLM and MCP.

## Installation

```bash
pip install llmcp
```

## Configuration

Set up your API keys as environment variables:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-..."

# Other providers
export GEMINI_API_KEY="..."
export MISTRAL_API_KEY="..."
export COHERE_API_KEY="..."
export GROQ_API_KEY="..."
```

## Usage

### Search for available models

```bash
# Search for all models
llmcp search "*"

# Search for specific models
llmcp search "gpt4*"
```

### Start an MCP server for a specific model

```bash
# Start a server with a specific model
llmcp serve gpt-4o-mini
```

### Test a model with a prompt

```bash
# Test a model with a prompt
llmcp test gpt-4o-mini "What is the capital of France?"
```

## Features

- Model search with API key validation
- MCP server with a minimalist ask tool
- Maximum token usage by default