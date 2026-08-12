# 设备配置矩阵（Android/OpenXR）

> 用途：记录项目 Android/VR 打包配置的**当前值、设置原因、目标设备影响**，特别是"为兼容 PICO Neo3 而妥协、接入新设备时需恢复"的配置项。
> 维护：每次改动设备相关配置时更新本表。最后更新：2026-08-11（M00-T004：已切换 UE5.6 + PICO OpenXR Plugin OS 5，配置基线更新）。

## 配置位置

- 项目 `Config/DefaultEngine.ini`：`[/Script/AndroidRuntimeSettings.AndroidRuntimeSettings]`、`[/Script/Engine.RendererSettings]`、`[/Script/AndroidSingleInstanceServiceEditor.AndroidSingleInstanceServiceRuntimeSettings]`、`[/Script/PICOOpenXRRuntimeSettings.PICOOpenXRRuntimeSettings]`、`[SystemSettings]`
- 项目 `Config/DefaultGame.ini`、`Config/Android/AndroidGame.ini`：Android 设备配置
- 项目 `Plugins/PICOOpen174f9f81d266V8/`：PICO OpenXR Plugin（OS 5，v1.6.1，含 swapchain 补丁）

## 配置矩阵（当前：UE5.6 + PICO OpenXR Plugin OS 5 + Neo3）

### 渲染与兼容（当前有效值）

| 配置项 | 当前值 | 说明 |
|---|---|---|
| 图形接口 | **Vulkan**（PICO OpenXR Plugin OS 5 官方要求；UE5.6 对 Neo3 Vulkan 驱动兼容，与 UE5.8 不同） | 官方路线：Vulkan；勿改回 GLES |
| `vr.MobileMultiView` | `False`（Neo3 兼容） | Neo3 layered framebuffer 不兼容；新设备可评估改回 `True` 提升性能 |
| `bPackageForOpenXRImmersive` | `True` | PICO 走 OpenXR |
| `MinSDKVersion` | `26` | 兼容 Neo3（Android 10/API 29） |
| `TargetSDKVersion` | `35` | 官方推荐 |
| `bPackageDataInsideApk` | `True` | 数据内置单文件 APK |
| `bPackageForMetaQuest` | `False` | 本项目 PICO 目标 |
| `Disable Separate RHI Thread`（PICO OpenXR 插件设置） | `True` | UE5.6 默认启用 RHI 线程，PICO 要求关闭（启用插件后自动关闭，手动确认） |

### ⚠️ swapchain 补丁（当前必须保留，新设备需评估）

| 位置 | 内容 | 说明与建议 |
|---|---|---|
| `Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp` | 拦截 `xrCreateSwapchain`，剥离 `XR_KHR_vulkan_swapchain_format_list` 扩展，只传单一 `B8G8R8A8_SRGB`（43）格式 | Neo3 系统 OpenXR 运行时（R2.1.12.0）对 format list 触发 ION ENOTTY 崩溃（2026-08-11 实测并修复）。**新设备（PICO 4+/Quest）接入时评估是否仍需要**：若新版运行时支持 format list，可移除补丁恢复引擎默认行为；升级 PICO 插件后须重打补丁（备份 `Build/Patches/PICOOpenXR/`，恢复脚本 `restore_pico_patch.ps1`） |

### UE5.8 遗留（已弃用，保留参考）

| 配置项 | 值 | 说明 |
|---|---|---|
| `a.UseSwappyForFramePacing` | `0` | UE5.8 时代禁用 Swappy（ASIS 已覆盖）；UE5.6 下由 PICO 插件管理，无需手动 |
| `NDKAPILevelOverride` | `android-26` | UE5.8 时代覆盖；UE5.6 用官方默认 |
| `Build/Android/ManifestActivityAdditions.txt` | MAIN+LAUNCHER+IMMERSIVE_HMD | UE5.8 时代 APL bug 补丁；**UE5.6 + PICO OpenXR Plugin 自动处理 manifest，此文件不再需要**（确认已移除/不生效） |
| `bSupportsVulkan` / `bSupportsVulkanSM5` | 见引擎默认 | UE5.6 官方 Vulkan 路线，无需手工关闭 |

## 历史参考：UE5.8 时代的 Neo3 兼容配置（已弃用，2026-08-09）

> UE5.8 路线已废弃（Neo3 与 UE5.8 不兼容，已降级 UE5.6）。以下为当时"为兼容 Neo3 而改"的记录，仅作历史参考，**不得直接应用于 UE5.6 项目**（UE5.6 已走 Vulkan 官方路线）。

- `bSupportsVulkan=False` / `bSupportsVulkanSM5=False`：Neo3 2022 Vulkan 驱动无法编译 UE5.8 SPIR-V → 改 GLES（UE5.6 无需，Vulkan 官方支持）。
- `vr.MobileMultiView=False`：Neo3 layered framebuffer 附件不兼容（`Framebuffer not complete 0x8cd6`）——**UE5.6 下仍保留 False**（见上表）。
- `r.MSAACount=0`：调试排障关闭；新设备恢复 2/4。
- `a.UseSwappyForFramePacing=0`：Neo3 上 Swappy 加载 libUnreal.so 失败；UE5.6 下由 PICO 插件管理。
- `NDKAPILevelOverride=android-26`：降级以兼容 Neo3；UE5.6 用官方默认。
- `Build/Android/ManifestActivityAdditions.txt`：UE5.8 APL bug 补丁（MAIN+LAUNCHER+IMMERSIVE_HMD）；**UE5.6 + PICO OpenXR Plugin 自动处理 manifest，不再需要**。
- `bEnableASISPlugin=True`：一体机单实例服务；UE5.6 保留（一体机标准）。

## 新设备接入检查清单

> 当前已处于 UE5.6 + PICO OpenXR Plugin（OS 5）路线（2026-08-11 迁移完成）。以下清单覆盖：新 PICO 设备接入、以及未来升级引擎的恢复。

### 当前状态（UE5.6 + Neo3，2026-08-11 已完成）

1. ✅ 项目已基于 UE5.6 官方 VR 模板重建（Content/Source/Config 已迁移）。
2. ✅ PICO OpenXR Plugin（OS 5）v1.6.1 已迁移至项目 `Plugins/`（源码编译，含 swapchain 补丁）。
3. ✅ RHI 线程关闭（PICO 插件要求）。
4. ✅ Vulkan 官方路线（UE5.6 对 Neo3 驱动兼容）。
5. ✅ Neo3 系统 5.13.7.S ≥ 官方要求 5.13.0。
6. ✅ swapchain 补丁已编译生效、真机场景可见（V-008）。
7. ⏳ 遗留：IMC 绑定 PICO Touch 按键、OpenXR Input PlayerMappableInputConfig、Neo3 手柄模型挂载（见 PicoNeo3BuildGuide「待办」）。

### 新设备接入（PICO 4 / 4 Ultra / 新机型）

1. 验证 swapchain 补丁是否仍需要：新版系统 OpenXR 运行时若支持 `XR_KHR_vulkan_swapchain_format_list`，移除补丁恢复引擎默认（备份在 `Build/Patches/PICOOpenXR/`）。
2. `vr.MobileMultiView` 评估改回 `True`（提升渲染性能）；`r.MSAACount` 恢复 2/4。
3. 确认系统版本与引擎/插件组合：UE 5.7 不支持 PICO 4 系列（Neo3 可用）；PICO 4 Ultra 支持。
4. 重新构建 + 真机验证（流程见 `PicoNeo3BuildGuide.md`）。

### 未来升级引擎（UE5.6 → 更新版本，若将来换）

1. 评估 PICO OpenXR Plugin 新版本兼容矩阵（官方文档 developer.picoxr.com）。
2. 升级插件后按 TD-005 重打 swapchain 补丁并符号验证（`PICOLayerCreateSwapchain`）。
3. 确认 manifest 由插件自动处理，无需 `ManifestActivityAdditions.txt`。
4. 重新构建 + 真机验证（流程见 `PicoNeo3BuildGuide.md`）。

## 历史结论速查（2026-08-09）

- PICO Neo3（Android 10 / API 29 / 2021 安全补丁 / 2022 GPU 驱动 / OpenXR 运行时 3.0.1）：与 UE5.8 **不兼容**（Vulkan shader 编译失败；GLES 下运行时 `Failed to create egl client compositor`）。工程配置对 PICO 4+ 应可直接运行。
- 详见 `TechnicalDecisions.md`「UE5.8 与 PICO Neo3 真机不兼容」与「真机调试进展」。
