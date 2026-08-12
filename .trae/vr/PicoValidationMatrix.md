# PICO 验证矩阵

| 编号 | 项目 | 文件 | 编辑器 | Android 构建 | PICO Neo3 真机 |
|---|---|---|---|---|---|
| VR-001 | OpenXR/PICO 插件启用 | 通过 | 通过 | 通过 | 部分通过（2026-08-11：场景可见，输入未完成） |
| VR-002 | HMD 6DoF 与重定位 | 不适用 | 通过 | 通过 | 待验证（场景已渲染，6DoF 待专项确认） |
| VR-003 | 双控制器输入 | 通过 | 通过 | 通过 | 待验证（IMC 需绑定 PICO Touch 按键） |
| VR-004 | 抓取、释放、双手交互 | 通过 | 通过 | 通过 | 待验证（同上） |
| VR-005 | 平滑移动、瞬移、转向 | 通过 | 通过 | 通过 | 待验证（同上） |
| VR-006 | 暂停/恢复与追踪丢失 | 不适用 | 待验证 | 通过 | 待验证 |
| VR-007 | 断网冷启动与游玩 | 不适用 | 不适用 | 通过 | 待验证 |
| VR-008 | 4v4 性能压力场景 | 不适用 | 待验证 | 通过 | 待验证 |

状态说明（2026-08-11 M00-T004 更新）：

- 文件层通过：`BP_XRPawn`、`BP_GrabComponent`、`BP_TeleportVisualizer`、手部/抓取/移动/瞬移输入资产（`IMC_Hands/Default`、`IA_Move/Turn/Grab_*`）、`SK_MannequinsXR` 均存在。
- 编辑器层通过：OpenXR、OpenXREyeTracker、OpenXRHandTracking、PICOController、EnhancedInput 插件运行中全部启用；OpenXR `xrCreateInstance succeeded`。
- Android 构建通过：UE5.6 BuildCookRun BUILD SUCCESSFUL，APK 产物 `ArchivedBuilds\Android\VRSanguoYanWuchang-arm64.apk`。
- 真机部分通过（2026-08-11）：swapchain 补丁生效、场景渲染可见（V-008）；输入映射未完成（IMC 需绑 PICO Touch、OpenXR Input 缺 PlayerMappableInputConfig、手柄模型未挂载），完成配置后回填 VR-001~VR-005 真机列。

证据统一登记到 `../registers/09-verification-register.md`。
