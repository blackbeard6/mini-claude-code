"""Configuration for the Baby Code agent."""

import logging

# Model configuration
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096

# Logging configuration
LOGGING_LEVEL = logging.ERROR
PFORMAT_WIDTH = 200

# Demo mode - shows all context before each API call
DEMO_MODE = True

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
