#!/usr/bin/env python3
"""Render self-contained policy entrypoints; never overwrite user-owned files."""
from __future__ import annotations

import argparse
from pathlib import Path
from common import MARKER, PolicyError, render_contents, safe_output_directory


def render(config: Path, out: Path, force: bool = False) -> list[Path]:
    outputs = render_contents(config)
    safe_output_directory(out)
    for name in outputs:
        target = out / name
        if target.exists():
            if not force:
                raise PolicyError(f"Target exists: {target}; use --force for previously generated files")
            if not target.is_file() or MARKER not in target.read_text(encoding="utf-8")[:220]:
                raise PolicyError(f"Refusing overwrite of non-generated file: {target}")
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, content in outputs.items():
        target = out / name
        target.write_text(content, encoding="utf-8")
        paths.append(target)
    return paths


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parent.parent / "templates/project.yaml")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--force", action="store_true", help="Replace only files previously marked as generated")
    args = ap.parse_args()
    try:
        for path in render(args.config, args.out, args.force):
            print(f"RENDERED {path}")
    except (PolicyError, OSError, UnicodeError) as exc:
        print(f"ERROR {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
