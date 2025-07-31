# MyMCPs Server

This is a sample MCP(Model Context Protocol) server built using the FastMCP python library.

## Features

- A `greet` tool that takes a name and returns a greeting.
- A `get_time` resource that returns the current server time.

## Getting Started

### Prerequisites

- Python 3.7+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/example/mymcps.git
   cd mymcps
   ```

2. Install the dependencies:
   ```bash
   pip install -r my_mcp_server/requirements.txt
   ```

### Running the server

To run the server, execute the following command:
```bash
uvicorn my_mcp_server.main:app --host 0.0.0.0 --port 8000
```

The server will be running at `http://0.0.0.0:8000`.

## MCP Client Integration

To integrate this server with your MCP client, you need to add the following configuration to your client's config file.

### Example Tool Configuration

```json
{
  "tools": [
    {
      "name": "greet",
      "url": "http://0.0.0.0:8000/tools/greet",
      "doc": "This tool greets the given name."
    }
  ]
}
```

### Example Resource Configuration

```json
{
  "resources": [
    {
      "name": "get_time",
      "url": "http://0.0.0.0:8000/resources/get_time",
      "doc": "This resource returns the current time."
    }
  ]
}
```

This will allow your MCP client to discover and use the tools and resources provided by this server.