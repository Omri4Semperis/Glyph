# Your mission

Plan/Implement Phase number {{phase_number}} / {{task_display}} from {{operation_document}}

## Before you start

1. Check if the task is still relevant. This is a living project— if it's changed significantly, inform me before proceeding.
2. Read the Background section of the operation document.
3. Read previous task/phase bottom lines and lessons learned, if any.
4. Additional context: {{additional_context}} (if applicable)
5. If you find any ambiguities, inconsistencies, or missing information in the task description, ask me for clarification.
6. Check if something you're about to implement already exists and can be reused or slightly adapted. If so, let me know before proceeding.

## Principles

1. **Reuse over creation:** Check if reusable/adaptable solutions exist, but only if it doesn't add unnecessary complexity. If creating something new is simpler— do that instead.
2. **Balance SOLID, DRY, and KISS:** Do not overengineer. For complex tasks, explain how you'll keep them simple.
3. **Clarify ambiguity:** If the task description is unclear, ask me with specific options (e.g., "A, B, or C?"). Avoid assumptions.

Take into account:

- **Current state:** The existing codebase
- **Objectives:** What the task aims to achieve
- **Dependencies:** Prerequisites or external factors
- **Risk Assessment:** Possible risks and mitigation strategies
- **Steps:** Start with benchmarking (warnings, errors, test fails). End with cleanup and verification (no new warnings/errors, tests pass). Mark completed items (subtasks, tasks and phases) with `[x]`, anywhere in the operation doc that's relevant. Final action: generate commit message format shown below.

## How to implement

1. Identify relevant documents and read them (e.g., design logs, operation docs, previous phases/tasks). Check for relevant lessons learned or bottom lines.
2. **Establish a baseline:** Build, run all tests, and note any warnings/errors (if applicable).
3. Implement while adhering to SOLID, DRY, and KISS principles.
4. **Verify completion:** Build/Run tests again and compare warnings/errors to baseline (if applicable). Nothing new should break.

## After completion

1. **Mark all completed items with [x]:**
   - Checkmark any subtasks that are done in their checklists
   - Checkmark the task(s) in the task list in the operation doc, as well as in the phases overview and D.O.D. sections, if applicable
   - If this is the last task of the phase, verify that the phase's D.O.D. checklist is complete and mark [x] on all done items
2. **Document concisely:** Add lessons learned / bottom line for this task/phase (non-trivial and succinct only; skip obvious items or standard successes).
3. Consider future phases/tasks. If you discovered something affecting them, add a comment to the relevant task/phase.
4. **Generate a commit message** (base it on what you actually did, not just the task description):

```txt
[operation name] P-[phase number]/T-[task or tasks] - <short task title>: Description of actual change
```

## Updating documentation with lessons learned

As you're working, new lessons may be learned or important actions may be taken which influence more than just the current thing you're doing. If such knowledge is achieved, then update the documentation in the correct place:

```md
| Scope | Update Location |
| - | - |
| Future phase in same operation | "Phase Lessons Learned" section of that phase |
| Future task in same operation | Comments or relevant section of that task |
| Whole current operation | "Lessons Learned during Operation" section |
| Future step of source design log | That future step |
| Entire source design log | DL's general lessons learned section |
```

Updating is important both **forward** (for future implementers) but also **backwards** (on past tasks/phases/steps— so it's clear that something happened later which might influence done achievements).

## Final Reminders

- **Read the permanent rules:** Use Glyph's tool get the `how_to_implement_a_phase_or_task.md` skill, which contains the authoritative guidelines for completing tasks.
- **Mark everything as done:** All completed subtasks (in checklists), tasks (in task lists), and phases (in overview and D.O.D. sections) must be marked with `[x]`.
- **Lessons learned must be non-trivial and succinct:** Only document insights that could impact future work. Avoid lengthy narratives or reporting of successful implementations (assumed to be the norm).
- **Benchmark bookends:** Always start with baseline (build/test/warnings) and end with verification (build/test/warnings again) to catch unexpected regressions.
- **Commit message:** Always provide a commit message in the format shown above in the "After completion" section.