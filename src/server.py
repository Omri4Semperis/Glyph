if __name__ == "__main__":
    try:
        from mcp_object import mcp

        from prompts.compact_conversation import compact_conversation

        print("Starting MCP server...")

        mcp.run()
    except KeyboardInterrupt:
        print("MCP server stopped by user.")
        pass
