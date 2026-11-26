# 02-可编辑内容（你平时只动这里）

| 编号 | 路径 | 用途 |
|------|------|------|
| 1 | `catalog/products.yml` | 产品名单（上新板子时改） |
| 2 | `catalog/home.md` | 网站首页说明文字 |
| 3 | `products/<产品ID>/01-xxx.md` 等 | **章节正文**（最常改） |
| 4 | `products/<产品ID>/assets/images/` | 教程配图 |
| 5 | `products/<产品ID>/assets/hardware/` | 原理图 / PCB / 3D / BOM |
| 6 | `products/<产品ID>/assets/attachments/` | 固件包、其它 zip / pdf |
| 7 | `products/<产品ID>/assets/code/` | 本仓短示例（可选） |
| 8 | `products/<产品ID>/assets/data/` | csv 等（可选） |

开源硬件与写教程的放法说明见仓库根目录 [README.md](../README.md)。

## 不要改

- 各产品目录下自动生成的 `index.md`（运行 sync / 推送后会再生）
- 不要把章节 `.md` 放进 `assets/` 里

改完后：`git add` → `commit` → `push`，或用编辑器点「发布」。
