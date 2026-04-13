# Code Review Report: [What's being reviewed]

> **CRITICAL: Issue Consistency Rule**
>
> Everything in this review is EITHER:
>
> - ✅ Good/Pass - No action needed
> - OR it's a tracked issue: `[issue_X emoji]` where emoji = ❌ Blocking, ⚠️ Important, ℹ️ Optional, 🦋 Cosmetic
>
> For example, "[issue_7 ❌]" in Code Quality must also appear in the Bottom Line table, Executive Summary count, and Recommendations.
>
> **NO standalone warnings, concerns, or recommendations without issue tracking.**
>
> Every issue MUST appear in: (1) First mention in detailed sections, (2) Bottom Line table, (3) Summary Table Status column, (4) Executive Summary count, (5) Recommendations section.
>
> [Remove this note when review is done and all issues are tracked consistently]

## Basic Data

- **Date:** [YYYY-MM-DD]
- **Reviewer:** [Name/Glyph AI Assistant]
- **Review Type:** [Implementation / Refactoring / Source code / PR / Artifact / etc.]
- **Review Focus:** [Full review / Functionality / Code quality / Testing / Documentation / Performance / Security / Custom]
- **Target Context / Stack:** [Language, framework/runtime, platform, version, constraints, etc.]
- **Assumptions:** [State any assumptions made because context was missing; otherwise "None"]
- **Primary References:** [Design log, operation doc, PR, issue, spec, benchmark, artifact, etc.]
- **Additional References:** [Supporting refs or "N/A"]

[One-paragraph overview. Lead with the most important finding and total issue count by severity. Mention material assumptions briefly.]

## Detailed Review

[For each new issue: what's wrong, where, why it matters, and next action if straightforward.]

### 1. Functionality Review

#### Requirements Verification

| Requirement | Status | Evidence |
| - | - | - |
| [Req 1] | ✅ or [issue_X emoji] | [Specific reference to implementation or test] |
| [Req 2] | ✅ | [Specific reference to implementation or test] |
| [Req 3] | ✅ | [Specific reference to implementation or test] |

#### [Optional: Feature Flow Diagram]

```mermaid
flowchart LR
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
```

#### Edge Cases Handling

- **[Edge Case 1]:** ✅ [Description of how it's handled]
- **[Edge Case 2]:** [issue_X emoji] [Description of issue]
- **[Edge Case 3]:** ✅ [Description of how it's handled]

#### Deviations from Design

1. **[Deviation 1]:** [Description]
   - **Reason:** [Why the deviation was necessary]
   - **Documentation:** [Where is this documented]
   - **Assessment:** ✅ / ⚠️ / ❌

2. **[Deviation 2]:** [Description]
   - **Reason:** [Why the deviation was necessary]
   - **Documentation:** [Where is this documented]
   - **Assessment:** ✅ / ⚠️ / ❌

### 2. Code Quality Review

#### Static Code Analysis

**Reviewed Files/Modules:**

- [File/Module 1]: [X lines, Y methods/functions, Z classes]
- [File/Module 2]: [X lines, Y methods/functions, Z classes]
- [File/Module 3]: [X lines, Y methods/functions, Z classes]

**Abnormal Findings:**

- [Finding 1]: [Description of any unusual metrics or patterns]
- [Finding 2]: [Description of any concerning aspects]

#### SOLID Principles & Design Patterns

- **Single Responsibility:** [Single responsibility assessment]
- **Open/Closed Principle:** [Extensibility assessment]
- **Liskov Substitution:** [Interface design assessment if applicable]
- **Interface Segregation:** [Cohesive interface assessment]
- **Dependency Inversion:** [Abstraction usage assessment]

#### DRY & KISS Principles

- **DRY (Don't Repeat Yourself):** [Code duplication assessment]
- **KISS (Keep It Simple, Stupid):** [Complexity and readability assessment]

#### Project Conventions & Patterns

- **Naming conventions:** ✅ [Assessment]
- **Code structure:** ✅ [Assessment]
- **Architecture compliance:** ✅ [Assessment]

#### [Optional: Module Architecture Diagram]

```mermaid
graph LR
    A[Module A] -->|dependency| B[Module B]
    B -->|uses| C[Module C]
```

#### Code Readability & Structure

- ✅ or [issue_X emoji] [Observation 1]
- ✅ or [Observation 2]

#### Inline Comments & Documentation

- **Complex Logic Comments:** ✅ or [issue_X emoji] [Assessment]
- **Function/Method Documentation:** ✅ or [issue_X emoji] [Assessment]
- **Code Clarity:** ✅ or [issue_X emoji] [Assessment]

#### Error Handling

- **Try/Catch Blocks:** ✅ or [issue_X emoji] [Assessment]
- **Error Messages:** ✅ [Assessment]
- **Error Recovery:** ✅ [Assessment]
- **Edge Case Errors:** ✅ [Assessment]

#### Logging

- **Log Coverage:** ✅ or [issue_X emoji] [Assessment]
- **Log Levels:** ✅ [Assessment]
- **Sensitive Data:** ✅ [Assessment]

### 3. Testing Review

#### Unit Tests

| Test File | Tested File(s)/Functionality | Test Count | Coverage Areas |
| - | - | - | - |
| [test_file_1.test.ts] | [source_file_1.ts - features A, B] | [10] | [Unit 1, Unit 2, Edge case 1] |
| [test_file_2.test.ts] | [source_file_2.ts - features C, D] | [15] | [Unit 3, Unit 4, Integration point 1] |

**Total Coverage:** [X%] statements, [Y%] branches, [Z%] functions

#### [Optional: Test Coverage Map]

```mermaid
graph TB
    subgraph "Test Files"
        T1[test_file_1.test.ts]
        T2[test_file_2.test.ts]
    end
    
    subgraph "Source Files"
        S1[source_file_1.ts]
        S2[source_file_2.ts]
    end
    
    T1 -->|X tests| S1
    T2 -->|Y tests| S2
```

#### Integration Tests

- **Test 1:** [Description of what is being tested]
  - **Status:** ✅ Present or [issue_X emoji] Missing
  - **Notes:** [Additional context]

- **Test 2:** [Description of what is being tested]
  - **Status:** ✅ Present or [issue_X emoji] Missing
  - **Notes:** [Additional context]

#### Edge Cases & Error Scenarios

**Tested:**

- [Edge case 1]: ✅ Tested at [location]
- [Edge case 2]: ✅ Tested at [location]

**Not Tested:**

- [issue_X emoji] [Edge case 3] - [Description and impact of not testing]
- [issue_Y emoji] [Edge case 4] - [Description and impact of not testing]

#### Test Quality & Best Practices

- **AAA Pattern:** ✅ or [issue_X emoji] [Assessment]
- **Mocks & Stubs:** ✅ or [issue_X emoji] [Assessment]
- **Test Clarity:** ✅ or [issue_X emoji] [Assessment]
- **Test Independence:** ✅ or [issue_X emoji] [Assessment]

### 4. Documentation Review

#### Code and Documentation Alignment

| Document Type | Document/File | Status | Notes |
| - | - | - | - |
| Design Log | [Link if applicable] | ✅ Aligned or [issue_X emoji] | [Brief note] |
| Operation Doc | [Link if applicable] | ✅ Aligned or [issue_X emoji] | [Brief note] |
| API Docs | [Link if applicable] | ✅ Aligned or [issue_X emoji] | [Brief note] |
| README | [Link if applicable] | ✅ Updated or [issue_X emoji] | [Brief note] |
| Inline Docs | Source files | ✅ Complete or [issue_X emoji] | [Brief note] |

#### External Documentation

- **[Documentation Type 1]:** ✅ or [issue_X emoji] [Assessment and findings]
- **[Documentation Type 2]:** ✅ or [issue_X emoji] [Assessment and findings]
- **[Documentation Type 3]:** ✅ or [issue_X emoji] [Assessment and findings]

#### Lessons Learned Documentation

- **In Design Log:** ✅ Documented or [issue_X emoji] [Details]
- **In Operation Document:** ✅ Documented or [issue_X emoji] [Details]
- **Should lessons be propagated to other projects?** ✅ Yes / No - [Reasoning]

### 5. Performance & Security Review

#### Performance Analysis

**Measured Performance:**

| Scenario | Metric | Result | Assessment |
| - | - | - | - |
| [Scenario 1] | [Response time/Memory/Throughput] | [Value] | [✅ Good / ⚠️ Acceptable / ❌ Concerning] |
| [Scenario 2] | [Response time/Memory/Throughput] | [Value] | ✅ or [issue_X emoji] |
| [Scenario 3] | [Response time/Memory/Throughput] | [Value] | ✅ or [issue_X emoji] |

#### [Optional: Performance Visualization]

```mermaid
graph LR
    A[Small load<br/>Xms] --> B[Medium load<br/>Yms]
    B --> C[Large load<br/>Zms]
```

**Performance Assessment:**

- ✅ None identified OR
- [issue_X emoji] [Concern description]

#### Security Review

**Input Validation:**

- ✅ Validated or [issue_X emoji]
- [Details of validation approach]

**Authentication & Authorization:**

- ✅ Secure or [issue_X emoji]
- [Assessment of auth/authz implementation]

**Data Handling:**

- ✅ Secure or [issue_X emoji]
- [Assessment of how sensitive data is handled]

**Security Findings:**

- ✅ or [issue_X emoji] [Security finding 1]
- ✅ or [Security finding 2]
- ✅ or [Security finding 3]

### 6. Lessons Learned

#### Confirmed Strengths (Optional)

1. **[Strength 1]:** [Non-trivial strengths worth reusing or preserving only]

#### What Could Be Improved

1. **[Improvement area 1]:** [What could have been better and why]

#### Unexpected Findings or Insights

- **[Finding 1]:** [Explanation of unexpected discovery]

#### Documentation of Lessons Learned

- **Are lessons documented in design log?** ✅ Yes or [issue_X emoji] [Details]
- **Are lessons documented in operation document?** ✅ Yes or [issue_X emoji] [Details]
- **Should lessons be propagated to other projects?** ✅ Yes / No - [Reasoning]

## Bottom Line - Issues Summary

| Issue # | Category | Location(s) | Origin | Severity | Recommendation |
| - | - | - | - | - | - |
| issue_1 | [Category] | [file.ext:Symbol:Lxx] | [DL or OP reference] | ❌ / ⚠️ / ℹ️ / 🦋 | [Action - 4 words max] |
| issue_2 | [Category] | [file.ext:Symbol:Lxx] | [DL or OP reference] | ❌ / ⚠️ / ℹ️ / 🦋 | [Action - 4 words max] |
| issue_3 | [Category] | [file.ext:Symbol:Lxx] | [DL or OP reference] | ❌ / ⚠️ / ℹ️ / 🦋 | [Action - 4 words max] |

## Summary Table

| Aspect | Status | Details |
| - | - | - |
| **Functionality** | ✅ / ⚠️ / ❌ | [One sentence summary, including which issue_X caused it] |
| **Code Quality** | ✅ / ⚠️ / ❌ | [One sentence summary] |
| **Architecture** | ✅ / ⚠️ / ❌ | [One sentence summary] |
| **Test Coverage** | ✅ / ⚠️ / ❌ | [One sentence summary] |
| **Documentation** | ✅ / ⚠️ / ❌ | [One sentence summary] |
| **Performance** | ✅ / ⚠️ / ❌ | [One sentence summary] |
| **Security** | ✅ / ⚠️ / ❌ | [One sentence summary] |

## Executive Summary

Overall [good/acceptable/poor] implementation with [X] identified issues.

### ❌ Blocking Issues (Must fix before merge)

- **issue_X:** [One-line description]
- **issue_Y:** [One-line description]

### ⚠️ Important Issues (Recommended)

- **issue_X:** [One-line description]
- **issue_Y:** [One-line description]
- **issue_Z:** [One-line description]

### ℹ️ Optional Issues (Nice-to-have)

- **issue_X:** [One-line description]

### 🦋 Cosmetic Issues (Minor)

- **issue_X:** [One-line description]

**Conclusion**: [Summary of what must be done before merge and what should be follow-up work]

## Recommendations

### ❌ Blocking

1. [Action for issue_X] (issue_X)
2. [Action for issue_Y] (issue_Y)

### ⚠️ Important

1. [Action for issue_X] (issue_X, [location])
2. [Action for issue_Y] (issue_Y)
3. [Action for issue_Z] (issue_Z)

### ℹ️ Optional

1. [Action for issue_X] (issue_X)

> **Note:** Show specific fix recommendations only if solutions are simple. For many or complex issues, suggest creating a detailed action plan (operation). Remove this note when done.

## Consistency Checklist [Remove when review is done]

Before finalizing this review, verify:

- [ ] Every issue uses format `[issue_X emoji]` consistently throughout
- [ ] No standalone ⚠️ warnings exist without an issue tag
- [ ] Issue count in Executive Summary matches Bottom Line table row count
- [ ] Every issue in Bottom Line appears in Summary Table (in relevant aspect rows with Status column)
- [ ] Every issue in Bottom Line has a recommendation in Recommendations section
- [ ] All "not perfect" items (warnings, concerns, partial implementations) are tracked as issues
- [ ] Every issue is verifiable from the reviewed material
- [ ] Recommendations fit the target context/stack and assumptions
- [ ] Low-signal cosmetic items were filtered unless they materially matter
