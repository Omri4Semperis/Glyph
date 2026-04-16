# Glyph overview

Glyph is an MCP that helps developers manage long-term tasks and projects with AI assistance while maintaining full control. It provides structured documentation through design logs (implementation decisions), operations (task checklists), and artifacts (persisted outputs), all linked together in a traceable reference graph.

## Primitives

- **Design Log**: Markdown file documenting implementation decisions and details. Immutable once created. Stored in `.assistant/design_logs/` as `dl_{number}_{title}.md`
- **Operation**: Checklist for achieving complex goals, broken into phases and tasks. Stored in `.assistant/operations/` as `op_{number}_{title}.md`
- **Artifact**: Important files persisted from `ad_hoc/` directory. Stored in `.assistant/artifacts/` as `art_{number}_{filename}.ext`
- **Ad-hoc Directory**: Temporary workspace (`.assistant/ad_hoc/`) for experiments and intermediate work. Reset between operations.
- **Reference Graph**: CSV file tracking all references between design logs, operations, and artifacts

## Directory Structure

Initializing Glyph via `init_assistant_dir` creates this structure:

```text
.assistant/
├── ad_hoc/                    # Temporary workspace for intermediate files
├── artifacts/                 # Persisted important files
│   ├── _summary.md           # Summary of all artifacts with descriptions
│   └── archived/             # Archived artifacts
├── design_logs/              # Design decisions and implementation plans
│   ├── _summary.md           # Summary of all design logs with descriptions
│   └── archived/             # Archived design logs
├── operations/               # Task checklists and operations
│   ├── _summary.md           # Summary of all operations with descriptions
│   └── archived/             # Archived operations
└── reference_graph.csv       # Tracks all cross-references between documents
```

**File naming conventions:**

- Design logs: `dl_{number}_{title}.md` (e.g., `dl_1_Authentication_Design.md`)
- Operations: `op_{number}_{title}.md` (e.g., `op_1_Database_Migration.md`)
- Artifacts: `art_{number}_{filename}.ext` (e.g., `art_1_config_template.json`)

**Summary files:**
Each directory contains a `_summary.md` with a quick overview of all documents and descriptions, auto-updated on creation.

**If the directory structure is corrupted:**
Reinitialize with `init_assistant_dir` using `overwrite=True`—this backs up the existing `.assistant` directory and creates a fresh structure.

## Reference Syntax

Link files using standard markdown syntax:

```markdown
[dl_1](.assistant/design_logs/dl_1_title.md)
[op_2](.assistant/operations/op_2_title.md)
[art_3](.assistant/artifacts/art_3_name.ext)
```

Or use descriptive text: `[See design for X](.assistant/design_logs/dl_1_title.md)`

### Tip: Use Mermaid Diagrams

For complex relationships or structures, use Mermaid diagrams instead of written explanations—visual diagrams are clearer, especially for workflows, dependencies, or hierarchies.

## Core Structural Principle

**Design logs should be linked to operations or artifacts.** Every design log should ideally reference or be referenced by at least one operation or artifact. This creates:

- A coherent knowledge graph with minimal orphaned documents
- Clear traceability from work (operations) to implementation decisions (design logs)
- Better categorization and context for documentation
- More meaningful reference graphs reflecting project structure

Not a strict requirement—if a design log has no immediate connection, consider linking it later.

## Scope & Independence

- Phases are organizational units. Group tasks by shared context, subsystem, or milestone rather than by presumed agent-session size.
- Tasks are the atomic execution checkpoints. After each task, the project should be in a working, verifiable state.
- Execution granularity is chosen by the user at runtime. The same operation should support delegating a whole phase or a single task.
- Task boundaries should support cold re-entry. A fresh agent should be able to continue by reading the operation background, phase background, and task background plus any checked subtasks and lessons learned.
- Small subtasks improve reviewability. The usual low file-count expectation on subtasks exists primarily to keep code review checkpoints quick and reliable.

## Working with the Ad Hoc Directory

The `.assistant/ad_hoc` directory is a workspace for temporary files created during operations.

### Purpose

- Store intermediate work products
- Hold files that may or may not have lasting value
- Provide a scratch space during active work

### Best Practices

1. **Use ad hoc for temporary work:** Files that might be discarded or are only relevant to the current task belong in `ad_hoc`.

2. **Persist valuable files:** If an ad hoc file has lasting significance:
   - Use `persist_artifacts` to move it to the `artifacts` directory
   - Ensures proper naming (`art_{number}_{name}`) and permanent storage
   - Persisted artifacts can be referenced by design logs and operations
   - **Link related design logs to the persisted artifact** to maintain structural integrity

3. **Clean up regularly:** Files in `ad_hoc` may be cleaned up between sessions—don't rely on them for long-term storage.

4. **When to persist:**
   - Documents important findings
   - Will be referenced by future work
   - Contains reusable templates, scripts, or configurations
   - Represents a deliverable or milestone

5. **When NOT to persist:**
   - Temporary debugging outputs
   - Superseded draft files
   - Test files that served their purpose
   - Single-session experimentation files

## Typical Workflow

1. **Init** → `init_assistant_dir` sets up the `.assistant` structure
2. **Work** → `add_operation` documents what you're doing
3. **Design** → `add_design_log` captures implementation decisions/findings (link to your operation)
4. **Produce** → Create files in `ad_hoc`, then `persist_artifacts` for keepers
5. **Connect** → Reference design logs from operations, operations from artifacts
6. **Verify** → `update_reference_graph` to visualize relationships
7. **Query** → Use `get_references_from` / `find_references_to` to navigate structure

**Key insight:** Design logs should reference or be referenced by operations/artifacts. Use reference tools to verify the knowledge graph is coherent.

## Communication Guidelines

If something is unclear or ambiguous, ask for clarification.
