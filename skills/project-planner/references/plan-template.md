# Implementation Plan: [Feature Name]

## Metadata

- **Date:** [YYYY-MM-DD]
- **Author:** [name]
- **Status:** Draft | In Review | Approved
- **Complexity:** Trivial | Small | Medium | Large

## Objective

[One sentence describing what this feature does and why.]

## Affected Modules

### Backend (Python/FastAPI)

| Layer | File Path | Action | Notes |
|-------|----------|--------|-------|
| Model | `app/models/xxx.py` | Create/Modify | [description] |
| Migration | `alembic/versions/xxx.py` | Create | [description] |
| Schema | `app/schemas/xxx.py` | Create/Modify | [description] |
| Repository | `app/repositories/xxx.py` | Create/Modify | [description] |
| Service | `app/services/xxx.py` | Create/Modify | [description] |
| Router | `app/routers/xxx.py` | Create/Modify | [description] |
| Dependency | `app/dependencies.py` | Modify | [description] |
| Config | `app/core/config.py` | Modify | [description] |

### Frontend (React/TypeScript)

| Layer | File Path | Action | Notes |
|-------|----------|--------|-------|
| Type | `src/types/xxx.ts` | Create/Modify | [description] |
| Service | `src/services/xxxService.ts` | Create/Modify | [description] |
| Query Hook | `src/hooks/useXxxQuery.ts` | Create | TanStack Query hook (useSuspenseQuery/useQuery) |
| Hook | `src/hooks/useXxx.ts` | Create | [description] |
| Server Component | `src/components/XxxServer.tsx` | Create | RSC — renders on server, zero client JS |
| Client Component | `src/components/Xxx.tsx` | Create/Modify | 'use client' — interactive, uses hooks/state |
| Page | `src/pages/XxxPage.tsx` | Create/Modify | [description] |

### Server Component Decision

For each new component, determine rendering strategy:
- **Server Component** (default in React 19): data fetching, static content, no interactivity → zero client JS
- **Client Component** (`'use client'`): needs hooks, event handlers, browser APIs, or state
- **Hybrid**: Server Component wrapper with Client Component islands for interactive parts

### Tests

| Type | File Path | Coverage |
|------|----------|----------|
| Unit (backend) | `tests/unit/test_xxx.py` | [what it tests] |
| Integration | `tests/integration/test_xxx.py` | [what it tests] |
| Unit (frontend) | `src/__tests__/Xxx.test.tsx` | [what it tests] |
| E2E | `tests/e2e/xxx.spec.ts` | [what it tests] |

### Other

| File | Action | Notes |
|------|--------|-------|
| `.env` | Modify | [new variables] |
| `requirements.txt` | Modify | [new packages] |
| `package.json` | Modify | [new packages] |

## Task List

### Task 1: [Title]

- **Files:** [list]
- **Preconditions:** None | Task [N]
- **Steps:**
  1. [step]
  2. [step]
- **Verify:** `[command]` — expect [result]
- **Complexity:** Trivial | Small | Medium | Large
- **Parallel:** Can run alongside Task [N] | Must be sequential

### Task 2: [Title]

[same structure]

## Dependency Graph

```
Task 1 (Model + Migration)
  └── Task 2 (Schemas)
       ├── Task 3 (Repository)
       │    └── Task 4 (Service)
       │         └── Task 5 (Router)
       │              └── Task 7 (Frontend Service)
       │                   └── Task 8 (Hook + Component)
       └── Task 6 (Shared Types) ──┘
```

Parallel opportunities:
- Tasks [X] and [Y] can run in parallel
- Tasks [A] and [B] have no dependency

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk 1] | Low/Med/High | Low/Med/High | [action] |
| [risk 2] | Low/Med/High | Low/Med/High | [action] |

See `references/risk-assessment-checklist.md` for full risk category checklist.

## Acceptance Criteria

- [ ] [Criterion 1: specific, testable condition]
- [ ] [Criterion 2: specific, testable condition]
- [ ] [Criterion 3: specific, testable condition]
- [ ] All new code has unit tests with >80% coverage
- [ ] Integration tests pass
- [ ] No security vulnerabilities introduced (code-review-security passes)
- [ ] Pre-merge checklist passes

## Migration Considerations

If this plan involves a framework/library version migration, see `references/migration-planning-guide.md` for:
- Deprecated API inventory and codemod strategy
- Version compatibility matrix
- Phased migration approach
- Rollback plan

## AI-Assisted Planning Notes

If AI tools were used to generate this plan:
- [ ] Human reviewed all file paths for accuracy
- [ ] Dependency graph verified manually
- [ ] No hallucinated APIs or non-existent libraries referenced
- [ ] Risk assessment includes AI-specific risks (generated code review, test coverage of AI output)

## Notes

[Any additional context, open questions, or decisions made during planning.]
