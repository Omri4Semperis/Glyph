# Your mission

Sync the most critical lessons learned from operation(s) {{operations_list}} back to design log(s) {{design_logs_list}}. Avoid duplicating lessons already present or reasonably assumed in the design logs.

## Tool hints

- Run `update_reference_graph(abs_path)` first so reference data is current.
- You can use `get_references_from(abs_path, file_name)` to discover which design logs an operation points to.
- You can use `find_references_to(abs_path, file_name)` to validate reverse links where needed.

## Process

1. **For each operation document:**
   - Read the entire operation document
   - Extract the most critical "Lessons Learned" from tasks and phases
   - Extract the most critical "Lessons Learned during Operation" section
   - Identify the related design logs from the References section

2. **Categorize lessons:**
   - **General lessons**: Apply to the overall approach or architecture
   - **Step-specific lessons**: Impact a specific step in the design log
   - **Future considerations**: New insights for future features

3. **For each related design log:**
   - Read the current design log content
   - Identify where each lesson should be added:
     - General lessons → Add to "Implementation Results" or new "Lessons Learned" section
     - Step-specific lessons → Add as notes under the relevant step in the Plan
     - Future considerations → Add to "Future Improvements" section or create one

4. **Update design logs:**
   - Add lessons concisely (minimal but clear)
   - Preserve existing content
   - Use clear attribution: "From [op_xxx]: lesson text"
   - Avoid duplicating lessons already present or reasonably assumed

## Output format

For each operation processed, report:

```txt
Operation: <operation_name>
Related Design Log: <design_log_name>
Lessons synced: <count>
- [General] <lesson_summary>
- [Step X] <lesson_summary>
...etc
```

## After syncing

1. Summarize total operations processed and lessons synced
2. Highlight any operations without a linked design log
3. Highlight any design logs that couldn't be updated (file not found, etc.)