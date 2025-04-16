# Changelog

## Version 0.2.0 (April 2025)

### New Features

- **Streaming Support**: Added `stream()` method to provide streaming responses from both OpenAI and Anthropic models, improving perceived latency and user experience
- **Enhanced Anthropic Integration**: Improved support for Claude models with better tool handling and conversion
- **Claude Tool Calling**: Enhanced support for tool calling with Claude models, including proper schema conversion and debugging options
- **Ollama Improvements**: Better integration with Ollama for running local models, including streaming support
- **Type Safety**: Improved type hints throughout the codebase

### Documentation Improvements

- Added comprehensive documentation for Claude tool calling
- Created new examples showcasing streaming functionality
- Added detailed API reference documentation for new methods
- Improved quickstart guide with streaming examples

### Bug Fixes

- Fixed issues with tool schema conversion between different provider formats
- Improved error handling for tool execution
- Enhanced token counting accuracy for streaming responses

### Internal Changes

- Refactored tool handling code for better maintainability
- Improved architecture for streaming support
- Added more robust error handling throughout the codebase

## Version 0.1.0 (Initial Release)

- Initial release of Unified LLM Client
- Support for OpenAI, Anthropic, and Ollama
- Basic tool calling support
- Async-first design

@author: skitsanos