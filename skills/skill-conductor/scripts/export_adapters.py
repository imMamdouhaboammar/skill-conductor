#!/usr/bin/env python3
"""Export host adapter packages for Skill Conductor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add project root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from skill_conductor.exporter import export_adapters


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "dist" / "adapters")
    parser.add_argument("--targets", type=str, help="Comma-separated target list")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    targets = (
        [t.strip() for t in args.targets.split(",") if t.strip()]
        if args.targets
        else None
    )
    res = export_adapters(args.repo_root, args.out, targets)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"\n[OK] Exported {len(res)} host adapter bundle(s) -> {args.out}\n")
        for r in res:
            print(f"  ✓ {r['target']:<15} -> {r['output']}")
        print()


if __name__ == "__main__":
    main()
