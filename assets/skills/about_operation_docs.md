# How to handle an Operation

An operation is a structured plan for implementing a feature or change in the codebase.
It contains background and phases with tasks and subtasks, each with checklists to ensure quality and completeness.

Once a template is created using one of the MCP's tools, fill out the operation file before implementation begins.

## Key Guidelines

### Leading principles in creating an operation

- KISS (Keep It Simple, Stupid): Avoid unnecessary complexity. Keep each phase and task straightforward.
- SOLID principles: Each task should adhere to good software design principles.
- Testing is done within subtasks, not as a separate task/phase—it's part of the development process.

### Structure

- Background (include only relevant items):
  - Background Information
  - Problem Statement
  - Goals
  - Approach
  - Constraints
  - Assumptions
  - Definitions
  - References
  - Verification Criteria
  - Mermaid chart showing phases and tasks dependency (if applicable)
- Phases
  - Background for each phase (shorter than the overall background)
  - Definition of Done (D.O.D.) checklist
  - Tasks
    - Background for each task (specific to the task)
    - A list of files involved, with full paths
    - Subtasks as a checklist
    - Lessons learned for each task

### Phases

- Each phase must have a clear Definition of Done (D.O.D.) checklist.
- If a phase has more than 1 task, add a numberless task verifying D.O.D. completeness. If only one task exists, the D.O.D. check is done within that task.
- D.O.D. verification must be against the actual code, not just crossed-off tasks.
- D.O.D. verification may lead to new tasks if items are incomplete.
- At the end of each phase, the project must be functional and runnable. If not achievable, highlight with ⚠️ in the phase description.

### Tasks

- Each task must have a clear background description.
- Tasks should be as **functionally** atomic as possible.
- List the files involved in each task.
- Subtasks should touch at most 2 files (3 in exceptional cases).
- At the end of each task, the build must pass and all unit/component tests must succeed.
- The first subtask of each task should review the current codebase to determine if the task is still valid or needs adjustment (if so, stop and inform the user).
- For each actionable task (tasks that change code), start with a build/run/test verification to establish a baseline. At the end, repeat to ensure no regressions.
- If a task is the last in a phase, include D.O.D. verification as a subtask.

### Difficulty Levels
  
Phases Overview Requirements:

- The `Phases overview` section of an operation **must** include two elements:
  1. A markdown table with columns: **Phase**, **# Tasks**, **Difficulties**, **Description**. The **Difficulties** column lists each task's difficulty (Breezy|Low|Medium|High|Nightmare) comma-separated (e.g., `Medium, Low, Medium`).
  2. A DAG showing dependencies at the phase and task level. Use a Mermaid `flowchart` with phase `subgraph`s and task nodes labeled `P{n}/T{m}` (e.g., `P1/T1`). This graph must show ordering and cross-phase/task dependencies.

Together these provide a tabular summary and visual dependency map for planning and verification.

Operations include standardized difficulty levels for every task and phase. Use the following scale:

- **Breezy** (0️⃣): Changes to a single existing file, involving just a few (well-defined) line additions, deletions, or modifications.
- **Low** (1️⃣): Changes limited to one or two files, with well-defined and straightforward modifications, or a single file with a focused functionality to add, change, or remove.
- **Medium** (2️⃣): Modifications spanning several files (up to 5), involving moderate complexity—such as adding a new feature, refactoring a module, or implementing a new class/function with dependencies.
- **High** (3️⃣): Significant changes across multiple files (up to 7), introducing new modules, complex refactoring, or integrating external libraries. Requires thorough testing and validation.
- **Nightmare** (4️⃣): Large-scale changes affecting most or all of the 10-file limit, such as major architectural updates, migrating a core component, or replacing a foundational dependency. Demands extensive planning, testing, and debugging.
- **Hell** (5️⃣): Extremely difficult, high risk, requires significant resources and time.

Guidance on applying difficulty levels:

- **Task Difficulty**: Every actionable task must include a `Task Difficulty` label from the scale above, indicating expected scope and testing effort.
- **Phase Difficulty**: Each phase must include a `Phase Difficulty` label—by default the maximum difficulty of its tasks (e.g., if any task is `High`, the phase is at least `High`) unless a different assessment is justified and documented.
- **Testing & Validation**: All difficulty levels imply testing and build/run validation. Higher levels demand broader coverage, integration testing, or manual verification as appropriate.
- **When to escalate**: If a task grows beyond its assigned difficulty during implementation, update `Task Difficulty`, re-evaluate `Phase Difficulty`, and document the reason.

### Dynamic Updates

- If during implementation new prerequisite tasks are identified, document them immediately.
- Lessons learned or actions impacting other phases/tasks should be noted in those affected phases/tasks.
- If during implementation you discover, learn, or do something relevant to other tasks/phases, document it there too so whoever implements them next will see it.

### Validation

- Ensure the build passes and all tests succeed after each task.
- Update relevant documentation to reflect changes.

### Checklist Management

- Cross out completed checklist items (subtasks and D.O.D. items).
- Add new tasks if D.O.D. verification reveals incomplete items.

### General Principles

- Keep descriptions concise.
- Omit details that don't contribute to task understanding.
- Keep it simple—don't over-engineer or prepare for hypothetical scenarios not in current requirements.
