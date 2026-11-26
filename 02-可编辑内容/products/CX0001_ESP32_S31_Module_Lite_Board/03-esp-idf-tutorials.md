# 第 3 章：ESP-IDF 教程外链（00～09）

本章为 **CX0001 硬件仓** 教程的镜像目录：正文在硬件仓维护，此处链到 **网页版（Pages）** 与 **GitHub 源文件 / 工程**，避免双份拷贝不同步。

**统一入口：** [教程 HTML 目录](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/index.html)

环境要求：**ESP-IDF v6.1.1**、`esp32s31`、`idf.py --preview`。

## 章节目录

| 章 | 主题 | 网页（排版版） | Markdown 源 | 示例工程 |
|:--:|------|----------------|-------------|----------|
| 00 | 开发环境 | [00_开发环境.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/00_开发环境.html) | [00_开发环境.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/00_%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83.md) | — |
| 01 | GPIO / 板载 LED | [01_GPIO_LED.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/01_GPIO_LED.html) | [01_GPIO_LED.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/01_GPIO_LED.md) | [01_GPIO_LED](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/01_GPIO_LED) |
| 02 | GPIO / BOOT 键 | [02_GPIO_BUTTON.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/02_GPIO_BUTTON.html) | [02_GPIO_BUTTON.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/02_GPIO_BUTTON.md) | [02_GPIO_BUTTON](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/02_GPIO_BUTTON) |
| 03 | WS2812 | [03_WS2812.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/03_WS2812.html) | [03_WS2812.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/03_WS2812.md) | [03_WS2812](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/03_WS2812) |
| 04 | USB 串口控制台 | [04_USB_SERIAL.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/04_USB_SERIAL.html) | [04_USB_SERIAL.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/04_USB_SERIAL.md) | [04_USB_SERIAL](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/04_USB_SERIAL) |
| 05 | USB 虚拟 U 盘 | [05_USB_MSC.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/05_USB_MSC.html) | [05_USB_MSC.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/05_USB_MSC.md) | [05_USB_MSC](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/05_USB_MSC) |
| 06 | BLE NUS 透传 | [06_BLE_UART.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/06_BLE_UART.html) | [06_BLE_UART.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/06_BLE_UART.md) | [06_BLE_UART](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/06_BLE_UART) |
| 07 | BLE 控灯 | [07_BLE_LED.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/07_BLE_LED.html) | [07_BLE_LED.md](https://zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/07_BLE_LED.md) | [07_BLE_LED](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/07_BLE_LED) |
| 08 | Wi-Fi Socket | [08_WIFI_SOCKET.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/08_WIFI_SOCKET.html) | [08_WIFI_SOCKET.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/08_WIFI_SOCKET.md) | [08_WIFI_SOCKET](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/08_WIFI_SOCKET) |
| 09 | 网页控 WS2812 | [09_WEB_WS2812.html](https://zhentao-lin.github.io/CX0001_ESP32_S31_Module_Lite_Board/09_WEB_WS2812.html) | [09_WEB_WS2812.md](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/04.%E6%95%99%E7%A8%8B/09_WEB_WS2812.md) | [09_WEB_WS2812](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/tree/main/03.Sketch/09_WEB_WS2812) |

## 示例：配置、编译第 1 章工程

各 Sketch 已带 `sdkconfig.defaults`（`esp32s31`、16MB Flash/PSRAM、自定义分区、USB-Serial-JTAG 控制台等）。**首次**打开工程或 `fullclean` 后需 `set-target`；要改引脚/间隔或 Wi-Fi 等再进 `menuconfig`。

**VS Code（Espressif IDF 扩展）：** 打开工程文件夹 → 选 **Set Espressif device target** → `esp32s31` → **SDK Configuration editor (menuconfig)** → Build → Flash。

**命令行：**

```powershell
cd <硬件仓路径>\03.Sketch\01_GPIO_LED

# 首次 / 换芯片 / 删过 build 后必做：写入目标并合并 sdkconfig.defaults
idf.py --preview set-target esp32s31

# 可选：图形配置（01 章在 Example Configuration 改 LED GPIO、闪烁间隔）
idf.py --preview menuconfig

idf.py --preview build
idf.py --preview -p <COM口> flash monitor
```

| 章节 | menuconfig 常用项 |
|------|-------------------|
| 01～07 | **Example Configuration**（若有）：引脚、间隔等 |
| 08、09 | **Example Configuration**：`Wi-Fi SSID` / `Password`（或先改 `sdkconfig.defaults` 再 `set-target`） |

若 `set-target` 后选项不对，可 `idf.py --preview fullclean` 后重做 `set-target` → `build`。

## 维护说明（给你自己）

- **改教程正文**：只改硬件仓 `04.教程/*.md`，运行 `python 04.教程/build_html.py` 后 push 硬件仓。
- **改本站导读**：只改本目录 `01-overview.md` 等；无需复制硬件仓全文。
- 若需把硬件仓链接写进根 README，可同时改 [硬件仓 README](https://github.com/Zhentao-Lin/CX0001_ESP32_S31_Module_Lite_Board/blob/main/README.md) 指向 [CX 产品教程站](https://zhentao-lin.github.io/CX_Product_Tutorials/)。

---



[← 返回本产品教程大纲](index.md) · [↑ 返回总产品大纲](../../index.md)
