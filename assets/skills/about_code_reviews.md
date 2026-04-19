# Code Review Guidelines

Use code reviews to identify real bugs, regression risks, missing tests, missing documentation, and unsafe assumptions. Keep the review proportional to the size and risk of the change.

## Gather Context First

Before reviewing, determine:

1. What is being reviewed: file, module, PR, feature, artifact, or document set.
2. Review focus: `full` by default, or a narrower focus such as correctness, testing, documentation, performance, security, readability, or conventions.
3. Target context: language, framework/runtime, platform, version, and any known constraints.
4. Severity threshold: `all` by default, or a narrower filter such as warnings-and-above or critical-only.

If some context is missing, do not block the review unless there is genuinely nothing to review. State the assumptions briefly near the top and continue.

## Severity Model

- `Critical`: correctness bugs, security vulnerabilities, data loss risks, or production-impacting failures.
- `Warning`: maintainability problems, likely regressions, missing tests, meaningful performance pitfalls, or documentation gaps that matter.
- `Info`: low-risk consistency issues, modernization opportunities, or minor polish.

## Review Lenses

Apply the lenses that fit the reviewed material:

1. Correctness and behavior: does the change match the intended behavior and handle edge cases?
2. Structure and design: are responsibilities clear and dependencies reasonable?
3. Naming and conventions: does the code match the local project style and domain terminology?
4. Performance and resource use: are there avoidable allocations, blocking calls, repeated work, or scaling risks?
5. Security and trust boundaries: are inputs validated, secrets handled correctly, and privileged operations protected?
6. Readability and maintainability: is the code easy to follow, test, and modify safely?
7. Testing and observability: are important paths verified, and will failures be visible?
8. Documentation and rollout: do docs, notes, and operational expectations match the change?

## Writing Rules

- Explain why each issue matters, not just what to change.
- Use the most specific location available.
- Keep findings verifiable. Do not speculate.
- Acknowledge concrete strengths when they are real and worth preserving.
- If there are many low-severity items, summarize them instead of flooding the review with noise.
- Respect the actual stack and version. Do not recommend features or conventions that do not fit the target context.

## Final Check

Before finalizing a review, verify:

- Every issue is real and traceable to the reviewed material.
- Each issue has a severity, location, impact, and concrete suggestion.
- Recommendations are ordered by impact.
- The final verdict matches the findings.
- If no issues were found, say so explicitly.