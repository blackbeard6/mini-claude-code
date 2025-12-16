#!/usr/bin/env python3
"""
Phase 1: Minimum Viable Coding Agent (Refactored)

A modular coding agent that demonstrates clean architecture:
- Separate configuration, tools, UI, and core logic
- Easy to extend with new tools
- Clean separation of concerns

Usage:
    export ANTHROPIC_API_KEY="your-key"
    python agent.py
"""

import logging
from tools.registry import ToolRegistry
from tools.file_tools import get_file_tools
from core.agent import Agent
from core.ui import (
    show_welcome_message,
    show_goodbye_message,
    show_clear_message,
    get_user_input,
    show_agent_separator
)
import config


def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=config.LOGGING_LEVEL,
        format='[%(levelname)s] %(message)s'
    )


def create_agent() -> Agent:
    """
    Create and configure the agent with tools.

    Returns:
        Configured Agent instance
    """
    # Create tool registry
    registry = ToolRegistry()

    # Register file tools
    for tool in get_file_tools():
        registry.register(tool)

    # Future: Add more tools here
    # for tool in get_bash_tools():
    #     registry.register(tool)

    # Create agent with registered tools
    agent = Agent(registry)

    return agent


def main():
    """Main chat loop."""
    setup_logging()
    show_welcome_message()

    agent = create_agent()

    while True:
        try:
            user_input = get_user_input()
        except (EOFError, KeyboardInterrupt):
            show_goodbye_message()
            break

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            show_goodbye_message()
            break

        if user_input.lower() == 'clear':
            agent.clear_history()
            show_clear_message()
            continue

        # Visual separator before agent response
        show_agent_separator()
        agent.run(user_input)
        print()  # Add spacing after response


if __name__ == "__main__":
    main()
