# Glyph

**An AI-powered MCP for managing long-term development tasks and projects while maintaining full control over your work.**

Glyph is a Model Context Protocol (MCP) server designed to help developers organize complex, multi-step projects with the power of AI assistance. It provides structured primitives for tracking design decisions, managing operations, and maintaining project artifacts—all while keeping you in complete control.

## ✨ Features

- **Design Logs** - Immutable, sequential records of design decisions and architectural changes
- **Operations** - Structured checklists with phases, tasks, and dependencies for complex goals
- **Artifacts** - Persistent project files with built-in versioning and traceability
- **Reference Graph** - Automatic dependency tracking between all project components
- **AI Integration** - Works seamlessly with Claude as an MCP server in VS Code
- **Audit Trail** - Complete, immutable history of project evolution

## 🚀 Installation

### Prerequisites

- Python 3.x
- UV package manager
- VS Code with Claude extension

### Setup

1. Add Glyph to your VS Code MCP configuration:

   Open or create `.vscode/settings.json` and add the following to your MCP settings, or edit your `mcp.json` directly:

   ```json
   "Glyph": {
     "type": "stdio",
     "command": "uv",
     "args": [
       "run",
       "--directory",
       "C:\\Users\\YourUsername\\OneDrive - Semperis\\Desktop\\Glyph\\src",
       "python",
       "server.py"
     ]
   }
   ```

   > **Note:** Update the path to match your actual Glyph installation directory.

2. Restart VS Code to activate the MCP

3. Start using Glyph tools in your Claude conversations!

## 📖 Core Concepts

### Design Log

A design log is an immutable markdown record that documents a step in your development process. It includes:

- Background and problem description
- Q&As and approaches considered
- Overview of tasks
- Decisions made
- Lessons learned

**Key principle:** Design logs cannot be modified after creation. Each new change creates a new design log, ensuring a fully traceable and auditable development history.

Design logs are stored in `.assistant/design_logs/` with filenames like `dl_1_title.md`, `dl_2_title.md`, etc.

### Operation

An operation is a checklist for achieving a complex goal. It consists of:

- **Background** - Overview of the entire operation
- **Mermaid Chart** - Visual representation of phases and task dependencies
- **Up to 4 Phases** - Each with background, definition of done, and tasks

#### Phase Structure

- **Background** - Describes the current state and desired outcome
- **Definition of Done** - Small checklist of completion criteria
- **Up to 4 Tasks** - Each contributing to the phase goal

#### Task Structure

- **Background** - Context, current state, and desired outcome
- **Files Involved** - List of files to be modified, created, or deleted
- **Subtasks** - Up to 5 checklist items with clear, manageable scope
- **Lessons Learned** - Key takeaways from task completion

> **Note:** Ideally, projects should be in a working state before and after each task.

### References

References link design logs, operations, and artifacts together, creating a dynamic, interconnected knowledge base.

**Reference syntax:**

```markdown
[dl_1](.assistant/design_logs/dl_1_title.md) - Design log reference
[op_2](.assistant/operations/op_2_title.md) - Operation reference
[art_3](.assistant/artifacts/art_3_name.ext) - Artifact reference
[Custom text](.assistant/design_logs/dl_1_title.md) - Descriptive text
```

### Artifacts

Artifacts are files persisted from the ad-hoc directory with built-in versioning. They're stored in `.assistant/artifacts/` with filenames like `art_1_name.ext`.

### Ad-hoc Directory

A temporary workspace for experiments and files that don't fit into the structured system. Use the persist tool to save important files as artifacts.

### Reference Graph

An automatically maintained CSV file (`.assistant/reference_graph.csv`) that maps all dependencies and references across your project components.

## 🛠️ Usage

Use Glyph's tools in Claude conversations to:

- Initialize a new project workspace
- Create design logs to document decisions
- Create operations to organize complex work
- Add artifacts for persistent project files
- Generate code reviews and design documentation

## 📦 Project Structure

```txt
.assistant/
├── design_logs/     - Immutable design log records
├── operations/      - Operation checklists
├── artifacts/       - Persisted project files
├── ad_hoc/         - Temporary workspace
└── reference_graph.csv - Dependency map
```
