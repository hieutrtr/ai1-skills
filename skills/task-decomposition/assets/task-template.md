# Task Template

Standalone task template for generating task plans. Can be used by scripts and agents.

## Single Task

```markdown
### Task [N]: [Title]
- **Files:** [list of files to create/modify]
- **Preconditions:** [task IDs that must be done first, or "none"]
- **Steps:**
  1. [concrete action]
  2. [concrete action]
- **Done when:** [exact verification command and expected output]
- **Complexity:** trivial | small | medium | large
- **Parallel:** [can run alongside Task X | must be sequential]
```

## Task Plan Header

```markdown
# Task Plan: [Feature Name]

Status: IN_PROGRESS | COMPLETED | BLOCKED
Total tasks: [N]
Completed: [M]
Strategy: layer-based | feature-first | migration

---
```

## Progress File

```markdown
# Progress

## Current Task
Task [N]: [Title]
Status: not started | in progress | blocked | done

## Completed
- [x] Task 1: [Title]

## Next Up
- [ ] Task 2: [Title]

## Blockers
[Any issues discovered during work]
```

## Findings File

```markdown
# Findings

## Decisions Made
- [decision and rationale]

## Blockers Encountered
- [blocker and resolution]

## Scope Changes
- [any tasks added or removed and why]
```
