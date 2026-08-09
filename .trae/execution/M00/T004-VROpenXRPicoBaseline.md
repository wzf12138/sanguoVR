# M00-T004 VR/OpenXR/PICO 基线

- 状态：blocked（2026-08-10 更新：V-005 PICO Neo3 真机验证失败，设备不兼容，待用户决策换设备或降级引擎）
- 优先级：P0
- 目标：补齐 Android SDK/NDK，配置 UE Android 构建环境，通过 Launch on Device 和 Standalone APK 两种方式在 PICO Neo3 真机上验证 VR 模板运行。

## 完整流程（7 个 Phase）

### Phase 1 — 安装 Android SDK
用户通过 sdkmanager 安装 android-34/35、NDK r27c、build-tools 35.0.1。

### Phase 2 — UE Android 路径配置
用户在 UE 编辑器 Project Settings → Android 中配置 SDK/NDK 路径，Accept License。

### Phase 3 — AI 核验
执行模型检查 SDK 组件存在性、VR 模板资产完整性、OpenXR/PICO 插件加载状态。结果写入 V-004。

### Phase 4 — PICO 开发者模式
用户在 PICO Neo3 上开启开发者模式 + USB 调试，`adb devices` 确认识别。

### Phase 5 — Launch on Device
UE 编辑器通过 adb 直连部署到 PICO。验证 VR 画面渲染、头显追踪、手柄追踪。

### Phase 6 — Standalone APK
构建独立 APK，adb 安装，断开 USB 后冷启动。验证 6DoF、双控制器、断网运行、退出重启。

### Phase 7 — AI 结果记录
V-005 登记真机验证结果，同步三份知识文档（PicoNeo3BuildGuide / EnvironmentSetup / TechnicalDecisions）。

## 验收

不得用配置存在替代运行验证，不得用 PC VR 替代 PICO Neo3 真机结论。两种部署方式都必须通过。
