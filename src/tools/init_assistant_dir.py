import os
from src.mcp_object import mcp

def create_tree(base_path: str, structure: dict) -> None:
    """
    Create a directory tree based on the provided structure dictionary.
    
    Args:
        base_path: The base path where the tree should be created.
        structure: A dictionary defining the directory structure.
    """
    dir_name = structure.get("dir_name")
    contains = structure.get("contains", [])
    
    current_path = os.path.join(base_path, dir_name)
    os.makedirs(current_path, exist_ok=True)
    
    for item in contains:
        if isinstance(item, dict):
            create_tree(current_path, item)
        elif isinstance(item, str):
            file_path = os.path.join(current_path, item)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("")  # Create an empty file

@mcp.tool()
def init_assistant_dir(p: str) -> bool:
    """
    Initialize the assistant directory at the given path. Recommended to use at the root of the project.
    
    Args:
        p: Path to the assistant directory. Recommended to use at the root of the project.
        
    Returns:
        True if initialization is successful, False otherwise.
    """
    dir_structure = {
        "dir_name": ".assistant",
        "contains": [
            {"dir_name": "ad_hoc"},
            {"dir_name": "artifactos"},
            {"dir_name": "design_logs", "contains": ["summary.md"]},
            {"dir_name": "operations"},
            {"dir_name": "reference_graphs"}
        ]
    }

    try:
        create_tree(p, dir_structure)
        return True
    except Exception as e:
        print(f"Error initializing assistant directory: {e}")
        return False