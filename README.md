# CX_Product_Tutorials

在线教程：https://zhentao-lin.github.io/CX_Product_Tutorials/

打开仓库后，**按文件夹编号看**即可：

| 文件夹 | 你要做什么 |
|--------|------------|
| **[01-使用说明](01-使用说明/)** | 阅读怎么用（从 `01-新手入门.md` 开始） |
| **[02-可编辑内容](02-可编辑内容/)** | **只在这里改教程**（章节、图片、硬件资料、产品名单） |
| **[03-网站系统-勿动](03-网站系统-勿动/)** | 网站引擎；**不要手改** |

## 最快上手

1. 打开 `01-使用说明/01-新手入门.md`
2. 改教程 / 传资料：去 `02-可编辑内容/products/<产品ID>/`
3. 可选：双击根目录 `start-editor.bat` 用网页编辑器
4. `git push` 后约 1～2 分钟网站更新

本地预览（可选）：双击 `build.bat`

## 写电路板教程时，文件放哪

所有内容都在：`02-可编辑内容/products/<产品ID>/`  
（现有产品例如 `CX_ESP32_S31_Module_Xiaozhi_Board`。新产品先改 `02-可编辑内容/catalog/products.yml`，再建同名文件夹。）

### 1. 开源硬件资料（原理图 / PCB / 3D / BOM）

```text
02-可编辑内容/products/<产品ID>/assets/hardware/
├─ schematic/     ← 原理图 PDF、源文件
├─ pcb/           ← PCB 工程或 Gerber ZIP
├─ 3d/            ← STEP / 渲染等
└─ bom/           ← BOM（csv / xlsx / pdf）
```

教程章节里用相对链接，例如：

```markdown
- [原理图](assets/hardware/schematic/schematic.pdf)
- [PCB 资料](assets/hardware/pcb/gerber.zip)
- [3D 模型](assets/hardware/3d/board.step)
- [BOM](assets/hardware/bom/bom.csv)
```

单文件建议 &lt; 50MB；特别大的工程可放网盘或单独硬件仓，教程里写外链。

### 2. 教程正文与配图

```text
02-可编辑内容/products/<产品ID>/
├─ 01-overview.md              ← 第 1 章正文
├─ 02-hardware.md              ← 第 2 章…
├─ 03-xxx.md                   ← 继续加章（两位数字开头）
└─ assets/images/              ← 教程配图（接线、截图、板照）
```

配图写法：

```markdown
![板子正面](assets/images/board-front.png)
```

固件 / 示例**代码仓库**可另建 GitHub 仓，教程里超链接即可，不必整仓塞进本教程仓库。

### 3. 其它常用目录（同一产品下）

| 路径 | 用途 |
|------|------|
| `assets/attachments/` | 固件包、其它 ZIP/PDF |
| `assets/code/` | 本仓偶尔放的短示例文件 |
| `assets/data/` | CSV 等数据（BOM 也可放这里） |

更细的写法见：`01-使用说明/03-图片与附件.md`。

> 若双击 bat 报找不到中文路径：已用 `_launch_*.py` 自动定位 `01-`/`02-`/`03-` 文件夹，请再试一次 `start-editor.bat`。
