# Complexity Estimation Guide

Methods for sizing tasks during decomposition. Choose based on your team's needs and planning context.

## Method 1: Trivial/Small/Medium/Large (Default)

The standard sizing used in task-decomposition skill. Best for individual developer or AI agent task sizing.

| Size | Files | Lines Changed | Tests Required | Typical Duration |
|------|-------|---------------|----------------|------------------|
| Trivial | 1 | <20 | None | Minutes |
| Small | 1-2 | <100 | Unit tests | Hours |
| Medium | 2-3 | <200 | Unit + integration | Half-day |
| Large | 3+ | 200+ | Full coverage | Full day+ |

**When to use:** Default for all task decomposition. Works well for developer estimation and AI agent task scoping.

## Method 2: T-Shirt Sizing (XS/S/M/L/XL)

Quick relative sizing for early estimation or roadmap planning.

| Size | Relative Effort | Rough Mapping |
|------|----------------|---------------|
| XS | Baseline (1x) | Trivial |
| S | 2-3x baseline | Small |
| M | 5-8x baseline | Medium |
| L | 13-20x baseline | Large |
| XL | 20x+ baseline | Should be split |

**When to use:** Roadmap discussions, backlog grooming, early-stage estimation where precision isn't needed. Good for communicating with product managers.

## Method 3: Fibonacci Story Points (1/2/3/5/8/13)

Standard agile estimation for sprint planning with velocity tracking.

| Points | Description |
|--------|-------------|
| 1 | Trivial, well-understood change |
| 2 | Small, straightforward task |
| 3 | Moderate complexity, some unknowns |
| 5 | Complex, multiple components |
| 8 | Very complex, significant unknowns |
| 13 | Should consider splitting |

**When to use:** Sprint planning with established teams tracking velocity. Requires calibration across the team. Not recommended for AI agent task sizing.

## Method 4: Throughput-Based (No Upfront Estimation)

Track items completed per time period instead of estimating individual items.

**How it works:**
1. Count tasks completed per sprint/week
2. Use historical throughput to forecast delivery
3. No individual task estimation needed

**When to use:** Experienced teams with consistent task sizing. Works well when tasks are already decomposed into similar-sized units. Reduces estimation overhead.

## Choosing a Method

| Context | Recommended Method |
|---------|-------------------|
| AI agent task execution | Trivial/S/M/L |
| Developer sprint planning | Fibonacci or T-shirt |
| Roadmap estimation | T-shirt sizing |
| Experienced team, consistent tasks | Throughput-based |
| Cross-team communication | T-shirt sizing |
| New team calibrating | Fibonacci with planning poker |

## Estimation Anti-Patterns

1. **Converting story points to hours** — They measure different things. Don't convert.
2. **Estimating in isolation** — Involve the people doing the work.
3. **Debating estimates too long** — If disagreement is more than 2 Fibonacci steps apart, discuss briefly then pick the higher value.
4. **Estimating tasks that should be split** — If estimation is hard, the task is too big. Split first, then estimate.
5. **Ignoring historical data** — Past velocity and throughput are your best predictors.
