# 设备配置矩阵（Android/OpenXR）

> 用途：记录项目 Android/VR 打包配置的**当前值、设置原因、目标设备影响**，特别是"为兼容 PICO Neo3 而妥协、接入新设备时需恢复"的配置项。
> 维护：每次改动设备相关配置时更新本表。最后更新：2026-08-09（M00-T004 深夜调试后）。

## 配置位置

- 项目 `Config/DefaultEngine.ini`：`[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]`、`[/Script/Engine.RendererSettings]`、`[/Script/AndroidSingleInstanceServiceEditor.AndroidSingleInstanceServiceRuntimeSettings]`、`[SystemSettings]`
- 项目 `Build/Android/ManifestActivityAdditions.txt`：manifest 附加（UE5.8 APL bug 补丁）

## 配置矩阵

### ⚠️ 为兼容 PICO Neo3 而改、新设备需恢复（影响效果）

| 配置项 | 当前值 | 设置原因（Neo3） | 新设备（PICO 4 / Quest / 新机型）建议 |
|---|---|---|---|
| `bSupportsVulkan` | `False` | Neo3 2022 年 Vulkan 驱动无法编译 UE5.8 SPIR-V shader（Pipeline 创建失败） | **改回 `True`**。新设备 Vulkan 驱动正常，性能优于 GLES |
| `bSupportsVulkanSM5` | `False` | 随 bSupportsVulkan 关闭 | **改回 `True`**（如需 SM5 渲染特性；移动 VR 通常不需要 SM6） |
| `vr.MobileMultiView` | `False` | Neo3 多视图 layered framebuffer 附件不兼容（`Framebuffer not complete 0x8cd6`） | **改回 `True`**。多视图显著提升 VR 渲染性能（单通道渲染），新设备驱动支持 |
| `r.MSAACount` | `0` | 调试排障时关闭（实测 MSAA 非 framebuffer 崩溃元凶，但已关闭） | **改回 `2` 或 `4`**。VR 画面抗锯齿质量，0 会导致明显锯齿 |
| `a.UseSwappyForFramePacing`（`[SystemSettings]`） | `0` | Neo3 上 Swappy（Android Game SDK 帧率控制）加载 libUnreal.so 失败 | **删除或改回 `1`**。Swappy 改善新设备帧率稳定/延迟 |
| `NDKAPILevelOverride` | `android-26` | 降到 26 以兼容 Neo3（Android 10/API 29，minSdk 需 ≤29） | **删除**（用引擎默认）。新设备系统新，无需此覆盖 |

### ✅ 永久正确 / 与设备无关（保留）

| 配置项 | 当前值 | 说明 |
|---|---|---|
| `bPackageForMetaQuest` | `False` | 本项目目标为 PICO；若改用 Meta Quest 设备需改 `True` |
| `bPackageForOpenXRImmersive` | `True` | PICO/新设备均走 OpenXR，保留 |
| `ExtraApplicationSettings` | 空（已清空 Quest 内容） | 删除 `com.oculus.supportedDevices` 与 `libopenxr.google.so` |
| `bBuildForES31` | `True` | 打包 GLES 3.1 shader；与 Vulkan 并存可作为兼容兜底，建议保留 |
| `MinSDKVersion` | `26` | UE5.8 官方最低安装版本 |
| `TargetSDKVersion` | `35` | UE5.8 官方推荐 |
| `bPackageDataInsideApk` | `True` | 数据内置 APK，单文件安装；项目规模小时保留，大项目可改回 OBB 模式 |
| `bEnableASISPlugin` | `True` | 一体机单实例服务（宏 `USE_ANDROID_STANDALONE=1`）；同时也是禁用 Swappy 的机制。新设备保留（一体机标准）；若未来用 Meta Quest 官方打包流程，ASIS 由其自动管理，可评估移除本项目手动设置 |

### ⚠️ manifest 附加补丁（新设备需验证）

| 文件 | 内容 | 说明与建议 |
|---|---|---|
| `Build/Android/ManifestActivityAdditions.txt` | GameActivity 添加 `<intent-filter><action MAIN/><category LAUNCHER/><category org.khronos.openxr.intent.category.IMMERSIVE_HMD/></intent-filter>` | 绕过 UE5.8 OpenXR APL bug（ASIS 启用后 UE 不再生成 LAUNCHER filter，且 APL 的 IMMERSIVE_HMD category 添加失效）。**新设备打包后先验证 manifest 是否已含所需 filter；若引擎修复或 Quest 打包自动添加，删除本文件避免重复 intent-filter** |

## 新设备接入检查清单

1. 恢复高性能配置：`bSupportsVulkan=True`、`bSupportsVulkanSM5=True`、`vr.MobileMultiView=True`、`r.MSAACount=2/4`、删除 `a.UseSwappyForFramePacing=0` 与 `NDKAPILevelOverride`。
2. 确认目标设备打包类型：PICO → `bPackageForMetaQuest=False`；Meta Quest → `True`。
3. 验证 manifest：新设备安装前 `aapt dump badging <apk>` 检查 `launchable-activity` 与 OpenXR category 是否符合预期；确认后可删除 `ManifestActivityAdditions.txt`。
4. 若改回 Vulkan：确认目标设备 Vulkan 驱动支持 UE5.8 SPIR-V（PICO 4 / 新机型：是）。
5. 重新构建 + 真机验证（流程见 `PicoNeo3BuildGuide.md`）。

## 历史结论速查（2026-08-09）

- PICO Neo3（Android 10 / API 29 / 2021 安全补丁 / 2022 GPU 驱动 / OpenXR 运行时 3.0.1）：与 UE5.8 **不兼容**（Vulkan shader 编译失败；GLES 下运行时 `Failed to create egl client compositor`）。工程配置对 PICO 4+ 应可直接运行。
- 详见 `TechnicalDecisions.md`「UE5.8 与 PICO Neo3 真机不兼容」与「真机调试进展」。
