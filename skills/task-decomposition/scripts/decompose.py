#!/usr/bin/env python3
"""Generate a structured task plan from a high-level objective.

Reads an objective (from --objective or --input file) and produces a task_plan.md
with decomposed tasks following the task-decomposition skill conventions.

Outputs:
  - task_plan.md: The complete task plan
  - progress.md: Initial progress tracker
  - manifest.json: List of all output files
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_OUTPUT_DIR = "/tmp/task-decomposition-output/"

TASK_PLAN_TEMPLATE = """# Task Plan: {feature_name}

Generated: {date}
Strategy: {strategy}
Status: IN_PROGRESS
Total tasks: {total_tasks}
Completed: 0

---

{tasks}
"""

PROGRESS_TEMPLATE = """# Progress

Generated: {date}

## Current Task
Task 1: {first_task_title}
Status: not started

## Completed
(none)

## Next Up
{next_up}

## Blockers
(none)
"""

TASK_TEMPLATE = """### Task {num}: {title}
- **Files:** {files}
- **Preconditions:** {preconditions}
- **Steps:**
{steps}
- **Done when:** {done_when}
- **Complexity:** {complexity}
- **Parallel:** {parallel}
"""


def parse_objective_file(filepath: str) -> dict:
    """Parse an objective input file (JSON format).

    Expected format:
    {
        "feature_name": "Add User Search",
        "objective": "Add server-side search to users list",
        "strategy": "layer-based",
        "layers": ["repository", "schema", "service", "router", "hook", "component"],
        "constraints": ["Must use existing User model", "Debounce 300ms"]
    }
    """
    with open(filepath, "r") as f:
        return json.load(f)


def generate_task_plan(objective_data: dict) -> str:
    """Generate a task plan from structured objective data."""
    feature_name = objective_data.get("feature_name", "Unnamed Feature")
    strategy = objective_data.get("strategy", "layer-based")
    layers = objective_data.get("layers", [])
    objective = objective_data.get("objective", "")
    constraints = objective_data.get("constraints", [])

    tasks = []
    task_num = 0

    if strategy == "layer-based":
        layer_order = [
            "infrastructure", "model", "migration", "schema", "repository",
            "service", "router", "types", "api-service", "hook",
            "component", "page", "unit-test", "integration-test", "e2e-test"
        ]
        ordered_layers = sorted(
            layers,
            key=lambda x: layer_order.index(x) if x in layer_order else 99
        )
        for layer in ordered_layers:
            task_num += 1
            tasks.append(TASK_TEMPLATE.format(
                num=task_num,
                title=f"Implement {layer} layer",
                files=f"`app/{layer}s/` or `src/{layer}s/`",
                preconditions="Task " + str(task_num - 1) if task_num > 1 else "none",
                steps=f"  1. Create/update {layer} implementation\n  2. Follow project conventions",
                done_when=f"Tests for {layer} pass",
                complexity="small",
                parallel="must be sequential"
            ))
    elif strategy == "feature-first":
        task_num += 1
        tasks.append(TASK_TEMPLATE.format(
            num=task_num,
            title=f"Implement {feature_name} - backend slice",
            files="Backend files for feature",
            preconditions="none",
            steps="  1. Implement backend feature slice\n  2. Add unit tests",
            done_when="Backend tests pass",
            complexity="medium",
            parallel="Can run alongside frontend design"
        ))
        task_num += 1
        tasks.append(TASK_TEMPLATE.format(
            num=task_num,
            title=f"Implement {feature_name} - frontend slice",
            files="Frontend files for feature",
            preconditions=f"Task {task_num - 1}",
            steps="  1. Implement frontend feature slice\n  2. Add component tests",
            done_when="Frontend tests pass",
            complexity="medium",
            parallel="must be sequential"
        ))
    elif strategy == "migration":
        task_num += 1
        tasks.append(TASK_TEMPLATE.format(
            num=task_num,
            title="Implement new path alongside old path",
            files="New implementation files",
            preconditions="none",
            steps="  1. Create new implementation\n  2. Keep old path untouched",
            done_when="New path tests pass AND old path still works",
            complexity="medium",
            parallel="must be sequential"
        ))
        task_num += 1
        tasks.append(TASK_TEMPLATE.format(
            num=task_num,
            title="Dual-write to both old and new paths",
            files="Integration points",
            preconditions=f"Task {task_num - 1}",
            steps="  1. Add dual-write logic\n  2. Verify both paths produce identical results",
            done_when="Integration tests confirm both paths match",
            complexity="medium",
            parallel="must be sequential"
        ))
        task_num += 1
        tasks.append(TASK_TEMPLATE.format(
            num=task_num,
            title="Switch to new path and remove old path",
            files="Old implementation files, integration points",
            preconditions=f"Task {task_num - 1}",
            steps="  1. Remove old path references\n  2. Clean up dual-write code",
            done_when="All tests pass with only new path",
            complexity="medium",
            parallel="must be sequential"
        ))

    if not tasks:
        task_num += 1
        tasks.append(TASK_TEMPLATE.format(
            num=task_num,
            title=f"Implement {feature_name}",
            files="TBD",
            preconditions="none",
            steps=f"  1. {objective}",
            done_when="TBD",
            complexity="medium",
            parallel="must be sequential"
        ))

    constraints_section = ""
    if constraints:
        constraints_section = "\n## Constraints\n" + "\n".join(
            f"- {c}" for c in constraints
        ) + "\n"

    plan = TASK_PLAN_TEMPLATE.format(
        feature_name=feature_name,
        date=datetime.now().strftime("%Y-%m-%d"),
        strategy=strategy,
        total_tasks=task_num,
        tasks="\n".join(tasks)
    )

    if constraints_section:
        plan += constraints_section

    return plan


def generate_progress(tasks_text: str, first_title: str, total: int) -> str:
    """Generate initial progress.md content."""
    next_up = ""
    for i in range(2, min(total + 1, 6)):
        next_up += f"- [ ] Task {i}\n"

    return PROGRESS_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d"),
        first_task_title=first_title,
        next_up=next_up if next_up else "(none)"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured task plan from a high-level objective."
    )
    parser.add_argument(
        "--input", "-i",
        help="Path to JSON file with objective data"
    )
    parser.add_argument(
        "--objective", "-o",
        help="Brief objective description (alternative to --input)"
    )
    parser.add_argument(
        "--feature-name", "-n",
        default="Unnamed Feature",
        help="Name of the feature being decomposed"
    )
    parser.add_argument(
        "--strategy", "-s",
        choices=["layer-based", "feature-first", "migration"],
        default="layer-based",
        help="Decomposition strategy to use"
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for generated files (default: {DEFAULT_OUTPUT_DIR})"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        if args.input:
            objective_data = parse_objective_file(args.input)
        elif args.objective:
            objective_data = {
                "feature_name": args.feature_name,
                "objective": args.objective,
                "strategy": args.strategy,
                "layers": [],
                "constraints": []
            }
        else:
            parser.error("Either --input or --objective is required")
            return

        plan = generate_task_plan(objective_data)
        plan_path = output_dir / "task_plan.md"
        plan_path.write_text(plan)

        first_title = objective_data.get("feature_name", "Task 1")
        total = plan.count("### Task ")
        progress = generate_progress(plan, first_title, total)
        progress_path = output_dir / "progress.md"
        progress_path.write_text(progress)

        manifest = {
            "generated_at": datetime.now().isoformat(),
            "skill": "task-decomposition",
            "strategy": objective_data.get("strategy", "layer-based"),
            "files": [
                {"path": str(plan_path), "type": "task_plan", "format": "markdown"},
                {"path": str(progress_path), "type": "progress", "format": "markdown"}
            ],
            "total_tasks": total
        }
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        print(f"Task plan generated successfully in {output_dir}")
        print(f"  - {plan_path}")
        print(f"  - {progress_path}")
        print(f"  - {manifest_path}")
        print(f"  Total tasks: {total}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        pass


if __name__ == "__main__":
    main()
