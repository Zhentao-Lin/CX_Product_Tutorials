"""Windows-safe launcher: avoid Chinese path literals in .bat (cmd GBK mangling)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def find_dir(prefix: str) -> Path:
    matches = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith(prefix))
    if not matches:
        raise SystemExit(f"找不到以 {prefix} 开头的文件夹（仓库根目录: {ROOT}）")
    return matches[0]


def main() -> int:
    system = find_dir("03-")
    req = system / "requirements-editor.txt"
    app = system / "tools" / "tutorial_editor" / "app.py"
    if not req.is_file():
        raise SystemExit(f"缺少依赖文件: {req}")
    if not app.is_file():
        raise SystemExit(f"缺少编辑器: {app}")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
        cwd=str(ROOT),
    )
    return subprocess.call([sys.executable, str(app)], cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
