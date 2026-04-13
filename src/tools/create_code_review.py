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
    additional_references: str = "N/A",
    review_type: str = "Implementation",
    review_focus: str = "Full review",
    target_context: str = "N/A",
    assumptions: str = "None",
    primary_references: str = "N/A"
) -> GlyphMCPResponse[None]:
    """
    Create a code review document from template in the ad_hoc directory.
    
    This tool generates a code review template with basic information pre-filled,
    ready to be completed with review findings. The file is saved in the
    .assistant/ad_hoc directory with a timestamp-based filename.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        what_is_being_reviewed: Subject of the review (e.g., "Export to CSV Feature", "User Authentication Module")
        design_log: Legacy alias for a design log reference. Merged into primary_references when provided.
        operation_doc: Legacy alias for an operation document reference. Merged into primary_references when provided.
        additional_references: Additional references like PR links, commit hashes, tickets, or benchmarks (default: "N/A")
        review_type: Review category such as Implementation, Refactoring, Source code, or PR review.
        review_focus: Review scope such as Full review, Testing, Documentation, or Security.
        target_context: Language, framework/runtime, platform, version, or other relevant constraints.
        assumptions: Assumptions made because some review context was missing.
        primary_references: Primary supporting references such as specs, PRs, design logs, operation docs, or artifacts.
    
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
        
        legacy_references = []
        if design_log != "N/A":
            legacy_references.append(f"Design Log: {design_log}")
        if operation_doc != "N/A":
            legacy_references.append(f"Operation Document: {operation_doc}")

        resolved_primary_references = primary_references
        if legacy_references:
            legacy_references_text = "; ".join(legacy_references)
            if resolved_primary_references == "N/A":
                resolved_primary_references = legacy_references_text
            else:
                resolved_primary_references = f"{resolved_primary_references}; {legacy_references_text}"

        # Fill in the template with provided information
        filled_content = template_content.replace("[What's being reviewed]", what_is_being_reviewed)
        filled_content = filled_content.replace("[Feature/Module Name]", what_is_being_reviewed)
        filled_content = filled_content.replace("[YYYY-MM-DD]", current_date)
        filled_content = filled_content.replace("[Name/Glyph AI Assistant]", "Glyph AI Assistant")
        filled_content = filled_content.replace("[Implementation / Refactoring / Source code / PR / Artifact / etc.]", review_type)
        filled_content = filled_content.replace("[Full review / Functionality / Code quality / Testing / Documentation / Performance / Security / Custom]", review_focus)
        filled_content = filled_content.replace("[Language, framework/runtime, platform, version, constraints, etc.]", target_context)
        filled_content = filled_content.replace("[State any assumptions made because context was missing; otherwise \"None\"]", assumptions)
        filled_content = filled_content.replace("[Design log, operation doc, PR, issue, spec, benchmark, artifact, etc.]", resolved_primary_references)
        filled_content = filled_content.replace("[Supporting refs or \"N/A\"]", additional_references)
        
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
            "The template has been pre-filled with the review subject, context, and references. "
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
