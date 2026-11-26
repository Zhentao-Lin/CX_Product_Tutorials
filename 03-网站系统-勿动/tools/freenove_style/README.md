# Freenove 风格教程工具（CX 仓库内）

依据 [`01-使用说明/05-文风与版式.md`](../../01-使用说明/05-文风与版式.md)。

将章节 **Markdown** 转为 Freenove 橙系 **单页 HTML**（不替代 Sphinx 站点）。

## 推荐入口（仓库根目录）

```powershell
cd E:\GitHub\CX_Product_Tutorials

python "03-网站系统-勿动/tools/cx_docs.py" preview-html --md 02-可编辑内容/products/CX_ESP32_S31_Module_Xiaozhi_Board/01-overview.md --open

python "03-网站系统-勿动/tools/cx_docs.py" check-md --md 02-可编辑内容/products/CX_ESP32_S31_Module_Xiaozhi_Board/01-overview.md
```

## 直接调用

```powershell
cd tools\freenove_style
python build.py ..\..\02-可编辑内容\products\...\01-overview.md --inline-css
python new_tutorial.py Demo -o ..\..\02-可编辑内容\products\Demo\00-full.md --chapters 2
```

| 脚本 | 作用 |
|------|------|
| `build.py` | 校验 md → 转 html → 校验 html |
| `md_to_html.py` | 转换 |
| `check_md.py` / `check_html.py` | 检查 |
| `new_tutorial.py` | 整本教程骨架（多章） |
| `assets/freenove-tutorial.css` | 样式 |

## AI 约定

写/润色教程：先改 `02-可编辑内容/products/**/*.md`，再跑 `cx_docs.py preview-html`；站点发布仍 `git push` → Sphinx。
