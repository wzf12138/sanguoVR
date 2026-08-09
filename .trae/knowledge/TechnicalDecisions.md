# 技术决策

## 已确认决策

| 项目 | 决策 |
|---|---|
| 引擎 | UE5.8 安装版 |
| 工程方式 | 全新 C++ 工程，不升级旧 UE4 项目 |
| 基础模板 | 以 UE5.8 官方 VR 模板为功能基准；用户将于 2026-08-09 基于官方 VR 模板手动重建项目，替换当前 C++ 空模板骨架，之后在模板能力上补齐本项目战斗与系统内容 |
| 目标设备 | PICO Neo3 普通版 |
| XR 基础 | 优先使用 UE5.8 内置 OpenXR |
| PICO 外部插件 | 第一里程碑前不安装，真机缺失能力时再评估 |
| 编程方式 | C++ 核心规则 + 蓝图表现与配置 |
| 输入 | Enhanced Input |
| 版本控制 | Git + Git LFS |
| 美术策略 | 先灰盒验证，再引入正式资源 |

当前开发工具为 Visual Studio Community 2026 Insiders，已安装 MSVC 14.51.36231、Windows SDK 10.0.26100 与 Unreal 工具。该工具链尚未由 UE5.8 完成清理编译验证，因此属于“已安装、待兼容验证”，不属于已通过的工程基线。若验证失败，改用 Epic 支持 UE5.8 的稳定版 Visual Studio。

当前 `.uproject` 已启用 UE5.8 内置 OpenXR、OpenXREyeTracker、OpenXRHandTracking 和 `PICOController`。这里的 `PICOController` 是引擎内置控制器支持，不等同于安装 PICO 外部运行时插件；第一里程碑前仍不引入外部插件。

## MCP 连接器验证（2026-08-09，M00-T003）

- MCP 服务器 `mcp_unreal-engine` 可用；`list_toolsets` 返回约 40 个工具集，覆盖 AgentSkill、AutomationTest、ConfigSettings、EditorApp、Logs、GameplayTags、Niagara、UMG、Sequencer、DataTable 等。
- 经 `call_tool` 调用 `EditorToolset.LogsToolset.GetLogCategories` 与 `GetLogEntries` 成功：日志类别可枚举，`LogLoad` 无 error/fail 条目，`LogTemp` 仅引擎自带 `UE::UnifiedErrorTest` 测试条目，编辑器会话模块与插件加载无致命错误。
- 编辑器 MCP 服务器当前已连接且可查询，后续工具链任务可直接经 MCP 执行编辑器内操作。
- 2026-08-09 更新：用户重启电脑后 MCP 桥接恢复正常，`list_toolsets` 再次返回约 40 个工具集，连接器可用性确认无遗留问题。

## UE5.8 与 PICO Neo3 真机不兼容（2026-08-09，M00-T004 阻塞）

- **现象**：APK 构建/安装成功（Pico Neo 3 识别，adb install Success），但应用启动后引擎静默退出（`VM exiting result code 0`），引擎零日志输出（`logcat -s UE` 全空）。
- **根因证据**：UE5.8 内置 SwappyDisplayManager（Android Game SDK 帧率组件，源码 `VulkanRHI/Private/Android/VulkanAndroidPlatform.cpp` 与 `UEDeployAndroid.CopySwappy` 无条件打包）以 `InMemoryDexClassLoader` 加载 `libUnreal.so` 失败（nativeLibraryDirectories 仅系统目录）；引擎日志系统未启动即退出。设备基线 Android 10 + 2021-04 安全补丁 + 2022 Vulkan 驱动。
- **已排除**：Vulkan/GLES 渲染后端（均尝试）、Quest 打包配置（已修正为 PICO）、NDK API 级别（android-26）、SDK/NDK/JDK 版本（均符合官方要求）。
- **结论**：UE5.8 与 PICO Neo3 环境不兼容，无引擎级配置开关绕过。
- **候选方向（待用户决策）**：A. 换 PICO 4/新设备（Android 12+，UE5.8 原生支持）；B. 降级 UE 5.4/5.5/5.6 + PICO 官方 OpenXR 插件（官方支持组合，对 Neo3 兼容）；C. 深挖引擎源码改造 Swappy（高投入）。

- **发现**：`Config/DefaultEngine.ini` 的 `[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]` 为 Meta Quest 配置（`bPackageForMetaQuest=True`、`ExtraApplicationSettings` 含 `com.oculus.supportedDevices` 与 `libopenxr.google.so`、`MinSDKVersion=32`、`TargetSDKVersion=32`），与本项目 PICO Neo3 目标设备决策不一致。
- **影响**：`MinSDKVersion=32` 高于 PICO Neo3 系统版本（Android 10 / API 29），将导致 APK 安装失败；Quest 打包内容对 PICO 无意义。
- **处理**（用户指挥，经 MCP `ConfigSettingsToolset.SetSectionProperties` 于 2026-08-09 完成，项目已保存）：`bPackageForMetaQuest=False`、`extraApplicationSettings` 清空 Quest 内容、`bPackageDataInsideApk=True`、`MinSDKVersion=26`（官方最低安装 26，兼容 API 29 设备）、`TargetSDKVersion=35`（官方推荐）；保留 `bPackageForOpenXRImmersive=True`（PICO 走内置 OpenXR）。
- 修改后需重新构建 APK 并在 PICO Neo3 真机验证。

## 代码边界

- C++：战斗状态、轨迹检测、伤害、格挡、移动接口和通用交互规则。
- 蓝图：VR 表现、流程、动画、音效、特效、UI 和关卡装配。
- Data Asset：武器、AI、难度、竞技场和反馈参数。
- 行为树或状态系统：AI 感知、战术选择和动作执行。

## 规划中的核心模块

- `CombatComponent`
- `WeaponComponent`
- `DefenseComponent`
- `DamageComponent`
- `VRMovementComponent`
- `InteractionComponent`
- `CombatResolver`

这些名称是架构规划，不代表当前已经创建。

## 变更门槛

以下变化必须先记录原因、收益、风险和回退方案：

- 更换 UE 主版本。
- 从 OpenXR 改为厂商专用 XR 路线。
- 安装影响运行时的第三方插件。
- 改变 `Content/VRSanguo` 根目录规范。
- 将核心规则从 C++ 移到蓝图或反向迁移。
