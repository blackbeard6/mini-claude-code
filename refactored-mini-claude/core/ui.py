"""UI components for the agent using Rich library."""

from rich.console import Console
from rich.markdown import Markdown
from pprint import pformat
from typing import List, Dict, Any
import config


# Global console instance
console = Console()


def show_welcome_message() -> None:
    """Display welcome message and instructions."""
    console.print("\n[bold]Baby Code Phase 1: Minimum Viable Coding Agent (Refactored)[/bold]")
    console.print("[dim]Commands: 'quit' to exit, 'clear' to reset conversation[/dim]\n")


def show_goodbye_message() -> None:
    """Display goodbye message."""
    console.print("\n[dim]Goodbye![/dim]\n")


def show_clear_message() -> None:
    """Display conversation cleared message."""
    console.print("[dim]Conversation cleared.[/dim]\n")


def get_user_input() -> str:
    """
    Get user input with styled prompt.

    Returns:
        User input string (stripped)
    """
    console.print("[bold]>[/bold] ", end="")
    return input().strip()


def show_agent_separator() -> None:
    """Display separator before agent response."""
    console.rule("[bold green]Agent", style="green")


def render_agent_response(text: str) -> None:
    """
    Render agent response as markdown.

    Args:
        text: Response text to render
    """
    if text:
        console.print(Markdown(text))


def show_demo_context(
    system_prompt: str,
    tools: List[Dict[str, Any]],
    conversation_history: List[Dict[str, Any]]
) -> None:
    """
    Display all context that will be sent to Claude in demo mode.
    Pauses execution until the user presses Enter.

    Args:
        system_prompt: The system prompt
        tools: List of tool schemas
        conversation_history: Current conversation
    """
    console.print()
    console.rule("[bold yellow]DEMO MODE: Context being sent to Claude[/bold yellow]", style="yellow")

    # System prompt
    console.print("\n[bold cyan]📋 SYSTEM PROMPT:[/bold cyan]")
    console.print(f"[dim]{system_prompt}[/dim]\n")

    # Tools
    console.print("[bold cyan]🛠️  AVAILABLE TOOLS:[/bold cyan]")
    tools_formatted = pformat(tools, width=config.PFORMAT_WIDTH)
    console.print(f"[dim]{tools_formatted}[/dim]\n")

    # Conversation history
    console.print("[bold cyan]💬 CONVERSATION HISTORY:[/bold cyan]")
    history_formatted = pformat(conversation_history, width=config.PFORMAT_WIDTH)
    console.print(f"[dim]{history_formatted}[/dim]\n")

    console.rule(style="yellow")
    console.print("[yellow]Press Enter to send this context to Claude...[/yellow] ", end="")
    input()
    console.print()
