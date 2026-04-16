"""
Consolidated prompts module.

All Glyph prompts (slash commands) in one place.
"""
import re
from typing import Any, Dict
from mcp_object import mcp
from read_an_asset import read_asset


OPTIONAL_BLOCK_PATTERN = re.compile(
    r"\{\{#(?P<key>[a-zA-Z_][a-zA-Z0-9_]*)\}\}(?P<content>.*?)\{\{/(?P=key)\}\}",
    re.DOTALL,
)


def _stringify_prompt_value(value: Any) -> str:
    """Convert prompt replacement values to strings, treating None as empty."""
    if value is None:
        return ""
    return str(value)


def _has_prompt_value(value: Any) -> bool:
    """Return whether a prompt replacement value should be considered present."""
    return bool(_stringify_prompt_value(value).strip())


def _optional_block_flag(*values: Any) -> str:
    """Return a truthy marker when any prompt value is present."""
    return "1" if any(_has_prompt_value(value) for value in values) else ""


def _render_optional_blocks(prompt: str, replacements_dict: Dict[str, Any]) -> str:
    """Render or remove optional template blocks based on replacement values."""
    previous_prompt = None

    while prompt != previous_prompt:
        previous_prompt = prompt
        prompt = OPTIONAL_BLOCK_PATTERN.sub(
            lambda match: match.group("content")
            if _has_prompt_value(replacements_dict.get(match.group("key")))
            else "",
            prompt,
        )

    return prompt


def _cleanup_prompt_whitespace(prompt: str) -> str:
    """Collapse blank-line gaps left behind by optional blocks."""
    prompt = re.sub(r"[ \t]+\n", "\n", prompt)
    prompt = re.sub(r"\n{3,}", "\n\n", prompt)
    return prompt.strip()


def replace_in_prompts(prompt: str, replacements_dict: Dict[str, Any]) -> str:
    """
    Replace placeholders in a prompt string based on a replacements dictionary.

    Args:
        prompt: The original prompt string with placeholders
        replacements_dict: A dictionary mapping placeholders to their replacements

    Returns:
        The prompt string with placeholders replaced
    """
    prompt = _render_optional_blocks(prompt, replacements_dict)

    for k, v in replacements_dict.items():
        this = "{{" + k + "}}"
        that = _stringify_prompt_value(v)

        if this not in prompt:
            continue
        
        prompt = prompt.replace(this, that)

    return _cleanup_prompt_whitespace(prompt)


def _normalize_number(value: int | float | str) -> str:
    """Convert numeric value to clean string (float 1.0 → int 1 → str '1')."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _format_task_display(task_number: str | int | float) -> str:
    """
    Convert task_number to grammatically correct display format.

    Examples:
        - 1 → "Task 1"
        - "3" → "Task 3"
        - "1-3" → "Tasks 1-3"
        - "1, 2, 5" → "Tasks 1, 2, 5"
        - "all" → "all tasks"
    """
    task_str = _normalize_number(task_number)

    if task_str == "all":
        return "all tasks"
    elif task_str.isdigit():
        return f"Task {task_str}"
    else:
        # It's a range like "1-3" or comma-separated like "1, 2, 5"
        return f"Tasks {task_str}"


def _load_phase_prompt(
    asset_filename: str,
    phase_number: str,
    task_number: str | int | float,
    operation_document: str,
    additional_context: str | None = None
) -> str:
    """
    Load and format a phase prompt (planning or implementation).
    
    Args:
        asset_filename: The markdown asset file to load (e.g., "implementation_command.md")
        phase_number: The phase identifier (can be a single number or a list like "1 and 2")
        task_number: The task(s) to display
        operation_document: The operation document name/path
        additional_context: Optional context to include in the prompt
        
    Returns:
        Formatted prompt text
        
    """
    template = read_asset(asset_filename)
    task_display = _format_task_display(task_number)
    return replace_in_prompts(template, {
        "phase_number": _normalize_number(phase_number),
        "task_display": task_display,
        "operation_document": operation_document,
        "additional_context": additional_context
    })


# =============================================================================
# DESIGN LOG & OPERATION CREATION
# =============================================================================

@mcp.prompt()
def create_design_log(
    topic: str,
    additional_context: str | None = None
) -> str:
    """
    Trigger the creation of a new design log.

    Args:
        topic: The topic or feature for the design log
        additional_context: Any additional context or constraints

    Returns:
        The prompt for creating a design log.
    """
    template = read_asset("create_design_log.md")
    return replace_in_prompts(template, {
        "topic": topic,
        "additional_context": additional_context
    })


@mcp.prompt()
def create_operation_doc(
    step_to_create_doc_for: int | float | str | None = None,
    design_log_name: str | None = None,
    source_context: str | None = None
) -> str:
    """
    Trigger the creation of an operation document from optional source context.

    Args:
        step_to_create_doc_for: Optional step number or identifier to focus the operation document on
        design_log_name: Optional name or path of the related design log
        source_context: Optional general source context when the operation is not tied to a specific design log step

    Returns:
        The prompt for creating an operation document.
    """
    template = read_asset("create_an_operation_doc.md")
    return replace_in_prompts(template, {
        "step_to_create_doc_for": (
            _normalize_number(step_to_create_doc_for)
            if step_to_create_doc_for is not None
            else None
        ),
        "design_log_name": design_log_name,
        "source_context": source_context,
        "has_source_context": _optional_block_flag(
            step_to_create_doc_for,
            design_log_name,
            source_context,
        ),
    })


# =============================================================================
# PLANNING & IMPLEMENTATION
# =============================================================================

@mcp.prompt()
def plan_phase_or_task(
    phase_number: str,
    task_number: str | int | float = "all",
    operation_document: str = "Operation Document",
    additional_context: str | None = None
) -> str:
    """
    Trigger planning of a phase/task from an operation document.

    Args:
        phase_number: The phase identifier to plan (single or multiple, e.g., "1 and 2")
        task_number: The task(s) to plan. Can be:
                     - Single task: 1, 2, 5
                     - Range: "1-3"
                     - Multiple: "1, 2, 5"
                     - All tasks: "all" (default)
        operation_document: Name or path of the operation document (default: "Operation Document")
        additional_context: Optional context to include in the prompt

    Returns:
        The planning prompt.
    """
    return _load_phase_prompt(
        "implementation_command.md",
        phase_number,
        task_number,
        operation_document,
        additional_context
    )


@mcp.prompt()
def implement_phase_or_task(
    phase_number: str,
    task_number: str | int | float = "all",
    operation_document: str = "Operation Document",
    additional_context: str | None = None
) -> str:
    """
    Trigger implementation of a phase/task from an operation document.

    Args:
        phase_number: The phase identifier to implement (single or multiple, e.g., "1 and 2")
        task_number: The task(s) to implement. Can be:
                     - Single task: 1, 2, 5
                     - Range: "1-3"
                     - Multiple: "1, 2, 5"
                     - All tasks: "all" (default)
        operation_document: Name or path of the operation document (default: "Operation Document")
        additional_context: Optional context to include in the prompt

    Returns:
        The implementation prompt.
    """
    return _load_phase_prompt(
        "implementation_command.md",
        phase_number,
        task_number,
        operation_document,
        additional_context
    )


# =============================================================================
# CODE REVIEW & SYNC
# =============================================================================

@mcp.prompt()
def perform_code_review(
    what_is_being_reviewed: str | None = None,
    design_log_name: str | None = None,
    additional_context: str | None = None
) -> str:
    """
    Trigger a code review of an entity.

    Args:
        what_is_being_reviewed: (Optional) Name of the entity being reviewed
        design_log_name: (Optional) Name of the related design log
        additional_context: (Optional) Additional context for the review

    Returns:
        The code review prompt.
    """
    template = read_asset("code_review.md")
    return replace_in_prompts(template, {
        "what_is_being_reviewed": what_is_being_reviewed,
        "design_log_name": design_log_name,
        "additional_context": additional_context,
        "has_references": _optional_block_flag(design_log_name, additional_context)
    })


@mcp.prompt()
def sync_lessons_learned(
    operations_list: str = "Please specify operation document paths",
    design_logs_list: str = "Design logs will be auto-detected from operation references"
) -> str:
    """
    Sync lessons learned from operations back to design logs.

    Args:
        operations_list: Comma-separated operation doc paths to sync from
        design_logs_list: Comma-separated design log paths to sync to (auto-detected if not specified)

    Returns:
        The sync lessons learned prompt.
    """
    template = read_asset("sync_lessons_learned.md")
    return replace_in_prompts(template, {
        "operations_list": operations_list,
        "design_logs_list": design_logs_list
    })


# =============================================================================
# UTILITY
# =============================================================================

@mcp.prompt()
def compact_conversation() -> str:
    """
    Summarize a long conversation for context transfer to a new session.

    Returns:
        The compact conversation prompt.
    """
    return read_asset("compact_conversation.md")
