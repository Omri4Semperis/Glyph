# Your mission

Create a design log for {{topic}}, following the design log principles and structure.

## Before starting

1. Read the design log principles using `get_design_log_principles`
2. Read an example design log using `get_example("design_log")` to understand the format and structure
3. Read the `about_glyph` skill to understand the workflow
4. Ask clarifying questions if the scope is unclear

{{#additional_context}}
## Additional context

- #{{additional_context}}
{{/additional_context}}

## Process

1. **Understand the scope**: What problem are we solving? What decisions need to be made?
2. **Gather information**: What existing code, documentation, or constraints are relevant?
3. **Ask questions**: List unknowns that need answers before proceeding
4. **Design solution**: Detail the architecture and implementation plan
5. **Evaluate step difficulty**: After each step, assess difficulty using these metrics:
   - **Read**: How much context is involved (e.g., number of files/lines)?
   - **Write**: How much new/modified code is required?
   - **Logic**: How complex and demanding is the step to implement?
   - **Average**: Calculate the average difficulty.
6. **Create the log (Phase 1 - Initial Creation)**:
   - Use Glyph's `add_design_log` tool to create the file
   - Populate these sections:
     - Background (context and problem)
     - Questions and Answers section with your questions
   - **STOP HERE and wait for user input**
   - Tell the user: "I've created the design log with questions in the Q&A section. Please review and answer them, then let me know when you're ready to continue."
7. **Complete the log (Phase 2 - After User Answers Questions)**:
   - After the user answers questions and confirms readiness
   - Continue populating the remaining sections:
     - Further analysis (if needed)
     - Decided approach
     - Verification criteria
     - Plan (with step breakdown)
   - Include architecture, file structure, and implementation plan
   - Add references to related design logs, operations, or artifacts

## When creating the log

- Use clear, descriptive title (will become filename)
- Ask targeted questions in the Q&A section—things you genuinely need to know
- Provide suggested answers where helpful
- Keep questions focused and relevant to the design decisions

## After Phase 2 completion

1. Review the complete document with the user
2. Verify all questions were answered and incorporated
3. Outline the phases for the operation doc
