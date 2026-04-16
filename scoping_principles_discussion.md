# Glyph Primitive Scoping - Discussion & Conclusions

**Date:** 2026-04-16

## Problem Statement

Glyph currently defines numeric limits for its primitives (up to 4 phases per operation doc, up to 4 tasks per phase, up to 5 subtasks per task, subtasks touching <=2 files), but not the reasoning behind them. The skills files teach agents how to format primitives, not how to size them.

The original intent was to let an agent work a phase independently, or a task when the phase is too complex. But the current flexibility is limited to design-log step count and subtask complexity. We need a principled scoping framework.

## Initial Proposal: "Agent-Completable Units"

The initial proposal was to size each primitive by what an agent can reliably complete in one focused session, and use difficulty ratings to decide between phase-level and task-level execution.

## Self-Critique of That Proposal

1. **"Agent-completable units" is circular and unmeasurable.** "Scope it so an agent can finish it in one session" does not define what a session is. Context windows vary by model, tasks vary by interaction needs, and "losing track" is not a clear threshold.

2. **The recommended ranges are still arbitrary.** Replacing "up to 4" with "2-4" does not derive a principle; it just rephrases the same guess.

3. **The sizing table is post-hoc rationalization.** The scoping questions were written to fit the existing numbers, not to produce them.

4. **The escalation trigger collapses the hierarchy.** If High-difficulty tasks should be delegated per-task rather than per-phase, then an operation author can always turn each hard task into its own phase. Phase and task stop meaning different things.

## The Deeper Issue: Conflating Structure and Execution

The proposal mixes two separate concerns:

- **Structural decomposition** - how to organize the work
- **Execution strategy** - how to assign work to agent sessions

Document structure should not also define execution boundaries. That is what causes the collapse above.

## What Each Primitive Should Actually Mean

### Phase = Cohesion

A phase should be defined by **cohesion**, not execution scope:

> A phase groups tasks that share context, touch the same area of the project, or serve the same sub-goal. At the end of a phase, the project reaches a meaningful, verifiable milestone.

Two hard tasks in the authentication subsystem still belong in one phase if they share context and milestone, even if the agent executes them one at a time. Splitting them only because they are hard loses information:

- The thematic connection disappears
- The shared Definition of Done disappears
- The operation turns into a flat task list with phase wrappers

A phase is valuable because it provides:

- Shared background
- Shared D.O.D.
- Visible grouping that says "these things go together"

### Task = Atomicity

A task is the **atomic unit of code change**. The project must be in a working state after each task.

### Subtask = Verifiability

A subtask is a single checkable action. If it needs sub-items, promote them to subtasks.

The <=2-file guideline exists for **human reviewability**, not agent capability. Glyph includes code review at operation completion and at DL completion. A small subtask diff can be reviewed quickly; a 6-file subtask usually cannot.

## Execution Granularity Is a Runtime Decision - Made by the User

Execution granularity should be chosen by the **user at runtime**, not encoded into the structure. The user sees the difficulty ratings, knows the agent's capability, and decides whether to delegate a whole phase or a single task. The operation doc should support entry at either level:

- **Enter at phase level** - read the phase background, D.O.D., and task descriptions, then execute sequentially. This works when tasks are Low/Medium and share enough context.
- **Enter at task level** - read the operation background, phase background, and one task. This works when a task needs full agent focus or the user is using a weaker model.

Difficulty is therefore a **routing signal**, not a structural rule. "High" should mean "consider delegating task-by-task," not "make this its own phase."

### Cold Re-Entry Must Be a First-Class Concern

Agent failure is normal: sessions time out, models lose context, and users switch agents. The document must support precise re-entry.

That makes **task self-containment** a structural requirement:

- Operation background + phase background + task background must be enough for a fresh agent
- An agent should not need sibling tasks to understand its assignment
- Checked subtasks and lessons learned should explain what changed

This does not require duplicating phase context. It requires writing task backgrounds so that reading operation -> phase -> task is sufficient.

## Revised Primitive Definitions

| Primitive | Defined By | Also Supports | Not Defined By |
|---|---|---|---|
| **Phase** | Cohesion: shared area, sub-goal, and milestone (D.O.D.) | User routing: difficulty signals phase-level vs. task-level delegation | Agent session boundaries |
| **Task** | Atomicity: one clear code-change goal; build passes afterward | Cold re-entry: enough background for a fresh agent | Difficulty or time to complete |
| **Subtask** | Verifiability: one checkable action, typically <=2 files | Human reviewability at code review checkpoints | Agent capability |

## Rethinking Difficulty

The current difficulty scale in `about_operation_docs.md` is mostly file-count based: Breezy = single file, Low = 1-2 files, Medium = up to 5, High = up to 7, Nightmare = up to 10. That conflates scope with complexity. A 2-file auth change can be harder than a 5-file rename.

Because difficulty is the user's routing signal, it should capture the task's **cognitive demand** - what makes an autonomous agent likely to struggle or get it wrong.

### What Difficulty Should Capture

- **Scope of understanding**: one function, one module, or cross-cutting concerns?
- **Decision complexity**: mechanical steps or real design trade-offs?
- **Risk surface**: can mistakes hide from tests, or affect shared state and downstream consumers?
- **Novelty**: is the agent following an existing pattern or inventing a new one?

### Proposed Revised Scale

- **Breezy**: Mechanical change. Clear what to do and where. No design decisions.
- **Low**: Straightforward change with minor decisions. The codebase already has the pattern.
- **Medium**: Requires understanding multiple areas. Some design decisions, but the direction is mostly clear.
- **High**: Significant design decisions. Cross-cutting concerns or shared infrastructure changes.
- **Nightmare**: Architectural change with high risk of unintended consequences and multiple interacting concerns.
- **Hell**: Extreme complexity, ambiguity, and risk. If this appears often, the task probably needs further decomposition.

File count can be a correlate, but not the definition. A mechanical 6-file rename may be Low. A subtle 2-file concurrency change may be Nightmare.

### What This Changes

The difficulty scale in `about_operation_docs.md` should lead with cognitive complexity. File counts should be removed as defining characteristics and, at most, kept as rough correlates.

## Right-Sizing: Avoiding Artificial Inflation

A common failure mode is **padding**: adding tasks or subtasks to make the structure look balanced. Examples:

- A "review existing code to ensure readiness" task when the phase has only one real task
- A "set up the environment" task that adds no meaningful work
- Splitting one naturally atomic change into several tasks just to fill a phase

**Single-task phases are valid.** If a phase is one cohesive milestone with one meaningful task, that is the right structure. It is better than:

- Adding filler tasks
- Merging unrelated work just to avoid a single-task phase

The reverse also applies: do not merge unrelated work into one oversized task just because each piece seems small. If two changes serve different purposes and can be verified independently, they are separate tasks.

**Test:** if removing a task or subtask loses no meaningful work, it is padding.

Padding also hurts execution. Each task adds review, baseline checks, and validation overhead. Filler multiplies that cost and makes the plan harder to review.

## User-Guided Scoping During Operation Creation

The principles above define what makes a good phase or task. They do not remove judgment. The agent creating the operation doc should calibrate the structure with the user.

Before finalizing the decomposition, the agent should ask a few short questions with recommended defaults. For example:

- **Granularity preference**: "I'm planning N phases with roughly M tasks each. Does that fit how you want to delegate this, or would you prefer fewer/more phases?" Recommendation: use the agent's best cohesion-based judgment.
- **Autonomy level**: "Some tasks are High difficulty. Do you want them kept as separate tasks within a phase so you can delegate task-by-task, or are you comfortable delegating the whole phase?" Recommendation: keep them as separate tasks; the user can still delegate the whole phase.
- **Scope calibration**: "Task X could stay whole or split into two smaller tasks. Do you want finer-grained progress tracking, or less overhead?" Recommendation: split when the parts are independently verifiable; keep together when splitting would create artificial seams.

This should be a brief calibration step during operation-doc creation, not a rigid questionnaire. The agent should present a proposed structure so the user reacts to something concrete.

This matters because the remaining judgment calls are exactly where the user has extra context: team norms, comfort with autonomy, and trust in the current model.

## The Glyph Workflow and How Scoping Supports It

These scoping principles support Glyph's workflow:

1. **Design Log creation** - The user and agent create the DL together. The user reviews the plan and approves the structure.
2. **Operation doc creation** - For each DL step, the user reviews phases, tasks, difficulty ratings, and the dependency DAG.
3. **Autonomous execution** - The user delegates a phase or task to an agent based on difficulty and agent capability.
4. **Code review** - The user reviews at operation completion and again at DL completion.

That is why:

- Phases need cohesion for step 2
- Tasks need atomicity for step 3
- Tasks need self-contained backgrounds for cold re-entry in step 3
- Subtasks need the <=2-file constraint for reviewability in step 4
- Difficulty needs to reflect cognitive complexity for routing in step 3

## Conclusions: What Glyph Should Teach

1. **Phases are organizational, not executional.** Group tasks by shared context and milestone, not by what an agent can finish in one go.
2. **Tasks are the atomic unit.** The project must be in a working state after each task.
3. **Tasks must support cold re-entry.** Operation + phase + task background must be enough for a fresh agent.
4. **Execution granularity is a user runtime decision.** Difficulty tells the user whether to delegate a whole phase or route work task-by-task.
5. **Subtask file limits serve human reviewability.** The <=2-file guideline exists for code review checkpoints, not agent capability.
6. **Difficulty should be defined by cognitive complexity.** Scope of understanding, decision complexity, risk surface, and novelty matter more than file count.
7. **Numeric ranges are guidelines, not rules.** 2-4 phases, 2-4 tasks per phase, and 3-6 subtasks per task are smell tests, not hard limits.
8. **Right-size primitives; do not pad.** Single-task phases are fine. Dummy tasks are not.
9. **Failure mid-execution is expected.** Task boundaries are natural recovery points, and lessons learned plus checked subtasks are the breadcrumbs.
10. **Ask the user to calibrate scoping.** The agent should propose a structure and ask a few targeted questions where judgment is required.

## Audit: Where Do the Numeric Limits Actually Appear?

A full read of the `assets/` directory confirms that the "up to 4 phases / up to 4 tasks / up to 5 subtasks" limits appear only in the README. No other asset communicates them to agents or users.

### Skills (what agents read when creating or implementing operations)

| File | Mentions numeric phase/task/subtask limits? | Notes |
|---|---|---|
| `about_operation_docs.md` | **No** | Describes phases, tasks, and subtasks, but gives no count limits. It does include file-count-based difficulty descriptions and the <=2-file subtask guideline. |
| `about_glyph.md` | **No** | Defines primitives and workflow, but no numeric composition limits. |
| `about_design_logs.md` | **No** | No limit on number of plan steps. |
| `how_to_implement_a_phase_or_task.md` | **No** | Says new phases may not be added during execution, but does not limit how many exist initially. |
| `mermaid_tips_and_tricks.md` | **No** | Diagram reference only. |

### Templates (structural blueprints)

| File | Mentions numeric limits? | Notes |
|---|---|---|
| `operation_doc_template.md` | **No** | Shows an example shape but states no maximums. |
| `dl_template.md` | **No** | Shows 3 plan steps, but states no limit. |
| `code_review_template.md` | **No** | Not relevant to operation scoping. |

### Prompts (instructions agents receive)

| File | Mentions numeric limits? | Notes |
|---|---|---|
| `create_an_operation_doc.md` | **No** | Requires the agent to propose a full structured plan (phases/tasks table, DAG, difficulty assignments with justifications) before creating the doc. No count constraints. |
| `create_design_log.md` | **No** | No step-count limits. |
| `implementation_command.md` | **No** | Execution guidance only. |
| `compact_conversation.md` | **No** | Session-summary prompt only. |
| `sync_lessons_learned.md` | **No** | Lesson-syncing workflow only. |
| `code_review.md` | **No** | Not relevant. |

### Examples (reference documents)

| File | Mentions numeric limits? | Notes |
|---|---|---|
| `operation_example.md` | **No** | Shows 3 phases, but does not prescribe a maximum. |
| `dl_example.md` | **No** | Shows 3 plan steps, but does not prescribe a maximum. |
| `code_review_example.md` | **No** | Not relevant. |

### Conclusion of Audit

The README limits are **invisible to agents**. Agents creating operations receive:

1. The `create_an_operation_doc` prompt - no limits
2. The `about_operation_docs` skill - no limits
3. The operation template - no limits
4. The operation example - an example scale, but no prescribed maximum

So agents are already operating without these constraints. The README limits are decorative unless the skills and prompts start teaching real scoping principles. Any scoping guidance added to the skills files will be the first time Glyph actually communicates sizing principles to agents.

## Where to Convey This

1. **`about_operation_docs.md`** - Add a "Sizing & Scoping Principles" section near the top. Cover phase/task/subtask definitions, cold re-entry, human-reviewability of the <=2-file subtask limit, anti-padding, guideline ranges, and the revised difficulty model.
2. **`create_an_operation_doc.md`** - The agent already proposes a full structured plan (phases/tasks table, DAG, difficulty assignments) before creating the doc. What is still missing is the explicit calibration questions about granularity, autonomy, and splitting trade-offs — add a short step prompting the agent to ask the user those questions after presenting the plan.
3. **`about_glyph.md`** - Add a short "Scope & Independence" subsection covering user orchestration, user-chosen execution granularity, and task boundaries as re-entry points.
4. **README** - Soften "Up to 4 Phases" into language like "typically 2-4 phases" so it reads as guidance rather than a hard limit.
