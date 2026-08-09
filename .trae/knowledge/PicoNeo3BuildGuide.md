# PICO Neo3 构建指南

## UE5.8 Android 工具链官方要求

| 组件 | 版本要求 | 状态 |
|------|---------|------|
| SDK 目标平台 | 推荐 android-35，最低 android-34 | 待安装 |
| NDK | r27c（27.2.12479018） | 待安装 |
| Build-tools | 35.0.1 | 待检查 |
| JDK | OpenJDK 21.0.3+ | OpenJDK 21.0.10 已安装 ✅ |
| Android Studio | Koala 2024.1.2 Patch 1 | 非必须 |
| 设备要求 | Android 8+，64-bit ARM，兼容 GPU（Adreno/Mali） | PICO Neo3 待确认 |

## 两种 PICO 部署方式

### 方式 A：Launch on Device（编辑器直连）
- UE 编辑器通过 adb 直接部署到 USB 连接的 PICO
- 适合快速迭代，不产生独立 APK
- 命令：`RunUAT.bat BuildCookRun -platform=Android -cook -stage -deploy -run`
- 前提：adb devices 能识别 PICO

### 方式 B：Standalone APK（独立打包）
- 构建独立 APK 文件，adb 安装后可断开 USB
- 验证离线运行能力（GameMasterPlan 要求）
- 命令：`RunUAT.bat BuildCookRun -platform=Android -configuration=Development -build -cook -stage -pak -archive`

## 目标

在 PICO Neo3 普通版上运行 UE5.8 项目，验证 OpenXR、头显追踪、双手柄输入、瞬移和抓取。

## 当前策略

- 第一阶段优先使用 UE5.8 内置 OpenXR
- 第一里程碑前不安装 PICO 外部插件
- 真机测试发现输入映射、刷新率或设备扩展能力缺失时，再评估与 UE5.8 兼容的 PICO 官方方案

## 验证项目状态

- 未验证：设备开发者模式
- 未验证：USB 调试授权
- 未验证：ADB 设备识别
- 未验证：Android SDK android-34/35
- 未验证：Android NDK r27c
- 未验证：Build-tools 35.0.1
- 未验证：方式 A Launch on Device（编辑器直连部署）
- 未验证：方式 B Standalone APK 构建与安装
- 未验证：OpenXR Runtime 正常
- 未验证：6DoF 头显追踪
- 未验证：左右手柄映射正常
- 未验证：震动反馈正常
- 未验证：断网冷启动
- 未验证：目标帧率稳定性

## 测试记录

尚未开始真机验证。后续每次测试记录日期、引擎配置、设备系统版本、结果和错误日志摘要。
