# Your mission

Plan the creation of a new operation document.

{{#has_source_context}}
## Source Context

{{#design_log_name}}- Related design log: {{design_log_name}}{{/design_log_name}}
{{#step_to_create_doc_for}}- Focus step or identifier: {{step_to_create_doc_for}}{{/step_to_create_doc_for}}
{{#source_context}}- General source context: {{source_context}}{{/source_context}}
{{/has_source_context}}

## Instructions

- First read the glyph rules; then:
- Read the operation document guidelines; then:
- Read an example operation document using `get_example("operation")` to understand the expected format and structure; and finally:
- write the creation plan for the operation document.

The operation document's Background section must be comprehensive, exhaustive and detailed. Use all relevant source material provided to you.
{{#design_log_name}}If a design log is provided, take all relevant information from it you can find (anywhere in the design log, not just the selected step).{{/design_log_name}}
{{#source_context}}If general source context is provided, incorporate it explicitly into the Background and phase planning.{{/source_context}}
The Background section must include:

- **State**: Current state of the system/process
- **Goal**: Desired outcome of this operation
- **Approach**: High-level summary of phases and tasks

The Background section is encouraged to include mermaid charts where appropriate (glyph's mermaid tool can advise on this).

## Before you create the doc

1. Prove you read through the provided source material and understood what relevant information should drive the operation doc.
1. Prove you read through the operation document guidelines and understood them, showing me how you will apply them.
1. You'll keep it SOLID, DRY and Simple.
1. Tell me how many phases and tasks in each phase you plan to have in the operation doc.
1. For each phase, include a **Phase Difficulty** and for each task include a **Task Difficulty** using the emoji scale (0 = trivial, 5 = extremely difficult): 0️⃣, 1️⃣, 2️⃣, 3️⃣, 4️⃣, 5️⃣

- For every chosen difficulty level provide a one-line justification explaining why that level was selected.
- Describe how testing and validation will scale with the difficulty (e.g., baseline build/tests for Breezy/Low, unit+integration for Medium, broader integration/manual testing for High/Nightmare/Hell).
- Phase difficulty should match the highest task difficulty in that phase.

The operation document must reflect these difficulty assignments in its phases and tasks so implementers know expected scope and verification effort.

1. In your phases overview, include both:
   - A markdown table with columns: **Phase #**, **Status**, **Title**, **Difficulty**, **Tasks**. The **Difficulty** column shows the phase difficulty (highest task difficulty). The **Tasks** column contains a nested table with task details (Task #, Title, Difficulty, Status).
   - Status uses: ❌ (Not started), ⏳ (In progress), ✅ (Done), ⚠️ (Done with issues/aborted)
   - A Phases/Tasks DAG (Mermaid flowchart) showing phase and task dependencies with task nodes labeled `P{n}/T{m}` (e.g., `P1/T1`, `P2/T1`).