# Decomposition Quality Checklist

Use this checklist to validate the quality of a task decomposition before starting implementation.

## Completeness

- [ ] **100% rule**: All work required by the objective is captured in tasks (no gaps)
- [ ] **No extras**: No tasks fall outside the objective scope
- [ ] **All layers covered**: Every affected layer (model, schema, service, router, hook, component, test) has corresponding tasks
- [ ] **Testing included**: Test tasks cover unit, integration, and E2E as appropriate

## Atomicity

- [ ] **Max 3 files per task**: No task touches more than 3 files
- [ ] **Max 200 lines per task**: No task changes more than 200 lines
- [ ] **Single outcome**: Each task has one clear, testable result
- [ ] **Split if needed**: Large tasks have been broken into smaller ones

## Verification

- [ ] **Every task has "Done when"**: No tasks missing verification commands
- [ ] **Commands are runnable**: Verification commands can be executed (not "it should work")
- [ ] **Tests exist or are created**: Verification relies on automated tests where possible
- [ ] **Incremental validity**: The codebase passes all tests after each task completes

## Dependencies

- [ ] **Preconditions declared**: Every task (except the first) lists its preconditions
- [ ] **No circular dependencies**: The dependency graph is acyclic
- [ ] **No orphaned tasks**: Every task is either a root (no preconditions) or reachable from a root
- [ ] **Parallelism identified**: Independent tasks are marked as parallelizable

## Complexity Sizing

- [ ] **All tasks sized**: Every task has a complexity assignment
- [ ] **Sizing is consistent**: Similar tasks have similar complexity ratings
- [ ] **No oversized tasks**: Tasks rated "large" have been reviewed for potential splitting
- [ ] **Method matches context**: Sizing method appropriate for the audience (dev vs. roadmap)

## AI Agent Readiness (if applicable)

- [ ] **Context provided**: Each task lists relevant files to read, not just files to modify
- [ ] **Constraints explicit**: "Do NOT modify" lists included where needed
- [ ] **Small increments**: Tasks are small enough for single-shot agent execution
- [ ] **Verification automated**: All "Done when" commands can run without human judgment

## Persistent Files

- [ ] **task_plan.md created**: Complete task list saved to disk
- [ ] **progress.md created**: Initial progress tracker created
- [ ] **findings.md planned**: Template ready for implementation notes
