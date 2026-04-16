# How to handle an Operation

An operation is a structured plan for implementing a feature or change in the codebase.
It contains background and phases with tasks and subtasks, each with checklists to ensure quality and completeness.

Once a template is created using one of the MCP's tools, fill out the operation file before implementation begins.

## Key Guidelines

### Leading principles in creating an operation

- KISS (Keep It Simple, Stupid): Avoid unnecessary complexity. Keep each phase and task straightforward.
- SOLID principles: Each task should adhere to good software design principles.
- Testing is done within subtasks, not as a separate task/phase—it's part of the development process.

### Sizing & Scoping Principles

- Scope phases by cohesion, not by what an agent can finish in one sitting.
- Scope tasks by atomicity: each task should represent one clear code-change goal, and the project should be in a working state afterward.
- Scope subtasks by verifiability: each subtask should be a single checkable action.
- Write task backgrounds for cold re-entry. A fresh agent should be able to read the operation background, phase background, and task background and proceed without relying on sibling tasks.
- Treat the usual counts as smell tests, not rules. Operations will often land around 2-4 phases, 2-4 tasks per phase, and 3-6 subtasks per task, but single-task phases and shorter or longer checklists are valid when they reflect the real work.
- Avoid padding. If removing a task or subtask would lose no meaningful work, it should not exist.

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

- A phase should group tasks that share a subsystem, context, or milestone.
- Each phase must have a clear Definition of Done (D.O.D.) checklist.
- If a phase has more than 1 task, add a numberless task verifying D.O.D. completeness. If only one task exists, the D.O.D. check is done within that task.
- D.O.D. verification must be against the actual code, not just crossed-off tasks.
- D.O.D. verification may lead to new tasks if items are incomplete.
- At the end of each phase, the project must be functional and runnable. If not achievable, highlight with ⚠️ in the phase description.
- Do not split a cohesive phase only because one task is difficult. Execution granularity is chosen at runtime by the user.

### Tasks

- Each task must have a clear background description.
- Tasks are the atomic unit of code change.
- List the files involved in each task.
- Subtasks should touch at most 2 files (3 in exceptional cases); this limit exists primarily for human reviewability.
- At the end of each task, the build must pass and all unit/component tests must succeed.
- The first subtask of each task should review the current codebase to determine if the task is still valid or needs adjustment (if so, stop and inform the user).
- For each actionable task (tasks that change code), start with a build/run/test verification to establish a baseline. At the end, repeat to ensure no regressions.
- If a task is the last in a phase, include D.O.D. verification as a subtask.
- A task may be difficult, but if it shares the same milestone and context as its neighboring tasks, it still belongs in the same phase.

### Difficulty Levels
  
Phases Overview Requirements:

- The `Phases overview` section of an operation **must** include two elements:
  1. A markdown table with columns: **Phase**, **# Tasks**, **Difficulties**, **Description**. The **Difficulties** column lists each task's difficulty (Breezy|Low|Medium|High|Nightmare) comma-separated (e.g., `Medium, Low, Medium`).
  2. A DAG showing dependencies at the phase and task level. Use a Mermaid `flowchart` with phase `subgraph`s and task nodes labeled `P{n}/T{m}` (e.g., `P1/T1`). This graph must show ordering and cross-phase/task dependencies.

Together these provide a tabular summary and visual dependency map for planning and verification.

Operations include standardized difficulty levels for every task and phase. Use the following scale:

- **Breezy** (0️⃣): Mechanical change. It is clear what to do and where to do it, with no meaningful design decisions.
- **Low** (1️⃣): Straightforward change with minor decisions. The codebase already provides the pattern to follow.
- **Medium** (2️⃣): Requires understanding multiple areas or interactions. Some design decisions are needed, but the direction is mostly clear.
- **High** (3️⃣): Significant design decisions, cross-cutting concerns, or shared-infrastructure changes. Mistakes are easy to make and costly to miss.
- **Nightmare** (4️⃣): Architectural or high-risk change with multiple interacting concerns and a high chance of unintended consequences.
- **Hell** (5️⃣): Extreme complexity, ambiguity, or risk. If this rating appears often, the plan likely needs more decomposition or user guidance.

Guidance on applying difficulty levels:

- **Difficulty is a routing signal**: It helps the user decide whether to delegate a whole phase or work task-by-task. It does not define phase boundaries.
- **Judge difficulty by cognitive complexity**: Base it on scope of understanding, decision complexity, risk surface, and novelty. File count is only a rough correlate.
- **Task Difficulty**: Every actionable task must include a `Task Difficulty` label from the scale above, indicating expected complexity and verification effort.
- **Phase Difficulty**: Each phase must include a `Phase Difficulty` label—by default the maximum difficulty of its tasks (e.g., if any task is `High`, the phase is at least `High`) unless a different assessment is justified and documented.
- **Testing & Validation**: All difficulty levels imply baseline build/run/test validation. Higher levels demand broader unit coverage, integration testing, or targeted manual verification as appropriate.
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
