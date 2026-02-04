---
name: task-decomposition
description: >-
  Decompose high-level objectives into atomic implementation tasks for Python/React
  projects. Use when breaking down large features, multi-file changes, migrations,
  refactoring, or event-driven microservices work requiring more than 3 steps. Supports
  layer-based, feature-first, and migration decomposition strategies. Produces
  independently-verifiable tasks with done-conditions, file paths, complexity estimates,
  testing pyramid alignment, and explicit ordering. Includes AI agent task structuring
  guidance for Claude Code, Cursor, and Copilot workflows. Creates persistent task
  files (task_plan.md, progress.md) to track state across context windows. Does NOT
  cover high-level planning (use project-planner) or architecture decisions (use
  system-architecture).
license: MIT
compatibility: 'Python 3.12+, React 18+, FastAPI, TypeScript'
metadata:
  author: platform-team
  version: '2.0.0'
  sdlc-phase: planning
allowed-tools: Read Grep Glob Write Bash
context: fork
---

# Task Decomposition

## When to Use

Activate this skill when:
- A large feature requires 4+ implementation steps
- Multi-file changes span both backend and frontend
- Tracking progress across context windows is needed
- The user says "break this down", "decompose", "create subtasks", or "what are the steps?"
- A previously-planned feature needs to be turned into executable tasks
- Delegating multi-step work to an AI coding agent that needs structured task plans
- Migrating or refactoring existing systems incrementally (strangler fig, domain-by-domain)
- Breaking down event-driven or microservices features across service boundaries

Do NOT use this skill for:
- High-level planning and risk assessment — use `project-planner`
- Architecture decisions — use `system-architecture`
- Single-file changes or trivial fixes — just do them directly

## Instructions

### Decomposition Rules

Every task produced by this skill must satisfy ALL of the following:

1. **Atomic scope**: Touches at most 2-3 files
2. **Independently verifiable**: Has a concrete command that proves completion
3. **Single outcome**: One clear, testable result per task
4. **Explicit preconditions**: Lists which other task IDs must be done first
5. **Sized**: Assigned a complexity (trivial/small/medium/large)

If a task touches >3 files or changes >200 lines, split it further.

**Completeness check (100% rule):** The sum of all tasks must capture 100% of the work defined by the objective — no gaps, no extras. Use `assets/decomposition-checklist.md` to validate decomposition quality before starting implementation.

### Task Template

Use this format for every task (also available as a standalone file in `assets/task-template.md`):

```
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

### Decomposition Strategies

Choose the strategy that fits the objective:

**Strategy 1: Layer-based (default for CRUD features)**

1. **Read the objective** — Understand the full scope from user input or an existing plan
2. **Identify layers** — Which layers are affected? (model, schema, repo, service, router, type, hook, component, page, test)
3. **Create tasks per layer** — One task per layer per feature unit. Default ordering:
   - Infrastructure and shared code first
   - Database models and migrations
   - Backend schemas (Pydantic)
   - Backend repository
   - Backend service
   - Backend router/endpoint
   - Shared TypeScript types
   - Frontend API service
   - Frontend hooks
   - Frontend components and pages
   - Tests (unit per layer, then integration, then E2E)
4. **Map dependencies** — Draw precondition chains. Look for parallelization opportunities.
5. **Assign complexity** — See complexity sizing below
6. **Write persistent files** — Save decomposition to disk (see below). Use `scripts/decompose.py` to generate task_plan.md and progress.md from structured input.

**Strategy 2: Feature-first (for domain-driven or microservices work)**

1. Identify bounded contexts or feature domains affected
2. Decompose by feature slice — each task delivers a vertical slice through the stack
3. Order by domain dependency (core domain first, supporting domains second)
4. Include integration tasks between feature boundaries

**Strategy 3: Migration/refactoring (for brownfield work)**

1. Identify the migration pattern (strangler fig, domain-by-domain, big bang)
2. Create tasks that maintain backward compatibility at each step
3. Include data migration tasks with rollback steps
4. Add verification tasks that confirm old and new paths produce identical results
5. Order tasks so the system remains deployable after each task completes

### Complexity Sizing

Use these heuristics:
- **Trivial**: 1 file, <20 lines, no new tests needed
- **Small**: 1-2 files, <100 lines, unit tests
- **Medium**: 2-3 files, <200 lines, unit + integration tests
- **Large**: 3+ files, 200+ lines, full test coverage

Alternative sizing approaches (use when collaborating with product teams):
- **T-shirt sizing** (XS/S/M/L/XL) — for early estimation or roadmap-level planning
- **Fibonacci points** (1/2/3/5/8/13) — for sprint planning with velocity tracking

For detailed comparison of all methods with selection guidance, see `references/complexity-guide.md`.

### Testing Task Patterns

Align test tasks with the testing pyramid (70% unit / 20% integration / 10% E2E):

- **Unit test tasks**: Create alongside or immediately after each layer implementation task. Verification: `pytest tests/unit/` or `npm test`
- **Integration test tasks**: Create after backend endpoint tasks complete. Verification: `pytest tests/integration/`
- **E2E test tasks**: Create only for critical user journeys after full-stack tasks complete. Verification: `npx playwright test`
- **Contract test tasks**: For microservices, add contract tests at service boundaries to validate API schemas between producer and consumer

When using TDD, structure each implementation task as: write failing test → implement → verify green.

### Decomposing for AI Agents

When tasks will be executed by AI coding agents (Claude Code, Cursor, Copilot):

1. **Provide context in each task** — List the relevant files the agent needs to read, not just the files to modify. Include architectural constraints and patterns to follow.
2. **Keep tasks small** — AI agents perform best with focused, single-purpose tasks. Prefer many small tasks over fewer large ones.
3. **Include verification commands** — Every task must have a runnable verification command. AI agents use test results as feedback loops to self-correct.
4. **Specify what NOT to change** — Agents may over-modify. Explicitly list files or patterns that should remain untouched.
5. **Order for incremental verification** — Each completed task should leave the codebase in a passing state. Never create tasks that require multiple completions before tests pass.

### Persistent Task Files

Create these files in the project root to track state across context windows:

**task_plan.md** — The complete task list:
```markdown
# Task Plan: [Feature Name]

Status: IN_PROGRESS
Total tasks: [N]
Completed: [M]

[All tasks in template format]
```

**progress.md** — Current state:
```markdown
# Progress

## Current Task
Task [N]: [Title]
Status: [not started | in progress | blocked | done]

## Completed
- [x] Task 1: [Title]
- [x] Task 2: [Title]

## Next Up
- [ ] Task 3: [Title]

## Blockers
[Any issues discovered during work]
```

**findings.md** — Notes discovered during implementation:
```markdown
# Findings

## Decisions Made
- [decision and rationale]

## Blockers Encountered
- [blocker and resolution]

## Scope Changes
- [any tasks added or removed and why]
```

Update these files after completing each task. This allows recovery if the context window resets.

Run `scripts/validate-plan.py task_plan.md` to check the plan against decomposition rules (atomicity, verification commands, dependency cycles, complexity sizing).

### Prioritization Rules

When multiple tasks have no dependency between them, prioritize in this order:
1. Infrastructure and configuration
2. Shared code and types
3. Backend implementation
4. Frontend implementation
5. Tests
6. Documentation

### Handling Scope Changes

If during implementation you discover:
- A task is larger than estimated → Split it and update task_plan.md
- A new task is needed → Add it with correct preconditions
- A task is unnecessary → Mark as "SKIPPED" with reason
- A circular dependency exists → Restructure to break the cycle

Always update the persistent files when scope changes.

## Examples

For additional worked examples (JWT auth, file upload, pagination, event-driven migration, feature-first refactoring), see `references/decomposition-examples.md`.

### Example 1: Decompose "Add Search to Users List" (Layer-based)

**Objective:** Add server-side search to the users list page with debounced input.

**Tasks:**

### Task 1: Add search query parameter to user repository
- **Files:** `app/repositories/user_repository.py`
- **Preconditions:** none
- **Steps:**
  1. Add `search(self, query: str, limit: int, offset: int)` method
  2. Use `ilike` for case-insensitive search on name and email
- **Done when:** `pytest tests/unit/test_user_repository.py -k test_search` passes
- **Complexity:** small
- **Parallel:** Can run alongside Task 2

### Task 2: Add search schema
- **Files:** `app/schemas/user.py`
- **Preconditions:** none
- **Steps:**
  1. Add `UserSearchParams` schema with `q: str | None`, `limit: int`, `offset: int`
- **Done when:** Schema validates with sample data
- **Complexity:** trivial
- **Parallel:** Can run alongside Task 1

### Task 3: Add search endpoint
- **Files:** `app/routers/users.py`, `app/services/user_service.py`
- **Preconditions:** Task 1, Task 2
- **Steps:**
  1. Add `search_users` method to service
  2. Add `GET /users/search?q=&limit=&offset=` endpoint
- **Done when:** `pytest tests/integration/test_users.py -k test_search_users` passes
- **Complexity:** small

### Task 4: Add frontend search hook
- **Files:** `src/hooks/useSearchUsers.ts`
- **Preconditions:** Task 3
- **Steps:**
  1. Create hook using `useQuery` with debounced search parameter
  2. Query key: `['users', 'search', { q, limit, offset }]`
- **Done when:** `npm test -- useSearchUsers` passes
- **Complexity:** small

### Task 5: Add search input to users page
- **Files:** `src/pages/UsersPage.tsx`, `src/components/SearchInput.tsx`
- **Preconditions:** Task 4
- **Steps:**
  1. Create `SearchInput` component with debounce (300ms)
  2. Integrate into `UsersPage` with `useSearchUsers` hook
- **Done when:** Search input renders, typing triggers debounced API call, results update
- **Complexity:** medium

### Example 2: Decompose "Migrate Notifications to Event-Driven" (Migration strategy)

**Objective:** Replace synchronous notification calls with an event-driven system using Kafka.

### Task 1: Add event schema definitions
- **Files:** `app/events/schemas.py`
- **Preconditions:** none
- **Steps:**
  1. Define `NotificationEvent` Pydantic model with event_type, payload, timestamp, correlation_id
  2. Define `EventEnvelope` wrapper with metadata
- **Done when:** `pytest tests/unit/test_event_schemas.py` passes
- **Complexity:** trivial

### Task 2: Create event producer service
- **Files:** `app/services/event_producer.py`, `app/core/kafka.py`
- **Preconditions:** Task 1
- **Steps:**
  1. Configure Kafka producer in `app/core/kafka.py`
  2. Create `EventProducer.publish(event)` method with serialization and error handling
- **Done when:** `pytest tests/unit/test_event_producer.py` passes (with mocked Kafka)
- **Complexity:** medium

### Task 3: Add event consumer for notifications
- **Files:** `app/consumers/notification_consumer.py`
- **Preconditions:** Task 1, Task 2
- **Steps:**
  1. Create consumer that subscribes to notification topic
  2. Route events to existing notification service methods
- **Done when:** `pytest tests/integration/test_notification_consumer.py` passes
- **Complexity:** medium

### Task 4: Dual-write in existing notification calls (strangler)
- **Files:** `app/services/notification_service.py`
- **Preconditions:** Task 2
- **Steps:**
  1. At each synchronous notification call, also publish the event
  2. Keep existing synchronous path working (dual-write)
- **Done when:** `pytest tests/integration/test_notifications.py` passes AND events appear in test Kafka topic
- **Complexity:** medium

### Task 5: Switch to event-only path and remove synchronous calls
- **Files:** `app/services/notification_service.py`, `app/routers/notifications.py`
- **Preconditions:** Task 3, Task 4
- **Steps:**
  1. Remove synchronous notification calls, keep only event publishing
  2. Verify consumer handles all notification types
- **Done when:** `pytest tests/integration/` passes with no synchronous notification calls remaining
- **Complexity:** medium

## Edge Cases

- **Tasks with circular dependencies**: Restructure by extracting the shared dependency into its own task that both can depend on. If truly circular, combine into one task.
- **Tasks that are hard to verify in isolation**: Add a lightweight integration test as the verification command. If the only way to verify is manual testing, document the manual steps explicitly.
- **Context window running out**: Immediately save current state to progress.md and findings.md. The next context can resume by reading these files.
- **Scope explosion**: If decomposition produces >15 tasks, group related tasks into phases. Complete phase 1 before decomposing phase 2 in detail.
- **External dependency blocking**: Mark the task as "BLOCKED" in progress.md with the reason. Continue with non-blocked tasks.
- **Microservices cross-service tasks**: When a task requires changes in multiple services, split into one task per service with explicit contract agreements. Add a contract test task to verify compatibility.
- **Migration rollback needs**: For each migration task, document the rollback procedure in the task steps. The system must be deployable after each task, including the ability to revert.
- **AI agent over-modifying**: If an AI agent changes files outside the task scope, add explicit "Do NOT modify" constraints to the task template. Review diffs after each agent-executed task.
