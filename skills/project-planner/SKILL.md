---
name: project-planner
description: >-
  Project planning and feature breakdown for Python/React full-stack projects.
  Use during the planning phase when breaking down feature requests, user stories,
  or product requirements into implementation plans. Covers React 19 Server Components
  planning, version migration (React 18→19, FastAPI, TypeScript 7), AI-assisted task
  decomposition, monorepo setup, real-time WebSocket features, and TanStack Query v5
  integration. Guides identification of affected files and modules, defines acceptance
  criteria, maps task dependencies, and estimates complexity. Produces structured task
  lists with file paths and verification steps. Does NOT cover architecture decisions
  (use system-architecture) or implementation (use python-backend-expert or
  react-frontend-expert).
license: MIT
compatibility: 'Python 3.12+, React 19+, FastAPI, SQLAlchemy 2.0+, Pydantic v2, TypeScript 5.2+, TanStack Query v5'
metadata:
  author: platform-team
  version: '1.1.0'
  sdlc-phase: planning
allowed-tools: Read Grep Glob WebSearch
context: fork
---

# Project Planner

## When to Use

Activate this skill when:
- Breaking down feature requests or user stories into implementation tasks
- Sprint planning or backlog refinement for a Python/React project
- Planning a new module, service, or cross-cutting feature
- Estimating complexity of a proposed change
- Identifying dependencies between tasks before starting implementation
- A stakeholder asks "how should we build this?"
- Planning a React major version migration (e.g., 18→19) with deprecation removal and new API adoption
- Using AI tools to assist with project planning draft generation and task decomposition
- Planning features that involve deciding between React Server Components and client components

Do NOT use this skill for:
- Architecture decisions (component boundaries, technology choices) — use `system-architecture`
- Generating implementation code — use `python-backend-expert` or `react-frontend-expert`
- API contract design — use `api-design-patterns`
- Breaking down tasks that are already well-defined into subtasks — use `task-decomposition`

## Instructions

### Planning Workflow

Follow these five steps in order for every planning request.

#### Step 1: Analyze the Requirement

1. Read the feature request, user story, or product requirement in full
2. Identify the **inputs** (what triggers the feature) and **outputs** (what the user sees or what changes)
3. List any **ambiguities** — questions that must be answered before implementation
4. If ambiguities exist, ask the user to clarify before proceeding
5. Write a one-sentence **objective statement**: "This feature allows [who] to [do what] so that [why]"

#### Step 2: Map Affected Modules

Identify every file and module that will be created or modified. Use this checklist:

**Backend (Python/FastAPI):**
- Routes: `app/routers/` — new or modified endpoint files (or domain-based: `app/{domain}/routes.py`)
- Services: `app/services/` — business logic modules
- Repositories: `app/repositories/` — data access layer
- Models: `app/models/` — SQLAlchemy ORM models (use `Mapped`/`mapped_column` style)
- Schemas: `app/schemas/` — Pydantic v2 request/response models
- Migrations: `alembic/versions/` — database migration files
- Dependencies: `app/dependencies.py` — FastAPI Depends() additions
- Config: `app/core/config.py` — new settings or environment variables
- Lifespan: `app/main.py` — use lifespan event handlers (not deprecated `on_event`)

Note: For larger projects, consider **domain-based organization** (`app/{domain}/routes.py`, `app/{domain}/service.py`, `app/{domain}/models.py`) instead of file-type organization.

**Frontend (React/TypeScript):**
- Pages: `src/pages/` — new or modified page components
- Components: `src/components/` — shared or feature-specific components
- Server Components: identify which components can be server-rendered (React 19 RSC) vs client-only
- Hooks: `src/hooks/` — custom hooks (useXxx), TanStack Query hooks (`useQuery`, `useSuspenseQuery`)
- Services: `src/services/` — API client functions
- Types: `src/types/` — TypeScript interfaces and types
- Tests: `src/__tests__/` or co-located `.test.tsx` files

**Shared:**
- API contract: OpenAPI schema changes
- Environment variables: `.env` additions
- Dependencies: `requirements.txt` / `package.json` additions

Run `Glob` and `Grep` on the codebase to confirm which files already exist and which must be created.

#### Step 3: Decompose into Tasks

Break the feature into ordered implementation tasks. Each task must satisfy:
- **Touches 1-3 files** — if more, split further
- **Has a single clear outcome** — one testable result
- **Includes a verification command** — `pytest`, `npm test`, manual check, or API call
- **Has explicit preconditions** — which tasks must be done first

Use this ordering principle:
1. Database model changes and migrations
2. Backend schemas (Pydantic models)
3. Backend repository layer
4. Backend service layer
5. Backend route/endpoint
6. Shared types (if TypeScript types generated from OpenAPI)
7. Frontend API service functions
8. Frontend hooks
9. Frontend components and pages
10. Tests for each layer (can be interleaved with TDD)
11. Integration and E2E tests

#### Step 4: Define Verification Steps

For each task, specify:
- **Command to run**: exact CLI command (e.g., `pytest tests/unit/test_users.py -k test_create_user`)
- **Expected result**: what "pass" looks like (status code, output text, behavior)
- **Rollback if failed**: what to undo or check if verification fails

#### Step 5: Identify Risks and Unknowns

Review the plan against common risk categories. See `references/risk-assessment-checklist.md` for the full checklist. Flag any item that applies:
- Data migration risks (schema changes, data loss potential)
- API breaking changes (existing consumers affected)
- Authentication/authorization changes (security surface changes)
- Performance regression (new queries, additional API calls, large payloads)
- Third-party dependency risks (new packages, version conflicts)
- Cross-cutting concerns (middleware changes, shared utility changes)
- Framework/library version migration (React 19 deprecations, SQLAlchemy 2.1 changes, TypeScript 7 strict-by-default) — see `references/migration-planning-guide.md`
- AI-generated code risks (review all AI-suggested code for security, correctness, and maintainability)

### Output Format

Produce a structured plan document following the template in `references/plan-template.md`. You can also use `scripts/plan-generator.py` to generate an initial plan scaffold from CLI arguments (run with `--help` for options). The plan must include:

1. **Objective** — one sentence
2. **Affected Modules** — file paths grouped by layer
3. **Task List** — ordered tasks with files, preconditions, verification
4. **Dependency Graph** — which tasks block which
5. **Risk Assessment** — flagged risks with mitigation
6. **Acceptance Criteria** — how to verify the feature is complete
7. **Estimated Complexity** — overall sizing (see below)

### Estimation Heuristics

| Size | Files | Lines Changed | Tests Needed | Typical Duration |
|------|-------|---------------|-------------|-----------------|
| Trivial | 1 file | <20 lines | None or 1 unit test | — |
| Small | 1-2 files | <100 lines | Unit tests | — |
| Medium | 3-5 files | <300 lines | Unit + integration tests | — |
| Large | 6+ files | 300+ lines | Full test suite, may need migration | — |

Assign a size to each task AND to the overall feature.

### Dependency Mapping Rules

- Database model changes **must precede** service layer changes
- Backend API endpoints **must precede** frontend integration
- Shared types and schemas **must precede** both backend and frontend consumers
- Tests should follow implementation of each layer (or precede with TDD)
- Migrations **must be tested** before deploying dependent code
- If two tasks have no dependency, they can be worked in parallel — note this explicitly

### Common Planning Patterns for FastAPI + React

**CRUD Feature:**
1. Model + migration → 2. Schemas → 3. Repository → 4. Service → 5. Router → 6. Frontend service → 7. Hook → 8. Component → 9. Tests

**Auth-Protected Feature:**
1. Auth dependency (if new) → 2. Permission model → 3-9. Same as CRUD with auth decorators

**Search/Filter Feature:**
1. Query parameters schema → 2. Repository filter method → 3. Service + router → 4. Frontend hook with debounce → 5. Search component → 6. Tests

**File Upload Feature:**
1. Storage service → 2. Upload endpoint (multipart) → 3. Model field for file reference → 4. Frontend upload component → 5. Preview component → 6. Tests

**Real-Time/WebSocket Feature:**
1. WebSocket endpoint + connection manager → 2. Event schemas → 3. Backend event dispatcher → 4. Frontend WebSocket hook → 5. Real-time UI component → 6. Reconnection/error handling → 7. Tests

**React Version Migration (e.g., 18→19):**
1. Dependency audit (React, React DOM, related packages) → 2. Deprecated API inventory (`forwardRef`, `<Context.Provider>`, class components) → 3. Codemod execution → 4. Manual fixes for codemod gaps → 5. Server Component opportunities identification → 6. React Compiler enablement → 7. Test suite update → 8. Performance verification

**Monorepo Setup:**
1. Choose tooling (Nx, Turborepo, Pants) → 2. Define workspace structure (`apps/`, `packages/`) → 3. Configure shared dependencies → 4. Set up build pipeline with caching → 5. Migrate existing code → 6. Update CI/CD → 7. Document conventions

## Examples

### Example: Add User Profile Picture Upload

**Objective:** Allow users to upload and display a profile picture.

**Affected Modules:**
- Backend: `app/models/user.py`, `app/schemas/user.py`, `app/services/storage_service.py` (new), `app/routers/users.py`, `alembic/versions/xxx_add_avatar_url.py`
- Frontend: `src/components/AvatarUpload.tsx` (new), `src/hooks/useUploadAvatar.ts` (new), `src/pages/ProfilePage.tsx`, `src/services/userService.ts`

**Task List:**
1. **Add avatar_url column** — Files: `app/models/user.py`, `alembic/versions/` — Preconditions: none — Verify: `alembic upgrade head` succeeds, column exists
2. **Create storage service** — Files: `app/services/storage_service.py` — Preconditions: none — Verify: unit test passes
3. **Add avatar schemas** — Files: `app/schemas/user.py` — Preconditions: Task 1 — Verify: schema validates
4. **Add upload endpoint** — Files: `app/routers/users.py` — Preconditions: Tasks 2, 3 — Verify: `pytest tests/integration/test_users.py -k test_upload_avatar`
5. **Add frontend upload hook** — Files: `src/hooks/useUploadAvatar.ts` — Preconditions: Task 4 — Verify: `npm test -- useUploadAvatar`
6. **Add AvatarUpload component** — Files: `src/components/AvatarUpload.tsx` — Preconditions: Task 5 — Verify: component renders, handles file selection
7. **Integrate into ProfilePage** — Files: `src/pages/ProfilePage.tsx` — Preconditions: Task 6 — Verify: manual test — upload, refresh, avatar displays

**Complexity:** Medium (7 tasks, 9 files, unit + integration tests)

### Example: Plan React 18→19 Migration

**Objective:** Migrate the frontend from React 18 to React 19, removing deprecated APIs and enabling Server Components.

**Affected Modules:**
- Frontend: `package.json`, all files using `forwardRef`, `<Context.Provider>`, class components, `ReactDOM.render()`
- Config: `tsconfig.json` (TypeScript 5.2+ required), `vite.config.ts` (React Compiler plugin)

**Task List:**
1. **Upgrade React dependencies** — Files: `package.json` — Preconditions: none — Verify: `npm install` succeeds, `npm run build` passes
2. **Run React 19 codemod** — Files: all `.tsx`/`.ts` — Preconditions: Task 1 — Verify: codemod report shows changes applied
3. **Replace forwardRef usage** — Files: components using `forwardRef` — Preconditions: Task 2 — Verify: `grep -r "forwardRef" src/` returns zero results
4. **Replace Context.Provider** — Files: context providers — Preconditions: Task 2 — Verify: `grep -r "Context.Provider" src/` returns zero results
5. **Enable React Compiler** — Files: `vite.config.ts` — Preconditions: Tasks 3, 4 — Verify: build succeeds with compiler plugin, remove manual `useMemo`/`useCallback`
6. **Identify RSC candidates** — Files: read-heavy pages — Preconditions: Task 5 — Verify: documented list of Server Component candidates
7. **Run full test suite** — Preconditions: Task 6 — Verify: all existing tests pass, performance benchmarks stable

**Complexity:** Large (7 tasks, many files, full test suite, migration risk)

### Example: Plan Real-Time Notifications

**Objective:** Add real-time push notifications using WebSocket so users see alerts without refreshing.

**Affected Modules:**
- Backend: `app/services/notification_service.py` (new), `app/routers/ws.py` (new), `app/models/notification.py`, `alembic/versions/`
- Frontend: `src/hooks/useNotifications.ts` (new), `src/components/NotificationBell.tsx` (new), `src/services/wsClient.ts` (new)

**Task List:**
1. **Add notification model** — Files: `app/models/notification.py`, `alembic/versions/` — Preconditions: none — Verify: migration applies
2. **Create WebSocket manager** — Files: `app/services/notification_service.py` — Preconditions: none — Verify: unit test
3. **Add WebSocket endpoint** — Files: `app/routers/ws.py` — Preconditions: Tasks 1, 2 — Verify: `websocat ws://localhost:8000/ws` connects
4. **Add frontend WebSocket client** — Files: `src/services/wsClient.ts` — Preconditions: Task 3 — Verify: connects and receives test message
5. **Add useNotifications hook** — Files: `src/hooks/useNotifications.ts` — Preconditions: Task 4 — Verify: hook returns notifications array
6. **Add NotificationBell component** — Files: `src/components/NotificationBell.tsx` — Preconditions: Task 5 — Verify: renders bell with count badge, dropdown shows notifications
7. **Add reconnection handling** — Files: `src/services/wsClient.ts` — Preconditions: Task 6 — Verify: auto-reconnects after disconnect

**Complexity:** Large (7 tasks, 8 files, WebSocket complexity, reconnection logic)

## Edge Cases

- **Cross-cutting changes** (auth middleware, error handling, logging): Flag for architecture review before planning implementation. These affect many files and may need their own planning session.
- **Database migrations with data transformation**: Always plan the migration as a separate task with its own rollback strategy. Never combine schema migration with data migration in one step.
- **Frontend state cascades**: When a change affects shared state (context, global store), map the full component tree that depends on it. Use React DevTools to trace consumers.
- **Breaking API changes**: If an endpoint contract changes, plan a versioning strategy (new endpoint, deprecation header) before implementation. Check who consumes the API.
- **Feature flags**: For large features, consider adding a feature flag task at the beginning. This allows partial deployment and rollback without code revert.
- **Third-party dependency additions**: Verify license compatibility, check for known vulnerabilities (npm audit, pip-audit), and pin exact versions in the plan.
- **React 19 migration deprecation cascade**: When migrating to React 19, deprecated APIs (`forwardRef`, `<Context.Provider>`, class components) may be deeply embedded. Plan a separate codemod task and manual fix pass. Third-party libraries may not support React 19 yet — audit all dependencies first.
- **AI-assisted code planning**: When using AI tools for planning drafts, always have a human review the generated plan for missed dependencies, incorrect file paths, and hallucinated APIs. AI excels at structure but may miss project-specific constraints.
- **Monorepo build pipeline**: Monorepo setups add CI/CD complexity (selective builds, dependency graph analysis, caching). Plan the build pipeline configuration as a separate task stream. Choose tooling before migrating code.
- **TypeScript major version upgrade**: TypeScript 7 (mid-2026) will enforce strict mode by default, drop ES5/AMD/UMD targets, and remove classic module resolution. Plan a separate migration task if upgrading. Audit `tsconfig.json` compatibility before updating.
