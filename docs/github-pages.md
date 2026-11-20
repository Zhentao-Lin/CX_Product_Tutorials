# 发布与自动更新

## 目标

- **浏览界面**：`sphinx-rtd-theme`（与 [Freenove 文档站](https://docs.freenove.com/en/latest/) 同类主题）
- **自动更新**：每次 push GitHub `main` → 站点自动重建

## 方案 A：GitHub Pages（推荐先启用）

1. 推送仓库 `CX-PRODUCT-TUTORIALS` 到 GitHub。
2. **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**。
3. 之后每次 push `main`，workflow `.github/workflows/pages.yml` 会 `sphinx-build` 并部署。
4. 访问：`https://<用户名>.github.io/CX-PRODUCT-TUTORIALS/`

## 方案 B：Read the Docs（与 Freenove 相同托管方式）

1. 登录 [readthedocs.org](https://readthedocs.org)，**Import a Project**，选 GitHub 上的 `CX-PRODUCT-TUTORIALS`。
2. 仓库根目录已有 `.readthedocs.yaml`，无需改构建命令。
3. 每次 push，RTD webhook 自动构建；默认域名形如 `https://cx-product-tutorials.readthedocs.io/`。
4. 可在 RTD 后台绑定自定义域名。

**A 与 B 可同时开启**：改 docs 一次，两处都会更新（各自独立触发）。

## 本地预览

```powershell
cd docs
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
make html
# 打开 _build/html/index.html
```

## 费用

公有仓库 + GitHub Pages + Read the Docs 开源项目：**0 元**。