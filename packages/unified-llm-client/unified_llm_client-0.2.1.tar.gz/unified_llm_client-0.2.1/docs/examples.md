# Examples

This page provides examples of using the Unified LLM Client for various scenarios.

## Basic Example

Simple usage with different LLM providers:

```python
import asyncio
from llm import AsyncLLMClient

async def main():
    # Initialize the client
    client = AsyncLLMClient()
    
    # OpenAI
    openai_response = await client.response(
        "Explain quantum computing in simple terms",
        model="gpt-4o-mini"
    )
    
    print("OpenAI response:", openai_response["text"])
    
    # Anthropic
    anthropic_response = await client.response(
        "Explain quantum computing in simple terms",
        model="claude-3-5-haiku-latest"
    )
    
    print("Anthropic response:", anthropic_response["text"])
    
    # Ollama (local models)
    ollama_client = AsyncLLMClient(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    
    ollama_response = await ollama_client.response(
        "Explain quantum computing in simple terms",
        model="llama3",
        use_responses_api=False
    )
    
    print("Ollama response:", ollama_response["text"])

if __name__ == "__main__":
    asyncio.run(main())
```

## OpenAI Tools Example

Using tools with OpenAI models:

```python
import asyncio
import json
from llm import AsyncLLMClient, ToolRegistry, llm_tool

@llm_tool
async def get_weather(location: str, unit: str = "celsius"):
    """Get the current weather for a location."""
    # Mock implementation
    return {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "sunny"
    }

async def main():
    # Create tool registry
    tools = ToolRegistry()
    tools.register("get_weather", get_weather)
    
    # Initialize client with tools
    client = AsyncLLMClient(tool_registry=tools)
    
    # Call OpenAI with tools
    response = await client.response(
        "What's the weather like in Paris?",
        model="gpt-4o",
        instructions="You are a helpful assistant with access to tools."
    )
    
    print(response["text"])

if __name__ == "__main__":
    asyncio.run(main())
```

## Anthropic Tool Calling

Using tools with Anthropic Claude:

```python
import asyncio
from llm import AsyncLLMClient, ToolRegistry, llm_tool

@llm_tool
def calculator(expression: str) -> float:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: A string containing a mathematical expression like "123 * 456"
    """
    # Create a safe evaluation environment
    safe_dict = {
        'abs': abs, 'round': round,
        'min': min, 'max': max,
        'sum': sum, 'pow': pow
    }
    
    # Replace common math operators with Python syntax
    expression = expression.replace('×', '*').replace('÷', '/')
    
    try:
        # Safely evaluate the expression
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return float(result)
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    # Create tool registry
    tools = ToolRegistry()
    tools.register("calculator", calculator)
    
    # Initialize client with tools
    client = AsyncLLMClient(tool_registry=tools)
    
    # Call Claude with tools
    response = await client.response(
        "What is 123 multiplied by 456? Use the calculator tool to find the exact answer.",
        model="claude-3-5-haiku-latest",
        instructions="You have access to a calculator tool. Use it for precise calculations."
    )
    
    print(response["text"])

if __name__ == "__main__":
    asyncio.run(main())
```

## Ollama Tools Example

Using tools with Ollama:

```python
import asyncio
from llm import AsyncLLMClient, ToolRegistry, llm_tool

@llm_tool
def search_database(query: str, limit: int = 5):
    """Search a database for information."""
    # Mock implementation
    results = [{"id": i, "title": f"Result {i} for {query}"} for i in range(limit)]
    return results

async def main():
    # Create tool registry
    tools = ToolRegistry()
    tools.register("search_database", search_database)
    
    # Initialize client with tools
    client = AsyncLLMClient(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        tool_registry=tools
    )
    
    # Call Ollama with tools
    response = await client.response(
        "Find information about machine learning frameworks",
        model="qwen2.5",  # Qwen models have better tool support
        instructions="You are a helpful assistant with access to a database search tool.",
        use_responses_api=False
    )
    
    print(response["text"])

if __name__ == "__main__":
    asyncio.run(main())
```

## Streaming Example

Streaming responses for improved UX:

```python
import asyncio
from llm import AsyncLLMClient

async def handle_chunk(chunk: str):
    print(chunk, end="", flush=True)

async def main():
    # Initialize client
    client = AsyncLLMClient()
    
    # Stream from OpenAI
    print("\nStreaming from OpenAI:")
    response = await client.stream(
        "Explain how quantum computers work in simple terms",
        model="gpt-4o-mini",
        stream_handler=handle_chunk
    )
    
    print(f"\n\nTokens used: {response['input_tokens']} input, {response['output_tokens']} output")
    
    # Stream from Anthropic
    print("\nStreaming from Anthropic:")
    response = await client.stream(
        "Explain how quantum computers work in simple terms",
        model="claude-3-5-haiku-latest",
        stream_handler=handle_chunk
    )
    
    print(f"\n\nTokens used: {response['input_tokens']} input, {response['output_tokens']} output")

if __name__ == "__main__":
    asyncio.run(main())
```

For more examples, check the `examples/` directory in the project repository:

- `01_basic_example.py` - Basic usage
- `02_openai_tools_example.py` - OpenAI tool calling
- `03_ollama_tools_example.py` - Ollama tool calling
- `04_anthropic_tool_calling.py` - Anthropic tool calling
- `05_streaming.py` - Streaming examples

@author: skitsanos