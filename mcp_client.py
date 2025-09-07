import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_url: str):
        """Connect to a remote MCP server."""
        try:
            # Use streamablehttp_client for remote servers
            http_transport = await self.exit_stack.enter_async_context(streamablehttp_client(server_url))
            self.read, self.write, _ = http_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.read, self.write))

            await self.session.initialize()

            response = await self.session.list_tools()
            tools = response.tools
            print(f"Connected to server with tools: {[tool.name for tool in tools]}")
            return f"Connected to server with tools: {[tool.name for tool in tools]}"
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return f"Failed to connect to server: {e}"


    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        if not self.session:
            return "Not connected to a server."

        try:
            messages = [{"role": "user", "content": query}]

            response = await self.session.list_tools()
            available_tools = [{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in response.tools]

            # Initial Claude API call
            response = self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=messages,
                tools=available_tools
            )

            final_text = []
            assistant_message_content = []

            for content in response.content:
                if content.type == 'text':
                    final_text.append(content.text)
                    assistant_message_content.append(content)
                elif content.type == 'tool_use':
                    tool_name = content.name
                    tool_args = content.input

                    # Execute tool call
                    result = await self.session.call_tool(tool_name, tool_args)
                    final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                    assistant_message_content.append(content)
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message_content
                    })
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result.content
                            }
                        ]
                    })

                    # Get next response from Claude
                    response = self.anthropic.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1000,
                        messages=messages,
                        tools=available_tools
                    )

                    for content in response.content:
                        if content.type == 'text':
                            final_text.append(content.text)


            return "\n".join(final_text)
        except Exception as e:
            return f"An error occurred: {e}"

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    """A simple main function for testing the client."""
    client = MCPClient()
    server_url = "http://127.0.0.1:8000/mcp" # placeholder
    await client.connect_to_server(server_url)

    if client.session:
        response = await client.process_query("What's the weather in London?")
        print(response)

    await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
