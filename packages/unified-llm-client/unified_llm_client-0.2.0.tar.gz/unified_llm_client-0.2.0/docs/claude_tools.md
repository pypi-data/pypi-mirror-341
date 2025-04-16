# Using Claude with Tools

This document provides important information about working with Claude and the Unified LLM Client's tools support.

## Claude Tools Support

Claude supports a different tool format compared to OpenAI. The Unified LLM Client handles the conversion, but there are some important details to be aware of.

## Tool Choice Parameter

When using the `tool_choice` parameter, different providers have different requirements:

- **OpenAI**: 
  - For Chat Completions API: Use `tool_choice="auto"` or `tool_choice="none"` as a string.
  - For the Responses API: The tool_choice parameter has limited support and may cause errors.

- **Claude**: 
  - Claude doesn't support the `tool_choice` parameter officially, but you can use `tool_choice="auto"` for consistency.
  - The parameter will simply be ignored by Claude's API.

Example of using tool_choice with OpenAI:

```python
response = await client.response(
    prompt,
    model="gpt-4o",
    instructions="You are a helpful assistant.",
    tool_choice="auto",  # As a string, not a dict
    use_responses_api=False  # Use Chat Completions API
)
```

### Schema Format Requirements

Claude tool schemas require the following structure:

```python
tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",  # This field is required!
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA"
            }
        },
        "required": ["location"]
    }
}
```

Note that the `"type": "object"` field in the `input_schema` is required by Claude's API and must be present.

### Working with Claude Tools

When using tools with Claude, consider the following best practices:

1. **Use Explicit Instructions**: Always include clear instructions telling Claude to use the tools available to it, for example: "Use the provided tools to answer the user's question thoroughly."

2. **Check Schema Format**: For debugging tool issues, set `anthropic_tool_debug=True` when calling `response()` to see the exact tool schemas being sent to Claude.

3. **Handle Tool Responses Gracefully**: Claude may sometimes truncate responses when using tools, especially with multiple tools. Consider using a conversational approach, providing tool outputs and asking for a synthesis.

## Example Usage

Here's an example of using Claude with tools and debugging the tool schemas:

```python
import asyncio
from llm import AsyncLLMClient, ToolRegistry, llm_tool

@llm_tool
def get_weather(location: str, unit: str = "celsius"):
    """Get the current weather for a location."""
    # Implementation...
    return weather_data

async def main():
    tools = ToolRegistry()
    tools.register("get_weather", get_weather)
    
    client = AsyncLLMClient(tool_registry=tools)
    
    # Enable debug mode to see tool schemas
    response = await client.response(
        "What's the weather like in Paris?",
        model="claude-3-5-haiku-latest",
        instructions="You are a helpful assistant that can check the weather. Use the provided tools.",
        temperature=0.7,
        anthropic_tool_debug=True  # Enable debug mode
    )
    
    print(response["text"])

if __name__ == "__main__":
    asyncio.run(main())
```

## Troubleshooting Claude Tools

If you're experiencing issues with Claude and tools:

1. Enable debug mode with `anthropic_tool_debug=True`
2. Check that the tool schema includes `"type": "object"` in the `input_schema`
3. Verify that required parameters like "location" are correctly specified
4. Consider increasing `max_tokens` to ensure complete responses

For more complex scenarios, see the examples in the `examples/` directory, particularly `claude_tools_example.py` and `claude_weather_example.py`.

## Comparing to OpenAI's Tool Format

For reference, here's how Claude's tool format differs from OpenAI's:

### Claude Format
```python
{
    "name": "get_weather",
    "description": "Get the weather in a location",
    "input_schema": {
        "type": "object",
        "properties": { /* ... */ },
        "required": [ /* ... */ ]
    }
}
```

### OpenAI Format
```python
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather in a location",
        "parameters": {
            "type": "object",
            "properties": { /* ... */ },
            "required": [ /* ... */ ]
        }
    }
}
```

The Unified LLM Client handles this conversion automatically, but understanding the differences can help when debugging tool issues.

@author: skitsanos
