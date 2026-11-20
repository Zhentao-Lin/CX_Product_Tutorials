# 图片、表格、代码与附件

章节正文仍是 **Markdown**；资源文件按目录存放，章节里用相对路径引用即可。推送 GitHub 后随站点一起发布。

## 目录规范

```text
docs/source/
  _static/                          # 全站共用（Logo、站点级示意图）
    images/
    downloads/                      # 全站可下载附件（PDF/ZIP…）

  products/<产品ID>/
    01-xxx.md                         # 章节（仅产品根下的 .md）
    assets/                           # 本产品专用资源（不要放章节 .md）
      images/                         # 照片、截图、原理图（png/jpg/svg/webp）
      attachments/                    # 固件包、PDF 手册、ZIP 工程
      code/                           # 较长源码文件（章节内用链接引用）
      data/                           # CSV 等大表格源文件（可选）
```

**原则**

| 类型 | 放哪里 | 章节里怎么写 |
|------|--------|----------------|
| 图片 | `assets/images/` | `![说明](assets/images/xxx.png)` |
| 表格 | 直接写在 `.md` 里 | Markdown 表格语法 |
| 短代码 | 直接写在 `.md` 里 | ` ```c ` 围栏代码块 |
| 长代码 | `assets/code/` | 链接 + 可选摘录 |
| 下载附件 | `assets/attachments/` 或 `_static/downloads/` | `[下载说明](assets/attachments/xx.zip)` |
| 全站图/附件 | `_static/images/`、`_static/downloads/` | 路径以 `../../_static/...` 从章节引用 |

从 `products/<ID>/某章.md` 引用本产品图片：`assets/images/xxx.png`（不要写绝对盘符路径）。

## 图片

```markdown
![模组版正视图](assets/images/board-front.png)
```

建议：PNG/WebP 用于截图，SVG 用于框图；单张尽量 &lt; 2MB，大图可先压缩。

## 表格（写在 MD 内）

```markdown
| 参数 | 数值 |
|------|------|
| 主控 | ESP32-S3 |
| 闪存 | 16MB |
```

复杂表格可先 Excel 整理，再贴进 MD 或把 CSV 放 `assets/data/` 并附下载链接。

## 代码

````markdown
```c
void setup() {
    Serial.begin(115200);
}
```
````

线上章节代码块旁有 **复制按钮**（`sphinx-copybutton`）。

整文件过长时，将源文件放进 `assets/code/`，章节中写：

```markdown
完整示例见 [hello_uart.ino](assets/code/hello_uart.ino)（可点击下载/查看）。
```

## 附件（ZIP / PDF / BIN）

```markdown
- [出厂固件 v1.0](assets/attachments/firmware_v1.0.bin)
- [示例工程包](assets/attachments/demo_project.zip)
```

二进制文件请用 **Git LFS** 或控制体积（单文件 &lt; 50MB）；超大文件可放网盘，MD 里写外链。

## 禁止与注意

- 不要在 `assets/` 下放会被当成「新章节」的 `03-xxx.md`（章节只放在产品根目录）。
- 资源文件名用英文/数字/连字符，避免空格与中文路径。
- 图片/附件随 `git push` 公开（公有仓库）—勿提交密钥、未公开固件。

## 新产品自动建目录

```powershell
python tools/cx_docs.py new-product --id CX_New --title "标题"
```

会自动创建 `assets/images|attachments|code|data`。已有产品可执行：

```powershell
python tools/cx_docs.py sync
```

`sync` 会补齐缺失的 `assets` 子目录。