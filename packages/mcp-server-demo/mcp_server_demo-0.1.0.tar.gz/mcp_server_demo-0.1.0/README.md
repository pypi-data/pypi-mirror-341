# MCP Server Demo

A demonstration MCP server implementation with Docker container management capabilities.

## Installation

```bash
pip install -e .
```

## Usage

You can run the MCP server in two ways:

1. Using the installed entry point:
```bash
mcp-server-demo
```

2. Using Python directly:
```bash
python -m mcp_server_demo
```

## Features

- Basic arithmetic operations (add)
- Docker container management:
  - Run containers
  - Stop containers
  - Remove containers
  - Get container status
  - Start stopped containers
