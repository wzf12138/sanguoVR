# PICO Neo3 构建指南

> 最后更新：2026-08-09（M00-T004 真机验证完成一轮，结论：UE5.8 与 Neo3 不兼容，配置已达理论正确，对 PICO 4+ 可直接运行）

## UE5.8 Android 工具链官方要求与实测状态

| 组件 | 版本要求 | 实测状态 |
|------|---------|---------|
| SDK 目标平台 | 推荐 android-35，最低编译 android-34，最低安装 26 | ✅ android-34/35 已装（`D:\AWork\Android_SDK\SDK\platforms`） |
| NDK | r27c（27.2.12479018） | ✅ 已装（`D:\AWork\Android_SDK\SDK\ndk\27.2.12479018`） |
| Build-tools | 35.0.1 | ✅ 已装 |
| JDK | OpenJDK 21.0.3+（UE5.8 官方） | ✅ Temurin JDK 21.0.12（`D:\AWork\Android_SDK\jdk-21.0.12+8`） |
| Gradle | 8.7（引擎自带 wrapper） | ✅ 发行版预置本地缓存（见下） |
| 设备要求 | Android 8+，64-bit ARM | ⚠️ PICO Neo3 = Android 10/API 29，但 OpenXR 运行时过老与 UE5.8 不兼容（见下） |

## 构建环境（必读）

### 每次构建前设置的环境变量（PowerShell）

```powershell
$env:GRADLE_USER_HOME = "D:\AWork\.gradle"          # Gradle 发行版与依赖缓存（D 盘，避免占 C 盘）
$env:JAVA_HOME = "D:\AWork\Android_SDK\jdk-21.0.12+8"
$env:ANDROID_HOME = "D:\AWork\Android_SDK\SDK"
$env:NDKROOT = "D:\AWork\Android_SDK\SDK\ndk\27.2.12479018"
$env:ANDROID_NDK_ROOT = "D:\AWork\Android_SDK\SDK\ndk\27.2.12479018"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
```

### 完整打包命令（含 Gradle 打包与归档）

```powershell
& "D:\AWork\Unreal\App\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="D:\AWork\Unreal\Project\VRSanguoYanWuchang\VRSanguoYanWuchang.uproject" -platform=Android -configuration=Development -build -cook -stage -pak -package -archive
```

- 必须带 `-package`（否则只 Stage 不打包 APK，Archive 会报 `obb not found`）。
- 首次打包会下载 Gradle 8.7 与依赖（已预置缓存到 `D:\AWork\.gradle\wrapper\dists\gradle-8.7-all\<hash>\`；若被清空需重新放置 zip 或走国内镜像）。
- 产物：`ArchivedBuilds\Android\VRSanguoYanWuchang-arm64.apk`。
- 编辑器运行中（Live Coding 激活）构建会失败，需先关闭编辑器。

### 已知构建坑（已解决）

| 问题 | 解决 |
|---|---|
| `Sdk: not found. Required version r27c` | 必须同时设置 `NDKROOT`（UBT 不会从 ANDROID_HOME 推导） |
| `obb was not found` | 构建命令加 `-package` |
| Gradle 下载超时（services.gradle.org） | 国内镜像下载 `gradle-8.7-all.zip` 放入 `D:\AWork\.gradle\wrapper\dists\gradle-8.7-all\<hash>\`（hash 目录由 wrapper 首次运行创建；放错目录无效） |
| Gradle 缓存占 C 盘 | `GRADLE_USER_HOME=D:\AWork\.gradle` |

## PICO 官方 UE 插件支持（2026-08-09 官网提炼）

来源：PICO 开发者文档《PICO Unreal SDK 介绍》《快速上手 PICO OpenXR 插件》（developer-cn.picoxr.com）。

### 插件支持矩阵（权威）

| UE 版本 | 支持插件 |
|---|---|
| 4.27 | PICOXR、OnlineSubsystemPico、PicoSpatialAudio |
| 5.5 | PICOXR、OnlineSubsystemPico、PICOEnterprise、PicoSpatialAudio |
| 5.6 | PICOXR、**PICOOpenXR**、**PICOSpatial**、OnlineSubsystemPico、PICOEnterprise、PicoSpatialAudio、IconConfigurator |
| 5.7 | **PICOOpenXR**、**PICOSpatial**、OnlineSubsystemPico、PICOEnterprise、PicoSpatialAudio、IconConfigurator |
| 5.8 | **不在官方矩阵**（PICO 官方插件不支持；仅可走 UE 内置 OpenXR） |

### PICO OpenXR 插件环境要求（官方原文）

- 虚幻引擎：**UE 5.6 或 5.7**
- 图形接口：**Vulkan**
- 操作系统：Windows 和 macOS
- 支持设备：**Project Swan（PICO OS 6）或 PICO Emulator**（新一代设备）
- 安装：Fab（PICO OpenXR 插件）或官网 SDK 下载（`developer-cn.picoxr.com/resources/?platform=unreal`）复制到项目 `Plugins/`
- 启用：Edit > Plugins > INSTALLED > Virtual Reality > **PICO For OpenXR** → Restart Now
- **RHI 线程**：UE 5.6+ 默认启用 RHI 线程，PICO OpenXR 要求**关闭**（Project Settings > Plugins > PICO OpenXR > Disable Separate RHI Thread）
- 配置辅助：PICO OpenXR Portal（Windows，自动弹出，一键项目配置与兼容检测）
- 输入映射：Project Swan 需绑定 **PICO Ultra Controller**；旧手柄映射（PICO 4）在新手柄通常可用，反之不可用，建议逐手柄型号绑定
- 打包：Platforms > Android > Package Project，FLAVOR SELECTIONS 推荐 **Android(OpenXR)**

### 对本项目的含义

1. **UE5.8 不在 PICO 官方插件支持范围**——若走 PICO 官方插件路线（PICOOpenXR），需降级 **UE 5.6 或 5.7**。
2. 官方推荐 **Vulkan + PICO OS 6 新设备**（Project Swan/PICO 4 Ultra 系列）——与我们在 Neo3（OS5/Android 10）上验证的失败路径（Vulkan shader 不兼容、EGL compositor 失败）一致，印证 Neo3 不在官方支持范围。
3. 两条可选路线：
   - **UE5.8 内置 OpenXR（现状）**：仅对 OS6 新设备有理论可行性（Epic 侧支持），无 PICO 官方插件保障。
   - **UE 5.6/5.7 + PICOOpenXR 插件（官方路线）**：Vulkan + OS6 设备，有官方文档与插件保障，推荐度更高。
4. 若走官方路线，`DeviceConfigurationMatrix.md` 的 Vulkan 改回项（`bSupportsVulkan=True` 等）恰好是官方要求，配置方向一致。

## PICO 真机部署与调试

### adb（USB 与无线）

```powershell
# USB 连接
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" devices
# 开启无线调试（USB 连接下执行一次）
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" tcpip 5555
# 设备 IP 查询（USB 或眼镜设置内）
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" shell "ip -f inet addr show wlan0"
# 无线连接（后续可用 -s 指定设备）
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" connect <IP>:5555
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" -s <IP>:5555 shell am force-stop com.YourCompany.VRSanguoYanWuchang
```

### 安装与启动

```powershell
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" install -r "D:\AWork\Unreal\Project\VRSanguoYanWuchang\ArchivedBuilds\Android\VRSanguoYanWuchang-arm64.apk"
```

> 注意：VR 应用必须从**头显内应用列表**启动（PICO 系统走 VR 启动流程）。`am start` 直启会绕过 VR 流程导致 `xrCreateSession` 失败（display_state=MENU）。

### 日志获取（重要：UE 引擎日志写文件，不输出 logcat）

```powershell
# UE 引擎日志文件（外部存储）
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" shell "tail -100 /sdcard/Android/data/com.YourCompany.VRSanguoYanWuchang/files/UnrealGame/VRSanguoYanWuchang/VRSanguoYanWuchang/Saved/Logs/VRSanguoYanWuchang.log"
# 设备系统日志（PICO 运行时/合成器；开发者选项开启"日志"开关后更详细）
& "D:\AWork\Android_SDK\SDK\platform-tools\adb.exe" logcat -d | Select-String -Pattern "APxrRuntime|PxrCompositor|xrt_session"
# APK manifest 检查
& "D:\AWork\Android_SDK\SDK\build-tools\35.0.1\aapt.exe" dump badging <apk路径> | Select-String "launchable-activity"
```

## 真机验证结论（2026-08-09）

- **PICO Neo3 与 UE5.8 不兼容（设备层硬限制）**：
  - Vulkan 路径：Neo3 2022 年 Vulkan 驱动无法编译 UE5.8 SPIR-V shader（`Shader compilation failed / Pipeline create failed`）。
  - OpenGLES 路径：Neo3 OpenXR 运行时 3.0.1 创建 EGL compositor 失败（`Failed to make EGL context current / Failed to create an egl client compositor` → `xrCreateSession: XR_ERROR_INITIALIZATION_FAILED`）。
- 已解决并确认的配置问题（对 PICO 4+ 应可直接运行）：Swappy 禁用（ASIS）、多视图关闭、OpenXR 启用（manifest 补丁）。**新设备接入时按 `DeviceConfigurationMatrix.md` 恢复高性能配置**。
- 已安装且可用的应用：`com.YourCompany.VRSanguoYanWuchang`（arm64，minSdk 26，targetSdk 35，数据内置 APK）。

## 待办（接入新设备后）

- 按 `DeviceConfigurationMatrix.md`「新设备接入检查清单」恢复配置并重新构建。
- 真机验证：OpenXR 运行、6DoF 头显追踪、双控制器输入、瞬移与抓取、断网冷启动、帧率。
- 验证通过后回填 `PicoValidationMatrix.md` 与 `09-verification-register.md` V-005。

## 历史测试记录

| 日期 | 引擎/配置 | 设备 | 结果 | 摘要 |
|---|---|---|---|---|
| 2026-08-09 | UE5.8 / GLES+ASIS+多视图关+OpenXR 补丁 | PICO Neo3（Android 10, API 29, 运行时 3.0.1） | 失败（引擎/运行时不兼容） | 引擎初始化、场景渲染、OpenXR 加载均成功；`xrCreateSession` 被运行时拒绝（EGL compositor 失败）；Neo3 系统 OpenXR 运行时过老 |
| 2026-08-09 | UE5.8 / Vulkan（bSupportsVulkan=True） | PICO Neo3 | 失败（shader 不兼容） | Vulkan Pipeline 创建失败（驱动 2022，编译不了 UE5.8 SPIR-V） |
