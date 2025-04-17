import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# --- 환경변수(.env) 로드 --------------------------------------------------
load_dotenv()     

# --- FastMCP 인스턴스 ----------------------------------------------------
mcp = FastMCP("MCP_server")

import dizest_MCP.tools    

def run(*, transport: str = "sse") -> None:
    mcp.run(transport=transport)
