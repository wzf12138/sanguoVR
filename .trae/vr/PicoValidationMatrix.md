# PICO 验证矩阵

| 编号 | 项目 | 文件 | 编辑器 | Android 构建 | PICO Neo3 真机 |
|---|---|---|---|---|---|
| VR-001 | OpenXR/PICO 插件启用 | 通过 | 通过 | 通过 | 待验证 |
| VR-002 | HMD 6DoF 与重定位 | 不适用 | 通过 | 通过 | 待验证 |
| VR-003 | 双控制器输入 | 通过 | 通过 | 通过 | 待验证 |
| VR-004 | 抓取、释放、双手交互 | 通过 | 通过 | 通过 | 待验证 |
| VR-005 | 平滑移动、瞬移、转向 | 通过 | 通过 | 通过 | 待验证 |
| VR-006 | 暂停/恢复与追踪丢失 | 不适用 | 待验证 | 通过 | 待验证 |
| VR-007 | 断网冷启动与游玩 | 不适用 | 不适用 | 通过 | 待验证 |
| VR-008 | 4v4 性能压力场景 | 不适用 | 待验证 | 通过 | 待验证 |

状态说明（2026-08-09 M00-T004）：

- 文件层通过：`BP_XRPawn`、`BP_GrabComponent`、`BP_TeleportVisualizer`、手部/抓取/移动/瞬移输入资产（`IMC_Hands/Default`、`IA_Move/Turn/Grab_*`）、`SK_MannequinsXR` 均存在。
- 编辑器层通过：OpenXR、OpenXREyeTracker、OpenXRHandTracking、PICOController、EnhancedInput 插件运行中全部启用；OpenXR `xrCreateInstance succeeded`（SteamVR/OpenXR 2.14.5 运行时）；PICOController 在 PC 端按预期"加载但忽略"（`XR_BD_controller_interaction` 扩展仅 Android/PICO 目标平台启用）。
- Android 构建与真机列为待验证，构建产物与真机证据生成后回填；不得以编辑器结论替代 PICO Neo3 真机结论。

证据统一登记到 `../registers/09-verification-register.md`。
