"""Core agent logic implementing the ReAct pattern."""

import logging
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
import config
from tools.registry import ToolRegistry
from core.ui import show_demo_context, render_agent_response


logger = logging.getLogger(__name__)


class Agent:
    """Coding agent that uses ReAct pattern with Claude."""

    def __init__(self, tool_registry: ToolRegistry):
        """
        Initialize the agent.

        Args:
            tool_registry: Registry of available tools
        """
        self.client = Anthropic()
        self.tool_registry = tool_registry
        self.conversation_history: List[Dict[str, Any]] = []

    def run(self, user_message: str) -> None:
        """
        Run the agent with a user message, streaming the response.

        This implements the ReAct (Reason, Act, Observe) loop:
        1. Send message to Claude (streaming)
        2. If Claude wants to use a tool, execute it and continue
        3. Repeat until Claude gives a final response

        Args:
            user_message: The user's message
        """
        # Add the user's message to the conversation
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # ReAct loop - keep going until the model stops using tools
        while True:
            # Demo mode: Show all context before making the API call
            if config.DEMO_MODE:
                show_demo_context(
                    config.SYSTEM_PROMPT,
                    self.tool_registry.get_tool_schemas(),
                    self.conversation_history
                )

            # Collect text for markdown rendering
            collected_text = []

            with self.client.messages.stream(
                model=config.MODEL,
                max_tokens=config.MAX_TOKENS,
                system=config.SYSTEM_PROMPT,
                tools=self.tool_registry.get_tool_schemas(),
                messages=self.conversation_history
            ) as stream:
                for event in stream:
                    if event.type == "content_block_delta":
                        if event.delta.type == "text_delta":
                            # Collect text chunks for markdown rendering
                            collected_text.append(event.delta.text)

                # Get the final message to extract complete tool uses
                final_message = stream.get_final_message()

            # Render collected text as markdown
            if collected_text:
                full_text = ''.join(collected_text)
                render_agent_response(full_text)

            # Use the content from the final message (has complete tool inputs)
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message.content
            })

            # Check if there are any tool uses
            tool_uses = [block for block in final_message.content if block.type == "tool_use"]

            if tool_uses:
                tool_results = []
                for block in tool_uses:
                    result = self.tool_registry.execute_tool(block.name, block.input)
                    logger.info("Executed tool: \"%s\", results:\n%s", block.name, result)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

                # Add tool results to the conversation
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                # Continue loop to get Claude's next response
                logger.info("Running the model with tool outputs")

            else:
                # No tool uses - we're done
                logger.info("ReAct loop complete, prompting user")
                return

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.

        Returns:
            Conversation history
        """
        return self.conversation_history
