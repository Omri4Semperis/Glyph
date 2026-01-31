from src.mcp_object import mcp

@mcp.tool()
def reverse_text(text: str) -> str:
    """
    Reverse the input string.
    """
    print(f"Using the reverse_text({text}) tool")
    return text[::-1]