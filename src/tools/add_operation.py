import os
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import add_document, validate_absolute_path, append_to_summary


def update_operation_summary(response: GlyphMCPResponse[None], abs_path: str, title: str, short_desc: str) -> None:
    """
    Update the _summary.md file with the newly created operation entry.
    
    Args:
        response: The response object from add_document.
        abs_path: The absolute path of the project's root where the .assistant folder is located.
        title: The title of the operation.
        short_desc: A short description for the operation.
    """
    if not response.success:
        return
    
    operations_dir = os.path.join(abs_path, BASE_NAME, "operations")
    summary_path = os.path.join(operations_dir, "_summary.md")
    
    # Extract filename from the context message
    for context in response.context:
        if "Created new operation document:" in context:
            filename = context.split(": ")[1]
            success, message = append_to_summary(summary_path, filename, short_desc)
            response.add_context(message)
            break


@mcp.tool()
def add_operation(abs_path: str, title: str, short_desc: str) -> GlyphMCPResponse[None]:
    """
    Add a new operation document file in the operations directory
    
    Prerequisite: Read the operation rules.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        title: The title for the operation. The file will be named op_{number}_{title}.md
        short_desc: A short description for the operation. Will be used in the summary.
    
    Returns:
        GlyphMCPResponse indicating success or failure.
    """
    response = GlyphMCPResponse[None]()
    if not validate_absolute_path(abs_path, response):
        return response
    
    response = add_document(
        abs_path=abs_path,
        title=title,
        subdirectory="operations",
        prefix="op",
        template_asset="operation_doc_template.md",
        doc_type="operation document"
    )
    
    update_operation_summary(response, abs_path, title, short_desc)
    
    return response
