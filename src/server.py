if __name__ == "__main__":
    try:
        from mcp_object import mcp

        from prompts.compact_conversation import compact_conversation

        from tools.init_assistant_dir import init_assistant_dir
        from tools.md_to_dict import md_to_dict
        from tools.get_dl_example_research import get_dl_example
        from tools.get_dl_rules import get_dl_rules
        from tools.add_design_log import add_design_log

        print("Starting MCP server...")

        mcp.run()
    except KeyboardInterrupt:
        print("MCP server stopped by user.")
        pass
