from mcp.server.fastmcp import FastMCP
from app.model import extract_file_content

print("Creating FastMCP server...")
mcp = FastMCP("tika")
print("FastMCP server created.")

@mcp.tool()
async def extract_file(file_path: str, tika_url: str) -> dict:
    """Extract content and metadata from a file using Tika.

    Args:
        file_path: Path to the file.
        tika_url: URL of the running Tika server.
    """
    print(f"extract_file tool called with file_path: {file_path}, tika_url: {tika_url}")
    return await extract_file_content(file_path, tika_url)

if __name__ == "__main__":
    print("Running MCP server with stdio transport...")
    mcp.run(transport="stdio")
    print("MCP server finished running.")
