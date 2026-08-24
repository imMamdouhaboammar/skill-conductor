"""Unified Command Line Interface for Skill Conductor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compiler import compile_spec, load_spec, validate_spec
from .constants import AGENT_CONFIG_MAP, KNOWN_TARGETS, VERSION
from .exporter import export_adapters
from .installer import detect_installed_agents, install_to_agent
from .packager import package_all_skills, package_skill
from .server import get_skills_catalog
from .validator import validate_all


def cmd_list(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd()
    catalog = get_skills_catalog(repo_root)
    if args.json:
        print(json.dumps(catalog, indent=2))
        return

    print(f"\n🎼 Skill Conductor v{VERSION} — Skills Suite ({len(catalog)} skills)\n")
    print(f"{'Skill Name':<30} {'Evals':<8} {'Description':<50}")
    print("-" * 90)
    for s in catalog:
        eval_str = f"{s['evals_count']} cases" if s["has_evals"] else "None"
        desc = (s["description"][:47] + "...") if len(s["description"]) > 50 else s["description"]
        print(f"{s['name']:<30} {eval_str:<8} {desc:<50}")
    print()


def cmd_install(args: argparse.Namespace) -> None:
    src = Path(args.source).resolve() if args.source else Path.cwd()
    res = install_to_agent(
        skill_or_repo_path=src,
        agent=args.agent,
        workspace_root=Path.cwd(),
        is_global=args.global_install,
    )
    if args.json:
        print(json.dumps(res, indent=2))
        return

    print(f"\n[OK] Installation completed for agent target: {args.agent}")
    if "results" in res:
        for r in res["results"]:
            print(f"  ✓ {r['agent_name']}: {r['count']} skill(s) -> {r['target_path']}")
    else:
        print(f"  ✓ {res['agent_name']}: {res['count']} skill(s) -> {res['target_path']}")
    print()


def cmd_validate(args: argparse.Namespace) -> None:
    skill_path = Path(args.skill_dir).resolve()
    targets = [t.strip() for t in args.targets.split(",") if t.strip()]
    plugin_root = Path(args.plugin_root).resolve() if args.plugin_root else Path.cwd()

    res = validate_all(skill_path, targets, plugin_root)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        status_icon = "✓" if res["pass"] else "✗"
        print(f"\n{status_icon} Validating: {skill_path.name} (targets: {', '.join(targets)})")
        print(f"  Errors: {res['errors']}, Warnings: {res['warnings']}\n")
        for f in res["findings"]:
            prefix = "[ERROR]" if f["severity"] == "error" else "[WARN]"
            print(f"  {prefix} [{f['code']}] {f['message']}")
        print()

    if not res["pass"]:
        sys.exit(1)


def cmd_package(args: argparse.Namespace) -> None:
    skill_path = Path(args.skill_path).resolve()
    out = Path(args.out).resolve() if args.out else Path.cwd() / "dist"

    if (skill_path / "SKILL.md").is_file():
        res = package_skill(skill_path, out)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n[OK] Packaged {res['name']} -> {res['path']}")
            print(f"     SHA256: {res['sha256']}")
            print(f"     Size:   {res['size_bytes']} bytes\n")
    elif (skill_path / "skills").is_dir() or skill_path.name == "skills":
        skills_dir = skill_path if skill_path.name == "skills" else skill_path / "skills"
        results = package_all_skills(skills_dir, out)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"\n[OK] Packaged {len(results)} skill(s) into {out}")
            for r in results:
                print(f"  ✓ {r['name']}.skill ({r['size_bytes']} bytes) - {r['sha256'][:12]}...")
            print()
    else:
        print(f"[ERROR] Path does not contain SKILL.md or skills/ directory: {skill_path}")
        sys.exit(1)


def cmd_compile(args: argparse.Namespace) -> None:
    spec_path = Path(args.spec).resolve()
    out_dir = Path(args.out).resolve()
    if args.check:
        spec = load_spec(spec_path)
        validate_spec(spec)
        print(json.dumps({"valid": True, "name": spec["name"]}))
        return

    out_path = compile_spec(spec_path, out_dir)
    print(json.dumps({"compiled": True, "path": str(out_path)}, indent=2))


def cmd_export(args: argparse.Namespace) -> None:
    root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd()
    out = Path(args.out).resolve() if args.out else root / "dist" / "adapters"
    targets = (
        [t.strip() for t in args.targets.split(",") if t.strip()]
        if args.targets
        else None
    )
    res = export_adapters(root, out, targets)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"\n[OK] Exported {len(res)} host adapter bundle(s) -> {out}\n")
        for r in res:
            print(f"  ✓ {r['target']:<15} -> {r['output']}")
        print()


def cmd_doctor(args: argparse.Namespace) -> None:
    root = Path(args.repo_root).resolve() if args.repo_root else Path.cwd()
    detected = detect_installed_agents(root)

    print(f"\n🏥 Skill Conductor Doctor v{VERSION}\n")
    print(f"Workspace root: {root}")
    print("\nDetected Agent Environments:")
    print("-" * 50)
    for agent, is_present in detected.items():
        icon = "✓ Installed" if is_present else "○ Not configured"
        config = AGENT_CONFIG_MAP[agent]
        print(f"  {icon:<18} {config['name']:<35} ({agent})")
    print("\nSupported Host Targets:")
    print("  " + ", ".join(sorted(KNOWN_TARGETS)))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="skill-conductor",
        description="Skill Conductor — Cross-host Skill engineering toolkit and plugin.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # list
    p_list = subparsers.add_parser("list", help="List all available skills in suite")
    p_list.add_argument("--repo-root", type=str, help="Repository root directory")
    p_list.add_argument("--json", action="store_true", help="Output as JSON")
    p_list.set_defaults(func=cmd_list)

    # install
    p_install = subparsers.add_parser("install", help="Install skills to target agent environments")
    p_install.add_argument(
        "--agent",
        default="all",
        help="Target agent (claude-code, codex, chatgpt, antigravity, cursor, windsurf, opencode, dsh, all)",
    )
    p_install.add_argument("--source", type=str, help="Path to skill or repository root")
    p_install.add_argument(
        "--global",
        dest="global_install",
        action="store_true",
        help="Install globally in user home instead of workspace",
    )
    p_install.add_argument("--json", action="store_true", help="Output as JSON")
    p_install.set_defaults(func=cmd_install)

    # validate
    p_val = subparsers.add_parser("validate", help="Validate skill structure and portability")
    p_val.add_argument("skill_dir", type=str, help="Path to skill folder")
    p_val.add_argument(
        "--targets",
        default="agent-skills,chatgpt,codex,claude-code,antigravity,cursor,windsurf,opencode,skills-sh,dsh",
        help="Comma-separated target list",
    )
    p_val.add_argument("--plugin-root", type=str, help="Plugin root path")
    p_val.add_argument("--json", action="store_true", help="Output as JSON")
    p_val.set_defaults(func=cmd_validate)

    # package
    p_pack = subparsers.add_parser("package", help="Package skill into .skill archive")
    p_pack.add_argument("skill_path", type=str, help="Skill folder or skills root")
    p_pack.add_argument("--out", type=str, help="Output directory")
    p_pack.add_argument("--json", action="store_true", help="Output as JSON")
    p_pack.set_defaults(func=cmd_package)

    # compile
    p_comp = subparsers.add_parser("compile", help="Compile SkillSpec JSON into Skill scaffold")
    p_comp.add_argument("--spec", required=True, type=str, help="SkillSpec JSON path")
    p_comp.add_argument("--out", required=True, type=str, help="Output directory")
    p_comp.add_argument("--check", action="store_true", help="Validate only without writing")
    p_comp.set_defaults(func=cmd_compile)

    # export
    p_exp = subparsers.add_parser("export", help="Export host adapter packages")
    p_exp.add_argument("--repo-root", type=str, help="Repository root directory")
    p_exp.add_argument("--out", type=str, help="Output directory")
    p_exp.add_argument("--targets", type=str, help="Comma-separated host target list")
    p_exp.add_argument("--json", action="store_true", help="Output as JSON")
    p_exp.set_defaults(func=cmd_export)

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Inspect local agent environments")
    p_doc.add_argument("--repo-root", type=str, help="Repository root directory")
    p_doc.set_defaults(func=cmd_doctor)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
