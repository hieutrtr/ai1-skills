#!/usr/bin/env python3
"""Validate a task plan against task-decomposition skill rules.

Reads a task_plan.md file and checks each task for:
- Atomic scope (max 2-3 files)
- Verification command present
- Preconditions declared
- Complexity sizing assigned
- Dependency graph acyclicity
- 100% rule (no orphaned or missing dependencies)

Outputs:
  - validation-report.json: Structured validation results
  - validation-report.md: Human-readable report
  - manifest.json: List of all output files
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_OUTPUT_DIR = "/tmp/task-decomposition-output/"

VALID_COMPLEXITIES = {"trivial", "small", "medium", "large"}


def parse_task_plan(content: str) -> list[dict]:
    """Parse a task_plan.md file into structured task objects."""
    tasks = []
    task_pattern = re.compile(
        r"###\s+Task\s+(\d+):\s+(.+?)(?=\n###\s+Task|\n##\s+|\Z)",
        re.DOTALL
    )

    for match in task_pattern.finditer(content):
        task_num = int(match.group(1))
        task_body = match.group(0)
        title = match.group(2).strip()

        files_match = re.search(r"\*\*Files:\*\*\s*(.+)", task_body)
        preconditions_match = re.search(r"\*\*Preconditions:\*\*\s*(.+)", task_body)
        done_match = re.search(r"\*\*Done when:\*\*\s*(.+)", task_body)
        complexity_match = re.search(r"\*\*Complexity:\*\*\s*(\w+)", task_body)
        parallel_match = re.search(r"\*\*Parallel:\*\*\s*(.+)", task_body)
        steps_match = re.search(
            r"\*\*Steps:\*\*\s*\n((?:\s+\d+\..+\n?)+)", task_body
        )

        files_str = files_match.group(1).strip() if files_match else ""
        file_list = [
            f.strip().strip("`")
            for f in files_str.split(",")
        ] if files_str else []

        preconditions_str = (
            preconditions_match.group(1).strip() if preconditions_match else "none"
        )
        precondition_ids = []
        if preconditions_str.lower() != "none":
            precondition_ids = [
                int(x) for x in re.findall(r"Task\s+(\d+)", preconditions_str)
            ]

        tasks.append({
            "num": task_num,
            "title": title,
            "files": file_list,
            "file_count": len(file_list),
            "preconditions": precondition_ids,
            "done_when": done_match.group(1).strip() if done_match else "",
            "complexity": complexity_match.group(1).lower() if complexity_match else "",
            "parallel": parallel_match.group(1).strip() if parallel_match else "",
            "has_steps": bool(steps_match),
        })

    return tasks


def validate_tasks(tasks: list[dict]) -> dict:
    """Validate parsed tasks against decomposition rules."""
    issues = []
    warnings = []
    task_nums = {t["num"] for t in tasks}

    for task in tasks:
        num = task["num"]
        prefix = f"Task {num}"

        # Rule 1: Atomic scope (max 3 files)
        if task["file_count"] > 3:
            issues.append({
                "task": num,
                "rule": "atomic_scope",
                "severity": "error",
                "message": f"{prefix}: Touches {task['file_count']} files (max 3). Split this task."
            })

        # Rule 2: Independently verifiable
        if not task["done_when"]:
            issues.append({
                "task": num,
                "rule": "verifiable",
                "severity": "error",
                "message": f"{prefix}: Missing 'Done when' verification command."
            })
        elif task["done_when"].lower() in ["tbd", "todo", "n/a"]:
            warnings.append({
                "task": num,
                "rule": "verifiable",
                "severity": "warning",
                "message": f"{prefix}: 'Done when' is placeholder ({task['done_when']}). Needs a concrete command."
            })

        # Rule 3: Has steps
        if not task["has_steps"]:
            warnings.append({
                "task": num,
                "rule": "steps",
                "severity": "warning",
                "message": f"{prefix}: No steps found. Add concrete action steps."
            })

        # Rule 4: Preconditions reference valid tasks
        for dep in task["preconditions"]:
            if dep not in task_nums:
                issues.append({
                    "task": num,
                    "rule": "preconditions",
                    "severity": "error",
                    "message": f"{prefix}: References Task {dep} which does not exist."
                })

        # Rule 5: Complexity sizing
        if not task["complexity"]:
            issues.append({
                "task": num,
                "rule": "complexity",
                "severity": "error",
                "message": f"{prefix}: Missing complexity sizing."
            })
        elif task["complexity"] not in VALID_COMPLEXITIES:
            warnings.append({
                "task": num,
                "rule": "complexity",
                "severity": "warning",
                "message": f"{prefix}: Complexity '{task['complexity']}' not standard. Use: {', '.join(VALID_COMPLEXITIES)}"
            })

        # Rule 6: Files listed
        if not task["files"] or task["files"] == [""]:
            warnings.append({
                "task": num,
                "rule": "files",
                "severity": "warning",
                "message": f"{prefix}: No files listed."
            })

    # Check for circular dependencies
    cycles = detect_cycles(tasks)
    for cycle in cycles:
        issues.append({
            "task": cycle[0],
            "rule": "acyclic",
            "severity": "error",
            "message": f"Circular dependency detected: {' -> '.join(f'Task {t}' for t in cycle)}"
        })

    return {
        "total_tasks": len(tasks),
        "errors": len(issues),
        "warnings": len(warnings),
        "issues": issues,
        "warnings_list": warnings,
        "passed": len(issues) == 0
    }


def detect_cycles(tasks: list[dict]) -> list[list[int]]:
    """Detect circular dependencies using DFS."""
    graph = {t["num"]: t["preconditions"] for t in tasks}
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])

        path.pop()
        rec_stack.discard(node)

    for task_num in graph:
        if task_num not in visited:
            dfs(task_num, [])

    return cycles


def format_report_md(validation: dict, filepath: str) -> str:
    """Format validation results as markdown."""
    status = "PASS" if validation["passed"] else "FAIL"
    lines = [
        f"# Task Plan Validation Report",
        f"",
        f"**File:** {filepath}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Status:** {status}",
        f"**Tasks:** {validation['total_tasks']}",
        f"**Errors:** {validation['errors']}",
        f"**Warnings:** {validation['warnings']}",
        f"",
    ]

    if validation["issues"]:
        lines.append("## Errors")
        lines.append("")
        for issue in validation["issues"]:
            lines.append(f"- **[{issue['rule']}]** {issue['message']}")
        lines.append("")

    if validation["warnings_list"]:
        lines.append("## Warnings")
        lines.append("")
        for warning in validation["warnings_list"]:
            lines.append(f"- **[{warning['rule']}]** {warning['message']}")
        lines.append("")

    if validation["passed"] and not validation["warnings_list"]:
        lines.append("All tasks pass validation rules.")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate a task plan against decomposition rules."
    )
    parser.add_argument(
        "plan_file",
        help="Path to task_plan.md file to validate"
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for validation reports (default: {DEFAULT_OUTPUT_DIR})"
    )

    args = parser.parse_args()
    plan_path = Path(args.plan_file)
    output_dir = Path(args.output_dir)

    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        if not plan_path.exists():
            print(f"Error: File not found: {plan_path}", file=sys.stderr)
            sys.exit(1)

        content = plan_path.read_text()
        tasks = parse_task_plan(content)

        if not tasks:
            print("Error: No tasks found in the plan file.", file=sys.stderr)
            sys.exit(1)

        validation = validate_tasks(tasks)

        # Write JSON report
        json_path = output_dir / "validation-report.json"
        json_path.write_text(json.dumps(validation, indent=2))

        # Write markdown report
        md_report = format_report_md(validation, str(plan_path))
        md_path = output_dir / "validation-report.md"
        md_path.write_text(md_report)

        # Write manifest
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "skill": "task-decomposition",
            "tool": "validate-plan",
            "input": str(plan_path),
            "files": [
                {"path": str(json_path), "type": "validation_report", "format": "json"},
                {"path": str(md_path), "type": "validation_report", "format": "markdown"}
            ],
            "result": "pass" if validation["passed"] else "fail",
            "errors": validation["errors"],
            "warnings": validation["warnings"]
        }
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        print(f"Validation {'PASSED' if validation['passed'] else 'FAILED'}")
        print(f"  Tasks: {validation['total_tasks']}")
        print(f"  Errors: {validation['errors']}")
        print(f"  Warnings: {validation['warnings']}")
        print(f"  Reports: {output_dir}")

        sys.exit(0 if validation["passed"] else 1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        pass


if __name__ == "__main__":
    main()
