import os
from mcp_object import mcp
from response import GlyphMCPResponse


@mcp.tool()
def get_dl_rules() -> GlyphMCPResponse[str]:
    """
    Returns the design log methodology rules from the assets directory.
    
    Returns:
        The content of design-log-rules.md as a string containing the design log methodology rules.
    """
    response = GlyphMCPResponse[str]()
    
    try:
        # Get the path to the assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        rules_file_path = os.path.join(project_root, "assets", "design-log-rules.md")
        
        # Read the rules file
        with open(rules_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        response.success = True
        response.result = content
        
    except FileNotFoundError:
        response.add_context(f"Design log rules file not found at {rules_file_path}")
    except Exception as e:
        response.add_context(f"Failed to load design log rules: {str(e)}")
    
    return response
