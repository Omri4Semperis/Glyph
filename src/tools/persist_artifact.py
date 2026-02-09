import os
import shutil
import re
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import get_next_number, validate_absolute_path, append_to_summary
from .reference_graph import update_reference_graph
from typing import List, Dict


def validate_source_file(source_file_path: str, response: GlyphMCPResponse[None]) -> bool:
    """
    Validate that the source file exists and is a file.
    
    Args:
        source_file_path: Path to the source file to validate.
        response: Response object to add context messages to.
    
    Returns:
        True if the file is valid, False otherwise.
    """
    if not os.path.exists(source_file_path):
        response.add_context(f"Source file not found: {source_file_path}")
        return False
    
    if not os.path.isfile(source_file_path):
        response.add_context(f"Source path is not a file: {source_file_path}")
        return False
    
    return True


def get_and_validate_dirs(abs_path: str, response: GlyphMCPResponse[None]) -> tuple[str, str] | None:
    """
    Get and validate the ad_hoc and artifacts directories.
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located.
        response: Response object to add context messages to.
    
    Returns:
        A tuple of (ad_hoc_dir, artifacts_dir) if both exist, None otherwise.
    """
    ad_hoc_dir = os.path.join(abs_path, BASE_NAME, "ad_hoc")
    artifacts_dir = os.path.join(abs_path, BASE_NAME, "artifacts")

    if not os.path.exists(ad_hoc_dir):
        response.add_context(f"ad_hoc directory not found: {ad_hoc_dir}")
        return None
    
    if not os.path.exists(artifacts_dir):
        response.add_context(
            f"Artifacts directory not found at {artifacts_dir}. "
            "Please initialize the assistant directory first."
        )
        return None
    
    return ad_hoc_dir, artifacts_dir


def copy_artifact(source_file_path: str, artifacts_dir: str) -> tuple[str, str]:
    """
    Copy the source file to the artifacts directory with proper naming.
    
    Args:
        source_file_path: Path to the source file.
        artifacts_dir: Path to the artifacts directory.
    
    Returns:
        A tuple of (new_filename, new_filepath).
    """
    # Get the next artifact number (using 'art' prefix, accepting any extension)
    next_number = get_next_number(artifacts_dir, "art", extension="")
    
    # Extract the original filename
    original_filename = os.path.basename(source_file_path)
    
    # Replace spaces with underscores in the filename
    sanitized_filename = original_filename.replace(' ', '_')
    
    # Create the new artifact filename
    new_filename = f"art_{next_number}_{sanitized_filename}"
    new_filepath = os.path.join(artifacts_dir, new_filename)
    
    # Copy the file to artifacts directory
    shutil.copy2(source_file_path, new_filepath)
    
    return new_filename, new_filepath


def fix_references_in_file(file_path: str, old_filename: str, new_filename: str) -> int:
    """
    Replace all references to old_filename with new_filename in a file.
    
    Args:
        file_path: Path to the file to update.
        old_filename: The original filename to search for.
        new_filename: The new filename to replace with.
    
    Returns:
        Number of replacements made.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences before replacement
        count = content.count(old_filename)
        
        if count > 0:
            # Replace all occurrences
            new_content = content.replace(old_filename, new_filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return count
    except Exception:
        # Silently skip files that can't be read/written
        return 0


def fix_references_in_directories(assistant_dir: str, old_filename: str, new_filename: str) -> dict[str, int]:
    """
    Fix all references to old_filename in design_logs, operations, and artifacts directories.
    
    Args:
        assistant_dir: Path to the .assistant directory.
        old_filename: The original filename to search for.
        new_filename: The new filename to replace with.
    
    Returns:
        Dictionary mapping file paths to number of replacements made.
    """
    replacements = {}
    
    for dir_name in ["design_logs", "operations", "artifacts"]:
        dir_path = os.path.join(assistant_dir, dir_name)
        
        if not os.path.exists(dir_path):
            continue
        
        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                count = fix_references_in_file(file_path, old_filename, new_filename)
                
                if count > 0:
                    replacements[file_path] = count
    
    return replacements


@mcp.tool()
def persist_artifacts(
    abs_path: str, 
    files: List[str],
    descriptions: Dict[str, str],
    delete_from_ad_hoc: bool,
    fix_references: bool
) -> GlyphMCPResponse[None]:
    """
    Persist files from the ad_hoc directory or other locations to the artifacts directory.
    
    Copies each file to the .assistant/artifacts/ directory and renames it with the pattern:
    art_{serial_number}_{original_file_name}.{original_extension}
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        files: List of filenames or full file paths to persist. If a filename without path is provided, 
               it's assumed to be in `.assistant/ad_hoc` dir. Full absolute paths are also supported.
        descriptions: Dictionary mapping each filename to its short description. Keys should match the filenames in `files`.
                     Each description will be added to the artifacts summary.
        delete_from_ad_hoc: If True, delete the original files from their source location after persisting.
        fix_references: If True, automatically scan all files in design_logs, operations, and artifacts directories 
                       and update any references from the old filename to the new artifact filename.
    
    Returns:
        GlyphMCPResponse indicating success or failure, with the new artifact filenames.
    """
    response = GlyphMCPResponse[None]()
    
    if not validate_absolute_path(abs_path, response):
        return response
    
    try:
        dirs = get_and_validate_dirs(abs_path, response)
        if dirs is None:
            return response
        
        ad_hoc_dir, artifacts_dir = dirs
        
        if not files:
            response.add_context("No files specified to persist.")
            return response
        
        # Validate descriptions
        if not descriptions:
            response.add_context("No descriptions provided. Each artifact requires a short description.")
            return response
        
        artifacts_summary_path = os.path.join(artifacts_dir, "_summary.md")
        
        for file_name in files:
            # Determine if file_name is a full path or just a filename
            if os.path.isabs(file_name):
                # Use the full path as-is
                source_file_path = file_name
                # Extract just the filename for the description lookup
                lookup_name = os.path.basename(file_name)
            else:
                # Treat as filename in ad_hoc directory
                source_file_path = os.path.join(ad_hoc_dir, file_name)
                lookup_name = file_name
            
            # Validate source file
            if not validate_source_file(source_file_path, response):
                continue  # Skip invalid files but continue with others
            
            # Check if description is provided for this file
            if lookup_name not in descriptions:
                response.add_context(f"Warning: No description provided for {lookup_name}. Skipping.")
                continue
            
            # Copy the artifact
            new_filename, new_filepath = copy_artifact(source_file_path, artifacts_dir)
            
            # Add to summary
            short_desc = descriptions[lookup_name]
            success, message = append_to_summary(artifacts_summary_path, new_filename, short_desc)
            response.add_context(message)
            
            # Add success context
            response.add_context(f"Persisted artifact: {new_filename}")
            response.add_context(f"Source: {source_file_path}")
            response.add_context(f"Destination: {new_filepath}")
            
            # Fix references if requested
            if fix_references:
                assistant_dir = os.path.join(abs_path, BASE_NAME)
                replacements = fix_references_in_directories(assistant_dir, file_name, new_filename)
                
                if replacements:
                    response.add_context(f"Fixed references to '{file_name}' -> '{new_filename}':")
                    for ref_file, count in replacements.items():
                        rel_path = os.path.relpath(ref_file, abs_path)
                        response.add_context(f"  - {rel_path}: {count} replacement(s)")
                else:
                    response.add_context(f"No references to '{file_name}' found to fix")
            
            # Delete original file if requested
            if delete_from_ad_hoc:
                try:
                    os.remove(source_file_path)
                    response.add_context(f"Deleted original file from ad_hoc: {file_name}")
                except Exception as e:
                    response.add_context(f"Warning: Failed to delete original file {file_name}: {str(e)}")
        
        # Update reference graph after persisting artifacts
        update_response = update_reference_graph(abs_path)
        if not update_response.success:
            response.add_context("Warning: Failed to update reference graph after persisting artifacts")
            response.add_context(update_response.context)
        else:
            response.add_context("Reference graph updated successfully")
        
        response.success = True
        
    except Exception as e:
        response.add_context(f"Failed to persist artifacts: {str(e)}")
    
    return response
