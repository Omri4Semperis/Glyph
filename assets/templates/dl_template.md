# Design Log: [Title]

- **Date:** [YYYY-MM-DD]
- **Author:** Glyph AI Assistant
- **Type:** [Research | Implementation | Both]
- **Related Docs:** [Link to related design logs, operations docs, artifacts (if any)]

---

**Note**: This is a general template, which can be adapted for both research and implementation design logs. Depending on the type and specific goal, some sections may be omitted, modified or added. Remove this comment when not needed anymore
---

## Background

### context

[Provide context about the current state of the system and any relevant history. For research: include what is currently known and unknown. For implementation: describe the current system state.]

### Problem

[Clearly state what problem you're trying to solve or what you need to understand. For research: frame as questions to answer or hypotheses to validate. For implementation: specify requirements and constraints.]

## Questions and Answers

> Keep questions even after answering - they provide valuable context.

[After having established the context and problem, the AI assistant will add questions here and **pause** to let the user answer them. The AI will wait for user confirmation before continuing with the rest of the document. If possible, each question should have suggested answers to help guide the user.]

> **Note to AI**: After populating this section with questions, STOP and explicitly ask the user to answer the questions and notify you when ready to continue.

### Q1

**Q1: [Question from AI assistant]**
A1: [Leave empty or provide a few answers for the user to choose from]

### Q2

**Q2: [Question from AI assistant]**
A2: [Leave empty or provide a few answers for the user to choose from]

[More Q&As as needed]

---

**⏸️ PAUSE POINT**: The AI assistant will stop here and wait for the user to answer the questions above before continuing to populate the sections below
---

## Further analysis

[Following the answers in the Q&A section, the AI assistant may need to perform further analysis to clarify the problem, explore alternatives, or refine the design. This section can include additional research, data analysis, or technical exploration as needed. It is also possible to remove this section if no further analysis is needed after the Q&A phase.]

## Decided approach

[For implementation: Describe the proposed solution in detail. The level of details should be such that a senior developer could understand and implement it- even if they had to make some decisions on their own. Include file paths, type signatures, data structures, API endpoints, charts and diagrams etc. For research: Describe the research methodology, data sources, analysis approach, etc.]

### Architecture / Research Design

[For implementation: High-level architecture description, optionally with a diagram. For research: Describe research methodology, data collection approach, analysis framework.]

### Database Schema

[Implementation only: If applicable, describe database changes. Remove this section if not applicable.]

### API Endpoints

[Implementation only: If applicable, describe API changes. Remove this section if not applicable.]

### File Structure

[Implementation only: Where will new/modified files live? Remove this section if not applicable.]

### Key Type Signatures

[Implementation only: If using TypeScript or similar, include type definitions. Remove this section if not applicable.]

### Examples

[Implementation only: Show good and bad coding patterns with code examples. For research: provide example data, analysis outputs, or findings. Remove this section if not applicable.]

### Trade-offs

[Discuss alternatives considered and why you chose this approach. For implementation: technical trade-offs, architecture choices. For research: methodology choices, data source trade-offs, analysis approach alternatives.]

## Verification Criteria

[What would it take to consider this design log's work "done"? For implementation: list acceptance criteria, test requirements, performance targets. For research: define what answers the research questions, validation methods for findings.]

## Plan

[Break down the work into phases, and group phases by topic. For implementation: describe implementation phases. For research: describe research phases (literature review, data collection, analysis, synthesis). This should be a high-level plan, not a detailed task list. If it's critical to have more than just a couple of sentence- include an artifact file and refer to it in the step itself. Remove this section if not applicable.]

**Steps overview**:
[A table grouping steps by topic and showing basic info about each step]

| Topic | Step | Status | Title | Effort (Read, Write, Logic, Average) |
| - | - | - | - | - |
| [Topic 1 name] | S1 | ❌ (Pending), ⏳ (In progress), ✅ (Done), ⚠️ (Done with issues/aborted) | [Title of Step 1] | [X/10], [X/10], [X/10], **[X.X/10]** |
| [Topic 1 name] | S2 | ❌/⏳/✅/⚠️ | [Title of Step 2] | [X/10], [X/10], [X/10], **[X.X/10]** |
| [Topic 2 name] | S3 | ❌/⏳/✅/⚠️ | [Title of Step 3] | [X/10], [X/10], [X/10], **[X.X/10]** |

### Step 1: [Title of Step 1] ❌/⏳/✅/⚠️

| Effort (Read, Write, Logic, Average) | In a nutshell | References |
| - | - | - |
| 5, 6, 8, **6.3** | [One short sentence describing the step] | [Links to relevant design logs, operations docs, artifacts, code files, research papers, etc. May be left empty before implementation/planning of this step starts] |

#### Step 1 details

[High level details about the step, including what needs to be done, how it should be done, and any relevant information. For implementation: include technical details, file paths, type signatures, data structures, API endpoints, charts and diagrams etc. For research: describe research activities, data sources, analysis approach, etc.]

#### Step 1 comments from other steps/locations

[If there are relevant comments from other design logs, operations docs, code reviews, steps, etc. that provide context or information for this step, they can be included here. This is especially useful if the step is related to or dependent on work done in other places.]

#### Step 1 lessons learned from this step that are only relevant as context for looking into this step in the future

[When implementing this step, there may be specific insights, challenges, or decisions that are particularly relevant for anyone looking at this step in the future. This section can be used to document those lessons learned, which can provide valuable context and guidance for future work related to this step.]

### Step 2: [Title of Step 2]

[etc. etc.]

### Learnings from all steps

[Lessons learned/important actions taken during the implementation of the steps that are relevant for the overall design log and not just for a specific step. This can include insights about the problem, the solution, the process, or any other aspect that is important to document for future reference.]

### Deviations from Original Plan

[Document any significant deviations from the original plan, including changes in approach, unexpected challenges, or new insights that led to adjustments in the design or implementation. This section helps provide context for why certain decisions were made and how the final outcome may differ from the initial plan.]
