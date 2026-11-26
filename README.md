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

### 3. 私有仓外链（硬件 / 代码只有你能进）

本教程仓是**公开**的；完整硬件工程、固件源码放在**私有** GitHub 仓库，章节里只写链接。  
**你登录后能打开；路人点开没权限。**

#### 3.1 怎么新建私有仓库（GitHub 网页）

1. 打开 https://github.com/new（需已登录）。
2. **Repository name**：起名，例如 `CX_ESP32_S31_Module_Hardware`、`CX_ESP32_S31_Module_Firmware`。
3. 选 **Private**（私有），不要选 Public。
4. 可选勾选 `Add a README`，点 **Create repository**。
5. 创建后浏览器地址栏就是仓库地址，例如：  
   `https://github.com/Zhentao-Lin/CX_ESP32_S31_Module_Hardware`  
   **复制这个地址**备用。

把原理图/PCB/源码用 Git 推到这个私有仓（或网页 Upload files），不要推到本公开教程仓。

#### 3.2 怎么把链接加进本教程

1. 打开对应产品章节，例如：  
   `02-可编辑内容/products/CX_ESP32_S31_Module_Xiaozhi_Board/01-overview.md`  
   （或用 `start-editor.bat` 打开同一章。）
2. 在文中合适位置粘贴下面模板，**只改括号里的网址**：

```markdown
## 相关仓库（内部）

| 内容 | 说明 |
|------|------|
| 硬件设计 | [私有 · PCB/原理图工程](https://github.com/Zhentao-Lin/你的私有硬件仓) |
| 固件源码 | [私有 · 固件仓库](https://github.com/Zhentao-Lin/你的私有固件仓) |

> 以上仓库为私有：仅维护者可见；公开读者无需访问也可按本教程操作。
```

单行也可以：

```markdown
内部硬件仓：https://github.com/Zhentao-Lin/你的私有硬件仓  
内部固件仓：https://github.com/Zhentao-Lin/你的私有固件仓
```

3. **保存**文件（编辑器里点「保存」，或 Cursor 里 `Ctrl+S`）。
4. **发布**：编辑器点「发布到网站」，或终端：

```powershell
cd E:\GitHub\CX_Product_Tutorials
git add -A
git commit -m "添加私有仓链接"
git push origin main
```

约 1～2 分钟后，公开教程页上会出现链接；你点能进私有仓，别人不能。

#### 3.3 注意

1. 私有仓文件**不要**再复制进本公开仓 `assets/`（否则就公开了）。
2. 公开 MD 里**不要**写 Token、密码、带密钥的下载地址。
3. 链接 URL 别人能看见，只是进不去；保密靠私有仓权限。
4. 若希望**读者也能下**某份资料：放本仓 `assets/hardware/`，或另建**公开**仓再链过来。

### 4. 其它常用目录（同一产品下）

| 路径 | 用途 |
|------|------|
| `assets/attachments/` | 固件包、其它 ZIP/PDF（放这里即公开） |
| `assets/code/` | 本仓偶尔放的短示例文件（公开） |
| `assets/data/` | CSV 等数据（公开） |

更细的写法见：`01-使用说明/03-图片与附件.md`。

> 若双击 bat 报找不到中文路径：已用 `_launch_*.py` 自动定位 `01-`/`02-`/`03-` 文件夹，请再试一次 `start-editor.bat`。
