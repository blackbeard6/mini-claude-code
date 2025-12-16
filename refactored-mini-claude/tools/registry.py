"""Tool registry for managing available tools."""

from typing import Dict, List, Any
from .base import Tool


class ToolRegistry:
    """Registry for managing agent tools."""

    def __init__(self):
        """Initialize an empty tool registry."""
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """
        Register a tool.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        """
        Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance

        Raises:
            KeyError: If tool not found
        """
        return self._tools[name]

    def execute_tool(self, name: str, tool_input: Dict[str, Any]) -> str:
        """
        Execute a tool by name.

        Args:
            name: Tool name
            tool_input: Parameters for the tool

        Returns:
            Tool execution result
        """
        if name not in self._tools:
            return f"Error: Unknown tool: {name}"

        tool = self._tools[name]
        return tool.execute(**tool_input)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Get all tool schemas in Anthropic API format.

        Returns:
            List of tool schemas
        """
        return [tool.to_anthropic_format() for tool in self._tools.values()]

    def list_tools(self) -> List[str]:
        """
        Get list of registered tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())
