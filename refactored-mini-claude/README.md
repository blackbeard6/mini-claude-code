# Phase 1: Refactored Coding Agent

A clean, modular refactor of the minimum viable coding agent demonstrating proper software architecture.

## Directory Structure

```
phase1-refactored/
├── agent.py              # Main entry point - CLI interface
├── config.py             # All configuration and constants
├── core/
│   ├── agent.py          # ReAct loop and core agent logic
│   └── ui.py             # Rich console UI components
└── tools/
    ├── base.py           # Base Tool class
    ├── registry.py       # Tool registry system
    └── file_tools.py     # File operation tools
```

## Architecture Benefits

### 1. **Separation of Concerns**
- **config.py**: Single source of truth for all settings
- **core/agent.py**: Pure business logic, UI-agnostic
- **core/ui.py**: All Rich console code isolated
- **tools/**: Modular tool system

### 2. **Easy to Extend**

#### Add a new tool:
```python
# In tools/bash_tools.py
from .base import Tool

def execute_bash(command: str) -> str:
    # Implementation...
    pass

bash_tool = Tool(
    name="bash",
    description="Execute bash commands",
    input_schema={...},
    function=execute_bash
)
```

```python
# In agent.py
from tools.bash_tools import bash_tool

registry.register(bash_tool)  # That's it!
```

#### Add .claude.md support:
```python
# In config.py
from pathlib import Path

def load_system_prompt():
    prompt = SYSTEM_PROMPT
    claude_md = Path('.claude.md')
    if claude_md.exists():
        prompt = claude_md.read_text() + '\n\n' + prompt
    return prompt

SYSTEM_PROMPT = load_system_prompt()
```

#### Add slash commands:
```python
# In core/ui.py
def get_user_input() -> str:
    user_input = input().strip()
    if user_input.startswith('/'):
        # Handle slash command
        return expand_slash_command(user_input)
    return user_input
```

### 3. **Testable**
Each component can be tested independently:
- Mock `ToolRegistry` for agent tests
- Test tools without running the agent
- Test UI rendering without API calls

## Usage

```bash
export ANTHROPIC_API_KEY="your-key"
python agent.py
```

## Next Steps for Demos

This architecture makes it easy to add:
- ✅ **Bash tool** - Execute shell commands
- ✅ **Slash commands** - `/review`, `/test`, etc.
- ✅ **.claude.md** - Custom instructions
- ✅ **Permissions** - Ask before dangerous operations
- ✅ **MCP servers** - Dynamic tool loading
- ✅ **Planning mode** - Separate planning/execution phases
