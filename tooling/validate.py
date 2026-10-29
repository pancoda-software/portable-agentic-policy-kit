#!/usr/bin/env python3
"""Validate canonical policy, skill registry, and optionally rendered entrypoints."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from common import GENERATED, ROOT, PolicyError, project_config, read_json_yaml, render_contents

EXPECTED_DECISIONS = {
    "D-01": "B", "D-02": "B", "D-03": "B", "D-04": "A",
    "D-04a": "Multi-Provider", "D-05": "B", "D-06": "B", "D-07": "B",
    "D-08": "B", "D-09": "B", "D-10": "B", "D-11": "B",
}
EXPECTED_SKILLS = {
    "grill-me", "grilling", "graft", "ponytail", "caveman", "refactor",
    "frontend-design", "baseline-ui", "improve-ui", "fixing-motion-performance",
}


def validate_sources(config: Path) -> list[str]:
    errors = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append("VERSION must be semver x.y.z")
    decisions = read_json_yaml(ROOT / "policy/decisions.yaml")
    if decisions.get("version") != version or decisions.get("schema") != 1:
        errors.append("Decision version/schema mismatch")
    actual_decisions = decisions.get("decisions", {})
    if not isinstance(actual_decisions, dict) or set(actual_decisions) != set(EXPECTED_DECISIONS):
        errors.append("Decision IDs do not match D-01 through D-11 plus D-04a")
    else:
        for key, value in EXPECTED_DECISIONS.items():
            item = actual_decisions[key]
            if not isinstance(item, dict) or item.get("option") != value or not item.get("name"):
                errors.append(f"Decision {key} incorrect or empty")
    defaults = decisions.get("defaults", {})
    required = {
        "local_retries_per_cause": 2,
        "escalated_retries_per_cause": 1,
        "total_corrections_per_task": 6,
        "max_parallel_writers": 2,
        "automatic_push": False,
        "automatic_paid_provider_switch": False,
        "dependency_install_requires_approval": True,
    }
    for name, expected in required.items():
        if type(defaults.get(name)) is not type(expected) or defaults.get(name) != expected:
            errors.append(f"Unsafe or inconsistent default: {name}")

    registry = read_json_yaml(ROOT / "policy/skill-registry.yaml")
    skills = registry.get("skills")
    if not isinstance(skills, list):
        errors.append("skills must be an array")
        skills = []
    ids = [x.get("id") for x in skills if isinstance(x, dict)]
    if set(ids) != EXPECTED_SKILLS or len(ids) != len(set(ids)):
        errors.append("Skill IDs missing or duplicated")
    for entry in skills:
        if not isinstance(entry, dict):
            errors.append("Invalid skill record")
            continue
        if entry.get("tier") not in ("REQUIRED", "PREFERRED", "OPTIONAL"):
            errors.append(f"Unknown tier for {entry.get('id')}")
        if not isinstance(entry.get("source"), str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", entry.get("source", "")):
            errors.append(f"Invalid source for {entry.get('id')}")
        if not isinstance(entry.get("depends_on"), list) or not set(entry["depends_on"]).issubset(ids):
            errors.append(f"Unresolved dependencies for {entry.get('id')}")
    core = (ROOT / "policy/core.md").read_text(encoding="utf-8")
    for needle in ("D-01", "D-02", "D-03", "D-04", "D-05", "D-06", "D-07", "D-08", "D-09", "D-10", "D-11", "2 local correction attempts", "1 escalated correction attempt", "6 total correction attempts", "Push", "DENY by default", "UNAVAILABLE"):
        if needle.casefold() not in core.casefold():
            errors.append(f"Core policy missing important invariant: {needle}")
    project_config(config)
    render_contents(config)
    return errors


def validate_generated(config: Path, generated: Path) -> list[str]:
    expected = render_contents(config)
    errors = []
    for name in GENERATED:
        path = generated / name
        if path.is_symlink() or not path.is_file():
            errors.append(f"Missing/unsafe generated file: {name}")
        elif path.read_text(encoding="utf-8") != expected[name]:
            errors.append(f"Drift detected: {name}")
    return errors


def skill_presence(project: Path) -> list[str]:
    """Informational, never assumes that skill presence means skill safety."""
    registry = read_json_yaml(ROOT / "policy/skill-registry.yaml")["skills"]
    roots = [project / ".agents/skills", project / ".claude/skills", project / ".codex/skills", Path.home() / ".agents/skills", Path.home() / ".claude/skills", Path.home() / ".codex/skills"]
    reports = []
    for skill in registry:
        candidate = next((root / skill["skill"] / "SKILL.md" for root in roots if (root / skill["skill"] / "SKILL.md").is_file()), None)
        reports.append(f"SKILL {skill['id']}: {'FOUND ' + str(candidate) if candidate else 'NOT DETECTED'} ({skill['tier']})")
    return reports


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=ROOT / "templates/project.yaml")
    ap.add_argument("--generated", type=Path, help="Compare generated files with canonical sources")
    ap.add_argument("--check-skills", action="store_true", help="Report local skill discovery without auto-installation")
    ap.add_argument("--project", type=Path, default=Path.cwd(), help="Workspace root for local skill discovery")
    args = ap.parse_args()
    try:
        errors = validate_sources(args.config)
        if args.generated:
            errors.extend(validate_generated(args.config, args.generated))
        if args.check_skills:
            for row in skill_presence(args.project):
                print(row)
    except (PolicyError, OSError, KeyError, UnicodeError) as exc:
        errors = [str(exc)]
    for err in errors:
        print(f"FAIL {err}")
    if errors:
        return 1
    print("PASS canonical policy and generated-file consistency" if args.generated else "PASS canonical policy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
