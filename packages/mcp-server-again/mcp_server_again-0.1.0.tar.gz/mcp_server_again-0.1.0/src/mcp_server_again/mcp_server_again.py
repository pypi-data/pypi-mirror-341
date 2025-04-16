from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo2")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b
