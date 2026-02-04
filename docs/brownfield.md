# Brownfield Project Guide

> **[← README](../README.md)** | [Greenfield Guide](greenfield.md) | [Skill Composition](skill-composition.md)

How to use AI1 Skills when integrating into an existing Python (FastAPI) + React codebase. Unlike greenfield, you start by understanding what exists, then adopt skills incrementally where they add the most value.

## Workflow Overview

```mermaid
flowchart TD
    Start([Existing Codebase]) --> Assess

    subgraph Assess["Phase 0: Assess Current State"]
        direction LR
        Understand["Understand codebase<br/>structure & patterns"] --> Gaps["Identify gaps<br/>testing, security,<br/>monitoring"]
    end

    Assess --> Quick

    subgraph Quick["Quick Wins (Week 1)"]
        direction LR
        SEC["/code-review-security<br/>Find vulnerabilities"] --> MON["/monitoring-setup<br/>Add observability"]
        MON --> PMC["/pre-merge-checklist<br/>Enforce quality gates"]
    end

    Quick --> Fill

    subgraph Fill["Fill Gaps (Week 2-3)"]
        direction LR
        PT["/pytest-patterns<br/>Add missing tests"]
        RT["/react-testing-patterns<br/>Add component tests"]
        E2E["/e2e-testing<br/>Add critical path tests"]
        PT --> E2E
        RT --> E2E
    end

    Fill --> Align

    subgraph Align["Align Patterns (Ongoing)"]
        direction LR
        BE["/python-backend-expert<br/>Standardize backend code"]
        FE["/react-frontend-expert<br/>Standardize frontend code"]
        FP["/fastapi-patterns<br/>Improve middleware/auth"]
    end

    Align --> New

    subgraph New["New Features (Ongoing)"]
        direction LR
        PP["/project-planner"] --> TD["/task-decomposition"]
        TD --> TDD["/tdd-workflow"]
    end

    Quick --> IR["/incident-response<br/>Create runbooks"]
    Fill --> DOC["/docker-best-practices<br/>Improve containers"]
    Align --> DEP["/deployment-pipeline<br/>Improve CI/CD"]

    New --> Production([Improved Codebase])
```

## Key difference from greenfield

In a greenfield project, you follow phases 1-8 in order. In a brownfield project, you:

1. **Start with operations and review skills** — they provide immediate value without changing existing code
2. **Fill testing gaps** — add coverage to existing code before modifying it
3. **Adopt implementation skills gradually** — apply patterns to new code, refactor old code incrementally
4. **Use planning skills for new features** — not for understanding existing code

```mermaid
quadrantChart
    title Skill Adoption Priority for Brownfield Projects
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Do First
    quadrant-2 Plan Carefully
    quadrant-3 Do Later
    quadrant-4 Quick Wins
    code-review-security: [0.25, 0.85]
    pre-merge-checklist: [0.30, 0.80]
    monitoring-setup: [0.35, 0.75]
    incident-response: [0.20, 0.65]
    pytest-patterns: [0.50, 0.80]
    react-testing-patterns: [0.55, 0.70]
    e2e-testing: [0.60, 0.75]
    python-backend-expert: [0.65, 0.60]
    fastapi-patterns: [0.70, 0.55]
    react-frontend-expert: [0.65, 0.55]
    docker-best-practices: [0.50, 0.50]
    deployment-pipeline: [0.60, 0.65]
    tdd-workflow: [0.45, 0.50]
    project-planner: [0.30, 0.45]
    task-decomposition: [0.30, 0.40]
    system-architecture: [0.75, 0.45]
    api-design-patterns: [0.70, 0.40]
```

---

## Step-by-step guide

### Step 0: Install and assess

Install the skills:

```bash
npx skills add hieutrtr/ai1-skills
```

Before using any implementation skills, understand your codebase's current state. Don't let skills impose patterns that conflict with existing conventions.

**Understand the existing structure:**

```
Explain the project structure — what frameworks are used, how code is organized,
what patterns exist for the backend and frontend.
```

**Identify gaps:**

```
What testing, security, and monitoring gaps exist in this codebase?
```

Document what you find. This assessment determines which skills to adopt first.

---

### Step 1: Quick wins — security and observability

These skills are read-only or additive. They don't change existing code patterns, so there's zero risk of breaking things.

#### Security audit

```
/code-review-security Audit the entire codebase for security vulnerabilities
```

```mermaid
flowchart TD
    Scan["/code-review-security"] --> Report["Security Report"]
    Report --> Crit{"Critical or<br/>High findings?"}
    Crit -->|Yes| Fix["Fix immediately<br/>before other work"]
    Crit -->|No| Backlog["Add Medium/Low<br/>to backlog"]
    Fix --> Rescan["/code-review-security<br/>Verify fixes"]
```

**What happens:** Claude scans for OWASP Top 10 vulnerabilities — SQL injection in raw queries, XSS via `dangerouslySetInnerHTML`, hardcoded secrets, missing auth checks, insecure dependencies. Produces a prioritized findings report.

**Action:** Fix Critical and High findings immediately. Track Medium and Low in your backlog.

#### Add monitoring

```
/monitoring-setup Add structured logging and health check endpoints to the existing API
```

**What happens:** Claude adds structlog configuration, request ID propagation middleware, `/health` and `/ready` endpoints, and Prometheus metrics — all additive, no existing code modified.

**Why first:** You need observability before making changes. If something breaks during the brownfield adoption, you need logs and metrics to diagnose it.

#### Create runbooks

```
/incident-response Create runbooks for this service based on its dependencies
```

**What happens:** Claude analyzes your service's dependencies (database, Redis, external APIs) and creates runbooks for common failure modes with diagnostic commands specific to your setup.

---

### Step 2: Enforce quality gates

Once monitoring is in place, set up quality gates for all future changes:

```
/pre-merge-checklist Set up the pre-merge validation process
```

**What happens:** Claude configures the automated check sequence (ruff, mypy, pytest, tsc, eslint, coverage thresholds) and provides the manual review checklist. From this point, every PR goes through the gate.

```mermaid
flowchart LR
    subgraph "Before Quality Gates"
        Old["Code Review<br/>(ad-hoc, inconsistent)"]
    end

    subgraph "After Quality Gates"
        New1["Automated<br/>ruff + mypy + tsc<br/>pytest + eslint"]
        New2["Security<br/>/code-review-security"]
        New3["Manual<br/>/pre-merge-checklist"]
        New1 --> New2 --> New3
    end

    Old -.->|"Adopt<br/>/pre-merge-checklist"| New1
```

**Key point:** Apply quality gates to new changes only. Don't try to fix every existing lint error at once — that creates a massive, unreviable PR.

---

### Step 3: Fill testing gaps

Before refactoring or modifying existing code, add test coverage to protect against regressions.

```mermaid
flowchart TD
    subgraph "Testing Gap Strategy"
        Measure["Measure current<br/>coverage"] --> Identify["Identify untested<br/>critical paths"]
        Identify --> Backend["/pytest-patterns<br/>Add backend tests<br/>for critical modules"]
        Identify --> Frontend["/react-testing-patterns<br/>Add component tests<br/>for key UI flows"]
        Backend --> E2E["/e2e-testing<br/>Add E2E for<br/>critical user journeys"]
        Frontend --> E2E
        E2E --> Safe["Safe to refactor"]
    end
```

**Start with the most critical, least tested code:**

```
/pytest-patterns Write integration tests for the authentication endpoints
```

```
/pytest-patterns Write tests for the payment service — focus on edge cases
```

**What happens:** Claude uses your existing test setup (or creates `conftest.py` if missing), follows the fixture architecture pattern, creates factories for test data, and writes tests that cover happy paths and edge cases.

**For frontend:**

```
/react-testing-patterns Write tests for the Dashboard and UserProfile components
```

**For critical user flows:**

```
/e2e-testing Write E2E tests for the login → create project → add task flow
```

**Target:** Get critical paths to 80%+ coverage before doing any refactoring.

#### Coverage-first approach

```mermaid
flowchart LR
    subgraph "Module Priority"
        Auth["Auth Module<br/>30% coverage<br/>High risk"]
        Payments["Payments<br/>45% coverage<br/>High risk"]
        Users["Users<br/>70% coverage<br/>Medium risk"]
        Settings["Settings<br/>20% coverage<br/>Low risk"]
    end

    Auth -->|"Test first"| Payments -->|"Test second"| Users -->|"Test third"| Settings
    style Auth fill:#ef4444,color:#fff
    style Payments fill:#f97316,color:#fff
    style Users fill:#eab308,color:#000
    style Settings fill:#22c55e,color:#fff
```

Prioritize by: `risk × (100% - current_coverage)`. High-risk, low-coverage modules first.

---

### Step 4: Standardize new code

Once quality gates and tests are in place, apply implementation skills to **new code only**. Don't rewrite existing code to match patterns — let patterns spread naturally as you add features and fix bugs.

**For new backend features:**

```
/python-backend-expert Add a notifications service with endpoints for user preferences
```

**What happens:** Claude follows the standardized pattern (repository → service → router) even if existing code doesn't. New code becomes the reference pattern for the team.

**For new frontend features:**

```
/react-frontend-expert Build the notification settings page
```

**What happens:** Claude follows the component structure, TanStack Query patterns, and accessibility requirements — even if existing components don't.

```mermaid
flowchart TD
    subgraph "Pattern Adoption Over Time"
        direction LR
        T1["Month 1<br/>New code follows patterns<br/>Old code unchanged"]
        T2["Month 2<br/>Bug fixes adopt patterns<br/>in touched files"]
        T3["Month 3<br/>Refactor adjacent code<br/>during feature work"]
        T4["Month 6<br/>70%+ codebase<br/>follows patterns"]
        T1 --> T2 --> T3 --> T4
    end
```

#### The Boy Scout Rule

When you touch existing code (bug fix, feature addition), improve the file you're in:

```
/python-backend-expert Refactor the user service to use the repository pattern
while fixing the duplicate email bug
```

This spreads patterns gradually without dedicated refactoring sprints.

---

### Step 5: Adopt TDD for new work

Once the team is comfortable with the testing skills, adopt TDD for new features:

```
/tdd-workflow Implement the notification delivery system using TDD
```

**What happens:** Claude writes a failing test first, implements the minimum to pass, then refactors. This ensures new features have test coverage from the start.

**Don't force TDD on bug fixes in untested code.** Instead:

```mermaid
flowchart TD
    Bug["Bug Report"] --> HasTests{"Module has<br/>tests?"}
    HasTests -->|Yes| TDD["/tdd-workflow<br/>Write failing test<br/>that reproduces bug"]
    HasTests -->|No| AddTests["/pytest-patterns<br/>Add baseline tests<br/>for the module first"]
    AddTests --> TDD
    TDD --> Fix["Fix the bug<br/>test turns green"]
```

---

### Step 6: Improve infrastructure gradually

These skills apply when you're ready to improve the deployment and containerization setup:

**If Dockerfiles exist but are suboptimal:**

```
/docker-best-practices Review and optimize the existing Dockerfiles
```

**What happens:** Claude analyzes your Dockerfiles for common issues — missing multi-stage builds, root user, bloated images, poor layer caching — and suggests improvements.

**If CI/CD exists but is incomplete:**

```
/deployment-pipeline Review the CI/CD pipeline and add missing stages
```

**What happens:** Claude identifies gaps (missing security scanning, no staging environment, no canary rollout, no rollback procedure) and adds the missing stages.

```mermaid
flowchart TD
    subgraph "Infrastructure Improvement Path"
        D1["Current State<br/>Basic Dockerfile<br/>Minimal CI"] --> D2["Add multi-stage build<br/>Add .dockerignore<br/>/docker-best-practices"]
        D2 --> D3["Add lint + type check<br/>to CI pipeline<br/>/deployment-pipeline"]
        D3 --> D4["Add staging deploy<br/>+ smoke tests<br/>/deployment-pipeline"]
        D4 --> D5["Add canary rollout<br/>+ rollback procedure<br/>/deployment-pipeline"]
    end
```

---

### Step 7: Use planning for new features

Once the codebase is stabilized with tests, quality gates, and monitoring, use planning skills for new feature development:

```
/project-planner Add a real-time collaboration feature to the task board
```

```
/task-decomposition Break down the collaboration feature into tasks
```

**This is the same as greenfield** from this point on — plan, design, implement (with TDD), review, deploy. The difference is that you now have an existing codebase with patterns and tests to guide new work.

---

## Brownfield adoption timeline

```mermaid
gantt
    title Skill Adoption Timeline
    dateFormat YYYY-MM-DD
    axisFormat %b %d

    section Week 1 — Quick Wins
    Install skills                          :a1, 2026-01-01, 1d
    Security audit (code-review-security)   :a2, after a1, 2d
    Fix critical findings                   :a3, after a2, 2d
    Add monitoring (monitoring-setup)       :a4, after a1, 3d
    Create runbooks (incident-response)     :a5, after a4, 2d

    section Week 2 — Quality Gates
    Set up pre-merge checks                 :b1, after a3, 1d
    Add backend tests (pytest-patterns)     :b2, after b1, 5d
    Add frontend tests (react-testing)      :b3, after b1, 5d

    section Week 3 — E2E & Patterns
    Add E2E tests (e2e-testing)             :c1, after b2, 3d
    Adopt patterns for new code             :c2, after b2, 5d
    Improve Docker setup                    :c3, after c1, 2d

    section Ongoing
    TDD for new features                    :d1, after c2, 14d
    CI/CD improvements                      :d2, after c3, 7d
    Planning for new features               :d3, after d1, 14d
```

---

## Brownfield checklist

Track your adoption progress:

```
## Phase 0: Assessment
- [ ] Codebase structure understood
- [ ] Existing patterns documented
- [ ] Testing gaps identified
- [ ] Security risks cataloged
- [ ] Monitoring gaps identified

## Phase 1: Quick Wins (no code changes to existing patterns)
- [ ] Security audit completed with /code-review-security
- [ ] Critical and High findings fixed
- [ ] Structured logging added with /monitoring-setup
- [ ] Health check endpoints added
- [ ] Runbooks created with /incident-response

## Phase 2: Quality Gates
- [ ] Pre-merge checks configured with /pre-merge-checklist
- [ ] CI pipeline runs linting + type checks
- [ ] Coverage thresholds set (start low, increase over time)

## Phase 3: Testing Gaps
- [ ] Critical backend paths tested with /pytest-patterns
- [ ] Key frontend components tested with /react-testing-patterns
- [ ] Critical user journeys covered with /e2e-testing
- [ ] Coverage above 60% on critical modules

## Phase 4: Pattern Adoption
- [ ] New backend code follows /python-backend-expert patterns
- [ ] New frontend code follows /react-frontend-expert patterns
- [ ] Existing code improved via Boy Scout Rule (when touched)

## Phase 5: Full SDLC (new features)
- [ ] TDD adopted for new features with /tdd-workflow
- [ ] Planning skills used for feature work
- [ ] Docker optimized with /docker-best-practices
- [ ] CI/CD improved with /deployment-pipeline
```

---

## Common mistakes in brownfield adoption

### Mistake 1: Rewriting everything at once

**Wrong:** "Refactor the entire backend to use the repository pattern"

**Right:** "Use the repository pattern for the new notifications module. Migrate the user module when we fix the duplicate email bug."

```mermaid
flowchart LR
    subgraph "Wrong"
        Big["Big Bang Rewrite<br/>1000+ files changed<br/>Months of work<br/>High risk"]
    end
    subgraph "Right"
        Inc1["New code<br/>follows pattern"] --> Inc2["Bug fixes<br/>adopt pattern"]
        Inc2 --> Inc3["Adjacent code<br/>refactored"]
        Inc3 --> Inc4["Dedicated<br/>small refactors"]
    end
    style Big fill:#ef4444,color:#fff
    style Inc4 fill:#22c55e,color:#fff
```

### Mistake 2: Adding tests without understanding existing behavior

**Wrong:** Writing tests based on what you think the code should do.

**Right:** Read the code first, write tests that verify what it actually does, then fix discrepancies.

```
# Right approach
/pytest-patterns Write characterization tests for the payment service
— test what it currently does, document any surprising behavior
```

### Mistake 3: Skipping the security audit

**Wrong:** "We'll do security review later, let's focus on features."

**Right:** Security audit is the first thing you do. It's read-only, low-effort, and may reveal issues that need immediate attention.

### Mistake 4: Applying all quality gates retroactively

**Wrong:** Running `mypy --strict` on a codebase with zero type annotations and trying to fix 2,000 errors.

**Right:** Enable strict checking for new files only. Use a `mypy.ini` that excludes legacy modules:

```ini
[mypy]
strict = true

[mypy-legacy_module.*]
ignore_errors = true
```

Gradually remove exclusions as you add type annotations during regular work.
