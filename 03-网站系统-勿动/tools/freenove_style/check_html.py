# -*- coding: utf-8 -*-
"""
Validate Freenove tutorial HTML against Style Guide §13.
Usage: python check_html.py <file.html>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def check(html_text: str) -> list[str]:
    issues: list[str] = []
    if "www.freenove.com" not in html_text:
        issues.append("缺少页眉/站点 www.freenove.com")
    if "#E3760C" not in html_text and "--fn-orange" not in html_text:
        issues.append("未检测到品牌色 #E3760C / --fn-orange（内联或外链 CSS）")
    if "site-header" not in html_text:
        issues.append("缺少 .site-header")
    if "toc-title" not in html_text and 'class="toc"' not in html_text:
        issues.append("缺少 Contents（.toc-title / .toc）")

    # empty headings
    for m in re.finditer(r"<h([123])(\s[^>]*)?>(.*?)</h\1>", html_text, re.I | re.S):
        inner = re.sub(r"<[^>]+>", "", m.group(3)).strip()
        if not inner:
            issues.append(f"存在空 h{m.group(1)}")
        if "\n\n" in m.group(3):
            issues.append(f"h{m.group(1)} 内含多余空行（可能导致橙条变高）")

    if "<table" in html_text and "#ED7D31" not in html_text and "--table-header" not in html_text:
        # if external css, ok if linked
        if "freenove-tutorial.css" not in html_text and "--table-header" not in html_text:
            issues.append("有表格但未看到表头橙色变量/色值（确认 CSS 已引用）")

    if "<pre" in html_text and "Courier New" not in html_text and "freenove-tutorial.css" not in html_text:
        issues.append("有代码块但未看到 Courier New（确认 CSS）")

    return issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    args = ap.parse_args(argv)
    path = Path(args.input)
    if not path.is_file():
        print(f"ERROR: {path}", file=sys.stderr)
        return 1
    issues = check(path.read_text(encoding="utf-8"))
    if not issues:
        print(f"PASS: {path}")
        return 0
    print(f"FAIL: {path} ({len(issues)} issues)")
    for it in issues:
        print(f"  - {it}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
