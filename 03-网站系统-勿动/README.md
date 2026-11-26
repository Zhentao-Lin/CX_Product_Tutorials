# 03-网站系统-勿动

本目录是网站构建引擎。**请勿手改**，除非你明确在维护 CI / Sphinx。

| 编号 | 路径 | 用途 |
|------|------|------|
| 1 | `sphinx-source/conf.py` | Sphinx 配置 |
| 2 | `sphinx-source/requirements.txt` | 云端构建依赖 |
| 3 | `sphinx-source/_static/` | 全站 CSS / 共用静态资源 |
| 4 | `tools/cx_docs.py` | sync / build（Actions 会跑） |
| 5 | `tools/tutorial_editor/` | 本地编辑器程序 |
| 6 | `tools/freenove_style/` | Freenove 单页预览工具 |
| 7 | `requirements-editor.txt` | 编辑器 Python 依赖 |
| 8 | `_build/` | 本地构建输出（不提交） |

仓库根目录仍保留：

- `.github/workflows/pages.yml` — Pages 发布（勿改）
- `.readthedocs.yaml` — RTD（勿改）
- `build.bat` / `start-editor.bat` — 可双击使用
