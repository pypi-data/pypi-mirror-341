# server.py
import sys

from mcp.server.fastmcp import FastMCP
    
# Create an MCP server
mcp = FastMCP("Add MCP")
    
    
# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
    
    
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a prompt for mathematical operations
@mcp.prompt("calculate")
def calculate_prompt(operation: str = None, numbers: str = None):
    """
    A prompt template for performing mathematical calculations.
    
    Args:
        operation: The type of operation (add, subtract, multiply, divide)
        numbers: The numbers to perform the operation on
    """
    # Construct a structured message using the arguments
    if operation and numbers:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please {operation} these numbers: {numbers}"
                    }
                }
            ]
        }
    else:
        # Default prompt if no arguments provided
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need help with a mathematical calculation. What operation would you like to perform, and on which numbers?"
                    }
                }
            ]
        }
        
if __name__ == "__main__":
    print("Starting MCP server...", file=sys.stderr)
    mcp.run()