"""File operation tools for the agent."""

from pathlib import Path
from .base import Tool


# Tool implementation functions

def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    try:
        # Create parent directories if they don't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def list_files(path: str = ".") -> str:
    """List files and directories in the given path."""
    try:
        entries = []
        p = Path(path)
        for entry in sorted(p.iterdir()):
            if entry.is_dir():
                entries.append(f"[DIR]  {entry.name}/")
            else:
                entries.append(f"[FILE] {entry.name}")
        if not entries:
            return f"Directory is empty: {path}"
        return "\n".join(entries)
    except FileNotFoundError:
        return f"Error: Directory not found: {path}"
    except NotADirectoryError:
        return f"Error: Not a directory: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error listing directory: {e}"


# Tool definitions

read_file_tool = Tool(
    name="read_file",
    description="Read the contents of a file at the given path. Returns the file content as a string.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the file to read"
            }
        },
        "required": ["path"]
    },
    function=read_file
)

write_file_tool = Tool(
    name="write_file",
    description="Write content to a file at the given path. Creates the file if it doesn't exist, or overwrites if it does.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the file to write"
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file"
            }
        },
        "required": ["path", "content"]
    },
    function=write_file
)

list_files_tool = Tool(
    name="list_files",
    description="List all files and directories in the given directory path.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The directory path to list (defaults to current directory)",
                "default": "."
            }
        },
        "required": []
    },
    function=list_files
)


def get_file_tools() -> list[Tool]:
    """Get all file operation tools."""
    return [read_file_tool, write_file_tool, list_files_tool]
