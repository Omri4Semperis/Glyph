# Things to keep in mind during task planning and implementation

When planning and implementing tasks, adhere to the following guidelines to ensure consistency, quality, and maintainability:

## Pre-Implementation

- **Important:** The documentation doesn't live in a vacuum. It's possible that during implementation or between phases the codebase would change. Therefore, the first subtask of each task should be to review the current codebase and determine whether the task is still valid as is, or whether it needs to be adjusted (in which case—stop execution and inform the user).
- **Establish a baseline:** Any code-changing task (i.e., not research or documentation tasks) must start with a comprehensive build, run, and test verification to establish a baseline. Note all warnings and errors.
- **Check for reusability:** Determine whether the task might reuse or adapt existing solutions before proceeding.

## Implementation Principles

- **KISS (Keep It Simple, Stupid)**: When planning and implementing, avoid unnecessary complexity. Each phase and task should be as straightforward as possible.
- **SOLID principles**: Keep each task adhering to the principles of good software design (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
- **Testing is Integral**: Testing is not a separate phase or task—it is part of every task and phase. Each phase should include explicit testing subtasks that verify the phase's work. Testing should never be deferred or grouped into a dedicated "testing phase." Examples of testing include: unit tests, integration tests, performance tests, cross-browser testing, end-to-end testing, and stress testing. The type of testing depends on the phase's goals.

## Post-Implementation

- **Verify with baseline:** Perform the same build/run/test verification as at the start. Compare warnings and errors to the baseline to ensure no regressions were introduced.
- **Mark completion:** All completed subtasks (in their checklists), tasks (in task lists), and phases (in phases overview and D.O.D. sections) must be explicitly marked with `[x]`.
- **Phase verification:** If a task is the last in a phase, ensure to verify the phase D.O.D. checklist is complete and mark `[x]` on all done items.
- **Document concisely:** Update lessons learned and bottom lines as applicable (see Documentation Guidelines below).
- **Provide commit message:** Once a task is done, provide the commit message as a ```txt snippet in conventional format:

  ```txt
  [operation name] P-[phase_number]/T-[task_number] - <short task title>: <actual changes made>
  ```

## Documentation Guidelines

- **Keep operation docs and design logs lean:** Avoid unnecessary bloat. Keep content clear, concise, and focused on actionable information.
- **Lessons learned must be non-trivial:** Only document insights that meaningfully impact future work or decisions. Exclude:
  - Successful implementations (assumed to be the norm)
  - Trivial observations or obvious outcomes
  - Lengthy narratives or blow-by-blow accounts
- **Proactive annotations:** When implementing a task and discovering information relevant to future tasks/phases, add comments to those sections so the next implementer will be informed. This applies backward (to past phases) and forward (to future ones).
- **Reference guidelines:** If during implementation you discover something that should be reflected in design logs or future operation docs, update those docs with a comment explaining the discovery.

## Dynamic Updates

During implementation, new information may arise that necessitates updates to the operation document:

- New tasks may be added dynamically. New phases may NOT be added.
- Lessons learned or actions taken during a phase, task, or subtask may impact future steps. In such cases, update the relevant sections with a comment so the next implementer will be informed.
