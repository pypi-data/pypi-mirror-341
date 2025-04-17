# ud83eudd16u2728 Creating Custom Profiles in Aki

> **Design your perfect AI assistant with exactly the capabilities you need!**

Aki empowers you to create specialized AI agents tailored to your unique needs using simple JSON configuration. This guide will walk you through creating customized Aki agents that excel at specific tasks.

---

## ud83dude80 Quick Start Guide

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83dudcdd Step 1: Create a Profile JSON File
Create a file at `~/.aki/profiles/my_agent.json` with your custom configuration:

```json
{
  "name": "DevOpsHelper",
  "description": "Infrastructure and deployment specialist",
  "system_prompt": "You are an expert in cloud infrastructure, CI/CD pipelines, and DevOps practices...",
  "tools": [
    "file_management_readonly",
    "code_analyzer",
    "shell_command",
    "web_search"
  ],
  "default_model": "(bedrock)us.anthropic.claude-3-7-sonnet-20250219-v1:0",
  "reasoning_config": {
    "default_enabled": true,
    "budget_tokens": 4096
  },
  "starters": [
    {
      "label": "Analyze Infrastructure",
      "message": "Help me analyze my cloud infrastructure setup"
    }
  ]
}
```

### ud83dude80 Step 2: Launch and Select
Start Aki and select your custom agent from the profile dropdown!
</div>

---

## ud83dudcd0 Profile Configuration Reference

### ud83dudcc1 File Location

Place your profile files in the recommended location:
- `~/.aki/profiles/` (recommended for user profiles)

### ud83dudccb Complete Profile Schema

```json
{
  "name": "Display Name",                        // The name shown in the UI
  "description": "What the agent does",          // Short description of capabilities
  "default": false,                             // Whether this is the default profile
  "order_id": 15,                              // UI position (smaller numbers first)
  
  // System prompt options (choose one):
  "system_prompt": "Inline system prompt...",    // Direct prompt text
  // OR
  "system_prompt_file": "prompts/agent.txt",    // File containing the prompt
  
  // Optional rules file for operational guidelines:
  "rules_file": "prompts/agent_rule.txt",
  
  // Tool configuration:
  "tools": ["tool1", "tool2"],                 // List of enabled tools
  "enabled_mcp_servers": "__ALL__",            // or ["server1", "server2"]
  
  // Model settings:
  "default_model": "(bedrock)us.anthropic.claude-3-7-sonnet-20250219-v1:0",
  
  // Reasoning configuration:
  "reasoning_config": {
    "default_enabled": true,                    // Enable extended reasoning
    "budget_tokens": 4096                       // Token budget for reasoning
  },
  
  // Quick-start buttons:
  "starters": [
    {
      "label": "Button Label",                  // Text shown on button
      "message": "What to send when clicked",   // Message sent when clicked
      "icon": "Optional icon URL"               // Optional button icon
    }
  ]
}
```

---

## ud83dudee0ufe0f Available Tools

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83dudcda Tool Collections
- `file_management_full`: Complete file operations (read/write/delete)
- `file_management_readonly`: Safe read-only file operations
</div>

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83euddf0 Individual Core Tools
- `shell_command`: Execute shell commands
- `render_html`: Display rich HTML content
- `code_analyzer`: Analyze code structure and patterns
- `python_executor`: Execute Python code snippets
- `web_search`: Search the web for information
- `tasklist`: Create and manage structured task lists
- `get_datetime_now`: Get current date and time
- `process_manager`: Run and monitor long-running processes
- `batch_tool`: Execute multiple tools simultaneously
- `think`: Enable structured reasoning for complex tasks
</div>

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83eudd16 MCP Extension Tools
Custom MCP servers can provide specialized tools. See the [MCP Guide](https://github.com/Aki-community/aki/blob/main/docs/mcp_guide.md) for details on available servers and their tools.
</div>

---

## ud83dude80 AI Model Configuration

### ud83eudde0 Available Models

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

Specify your preferred model using the `default_model` field:

```json
{
  "default_model": "(bedrock)us.anthropic.claude-3-7-sonnet-20250219-v1:0"
}
```

#### Recommended Models:
- `(bedrock)us.anthropic.claude-3-7-sonnet-20250219-v1:0` - Claude 3.7 Sonnet (cutting-edge reasoning)
- `(bedrock)us.anthropic.claude-3-5-sonnet-20241022-v2:0` - Claude 3.5 Sonnet (balanced performance)
- `(bedrock)us.anthropic.claude-3-5-haiku-20241022-v1:0` - Claude 3.5 Haiku (faster responses)
</div>

### ud83eudde9 Advanced Reasoning Configuration

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

Unlock more powerful reasoning capabilities:

```json
{
  "reasoning_config": {
    "default_enabled": true,  // Enable extended reasoning by default
    "budget_tokens": 4096     // Maximum tokens for reasoning steps
  }
}
```

This allows the AI to perform more thorough analysis and problem-solving when tackling complex tasks.
</div>

---

## ud83dudcd6 System Prompts and Rules

### ud83dudcac System Prompts

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

#### 1. Inline Prompt
Defined directly in your profile JSON:
```json
{
  "system_prompt": "You are an expert in cloud architecture specializing in AWS services..."
}
```

#### 2. File Reference
Loaded from an external file for more complex prompts:
```json
{
  "system_prompt_file": "prompts/my_agent.txt"
}
```
</div>

### ud83dudccb Rules Files

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

Rules files provide detailed operational guidelines that dictate how the agent should behave:

```json
{
  "rules_file": "prompts/my_agent_rule.txt"
}
```

A rules file uses the `<rule>...</rule>` format and contains specific instructions:

```text
<rule>
1. Task Management:
   - Always use batch_tool for efficiency
   - Keep users informed with task status updates
   - Break down complex problems into manageable tasks

2. Tool Usage:
   - Use specific patterns for tool operations
   - Implement safety checks before file modifications

3. Response Formatting:
   - Follow specific citation formats
   - Structure answers consistently
</rule>
```
</div>

### ud83duddbcufe0f Prompt Structure

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

Organize your system prompts using these sections:

```text
<role_definition>
Define the agent's primary role and expertise
</role_definition>

<capabilities>
List specific capabilities and skills
</capabilities>

<instructions>
Provide detailed instructions for:
1. Task handling approach
2. Tool usage guidelines
3. Response formatting
</instructions>
```
</div>

---

## ud83dudcbb Example Profiles

### ud83dudcd6 Example 1: Documentation Assistant

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

```json
{
  "name": "Doc Assistant",
  "description": "Documentation specialist with advanced search",
  "order_id": 5,
  "system_prompt": "You are an expert in technical documentation and knowledge management...",
  "rules_file": "prompts/doc_assistant_rule.txt",
  "tools": [
    "file_management_readonly",
    "web_search",
    "batch_tool",
    "tasklist",
    "think"
  ],
  "default_model": "(bedrock)us.anthropic.claude-3-7-sonnet-20250219-v1:0",
  "reasoning_config": {
    "default_enabled": true,
    "budget_tokens": 4096
  },
  "starters": [
    {
      "label": "Find Documentation",
      "message": "I need help finding documentation about..."
    },
    {
      "label": "Search Patterns",
      "message": "Can you find code patterns for..."
    }
  ]
}
```
</div>

### ud83dudc68u200dud83dudcbb Example 2: Development Helper

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

```json
{
  "name": "Dev Helper",
  "description": "Complete coding assistant with server management",
  "order_id": 15,
  "system_prompt_file": "prompts/dev_helper.txt",
  "tools": [
    "code_analyzer",
    "python_executor",
    "file_management_readonly",
    "process_manager",
    "batch_tool",
    "think"
  ],
  "enabled_mcp_servers": "__ALL__",
  "default_model": "(bedrock)us.anthropic.claude-3-5-sonnet-20241022-v2:0",
  "starters": [
    {
      "label": "Analyze Code",
      "message": "Analyze this codebase and identify improvements..."
    },
    {
      "label": "Start Server",
      "message": "Run a development server for this project..."
    },
    {
      "label": "Generate Tests",
      "message": "Create unit tests for this module..."
    }
  ]
}
```
</div>

---

## ud83dudd30 Profile Ordering and Selection

### ud83dudccb Profile Order Control

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

Control how your profile appears in the UI selection list:

```json
{
  "name": "My Custom Agent",
  "description": "My specialized AI assistant",
  "order_id": 5,  // Appears before Aki in the list
  // other configuration...
}
```

#### Profile Order Rules

1. **Lower numbers appear first** in the selection list
2. Built-in profiles have these default order values:
   - Aki: 10
   - Akira: 20
   - Akisa: 30
   - Aki Team: 40
   - Custom profiles without `order_id`: 100
3. You can use **negative numbers** or **decimal values** (like 9.5) for precise positioning
</div>

### ud83dudd1d Default Profile Settings

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

The `default` and `order_id` fields serve different purposes:

- `"default": true` - Determines which profile is automatically selected when Aki starts
- `"order_id": value` - Controls where the profile appears in the selection list

To make a profile both default AND first in the list:
```json
{
  "name": "My Default Profile",
  "default": true,
  "order_id": 1,  
  // other settings...
}
```
</div>

---

## u2714ufe0f Best Practices

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83dudd10 Tool Selection Best Practices
- Start with `file_management_readonly` for safety
- Only enable tools your agent actually needs
- Use `enabled_mcp_servers` to control external tool access
- Include `think` and `batch_tool` for complex reasoning tasks
</div>

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83dudcac System Prompt Best Practices
- Be specific about the agent's role, expertise, and limitations
- Use rules files for detailed operational guidelines
- Define clear task management patterns and tool usage protocols
- Include specific formatting requirements and examples
</div>

<div style="background-color: #fff8f0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83eudde0 Model Selection Best Practices
- Use Claude 3.7 for complex reasoning and specialized expertise
- Choose Claude 3.5 Sonnet for balanced performance
- Select Claude 3.5 Haiku for faster responses on simpler tasks
- Configure reasonable token budgets (2048-8192) based on complexity
</div>

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83dudd79ufe0f Starter Button Best Practices
- Create task-specific starter buttons
- Use clear, action-oriented button labels
- Design starter messages that provide initial context
- Group related functionality with multiple starters
</div>

---

## u2757 Important Notes

<div style="background-color: #fff8f0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

1. Profile names must be unique across all profiles
2. Invalid tool names are silently ignored
3. System prompts should align with the tools you've enabled
4. Built-in profiles cannot be overridden or modified
5. Profile changes require an Aki restart to take effect
6. File paths in your profiles are relative to the profiles directory
</div>

---

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### ud83dude80 Ready for Advanced Customization?
For advanced multi-agent profiles using Python, check out the [Development Guide](https://github.com/Aki-community/aki/blob/main/docs/development_guide.md).
</div>