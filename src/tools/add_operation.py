from mcp_object import mcp
from response import GlyphMCPResponse
from ._utils import add_document


@mcp.tool()
def add_operation(base_dir_path: str, title: str) -> GlyphMCPResponse[None]:
    """
    Add a new operation document file in the operations directory.
    
    Prerequisite: Read the operation rules.
    
    Args:
        base_dir_path: The base directory path where the .assistant folder is located.
        title: The title for the operation. The file will be named op_{number}_{title}.md
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    return add_document(
        base_dir_path=base_dir_path,
        title=title,
        subdirectory="operations",
        prefix="op",
        template_asset="operation_doc_template.md",
        doc_type="operation document"
    )
