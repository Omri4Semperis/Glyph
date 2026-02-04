from mcp_object import mcp
from read_an_asset import read_asset

@mcp.prompt()
def compact_conversation_prompt() -> str:
    """
    A useful prompt to summarize long conversations.
    """
    return read_asset("compact_conversation.md")
