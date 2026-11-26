"""Windows-safe build launcher: avoid Chinese path literals in .bat."""
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
    cx = system / "tools" / "cx_docs.py"
    if not cx.is_file():
        raise SystemExit(f"缺少工具: {cx}")
    return subprocess.call(
        [sys.executable, str(cx), "build", *sys.argv[1:]],
        cwd=str(ROOT),
    )


if __name__ == "__main__":
    raise SystemExit(main())
