from typing_extensions import Literal
from mcp_object import mcp
from read_an_asset import read_asset

@mcp.prompt()
def create_an_operation_doc_prompt(
    step_to_create_doc_for: float
) -> str:
    """
    Use this prompt when creating an operation document for a specific step in a design log.

    Args:
        step_to_create_doc_for (float): The step number to create the operation document for
    
    Returns:
        str: The generated prompt string.
    """
    template = read_asset("create_an_operation_doc.md")
    return template.format(step_to_create_doc_for=step_to_create_doc_for)
