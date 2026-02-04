from mcp_object import mcp
from response import GlyphMCPResponse
from read_an_asset import read_asset_exact as _read_asset_exact


@mcp.tool()
def read_asset_exact(relative_path: str) -> GlyphMCPResponse[str]:
    """
    Reads the content of a file from the assets directory using an exact relative path.
    
    Use this tool when:
    - read_asset() returned an error about multiple files with the same name
    - You know the exact location of the asset you want to read
    
    The relative path should be from the assets directory root.
    Example paths:
    - 'prompts/compact_conversation.md'
    - 'rules/design_log_rules.md'
    - 'templates/dl_template.md'
    - 'examples/dl_example_research.md'
    - 'skills/_how_to_glyph.md'
    
    Args:
        relative_path: The path relative to the assets directory 
                      (e.g., 'prompts/compact_conversation.md').
    
    Returns:
        GlyphMCPResponse containing the file content or error information.
    """
    response = GlyphMCPResponse[str]()
    content = _read_asset_exact(relative_path)
    
    # Check if content is an error message
    if content.startswith("Asset file") or content.startswith("Error reading"):
        response.add_context(content)
    else:
        response.success = True
        response.result = content
    
    return response