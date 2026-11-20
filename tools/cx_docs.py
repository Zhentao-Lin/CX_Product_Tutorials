#!/usr/bin/env python3
"""
CX 教程站维护工具：只维护 catalog + Markdown，自动同步 Sphinx 目录并构建。

用法:
  python tools/cx_docs.py sync
  python tools/cx_docs.py new-product --id CX_... --title "标题"
  python tools/cx_docs.py new-chapter --product CX_... --file 03-foo --title "章节名"
  python tools/cx_docs.py build [--open]
  python tools/cx_docs.py serve
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

try:
    import yaml
except ImportError:
    print("请先安装依赖: pip install -r docs/requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "products.yml"
HOME_MD = ROOT / "catalog" / "home.md"
SOURCE = ROOT / "docs" / "source"
PRODUCTS = SOURCE / "products"
TEMPLATES = ROOT / "templates"
BUILD_OUT = ROOT / "docs" / "_build" / "html"

GENERATED_BANNER_RST = (
    ".. 本文件由 tools/cx_docs.py 自动生成，请勿手改；请编辑 catalog/products.yml 与各章节 .md。\n\n"
)

NAV_FOOTER = """
---

[← 返回本产品教程大纲](index.rst) · [↑ 返回总产品大纲](../../index.rst)
""".strip()

ASSET_SUBDIRS = ("images", "attachments", "code", "data")


def ensure_product_asset_dirs(product_id: str) -> None:
    """为每个产品创建 assets 子目录（images / attachments / code / data）。"""
    base = PRODUCTS / product_id / "assets"
    for name in ASSET_SUBDIRS:
        d = base / name
        d.mkdir(parents=True, exist_ok=True)
        keep = d / ".gitkeep"
        if not keep.exists():
            keep.touch()


def ensure_global_static_dirs() -> None:
    for path in (
        SOURCE / "_static" / "images",
        SOURCE / "_static" / "downloads",
    ):
        path.mkdir(parents=True, exist_ok=True)
        keep = path / ".gitkeep"
        if not keep.exists():
            keep.touch()


def load_catalog() -> list[dict]:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    products = data.get("products") or []
    if not products:
        raise SystemExit(f"未在 {CATALOG} 中找到任何产品")
    return products


def save_catalog(products: list[dict]) -> None:
    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.dump(
        {"products": products},
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    CATALOG.write_text(
        "# 产品清单（章节不用写在这里：各产品目录下的 *.md 会自动进入目录）\n" + text,
        encoding="utf-8",
    )


def chapter_title_from_md(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"^#\s+(.+)", line.strip())
        if m:
            return m.group(1).strip()
    return path.stem.replace("-", " ")


def list_chapters(product_id: str) -> list[tuple[str, str]]:
    """返回 [(filename_without_path, title), ...] 按文件名排序"""
    d = PRODUCTS / product_id
    if not d.is_dir():
        return []
    items: list[tuple[str, str]] = []
    for md in sorted(d.glob("*.md")):
        if md.name in ("outline.md",):
            continue
        stem = md.stem
        items.append((stem, chapter_title_from_md(md)))
    return items


def write_root_index(products: list[dict]) -> None:
    if not HOME_MD.is_file():
        HOME_MD.parent.mkdir(parents=True, exist_ok=True)
        HOME_MD.write_text(
            "本站为 **总产品大纲**。\n\n请在左侧目录选择产品。\n",
            encoding="utf-8",
        )
    lines = [
        GENERATED_BANNER_RST.rstrip(),
        "CX 硬件产品教程",
        "=" * 12,
        "",
        ".. include:: ../../catalog/home.md",
        "   :parser: myst_parser.parsers.sphinx_.SphinxParser",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "   :caption: 产品列表",
        "",
    ]
    for p in products:
        pid = p["id"]
        lines.append(f"   products/{pid}/index")
    lines.append("")
    path = SOURCE / "index.rst"
    path.write_text("\n".join(lines), encoding="utf-8")


def write_product_index(product: dict, chapters: list[tuple[str, str]]) -> None:
    pid = product["id"]
    title = product["title"]
    summary = (product.get("summary") or "").strip()
    status = product.get("status") or ""

    lines = [
        GENERATED_BANNER_RST.rstrip(),
        title,
        "=" * max(8, len(title)),
        "",
        f"**产品 ID：** ``{pid}``",
        "",
    ]
    if status:
        lines.append(f"**状态：** {status}")
        lines.append("")
    if summary:
        lines.extend(summary.splitlines())
        lines.append("")
    outline_md = PRODUCTS / pid / "outline.md"
    if outline_md.is_file():
        lines.extend(
            [
                ".. include:: outline.md",
                "   :parser: myst_parser.parsers.sphinx_.SphinxParser",
                "",
            ]
        )
    lines.extend(
        [
            "本页为 **产品教程大纲**；章节见下方目录与左侧导航。",
            "",
            ":doc:`返回总产品大纲 </index>`",
            "",
        ]
    )
    if chapters:
        lines.extend(
            [
                ".. toctree::",
                "   :maxdepth: 1",
                "   :caption: 章节",
                "",
            ]
        )
        for stem, _title in chapters:
            lines.append(f"   {stem}")
        lines.append("")
    else:
        lines.append("（暂无章节：在本目录添加 ``01-xxx.md`` 后执行 sync。）")
        lines.append("")

    out_dir = PRODUCTS / pid
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.rst").write_text("\n".join(lines), encoding="utf-8")


def ensure_nav_footer(md_path: Path) -> bool:
    text = md_path.read_text(encoding="utf-8")
    if "返回本产品教程大纲" in text:
        return False
    new_text = text.rstrip() + "\n\n" + NAV_FOOTER + "\n"
    md_path.write_text(new_text, encoding="utf-8")
    return True


def cmd_sync(_: argparse.Namespace) -> int:
    ensure_global_static_dirs()
    products = load_catalog()
    seen: set[str] = set()
    for product in products:
        pid = product["id"]
        if pid in seen:
            raise SystemExit(f"重复的产品 ID: {pid}")
        seen.add(pid)
        if (PRODUCTS / pid).is_dir():
            ensure_product_asset_dirs(pid)
        chapters = list_chapters(pid)
        if not (PRODUCTS / pid).is_dir() and chapters:
            raise SystemExit(f"产品目录不存在: {PRODUCTS / pid}")
        for md in (PRODUCTS / pid).glob("*.md"):
            ensure_nav_footer(md)
        write_product_index(product, chapters)

    write_root_index(products)

    # 校验 catalog 中有条目但无目录
    orphans = [p["id"] for p in products if not (PRODUCTS / p["id"]).is_dir()]
    if orphans:
        print("警告: 下列产品尚未创建目录（可用 new-product）:", ", ".join(orphans))

    print(f"sync 完成: {len(products)} 个产品, 根目录 {SOURCE / 'index.rst'} 已更新")
    return 0


def cmd_new_product(args: argparse.Namespace) -> int:
    pid = args.id.strip()
    if not re.match(r"^CX_[\w]+$", pid):
        print("建议产品 ID 形如 CX_ESP32_S31_Module_Xiaozhi_Board", file=sys.stderr)

    products = load_catalog()
    if any(p["id"] == pid for p in products):
        raise SystemExit(f"产品已存在: {pid}")

    products.append(
        {
            "id": pid,
            "title": args.title,
            "status": args.status or "策划中",
            "summary": args.summary or f"{args.title} 教程（待补充简介）。\n",
        }
    )
    save_catalog(products)

    (PRODUCTS / pid).mkdir(parents=True, exist_ok=True)
    ensure_product_asset_dirs(pid)
    # 可选首章
    if args.chapter:
        chap_file = args.chapter
        if not chap_file.endswith(".md"):
            chap_file += ".md"
        chap_path = PRODUCTS / pid / chap_file
        title = args.chapter_title or "概述"
        chap_path.write_text(
            f"# {title}\n\n（在此编写正文。）\n\n{NAV_FOOTER}\n",
            encoding="utf-8",
        )

    cmd_sync(argparse.Namespace())
    print(f"已创建产品 {pid} @ {PRODUCTS / pid}")
    return 0


def cmd_new_chapter(args: argparse.Namespace) -> int:
    pid = args.product
    products = load_catalog()
    if not any(p["id"] == pid for p in products):
        raise SystemExit(f"未知产品: {pid}（先用 new-product 或写入 catalog）")

    stem = args.file.removesuffix(".md")
    if not re.match(r"^\d{2}-[\w-]+$", stem):
        print("建议章节文件名: 03-short-name（两位数字前缀）", file=sys.stderr)

    md_path = PRODUCTS / pid / f"{stem}.md"
    if md_path.exists():
        raise SystemExit(f"文件已存在: {md_path}")

    PRODUCTS / pid
    (PRODUCTS / pid).mkdir(parents=True, exist_ok=True)
    md_path.write_text(
        f"# {args.title}\n\n## 本章目标\n\n（待编写。）\n\n{NAV_FOOTER}\n",
        encoding="utf-8",
    )
    cmd_sync(argparse.Namespace())
    print(f"已创建章节 {md_path}")
    return 0


def ensure_sphinx_deps() -> None:
    try:
        import sphinx  # noqa: F401
        import yaml  # noqa: F401
        import myst_parser  # noqa: F401
        return
    except ImportError:
        pass
    req = ROOT / "docs" / "requirements.txt"
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(req)],
        cwd=ROOT,
    )
    if r.returncode != 0:
        raise SystemExit(
            "依赖安装失败。建议: python -m venv .venv && .venv\\Scripts\\activate && "
            "pip install -r docs/requirements.txt"
        )


def run_sphinx(extra: list[str] | None = None) -> None:
    BUILD_OUT.parent.mkdir(parents=True, exist_ok=True)
    ensure_sphinx_deps()
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        str(SOURCE),
        str(BUILD_OUT),
        "-W",
        "--keep-going",
    ]
    if extra:
        cmd.extend(extra)
    subprocess.run(cmd, check=True, cwd=ROOT)


def cmd_build(args: argparse.Namespace) -> int:
    cmd_sync(argparse.Namespace())
    run_sphinx()
    print(f"构建完成: {BUILD_OUT / 'index.html'}")
    if args.open and (BUILD_OUT / "index.html").is_file():
        webbrowser.open((BUILD_OUT / "index.html").as_uri())
    return 0


def cmd_serve(_: argparse.Namespace) -> int:
    cmd_sync(argparse.Namespace())
    req = ROOT / "docs" / "requirements.txt"
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(req), "sphinx-autobuild"],
        check=True,
        cwd=ROOT,
    )
    subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx_autobuild",
            str(SOURCE),
            str(BUILD_OUT),
            "--open-browser",
        ],
        cwd=ROOT,
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="CX 教程站：catalog + MD → Sphinx")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="根据 catalog 与各产品 *.md 生成 index.rst")
    p_sync.set_defaults(func=cmd_sync)

    p_np = sub.add_parser("new-product", help="登记新产品并创建目录")
    p_np.add_argument("--id", required=True)
    p_np.add_argument("--title", required=True)
    p_np.add_argument("--status", default="策划中")
    p_np.add_argument("--summary", default="")
    p_np.add_argument("--chapter", help="可选首章文件名，如 01-overview")
    p_np.add_argument("--chapter-title", default="概述")
    p_np.set_defaults(func=cmd_new_product)

    p_nc = sub.add_parser("new-chapter", help="在某产品下新建章节 MD")
    p_nc.add_argument("--product", required=True)
    p_nc.add_argument("--file", required=True, help="如 03-wifi")
    p_nc.add_argument("--title", required=True)
    p_nc.set_defaults(func=cmd_new_chapter)

    p_build = sub.add_parser("build", help="sync + sphinx-build")
    p_build.add_argument("--open", action="store_true", help="构建后用浏览器打开")
    p_build.set_defaults(func=cmd_build)

    p_serve = sub.add_parser("serve", help="sync + 本地热重载预览")
    p_serve.set_defaults(func=cmd_serve)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())