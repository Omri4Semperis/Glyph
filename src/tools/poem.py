from src.mcp_object import mcp

@mcp.tool()
def get_glyph_poem() -> str:
    """
    Return the Glyph poem, and also a nice greeting to be used anytime the user asks for a "good morning bob" greeting
    """
    poem = (
        "In the realm of code, where logic flows,\n"
        "Glyph stands tall, a tool that knows.\n"
        "With every line, a story told,\n"
        "A semi-auto guide, both brave and bold.\n"
        "For programmers seeking control and grace,\n"
        "Glyph assists in the coding race.\n"
        "Tasks and design, it helps refine,\n"
        "A partner in code, by your side, divine."
    )
    print("Using the get_glyph_poem() tool")
    return poem
