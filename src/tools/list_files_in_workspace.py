from src.mcp_object import mcp

@mcp.tool()
def list_files_in_workspace(p: str) -> str:
    """
    List all files in the given workspace path.
    """
    import os

    try:
        files = os.listdir(p)
        print(f"Using the list_files_in_workspace({p}) tool")
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"