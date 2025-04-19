from fastmcp import FastMCP
from mcp_x_server.agents.tweet_agent import agent

mcp = FastMCP("X MCP 🚀", description="A simple MCP server")

# Posting on X
@mcp.tool()
async def create_tweet(text: str) -> str:
    """Create a tweet"""
    # Ignore the return value
    r = await agent.run(text) 
    return r.output