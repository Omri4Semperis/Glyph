In this prompt:

[phase_number] = {{phase_number}}
[task_display] = {{task_display}}
[operation_document] = {{operation_document}}
[additional_context] = {{additional_context}}

# Your mission

Plan/Implement Phase [phase_number] / [task_display] from [operation_document].

**Mode:** If you're in Planning mode, create a detailed plan and wait for approval. If you're in Implementation mode, proceed with execution.

## Before you start

1. Check if the task is still relevant. This is a living project—if it's changed significantly, inform me before proceeding.
2. Read the Background section of the operation document.
3. Read previous task/phase bottom lines and lessons learned, if any.
4. [additional_context]
5. If you find any ambiguities, inconsistencies, or missing information in the task description, ask me for clarification.
6. Check if something you're about to implement already exists and can be reused or slightly adapted. If so, let me know before proceeding.

## Planning principles (for Planning mode)

1. **Reuse over creation:** Check if reusable/adaptable solutions exist, but only if it doesn't add unnecessary complexity. If creating something new is simpler—do that instead.
2. **Balance SOLID, DRY, and KISS:** Do not overengineer. For complex tasks, explain how you'll keep them simple.
3. **Clarify ambiguity:** If the task description is unclear, ask me with specific options (e.g., "A, B, or C?"). Avoid assumptions.

## Define your plan (for Planning mode)

Create a detailed plan for [phase_number] / [task_display] which includes:

- **Current state:** Brief description of the current situation
- **Objectives:** What the task aims to achieve
- **Steps:** Clear sequence of actions. Start with benchmarking (warnings, errors, test fails). End with cleanup and verification (no new warnings/errors, tests pass). Final action: generate commit message format shown below.
- **Dependencies:** Prerequisites or external factors
- **Risk Assessment:** Possible risks and mitigation strategies (free-text paragraph)

**Getting feedback:**

- For **complex plans** (anything beyond straightforward steps): Present with enumerated options and wait for approval
- For **straightforward plans:** Simply ask for go-ahead

## How to implement (for Implementation mode)

1. Identify relevant documents and read them (use Glyph tools if needed to find related materials).
2. Build and run all tests to establish a benchmark (if applicable).
3. Implement the task, adhering to SOLID, DRY, and KISS principles.
4. Build/Run tests and compare to benchmark (if applicable).

## After completion (both modes)

1. Checkmark [x] the task(s) in the task list in the document if applicable.
2. If this is the last task of the phase, verify that the phase's D.O.D. checklist is complete and mark [x] on done items.
3. Add lessons learned / bottom line for this task/phase in the document (succinct; skip obvious items. e.g., No need to mention success as it's the norm).
4. Consider future phases/tasks. If you discovered something affecting them, add a comment to the relevant task/phase.
5. Generate a commit message (base it on what you actually did, not just the task description. If you deviated, reflect that in the message):

```txt
[operation name] P-[phase_number]/T-[task_display] - <short task title>: Description of actual change
```

## Updating documentation with lessons learned

When planning/implementing a phase/task, new lessons may be learned or important actions may be taken which influence more than just the current thing the assistant is doing. If such knowledge is achieved, then update the documentation in the correct place. The places are:

- **If the info is relevant to a future phase in the same operation:** Update it in the "Phase Lessons Learned" section of that future phase.
- **If the info is relevant to a future task in the same operation:** Update it in the comments or relevant section of that future task.
- **If the knowledge is relevant for the whole current operation:** Add it in the "Lessons Learned during Operation" section of that operation.
- **If the info is relevant to a future step of the design log from which this operation was born:** Update it in that future step.
- **If the info is relevant to the entire design log from which this operation was born:** Update it in the place of the DL meant for general lessons learned.

Updating is important both **forward** (so that future implementers see the comment) but also **backwards** (on past tasks/phases/steps—so that it's clear that something happened later which might influence done achievements).