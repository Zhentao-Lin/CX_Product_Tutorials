# -*- coding: utf-8 -*-
"""
Convert Freenove tutorial Markdown → HTML (Style Guide §13).
Usage:
  python md_to_html.py <input.md> [-o out.html] [--title TITLE] [--inline-css]
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSS_FILE = ROOT / "assets" / "freenove-tutorial.css"


def slugify(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", t, flags=re.UNICODE)
    t = re.sub(r"\s+", "-", t)
    return t or "section"


def inline_format(text: str) -> str:
    """Escape then apply simple inline markdown."""
    # extract code spans first
    parts: list[str] = []
    last = 0
    for m in re.finditer(r"`([^`]+)`", text):
        parts.append(("t", text[last : m.start()]))
        parts.append(("c", m.group(1)))
        last = m.end()
    parts.append(("t", text[last:]))

    out = []
    for kind, val in parts:
        if kind == "c":
            out.append(f"<code>{html.escape(val)}</code>")
            continue
        s = html.escape(val)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(
            r"\[([^\]]+)\]\((https?://[^)]+)\)",
            r'<a href="\2">\1</a>',
            s,
        )
        out.append(s)
    return "".join(out)


def is_table_sep(line: str) -> bool:
    s = line.strip()
    if "|" not in s:
        return False
    return bool(re.match(r"^\|?[\s:\-|]+\|[\s:\-|]*\|?$", s))


def parse_table_row(line: str) -> list[str]:
    s = line.strip().strip("|")
    return [c.strip() for c in s.split("|")]


def convert(md_text: str, page_title: str, css_href: str | None, css_inline: str | None) -> str:
    lines = md_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    body: list[str] = []
    toc_h1: list[tuple[str, str]] = []  # (id, title)
    toc_tree: list[dict] = []  # {id, title, children:[{id,title}]}
    current_h1: dict | None = None

    i = 0
    n = len(lines)

    # skip leading pure metadata blockquotes / title-only note until first real # heading
    # keep content as-is from start

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            code = html.escape("\n".join(code_lines))
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            body.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        # heading
        hm = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if hm:
            level = len(hm.group(1))
            title = hm.group(2).strip()
            # skip document title-like first H1 if it's a meta "Sample Tutorial" banner? keep all
            sid = slugify(title)
            # ensure unique ids
            sid_base = sid
            k = 2
            existing = {x["id"] for x in toc_tree} | {
                c["id"] for x in toc_tree for c in x.get("children", [])
            }
            while sid in existing:
                sid = f"{sid_base}-{k}"
                k += 1

            if level == 1:
                node = {"id": sid, "title": title, "children": []}
                toc_tree.append(node)
                current_h1 = node
                body.append(f'<h1 id="{sid}">{inline_format(title)}</h1>')
            elif level == 2:
                if current_h1 is None:
                    current_h1 = {"id": "preface", "title": "Root", "children": []}
                    toc_tree.append(current_h1)
                current_h1["children"].append({"id": sid, "title": title})
                body.append(f'<h2 id="{sid}">{inline_format(title)}</h2>')
            else:
                body.append(f"<h3>{inline_format(title)}</h3>")
            i += 1
            continue

        # hr
        if re.match(r"^-{3,}\s*$", stripped) or re.match(r"^\*{3,}\s*$", stripped):
            i += 1
            continue

        # blockquote / pic
        if stripped.startswith(">"):
            raw = re.sub(r"^>\s?", "", stripped)
            # unfold continued >
            i += 1
            while i < n and lines[i].strip().startswith(">"):
                raw += " " + re.sub(r"^>\s?", "", lines[i].strip())
                i += 1
            pic_m = re.match(r"\*\*\[配图\]\*\*\s*(.*)$", raw) or re.match(
                r"\[配图\]\s*(.*)$", raw
            )
            if pic_m:
                body.append(f'<div class="pic">[配图] {inline_format(pic_m.group(1).strip())}</div>')
            else:
                body.append(f"<blockquote><p>{inline_format(raw)}</p></blockquote>")
            continue

        # table
        if "|" in stripped and i + 1 < n and is_table_sep(lines[i + 1]):
            headers = parse_table_row(line)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip() and not lines[i].strip().startswith("#"):
                if is_table_sep(lines[i]):
                    i += 1
                    continue
                rows.append(parse_table_row(lines[i]))
                i += 1
            thead = "".join(f"<th>{inline_format(h)}</th>" for h in headers)
            tb = []
            for row in rows:
                # pad/truncate
                cells = (row + [""] * len(headers))[: len(headers)]
                tb.append("<tr>" + "".join(f"<td>{inline_format(c)}</td>" for c in cells) + "</tr>")
            body.append(
                "<table><thead><tr>"
                + thead
                + "</tr></thead><tbody>"
                + "".join(tb)
                + "</tbody></table>"
            )
            continue

        # ordered list
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(f"<li>{inline_format(item)}</li>")
                i += 1
            body.append("<ol>" + "".join(items) + "</ol>")
            continue

        # unordered list
        if re.match(r"^[-*+]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*+]\s+", lines[i].strip()):
                item = re.sub(r"^[-*+]\s+", "", lines[i].strip())
                # skip toc-only nested complexity: flat
                items.append(f"<li>{inline_format(item)}</li>")
                i += 1
            body.append("<ul>" + "".join(items) + "</ul>")
            continue

        # blank
        if not stripped:
            i += 1
            continue

        # paragraph (merge consecutive non-empty non-special lines)
        para = [stripped]
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if not ns:
                break
            if ns.startswith("#") or ns.startswith(">") or ns.startswith("```"):
                break
            if re.match(r"^\d+\.\s+", ns) or re.match(r"^[-*+]\s+", ns):
                break
            if "|" in ns:
                break
            if re.match(r"^-{3,}\s*$", ns):
                break
            para.append(ns)
            i += 1
        body.append("<p>" + inline_format(" ".join(para)) + "</p>")

    # build TOC from h1/h2 only
    toc_html = ['<div class="toc-title">Contents</div>', '<nav class="toc"><ul>']
    for h1 in toc_tree:
        # skip meta titles that look like "Sample Tutorial"
        if h1["title"].startswith("Sample Tutorial"):
            continue
        toc_html.append(
            f'<li><a href="#{h1["id"]}">{html.escape(h1["title"])}</a>'
        )
        if h1["children"]:
            toc_html.append("<ul>")
            for ch in h1["children"]:
                toc_html.append(
                    f'<li><a href="#{ch["id"]}">{html.escape(ch["title"])}</a></li>'
                )
            toc_html.append("</ul>")
        toc_html.append("</li>")
    toc_html.append("</ul></nav>")

    # insert TOC after first block that looks like Important Information section end?
    # Prefer: after first h1 if it's Important Information, before second h1; else prepend after meta
    inserted = False
    final_body: list[str] = []
    h1_count = 0
    for chunk in body:
        final_body.append(chunk)
        if chunk.startswith("<h1 "):
            h1_count += 1
            if h1_count == 1:
                # after important info content until next h1 — defer: insert before 2nd h1
                pass
        if chunk.startswith("<h1 ") and h1_count == 2 and not inserted:
            # insert TOC before this h1
            final_body.pop()
            final_body.extend(toc_html)
            final_body.append(chunk)
            inserted = True
    if not inserted:
        final_body = toc_html + final_body

    if css_inline:
        style_tag = f"<style>\n{css_inline}\n</style>"
    else:
        href = css_href or "assets/freenove-tutorial.css"
        style_tag = f'<link rel="stylesheet" href="{html.escape(href)}" />'

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(page_title)}</title>
{style_tag}
</head>
<body>
<div class="site-header"><a href="https://www.freenove.com">www.freenove.com</a></div>
<article class="page">
<p class="meta">Generated from Markdown · Freenove_Tutorial_Style_Guide §13</p>
{"".join(final_body)}
</article>
</body>
</html>
"""
    return doc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Freenove tutorial MD → HTML")
    ap.add_argument("input", help="input .md path")
    ap.add_argument("-o", "--output", help="output .html path")
    ap.add_argument("--title", help="HTML <title>")
    ap.add_argument(
        "--inline-css",
        action="store_true",
        help="embed CSS into HTML (portable single file)",
    )
    ap.add_argument(
        "--css-href",
        default=None,
        help="stylesheet href if not inline (default: relative to out or assets/...)",
    )
    args = ap.parse_args(argv)

    inp = Path(args.input).resolve()
    if not inp.is_file():
        print(f"ERROR: not found: {inp}", file=sys.stderr)
        return 1

    out = Path(args.output).resolve() if args.output else inp.with_suffix(".html")
    title = args.title or inp.stem

    md_text = inp.read_text(encoding="utf-8")
    css_text = CSS_FILE.read_text(encoding="utf-8") if CSS_FILE.is_file() else ""

    if args.inline_css:
        html_doc = convert(md_text, title, None, css_text)
    else:
        if args.css_href:
            href = args.css_href
        else:
            # relative path from out to CSS_FILE
            try:
                href = os.path.relpath(CSS_FILE, out.parent).replace("\\", "/")
            except ValueError:
                href = str(CSS_FILE)
        html_doc = convert(md_text, title, href, None)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    print(f"OK: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
