# chuk_mcp/chuk_mcp.mcp_client/messages/initialize/chuk_mcp.mcp_client_capabilties.py
from chuk_mcp.mcp_client.mcp_pydantic_base import McpPydanticBase, Field

class MCPClientCapabilities(McpPydanticBase):
    roots: dict = Field(default_factory=lambda: {"listChanged": True})
    sampling: dict = Field(default_factory=dict)
    experimental: dict = Field(default_factory=dict)