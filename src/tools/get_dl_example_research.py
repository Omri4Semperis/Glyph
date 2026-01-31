import os
from typing import Literal
from mcp_object import mcp
from response import GlyphMCPResponse


@mcp.tool()
def get_dl_example(example_type: Literal["research_dl_example", "implementation_dl_example"]) -> GlyphMCPResponse[str]:
    """
    Returns the content of a design log example from the assets directory.
    
    Args:
        example_type: Type of design log example to retrieve. Must be either:
            - "research_dl_example": Returns dl_example_research.md
            - "implementation_dl_example": Returns dl_example_implementation.md
    
    Returns:
        The content of the requested design log example as a string.
    """
    response = GlyphMCPResponse[str]()
    
    # Map example types to file names
    file_map = {
        "research_dl_example": "dl_example_research.md",
        "implementation_dl_example": "dl_example_implementation.md"
    }
    
    try:
        # Get the filename for the requested type
        filename = file_map.get(example_type)
        if not filename:
            response.add_context(f"Invalid example type: {example_type}. Must be 'research_dl_example' or 'implementation_dl_example'")
            return response
        
        # Get the path to the assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        example_file_path = os.path.join(project_root, "assets", filename)
        
        # Read the example file
        with open(example_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        response.success = True
        response.result = content
        
    except FileNotFoundError:
        response.add_context(f"Design log example file not found at {example_file_path}")
    except Exception as e:
        response.add_context(f"Failed to load design log example: {str(e)}")
    
    return response
