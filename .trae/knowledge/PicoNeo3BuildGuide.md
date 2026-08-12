# PICO Neo3 构建指南

> 最后更新：2026-08-11（M00-T004：UE5.6 迁移执行中，swapchain 补丁生效、真机场景可见；构建环境已切 UE5.6）

## UE5.6 Android 工具链要求与实测状态

| 组件 | 版本要求 | 实测状态 |
|------|---------|---------|
| 引擎 | UE 5.6 安装版（PICO OpenXR Plugin OS 5 官方支持 5.6/5.7） | ✅ 已用（`D:\AWork\Unreal\App\UE_5.6`，5.6.1，CL 44394996） |
| SDK 目标平台 | 推荐 android-35，最低安装 26 | ✅ android-34/35 已装（`D:\AWork\Android_SDK\SDK\platforms`） |
| NDK | r27c（27.2.12479018） | ✅ 已装（`D:\AWork\Android_SDK\SDK\ndk\27.2.12479018`） |
| Build-tools | 35.0.1 | ✅ 已装 |
| JDK | OpenJDK 21 | ✅ Temurin JDK 21.0.12（`D:\AWork\Android_SDK\jdk-21.0.12+8`） |
| Gradle | 引擎自带 wrapper（UE5.6 用 8.x） | ✅ 发行版预置本地缓存（见下） |
| 设备要求 | PICO Neo3，系统 ≥ 5.13.0 | ✅ Neo3 系统 5.13.7.S，满足官方 OpenXR 插件要求 |

## 构建环境（必读）

### 每次构建前设置的环境变量（PowerShell）

```powershell
$env:ANDROID_HOME = "D:\AWork\Android_SDK\SDK"
$env:NDKROOT = "D:\AWork\Android_SDK\SDK\ndk\27.2.12479018"
$env:JAVA_HOME = "D:\AWork\Android_SDK\jdk-21.0.12+8"
$env:uebp_LogFolder = "C:\Users\PC\AppData\Local\Temp\UATLogs"
# 可选（若 Gradle 缓存目录切换过）
$env:GRADLE_USER_HOME = "D:\AWork\.gradle"
```

### 完整打包命令（UE5.6，含 Gradle 打包与归档）

```powershell
& "D:\AWork\Unreal\App\UE_5.6\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="D:\AWork\Unreal\Project\VRSanguoYanWuchang\VRSanguoYanWuchang.uproject" -platform=Android -configuration=Development -build -cook -stage -pak -package -archive
```

- 必须带 `-package`（否则只 Stage 不打包 APK，Archive 会报 `obb not found`）。
- 产物：`ArchivedBuilds\Android\VRSanguoYanWuchang-arm64.apk`；符号库在 `ArchivedBuilds\Android\VRSanguoYanWuchang_Symbols_v1\`。
- 编辑器运行中（Live Coding 激活）构建会失败，需先关闭编辑器。
- 引擎增量构建对**引擎目录内插件源码变化不可见**（adaptive non-unity 用 `git status` 判断 working set）；PICO 插件已在项目 `Plugins/`，源码变化可被正常检测。

### 已知构建坑（已解决）

| 问题 | 解决 |
|---|---|
| `Sdk: not found. Required version r27c` | 必须同时设置 `NDKROOT`（UBT 不会从 ANDROID_HOME 推导） |
| `obb was not found` | 构建命令加 `-package` |
| Gradle 下载超时（services.gradle.org） | 国内镜像下载 gradle-all.zip 放入 `D:\AWork\.gradle\wrapper\dists\`（hash 目录由 wrapper 首次运行创建；放错目录无效） |
| Gradle 缓存占 C 盘 | `GRADLE_USER_HOME=D:\AWork\.gradle` |
| **`Missing precompiled manifest for 'PICOOpenXRRuntimeSettings'`**（引擎 Marketplace 插件） | 安装版引擎中 Marketplace 插件必按 precompiled 处理并要求 manifest；把 PICO 插件迁移到项目 `Plugins/` 并从源码编译解决（见「PICO 插件迁移」） |
| **`Precompiled rules assembly UE5Rules.dll does not exist`** | **不要删除** `Engine\Intermediate\Build\BuildRules\`（安装版引擎预编译规则，Epic 打包时生成，本机无法从源码重建完整版）；误删后用 Epic Launcher「验证/修复」引擎恢复 |
| **`Couldn't find target rules file for target 'ShaderCompileWorker'`** | 安装版引擎裁剪了工具源码（`Source\Programs` 无 ShaderCompileWorker），从源码重建 UE5Rules.dll 必然不完整；必须恢复安装版原始 DLL（同上） |
| **`RunUAT.bat ERROR: AutomationTool failed to compile`** | 安装版引擎无 `BuildUAT.bat`；`InstalledBuild.txt` 存在时 RunUAT 走预编译路径，勿移除该标志；若已移除，用 `-nocompileuat` 参数或恢复标志 |
| **补丁改了源码但 APK 内无新符号** | ① 插件在引擎目录时增量构建检测不到（git status 盲区）→ 迁移到项目 Plugins；② 源码文件时间戳比 `.o` 旧（`Copy-Item` 保留旧时间戳）→ `touch` 源码或删除插件 `Intermediate\Build\Android` 强制重编；③ 规则 DLL 缓存（`C:\Users\PC\AppData\Local\UnrealEngine\Intermediate\Build\BuildRules\MarketplaceRules.dll`）未刷新 → 删除该缓存 |
| **`Swapchain format not supported (50)` 后原生崩溃**（Neo3 运行时） | 已打补丁：`PICO_HMD.cpp` 拦截 `xrCreateSwapchain` 剥离 format list（详见 `TechnicalDecisions.md`「swapchain 补丁」） |

### PICO 插件迁移（2026-08-11）

- 插件从引擎 `Engine/Plugins/Marketplace/PICOOpen174f9f81d266V8` 迁移到项目 `Plugins/PICOOpen174f9f81d266V8`；引擎目录原插件改名 `.disabled`。
- 迁移原因与配套修改（`PrecompileForTargets`、`Installed=false`）见 `TechnicalDecisions.md`。
- 项目插件关键文件：`PICOOpenXR.uplugin`、`Source/PICOOpenXRHMD/Private/PICO_HMD.cpp`（含补丁）、`Source/ThirdParty/PICOOpenXRLoader/libs/arm64-v8a/libopenxr_loader_pico.so`（Neo3 运行时库，勿删）。
- 备份：补丁前文件备份于项目内 `Build/Patches/PICOOpenXR/`（恢复脚本 `Build/Patches/PICOOpenXR/restore_pico_patch.ps1`，随 git 提交）。

## PICO 官方 UE 插件支持（2026-08-10 官网提炼，已修正 OS5/OS6 区分）

来源：PICO 开发者文档（developer.picoxr.com），两个 OS 版本需区分。

### 关键区分：OS 5 vs OS 6（之前犯过错）

PICO 有两套 Unreal SDK 文档体系：

| 文档 | 目标系统 | 目标设备 | 我们的关联 |
|---|---|---|---|
| PICO Unreal SDK（OS 6）| OS 6 | Project Swan 等新设备 | 与本项目 Neo3 无关 |
| **PICO Unreal OpenXR Plugin（OS 5）** | **OS 5** | **PICO Neo3、PICO 4、PICO 4 Ultra** | **✅ 本项目官方路线** |
| PICO Unreal Integration SDK（OS 5）| OS 5 | PICO VR 一体机 | 功能全面但笨重，OpenXR Plugin 更简洁 |

### PICO Unreal OpenXR Plugin（OS 5）— Neo3 官方路线（权威）

- 所属体系：**OS 5**（非 OS 6！注意区分）
- 虚幻引擎：**UE 5.6 或 5.7**（UE 5.7 不支持 PICO 4 系列，但支持 Neo3）
- 图形接口：**Vulkan**
- 操作系统：Windows 和 macOS
- 支持的 PICO 设备型号：**PICO Neo3 系列**、PICO 4 系列 (不支持 UE 5.7)、PICO 4 Ultra 系列、PICO G3（有限支持）
- PICO 设备系统版本：**5.13.0 及以上**
- 安装方式：Fab（免费添加）→ Epic Games Launcher → My Library → 安装到引擎
  - Fab 链接：https://www.fab.com/listings/a7eb0f28-d7f1-4b30-8d2d-49d12eeb1d62
  - 或从官网下载 SDK（developer.picoxr.com/resources/?platform=unreal）复制到项目 `Plugins/`
- 启用：Edit > Plugins > Virtual Reality > **PICO For OpenXR** → Restart Now
- **RHI 线程**：UE 5.6+ 默认启用，PICO OpenXR 要求**关闭**（启用插件后自动关闭）
- 配置辅助：PICO OpenXR Portal（Windows，自动弹出，一键项目配置与兼容检测）
- 打包：Platforms > Android > Package Project，FLAVOR SELECTIONS 推荐 **Android(OpenXR)**

### PICO Unreal Integration SDK（OS 5）— 备选路线

- 版本：3.4.0
- 功能全面：渲染、交互、追踪、MR、空间锚点、平台服务等
- 面向 PICO VR 一体机（含 Neo3）；有 UE5 特性支持
- 相比 OpenXR Plugin：功能更全但更重，需要导入 SDK 替换插件；本项目用 OpenXR Plugin 足够。

### 对本项目的含义（修正后）

1. ✅ **PICO Unreal OpenXR Plugin（OS 5）官方支持 Neo3**——这是我们的路线。
2. ✅ 推荐 **UE 5.6**（UE 5.7 不支持 PICO 4 系列，但 Neo3 可用 5.7；稳妥选 5.6）。
3. ⚠️ **系统版本阈值**：设备系统需≥5.13.0——待验证 Neo3 实际固件版本（可能需升级）。
4. ❌ **不推荐 UE 5.8**——PICO 官方插件不支持；UI5.8 内置 OpenXR 对 Neo3 已验证不兼容。✅ Neo3 系统版本 5.13.7.S 已满足官方 OpenXR 插件要求（≥5.13.0）。
5. 🔄 从 UE5.8 迁移到 5.6：需**新建项目**（5.8 项目无法被 5.6 打开）→ 手工迁移 Content/Config/Source → 重新启用 PICO OpenXR 插件。
6. 💾 本地旧 SDK（`D:\AGame\Pico_Neo_3\SDK`）为 UE4 时代 PICOXR 旧插件，与本项目无关，可删除（用户已确认可删）。

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

## 真机验证结论（2026-08-11 更新）

### UE5.8 路线（2026-08-09，已弃用）

- **PICO Neo3 与 UE5.8 不兼容（设备层硬限制）**：
  - Vulkan 路径：Neo3 2022 年 Vulkan 驱动无法编译 UE5.8 SPIR-V shader（`Shader compilation failed / Pipeline create failed`）。
  - OpenGLES 路径：Neo3 OpenXR 运行时 3.0.1 创建 EGL compositor 失败（`Failed to make EGL context current / Failed to create an egl client compositor` → `xrCreateSession: XR_ERROR_INITIALIZATION_FAILED`）。
- 已解决并确认的配置问题（对 PICO 4+ 应可直接运行）：Swappy 禁用（ASIS）、多视图关闭、OpenXR 启用（manifest 补丁）。**新设备接入时按 `DeviceConfigurationMatrix.md` 恢复高性能配置**。

### UE5.6 路线（2026-08-11，当前）

- **场景渲染已通**：swapchain 补丁生效（`PICOLayerCreateSwapchain` 符号确认；Neo3 真机场景可见，`Swapchain format not supported (50)` 回退后正常创建，无原生崩溃）。
- **输入遗留（进行中）**：
  - IMC 资产需按 PICO 官方文档绑定 PICO Touch 按键（IA_Move→PICO Touch (R) Thumbstick Y 等），当前为 Quest 风格绑定。
  - OpenXR Input 项目设置缺 `PlayerMappableInputConfig`（引擎日志警告 `action bindings will not be visible to the OpenXR runtime`）。
  - `DefaultInput.ini` 曾指向不存在的 `/Game/XRFramework/Input/`（5.8 迁移残留），已修复为 `/Game/VRTemplate/Input/`（v3 日志确认 IMC 全部加载成功）。
- **手柄模型遗留**：VRPawn 用官方 MannequinsXR 手部模型，PICO 官方要求挂载插件自带 `Meshes/PicoNeo3/SM_PICONeo3_L/R` + `M_PICONeo3Controller`。

## 待办（UE5.6 真机完成）

- 编辑器内：VRPawn 挂载 Neo3 手柄模型；IMC_Default/IMC_Hands 等绑定 PICO Touch 按键；配置 OpenXR Input 的 PlayerMappableInputConfig。
- 真机验证：双控制器输入、瞬移与抓取、断网冷启动、帧率。
- 验证通过后回填 `PicoValidationMatrix.md` 与 `09-verification-register.md` V-008。

## 历史测试记录

| 日期 | 引擎/配置 | 设备 | 结果 | 摘要 |
|---|---|---|---|---|
| 2026-08-09 | UE5.8 / GLES+ASIS+多视图关+OpenXR 补丁 | PICO Neo3（Android 10, API 29, 运行时 3.0.1） | 失败（引擎/运行时不兼容） | 引擎初始化、场景渲染、OpenXR 加载均成功；`xrCreateSession` 被运行时拒绝（EGL compositor 失败）；Neo3 系统 OpenXR 运行时过老 |
| 2026-08-09 | UE5.8 / Vulkan（bSupportsVulkan=True） | PICO Neo3 | 失败（shader 不兼容） | Vulkan Pipeline 创建失败（驱动 2022，编译不了 UE5.8 SPIR-V） |
| 2026-08-11 | UE5.6 + PICO OpenXR Plugin 1.6.1（项目 Plugins）+ swapchain 补丁 | PICO Neo3（系统 5.13.7.S） | 部分通过（场景可见，输入未完成） | swapchain 补丁生效，场景渲染正常；手柄模型未挂载、输入映射未绑 PICO Touch，待编辑器配置 |
