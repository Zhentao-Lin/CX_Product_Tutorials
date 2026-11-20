# CX_Product_Tutorials

> **新手请先看：** [新手入门-手把手教程.md](新手入门-手把手教程.md)  
> **想点点鼠标就改教程：** 双击 [`start-editor.bat`](start-editor.bat) → [教程编辑器使用说明.md](教程编辑器使用说明.md)  
> **教程网址：** https://zhentao-lin.github.io/CX_Product_Tutorials/

Sphinx + **Read the Docs 主题**，浏览界面接近 [Freenove 在线教程](https://docs.freenove.com/en/latest/)。

## 你每天只需关心什么？

| 你做什么 | 不需要做什么 |
|----------|----------------|
| 在 `docs/source/products/<产品ID>/` 下 **写/改 `.md`** | 手改 `index.rst`（自动生成） |
| 新产品：改 `catalog/products.yml` 或跑 `new-product` | 自己拼 toctree |
| 新章节：新建 `03-xxx.md`，**第一行 `# 标题`** | 在 yml 里逐章登记 |
| 可选本地预览：`.\build.bat` 或 `build` | 本地不必构建也能发布（见下） |

**最省事工作流：只改 Markdown → `git push`**。GitHub Actions 会先 `sync` 再构建站点，**不必在本机编译**。

## 自动更新网站

| 部署 | 触发 |
|------|------|
| **GitHub Pages** | push `main` → Actions：`sync` + `sphinx-build` + 部署 |
| **Read the Docs**（可选，与 Freenove 同托管） | 关联仓库后 push 自动构建（`.readthedocs.yaml` 含 `pre_build: sync`） |

## 命令行工具 `tools/cx_docs.py`

```powershell
# 根据 catalog + 各目录 *.md 生成 index.rst（CI 会自动跑）
python tools/cx_docs.py sync

# 登记新产品 + 建目录
python tools/cx_docs.py new-product --id CX_ESP32_S31_Module_Xiaozhi_Board --title "ESP32-S3 小智板（模组）"

# 新产品时顺带首章
python tools/cx_docs.py new-product --id CX_Demo --title "演示板" --chapter 01-overview --chapter-title "概述"

# 新产品下加一章
python tools/cx_docs.py new-chapter --product CX_ESP32_S31_Module_Xiaozhi_Board --file 03-wifi --title "Wi-Fi 配网"

# 本地：同步 + 编译（可加 --open 打开浏览器）
python tools/cx_docs.py build
.\build.bat

# 边改 MD 边刷新浏览器
python tools/cx_docs.py serve
```

章节规则：文件名 `NN-英文名.md`，按名字排序进左侧目录；标题取自 MD **首个 `# 标题`**。新建章节时工具会自动加文末「返回大纲」链接。

## 目录结构

```text
catalog/products.yml          # 仅产品元数据（id / title / summary / status）
docs/source/
  _static/images|downloads/   # 全站图片与附件
  index.rst                   # [自动生成] 总产品大纲
  products/<产品ID>/
    index.rst                 # [自动生成] 产品大纲
    01-xxx.md                 # [你编写] 章节正文
    assets/                   # 本产品图片、ZIP、源码文件等
      images/
      attachments/
      code/
      data/
tools/cx_docs.py
build.ps1 / build.bat
```

**图片、表格、代码、下载附件**怎么放、怎么写在 MD 里：见 [docs/assets-guide.md](docs/assets-guide.md)。

## 本地环境（可选）

```powershell
cd docs
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..
python tools/cx_docs.py build --open
```

输出：`docs/_build/html/index.html`

## 更省事的做法（推荐）

1. 装好 Python 3.10+。
2. 写文章时只动 `catalog/products.yml`（新产品）和 `*.md`（章节）。
3. **直接 push GitHub**，等 1～2 分钟 Pages 更新。
4. 需要看版式时再运行 `build`。

详情：[docs/content-workflow.md](docs/content-workflow.md)、[docs/github-pages.md](docs/github-pages.md)。