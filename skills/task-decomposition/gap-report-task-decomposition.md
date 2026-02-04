---
skill_name: 'task-decomposition'
skill_version: '1.0.0'
analysis_date: '2026-02-04'
status: 'IN_PROGRESS'
---

# Gap Report: task-decomposition

## Audit Baseline

### Skill Inventory
- SKILL.md: 223 lines
- Scripts: 0 (no scripts/ directory)
- References: 1 (decomposition-examples.md)
- Assets: 0 (no assets/ directory)

### Current Coverage
- Topics addressed: decomposition rules, task template format, decomposition process (6-step), persistent task files (task_plan.md, progress.md, findings.md), prioritization rules, scope change handling, anti-patterns
- Use cases covered: large features (4+ steps), multi-file changes, cross-context tracking, explicit decompose/subtask requests
- Patterns documented: layer-based ordering (model → schema → repo → service → router → type → hook → component → page → tests), complexity sizing (trivial/small/medium/large), dependency mapping, parallel task identification

---

## Research Findings

### Topic 1: AI Coding Agent Task Decomposition (2025-2026)
**Current State:** Planning-centric agents now use two-phase approaches: structured task decomposition followed by execution monitoring with adaptive replanning. Frameworks like TDAG (Dynamic Task Decomposition and Agent Generation) and ADaPT (As-Needed Decomposition) represent the cutting edge.
**Key Changes:** AI agents now iterate in small loops, use structured multi-step reasoning, generate prompt plans for sequential execution, and integrate testing as a safety net within the decomposition itself. Context provision is critical — agents perform best with relevant code, docs, and constraints.
**Best Practices:** Break work into small testable increments; use hierarchical or demand-driven decomposition; maintain strong testing and quality gates; provide rich context; keep humans in the loop for oversight.
**Deprecations:** Monolithic task descriptions without verification steps are discouraged. Large single-prompt approaches replaced by chunked workflows.
**Sources:** mgx.dev, addyosmani.com, dev.to, uipath.com

### Topic 2: Work Breakdown Structure (WBS) Best Practices
**Current State:** WBS remains foundational for project planning. The 8/80 rule (each work package 8-80 hours) and 100% rule (all project work captured) are standard. Deliverable-oriented WBS preferred over phase-based for shorter projects.
**Key Changes:** Modern tools (Jira, Miro, GanttPRO) now support automated WBS generation. Focus on nouns (deliverables) not verbs (activities). Limit to 3-5 levels of hierarchy.
**Best Practices:** 100% rule ensures nothing missed; involve the team in WBS creation; create a WBS dictionary for clarity; use deliverable-based decomposition for clear outcomes.
**Deprecations:** Using lifecycle phases as major WBS deliverables is discouraged.
**Sources:** atlassian.com, projectmanager.com, miro.com, asana.com

### Topic 3: Monorepo Task Decomposition Strategies
**Current State:** Nx and Turborepo are the leading monorepo tools. Turborepo focuses on execution speed with task graph configuration in turbo.json. Nx provides comprehensive ecosystem with dependency visualization and distributed task execution across machines.
**Key Changes:** Task graph-based execution is standard. Turborepo enables incremental migration (one task or one package at a time). Nx supports distributed task execution across 50+ machines.
**Best Practices:** Define task dependencies explicitly in pipeline config; combine with code ownership enforcement and selective test runners; choose Turborepo for speed-focused needs, Nx for architectural guardrails.
**Deprecations:** None major — both tools evolving actively.
**Sources:** wisp.blog, dev.to, aviator.co

### Topic 4: Task Complexity Estimation (Agile 2025-2026)
**Current State:** Story points using Fibonacci sequence remain standard but face growing alternatives. AI-powered estimation is emerging — 84% of organizations integrated AI into pipelines per Digital.ai's 2025 report.
**Key Changes:** T-shirt sizing (XS/S/M/L/XL) gaining traction for early estimation. #NoEstimates movement growing for experienced teams. Throughput-based estimation (items per time period) replacing upfront estimation for some teams. AI tools auto-suggest story points from historical data.
**Best Practices:** Combine techniques (affinity mapping + planning poker + analogy-based); use story points for sprint planning, hours for daily execution; leverage AI-assisted estimation for data-driven accuracy.
**Deprecations:** Pure story point reliance declining; manual-only estimation being supplemented by AI.
**Sources:** monday.com, ones.com, axify.io, parabol.co

### Topic 5: AI Coding Assistant Task Planning Tools
**Current State:** Three dominant tools: Cursor (flow-state editing, 4.9/5 rating), Claude Code (terminal-native agentic system, 200K token context, $1B ARR by Nov 2025), GitHub Copilot (enterprise standard, agent mode). Windsurf and OpenAI Codex emerging.
**Key Changes:** Shift from autocomplete to agentic workflows. Claude Code operates as delegation model ("refactor auth module to use JWT"). Cursor excels at inline flow editing. Many developers use multiple tools together.
**Best Practices:** Use Cursor for writing, Claude for thinking; always inspect diffs and test outcomes; use layered AI stack (copilot + agent + terminal assistant + CI AI); know when to trust vs. question the AI.
**Deprecations:** Simple autocomplete-only assistants being replaced by agent-based workflows.
**Sources:** nucamp.co, usama.codes, faros.ai, artificialanalysis.ai

### Topic 6: Dependency Graph & Task Ordering in CI/CD
**Current State:** Average application contains 1,200+ open source components (64% transitive). YAML pipelines as code are standard. Quality gates enforce standards at pipeline checkpoints.
**Key Changes:** Dependency graphs used for change impact analysis, vulnerability auditing, SBOM generation. Jobs in same stage run parallel by default — explicit dependency declarations needed. Layered testing strategy in pipelines: unit → integration → E2E.
**Best Practices:** Use lock files and version pinning; build once deploy everywhere; automated dependency scanning (Snyk, Dependabot); provide fast feedback (<5 minutes for CI); explicit task ordering via dependency declarations.
**Deprecations:** UI-configured pipelines replaced by YAML pipeline-as-code.
**Sources:** krasamo.com, wondermentapps.com, codeant.ai, puppygraph.com

### Topic 7: Microservices & Event-Driven Architecture Task Decomposition
**Current State:** Event-driven architecture (EDA) standard for microservices communication. Components: event producers, consumers, event bus, event store. Domain-Driven Design identifies bounded contexts for service boundaries.
**Key Changes:** Choreography over orchestration pattern gaining dominance. Event sourcing + CQRS most common pattern pair (57% of surveyed organizations). Saga pattern for distributed transactions. Four decomposition patterns: strangler, domain-first, customer-impact, technical-debt.
**Best Practices:** Use Event Storming sessions for domain event identification; implement event sourcing for auditability; use saga pattern for distributed transactions; phase implementation incrementally.
**Deprecations:** Direct synchronous communication between microservices being replaced by event-driven patterns.
**Sources:** akamai.com, microservices.io, ijsat.org, confluent.io

### Topic 8: FastAPI Project Structure Best Practices (2025-2026)
**Current State:** Three-layer architecture is now essential: Presentation (routes), Service (business logic), Data Access (repositories). Service layer architecture considered mandatory for production apps.
**Key Changes:** "Thin routes, fat services" is the standard pattern. DTOs for inter-layer communication. Pydantic BaseSettings for config management. Python 3.12+ with async best practices.
**Best Practices:** Separate routers/services/models/schemas/core/db directories; use FastAPI dependency injection; keep route handlers thin; centralize business logic in services; use DTOs for type safety between layers.
**Deprecations:** Putting business logic in route handlers; monolithic file structures.
**Sources:** dev.to, medium.com, fastlaunchapi.dev, zestminds.com

### Topic 9: React/TypeScript Project Decomposition (2025-2026)
**Current State:** Feature-first architecture replaces type-based organization. Component hierarchy follows React's official "Thinking in React" guidance. One-way data flow with state ownership at closest common parent.
**Key Changes:** Kebab-case naming convention standard for 2025. Deep nesting limited to 2-3 levels max. Feature-first folder structure gaining dominance. Vite recommended as default bundler (or Turbopack in Next.js).
**Best Practices:** Use feature-first architecture; limit folder nesting to 2-3 levels; configure absolute imports via tsconfig paths; use functional components + hooks; React.memo/useMemo for performance; TypeScript strict mode.
**Deprecations:** Type-based folder organization (controllers/services/utils) declining; deep folder hierarchies discouraged.
**Sources:** developerway.com, robinwieruch.de, netguru.com, patterns.dev

### Topic 10: Testing Strategy Task Breakdown (TDD/BDD/Contract Testing)
**Current State:** Testing pyramid remains foundational with 70-20-10 ratio (unit/integration/E2E). TDD adoption growing — IBM/Microsoft report up to 90% fewer pre-release defects. BDD uses Gherkin syntax for natural language tests.
**Key Changes:** AI-powered TDD emerging. Test trophy model gaining traction alongside pyramid. Cost economics: bug found in unit test costs $1 to fix vs. $1,000 in production. TDD increases initial dev time 15-35% but dramatically reduces defects.
**Best Practices:** Start with robust unit test suite via TDD; add integration tests for component interactions; minimal but critical E2E tests for key journeys; blend TDD (code validation) + BDD (behavior specs) + contract testing (service boundaries); don't test trivial code.
**Deprecations:** Testing only at E2E level; manual-only testing strategies.
**Sources:** martinfowler.com, fullscale.io, nopaccelerate.com, devzery.com

---

## Gap Analysis

### Outdated Content (Must Update)

| Item | Current State | Required Update | Priority | Target Step |
|------|--------------|-----------------|----------|-------------|
| Complexity sizing heuristics | Trivial/small/medium/large based only on file count and line count | Add T-shirt sizing alternative, throughput-based estimation reference, and context for when to use each method | Medium | step-04 |
| Layer ordering list | Lists 13 layers but doesn't mention feature-first or domain-driven alternatives | Add feature-first decomposition as alternative ordering strategy alongside layer-based | Medium | step-04 |
| Decomposition process | 6-step sequential process without AI-agent integration | Add guidance for structuring tasks for AI agent execution (context provision, small testable increments, verification commands) | High | step-04 |

### Missing Content (Must Add)

| Topic | Why Needed | What to Add | Priority | Target Step |
|-------|-----------|-------------|----------|-------------|
| AI-assisted decomposition | AI coding agents are central to modern development; tasks need to be structured for agent execution | "Decomposing for AI Agents" section: context provision, small loops, testing as safety net, prompt plan generation | High | step-04 |
| Testing strategy integration | Research shows testing integral to decomposition (70-20-10 ratio). Current skill mentions tests in ordering but lacks strategy guidance | Testing task patterns: when to create unit/integration/E2E tasks, testing pyramid alignment, TDD cycle integration | High | step-04 |
| Microservices/event-driven decomposition | Current skill only covers CRUD layer-based decomposition. No coverage of distributed systems | Event-driven decomposition patterns: event sourcing tasks, saga pattern tasks, service boundary identification | Medium | step-04 |
| Migration/refactoring decomposition | No guidance for decomposing brownfield migration tasks (strangler pattern, incremental migration) | Migration-specific decomposition: strangler fig pattern tasks, data migration tasks, backward compatibility tasks | Medium | step-04 |
| WBS methodology connection | Established WBS practices (100% rule, 8/80 rule) not referenced despite being foundational | Reference to WBS 100% rule (capture all work) and 8/80 rule as validation checks on decomposition completeness | Low | step-04 |
| Monorepo task decomposition | No guidance for decomposing tasks across monorepo packages/workspaces | Cross-package dependency handling, task graph awareness, selective execution guidance | Low | step-04 |
| CI/CD pipeline task alignment | Tasks don't reference how they map to CI/CD pipeline stages or quality gates | Guidance on aligning task verification with CI pipeline stages; quality gate checkpoints | Low | step-04 |

### Script Gaps

| Script | Issue | Required Change | Target Step |
|--------|-------|-----------------|-------------|
| decompose.py (NEW) | No scripts exist — missing automation for task plan generation | Create Python script that generates task_plan.md from structured input (objective, layers, constraints) with argparse CLI and file output | step-06 |
| validate-plan.py (NEW) | No validation script for generated task plans | Create Python script that validates task plans against decomposition rules (atomicity, verification, preconditions, complexity sizing) with file output | step-06 |

### Reference Gaps

| Reference | Issue | Required Change | Target Step |
|-----------|-------|-----------------|-------------|
| decomposition-examples.md | Only covers CRUD features (search, auth, file upload, pagination). Missing modern architecture patterns | Add examples for: event-driven feature, migration/refactoring, microservices decomposition | step-06 |
| complexity-guide.md (NEW) | No reference for complexity estimation methods | Create reference covering T-shirt sizing, Fibonacci story points, throughput-based estimation, and when to use each | step-06 |

### Asset Gaps

| Asset | Issue | Required Change | Target Step |
|-------|-------|-----------------|-------------|
| task-template.md (NEW) | Task template is embedded in SKILL.md but not available as standalone asset | Extract task template as reusable asset file that scripts and agents can reference | step-06 |
| decomposition-checklist.md (NEW) | No checklist for validating decomposition quality | Create checklist covering: 100% rule, atomicity check, verification completeness, dependency graph acyclicity, complexity sizing consistency | step-06 |

### File Output Non-Compliance

| Script | Missing | Required Change | Target Step |
|--------|---------|-----------------|-------------|
| decompose.py (NEW) | N/A — script doesn't exist yet | Must be created with --output-dir flag, JSON/MD file output, manifest.json | step-06, step-07 |
| validate-plan.py (NEW) | N/A — script doesn't exist yet | Must be created with --output-dir flag, JSON report output, manifest.json | step-06, step-07 |

---

## Priority Summary

- High priority gaps: 3 (AI-assisted decomposition, testing strategy integration, decomposition process update)
- Medium priority gaps: 5 (complexity sizing, layer ordering, microservices decomposition, migration decomposition, decomposition-examples.md update)
- Low priority gaps: 5 (WBS methodology, monorepo decomposition, CI/CD alignment, complexity-guide.md, task-template.md)
- Total gaps: 13 + 2 new scripts + 1 new reference + 2 new assets = 18 items
