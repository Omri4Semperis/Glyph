Design logs are meant to be written such that a senior developer could understand and implement the design based on the information provided, even if they had to make some decisions on their own. This means that design logs should include specific details such as file paths, type signatures, data structures, API endpoints, charts and diagrams when relevant. The goal is to provide enough information for someone to implement the design without needing to ask too many follow-up questions.

When creating an operation doc out of a plan step in this design log, you should consider all information in this design log- including background, Q&A, decisions etc, and even the lessons learned section at the bottom.

# Design Log Methodology Rules

The project follows a rigorous design log methodology for all significant features and architectural changes.

## Before Making Changes

1. **Check design logs** in `.assistant/design_logs/_summary.md` for existing designs and implementation notes, then read the relevant logs
2. **For new features**: Create design log first, get approval, then implement
3. **Read related design logs** to understand context and constraints

## When Creating Design Logs

### Two-Phase Creation Process

Design logs are created in **two phases** with a user input pause in between:

**Phase 1: Initial Creation (Stop at Q&A)**
1. **Create the file** using the `add_design_log` tool
2. **Populate through Q&A section**:
   - Background (context)
   - Problem statement
   - Questions and Answers section with your questions
3. **STOP and wait for user** to answer the questions
4. **Explicitly instruct the user**: Tell them you've added questions in the Q&A section and ask them to answer the questions and notify you when ready

**Phase 2: Complete the Document (After User Answers)**
5. **Resume after user confirmation** that questions are answered
6. **Complete remaining sections**:
   - Further analysis (if needed based on answers)
   - Decided approach (architecture/research design)
   - Verification criteria
   - Plan (with step breakdown and difficulty ratings)
   - Examples, trade-offs, etc.

### Content Guidelines

1. **Structure**: Background → Problem → Questions and Answers → Further Analysis → Decided Approach → Verification Criteria → Plan
2. **Be specific**: Include file paths, type signatures, validation rules
3. **Show examples**: Use ✅/❌ for good/bad patterns, include realistic code
4. **Explain why**: Don't just describe what, explain rationale and trade-offs
5. **Ask Questions (in the file)**: For anything that is not clear, or missing information - these questions should be targeted and relevant to design decisions
6. **When answering question**: keep the questions, just add answers (this happens during the pause between Phase 1 and Phase 2)
7. **Be brief**: write short explanations and only what most relevant
8. **Draw Diagrams**: Use mermaid inline diagrams when it makes sense
9. **Define verification criteria**: how do we know the implementation solves the original problem

## When Implementing

1. **Follow the implementation plan** phases from the design log
2. **Write tests first** or update existing tests to match new behavior
3. **Do not Update design log** initial section once implementation started
4. **Append design log** with "Implementation Results" section as you go
5. **Document deviations**: Explain why implementation differs from design
6. **Run tests**: Include test results (X/Y passing) in implementation notes
7. **After Implementation** add a summary of deviations from original design

## When Answering Questions

1. **Reference design logs** by number when relevant (e.g., "See Design Log #50")
2. **Use codebase terminology**: Adapt to your project's conventions
3. **Show type signatures**: Include relevant type definitions for your language
4. **Consider backward compatibility**: Default to non-breaking changes

## References

Writing references in a design log is encouraged, using standard markdown file references:

- Referencing another design log: `[dl_123](.assistant/design_logs/dl_123_title.md)` - use the full filename
- Referencing an artifact: `[art_123](.assistant/artifacts/art_123_name.ext)` - use the full filename with extension
- Referencing an operation: `[op_123](.assistant/operations/op_123_title.md)` - use the full filename

You can also use descriptive link text: `[See design log about feature X](.assistant/design_logs/dl_123_feature_x.md)`