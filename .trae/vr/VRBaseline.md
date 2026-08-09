# VR 基线

## 目标

- 引擎：UE 5.8。
- 运行时：OpenXR 主路径。
- 一期设备：PICO Neo3，Android 离线运行。
- 工程保留官方 VR 模板的 Pawn、手部、抓取、瞬移和输入资产，不以空骨架替换成熟模板能力。

## 工程要求

- `.uproject` 启用 OpenXR、OpenXREyeTracker、OpenXRHandTracking、PICOController，并声明 Android。
- 相机与追踪原点、玩家胶囊、虚拟身体和物理交互具有明确空间所有权。
- 帧率、输入延迟和追踪丢失必须可观测；设备验证结果写入登记册。

## 验证层级

1. 文件：插件、平台和配置存在。
2. 编辑器：VR Preview 或等效 OpenXR 环境可启动。
3. 构建：Android 包可生成、安装和启动。
4. 真机：输入、追踪、移动、交互、暂停恢复和断网运行通过。
