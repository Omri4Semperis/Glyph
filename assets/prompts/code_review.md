# Your mission

Perform a code review{{#what_is_being_reviewed}} of #{{what_is_being_reviewed}}{{/what_is_being_reviewed}}

## Before starting

1. Read the review guidance using `get_skill("about_code_reviews")`.
2. Read an example code review using `get_example("code_review")` to understand the expected structure.
3. Gather review context before writing: what is being reviewed, review type, review focus, target context/stack, severity threshold, and supporting references.
4. If some context is missing, do not block the review unless there is genuinely nothing to review. Default to a full review, all severities, and the best available target context. State assumptions briefly and continue.

{{#has_references}}

## Additional References

{{#design_log_name}}- #{{design_log_name}}
{{/design_log_name}}
{{#additional_context}}- {{additional_context}}
{{/additional_context}}
{{/has_references}}

## Review goals

- Surface real bugs, regression risks, missing tests, missing documentation, and unsafe assumptions.
- Keep the report proportional to the size and risk of the change.
- Keep the report general unless the reviewed material is tied to a specific stack.
- Findings come first. Positive notes should be specific and useful, not filler.
- Keep every finding verifiable from the reviewed material.

## Review structure

Use this structure unless a section does not apply:

- Summary
- Issues
- What's Done Well
- Recommendations
- Verification Checklist
- Conclusion

## Guidance

- Put each issue in the Issues table with these columns: `#`, `Severity`, `Location`, `Issue`, `Why It Matters`, `Suggestion`.
- Sort issues by severity and then by user impact.
- Use `Critical` for correctness/security/data-loss risks, `Warning` for meaningful quality or coverage gaps, and `Info` for low-risk polish.
- Use the most specific location available.
- State assumptions near the top when context is incomplete.
- If no issues were found, say `No issues found.` instead of inventing weaker notes.
- Only include performance or security findings when they are requested or clearly relevant to the reviewed change.
- Keep "What's Done Well" to concrete strengths that should be preserved.
- Acknowledge at least one or two concrete strengths when the reviewed material genuinely earns it.
- Explain why each issue matters, not just what to change.
- Keep recommendations aligned to the actual findings.
- Order recommendations by impact.
- If there are many low-severity notes, summarize them instead of listing every nit.
- Do not flag patterns as issues when they are appropriate for the target stack or version.
- Do not add extra summary tables, issue taxonomies, or bookkeeping sections.

## Final notes

- Use Glyph's `add_code_review` tool to generate the report in `.assistant/ad_hoc` and then fill it with findings.
- Consider using Glyph's `static_code_analysis` tool only when it adds meaningful signal.
- If the review should be kept as a tracked artifact, persist it with `persist_artifacts`.
- Keep the report concise.