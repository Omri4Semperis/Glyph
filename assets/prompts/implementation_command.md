# Your mission

Plan/Implement Phase number {{phase_number}} / {{task_display}} from #{{operation_document}}

## Before you start

1. Check if the task is still relevant. If the project changed significantly, inform me before proceeding.
2. Read the Background section of the operation document.
3. Read previous task/phase bottom lines and lessons learned, if any.
4. If the task description has ambiguities, inconsistencies, or missing information, ask me for clarification.
5. Check if what you're about to implement already exists and can be reused or adapted. If so, let me know before proceeding.

{{#additional_context}}
Additional context: #{{additional_context}}
{{/additional_context}}

## Principles

1. **Reuse over creation:** Check for reusable/adaptable solutions, but only if it doesn't add unnecessary complexity. If creating something new is simpler, do that instead.
2. **Balance SOLID, DRY, and KISS:** Do not overengineer. For complex tasks, explain how you'll keep them simple.
3. **Clarify ambiguity:** If the task description is unclear, ask me with specific options (e.g., "A, B, or C?"). Avoid assumptions.

Take into account:

- **Current state:** The existing codebase
- **Objectives:** What the task aims to achieve
- **Dependencies:** Prerequisites or external factors
- **Risk Assessment:** Possible risks and mitigation strategies
- **Steps:** Start with benchmarking (warnings, errors, test fails). End with verification (no new warnings/errors, tests pass). Mark completed items with `[x]` anywhere relevant in the operation doc. Final action: generate commit message per format below.

## How to implement

1. Read relevant documents (design logs, operation docs, previous phases/tasks). Check for lessons learned or bottom lines.
2. **Establish a baseline:** Build, run all tests, and note any warnings/errors (if applicable).
3. Implement adhering to SOLID, DRY, and KISS.
4. **Verify completion:** Build/run tests again and compare to baseline (if applicable). Nothing new should break.

## After completion

1. **Mark all completed items with [x]:**
   - Mark completed subtasks in their checklists
   - Mark completed tasks in task lists, phases overview, and D.O.D. sections
   - If the last task of the phase, verify the phase D.O.D. checklist is complete and mark all done items
2. **Document concisely:** Add lessons learned / bottom line (non-trivial and succinct only; skip obvious or standard successes).
3. If you discovered something affecting future phases/tasks, add a comment to the relevant section.
4. **Generate a commit message** (base it on what you actually did, not just the task description):

```txt
[operation name] P-[phase number]/T-[task or tasks] - <short task title>: Description of actual change
```

## Updating documentation with lessons learned

When lessons learned or actions taken influence beyond the current scope, update documentation in the correct place:

```txt
(Scope to comment about) --> (Where to update)
---
(Future phase in same operation) --> ("Phase Lessons Learned" section of that phase)
(Future task in same operation) --> (Comments or relevant section of that task)
(Whole current operation) --> ("Lessons Learned during Operation" section)
(Future step of source design log) --> (That future step)
(Entire source design log) --> (DL's general lessons learned section)
```

Update both **forward** (for future implementers) and **backward** (on past tasks/phases/steps—so it's clear that something happened later that may affect completed work).

## Final Reminders

- **Read the permanent rules:** Use `get_skill("how_to_implement_a_phase_or_task")` for the authoritative implementation guidelines.
- **Benchmark bookends:** Always start with baseline (build/test/warnings) and end with verification to catch regressions.
- **Mark everything as done:** Mark all completed subtasks, tasks, and phases with `[x]`. Update status as you go, not just at the end (❌ Not started, ⏳ In progress, ✅ Done, ⚠️ Done with issues/aborted).
- **Lessons learned must be non-trivial and succinct:** Only document insights impacting future work. Avoid narratives or reporting successful implementations (assumed to be the norm).
- **When outputs are produced:** If important ad-hoc outputs were created, use `persist_artifacts`. If cross-document references changed, run `update_reference_graph`.
- **Commit message:** Always provide a commit message per the format in the After completion section.