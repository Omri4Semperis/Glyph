import os
import re
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from read_an_asset import read_asset


def get_next_dl_number(design_logs_dir: str) -> int:
    """
    Get the next design log number by scanning existing files in the design_logs directory.
    
    Args:
        design_logs_dir: Path to the design_logs directory.
    
    Returns:
        The next available design log number.
    """
    if not os.path.exists(design_logs_dir):
        return 1
    
    max_number = 0
    pattern = re.compile(r'^dl_(\d+)_.*\.md$')
    
    for filename in os.listdir(design_logs_dir):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_number:
                max_number = num
    
    return max_number + 1


@mcp.tool()
def add_design_log(base_dir_path: str, title: str) -> GlyphMCPResponse:
    """
    Add a new design log file in the design log directory.
    
    Args:
        base_dir_path: The base directory path where the .assistant folder is located.
        title: The title for the design log. The file will be named dl_{number}_{title}.md
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    response = GlyphMCPResponse[None]()
    
    try:
        # Construct the design_logs directory path
        design_logs_dir = os.path.join(base_dir_path, BASE_NAME, "design_logs")
        
        # Check if the assistant directory is initialized
        if not os.path.exists(design_logs_dir):
            response.add_context(f"Design logs directory not found at {design_logs_dir}. Please initialize the assistant directory first.")
            return response
        
        # Get the next design log number
        next_number = get_next_dl_number(design_logs_dir)
        
        # Sanitize the title for use in filename (replace spaces with underscores, remove special chars)
        sanitized_title = re.sub(r'[^\w\s-]', '', title).strip()
        sanitized_title = re.sub(r'[-\s]+', '_', sanitized_title).lower()
        
        # Create the new filename
        new_filename = f"dl_{next_number}_{sanitized_title}.md"
        new_filepath = os.path.join(design_logs_dir, new_filename)
        
        # Read the template
        template_content = read_asset("dl_template.md")
        
        # Write the new design log file
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        response.add_context(f"Created new design log: {new_filename}")
        
        # Append entry to summary.md
        summary_path = os.path.join(design_logs_dir, "_summary.md")
        
        if os.path.exists(summary_path):
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(f"\n- **[{new_filename}]({new_filename})**: {title}\n")
            response.add_context(f"Added entry to summary.md")
        else:
            response.add_context(f"Warning: summary.md not found at {summary_path}")
        
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to create design log: {str(e)}")
    
    return response
