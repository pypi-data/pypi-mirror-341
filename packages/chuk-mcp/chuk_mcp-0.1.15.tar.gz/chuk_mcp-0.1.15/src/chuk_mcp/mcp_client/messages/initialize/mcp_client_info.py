# chuk_mcp/chuk_mcp.mcp_client/messages/initialize/chuk_mcp.mcp_client_info.py
from chuk_mcp.mcp_client.mcp_pydantic_base import McpPydanticBase

class MCPClientInfo(McpPydanticBase):
    name: str = "MCP-CLI"
    version: str = "0.2"