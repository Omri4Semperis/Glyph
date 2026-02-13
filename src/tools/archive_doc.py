import os
import shutil
import re
from mcp_object import mcp
from config import BASE_NAME
from response import GlyphMCPResponse
from ._utils import validate_absolute_path, append_to_summary
from .reference_graph import update_reference_graph
from typing import Literal, Optional


def find_document_by_number(directory: str, prefix: str, number: int) -> tuple[str, str] | None:
    """
    Find a document file by its type and number.
    
    Args:
        directory: Path to the directory to search in.
        prefix: The file prefix (e.g., 'dl', 'op', 'art').
        number: The document number to find.
    
    Returns:
        A tuple of (filename, filepath) if found, None otherwise.
    """
    if not os.path.exists(directory):
        return None
    
    pattern = re.compile(rf'^{prefix}_{number}_.*')
    
    for filename in os.listdir(directory):
        if pattern.match(filename) and os.path.isfile(os.path.join(directory, filename)):
            return filename, os.path.join(directory, filename)
    
    return None


def move_to_archive(source_path: str, archive_dir: str, filename: str) -> str:
    """
    Move a file to the archive directory.
    
    Args:
        source_path: Path to the source file.
        archive_dir: Path to the archive directory.
        filename: Name of the file.
    
    Returns:
        The new file path in the archive directory.
    """
    os.makedirs(archive_dir, exist_ok=True)
    destination_path = os.path.join(archive_dir, filename)
    shutil.move(source_path, destination_path)
    return destination_path


def fix_references_to_archived_file(assistant_dir: str, filename: str) -> dict[str, int]:
    """
    Update all references to point to the archived file location.
    
    This updates references from 'filename' to 'archived/filename' in all files
    across design_logs, operations, and artifacts directories.
    
    Args:
        assistant_dir: Path to the .assistant directory.
        filename: The filename that was archived.
    
    Returns:
        Dictionary mapping file paths to number of replacements made.
    """
    replacements = {}
    archived_reference = f"archived/{filename}"
    
    for dir_name in ["design_logs", "operations", "artifacts"]:
        dir_path = os.path.join(assistant_dir, dir_name)
        
        if not os.path.exists(dir_path):
            continue
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                # Skip the archived file itself
                if file == filename and "archived" in root:
                    continue
                    
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count and replace references
                    # We need to be careful not to replace if it's already archived/filename
                    # Use regex to match filename but not archived/filename
                    pattern = rf'(?<!archived/){re.escape(filename)}'
                    matches = re.findall(pattern, content)
                    count = len(matches)
                    
                    if count > 0:
                        new_content = re.sub(pattern, archived_reference, content)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        replacements[file_path] = count
                        
                except Exception:
                    # Silently skip files that can't be read/written
                    pass
    
    return replacements


def fix_references_within_archived_file(file_path: str) -> int:
    """
    Update references within the archived file to account for its new location.
    
    When a file moves from 'docs/' to 'docs/archived/', we need to update
    any references it makes to sibling files. For example:
    - 'op_1_foo.md' -> '../op_1_foo.md'
    - 'dl_5_bar.md' -> '../dl_5_bar.md'
    
    Args:
        file_path: Path to the archived file.
    
    Returns:
        Number of replacements made.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns for document references that need updating
        # Match patterns like: dl_1_*, op_2_*, art_3_*
        patterns = [
            (r'(?<!\.\./)(dl_\d+_[^\s\)]+\.md)', r'../\1'),  # design logs
            (r'(?<!\.\./)(op_\d+_[^\s\)]+\.md)', r'../\1'),  # operations
            (r'(?<!\.\./)(?<!archived/)(art_\d+_[^\s\)]+)', r'../\1'),  # artifacts
        ]
        
        new_content = content
        total_replacements = 0
        
        for pattern, replacement in patterns:
            matches = re.findall(pattern, new_content)
            if matches:
                new_content = re.sub(pattern, replacement, new_content)
                total_replacements += len(matches)
        
        if total_replacements > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return total_replacements
        
    except Exception:
        return 0


def remove_from_summary(summary_path: str, filename: str) -> bool:
    """
    Remove an entry from the _summary.md file.
    
    Args:
        summary_path: Path to the _summary.md file.
        filename: The filename to remove from the summary.
    
    Returns:
        True if successful, False otherwise.
    """
    if not os.path.exists(summary_path):
        return False
    
    try:
        with open(summary_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter out the line containing this filename
        new_lines = [line for line in lines if f"`{filename}`" not in line]
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return True
    except Exception:
        return False


@mcp.tool()
def archive_document(
    abs_path: str,
    doc_type: Literal["operation", "artifact", "design_log"],
    number: int
) -> GlyphMCPResponse[None]:
    """
    Archive a document by moving it to the archived subdirectory and updating all references.
    
    This tool:
    1. Finds the document by type and number
    2. Moves it to the 'archived' subdirectory within its document type folder
    3. Updates all references TO the archived file (from other docs)
    4. Updates references WITHIN the archived file (adjusts relative paths)
    5. Removes the entry from the _summary.md file
    6. Updates the reference graph
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        doc_type: Type of document to archive - "operation", "artifact", or "design_log".
        number: The document number to archive (e.g., 1 for dl_1_*, 2 for op_2_*).
    
    Returns:
        GlyphMCPResponse indicating success or failure with detailed context.
    """
    response = GlyphMCPResponse[None]()
    
    if not validate_absolute_path(abs_path, response):
        return response
    
    try:
        # Map doc_type to directory name and prefix
        type_mapping = {
            "design_log": ("design_logs", "dl"),
            "operation": ("operations", "op"),
            "artifact": ("artifacts", "art")
        }
        
        if doc_type not in type_mapping:
            response.add_context(f"Invalid doc_type: {doc_type}. Must be 'operation', 'artifact', or 'design_log'.")
            return response
        
        dir_name, prefix = type_mapping[doc_type]
        assistant_dir = os.path.join(abs_path, BASE_NAME)
        doc_dir = os.path.join(assistant_dir, dir_name)
        archive_dir = os.path.join(doc_dir, "archived")
        
        # Check if directory exists
        if not os.path.exists(doc_dir):
            response.add_context(f"Directory not found: {doc_dir}. Please initialize the assistant directory first.")
            return response
        
        # Find the document
        result = find_document_by_number(doc_dir, prefix, number)
        if result is None:
            response.add_context(f"Document not found: {prefix}_{number}_* in {doc_dir}")
            return response
        
        filename, filepath = result
        response.add_context(f"Found document: {filename}")
        
        # Move to archive
        new_path = move_to_archive(filepath, archive_dir, filename)
        response.add_context(f"Moved to archive: {new_path}")
        
        # Update references TO this file from other documents
        replacements = fix_references_to_archived_file(assistant_dir, filename)
        
        if replacements:
            response.add_context(f"Updated references to '{filename}' -> 'archived/{filename}':")
            for ref_file, count in replacements.items():
                rel_path = os.path.relpath(ref_file, abs_path)
                response.add_context(f"  - {rel_path}: {count} replacement(s)")
        else:
            response.add_context(f"No references to '{filename}' found in other documents")
        
        # Update references WITHIN the archived file
        internal_replacements = fix_references_within_archived_file(new_path)
        if internal_replacements > 0:
            response.add_context(f"Updated {internal_replacements} internal reference(s) within the archived file")
        
        # Remove from summary
        summary_path = os.path.join(doc_dir, "_summary.md")
        if remove_from_summary(summary_path, filename):
            response.add_context(f"Removed entry from {dir_name}/_summary.md")
        
        # Update reference graph
        update_response = update_reference_graph(abs_path)
        if not update_response.success:
            response.add_context("Warning: Failed to update reference graph after archiving")
            response.add_context(update_response.context)
        else:
            response.add_context("Reference graph updated successfully")
        
        response.success = True
        response.add_context(f"Successfully archived {doc_type} #{number}")
        
    except Exception as e:
        response.add_context(f"Failed to archive document: {str(e)}")
    
    return response


def find_archived_document_by_number(archive_dir: str, prefix: str, number: int) -> tuple[str, str] | None:
    """
    Find an archived document file by its type and number.
    
    Args:
        archive_dir: Path to the archived directory to search in.
        prefix: The file prefix (e.g., 'dl', 'op', 'art').
        number: The document number to find.
    
    Returns:
        A tuple of (filename, filepath) if found, None otherwise.
    """
    if not os.path.exists(archive_dir):
        return None
    
    pattern = re.compile(rf'^{prefix}_{number}_.*')
    
    for filename in os.listdir(archive_dir):
        if pattern.match(filename) and os.path.isfile(os.path.join(archive_dir, filename)):
            return filename, os.path.join(archive_dir, filename)
    
    return None


def move_from_archive(source_path: str, destination_dir: str, filename: str) -> str:
    """
    Move a file from the archive directory back to the main directory.
    
    Args:
        source_path: Path to the archived file.
        destination_dir: Path to the destination directory.
        filename: Name of the file.
    
    Returns:
        The new file path in the destination directory.
    """
    destination_path = os.path.join(destination_dir, filename)
    shutil.move(source_path, destination_path)
    return destination_path


def fix_references_from_archived_file(assistant_dir: str, filename: str) -> dict[str, int]:
    """
    Update all references from 'archived/filename' back to just 'filename' in all files.
    
    Args:
        assistant_dir: Path to the .assistant directory.
        filename: The filename that is being unarchived.
    
    Returns:
        Dictionary mapping file paths to number of replacements made.
    """
    replacements = {}
    archived_reference = f"archived/{filename}"
    
    for dir_name in ["design_logs", "operations", "artifacts"]:
        dir_path = os.path.join(assistant_dir, dir_name)
        
        if not os.path.exists(dir_path):
            continue
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace archived/filename with just filename
                    count = content.count(archived_reference)
                    
                    if count > 0:
                        new_content = content.replace(archived_reference, filename)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        replacements[file_path] = count
                        
                except Exception:
                    # Silently skip files that can't be read/written
                    pass
    
    return replacements


def fix_references_within_unarchived_file(file_path: str) -> int:
    """
    Update references within the unarchived file to remove the '../' prefix.
    
    When a file moves from 'docs/archived/' back to 'docs/', we need to update
    any references it makes to sibling files. For example:
    - '../op_1_foo.md' -> 'op_1_foo.md'
    - '../dl_5_bar.md' -> 'dl_5_bar.md'
    
    Args:
        file_path: Path to the unarchived file.
    
    Returns:
        Number of replacements made.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Patterns to reverse the archiving changes
        # Match patterns like: ../dl_1_*, ../op_2_*, ../art_3_*
        patterns = [
            (r'\.\.\/(dl_\d+_[^\s\)]+\.md)', r'\1'),  # design logs
            (r'\.\.\/(op_\d+_[^\s\)]+\.md)', r'\1'),  # operations
            (r'\.\.\/(art_\d+_[^\s\)]+)', r'\1'),  # artifacts
        ]
        
        new_content = content
        total_replacements = 0
        
        for pattern, replacement in patterns:
            matches = re.findall(pattern, new_content)
            if matches:
                new_content = re.sub(pattern, replacement, new_content)
                total_replacements += len(matches)
        
        if total_replacements > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return total_replacements
        
    except Exception:
        return 0


@mcp.tool()
def unarchive_document(
    abs_path: str,
    doc_type: Literal["operation", "artifact", "design_log"],
    number: int,
    short_desc: Optional[str] = None
) -> GlyphMCPResponse[None]:
    """
    Unarchive a document by moving it back from the archived subdirectory and updating all references.
    
    This tool:
    1. Finds the archived document by type and number
    2. Moves it from the 'archived' subdirectory back to the main folder
    3. Updates all references TO the file (from 'archived/filename' to 'filename')
    4. Updates references WITHIN the file (removes '../' prefixes)
    5. Optionally adds the entry back to the _summary.md file
    6. Updates the reference graph
    
    Args:
        abs_path: The absolute path of the project's root where the .assistant folder is located. Absolute path is required.
        doc_type: Type of document to unarchive - "operation", "artifact", or "design_log".
        number: The document number to unarchive (e.g., 1 for dl_1_*, 2 for op_2_*).
        short_desc: Optional short description to add back to the _summary.md file. If not provided, the entry is not added to the summary.
    
    Returns:
        GlyphMCPResponse indicating success or failure with detailed context.
    """
    response = GlyphMCPResponse[None]()
    
    if not validate_absolute_path(abs_path, response):
        return response
    
    try:
        # Map doc_type to directory name and prefix
        type_mapping = {
            "design_log": ("design_logs", "dl"),
            "operation": ("operations", "op"),
            "artifact": ("artifacts", "art")
        }
        
        if doc_type not in type_mapping:
            response.add_context(f"Invalid doc_type: {doc_type}. Must be 'operation', 'artifact', or 'design_log'.")
            return response
        
        dir_name, prefix = type_mapping[doc_type]
        assistant_dir = os.path.join(abs_path, BASE_NAME)
        doc_dir = os.path.join(assistant_dir, dir_name)
        archive_dir = os.path.join(doc_dir, "archived")
        
        # Check if archived directory exists
        if not os.path.exists(archive_dir):
            response.add_context(f"Archived directory not found: {archive_dir}")
            return response
        
        # Find the archived document
        result = find_archived_document_by_number(archive_dir, prefix, number)
        if result is None:
            response.add_context(f"Archived document not found: {prefix}_{number}_* in {archive_dir}")
            return response
        
        filename, filepath = result
        response.add_context(f"Found archived document: {filename}")
        
        # Move from archive back to main directory
        new_path = move_from_archive(filepath, doc_dir, filename)
        response.add_context(f"Moved from archive: {new_path}")
        
        # Update references TO this file from other documents
        replacements = fix_references_from_archived_file(assistant_dir, filename)
        
        if replacements:
            response.add_context(f"Updated references from 'archived/{filename}' -> '{filename}':")
            for ref_file, count in replacements.items():
                rel_path = os.path.relpath(ref_file, abs_path)
                response.add_context(f"  - {rel_path}: {count} replacement(s)")
        else:
            response.add_context(f"No references to 'archived/{filename}' found in other documents")
        
        # Update references WITHIN the unarchived file
        internal_replacements = fix_references_within_unarchived_file(new_path)
        if internal_replacements > 0:
            response.add_context(f"Updated {internal_replacements} internal reference(s) within the unarchived file")
        
        # Add back to summary if description provided
        if short_desc:
            summary_path = os.path.join(doc_dir, "_summary.md")
            success, message = append_to_summary(summary_path, filename, short_desc)
            if success:
                response.add_context(f"Added entry back to {dir_name}/_summary.md")
            else:
                response.add_context(f"Warning: {message}")
        else:
            response.add_context("No description provided, skipping summary update")
        
        # Update reference graph
        update_response = update_reference_graph(abs_path)
        if not update_response.success:
            response.add_context("Warning: Failed to update reference graph after unarchiving")
            response.add_context(update_response.context)
        else:
            response.add_context("Reference graph updated successfully")
        
        response.success = True
        response.add_context(f"Successfully unarchived {doc_type} #{number}")
        
    except Exception as e:
        response.add_context(f"Failed to unarchive document: {str(e)}")
    
    return response
