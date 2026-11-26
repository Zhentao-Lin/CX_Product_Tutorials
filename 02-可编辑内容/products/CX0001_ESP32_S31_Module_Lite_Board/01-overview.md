# 第 1 章：产品概述

**CX0001** 是基于 **ESP32-S31** 的 Module Lite 精简开发板：片上 Wi-Fi 6、蓝牙 5.4、**USB-Serial-JTAG**（烧录/日志）与 **USB-OTG**（Device 类示例如 MSC）。

## 本章目标

1. 弄清本产品在 CX 教程站中的位置：**详细教程不在本仓库重复维护**。
2. 知道硬件资料、示例工程与分章教程所在的 **GitHub 硬件仓**。
3. 用网页版目录按 00～09 章顺序学习。

## 教程维护方式（引用硬件仓）

| 内容 | 维护仓库 | 在本站的呈现 |
|------|----------|----------------|
| 分章 Markdown / HTML、`03.Sketch` 工程 | [CX0001_ESP32_S31_Module_Lite_Board](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board) | 第 3 章起链到该仓 Pages |
| 本站产品页 | 本仓 `CX_Product_Tutorials` | 概述、资料索引、外链目录 |

**排版版教程（推荐）：**  
[https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/index.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/index.html)

修改教程正文请到硬件仓 `04.教程/*.md`，运行 `build_html.py` 后 push；硬件仓 Actions 会更新 Pages。

## 引脚示意

![CX0001 引脚图](https://raw.githubusercontent.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/main/06.Picture/Pinout_CX0001.png)

## 板上常用 GPIO（示例工程默认）

| 项目 | 值 |
|------|-----|
| 板载 LED | GPIO38（高有效） |
| BOOT 键 | GPIO61（低有效） |
| WS2812 | GPIO39（GRB，板载 1 颗） |
| 烧录 / 日志 | USB-Serial-JTAG |
| USB Device（如 MSC） | USB-OTG（与烧录口不是同一 Type-C） |
| Flash / PSRAM | 16 MB / 16 MB |

目标芯片：`esp32s31`；`idf.py` 需带 **`--preview`**（ESP-IDF v6.1.0）。

## 相关仓库

| 内容 | 链接 |
|------|------|
| 硬件 + 教程 + 示例源码（公开） | [Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board) |
| 在线 HTML 教程 | [GitHub Pages 目录](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/index.html) |

## Step：第一次打开教程

1. 浏览器打开 [网页目录](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/index.html)。
2. 从 **00 · 开发环境** 起按顺序阅读；每章对应硬件仓 `03.Sketch` 下同名工程。
3. 克隆硬件仓到**纯 ASCII 路径**（勿含中文/空格），在 VS Code 用 ESP-IDF 扩展打开对应 Sketch 编译烧录。

下一章：[硬件资料索引](02-hardware-materials.md) · 完整章节目录见 [ESP-IDF 教程外链](03-esp-idf-tutorials.md)。

---



[← 返回本产品教程大纲](index.md) · [↑ 返回总产品大纲](../../index.md)
