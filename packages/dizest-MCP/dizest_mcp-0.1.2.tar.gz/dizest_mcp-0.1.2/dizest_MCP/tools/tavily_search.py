import os
from typing import Dict
from tavily import TavilyClient
from dizest_MCP.mcp_server import mcp

_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))

@mcp.tool()
def tavily_search(query: str) -> Dict:
    """Search the web via Tavily."""
    try:
        return _client.search(query=query, search_depth="advanced")
    except Exception as e:
        return {"error": str(e), "results": [{"content": f"검색 중 오류: {e}"}]}