# MCP-MultilspyLSP Guidelines

## Commands
- `just setup` - Create venv and install dependencies
- `just test` - Run all tests
- `just test tests/test_server.py::TestMultilspyMcpServer::test_request_definition` - Run single test
- `just lint` - Run linting and type checking
- `just lint-fix` - Automatically fix linting issues
- `just run` - Run the MCP server
- `just dev` - Run the MCP server in development mode
- `just install` - Install the MCP server locally
- `just clean` - Remove temporary files and caches

## Code Style
- **Python Version**: 3.12+
- **Imports**: Group standard lib, third-party, and local imports with blank lines
- **Quotation**: Use double quotes for strings
- **Indentation**: 4 spaces, no tabs
- **Line Length**: 100 characters maximum
- **Type Hints**: Use static typing for all function parameters and return values
- **Error Handling**: Use try/except blocks with specific exceptions; return structured error responses
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
- **Async**: Use async/await for all I/O operations
- **Testing**: Use unittest with AsyncMock for testing async functions