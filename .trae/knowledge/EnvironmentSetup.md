# 开发环境

## 当前状态

- 2026-09-04：**本机 Python 解释器实况**——PATH 中 `python`/`python3` 均指向 Trae 内置解释器 `C:\Users\PC\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe`（3.10.11，已含 pyyaml 6.0.3），治理脚本（`dashboard/check-integrity.py`、`generate-static.py`）直接用 `python` 运行即可；无独立 `py` 启动器、无 `D:\Python`。如未来安装独立解释器，按磁盘规则放 `C:`。
- 2026-09-04：**引擎版本勘误**——项目现用 UE 5.6（5.6.1），README 已同步修正。本文下方 2026-08-09 前后的 "UE5.8" 章节为 M00 期历史记录（当时的探索结论，含"PICO Neo3 与 UE5.8 不兼容"），按原貌保留供审计，不反映当前工具链。
- UE5.8 已安装，且安装中包含官方 VR 模板。
- Visual Studio 2019 已由用户手动卸载；原安装目录只剩少量无效残留。
- Visual Studio Community 2026 Insiders 已安装，不再执行安装 VS2022 的旧计划。
- PICO Neo3 普通版为一期真机目标。
- 2026-08-08：已确认 VS2026 位于 `D:\AWork\Visual_Studio_2026\vs2026`，包含 MSVC 14.51.36231、Windows SDK 和 Unreal 专属组件。
- vswhere 暂未识别 VS2026 实例，可能需要系统重启使注册信息落盘。
- UE4.27 残留位于项目工作目录之外，不属于本项目目录整理范围。

## 2026-08-09 M00-T003 工具链检查结果

- UE5.8 安装路径：`D:\AWork\Unreal\App\UE_5.8`（注册表 `HKLM:\SOFTWARE\EpicGames\Unreal Engine\5.8` 确认）；`RunUAT.bat`、`Build.bat`、`UnrealBuildTool.dll` 均存在。
- Visual Studio：`D:\AWork\Visual_Studio_2026\vs2026`，MSVC 工具集版本 14.51.36231（另有 14.50.35717），`vcvars64.bat` 存在；**UBT 实际选用 MSVC 14.50.35717（VS 14.50.35737）与 Windows SDK 10.0.22621.0**，即 UE5.8 选择稳定工具集而非 14.51/10.0.26100 预览组合。
- vswhere 状态：`Setup\Instances` 注册表（HKLM 64 位视图与 WOW6432Node）手工注册 VS2026 实例键后，vswhere 3.1.7 仍返回空列表——vswhere 走 VS Setup Configuration 接口，不识别手工键，属 VS2026 非安装器注册的固有表现。**对构建无影响**（UBT 独立探测 MSVC，编译已成功）；仅影响编辑器内"打开 IDE/Live Coding 联动"等辅助功能。正解为 VS 安装器修复/重装，属系统级操作，不在任务范围。注册键已保留，无害。
- Windows SDK：`10.0.26100.0`（另有 10.0.22621.0），位于 `C:\Program Files (x86)\Windows Kits\10`；UBT 实际使用 `10.0.22621.0`。
- `.uproject` 核对：OpenXR、PICOController（Win64/Linux/Android）、OpenXREyeTracker、OpenXRHandTracking、ModelContextProtocol、AllToolsets 六个插件均启用，TargetPlatforms 含 Android。
- MCP 连接器：`list_toolsets` 调用成功，返回约 40 个工具集；编辑器日志类别可枚举，`LogLoad` 无错误，`LogTemp` 仅引擎自带 UnifiedErrorTest 测试条目。
- **清理编译（2026-08-09）：成功**。`Rebuild.bat VRSanguoYanWuchangEditor Win64 Development`，`Result: Succeeded`，总耗时 33.35 秒（UBA 本地执行器 30.29 秒，10 个动作）；源码含 `VRSanguoYanWuchang.cpp`、`VRSanguoBootstrapActor.cpp`（原 `VRSanguoBootstrapComponent.cpp`，2026-08-10 按 UE 命名规范更名），输出二进制 `D:\AWork\Unreal\App\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe`。
- 生成项目文件：UE5.8 的 `Engine\Build\BatchFiles\` 已无 `GenerateProjectFiles.bat`，UBT 构建时自动生成 makefile（"Creating makefile"），无需单独执行。
- Android SDK/NDK/JDK 版本及路径：未验证（UBT 无法运行识别，保持待验证）。
- PICO Neo3 系统版本和连接结果：未验证（本任务不含真机）。

## 2026-08-09 M00-T004 Android 环境检查

- Android SDK 根目录 `D:\AWork\Android_SDK\SDK`：含 `platforms`（android-30/32/33/34/**35**）、`build-tools`（29.0.2/30.0.3/**35.0.1**）、`ndk`（21.4.7075529/**27.2.12479018**）、`cmdline-tools/latest`、`platform-tools`（adb）。
- **JDK 现状**：系统与用户 PATH 均无 Java 条目、JAVA_HOME 未设置；机器上原无独立 JDK（仅 Android Studio 2021 自带 JRE 11 与 TRAE 运行时 JRE 21）。
- **已安装 Temurin JDK 21**：`D:\AWork\Android_SDK\jdk-21.0.12+8`（OpenJDK 21.0.12 LTS，含 javac），满足 UE5.8 官方 Java runtime 要求（OpenJDK 21.0.3+）。已由用户在真实 PowerShell 中下载解压并验证。
- **UE5.8 官方要求（Android Development Prerequisites）**：Android Studio Koala 2024.1.2 Patch 1；SDK 推荐 35、最低编译 34、最低安装 26；NDK r27c；Build-tools 35.0.1；Java OpenJDK 21。
- **引擎 `Android_SDK.json` 权威声明**：`platforms: android-34`、`ndk: 27.2.12479018`、`build-tools: 35.0.1`。
- **UAT 行为**：`AndroidPlatform.Automation.cs` 仅读取 `JAVA_HOME`，无 JDK 版本硬检查；打包 Gradle 为 8.7（支持运行于 JDK 8-21）。
- 组件补齐：SDK 组件已由用户经 sdkmanager 真实安装并验证（platforms android-34/35、build-tools 35.0.1、ndk 27.2.12479018）。注意：执行终端为沙箱视图，系统级安装/文件落盘操作须由用户在真实 PowerShell 执行，AI 终端结果仅作参考。
- 历史记录：任务 Step 0 原写 NDK `25.1.8937393`（r25b，UE5.4 旧要求），已按 UE5.8 官方要求修正为 `27.2.12479018`。

## 2026-08-09 M00-T004 Android 构建与真机调试（晚间）

- **APK 构建链路打通**：`BuildCookRun ... -package -archive` BUILD SUCCESSFUL（约 2-6 分钟增量）；APK 产物 `ArchivedBuilds\Android\VRSanguoYanWuchang-arm64.apk`（159.8MB，arm64，minSdk 26，targetSdk 35，数据内置 APK）。
- **Gradle**：发行版 8.7 已由国内镜像下载并预置 `D:\AWork\.gradle\wrapper\dists\gradle-8.7-all\<hash>\gradle-8.7-all.zip`；`GRADLE_USER_HOME=D:\AWork\.gradle` 使其缓存落 D 盘（不占 C 盘）。hash 目录由 wrapper 首次运行创建，zip 放错目录会导致重新联网下载超时。
- **无线 adb**：PICO 已启用（`adb tcpip 5555` + `adb connect 192.168.31.76:5555`），AI 终端可直接调试设备（日志抓取、安装、启动）。
- **PowerShell 执行策略**：TRAE 命令终端调用宿主机 PowerShell，因 ExecutionPolicy=Restricted 曾无法执行任何命令；已设 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 修复。
- **Git（M00-T002）**：用户已完成 Git for Windows + Git LFS 安装、仓库初始化与远程推送（2026-08-09 确认）。
- **真机结论**：PICO Neo3 与 UE5.8 不兼容（设备层硬限制，详见 `PicoNeo3BuildGuide.md` 与 `DeviceConfigurationMatrix.md`、`TechnicalDecisions.md`）；工程配置已达理论正确，对 PICO 4+ 应可直接运行。

## 后续执行顺序

1. ~~系统重启后确认 vswhere 与 UE5.8 能识别 VS2026。~~ ✅ 编译已通过（M00-T003）
2. ~~使用现有工程执行一次清理编译。~~ ✅ 已通过（M00-T003）
3. ~~补齐 Android SDK：android-34/35 平台 + NDK r27c（M00-T004 Step 0）。~~ ✅ 已装并构建成功
4. ~~验证 JDK 21 兼容性~~ ✅ UE5.8 官方要求 OpenJDK 21.0.3+，我们的 21.0.10 完全匹配
5. ~~安装 Git，初始化 Git + Git LFS 并创建基线提交。~~ ✅ 已完成并推送（2026-08-09）
6. 接入新设备（PICO 4+）后：按 `DeviceConfigurationMatrix.md` 恢复高性能配置 → 重新构建 → 真机验证（M00-T004 Step 5）

## 记录要求

- UE5.8 实际使用的 Visual Studio 版本。
- MSVC 工具链版本。
- Windows SDK 版本。
- Android SDK、NDK、JDK 版本及路径。
- UE5.8 编译验证结果。
- PICO Neo3 系统版本和连接结果。
