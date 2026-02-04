# Glyph MCP Service - Test Runner

## Overview

The `test_runner.py` is an interactive manual testing tool that demonstrates the behavior of the Glyph MCP service. It allows developers to explore and verify the functionality of various tools through 20 different scenarios.

## Purpose

This runner is designed to:
- Show developers how the service behaves in different situations
- Demonstrate error handling and edge cases
- Provide a hands-on walkthrough of the system's capabilities
- Serve as living documentation through executable examples

## Running the Test Runner

```bash
python test_runner.py
```

## How It Works

The test runner creates a **temporary isolated environment** with:
- Mock asset directories with unique and duplicate files
- Test project directories with various configurations
- Sample markdown files for parsing
- Ad-hoc files for artifact persistence testing

All tests use **real function calls** (not mocked logic), so you see the actual behavior of the system. The temporary environment is automatically cleaned up when you exit.

## Available Scenarios

### Asset Reading (1-5)
- **Scenario 1**: Read a unique asset file (success case)
- **Scenario 2**: Read a non-existent asset (error handling)
- **Scenario 3**: Read duplicate asset names (helpful error with recommendations)
- **Scenario 4**: Use `read_asset_exact()` to resolve duplicates (success)
- **Scenario 5**: Use `read_asset_exact()` with invalid path (error)

### Assistant Directory Initialization (6-8)
- **Scenario 6**: Initialize a new assistant directory (success)
- **Scenario 7**: Try to initialize when already exists without overwrite flag
- **Scenario 8**: Initialize with overwrite (creates backup)

### Design Logs (9-10, 20)
- **Scenario 9**: Add a design log to initialized project (success)
- **Scenario 10**: Try to add design log without initialization (error)
- **Scenario 20**: Create multiple design logs showing sequential numbering

### Operations (11)
- **Scenario 11**: Add an operation document (success)

### Artifact Persistence (12-13)
- **Scenario 12**: Persist files from ad_hoc to artifacts directory (success)
- **Scenario 13**: Try to persist non-existent file (error)

### Markdown Processing (14-15)
- **Scenario 14**: Parse markdown file into hierarchical dictionary (success)
- **Scenario 15**: Try to parse non-existent markdown file (error)

### Reference Graph (16-18)
- **Scenario 16**: Update reference graph by scanning files
- **Scenario 17**: Get all files referenced by a specific file
- **Scenario 18**: Find all files that reference a specific file

### Input Validation (19)
- **Scenario 19**: Test path validation (relative vs absolute paths)

## Interactive Menu Options

When you run the test runner, you'll see a menu with these options:

- **Enter a number (1-20)**: Run a specific scenario
- **Enter 'a'**: Run all scenarios sequentially (with pauses between each)
- **Enter 'q'**: Quit the test runner

## Example Session

```
Enter scenario number (or 'a' for all, 'q' to quit): 3

================================================================================
SCENARIO 3: Read Duplicate Asset Names
================================================================================
Description: Attempting to read an asset that exists in multiple locations.
The system should detect this and provide helpful guidance.
--------------------------------------------------------------------------------

Calling: read_asset('duplicate.md')

Result:
--------------------------------------------------------------------------------
Multiple assets named 'duplicate.md' found (2 matches).

Please use read_asset_exact() with the relative path instead:

  Path: location1/duplicate.md
  Preview:
    | # Duplicate in Location 1
    | 
    | This is the first copy.

  Path: location2/nested/duplicate.md
  Preview:
    | # Duplicate in Location 2
    | 
    | This is the second copy in a nested folder.

Example: read_asset_exact('location1/duplicate.md')
--------------------------------------------------------------------------------

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
OBSERVATION: The system detected multiple files and provided:
  1. A clear error message
  2. Previews of each file to help identify the correct one
  3. A recommendation to use read_asset_exact() with the full path
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

## Technical Implementation

### Hybrid Approach
The test runner uses a **hybrid approach** combining:
1. **Real function calls**: All tools are called with actual implementations
2. **Temporary test environment**: Isolated directories prevent affecting real data
3. **Mocking where needed**: Only `_get_assets_dir()` is patched to redirect to test assets

### Key Features
- Automatic setup and teardown of test environment
- Clear scenario headers and formatted output
- Raw output display (as requested)
- OBSERVATION blocks highlighting key behaviors
- Sequential numbering for scenarios

## Best Practices Demonstrated

1. **Isolated Testing**: All tests run in temporary directories
2. **Real Behavior**: Uses actual function implementations, not mocks
3. **Clear Documentation**: Each scenario explains what it demonstrates
4. **Error Scenarios**: Shows both success and failure cases
5. **Interactive Exploration**: Users can run scenarios in any order

## Cleanup

The test runner automatically cleans up all temporary files and directories when you exit, regardless of how you exit (normal quit, Ctrl+C, etc.).

## Future Extensions

Potential additions:
- Add scenarios for more edge cases as they're discovered
- Export scenario results to a report file
- Add timing information for performance testing
- Create comparison tests between versions

## Notes for Developers

- This is a **manual test runner**, not automated unit tests
- It's meant for exploration and demonstration, not CI/CD pipelines
- The output is intentionally raw to show actual system behavior
