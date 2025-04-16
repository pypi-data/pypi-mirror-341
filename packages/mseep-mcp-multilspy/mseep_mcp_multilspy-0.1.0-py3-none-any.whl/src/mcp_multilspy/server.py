import asyncio
import os
from dataclasses import dataclass
from typing import Any

from mcp.server.fastmcp import FastMCP
from multilspy import LanguageServer
from multilspy.multilspy_config import Language, MultilspyConfig
from multilspy.multilspy_logger import MultilspyLogger

# Create an MCP server
mcp = FastMCP("MultilspyLSP")


@dataclass
class LspSession:
    """Active language server session with associated project root."""

    language_server: LanguageServer
    project_root: str
    language: Language


# Global mapping of session_id to language server instances
lsp_sessions: dict[str, LspSession] = {}


@mcp.tool()
async def initialize_language_server(
    session_id: str,
    project_root: str,
    language: str,
    debug: bool = False,
) -> dict[str, Any]:
    """
    Initialize a language server for the specified language and project.

    Parameters:
        session_id: Unique identifier for this language server session
        project_root: Absolute path to the project root directory
        language: Programming language to initialize the server for (e.g., "python", "java", "typescript")
        debug: Enable debug logging
    
    Returns:
        Dictionary containing session info and initialization status
    """
    # Validate the language is supported
    try:
        lang = Language(language.upper())
    except ValueError:
        supported = [l.name.lower() for l in Language]
        return {
            "success": False,
            "error": f"Unsupported language: {language}. Supported languages: {', '.join(supported)}"
        }

    # Validate project root exists
    if not os.path.isdir(project_root):
        return {
            "success": False,
            "error": f"Project root directory does not exist: {project_root}"
        }

    # Initialize config and logger
    config = MultilspyConfig.from_dict({
        "code_language": language.lower(),
        "trace_lsp_communication": debug,
        "start_independent_lsp_process": True
    })
    
    logger = MultilspyLogger()
    
    try:
        # Create language server
        lsp = LanguageServer.create(config, logger, project_root)
        
        # Start the server
        server_task = asyncio.create_task(start_lsp_server(lsp))
        
        # Store the session
        lsp_sessions[session_id] = LspSession(
            language_server=lsp,
            project_root=project_root,
            language=lang
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "language": language,
            "project_root": project_root
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to initialize language server: {str(e)}"
        }


async def start_lsp_server(lsp: LanguageServer) -> None:
    """Start the language server in a context manager."""
    async with lsp.start_server():
        # Keep server alive until it's closed elsewhere
        while True:
            await asyncio.sleep(1)


@mcp.tool()
async def shutdown_language_server(session_id: str) -> dict[str, Any]:
    """
    Shutdown a language server session.
    
    Parameters:
        session_id: The session ID returned from initialize_language_server
    
    Returns:
        Dictionary indicating success or failure
    """
    if session_id not in lsp_sessions:
        return {
            "success": False,
            "error": f"Session not found: {session_id}"
        }
    
    try:
        # Just remove from the sessions dict, the context manager will handle cleanup
        del lsp_sessions[session_id]
        return {
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to shutdown language server: {str(e)}"
        }


@mcp.tool()
async def request_definition(
    session_id: str,
    file_path: str,
    line: int,
    column: int
) -> dict[str, Any]:
    """
    Find the definition of a symbol at the specified location.
    
    Parameters:
        session_id: The session ID returned from initialize_language_server
        file_path: Path to the file containing the symbol, relative to project root
        line: Line number (0-indexed)
        column: Column number (0-indexed)
    
    Returns:
        Definition information for the symbol
    """
    if session_id not in lsp_sessions:
        return {
            "success": False,
            "error": f"Session not found: {session_id}"
        }
    
    session = lsp_sessions[session_id]
    lsp = session.language_server
    
    try:
        async with lsp.start_server():
            with lsp.open_file(file_path):
                result = await lsp.request_definition(file_path, line, column)
                
                if not result:
                    return {
                        "success": True,
                        "found": False,
                        "definitions": []
                    }
                
                # Convert definitions to a more usable format
                definitions = []
                for definition in result:
                    # Get relative path from project root
                    full_path = definition.uri.replace("file://", "")
                    rel_path = os.path.relpath(full_path, session.project_root)
                    
                    definitions.append({
                        "file": rel_path,
                        "start": {
                            "line": definition.range.start.line,
                            "character": definition.range.start.character
                        },
                        "end": {
                            "line": definition.range.end.line,
                            "character": definition.range.end.character
                        }
                    })
                
                return {
                    "success": True,
                    "found": True,
                    "definitions": definitions
                }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get definition: {str(e)}"
        }


@mcp.tool()
async def request_references(
    session_id: str,
    file_path: str,
    line: int,
    column: int
) -> dict[str, Any]:
    """
    Find all references of a symbol at the specified location.
    
    Parameters:
        session_id: The session ID returned from initialize_language_server
        file_path: Path to the file containing the symbol, relative to project root
        line: Line number (0-indexed)
        column: Column number (0-indexed)
    
    Returns:
        References information for the symbol
    """
    if session_id not in lsp_sessions:
        return {
            "success": False,
            "error": f"Session not found: {session_id}"
        }
    
    session = lsp_sessions[session_id]
    lsp = session.language_server
    
    try:
        async with lsp.start_server():
            with lsp.open_file(file_path):
                result = await lsp.request_references(file_path, line, column)
                
                if not result:
                    return {
                        "success": True,
                        "found": False,
                        "references": []
                    }
                
                # Convert references to a more usable format
                references = []
                for reference in result:
                    # Get relative path from project root
                    full_path = reference.uri.replace("file://", "")
                    rel_path = os.path.relpath(full_path, session.project_root)
                    
                    references.append({
                        "file": rel_path,
                        "start": {
                            "line": reference.range.start.line,
                            "character": reference.range.start.character
                        },
                        "end": {
                            "line": reference.range.end.line,
                            "character": reference.range.end.character
                        }
                    })
                
                return {
                    "success": True,
                    "found": True,
                    "references": references
                }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get references: {str(e)}"
        }


@mcp.tool()
async def request_completions(
    session_id: str,
    file_path: str,
    line: int,
    column: int
) -> dict[str, Any]:
    """
    Get completion suggestions for a location in the code.
    
    Parameters:
        session_id: The session ID returned from initialize_language_server
        file_path: Path to the file containing the location, relative to project root
        line: Line number (0-indexed)
        column: Column number (0-indexed)
    
    Returns:
        Completion suggestions for the location
    """
    if session_id not in lsp_sessions:
        return {
            "success": False,
            "error": f"Session not found: {session_id}"
        }
    
    session = lsp_sessions[session_id]
    lsp = session.language_server
    
    try:
        async with lsp.start_server():
            with lsp.open_file(file_path):
                result = await lsp.request_completions(file_path, line, column)
                
                if not result or not result.items:
                    return {
                        "success": True,
                        "found": False,
                        "completions": []
                    }
                
                # Convert completions to a more usable format
                completions = []
                for item in result.items:
                    completion = {
                        "label": item.label,
                        "kind": item.kind,
                        "detail": item.detail or "",
                    }
                    if item.documentation:
                        completion["documentation"] = item.documentation
                    completions.append(completion)
                
                return {
                    "success": True,
                    "found": True,
                    "completions": completions
                }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get completions: {str(e)}"
        }


@mcp.tool()
async def request_hover(
    session_id: str,
    file_path: str,
    line: int,
    column: int
) -> dict[str, Any]:
    """
    Get hover information for a symbol at the specified location.
    
    Parameters:
        session_id: The session ID returned from initialize_language_server
        file_path: Path to the file containing the symbol, relative to project root
        line: Line number (0-indexed)
        column: Column number (0-indexed)
    
    Returns:
        Hover information for the symbol
    """
    if session_id not in lsp_sessions:
        return {
            "success": False,
            "error": f"Session not found: {session_id}"
        }
    
    session = lsp_sessions[session_id]
    lsp = session.language_server
    
    try:
        async with lsp.start_server():
            with lsp.open_file(file_path):
                result = await lsp.request_hover(file_path, line, column)
                
                if not result or not result.contents:
                    return {
                        "success": True,
                        "found": False,
                        "hover": None
                    }
                
                # Extract hover content
                content = ""
                if isinstance(result.contents, str):
                    content = result.contents
                elif hasattr(result.contents, "value"):
                    content = result.contents.value
                
                return {
                    "success": True,
                    "found": True,
                    "hover": {
                        "content": content
                    }
                }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get hover information: {str(e)}"
        }


@mcp.tool()
async def request_document_symbols(
    session_id: str,
    file_path: str
) -> dict[str, Any]:
    """
    Get all symbols defined in a document.
    
    Parameters:
        session_id: The session ID returned from initialize_language_server
        file_path: Path to the file to analyze, relative to project root
    
    Returns:
        Symbols defined in the document
    """
    if session_id not in lsp_sessions:
        return {
            "success": False,
            "error": f"Session not found: {session_id}"
        }
    
    session = lsp_sessions[session_id]
    lsp = session.language_server
    
    try:
        async with lsp.start_server():
            with lsp.open_file(file_path):
                result = await lsp.request_document_symbols(file_path)
                
                if not result:
                    return {
                        "success": True,
                        "found": False,
                        "symbols": []
                    }
                
                # Convert symbols to a more usable format
                symbols = []
                for symbol in result:
                    symbols.append({
                        "name": symbol.name,
                        "kind": symbol.kind,
                        "start": {
                            "line": symbol.range.start.line,
                            "character": symbol.range.start.character
                        },
                        "end": {
                            "line": symbol.range.end.line,
                            "character": symbol.range.end.character
                        }
                    })
                
                return {
                    "success": True,
                    "found": True,
                    "symbols": symbols
                }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get document symbols: {str(e)}"
        }


@mcp.resource("multilspy://languages")
def get_supported_languages() -> dict[str, Any]:
    """
    Get a list of programming languages supported by the multilspy server.
    
    Returns:
        Dictionary of supported languages and their descriptions
    """
    languages = {
        "java": "Java support using Eclipse JDTLS",
        "python": "Python support using jedi-language-server",
        "rust": "Rust support using Rust Analyzer",
        "csharp": "C# support using OmniSharp/RazorSharp",
        "typescript": "TypeScript support using TypeScriptLanguageServer",
        "javascript": "JavaScript support using TypeScriptLanguageServer",
        "go": "Go support using gopls",
        "dart": "Dart support using Dart Language Server",
        "ruby": "Ruby support using Solargraph"
    }
    
    return {
        "supported_languages": languages
    }


@mcp.prompt()
def get_started() -> str:
    """
    Returns a prompt to help users get started with the multilspy MCP server.
    """
    return """
# MultilspyLSP MCP Server

This server provides Language Server Protocol (LSP) functionality via multilspy.

## Getting Started

First, initialize a language server session:

```python
# Initialize a Python language server session
result = await initialize_language_server(
    session_id="my-session-1", 
    project_root="/path/to/your/project",
    language="python"
)
```

Then, use the session to get language intelligence:

```python
# Find where a symbol is defined
definitions = await request_definition(
    session_id="my-session-1",
    file_path="src/main.py",
    line=10,  # 0-indexed
    column=15  # 0-indexed
)

# Get code completion suggestions
completions = await request_completions(
    session_id="my-session-1",
    file_path="src/main.py",
    line=10,
    column=15
)
```

Remember to shut down the session when done:

```python
await shutdown_language_server(session_id="my-session-1")
```

## Supported Languages

- Java (Eclipse JDTLS)
- Python (jedi-language-server)
- Rust (Rust Analyzer)
- C# (OmniSharp/RazorSharp)
- TypeScript (TypeScriptLanguageServer)
- JavaScript (TypeScriptLanguageServer)
- Go (gopls)
- Dart (Dart Language Server)
- Ruby (Solargraph)
"""


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()