# -*- coding: utf-8 -*-
"""
Validate Freenove tutorial Markdown structure / style-guide conventions.
Usage: python check_md.py <file.md> [--strict]
Exit 0 = pass, 1 = fail.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def check(md: str, strict: bool = False) -> list[str]:
    issues: list[str] = []
    lines = md.splitlines()

    h1 = [ln for ln in lines if re.match(r"^#\s+", ln) and not ln.startswith("##")]
    h2 = [ln for ln in lines if re.match(r"^##\s+", ln)]
    if not h1:
        issues.append("缺少一级标题 `#`（章 / Important Information / Preface）")
    if not any("Chapter" in ln or "章" in ln for ln in h1) and strict:
        issues.append("未发现 Chapter / 章 一级标题（strict）")

    # empty heading
    for i, ln in enumerate(lines, 1):
        if re.match(r"^#{1,3}\s*$", ln):
            issues.append(f"L{i}: 空标题")
        m = re.match(r"^(#{1,3})\s+(.+)$", ln)
        if m and ("\n" in m.group(2) or m.group(2).strip() == ""):
            issues.append(f"L{i}: 标题内容异常")

    # pic convention
    for i, ln in enumerate(lines, 1):
        if "配图" in ln and ln.strip().startswith(">"):
            if not re.search(r"\*\*\[配图\]\*\*|\[配图\]", ln):
                issues.append(f"L{i}: 配图建议写成 `> **[配图]** …`")

    # code fences balanced
    fences = [i for i, ln in enumerate(lines, 1) if ln.strip().startswith("```")]
    if len(fences) % 2:
        issues.append(f"代码围栏未闭合（共 {len(fences)} 个 ```）")

    # Project under Chapter naming hint
    for ln in h2:
        if ln.startswith("## Project"):
            if not re.search(r"Project\s+\d+\.\d+", ln):
                issues.append(f"Project 标题建议含编号：{ln.strip()}")

    # fluff heuristics (soft)
    fluff = ["综上所述", "值得注意的是，在当今", "本文将详细介绍", "首先，我们需要了解"]
    for i, ln in enumerate(lines, 1):
        for f in fluff:
            if f in ln:
                issues.append(f"L{i}: 疑似废话套话「{f}」")

    if strict:
        for i, ln in enumerate(lines, 1):
            if re.match(r"^###\s+Step\s*$", ln.strip()) or ln.strip() == "### Step":
                # ensure following list exists
                j = i
                found = False
                while j < len(lines) and j < i + 15:
                    if re.match(r"^\d+\.\s+", lines[j]):
                        found = True
                        break
                    if re.match(r"^#{1,3}\s+", lines[j]):
                        break
                    j += 1
                if not found:
                    issues.append(f"L{i}: Step 下未发现编号步骤（strict）")

    return issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)
    path = Path(args.input)
    if not path.is_file():
        print(f"ERROR: {path}", file=sys.stderr)
        return 1
    issues = check(path.read_text(encoding="utf-8"), args.strict)
    if not issues:
        print(f"PASS: {path}")
        return 0
    print(f"FAIL: {path} ({len(issues)} issues)")
    for it in issues:
        print(f"  - {it}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
