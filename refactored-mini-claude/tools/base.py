"""Base classes for tool implementations."""

from typing import Callable, Dict, Any


class Tool:
    """Base class for agent tools."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        function: Callable
    ):
        """
        Initialize a tool.

        Args:
            name: Tool name (used by Claude to call it)
            description: What the tool does
            input_schema: JSON schema describing the tool's parameters
            function: Python function to execute
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.function = function

    def to_anthropic_format(self) -> Dict[str, Any]:
        """Convert tool to Anthropic API format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema
        }

    def execute(self, **kwargs) -> str:
        """Execute the tool with given parameters."""
        try:
            return self.function(**kwargs)
        except Exception as e:
            return f"Error executing {self.name}: {e}"
