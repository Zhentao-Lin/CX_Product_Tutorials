# -*- coding: utf-8 -*-
"""
One-shot: check_md → md_to_html → check_html
Usage:
  python build.py ../Sample_Tutorial_3Chapters.md
  python build.py ../Sample_Tutorial_3Chapters.md -o ../out.html --inline-css --strict
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd))
    p = subprocess.run(cmd, cwd=str(ROOT))
    return p.returncode


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="ChaoXi tutorial build pipeline")
    ap.add_argument("input", help="source .md")
    ap.add_argument("-o", "--output", help="output .html")
    ap.add_argument("--inline-css", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--skip-check", action="store_true")
    args = ap.parse_args(argv)

    md = Path(args.input).resolve()
    html_out = Path(args.output).resolve() if args.output else md.with_suffix(".html")
    py = sys.executable

    if not args.skip_check:
        rc = run([py, str(ROOT / "check_md.py"), str(md)] + (["--strict"] if args.strict else []))
        if rc != 0:
            return rc

    cmd = [py, str(ROOT / "md_to_html.py"), str(md), "-o", str(html_out)]
    if args.inline_css:
        cmd.append("--inline-css")
    rc = run(cmd)
    if rc != 0:
        return rc

    if not args.skip_check:
        rc = run([py, str(ROOT / "check_html.py"), str(html_out)])
        if rc != 0:
            return rc

    print("BUILD OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
