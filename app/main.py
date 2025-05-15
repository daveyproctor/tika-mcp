import sys
import traceback
import json
from mcp.server.fastmcp import FastMCP
from app.model import extract_file_content

# Set up logging to a file
import logging
logging.basicConfig(
    filename='mcp_server.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("Creating FastMCP server...")
logging.info("Creating FastMCP server...")
try:
    mcp = FastMCP("tika")
    print("FastMCP server created.")
    logging.info("FastMCP server created.")
except Exception as e:
    print(f"Error creating FastMCP server: {e}")
    logging.error(f"Error creating FastMCP server: {e}")
    traceback.print_exc()
    logging.error(traceback.format_exc())
    sys.exit(1)

@mcp.tool()
async def extract_file(file_path: str, tika_url: str) -> dict:
    """Extract content and metadata from a file using Tika.

    Args:
        file_path: Path to the file.
        tika_url: URL of the running Tika server.
    """
    print(f"extract_file tool called with file_path: {file_path}, tika_url: {tika_url}")
    logging.info(f"extract_file tool called with file_path: {file_path}, tika_url: {tika_url}")
    try:
        result = await extract_file_content(file_path, tika_url)
        logging.info(f"extract_file_content returned: {result}")
        return result
    except Exception as e:
        print(f"Error in extract_file: {e}")
        logging.error(f"Error in extract_file: {e}")
        traceback.print_exc()
        logging.error(traceback.format_exc())
        return {"error": str(e)}

if __name__ == "__main__":
    print("Running MCP server with stdio transport...")
    logging.info("Running MCP server with stdio transport...")
    try:
        # Run the server with stdio transport
        mcp.run(transport="stdio")
        
        print("MCP server finished running.")
        logging.info("MCP server finished running.")
    except Exception as e:
        print(f"Error running MCP server: {e}")
        logging.error(f"Error running MCP server: {e}")
        traceback.print_exc()
        logging.error(traceback.format_exc())
        sys.exit(1)
