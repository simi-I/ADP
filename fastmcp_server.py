from fastmcp import FastMCP, Client

# Initialize the FastMCP server.
mcp_server = FastMCP()

# The `@mcp_server.tool` decorators registers this python function as an MCP tool
@mcp_server.tool
def greet(name: str) -> str:
    """
    Generates a personalizzed greeting.
    
    Args:
        name: The name of the person to greet.
    Returns:
        A greeting String.
    """
    return f"Hello, {name}! Nice to meet you."

if __name__ == "__main__":
    mcp_server.run(
    transport="http",
    host="127.0.0.1",
    port=8001
)
    