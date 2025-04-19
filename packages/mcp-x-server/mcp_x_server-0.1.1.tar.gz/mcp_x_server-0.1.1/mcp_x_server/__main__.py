from server import mcp

def cli():
     mcp.run(transport="stdio")

if __name__ == "__main__":
    cli()
