import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import os
import google.generativeai as genai
from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel('gemini-1.5-flash')


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
            response = await self.session.list_tools()

            gemini_tools = [
                {"name": tool.name, "description": tool.description, "parameters": tool.inputSchema}
                for tool in response.tools
            ]

            chat = self.model.start_chat(enable_automatic_function_calling=True)
            response = chat.send_message(query, tools=gemini_tools)

            for content in response:
                for part in content.parts:
                    if "function_call" in part:
                        function_call = part.function_call
                        tool_name = function_call.name
                        tool_args = {key: value for key, value in function_call.args.items()}

                        tool_response = await self.session.call_tool(tool_name, tool_args)

                        chat.send_message(
                            genai.Part(
                                function_response = genai.protos.FunctionResponse(
                                    name=tool_name,
                                    response=tool_response.model_dump()
                                )
                            )
                        )

            return response.text

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
    # The user needs to provide their Gemini API key in a .env file
    # with the key GEMINI_API_KEY.
    if os.getenv("GEMINI_API_KEY") is None:
        print("Please set the GEMINI_API_KEY environment variable in a .env file.")
    else:
        asyncio.run(main())
