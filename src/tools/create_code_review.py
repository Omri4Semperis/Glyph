"""
Tool for creating code review documents in the ad_hoc directory.
"""
import os
from datetime import datetime
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from read_an_asset import read_asset
from ._utils import validate_absolute_path, sanitize_title


@mcp.tool()
def add_code_review(
    abs_path: str,
    what_is_being_reviewed: str = "Feature/Module Name",
    design_log: str = "N/A",
    operation_doc: str = "N/A",
    additional_references: str = "N/A"
) -> GlyphMCPResponse[None]:
    """
    Create a code review document from template in the ad_hoc directory.
    
    This tool generates a code review template with basic information pre-filled,
    ready to be completed with review findings. The file is saved in the 
    .assistant/ad_hoc directory with a timestamp-based filename.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        what_is_being_reviewed: What is being reviewed (e.g., "Export to CSV Feature", "User Authentication Module")
        design_log: Link or reference to related design log (default: "N/A")
        operation_doc: Link or reference to related operation document (default: "N/A")
        additional_references: Additional references like PR links, commit hashes, etc. (default: "N/A")
    
    Returns:
        GlyphMCPResponse indicating success or failure with the path to the created file.
    """
    response = GlyphMCPResponse[None]()
    
    if not validate_absolute_path(abs_path, response):
        return response
    
    try:
        # Check if ad_hoc directory exists
        ad_hoc_dir = os.path.join(abs_path, BASE_NAME, "ad_hoc")
        if not os.path.exists(ad_hoc_dir):
            response.add_context(
                f"ad_hoc directory not found at {ad_hoc_dir}. "
                "Please initialize the assistant directory first using the init_assistant_dir tool."
            )
            return response
        
        # Read the code review template
        template_content = read_asset("code_review_template.md")
        
        # Get current date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Fill in the template with provided information
        filled_content = template_content.replace("[Feature/Module Name]", what_is_being_reviewed)
        filled_content = filled_content.replace("[YYYY-MM-DD]", current_date)
        filled_content = filled_content.replace("[Name/Glyph AI Assistant]", "Glyph AI Assistant")
        filled_content = filled_content.replace("[Type: Source code / Implementation / Refactoring / etc.]", "Implementation")
        filled_content = filled_content.replace("[Link to design log if applicable]", design_log)
        filled_content = filled_content.replace("[Link to operation document if applicable]", operation_doc)
        filled_content = filled_content.replace("[PR link, commit hash, requirements document, etc.]", additional_references)
        
        # Create filename with timestamp and sanitized review subject
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_subject = sanitize_title(what_is_being_reviewed.replace("/", "_"))
        # Limit the subject length in filename
        if len(sanitized_subject) > 40:
            sanitized_subject = sanitized_subject[:40]
        filename = f"code_review_{timestamp}_{sanitized_subject}.md"
        filepath = os.path.join(ad_hoc_dir, filename)
        
        # Write the filled template to ad_hoc directory
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(filled_content)
        
        response.add_context(f"Created code review template: {filename}")
        response.add_context(f"Full path: {filepath}")
        response.add_context(
            "The template has been pre-filled with basic information. "
            "Complete the review by filling in the detailed sections with your findings."
        )
        response.add_context(
            "Remember: Everything is either ✅ Good or [issue_X emoji]. "
            "Track all issues consistently across all sections."
        )
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to create code review template: {str(e)}")
    
    return response
