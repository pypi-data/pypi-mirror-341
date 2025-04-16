"""Client functions for llmcp."""
import os
import sys
import time
import asyncio
import fnmatch
import logging
from typing import Dict, List, Tuple

# Disable all logging output below critical
logging.basicConfig(level=logging.CRITICAL)

import litellm
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def get_models() -> Dict[str, str]:
    """Get available models from LiteLLM."""
    # Redirect stdout temporarily to suppress litellm messages
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    
    try:
        models = {}
        # Add essential models
        core_models = {
            "gpt-4o": "OpenAI",
            "gpt-4o-mini": "OpenAI",
            "gpt-3.5-turbo": "OpenAI",
            "anthropic/claude-3-opus-20240229": "Anthropic",
            "anthropic/claude-3-sonnet-20240229": "Anthropic",
            "mistral/mistral-large-latest": "Mistral"
        }
        
        # Add core models
        for model, provider in core_models.items():
            try:
                litellm.get_llm_provider(model=model)
                models[model] = provider
            except:
                pass
        
        # Add additional models
        for model_name, info in list(litellm.model_cost.items())[:100]:  # Limit to avoid excessive processing
            if model_name in models or not model_name.startswith(("gpt", "claude", "mistral")):
                continue
            try:
                _, provider, _, _ = litellm.get_llm_provider(model=model_name)
                models[model_name] = provider.title() 
            except:
                pass
        
        return models
    finally:
        # Restore stdout
        sys.stdout.close()
        sys.stdout = original_stdout

def check_api_key(provider: str) -> bool:
    """Check if API key for the provider is set."""
    key_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "vertex_ai": "GEMINI_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY",
        "groq": "GROQ_API_KEY",
    }
    env_var = key_map.get(provider.lower())
    return env_var and os.environ.get(env_var, "").strip() != ""

def search_models(pattern: str) -> None:
    """Search models matching pattern and check API keys."""
    models = get_models()
    matching = {name: provider for name, provider in models.items() 
               if fnmatch.fnmatch(name.lower(), pattern.lower())}
    
    if not matching:
        print(f"No models found matching: {pattern}")
        return
    
    # Group by provider
    by_provider = {}
    for name, provider in matching.items():
        if provider not in by_provider:
            by_provider[provider] = []
        by_provider[provider].append(name)
    
    # Print results
    print(f"Models matching: {pattern}")
    print("-" * 50)
    
    provider_keys = {}
    for provider in by_provider:
        provider_keys[provider] = check_api_key(provider.lower())
    
    for provider, models_list in sorted(by_provider.items()):
        has_key = provider_keys[provider]
        key_status = "✓" if has_key else "✗"
        print(f"{provider} [{key_status}]")
        for model in sorted(models_list):
            print(f"  {model}")
        print()
    
    print("API Key: ✓ = available, ✗ = missing")

async def test_model_async(model_name: str, prompt: str) -> None:
    """Test a model by starting an MCP server and sending a prompt."""
    server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script, model_name],
        env=os.environ.copy()
    )
    
    print(f"Testing model: {model_name}")
    print(f"Prompt: \"{prompt}\"")
    
    try:
        start_time = time.time()
        
        async with stdio_client(server_params) as (read, write):
            print("Server started")
            
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                tools = await session.list_tools()
                if "ask" not in [t.name for t in tools.tools]:
                    print("Error: 'ask' tool not available")
                    return
                
                print("Sending prompt...")
                result = await session.call_tool("ask", arguments={"prompt": prompt})
                
                response_text = None
                for content in result.content:
                    if content.type == "text":
                        response_text = content.text
                        break
                
                if not response_text:
                    print("Error: No response received")
                    return
                
                duration = time.time() - start_time
                print("\nResponse:")
                print(response_text)
                print(f"Time: {duration:.2f}s")
    
    except Exception as e:
        print(f"Error: {str(e)}")

def test_model(model_name: str, prompt: str) -> None:
    """Entry point for testing a model."""
    asyncio.run(test_model_async(model_name, prompt))