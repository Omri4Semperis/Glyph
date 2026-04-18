Design logs should be written so a senior developer can understand and implement the design from the information provided, making some decisions independently. Include specific details: file paths, type signatures, data structures, API endpoints, charts and diagrams when relevant. The goal is to provide enough information to implement without excessive follow-up questions.

When creating an operation doc from a plan step in a design log, consider all information—background, Q&A, decisions, and the lessons learned section.

# Design Log Methodology Rules

The project follows a rigorous design log methodology for all significant features and architectural changes.

## Before Making Changes

1. **Check design logs** in `.assistant/design_logs/_summary.md` for existing designs and implementation notes, then read the relevant logs
2. **For new features**: Create design log first, get approval, then implement
3. **Read related design logs** to understand context and constraints

## When Creating Design Logs

### Two-Step Creation Process

Design logs are created in **two steps** with a pause for user input:

**Step 1: Initial Creation (Stop at Q&A)**

1. **Create the file** using the `add_design_log` tool
2. **Populate through Q&A section**:
   - Background (context)
   - Problem statement
   - Questions and Answers section with your questions
3. **STOP and wait for user** to answer the questions
4. **Explicitly instruct the user**: Tell them questions are in the Q&A section and ask them to answer and notify when ready

**Step 2: Complete the Document (After User Answers)**
5. **Resume after user confirmation** that questions are answered
6. **Complete remaining sections**:

- Further analysis (if needed based on answers)
- Decided approach (architecture and implementation design)
- Verification criteria
- Plan (with step breakdown and difficulty ratings)
- Examples, trade-offs, etc.

### Content Guidelines

1. **Structure**: Background → Problem → Questions and Answers → Further Analysis → Decided Approach → Verification Criteria → Plan
2. **Be specific**: Include file paths, type signatures, validation rules
3. **Show examples**: Use ✅/❌ for good/bad patterns, include realistic code
4. **Explain why**: Don't just describe what, explain rationale and trade-offs
5. **Ask Questions (in the file)**: For anything unclear or missing—questions should be targeted and relevant to design decisions
6. **When answering questions**: Keep the questions, add answers below them (during the Step 1→2 pause)
7. **Step checkbox convention**: In the Plan section, every step title must include `[ ]` initially. Change to `[x]` only when the user explicitly marks that step as done.
8. **Be brief**: Write short explanations covering only what's most relevant
9. **Draw Diagrams**: Use Mermaid inline diagrams when applicable
10. **Define verification criteria**: How to confirm the implementation solves the original problem

## When Implementing

1. **Follow the implementation plan** steps from the design log
2. **Write tests first** or update existing tests to match new behavior
3. **Do not update** initial design log sections once implementation starts
4. **Append design log** with "Implementation Results" section as you go
5. **Document deviations**: Explain why implementation differs from design
6. **Run tests**: Include test results (X/Y passing) in implementation notes
7. **After implementation**: Add a summary of deviations from original design

## When Answering Questions

1. **Reference design logs** by number when relevant (e.g., "See Design Log #50")
2. **Use codebase terminology**: Adapt to your project's conventions
3. **Show type signatures**: Include relevant type definitions
4. **Consider backward compatibility**: Default to non-breaking changes

## References

Use standard markdown file references in design logs:

- Referencing another design log: `[dl_123](.assistant/design_logs/dl_123_title.md)` - use the full filename
- Referencing an artifact: `[art_123](.assistant/artifacts/art_123_name.ext)` - use the full filename with extension
- Referencing an operation: `[op_123](.assistant/operations/op_123_title.md)` - use the full filename

You can also use descriptive link text: `[See design log about feature X](.assistant/design_logs/dl_123_feature_x.md)`