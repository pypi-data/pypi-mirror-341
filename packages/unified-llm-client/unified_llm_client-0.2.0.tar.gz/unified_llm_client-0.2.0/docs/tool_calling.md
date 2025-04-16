# Tool Calling with the Unified LLM Client

This document explains how to use tool calling (also known as function calling) with the Unified LLM Client across different providers.

## Overview

Tool calling allows LLMs to invoke external functions to perform tasks they can't do directly, such as accessing real-time data, performing calculations, or interacting with external systems.

The Unified LLM Client provides a consistent interface for tool calling across providers (OpenAI, Anthropic, etc.) by handling the provider-specific format differences automatically.

## Defining Tools

The recommended way to define tools is using the `llm_tool` decorator:

```python
from llm.tooling import llm_tool

@llm_tool
async def get_weather(location: str, unit: str = "celsius"):
    """
    Get current weather for a location.
    
    Args:
        location: City name (e.g., "San Francisco")
        unit: Temperature unit (celsius or fahrenheit)
        
    Returns:
        Dictionary with weather information
    """
    # Implementation here
    return {
        "temperature": 22,
        "conditions": "sunny",
        "humidity": 65
    }
```

The decorator automatically creates schema definitions for both OpenAI and Anthropic formats.

## Registering Tools

Tools must be registered with a `ToolRegistry`:

```python
from llm.tooling import ToolRegistry

# Create registry
registry = ToolRegistry()

# Register tools
registry.register("get_weather", get_weather)
registry.register("search_web", search_web)
```

## Using Tools with the Unified Client

The key advantage of the Unified LLM Client is that you can use the same tools with different providers:

```python
from llm.client import AsyncLLMClient

# Create client with tool registry
client = AsyncLLMClient(tool_registry=registry)

# Use with OpenAI
openai_response = await client.response(
    "What's the weather in San Francisco?",
    model="gpt-4o",
    instructions="You have access to weather information."
)

# Use with Anthropic (same client, same tools)
anthropic_response = await client.response(
    "What's the weather in New York?",
    model="claude-3-5-haiku-latest",
    instructions="You have access to weather information."
)
```

The client automatically handles format conversion between providers!

## Format Differences

### OpenAI Tool Format

OpenAI uses this format:

```python
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "unit": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}
```

### Anthropic Tool Format

Anthropic uses this simpler format:

```python
{
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string"}
        },
        "required": ["location"]
    }
}
```

The client automatically handles this conversion under the hood!

## Complete Example

```python
import asyncio
from llm.client import AsyncLLMClient
from llm.tooling import ToolRegistry, llm_tool
from dotenv import load_dotenv

@llm_tool
async def get_weather(location: str):
    """Get weather for a location."""
    return {"temperature": 72, "conditions": "sunny"}

@llm_tool
async def search_web(query: str, max_results: int = 3):
    """Search the web for information."""
    return {"results": [f"Result for {query}"]}

async def main():
    load_dotenv()  # Load API keys from .env file
    
    # Set up registry
    registry = ToolRegistry()
    registry.register("get_weather", get_weather)
    registry.register("search_web", search_web)
    
    # Create unified client
    client = AsyncLLMClient(tool_registry=registry)
    
    # Example query
    query = "What's the weather in Paris and find information about the Eiffel Tower."
    
    # Call different providers with the same client and tools
    providers = [
        {"name": "OpenAI", "model": "gpt-4o-mini"},
        {"name": "Anthropic", "model": "claude-3-5-haiku-latest"}
    ]
    
    for provider in providers:
        print(f"\nTesting with {provider['name']}...")
        try:
            response = await client.response(
                user_input=query,
                model=provider["model"],
                instructions="You are a helpful assistant with access to tools."
            )
            print(f"\nResponse from {provider['name']}:")
            print(response["text"])
        except Exception as e:
            print(f"Error with {provider['name']}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Supported Models

These models are known to support tool calling:

- OpenAI: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo
- Anthropic: claude-3-5-haiku-latest (primary supported model), claude-3-haiku-20240307, claude-3-5-haiku-20240307

## Error Handling

The client includes built-in error handling for common tool-related issues:

- Missing tools in registry
- Format conversion problems
- Provider-specific tool errors

All errors are logged and propagated appropriately.

## Advanced Features

- **Structured Outputs**: Tool functions can return dictionaries, lists, or other structured data
- **Type Validation**: Parameters are converted to the appropriate types when possible
- **Format Conversion**: The client handles all format differences between providers automatically
