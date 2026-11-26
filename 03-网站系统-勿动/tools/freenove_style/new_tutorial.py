# -*- coding: utf-8 -*-
"""
Scaffold a new Freenove tutorial Markdown from template.
Usage:
  python new_tutorial.py MyProduct_Tutorial -o ../MyProduct_Tutorial.md --chapters 3
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "templates" / "tutorial.md.tpl"


def render(product: str, chapters: int) -> str:
    tpl = TEMPLATE.read_text(encoding="utf-8")
    blocks = []
    for n in range(1, chapters + 1):
        blocks.append(
            f"""# Chapter {n} Topic{n}

一句话说明本章做什么。

> **[配图]** 本章关键元件实物

## Project {n}.1 First Project

### Component List

| 名称 | 数量 |
|------|------|
| 主控板 | 1 |
| （元件） | 1 |

### Circuit

| 从 | 到 |
|----|-----|
| （脚） | （脚） |

> **[配图]** 接线图

### Step

1. 断电接线。
2. 上电，选对开发板与端口。
3. 上传代码。
4. 观察现象。

### Code

```c
// TODO
void setup() {{}}
void loop() {{}}
```

### If It Fails

1. （排查项）
"""
        )
    body = "\n---\n\n".join(blocks)
    return (
        tpl.replace("{{PRODUCT}}", product)
        .replace("{{CHAPTERS}}", body)
        .replace("{{N}}", str(chapters))
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="product / file stem")
    ap.add_argument("-o", "--output", help="output md path")
    ap.add_argument("--chapters", type=int, default=1)
    args = ap.parse_args(argv)
    out = Path(args.output) if args.output else Path.cwd() / f"{args.name}.md"
    text = render(args.name, max(1, args.chapters))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"OK: {out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
