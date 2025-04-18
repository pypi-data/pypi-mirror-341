from fastmcp import FastMCP, Client

mcp = FastMCP("Bus Mgmt MCP Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

import asyncio
client = Client(mcp)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result[0].text)

asyncio.run(call_tool("Tom"))
asyncio.run(call_tool("Jill"))

def main():
    print("bus-mgmt-mcp-server is running")
    mcp.run()
