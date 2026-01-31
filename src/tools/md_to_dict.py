from typing import Dict
from markdown_it import MarkdownIt

from src.mcp_object import mcp

@mcp.tool()
def md_to_dict(file_path: str) -> Dict[str, str]:
    """
    Parses a Markdown file into a dictionary using top-level headers as keys.
    
    Args:
        file_path: Path to the .md file.
        
    Returns:
        A dictionary where keys are header text and values are the content below.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    md = MarkdownIt()
    tokens = md.parse(md_text)
    
    result = {}
    current_key = None
    content_buffer = []

    for token in tokens:
        if token.type == "heading_open" and token.tag == "h1":
            # Save previous section
            if current_key:
                result[current_key] = "".join(content_buffer).strip()
                content_buffer = []
            
            # Find the next inline token for the header text
            current_key = None 
        elif token.type == "inline" and current_key is None:
            current_key = token.content
        elif token.type not in ["heading_open", "heading_close"]:
            if token.content:
                content_buffer.append(token.content)

    # Catch last section
    if current_key:
        result[current_key] = "".join(content_buffer).strip()

    return result