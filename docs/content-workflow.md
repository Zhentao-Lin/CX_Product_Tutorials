# 日常更新流程（MD 优先）

## 推荐：只 push，不本地编译

1. 编辑章节 Markdown：`docs/source/products/<产品ID>/NN-xxx.md`
2. `git add` / `git commit` / `git push origin main`
3. GitHub Actions 执行 `python tools/cx_docs.py sync` 后构建 Pages，站点自动更新。

章节 **不用** 写进 `catalog/products.yml`；工具会扫描该产品目录下全部 `*.md`，按文件名排序。

## 改已有章节

只改 `.md` 正文即可；标题改了请同步修改文首 `# 一级标题`（会出现在侧栏与大纲）。

## 新增章节

**方式 A（最简单）**

1. 在对应产品目录新建 `03-wifi.md`：

   ```markdown
   # Wi-Fi 配网

   正文...
   ```

2. push；或本地先 `python tools/cx_docs.py sync` 看一眼目录。

**方式 B（脚手架）**

```powershell
python tools/cx_docs.py new-chapter --product CX_ESP32_S31_Module_Xiaozhi_Board --file 03-wifi --title "Wi-Fi 配网"
```

## 新增产品

**方式 A**

1. 在 `catalog/products.yml` 增加一段（参考现有项）。
2. 创建目录 `docs/source/products/<产品ID>/`，放入 `01-overview.md` 等。
3. push 或 `python tools/cx_docs.py sync`。

**方式 B**

```powershell
python tools/cx_docs.py new-product --id CX_New_Board --title "新板子" --chapter 01-overview
```

## 自动生成的文件

- `docs/source/index.rst`
- `docs/source/products/<ID>/index.rst`

文件头注明「请勿手改」。需要调整大纲文案时，改 `catalog/products.yml` 里的 `summary` / `title`，再 `sync`。

## 本地预览（可选）

```powershell
.\build.bat
# 或
python tools/cx_docs.py serve
```