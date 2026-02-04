#!/usr/bin/env python3
"""Generate a structured implementation plan document from input parameters.

Produces a markdown plan file following the project-planner skill's plan template,
with sections for objective, affected modules, task list, dependency graph,
risk assessment, and acceptance criteria.

Output: Writes plan document to --output-dir (default: /tmp/project-planner-output/).
"""

import argparse
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a structured implementation plan document"
    )
    parser.add_argument(
        "feature_name",
        help="Name of the feature to plan (used as plan title)",
    )
    parser.add_argument(
        "--objective",
        required=True,
        help="One-sentence objective statement for the feature",
    )
    parser.add_argument(
        "--complexity",
        choices=["trivial", "small", "medium", "large"],
        default="medium",
        help="Overall complexity estimate (default: medium)",
    )
    parser.add_argument(
        "--author",
        default="auto-generated",
        help="Plan author name (default: auto-generated)",
    )
    parser.add_argument(
        "--backend-files",
        nargs="*",
        default=[],
        help="Backend file paths affected (e.g., app/models/user.py)",
    )
    parser.add_argument(
        "--frontend-files",
        nargs="*",
        default=[],
        help="Frontend file paths affected (e.g., src/components/User.tsx)",
    )
    parser.add_argument(
        "--tasks",
        nargs="*",
        default=[],
        help='Task descriptions (e.g., "Add user model" "Create schema")',
    )
    parser.add_argument(
        "--risks",
        nargs="*",
        default=[],
        help='Risk descriptions (e.g., "Schema migration on large table")',
    )
    parser.add_argument(
        "--has-migration",
        action="store_true",
        help="Flag if database migration is involved",
    )
    parser.add_argument(
        "--has-rsc",
        action="store_true",
        help="Flag if React Server Components are involved",
    )
    parser.add_argument(
        "--output-dir",
        default="/tmp/project-planner-output",
        help="Output directory for generated files (default: /tmp/project-planner-output)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "both"],
        default="both",
        help="Output format (default: both)",
    )
    return parser.parse_args()


def generate_plan_markdown(args):
    """Generate the plan as a markdown document."""
    date = datetime.now().strftime("%Y-%m-%d")
    slug = args.feature_name.lower().replace(" ", "-")

    lines = [
        f"# Implementation Plan: {args.feature_name}",
        "",
        "## Metadata",
        "",
        f"- **Date:** {date}",
        f"- **Author:** {args.author}",
        "- **Status:** Draft",
        f"- **Complexity:** {args.complexity.capitalize()}",
        "",
        "## Objective",
        "",
        args.objective,
        "",
        "## Affected Modules",
        "",
    ]

    if args.backend_files:
        lines.append("### Backend (Python/FastAPI)")
        lines.append("")
        lines.append("| Layer | File Path | Action | Notes |")
        lines.append("|-------|----------|--------|-------|")
        for f in args.backend_files:
            layer = _infer_layer(f)
            lines.append(f"| {layer} | `{f}` | Create/Modify | — |")
        lines.append("")

    if args.frontend_files:
        lines.append("### Frontend (React/TypeScript)")
        lines.append("")
        lines.append("| Layer | File Path | Action | Notes |")
        lines.append("|-------|----------|--------|-------|")
        for f in args.frontend_files:
            layer = _infer_frontend_layer(f)
            lines.append(f"| {layer} | `{f}` | Create/Modify | — |")
        lines.append("")

    if args.has_rsc:
        lines.extend([
            "### Server Component Decision",
            "",
            "This feature involves React Server Components. For each component:",
            "- Determine if it needs interactivity (client) or is read-only (server)",
            "- Server Components: data fetching, static content, zero client JS",
            "- Client Components: hooks, event handlers, browser APIs",
            "",
        ])

    lines.extend([
        "## Task List",
        "",
    ])

    if args.tasks:
        for i, task in enumerate(args.tasks, 1):
            precond = f"Task {i - 1}" if i > 1 else "None"
            lines.extend([
                f"### Task {i}: {task}",
                "",
                "- **Files:** [identify from affected modules]",
                f"- **Preconditions:** {precond}",
                "- **Steps:**",
                "  1. [define steps]",
                f"- **Verify:** [define verification]",
                f"- **Complexity:** {args.complexity.capitalize()}",
                "",
            ])
    else:
        lines.extend([
            "### Task 1: [Title]",
            "",
            "- **Files:** [list]",
            "- **Preconditions:** None",
            "- **Steps:**",
            "  1. [step]",
            "- **Verify:** [command] — expect [result]",
            "",
        ])

    lines.extend([
        "## Dependency Graph",
        "",
        "```",
    ])
    if args.tasks:
        for i, task in enumerate(args.tasks, 1):
            indent = "  " * (i - 1)
            connector = "└── " if i > 1 else ""
            lines.append(f"{indent}{connector}Task {i} ({task})")
    else:
        lines.append("Task 1 → Task 2 → Task 3")
    lines.extend([
        "```",
        "",
        "## Risk Assessment",
        "",
        "| Risk | Likelihood | Impact | Mitigation |",
        "|------|-----------|--------|------------|",
    ])

    if args.risks:
        for risk in args.risks:
            lines.append(f"| {risk} | Medium | Medium | [define mitigation] |")
    else:
        lines.append("| [identify risks] | Low/Med/High | Low/Med/High | [action] |")

    if args.has_migration:
        lines.append("| Database migration on production | Medium | High | Test on staging, write downgrade(), backup before run |")

    lines.extend([
        "",
        "See `references/risk-assessment-checklist.md` for full risk category checklist.",
        "",
        "## Acceptance Criteria",
        "",
        "- [ ] All tasks completed and verified",
        "- [ ] All new code has unit tests with >80% coverage",
        "- [ ] Integration tests pass",
        "- [ ] No security vulnerabilities introduced",
        "- [ ] Pre-merge checklist passes",
        "",
    ])

    if args.has_migration:
        lines.append("- [ ] Database migration tested on staging with production-like data")
        lines.append("- [ ] Rollback migration tested")
        lines.append("")

    if args.has_rsc:
        lines.append("- [ ] Server Components render correctly on server")
        lines.append("- [ ] Client Components hydrate without errors")
        lines.append("- [ ] No unnecessary client JS shipped for server-only components")
        lines.append("")

    lines.extend([
        "## Notes",
        "",
        f"Generated by project-planner/scripts/plan-generator.py on {date}.",
        f"Review and refine before implementation.",
        "",
    ])

    return "\n".join(lines)


def generate_plan_json(args):
    """Generate the plan as structured JSON."""
    return {
        "feature_name": args.feature_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "author": args.author,
        "status": "Draft",
        "complexity": args.complexity,
        "objective": args.objective,
        "backend_files": args.backend_files,
        "frontend_files": args.frontend_files,
        "tasks": [
            {"id": i, "title": task, "preconditions": [i - 1] if i > 1 else []}
            for i, task in enumerate(args.tasks, 1)
        ],
        "risks": args.risks,
        "has_migration": args.has_migration,
        "has_rsc": args.has_rsc,
    }


def _infer_layer(filepath):
    """Infer the backend layer from a file path."""
    mapping = {
        "models": "Model",
        "schemas": "Schema",
        "repositories": "Repository",
        "services": "Service",
        "routers": "Router",
        "dependencies": "Dependency",
        "config": "Config",
        "alembic": "Migration",
    }
    for key, layer in mapping.items():
        if key in filepath:
            return layer
    return "Other"


def _infer_frontend_layer(filepath):
    """Infer the frontend layer from a file path."""
    mapping = {
        "pages": "Page",
        "components": "Component",
        "hooks": "Hook",
        "services": "Service",
        "types": "Type",
    }
    for key, layer in mapping.items():
        if key in filepath:
            return layer
    return "Other"


def main():
    args = parse_args()
    output_dir = args.output_dir
    slug = args.feature_name.lower().replace(" ", "-")

    try:
        os.makedirs(output_dir, exist_ok=True)

        outputs = []

        if args.format in ("markdown", "both"):
            md_content = generate_plan_markdown(args)
            md_path = os.path.join(output_dir, f"plan-{slug}.md")
            with open(md_path, "w") as f:
                f.write(md_content)
            outputs.append(md_path)
            print(f"Markdown plan written to: {md_path}")

        if args.format in ("json", "both"):
            json_data = generate_plan_json(args)
            json_path = os.path.join(output_dir, f"plan-{slug}.json")
            with open(json_path, "w") as f:
                json.dump(json_data, f, indent=2)
            outputs.append(json_path)
            print(f"JSON plan written to: {json_path}")

        # Write manifest
        manifest = {
            "generator": "project-planner/scripts/plan-generator.py",
            "timestamp": datetime.now().isoformat(),
            "feature": args.feature_name,
            "outputs": outputs,
        }
        manifest_path = os.path.join(output_dir, "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"Manifest written to: {manifest_path}")

    except Exception:
        raise
    finally:
        # Cleanup: nothing to clean up for file generation
        pass


if __name__ == "__main__":
    main()
