import os
from response import GlyphMCPResponse


def _get_assets_dir() -> str:
    """Returns the absolute path to the assets directory."""
    return os.path.join(os.path.dirname(__file__), '..', 'assets')


def _get_file_preview(file_path: str, num_lines: int = 5) -> str:
    """Returns the first few lines of a file for preview."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = []
            for i, line in enumerate(file):
                if i >= num_lines:
                    break
                lines.append(line.rstrip())
            return '\n'.join(lines)
    except Exception:
        return "(Could not read preview)"


def _find_all_matches(filename: str) -> list[tuple[str, str]]:
    """
    Find all files matching the given filename in assets directory.
    
    Returns:
        List of tuples: (relative_path_from_assets, absolute_path)
    """
    assets_dir = _get_assets_dir()
    matches = []
    
    for root, dirs, files in os.walk(assets_dir):
        if filename in files:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, assets_dir)
            matches.append((rel_path, abs_path))
    
    return matches


def read_asset(filename: str) -> str:
    """
    Reads the content of a file from the assets directory.
    Searches recursively through all subdirectories to find the file.
    
    Args:
        filename: The name of the file to read (e.g., 'example.txt').
    
    Returns:
        The content of the asset file as a string.
    
    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If multiple files with the same name exist.
    """    
    matches = _find_all_matches(filename)
    
    if len(matches) == 0:
        raise FileNotFoundError(f"Asset file '{filename}' not found in assets directory or any subdirectory.")
    
    if len(matches) == 1:
        rel_path, abs_path = matches[0]
        with open(abs_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    # Multiple matches found - provide helpful error
    error_lines = [
        f"Multiple assets named '{filename}' found ({len(matches)} matches).",
        "",
        "Please use read_asset_exact() with the relative path instead:",
        ""
    ]
    
    for rel_path, abs_path in matches:
        preview = _get_file_preview(abs_path)
        error_lines.append(f"  Path: {rel_path}")
        error_lines.append(f"  Preview:")
        for line in preview.split('\n'):
            error_lines.append(f"    | {line}")
        error_lines.append("")
    
    error_lines.append(f"Example: read_asset_exact('{matches[0][0]}')")
    
    raise ValueError('\n'.join(error_lines))


def read_asset_exact(relative_path: str) -> str:
    """
    Use this function when multiple files have the same name and you need to specify
    which one to read, or when you know the exact location of the file.
    
    Args:
        relative_path: The path relative to the assets directory 
                      (e.g., 'prompts/compact_conversation.md' or 'rules/design_log_rules.md').
    
    Returns:
        The content of the asset file as a string.
    
    Raises:
        FileNotFoundError: If the file is not found at the specified path.
    """    
    assets_dir = _get_assets_dir()
    file_path = os.path.join(assets_dir, relative_path)
    
    # Normalize path separators for cross-platform compatibility
    file_path = os.path.normpath(file_path)
    
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Asset file '{relative_path}' not found. Ensure the path is relative to the assets directory.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
