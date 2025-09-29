import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

FASTMCP_SERVERS_URL = "http://localhost:8001/mcp"

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name = 'fastmcp_greeter_agent',
    instruction='You are a friendly assistant that can greet people by their name. Use the "greet" tool',
    tools=[
        MCPToolset(
            connection_params = StreamableHTTPConnectionParams(
                url = FASTMCP_SERVERS_URL,
            ),
            tool_filter = ['greet']
        )
    ],
)