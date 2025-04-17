import asyncio
import sys
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    """Run a simple MCP client to test the Norman MCP server."""
    print("Setting up MCP client...")
    
    # Define server parameters
    server_params = StdioServerParameters(
        command="norman-mcp",
        args=["--email", "bond9555@gmail.com", "--password", "949254aA!@", "--environment", "sandbox", "--debug"],
        env=None
    )
    
    # Create an exit stack for proper resource management
    exit_stack = AsyncExitStack()
    
    try:
        print("Connecting to Norman MCP server...")
        # Connect to the server
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        
        # Create a client session
        session = await exit_stack.enter_async_context(ClientSession(stdio, write))
        
        # Initialize the connection
        print("Initializing connection...")
        await session.initialize()
        
        # List available tools
        print("Listing available tools...")
        tools_response = await session.list_tools()
        print(f"Available tools: {[tool.name for tool in tools_response.tools]}")
        
        # List available resources
        print("Listing available resources...")
        resources_response = await session.list_resources()
        print(f"Available resources: {[resource.uri for resource in resources_response.resources]}")
        
        # If there are any resources, try to read one
        if resources_response.resources:
            first_resource = resources_response.resources[0]
            print(f"Reading resource: {first_resource.uri}")
            content, mime_type = await session.read_resource(first_resource.uri)
            print(f"Resource content: {content[:100]}...")
        
        # If there are any tools, try to call one
        if tools_response.tools:
            first_tool = tools_response.tools[0]
            print(f"Calling tool: {first_tool.name}")
            result = await session.call_tool(first_tool.name, {})
            print(f"Tool result: {result}")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error testing Norman MCP server: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Close all resources
        await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main()) 