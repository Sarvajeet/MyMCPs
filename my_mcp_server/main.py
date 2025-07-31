from fastmcp import FastMCP
import datetime

app = FastMCP()

# Define a sample tool
@app.tool()
async def greet(name: str) -> str:
    """
    This tool greets the given name.
    """
    return f"Hello, {name}!"

# Define a sample resource
@app.resource("http://example.com/get_time")
async def get_time():
    """
    This resource returns the current time.
    """
    return {"time": datetime.datetime.now().isoformat()}
