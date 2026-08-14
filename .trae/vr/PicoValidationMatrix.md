# PICO 验证矩阵

| 编号 | 项目 | 文件 | 编辑器 | Android 构建 | PICO Neo3 真机 |
|---|---|---|---|---|---|
| VR-001 | OpenXR/PICO 插件启用 | 通过 | 通过 | 通过 | 通过（2026-08-13：场景可见、OpenXR 会话正常、手柄追踪可见） |
| VR-002 | HMD 6DoF 与重定位 | 不适用 | 通过 | 通过 | 通过（2026-08-13：场景随头部 6DoF 正常渲染与重定位，无异常） |
| VR-003 | 双控制器输入 | 通过 | 通过 | 通过 | 通过（2026-08-13：IMC 按 PICO 官方文档绑定 5 个全部生效，双控制器操作可用） |
| VR-004 | 抓取、释放、双手交互 | 通过 | 通过 | 通过 | 通过（2026-08-13：抓取/释放可用；双手交互随输入链路打通） |
| VR-005 | 平滑移动、瞬移、转向 | 通过 | 通过 | 通过 | 通过（2026-08-13：移动/瞬移/转向输入生效，操作正常） |
| VR-006 | 暂停/恢复与追踪丢失 | 不适用 | 待验证 | 通过 | 待验证（未专项测试） |
| VR-007 | 断网冷启动与游玩 | 不适用 | 不适用 | 通过 | 待验证（未专项测试） |
| VR-008 | 4v4 性能压力场景 | 不适用 | 待验证 | 通过 | 待验证（未专项测试；Neo3 卡顿已登记 TD-011） |

状态说明（2026-08-13 M00-T004 更新）：

- 文件层通过：`BP_XRPawn`、`BP_GrabComponent`、`BP_TeleportVisualizer`、手部/抓取/移动/瞬移输入资产（`IMC_Hands/Default`、`IA_Move/Turn/Grab_*`）、`SK_MannequinsXR` 均存在。
- 编辑器层通过：OpenXR、OpenXREyeTracker、OpenXRHandTracking、PICOController、EnhancedInput 插件运行中全部启用；OpenXR `xrCreateInstance succeeded`。
- Android 构建通过：UE5.6 BuildCookRun BUILD SUCCESSFUL，APK 产物 `ArchivedBuilds\Android\VRSanguoYanWuchang-arm64.apk`。
- 真机通过（2026-08-13）：swapchain 补丁生效、场景渲染可见；输入映射按 PICO 官方文档绑定 5 个 IMC 全部生效；VRPawn 挂载 `SM_PICONeo3_L/R` 手柄模型、隐藏骨骼手部（实例实测 bVisible=False）；手柄模型碰撞改为 NoCollision 修复 SpawnActor 失败；真机确认手柄单独显示、操作可用。日志无 SpawnActor 失败。
- 待验证项（VR-006/007/008）未做专项测试，保持待验证，不得包装为通过。
- 遗留：Neo3 真机卡顿（TD-011），待 T006 性能门禁定位优化。

证据统一登记到 `../registers/09-verification-register.md`。
