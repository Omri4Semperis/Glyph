import os

def read_asset(filename) -> str:
    """
    Reads the content of a file from the assets directory.
    
    Args:
        filename (str): The name of the file to read (e.g., 'example.txt').
    
    Returns:
        str: The content of the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there's an error reading the file.
    """
    assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    file_path = os.path.join(assets_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()