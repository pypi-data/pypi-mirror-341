# 🔌 Model Context Protocol (MCP) Guide

> **Transform Aki into your perfect AI assistant by adding custom capabilities!**

This guide explains how MCP works in Aki and walks you through developing your own MCP servers to extend Aki's functionality with specialized tools and services.

---

## 📋 Overview

The Model Context Protocol (MCP) is an open standard that enables Aki to communicate with external tools and services via JSON-RPC. This powerful protocol allows you to enhance Aki's capabilities by connecting new servers that provide specialized functionality—from database access to external APIs and beyond.

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 💡 What Can MCP Do?
- Connect to specialized services and tools
- Add domain-specific capabilities to your agents
- Create custom workflows for your unique needs
- Integrate with external APIs and databases
- Build persistent memory and knowledge systems
</div>

---

## 🏗️ Key Components

### 📄 Server Configuration

MCP servers are configured in `~/.aki/mcp_settings.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npm",
      "args": ["--prefix", "${aki_home}/mcp_servers/my-server", "start"],
      "disabled": false,
      "env": {},
      "check_install_script": {
        "command": "npm",
        "args": ["list", "--prefix", "${aki_home}/mcp_servers/my-server"],
        "expected_output": "my-mcp-server@1.0.0"
      },
      "install_scripts": [
        {
          "command": "npm",
          "args": ["install"],
          "cwd": "${aki_home}/mcp_servers/my-server"
        }
      ]
    }
  }
}
```

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

#### Configuration Fields
- `command`: Command to start the server
- `args`: Command line arguments
- `disabled`: Whether the server is disabled
- `env`: Environment variables
- `check_install_script`: Script to verify installation
- `install_scripts`: Scripts to install the server
</div>

### 🚀 Server Lifecycle Management

Aki intelligently manages the entire MCP server lifecycle:

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

#### 1. Installation Check
- Runs `check_install_script` to verify installation
- Compares output with expected values
- Flags servers that need installation

#### 2. Installation Process
- Executes `install_scripts` in sequence for missing servers
- Sets up proper environment variables
- Validates successful installation

#### 3. Health Check
- Establishes test connections
- Validates tool availability and responses
- Maintains server state information
</div>

---

## 👨‍💻 Developing MCP Servers

### 📁 Project Structure

```
my-mcp-server/
├── src/
│   └── index.ts    # Server implementation
├── package.json    # Dependencies
└── tsconfig.json   # TypeScript config
```

### ⚙️ Server Implementation

Create a powerful TypeScript implementation:

```typescript
import { Server, ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk';

// Create server
const server = new Server('my-server', '1.0.0');

// Register tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'my_tool',
        description: 'What my tool does',
        inputSchema: {
          type: 'object',
          properties: {
            param1: { type: 'string' }
          }
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { tool, arguments: args } = request;
  
  // Tool implementation
  const result = await myToolLogic(args);
  
  return {
    content: [
      {
        type: 'text',
        text: result
      }
    ]
  };
});

// Start server
server.listen();
```

### 🔄 Tool Response Format

```typescript
{
  content: [
    {
      type: 'text',
      text: 'Result text'
    },
    {
      type: 'error',
      text: 'Error message'
    }
  ]
}
```

---

## 🧩 Using MCP Tools in Profiles

### 🔌 Enable MCP Servers

In your custom profile JSON:

```json
{
  "name": "My Agent",
  "description": "Uses MCP tools",
  "enabled_mcp_servers": ["my-server"],  // or "__ALL__"
  "tools": ["my_tool"]
}
```

### 🛠️ Access MCP Tools

Reference tools in your system prompts:

```text
<capabilities>
Use my_tool for specialized tasks:
- Parameter: param1 (string)
- Returns: text result
</capabilities>
```

---

## ✅ Best Practices

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 🏗️ Server Development
- Implement comprehensive error handling
- Provide detailed tool descriptions and schemas
- Follow the JSON-RPC 2.0 specification
- Include proper logging for troubleshooting
</div>

<div style="background-color: #f0fcf0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 🛠️ Tool Design
- Build focused, single-purpose tools
- Validate and sanitize all inputs thoroughly
- Return structured responses with clear formatting
- Handle errors gracefully with informative messages
</div>

<div style="background-color: #fff8f0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 🔒 Security Considerations
- Validate all inputs to prevent injection attacks
- Sanitize file paths to prevent directory traversal
- Implement rate limiting for resource-intensive operations
- Avoid exposing sensitive information in responses
</div>

---

## 🔍 Troubleshooting

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 🔧 Installation Issues
Check the server state:
```bash
cat ~/.aki/mcp_server_state.json
```

Try manual installation:
```bash
cd ~/.aki/mcp_servers/my-server
npm install
npm start
```
</div>

<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 📡 Communication Issues
Test the server directly:
```bash
echo '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}' | node dist/index.js
```
Check logs for connection errors and validate your JSON-RPC requests.
</div>

---

## 📚 Example Servers

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 🧠 Memory Server

**Capabilities:**
- Knowledge graph storage and retrieval
- Entity relationship tracking
- Cross-session persistent memory

Add this config to `~/.aki/mcp_settings.json`:
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```
</div>

### 🌐 Discover More MCP Servers

Explore the growing ecosystem of MCP servers: [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

---

<div style="background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;">

### 🚀 Ready to Build?

By creating custom MCP servers, you can extend Aki with capabilities perfectly tailored to your specific needs. From connecting to specialized databases to integrating with your organization's internal tools, MCP makes Aki infinitely extensible.

Start building today and transform your AI assistant into a powerful extension of your development workflow!
</div>