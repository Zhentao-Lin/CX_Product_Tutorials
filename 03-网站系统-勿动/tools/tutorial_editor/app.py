"""
本地教程编辑器：改 MD、预览、保存（git commit）、发布（git push）。
仅监听 127.0.0.1，请勿暴露到公网。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory

# app.py → tutorial_editor → tools → 03-网站系统-勿动 → 仓库根
ROOT = Path(__file__).resolve().parents[3]
SYSTEM = ROOT / "03-网站系统-勿动"
if str(SYSTEM) not in sys.path:
    sys.path.insert(0, str(SYSTEM))

from tools import cx_docs  # noqa: E402

PRODUCTS = cx_docs.PRODUCTS
CATALOG = cx_docs.CATALOG
SOURCE = cx_docs.SOURCE
NAV_FOOTER = cx_docs.NAV_FOOTER
HOME_MD = cx_docs.HOME_MD

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)


def safe_product_id(pid: str) -> bool:
    return bool(re.match(r"^CX_[\w]+$", pid or ""))


def safe_chapter_stem(stem: str) -> bool:
    return bool(re.match(r"^\d{2}-[\w-]+$", stem or ""))


def chapter_path(product_id: str, stem: str) -> Path:
    if not safe_product_id(product_id) or not safe_chapter_stem(stem):
        raise ValueError("非法路径")
    return PRODUCTS / product_id / f"{stem}.md"


def run_git(args: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    p = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/products")
def api_products():
    products = cx_docs.load_catalog()
    out = []
    for p in products:
        pid = p["id"]
        chapters = [
            {"stem": stem, "title": title}
            for stem, title in cx_docs.list_chapters(pid)
        ]
        out.append(
            {
                "id": pid,
                "title": p.get("title", pid),
                "status": p.get("status", ""),
                "chapters": chapters,
            }
        )
    return jsonify(products=out)


@app.get("/api/home")
def api_get_home():
    if not HOME_MD.is_file():
        HOME_MD.parent.mkdir(parents=True, exist_ok=True)
        HOME_MD.write_text("# 总产品大纲说明\n\n", encoding="utf-8")
    return jsonify(content=HOME_MD.read_text(encoding="utf-8"))


@app.put("/api/home")
def api_put_home():
    data = request.get_json(force=True) or {}
    content = data.get("content", "")
    HOME_MD.parent.mkdir(parents=True, exist_ok=True)
    HOME_MD.write_text(content, encoding="utf-8")
    cx_docs.cmd_sync(type("NS", (), {})())
    return jsonify(ok=True)


@app.get("/api/product")
def api_get_product():
    pid = request.args.get("id", "")
    if not safe_product_id(pid):
        return jsonify(error="非法产品 ID"), 400
    products = cx_docs.load_catalog()
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return jsonify(error="产品不存在"), 404
    outline = PRODUCTS / pid / "outline.md"
    outline_text = outline.read_text(encoding="utf-8") if outline.is_file() else ""
    return jsonify(
        id=pid,
        title=product.get("title", ""),
        status=product.get("status", ""),
        summary=product.get("summary", ""),
        outline=outline_text,
    )


@app.put("/api/product")
def api_put_product():
    data = request.get_json(force=True) or {}
    pid = data.get("id", "")
    if not safe_product_id(pid):
        return jsonify(error="非法产品 ID"), 400
    products = cx_docs.load_catalog()
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return jsonify(error="产品不存在"), 404
    product["title"] = data.get("title") or product["title"]
    product["status"] = data.get("status", product.get("status", ""))
    product["summary"] = data.get("summary", product.get("summary", ""))
    cx_docs.save_catalog(products)
    outline = (data.get("outline") or "").strip()
    outline_path = PRODUCTS / pid / "outline.md"
    if outline:
        outline_path.write_text(outline + "\n", encoding="utf-8")
    elif outline_path.is_file():
        outline_path.unlink()
    cx_docs.cmd_sync(type("NS", (), {})())
    return jsonify(ok=True)


@app.post("/api/product")
def api_new_product():
    data = request.get_json(force=True) or {}
    pid = (data.get("id") or "").strip()
    title = (data.get("title") or "").strip()
    if not safe_product_id(pid) or not title:
        return jsonify(error="需要合法产品 ID（CX_...）和中文标题"), 400
    products = cx_docs.load_catalog()
    if any(p["id"] == pid for p in products):
        return jsonify(error="产品 ID 已存在"), 409
    products.append(
        {
            "id": pid,
            "title": title,
            "status": data.get("status") or "策划中",
            "summary": data.get("summary") or f"{title} 教程\n",
        }
    )
    cx_docs.save_catalog(products)
    (PRODUCTS / pid).mkdir(parents=True, exist_ok=True)
    cx_docs.ensure_product_asset_dirs(pid)
    if data.get("chapter"):
        stem = data["chapter"].removesuffix(".md")
        if safe_chapter_stem(stem):
            chap_title = data.get("chapter_title") or "概述"
            (PRODUCTS / pid / f"{stem}.md").write_text(
                f"# {chap_title}\n\n## 本章目标\n\n（待编写。）\n\n{NAV_FOOTER}\n",
                encoding="utf-8",
            )
    cx_docs.cmd_sync(type("NS", (), {})())
    return jsonify(ok=True, id=pid)


@app.get("/api/chapter")
def api_get_chapter():
    pid = request.args.get("product", "")
    stem = request.args.get("stem", "")
    path = chapter_path(pid, stem)
    if not path.is_file():
        return jsonify(error="章节不存在"), 404
    return jsonify(
        product=pid,
        stem=stem,
        content=path.read_text(encoding="utf-8"),
    )


@app.put("/api/chapter")
def api_put_chapter():
    data = request.get_json(force=True) or {}
    pid = data.get("product", "")
    stem = data.get("stem", "")
    content = data.get("content", "")
    path = chapter_path(pid, stem)
    if not path.is_file():
        return jsonify(error="章节不存在"), 404
    path.write_text(content, encoding="utf-8")
    if "返回本产品教程大纲" not in content:
        cx_docs.ensure_nav_footer(path)
    return jsonify(ok=True)


@app.post("/api/chapter")
def api_new_chapter():
    data = request.get_json(force=True) or {}
    pid = data.get("product", "")
    stem = (data.get("stem") or "").removesuffix(".md")
    title = data.get("title") or "新章节"
    if not safe_product_id(pid) or not safe_chapter_stem(stem):
        return jsonify(error="产品 ID 或章节名不合法（章节请用 03-xxx 格式）"), 400
    path = chapter_path(pid, stem)
    if path.exists():
        return jsonify(error="章节已存在"), 409
    (PRODUCTS / pid).mkdir(parents=True, exist_ok=True)
    cx_docs.ensure_product_asset_dirs(pid)
    body = f"# {title}\n\n## 本章目标\n\n（待编写。）\n\n{NAV_FOOTER}\n"
    path.write_text(body, encoding="utf-8")
    cx_docs.cmd_sync(type("NS", (), {})())
    return jsonify(ok=True, stem=stem)


@app.delete("/api/chapter")
def api_delete_chapter():
    pid = request.args.get("product", "")
    stem = request.args.get("stem", "")
    path = chapter_path(pid, stem)
    if not path.is_file():
        return jsonify(error="章节不存在"), 404
    path.unlink()
    cx_docs.cmd_sync(type("NS", (), {})())
    return jsonify(ok=True)


@app.post("/api/upload-image")
def api_upload_image():
    pid = request.form.get("product", "")
    if not safe_product_id(pid):
        return jsonify(error="非法产品 ID"), 400
    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify(error="未选择文件"), 400
    name = Path(f.filename).name
    if not re.match(r"^[\w.\-]+\.(png|jpg|jpeg|gif|webp|svg)$", name, re.I):
        return jsonify(error="仅支持 png/jpg/jpeg/gif/webp/svg"), 400
    dest_dir = PRODUCTS / pid / "assets" / "images"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / name
    f.save(dest)
    rel = f"assets/images/{name}"
    snippet = f"![{name}]({rel})"
    return jsonify(ok=True, path=rel, markdown=snippet)


@app.post("/api/sync")
def api_sync():
    cx_docs.cmd_sync(type("NS", (), {})())
    return jsonify(ok=True, message="目录已同步")


@app.post("/api/save")
def api_save():
    """客户端应先 PUT 当前文档；此处 sync + git add + commit"""
    data = request.get_json(force=True) or {}
    msg = data.get("message") or f"编辑器保存 {datetime.now():%Y-%m-%d %H:%M:%S}"
    cx_docs.cmd_sync(type("NS", (), {})())
    code, out = run_git(["add", "-A"])
    if code != 0:
        return jsonify(ok=False, step="git add", detail=out), 500
    code, out = run_git(["commit", "-m", msg])
    if code != 0:
        if "nothing to commit" in out.lower():
            return jsonify(ok=True, message="没有新的改动需要提交", detail=out)
        return jsonify(ok=False, step="git commit", detail=out), 500
    return jsonify(ok=True, message="已保存到本地 Git", detail=out)


@app.post("/api/publish")
def api_publish():
    code, out = run_git(["push", "origin", "main"])
    if code != 0:
        return jsonify(ok=False, step="git push", detail=out), 500
    return jsonify(
        ok=True,
        message="已推送到 GitHub，约 1～2 分钟后网站会更新",
        site="https://zhentao-lin.github.io/CX_Product_Tutorials/",
        detail=out,
    )


@app.get("/api/status")
def api_status():
    code, branch = run_git(["branch", "--show-current"])
    code2, status = run_git(["status", "--short"])
    return jsonify(
        branch=branch if code == 0 else "?",
        status=status if code2 == 0 else "",
        repo=str(ROOT),
    )


def main():
    import webbrowser
    from threading import Timer

    port = 8765
    url = f"http://127.0.0.1:{port}/"
    Timer(1.2, lambda: webbrowser.open(url)).start()
    print(f"教程编辑器: {url}")
    print("关闭本窗口即可退出编辑器。")
    app.run(host="127.0.0.1", port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()