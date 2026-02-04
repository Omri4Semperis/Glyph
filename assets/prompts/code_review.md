```markdown
Perform a code review of operation: {operation_name}

**References:**

- Operation Document: {operation_doc_path}
- Design Log (if applicable): {design_log_path}

**Before starting:**

1. Read the operation document thoroughly
2. Read the related design log if provided
3. Understand the original requirements and constraints

**Review Scope:**

{review_scope}
<!-- Options: full (all phases), specific phases/tasks, or changes since last review -->

**Review Checklist:**

1. **Functionality**
   - Do all implemented features match the requirements?
   - Are there any deviations from the design? Are they justified and documented?
   - Are edge cases handled?

2. **Code Quality**
   - Is the code clean, readable, and well-structured?
   - Does it follow project conventions and patterns?
   - Is there appropriate error handling?
   - Are SOLID, DRY, and KISS principles followed?

3. **Test Coverage**
   - Are there sufficient unit tests?
   - Are integration tests present for key flows?
   - Are edge cases and error scenarios tested?

4. **Documentation**
   - Are inline comments present for complex logic?
   - Is external documentation updated?
   - Are lessons learned documented in the operation?

5. **Performance & Security**
   - Are there any performance concerns?
   - Are there security vulnerabilities?
   - Is input validation present?

**Output:**

Generate a code review report following the example template. Include:

- Summary table with pass/fail/warning status
- Detailed findings for each review category
- Specific code issues with locations and suggestions
- Recommendations categorized by priority (Must Fix, Should Fix, Nice to Have)
- Lessons learned that should propagate back to the design log

**After review:**

1. Discuss findings with the user
2. Create action items for any issues found
3. If lessons learned are significant, suggest updating the design log
```
