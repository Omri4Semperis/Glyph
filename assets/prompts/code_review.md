# Your mission

Perform a code review{{#what_is_being_reviewed}} of #{{what_is_being_reviewed}}{{/what_is_being_reviewed}}

## Before starting

1. Read an example code review using `get_example("code_review")` to understand the format, structure, and issue tracking
2. Study how issues progress from detailed sections to Bottom Line, Summary Table, Executive Summary, and Recommendations
3. Gather review context before writing: what's being reviewed, review type, focus (default: full), target context/stack, severity scope (default: all), and supporting references.
4. If context is missing, don't block the review unless there's genuinely nothing to review. State assumptions in Basic Data and continue.

{{#has_references}}

## Additional References

{{#design_log_name}}- #{{design_log_name}}
{{/design_log_name}}
{{#additional_context}}- {{additional_context}}
{{/additional_context}}
{{/has_references}}

## Review structure

The structure offers multiple ways to quickly understand the reviewed material at varying detail levels.

- Basic Data - establishes review type, focus, target context/stack, assumptions, and references
- Detailed sections - "Functionality", "Code/Inline documentation/Comments", "Testing/Coverage", "Documentation/Alignment of docs to code", "Performance & Security" (when explicitly requested by the user or clearly central to the reviewed change)
- Lessons Learned
- The bottom line
- Summary Table - includes all detailed sections + lessons learned in a tabular format
- Executive summary (yes, towards the end)
- Recommendations

Issues may surface at any point alongside positive findings. Mention them in detailed sections and also in the Bottom Line table and Summary Table. Issues use special syntax (e.g., `[issue_3 ⚠️]` for the third issue, an important one).

At first mention, succinctly explain: what's wrong, where, why it matters, and the concrete next action if straightforward. Use the most specific location available (file + symbol + line).

## CRITICAL: Issue Consistency Rules

**The Binary Principle**: Everything you find is EITHER:

- ✅ Good/Pass - No action needed
- OR it's a tracked issue with severity (❌ Blocking, ⚠️ Important, ℹ️ Nice-to-have, 🦋 Cosmetic)

**No standalone warnings, concerns, or recommendations.** If something is "partially handled", "could be improved", "consider doing X", or "nice to have"—it IS an issue and MUST be tracked.

**Issue Reference Format**: Always use `[issue_X emoji]` format where X is the issue number and emoji matches severity:

- `[issue_1 ❌]` for blocking/critical
- `[issue_2 ⚠️]` for important
- `[issue_3 ℹ️]` for nice-to-have
- `[issue_4 🦋]` for cosmetic

**Every issue MUST appear in ALL of these places**:

1. **First mention** in detailed sections (where it's discovered)
2. **Bottom Line - Issues Summary table** (all issues listed)
3. **Summary Table** - Referenced in Status or Details column for relevant aspect (e.g., "⚠️ Warning [issue_1 ⚠️, issue_2 ⚠️]")
4. **Executive Summary** - Total count must match all tracked issues
5. **Recommendations section** - Every issue gets a recommendation

**Consistency Check**: Before finalizing the review, verify that:

- Each issue number appears consistently with the same severity emoji everywhere
- No warnings/concerns exist outside the issue tracking system
- The issue count in Executive Summary matches the Bottom Line table
- All issues from Bottom Line appear in Summary Table and Recommendations

**The structure**:

- Basic data:
  - Date
  - Reviewer
  - Review type
  - Review focus
  - Target context/stack
  - Assumptions
  - Primary references
  - Additional references (PR link, commit hash, benchmark note, etc.)
- Detailed review
  - **IMPORTANT**: In EVERY detailed section below, use ONLY two types of markers:
    - ✅ for things that are good/pass
    - `[issue_X emoji]` for ANYTHING that is not perfect (warnings, concerns, partial implementations, recommendations, nice-to-haves, etc.)
  - Functionality ("Do all implemented features match the requirements?")
    - Requirements Verification (A table with columns: Requirement, Status, Evidence)
    - Are edge cases handled? (Mark each as ✅ or [issue_X emoji])
    - Deviations from design- Are they justified and documented?
  - Code Quality
    - Static code analysis (line counts in reviewed modules + abnormal findings exceeding thresholds, e.g., methods over 20 lines)
    - Are SOLID, DRY, and KISS principles followed?
    - Does it follow project conventions and patterns?
    - Is the code clean, readable, and well-structured?
    - Are inline comments present for complex logic?
    - Is there appropriate error handling?
    - Logging
  - Testing
    - Unit tests (table with columns: Test file, tested file(s)/functionality, Test count, Coverage areas)
    - Are integration tests present for key flows?
    - Are edge cases and error scenarios tested?
    - Testing quality and best practices (AAA pattern, mocks/stubs, etc.)
  - Documentation
    - Code and docs alignment
    - Any other relevant documentation (README, external docs, artifacts, operation doc, etc.)
    - Is external documentation updated per review findings?
    - Are lessons learned documented appropriately?
  - Performance & Security (when explicitly requested by the user or clearly central to the reviewed change)
    - Measured performance (response times, memory usage, etc.)
    - Are there any performance concerns?
    - Security review (input validation, auth, data handling, etc.)
    - Are there security vulnerabilities?
  - Lessons Learned
    - Confirmed strengths or reusable patterns (only when materially useful)
    - What could be improved?
    - Any unexpected findings or insights?
    - Are all lessons documented in appropriate documents (design log, operation doc, etc.) beyond the one being reviewed?
- Executive summary- one paragraph with a Pass ✅ or Fail ❌ for the review.
- Bottom line—issues summary table with columns:
  - Issue # (1, 2, 3, etc.)
  - Category (Code/inline documentation, Testing, Documentation, Performance, Security, etc.)
  - Location(s) (As specific as possible, e.g., `src/module.py:Class.method:L42`)
  - Origin (References that may have caused this issue, e.g., "dl_6 step 5" or "OP_123 Phase 2/Task 1")
  - Severity (Blocking/Critical ❌, Important ⚠️, Nice to have/Optional ℹ️, Cosmetic/Recommendation 🦋)
  - Recommendation (4 words max, e.g., "Refactor method X", "Add unit tests", "Update documentation", etc.)
- Summary Table with columns:
  - Aspect (Functionality, Code Quality, Architecture, Test Coverage, Documentation, Performance, Security, Design Log Compliance (if provided), Size Constraints)
  - Status (Pass ✅, Fail ❌, Warning ⚠️) - **MUST include issue references when status is Warning/Fail** (e.g., "⚠️ Warning [issue_1 ⚠️, issue_2 ⚠️]" or "❌ Blocking [issue_4 ❌, issue_5 ❌]")
  - Details (one short sentence per aspect, e.g., "All requirements met", "Clean code with minor issues", "Missing tests for edge cases", etc.)
- Executive summary- overall assessment. Must include:
  - Total issue count (must match Bottom Line table)
  - Breakdown by severity (e.g., "2 Blocking, 5 Important, 1 Nice-to-have")
  - List each issue with its one-line summary
  - Final Pass ✅ or Fail ❌ verdict
- Recommendations—one of three forms:
  - "Nothing to add" (only if zero issues found)
  - "A few simple issues found, here are the recommended solutions/actions: [detailed recommendations for each issue by issue number]"
  - "Issues found (sorted by severity). Basic recommendations: [per issue by number]." End with: "A more detailed action plan should be created."
  - **CRITICAL**: Every issue from the Bottom Line table MUST have a corresponding recommendation listed here

## Final notes

- Use Glyph's `create_code_review` tool to generate a template report (saved in `.assistant/ad_hoc`) and fill it with findings.
- Use Glyph's static code analysis tool for file metrics and mermaid tool for visualizing complex code structures or flows.
- No generic praise or filler. Only include confirmed strengths when non-trivial, reusable, or directly relevant.

**Before submitting the review, verify**:

1. Every issue number appears with consistent severity emoji throughout
2. No standalone issues/concerns exist without an issue tag
3. Issue count in Executive Summary = Row count in Bottom Line table
4. Every issue in Bottom Line appears in Summary Table (in relevant aspect rows)
5. Every issue in Bottom Line has a recommendation listed
6. Every issue is verifiable in the reviewed material; do not speculate
7. Recommendations fit the target context/stack without assuming unavailable features or tooling
8. Low-signal cosmetic items filtered unless they materially affect readability or consistency
9. If no issues were found, say so explicitly instead of manufacturing issues
