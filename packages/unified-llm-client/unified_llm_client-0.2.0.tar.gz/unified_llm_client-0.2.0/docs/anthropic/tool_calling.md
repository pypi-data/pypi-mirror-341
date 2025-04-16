# Anthropic Tool Calling Guide

This guide explains how to use tool calling with Anthropic Claude models in the Unified LLM Client.

## Overview

Anthropic Claude models support tool calling through their API, but the format differs from OpenAI's tool calling format. The Unified LLM Client provides a seamless experience by automatically converting between these formats.

### Supported Models

Tool calling is confirmed to work with the following Anthropic models:

- `claude-3-5-haiku-latest` (primary supported model)
- `claude-3-haiku-20240307`
- `claude-3-5-haiku-20240307`

Other Claude models may work but are not guaranteed to support tool calling.

## Tool Definition

### Anthropic's Tool Format

Anthropic uses a simpler schema for tools compared to OpenAI:

```python
{
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            }
        },
        "required": ["location"],
    }
}
```

### Using the `llm_tool` Decorator

The recommended way to define tools is using the `llm_tool` decorator, which automatically creates compatible schemas for both OpenAI and Anthropic:

```python
from llm.tooling import llm_tool

@llm_tool
async def get_weather(location: str):
    """
    Get the current weather in a given location.
    
    Args:
        location: The city and state, e.g. San Francisco, CA
    
    Returns:
        A dictionary with weather information
    """
    # Implementation
    return {"temperature": 72, "conditions": "sunny"}
```

## Tool Registry

The `ToolRegistry` class manages your tools and automatically handles format conversions:

```python
from llm.tooling import ToolRegistry

# Create a registry
registry = ToolRegistry()

# Register tools
registry.register("get_weather", get_weather)
registry.register("search", search_function)

# Get tools in Anthropic format
anthropic_tools = registry.get_schemas("anthropic")
```

## Making Tool Calls with Anthropic

```python
from anthropic import AsyncAnthropic
from llm.anthropic import handle_anthropic_api

# Initialize client
client = AsyncAnthropic(api_key="your-api-key")

# Call the API with tools
response = await handle_anthropic_api(
    client=client,
    user_input="What's the weather in San Francisco?",
    model="claude-3-5-haiku-latest",
    instructions="You are a helpful assistant with access to tools.",
    tools=anthropic_tools,
    tool_registry=registry,
    temperature=0.0,
    max_tokens=1024,
)

# Access the final response
print(response["text"])
```

## Format Conversion

The Unified LLM Client automatically converts between different tool formats:

### From OpenAI Format to Anthropic Format

```python
# OpenAI format
openai_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather information",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}

# Automatically converted to Anthropic format
# {
#     "name": "get_weather",
#     "description": "Get weather information",
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "location": {"type": "string"}
#         },
#         "required": ["location"]
#     }
# }
```

## Complete Example

See `/examples/anthropic_tool_example.py` for a complete, working example of tool calling with Anthropic Claude models.

```python
# Basic usage
tool_registry = ToolRegistry()
tool_registry.register("get_weather", get_weather)
tools = tool_registry.get_schemas("anthropic")

response = await handle_anthropic_api(
    client=client,
    user_input="What's the weather like in San Francisco?",
    model="claude-3-5-haiku-latest", 
    tools=tools,
    tool_registry=tool_registry,
)
```

## Troubleshooting

If you encounter issues with tool calling:

1. Ensure you're using a supported model (`claude-3-5-haiku-latest` is recommended)
2. Check your tool definitions match the expected format
3. Enable DEBUG logging to see detailed information about the tool conversion and execution process

## Limitations

- Recursive tool calls are not currently supported
- Some Claude models may not fully support tool calling
- The exact format of tool responses may vary between API versions
