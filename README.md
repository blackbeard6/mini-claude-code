# Mini Claude Code

A simple coding agent written for the purpose of giving developers a glimpse into how coding agents work under the hood. `/one-file-claude/agent.py` is a coding agent that's only ~300 lines of code, but can still be used to build pretty cool things -- check out `/example-code-products`. In `/refactored-mini-claude` there is a multi-module version, written by `/one-file-claude/agent.py` and me 😁.

## Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Usage

```bash
cd one-file-claude
python agent.py
```
or
```bash
cd refactored-mini-claude
python agent.py
```
#### Demo-mode
Toggle `DEMO_MODE` to `True` in `refactored-mini-claude/config.py` to see the prompt being sent to Claude at every iteration of the ReAct loop.

### Available Commands
- Type your requests naturally (e.g., "read the config.py file")
- `clear` - Reset conversation history
- `quit` - Exit the agent

## Example Interactions

```
> List all Python files in this directory
> Read the agent.py file
> Create a simple Snake game I can open in my browser with arrow key controls and score tracking
> Create a personal website
> Read the agent.py file and create a refactored, multi-module, extensible, and readable version in a new directory
```

## How It Works

The agent implements the ReAct pattern:

0. **Prompt**: the Python code combines the system prompt, the tool descriptions, and the user's prompt into one prompt to input to the Claude model
1. **Reason**: Claude tries to answer, and if it can't answer via text output, it might decide it needs to use a tool to take an action or gather more context.
2. **Act**: Claude outputs a tool-use request, which is converted into a Python function call by mapping the String tool-name to a function (read_file, write_file, list_files).
3. **Observe**:  The tool output is put into a prompt that also contains the system prompt, the tool descriptions, and the conversation history, and this is sent to Claude again.
4. **Repeat**: Until the task is complete

## Tools Available

- `read_file(path)` - Read file contents
- `write_file(path, content)` - Create or overwrite a file
- `list_files(path)` - List directory contents

## Development

#### Ideas for extending
- [ ] Implement a `CLAUDE.md`-like system
- [ ] Implement slash commands
- [ ] Implement a toy MCP
- [ ] Implement permissions
- [ ] Implement a to-do list feature
- [ ] Implement more tools -- e.g., targeted insertions, bash commands
