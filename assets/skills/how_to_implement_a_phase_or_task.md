# Things to keep in mind during tasks work

## Pre-Implementation

- **Important:** The codebase may change during or between phases. Before each task, review the current codebase to determine if the task is still valid or needs adjustment (if so, stop and inform the user).
- **Establish a baseline:** Any code-changing task (not research/documentation) must start with a build/run/test verification to establish a baseline. Note all warnings and errors.
- **Check for reusability:** Check whether existing code can be reused or adapted before proceeding.

## Implementation Principles

- **Keep It Simple**: Avoid unnecessary complexity. Keep implementation straightforward.
- **SOLID principles**: Adhere to good software design (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
- **Testing is Integral**: Testing is not a separate phase—it's part of every task. Each implementation must include tests for new/changed code—never defer or group into a dedicated testing phase. Examples: unit, integration, performance, cross-browser, end-to-end, and stress tests.

## Post-Implementation

- **Verify with baseline:** Repeat the build/run/test verification. Compare warnings and errors to the baseline to ensure no regressions.
- **Mark completion:** Mark all completed subtasks, tasks, and phases with `[x]` in their respective checklists, task lists, overview, and D.O.D. sections.
- **Phase verification:** If a task is the last in a phase, verify the phase D.O.D. checklist is complete and mark all done items with `[x]`.
- **Document concisely:** Update lessons learned and bottom lines as applicable (see below).
- **Provide commit message:** Once done, provide a commit message:

  ```txt
  [operation name] P-[phase_number]/T-[task_number] - <short task title>: <actual changes made>
  ```

## Documentation Guidelines

- **Keep operation docs and design logs lean:** Avoid bloat. Keep content concise and focused on actionable information.
- **Lessons learned must be non-trivial:** Only document insights that impact future work or decisions. Exclude:
  - Successful implementations (assumed to be the norm)
  - Trivial observations or obvious outcomes
  - Lengthy narratives or blow-by-blow accounts
- **Proactive annotations:** When discovering information relevant to other tasks/phases, add comments to those sections—both backward (past phases) and forward (future ones).
- **Reference guidelines:** If a discovery should be reflected in design logs or future operations, update those docs with a comment.

## Dynamic Updates

During implementation, new information may require updates to the operation document:

- New tasks may be added dynamically. New phases may NOT be added.
- Lessons learned or actions impacting future steps should be added to the relevant sections so the next implementer is informed.
