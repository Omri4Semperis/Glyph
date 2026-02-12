"""
Consolidated knowledge/skills module.

Provides access to all Glyph knowledge assets: skills, examples, and templates.
"""
from typing import Literal
from mcp_object import mcp
from response import GlyphMCPResponse
from read_an_asset import read_asset


def _read_asset_with_response(filename: str) -> GlyphMCPResponse[str]:
    """Read an asset file and return it wrapped in a GlyphMCPResponse."""
    response = GlyphMCPResponse[str]()
    try:
        content = read_asset(filename)
        response.success = True
        response.result = content
    except (FileNotFoundError, ValueError) as e:
        response.add_context(str(e))
    
    return response


# =============================================================================
# SKILLS
# =============================================================================

@mcp.tool()
def get_skill(
    skill: Literal[
        "about_glyph",
        "about_design_logs",
        "about_operation_docs",
        "how_to_implement_a_phase_or_task",
        "mermaid_tips_and_tricks"
    ]
) -> GlyphMCPResponse[str]:
    """
    Returns skill/knowledge content for the specified topic.
    
    Use this tool to access Glyph methodology guidelines, principles, and best practices.

    Args:
        skill: The skill to retrieve:
            - "about_glyph": Complete guide to all Glyph tools and skills
            - "about_design_logs": Guidelines for creating and maintaining design logs
            - "about_operation_docs": Guidelines for creating and managing operations
            - "how_to_implement_a_phase_or_task": Guidelines for planning and implementing tasks
            - "mermaid_tips_and_tricks": Examples and tips for creating Mermaid diagrams

    Returns:
        The skill content.
    """
    file_map = {
        "about_glyph": "about_glyph.md",
        "about_design_logs": "about_design_logs.md",
        "about_operation_docs": "about_operation_docs.md",
        "how_to_implement_a_phase_or_task": "how_to_implement_a_phase_or_task.md",
        "mermaid_tips_and_tricks": "mermaid_tips_and_tricks.md"
    }
    
    filename = file_map.get(skill)
    if not filename:
        response = GlyphMCPResponse[str]()
        response.add_context(f"Invalid skill: {skill}. Must be one of: {', '.join(file_map.keys())}")
        return response
    
    return _read_asset_with_response(filename)


# =============================================================================
# EXAMPLES
# =============================================================================

@mcp.tool()
def get_example(
    example: Literal[
        "design_log",
        "operation_doc",
        "code_review"
    ]
) -> GlyphMCPResponse[str]:
    """
    Returns an example file for the specified document type.
    
    Use this tool when you need to reference an example for creating design logs, 
    operations, or code reviews.

    Args:
        example: Type of example to retrieve:
            - "design_log": Example design log
            - "operation_doc": Example operation document
            - "code_review": Example code review report

    Returns:
        The content of the requested example.
    """
    file_map = {
        "design_log": "dl_example_implementation.md",
        "operation_doc": "operation_example.md",
        "code_review": "code_review_example.md"
    }

    filename = file_map.get(example)
    if not filename:
        response = GlyphMCPResponse[str]()
        response.add_context(f"Invalid example: {example}. Must be one of: {', '.join(file_map.keys())}")
        return response

    return _read_asset_with_response(filename)


# =============================================================================
# TEMPLATES
# =============================================================================

@mcp.tool()
def get_template(
    template: Literal[
        "design_log",
        "operation_doc",
        "code_review"
    ]
) -> GlyphMCPResponse[str]:
    """
    Returns a template for the specified document type.
    
    Use this tool when you need to access a template for creating design logs, 
    operations, or code reviews.

    Args:
        template: Type of template to retrieve:
            - "design_log": Template for design logs
            - "operation_doc": Template for operation documents
            - "code_review": Template for code review reports

    Returns:
        The content of the requested template.
    """
    file_map = {
        "design_log": "dl_template.md",
        "operation_doc": "operation_doc_template.md",
        "code_review": "code_review_template.md"
    }

    filename = file_map.get(template)
    if not filename:
        response = GlyphMCPResponse[str]()
        response.add_context(f"Invalid template: {template}. Must be one of: {', '.join(file_map.keys())}")
        return response

    return _read_asset_with_response(filename)
