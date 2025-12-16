#!/usr/bin/env python3
"""
Phase 1: Minimum Viable Coding Agent

A simple coding agent in ~300 lines that can:
- Read files
- Write files
- List directory contents
- Reason through tasks using the ReAct pattern

Usage:
    export ANTHROPIC_API_KEY="your-key"
    python agent.py
"""

import logging
from pathlib import Path
from anthropic import Anthropic
from rich.console import Console
from rich.markdown import Markdown

# Configure logging
loggingLevel = logging.INFO
DEMO_MODE = True  # Set to True to show all context before each API call

logging.basicConfig(
    level=loggingLevel,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the Anthropic client
client = Anthropic()

# Initialize Rich console for markdown rendering
console = Console()

# System prompt that defines the agent's behavior
SYSTEM_PROMPT = """You are a helpful coding assistant that can read, write, and manage files.

You have access to the following tools:
- read_file: Read the contents of a file
- write_file: Write content to a file (creates or overwrites)
- list_files: List files in a directory

When given a task:
1. Think about what you need to do
2. Use tools to gather information or make changes
3. Continue until the task is complete
4. Explain what you did

Always be careful when writing files - make sure you understand the existing content first."""

# Define the tools the agent can use
# This goes into the prompt to the model to let the model know how to call different Python functions
# Very similar to MCP
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file at the given path. Returns the file content as a string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to read"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file at the given path. Creates the file if it doesn't exist, or overwrites if it does.",
        "input_schema": {
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
        }
    },
    {
        "name": "list_files",
        "description": "List all files and directories in the given directory path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list (defaults to current directory)",
                    "default": "."
                }
            },
            "required": []
        }
    }
]


# For sake of the demo, I think it makes more sense to write these functions first -- define tools in code first since that's most
# familiar. The tool list above is an API that converts natural language to a code call, and explains to the AI agent how to use
# it
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


# Key piece -- Claude operates in natural language. This converts the natural language into a function call.
def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool and return its result."""
    try:
        if tool_name == "read_file":
            return read_file(tool_input["path"])
        elif tool_name == "write_file":
            return write_file(tool_input["path"], tool_input["content"])
        elif tool_name == "list_files":
            return list_files(tool_input.get("path", "."))
        else:
            return f"Error: Unknown tool: {tool_name}"
    except Exception as e:
        return f"Error executing {tool_name}: {e}"


def run_agent(user_message: str, conversation_history: list = None) -> None:
    """
    Run the agent with a user message.

    This implements the ReAct (Reason, Act, Observe) loop:
    1. Send message to Claude
    2. If Claude wants to use a tool, execute it and continue
    3. Repeat until Claude gives a final response
    """
    if conversation_history is None:
        conversation_history = []

    # Add the user's message to the conversation
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # ReAct loop - keep going until the model stops using tools
    while True:
        # Get response from Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=conversation_history
        )

        # Render any text content as markdown
        text_content = [block.text for block in response.content if hasattr(block, 'text')]
        if text_content:
            console.print(Markdown(''.join(text_content)))

        # Add assistant's response to conversation history
        conversation_history.append({
            "role": "assistant",
            "content": response.content
        })

        # Check if there are any tool uses
        tool_uses = [block for block in response.content if block.type == "tool_use"]

        if tool_uses:
            tool_results = []
            for block in tool_uses:
                result = execute_tool(block.name, block.input)
                logger.info("Executed tool: \"%s\", results:\n%s", block.name, result)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

            # Add tool results to the conversation
            conversation_history.append({
                "role": "user",
                "content": tool_results
            })
            # Continue loop to get Claude's next response
            logger.info("Running the model with tool outputs")

        else:
            # No tool uses - we're done
            logger.info("ReAct loop complete, prompting user")
            return


def main():
    """Main chat loop."""
    console.print("\n[bold]Baby Code Phase 1: Minimum Viable Coding Agent[/bold]")
    console.print("[dim]Commands: 'quit' to exit, 'clear' to reset conversation[/dim]\n")

    conversation_history = []

    while True:
        try:
            # Get user input
            console.print("[bold]>[/bold] ", end="")
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            console.print("\n[dim]Goodbye![/dim]\n")
            break

        if user_input.lower() == 'clear':
            conversation_history = []
            console.print("[dim]Conversation cleared.[/dim]\n")
            continue

        # Visual separator before agent response
        console.rule("[bold green]Agent", style="green")
        run_agent(user_input, conversation_history)
        print()  # Add spacing after response


if __name__ == "__main__":
    main()
