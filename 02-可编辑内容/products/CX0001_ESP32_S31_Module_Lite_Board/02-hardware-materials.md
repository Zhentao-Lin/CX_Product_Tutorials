# 第 2 章：硬件资料索引

原理图、PCB、数据手册与板照均在硬件仓对应目录；此处仅做**公开链接索引**（与硬件仓保持同步）。

## 资料目录（GitHub）

| 类型 | 硬件仓路径 | 打开 |
|------|------------|------|
| 原理图 PDF | `01.原理图/` | [浏览目录](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/01.%E5%8E%9F%E7%90%86%E5%9B%BE) |
| PCB | `02.PCB/` | [浏览目录](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/02.PCB) |
| 芯片 / 模组手册 | `05.Datasheet/` | [浏览目录](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/05.Datasheet) |
| 板照与引脚图 | `06.Picture/` | [浏览目录](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/06.Picture) |

引脚图直链：[Pinout_CX0001.png](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/06.Picture/Pinout_CX0001.png)

## 示例固件工程

九个 ESP-IDF 工程位于硬件仓 `03.Sketch/`（01_GPIO_LED … 09_WEB_WS2812）：

[打开 03.Sketch 根目录](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch)

## Step：下载资料到本地

1. 克隆或 Download ZIP：[硬件仓库](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board)。
2. 用 PDF 阅读器打开 `01.原理图` 下 SCH；需要 PCB 时打开 `02.PCB`。
3. 写程序时以 `06.Picture/Pinout_CX0001.png` 与教程中的 GPIO 表对照接线。

继续学习：[ESP-IDF 教程外链（00～09）](03-esp-idf-tutorials.md)。

---



[← 返回本产品教程大纲](index.md) · [↑ 返回总产品大纲](../../index.md)
