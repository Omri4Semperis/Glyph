# Assets Restructure Summary

## Changes Made

### 1. Assets Directory Restructured

The flat `assets/` directory has been reorganized into logical subdirectories:

```txt
assets/
├── skills/           # Skills-related documentation
│   └── _how_to_glyph.md
├── rules/            # Rules and guidelines
│   ├── design_log_rules.md
│   ├── operation_rules.md
│   └── read_before_task_planning_and_implementation.md
├── templates/        # Templates for creating documents
│   ├── dl_template.md
│   ├── operation_doc_template.md
│   └── operation_template.md
├── examples/         # Example files
│   ├── dl_example_implementation.md
│   └── dl_example_research.md
└── prompts/          # Prompt text templates (NEW)
    ├── compact_conversation.md
    ├── create_an_operation_doc.md
    └── implementation_command.md
```

### 2. Prompts Converted to Markdown

All hardcoded prompt strings in `src/prompts/*.py` have been extracted to markdown files in `assets/prompts/`:

- `compact_conversation.py` → reads from `compact_conversation.md`
- `create_an_operation_doc.py` → reads from `create_an_operation_doc.md` (with parameter substitution)
- `implement_command.py` → reads from `implementation_command.md` (with parameter substitution)

The Python files are now thin wrappers that read the markdown and perform parameter substitution using `.format()`.

### 3. `read_asset` Function Enhanced

Updated `src/read_an_asset.py` to:

- Search recursively through all subdirectories
- **Detect duplicate filenames** - if multiple files have the same name, returns an informative error with:
  - Number of matches found
  - Relative path of each matching file
  - Preview of first 5 lines of each file
  - Recommendation to use `read_asset_exact()`

### 4. New `read_asset_exact` Function and MCP Tool

Added `read_asset_exact(relative_path)` for precise file access:
- Accepts a relative path from assets root (e.g., `'prompts/compact_conversation.md'`)
- Exposed as an MCP tool via `src/skills/read_asset_exact.py`
- Cross-platform compatible (normalizes path separators)

Example:
```python
# If read_asset("config.md") finds duplicates, use:
content = read_asset_exact("rules/config.md")
```

### 5. No Changes to Existing Callers

All existing callers (`src/skills/_utils.py`, `src/skills/*.py`) continue to work without modification because `read_asset` still accepts just a filename and finds it automatically.

## Benefits

1. **Better Organization**: Assets are now categorized by type
2. **Easier Maintenance**: Prompt text can be edited without touching Python code
3. **Improved Readability**: Python prompt files are now much cleaner
4. **Backward Compatible**: Existing code continues to work
5. **Scalable**: Easy to add new assets in the appropriate subdirectory
6. **Robust Duplicate Handling**: Clear error messages and resolution path when duplicate filenames exist

## Testing

The MCP server starts successfully, confirming:

- All imports work correctly
- File paths are resolved properly
- The recursive search function works as expected