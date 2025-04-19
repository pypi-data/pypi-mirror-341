from mcp_x_server.server import mcp
import sys
sys.path.append("..")

def cli():
     mcp.run(transport="stdio")

if __name__ == "__main__":
    cli()
