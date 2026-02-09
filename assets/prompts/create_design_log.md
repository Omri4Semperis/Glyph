In this prompt:

<topic> = {{topic}}
<design_log_type> = {{design_log_type}}
<additional_context> = {{additional_context}}

# Your mission

Create a design log for <topic>

**Design Log Type:** <design_log_type>
<!-- Options: research, implementation, or both -->

## Before starting

1. Read the design log principles using `get_design_log_principles`
2. Read the `about_glyph` skill to understand the workflow
3. Ask clarifying questions if the scope is unclear

## Context

- <additional_context>

## Process

1. **Understand the scope**: What problem are we solving? What decisions need to be made?
2. **Gather information**: What existing code, documentation, or constraints are relevant?
3. **Ask questions**: List unknowns that need answers before proceeding
4. **Research options**: For research logs, explore alternatives and trade-offs
5. **Design solution**: For implementation logs, detail the architecture and plan
6. **Evaluate step difficulty**: After each step, assess the difficulty using the following metrics:
   - **Read**: How much context is involved (e.g., number of files/lines)?
   - **Write**: How much new/modified code is required?
   - **Logic**: How complex and demanding is the step to implement?
   - **Average**: Calculate the average difficulty.
7. **Create the log (Phase 1 - Initial Creation)**: 
   - Use Glyph's `add_design_log` tool to create the file
   - Populate the following sections:
     - Background (context and problem)
     - Questions and Answers section with your questions
   - **STOP HERE and wait for user input**
   - Explicitly tell the user: "I've created the design log and added questions in the Q&A section. Please review and answer the questions, then let me know when you're ready for me to continue completing the document."
8. **Complete the log (Phase 2 - After User Answers Questions)**:
   - After the user has answered your questions and confirmed they're ready
   - Continue populating the remaining sections:
     - Further analysis (if needed)
     - Decided approach
     - Verification criteria
     - Plan (with step breakdown)
   - For research: focus on options, trade-offs, recommendations
   - For implementation: include architecture, file structure, implementation plan
   - Add references to related design logs, operations, or artifacts

## When creating the log

- Use clear, descriptive title (will become filename)
- Ask targeted questions in the Q&A section - things you genuinely need to know
- Provide suggested answers where helpful to guide the user
- Keep questions focused and relevant to the design decisions

## After Phase 2 completion

1. Review the complete document with the user
2. Verify all questions were answered and incorporated into the design
3. If implementation type, outline the phases for the operation doc