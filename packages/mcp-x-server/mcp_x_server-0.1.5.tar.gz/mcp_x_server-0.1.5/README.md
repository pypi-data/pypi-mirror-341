# MCP X Server
What can you do with MCP X Server? Give it a sentence or a topic, and it will help you write and refine a tweet, then publish it to X.

## Build image
```shell
docker build -t mcp-x-server:latest .
```

## How to run with STDIO

### Local
```json
{
    "mcpServices": {
        "x-mcp": {
            "command": "uv",
            "args": [
                "run",
                "--with",
                "fastmcp",
                "--with",
                "pydantic-ai",
                "--with",
                "pydantic-ai-slim[duckduckgo,openai]",
                "--with",
                "dotenv",
                "--with",
                "python-twitter-v2",
                "fastmcp",
                "run",
                "/Users/wenyanglu/Workspace/ai/mcp_x_server/server.py"
            ],
            "env": {
                "CONSUMER_KEY": "*******************",,
                "CONSUMER_SECRET": "*******************",
                "ACCESS_TOKEN": "*******************",
                "ACCESS_SECRET": "*******************",
                "DEEPSEEK_API_KEY": "*******************"
            }
        }
    }
}
```

### Docker
```shell
docker run -i \
  -e CONSUMER_KEY="your-consumer-key" \
  -e CONSUMER_SECRET="your-consumer-secret" \
  -e ACCESS_TOKEN="your-access-token" \
  -e ACCESS_SECRET="your-access-secret" \
  -e DEEPSEEK_API_KEY="your-deepseek-key" \
  mcp-x-server:latest
```

## Run with SSE
```shell
fastmcp run --transport sse server.py
```