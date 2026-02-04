# Skill Composition Guide

> **[README](../README.md)** | [Greenfield Guide](greenfield.md) | [Brownfield Guide](brownfield.md)

How the 17 AI1 Skills relate to each other — activation rules, artifact flow between skills, same-phase pairings, and when *not* to use a skill.

## How Skills Activate

Skills activate based on keywords in your prompt. Each skill's `description` field contains phase-specific keywords and negative keywords ("Does NOT cover...") that help Claude pick the right one.

### Activation Examples

| Prompt Pattern | Activates | Does NOT Activate |
|---------------|-----------|-------------------|
| "plan the user auth feature" | `project-planner` | task-decomposition, system-architecture |
| "break this down into tasks" | `task-decomposition` | project-planner |
| "design the database schema" | `system-architecture` | python-backend-expert, api-design-patterns |
| "design the API contract for users" | `api-design-patterns` | system-architecture, python-backend-expert |
| "create a FastAPI endpoint for users" | `python-backend-expert` | fastapi-patterns, api-design-patterns |
| "configure CORS middleware" | `fastapi-patterns` | python-backend-expert |
| "set up JWT authentication dependency" | `fastapi-patterns` | python-backend-expert, code-review-security |
| "build a React user profile component" | `react-frontend-expert` | react-testing-patterns |
| "write tests for UserProfile component" | `react-testing-patterns` | react-frontend-expert, e2e-testing |
| "use TDD to build the payment service" | `tdd-workflow` | pytest-patterns, python-backend-expert |
| "write pytest tests for UserService" | `pytest-patterns` | react-testing-patterns, tdd-workflow |
| "write E2E test for login flow" | `e2e-testing` | pytest-patterns, react-testing-patterns |
| "review this PR for security" | `code-review-security` | pre-merge-checklist |
| "check if this PR is ready to merge" | `pre-merge-checklist` | code-review-security |
| "deploy to production" | `deployment-pipeline` | docker-best-practices |
| "optimize the Dockerfile" | `docker-best-practices` | deployment-pipeline |
| "we have a production outage" | `incident-response` | monitoring-setup |
| "set up Prometheus metrics" | `monitoring-setup` | incident-response |
| "add a WebSocket endpoint" | `fastapi-patterns` | python-backend-expert |
| "add structured logging" | `monitoring-setup` | python-backend-expert |
| "create GitHub Actions workflow" | `deployment-pipeline` | docker-best-practices |

**Tip:** If Claude activates the wrong skill, add clarifying keywords. For example, "create a FastAPI endpoint" activates `python-backend-expert`, while "configure FastAPI middleware" activates `fastapi-patterns`.

---

## Skill Relationships

### Vertical Composition (Producer → Consumer)

Skills pass artifacts down the SDLC. A producer skill's output becomes the input for a consumer skill.

```mermaid
flowchart TD
    PP["project-planner<br/>Implementation plan"] --> TD["task-decomposition<br/>Atomic tasks"]
    SA["system-architecture<br/>ADRs, layer decisions"] --> BE["python-backend-expert"]
    SA --> FE["react-frontend-expert"]
    AD["api-design-patterns<br/>API contracts"] --> BE
    AD --> FE
    BE -- "Backend code" --> PT["pytest-patterns"]
    FE -- "Components/hooks" --> RT["react-testing-patterns"]
    DOC["docker-best-practices<br/>Container images"] --> DEP["deployment-pipeline"]
    MON["monitoring-setup<br/>Observability infra"] --> IR["incident-response"]
```

| Producer | Artifact | Consumer |
|----------|----------|----------|
| `project-planner` | Implementation plan | `task-decomposition` |
| `system-architecture` | Architecture decisions, ADRs | `python-backend-expert`, `react-frontend-expert` |
| `api-design-patterns` | API contracts, schema conventions | `python-backend-expert`, `react-frontend-expert` |
| `python-backend-expert` | Backend code | `pytest-patterns` |
| `react-frontend-expert` | React components/hooks | `react-testing-patterns` |
| `docker-best-practices` | Container images | `deployment-pipeline` |
| `monitoring-setup` | Observability infrastructure | `incident-response` |

### Horizontal Composition (Same-Phase Pairing)

Some skills operate in parallel within the same phase. They have non-overlapping scopes and complement each other.

| Phase | Skill A | Skill B | How They Pair |
|-------|---------|---------|---------------|
| Architecture | `system-architecture` (system-level) | `api-design-patterns` (API contracts) | Architecture decisions inform API design |
| Backend Implementation | `python-backend-expert` (app patterns) | `fastapi-patterns` (framework mechanics) | CRUD vs middleware/auth/WebSocket |
| Testing | `pytest-patterns` (backend) | `react-testing-patterns` (frontend) | Same phase, different stacks |
| Testing | `pytest-patterns` (unit/integration) | `e2e-testing` (browser E2E) | Different test levels |
| Testing | `tdd-workflow` (methodology) | any testing skill (patterns) | TDD drives; testing skill provides patterns |
| Code Review | `code-review-security` (security) | `pre-merge-checklist` (quality) | Security + quality gates together |
| Deployment | `deployment-pipeline` (CI/CD) | `docker-best-practices` (containers) | Containers feed into pipelines |
| Operations | `incident-response` (incidents) | `monitoring-setup` (observability) | Monitoring enables incident diagnosis |

---

## When NOT to Use a Skill

Each skill has explicit negative keywords — things it does *not* handle. If your request falls outside a skill's scope, use the alternative listed below.

| Skill | Does NOT Handle | Use Instead |
|-------|----------------|-------------|
| `project-planner` | Architecture decisions, code implementation | `system-architecture`, `python-backend-expert` |
| `task-decomposition` | High-level planning, architecture | `project-planner`, `system-architecture` |
| `system-architecture` | Implementation code, API contracts | `python-backend-expert`, `api-design-patterns` |
| `api-design-patterns` | Implementation code, system architecture | `python-backend-expert`, `system-architecture` |
| `python-backend-expert` | Testing, middleware/WebSockets | `pytest-patterns`, `fastapi-patterns` |
| `fastapi-patterns` | Basic CRUD, repository/service patterns | `python-backend-expert` |
| `react-frontend-expert` | Testing, E2E, backend | `react-testing-patterns`, `e2e-testing` |
| `react-testing-patterns` | E2E browser tests, backend tests | `e2e-testing`, `pytest-patterns` |
| `tdd-workflow` | Testing patterns (how to write tests) | `pytest-patterns`, `react-testing-patterns` |
| `pytest-patterns` | Frontend tests, E2E tests | `react-testing-patterns`, `e2e-testing` |
| `e2e-testing` | Unit tests, component tests | `pytest-patterns`, `react-testing-patterns` |
| `code-review-security` | Deployment security, quality metrics | `docker-best-practices`, `pre-merge-checklist` |
| `pre-merge-checklist` | Security-specific review (OWASP depth) | `code-review-security` |
| `deployment-pipeline` | Docker image building, incident response | `docker-best-practices`, `incident-response` |
| `docker-best-practices` | Deployment orchestration, CI/CD | `deployment-pipeline` |
| `incident-response` | Monitoring setup, deployment | `monitoring-setup`, `deployment-pipeline` |
| `monitoring-setup` | Incident response, deployment | `incident-response`, `deployment-pipeline` |

---

## Common Multi-Skill Workflows

### Backend TDD Workflow

Three skills collaborate on each unit of backend work:

```mermaid
sequenceDiagram
    participant TDD as /tdd-workflow
    participant PT as /pytest-patterns
    participant BE as /python-backend-expert

    Note over TDD: RED
    TDD->>PT: Write failing test
    PT-->>TDD: test_create_user() FAILS

    Note over TDD: GREEN
    TDD->>BE: Implement minimum code
    BE-->>TDD: UserRepository.create() PASSES

    Note over TDD: REFACTOR
    TDD->>BE: Clean up, extract patterns
    TDD->>PT: Run all tests — still green

    Note over TDD: Next RED
    TDD->>PT: Write next failing test
```

### Security Review Before Merge

Two code review skills run in sequence:

```mermaid
flowchart LR
    PR["Pull Request"] --> SEC["/code-review-security<br/>OWASP Top 10 scan"]
    SEC -->|Findings fixed| PMC["/pre-merge-checklist<br/>Quality gates"]
    PMC -->|All checks pass| Merge["Merge"]
```

### Full Deployment Sequence

```mermaid
flowchart LR
    Code["Reviewed Code"] --> DOC["/docker-best-practices<br/>Build images"]
    DOC --> DEP["/deployment-pipeline<br/>CI/CD + canary rollout"]
    DEP --> MON["/monitoring-setup<br/>Verify observability"]
    MON --> IR["/incident-response<br/>Runbooks ready"]
```

### Frontend TDD Workflow

```mermaid
sequenceDiagram
    participant TDD as /tdd-workflow
    participant RT as /react-testing-patterns
    participant FE as /react-frontend-expert

    Note over TDD: RED
    TDD->>RT: Write failing component test
    RT-->>TDD: screen.getByText("Loading") FAILS

    Note over TDD: GREEN
    TDD->>FE: Implement minimum JSX
    FE-->>TDD: Loading spinner PASSES

    Note over TDD: Next RED
    TDD->>RT: Write test for data rendering
    Note over RT: MSW handler for /api/projects
    RT-->>TDD: findByText("My Project") FAILS

    TDD->>FE: Implement TanStack Query + list
    FE-->>TDD: PASSES
```

---

## MCP Server Integration

Skills become more powerful when paired with MCP servers that provide live data access:

| Skill | MCP Server | What It Enables |
|-------|------------|-----------------|
| `project-planner` | Jira MCP | Create issues, query backlog, link tasks to plan |
| `task-decomposition` | Jira MCP | Create subtasks, track decomposed items |
| `python-backend-expert` | PostgreSQL MCP | Query database for schema inspection during implementation |
| `pytest-patterns` | CI Server MCP | Trigger test runs, fetch coverage reports |
| `code-review-security` | GitHub MCP | Fetch PR diffs, post review comments, check CI status |
| `pre-merge-checklist` | GitHub MCP | Verify CI checks, fetch PR metadata |
| `deployment-pipeline` | GitHub MCP, Kubernetes MCP | Trigger deploys, check pod status, manage rollbacks |
| `incident-response` | Datadog/PagerDuty MCP | Query metrics, check alerts, manage incidents |
| `monitoring-setup` | Datadog MCP | Configure dashboards, verify alert rules |
