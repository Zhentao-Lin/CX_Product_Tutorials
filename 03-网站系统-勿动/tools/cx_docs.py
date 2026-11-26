#!/usr/bin/env python3
"""
CX 教程站维护工具：只维护 02-可编辑内容（catalog + 章节 MD），自动同步 Sphinx 并构建。

用法（在仓库根目录）:
  python "03-网站系统-勿动/tools/cx_docs.py" sync
  python "03-网站系统-勿动/tools/cx_docs.py" build [--open]
  python "03-网站系统-勿动/tools/cx_docs.py" new-product --id CX_... --title "标题"
  python "03-网站系统-勿动/tools/cx_docs.py" new-chapter --product CX_... --file 03-foo --title "章节名"
  python "03-网站系统-勿动/tools/cx_docs.py" serve
  python "03-网站系统-勿动/tools/cx_docs.py" preview-html --md 02-可编辑内容/products/.../01-xxx.md
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import webbrowser
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
# .../03-网站系统-勿动/tools/cx_docs.py → parents[2] = 仓库根
ROOT = TOOLS_DIR.parents[1]
SYSTEM = ROOT / "03-网站系统-勿动"
EDITABLE = ROOT / "02-可编辑内容"
GUIDES = ROOT / "01-使用说明"

FREENOVE_STYLE = TOOLS_DIR / "freenove_style"

CATALOG = EDITABLE / "catalog" / "products.yml"
HOME_MD = EDITABLE / "catalog" / "home.md"
PRODUCTS = EDITABLE / "products"

# Sphinx 源目录（勿手改）；products 通过链接指向 02-可编辑内容/products
SOURCE = SYSTEM / "sphinx-source"
BUILD_OUT = SYSTEM / "_build" / "html"
REQUIREMENTS = SOURCE / "requirements.txt"

NAV_FOOTER = """
---

[← 返回本产品教程大纲](index.md) · [↑ 返回总产品大纲](../../index.md)
""".strip()

ASSET_SUBDIRS = ("images", "attachments", "code", "data")


def _need_yaml():
    try:
        import yaml  # noqa: F401
    except ImportError:
        print(
            f'请先安装依赖: pip install -r "{REQUIREMENTS.as_posix()}"',
            file=sys.stderr,
        )
        sys.exit(1)


def _unlink_if_exists(path: Path) -> None:
    if path.is_file() or path.is_symlink():
        path.unlink()
    elif path.is_dir():
        # 不要删真正的产品目录；仅清理错误占位
        pass


def ensure_products_link() -> None:
    """让 sphinx-source/products → 02-可编辑内容/products（CI / 本地构建用）。"""
    SOURCE.mkdir(parents=True, exist_ok=True)
    PRODUCTS.mkdir(parents=True, exist_ok=True)
    link = SOURCE / "products"
    target = PRODUCTS.resolve()

    if link.exists() or link.is_symlink():
        try:
            if link.resolve() == target or os.path.samefile(link, target):
                return
        except OSError:
            pass
        if link.is_symlink() or link.is_file():
            link.unlink()
        elif link.is_dir():
            raise SystemExit(
                f"冲突: {link} 已是普通目录。请删掉后重跑 sync（应联接到 {target}）"
            )

    if os.name == "nt":
        r = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if r.returncode != 0:
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as e:
                raise SystemExit(f"无法创建 products 链接: {e}\n{r.stderr}") from e
    else:
        link.symlink_to(target, target_is_directory=True)


def ensure_product_asset_dirs(product_id: str) -> None:
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
        SOURCE / "_static" / "css",
    ):
        path.mkdir(parents=True, exist_ok=True)
        if path.name != "css":
            keep = path / ".gitkeep"
            if not keep.exists():
                keep.touch()


def load_catalog() -> list[dict]:
    _need_yaml()
    import yaml

    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    products = data.get("products") or []
    if not products:
        raise SystemExit(f"未在 {CATALOG} 中找到任何产品")
    return products


def save_catalog(products: list[dict]) -> None:
    _need_yaml()
    import yaml

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
    d = PRODUCTS / product_id
    if not d.is_dir():
        return []
    items: list[tuple[str, str]] = []
    for md in sorted(d.glob("*.md")):
        if md.name in ("outline.md", "index.md"):
            continue
        items.append((md.stem, chapter_title_from_md(md)))
    return items


def write_root_index(products: list[dict]) -> None:
    if not HOME_MD.is_file():
        HOME_MD.parent.mkdir(parents=True, exist_ok=True)
        HOME_MD.write_text(
            "本站为 **总产品大纲**。\n\n请在左侧目录选择产品。\n",
            encoding="utf-8",
        )
    home = HOME_MD.read_text(encoding="utf-8").strip()
    lines = [
        "<!-- 由 cx_docs.py 自动生成，请勿手改；请编辑 02-可编辑内容/catalog/ -->",
        "",
        "# CX 硬件产品教程",
        "",
        home,
        "",
        "```{toctree}",
        ":maxdepth: 2",
        ":caption: 产品列表",
        "",
    ]
    for p in products:
        lines.append(f"products/{p['id']}/index")
    lines.extend(["```", ""])
    out = SOURCE / "index.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    rst = SOURCE / "index.rst"
    if rst.is_file():
        rst.unlink()


def write_product_index(product: dict, chapters: list[tuple[str, str]]) -> None:
    pid = product["id"]
    title = product["title"]
    summary = (product.get("summary") or "").strip()
    status = product.get("status") or ""

    lines = [
        "<!-- 由 cx_docs.py 自动生成，请勿手改；请编辑 catalog 与章节 .md -->",
        "",
        f"# {title}",
        "",
        f"**产品 ID：** `{pid}`",
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
        lines.append(outline_md.read_text(encoding="utf-8").strip())
        lines.append("")
    lines.extend(
        [
            "本页为 **产品教程大纲**；章节见下方目录与左侧导航。",
            "",
            "[← 返回总产品大纲](../../index.md)",
            "",
        ]
    )
    if chapters:
        lines.extend(
            [
                "```{toctree}",
                ":maxdepth: 1",
                ":caption: 章节",
                "",
            ]
        )
        for stem, _title in chapters:
            lines.append(stem)
        lines.extend(["```", ""])
    else:
        lines.append("（暂无章节：在本目录添加 `01-xxx.md` 后执行 sync。）")
        lines.append("")

    out_dir = PRODUCTS / pid
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    old = out_dir / "index.rst"
    if old.is_file():
        old.unlink()


def ensure_nav_footer(md_path: Path) -> bool:
    if md_path.name in ("index.md", "outline.md"):
        return False
    text = md_path.read_text(encoding="utf-8")
    original = text
    text = text.replace("index.rst", "index.md")
    if "返回本产品教程大纲" not in text:
        text = text.rstrip() + "\n\n" + NAV_FOOTER + "\n"
    if text != original:
        md_path.write_text(text, encoding="utf-8")
        return True
    return False


def cmd_sync(_: argparse.Namespace) -> int:
    ensure_global_static_dirs()
    ensure_products_link()
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

    orphans = [p["id"] for p in products if not (PRODUCTS / p["id"]).is_dir()]
    if orphans:
        print("警告: 下列产品尚未创建目录（可用 new-product）:", ", ".join(orphans))

    print(f"sync 完成: {len(products)} 个产品 → {SOURCE / 'index.md'}")
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

    (PRODUCTS / pid).mkdir(parents=True, exist_ok=True)
    md_path.write_text(
        f"""# {args.title}

一句话说明本章做什么。

## 本章目标

1. （目标）

## Step

1. （第一步）

> **[配图]** （必要时补充）

## Code

```cpp
// TODO
```

## If It Fails

- （排查）

{NAV_FOOTER}
""",
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
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
        cwd=ROOT,
    )
    if r.returncode != 0:
        raise SystemExit(
            f"依赖安装失败。请执行: pip install -r \"{REQUIREMENTS.as_posix()}\""
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
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "-r",
            str(REQUIREMENTS),
            "sphinx-autobuild",
        ],
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


def _resolve_md(path_str: str) -> Path:
    p = Path(path_str)
    if not p.is_absolute():
        p = (ROOT / p).resolve()
    if not p.is_file():
        raise SystemExit(f"找不到 Markdown: {p}")
    return p


def cmd_preview_html(args: argparse.Namespace) -> int:
    md = _resolve_md(args.md)
    out = Path(args.output).resolve() if args.output else md.with_suffix(".freenove.html")
    build_py = FREENOVE_STYLE / "build.py"
    if not build_py.is_file():
        raise SystemExit(f"缺少工具: {build_py}")
    cmd = [sys.executable, str(build_py), str(md), "-o", str(out)]
    if not args.no_inline_css:
        cmd.append("--inline-css")
    if args.strict:
        cmd.append("--strict")
    r = subprocess.run(cmd, cwd=str(FREENOVE_STYLE))
    if r.returncode != 0:
        return r.returncode
    print(f"Freenove 预览: {out}")
    if args.open and out.is_file():
        webbrowser.open(out.as_uri())
    return 0


def cmd_check_md(args: argparse.Namespace) -> int:
    md = _resolve_md(args.md)
    cmd = [sys.executable, str(FREENOVE_STYLE / "check_md.py"), str(md)]
    if args.strict:
        cmd.append("--strict")
    return subprocess.run(cmd, cwd=str(FREENOVE_STYLE)).returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CX 教程站：02-可编辑内容 → Sphinx Pages"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="同步目录并生成 index.md")
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
    p_build.add_argument("--open", action="store_true")
    p_build.set_defaults(func=cmd_build)

    p_serve = sub.add_parser("serve", help="本地热重载预览")
    p_serve.set_defaults(func=cmd_serve)

    p_prev = sub.add_parser("preview-html", help="Freenove 单页 HTML 预览")
    p_prev.add_argument("--md", required=True)
    p_prev.add_argument("-o", "--output")
    p_prev.add_argument("--open", action="store_true")
    p_prev.add_argument("--no-inline-css", action="store_true")
    p_prev.add_argument("--strict", action="store_true")
    p_prev.set_defaults(func=cmd_preview_html)

    p_chk = sub.add_parser("check-md", help="校验章节 MD")
    p_chk.add_argument("--md", required=True)
    p_chk.add_argument("--strict", action="store_true")
    p_chk.set_defaults(func=cmd_check_md)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
