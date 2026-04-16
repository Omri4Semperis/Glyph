# Your mission

Create a new operation document.

{{#has_source_context}}

## Source Context

{{#design_log_name}}- Related design log: {{design_log_name}}{{/design_log_name}}
{{#step_to_create_doc_for}}- Focus step or identifier: {{step_to_create_doc_for}}{{/step_to_create_doc_for}}
{{#source_context}}- General source context: {{source_context}}{{/source_context}}
{{/has_source_context}}

## Instructions

- Consider first reading Glyph fundamentals using `get_skill("about_glyph")`; then:
- Consider reading operation document guidelines using `get_skill("about_operation_docs")`; then:
- Consider reading an example operation document using `get_example("operation_doc")` to understand the format and structure; then:
- Optionally read the operation template using `get_template("operation_doc")`;

The Background section must be comprehensive and detailed. Use all relevant source material.
{{#design_log_name}}If a design log is provided, take all relevant information from it (anywhere in the log, not just the selected step).{{/design_log_name}}
{{#source_context}}If general source context is provided, incorporate it explicitly into the Background and phase planning.{{/source_context}}
The Background section must include:

- **State**: Current state of the system/process
- **Goal**: Desired outcome of this operation
- **Approach**: High-level summary of phases and tasks

Include mermaid charts in the Background where appropriate (Glyph's mermaid tool can advise).

## Before you create the doc

1. Show you've read the source material and understood what information should drive the operation doc.
1. Show you've read the operation document guidelines and how you'll apply them.
1. Keep it SOLID, DRY, and Simple.
1. Tell me the planned number of phases and tasks per phase.
1. After presenting the proposed structure, ask a short calibration set of user-facing questions before creating the doc:
   - Granularity preference: does the proposed number of phases and tasks match how the user wants to delegate the work?
   - Autonomy level: for any `High` or harder tasks, does the user want to delegate phase-by-phase or task-by-task?
   - Scope calibration: where a task could reasonably stay whole or be split, does the user prefer finer-grained progress tracking or less overhead?
   - Provide a recommended default answer for each question based on the plan you proposed.
1. Include **Phase Difficulty** and **Task Difficulty** using the emoji scale (0 = trivial, 5 = extremely difficult): 0️⃣, 1️⃣, 2️⃣, 3️⃣, 4️⃣, 5️⃣

- For each difficulty level, provide a one-line justification.
- Describe how testing scales with difficulty (e.g., baseline build/tests for Breezy/Low, broader unit and integration checks for Medium, broader testing and targeted manual verification for High/Nightmare/Hell).
- Phase difficulty should match the highest task difficulty in that phase.
- Base difficulty on cognitive complexity, risk, and novelty rather than raw file count.

The operation doc must reflect these difficulty assignments so implementers know expected scope and verification effort.

1. In your phases overview, include both:
   - A markdown table with columns: **Phase #**, **Status**, **Title**, **Difficulty**, **Tasks**. The **Difficulty** column shows the phase difficulty (highest task difficulty). The **Tasks** column contains a nested table with task details (Task #, Title, Difficulty, Status).
   - Status uses: ❌ (Not started), ⏳ (In progress), ✅ (Done), ⚠️ (Done with issues/aborted)
   - A Phases/Tasks DAG (Mermaid flowchart) showing phase and task dependencies with task nodes labeled `P{n}/T{m}` (e.g., `P1/T1`, `P2/T1`).

## After planning

1. Create the operation document file using `add_operation(abs_path, title, short_desc)`.
2. Fill the created operation document with the finalized plan, phases, tasks, and difficulty assignments.