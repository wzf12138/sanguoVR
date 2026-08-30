# 任务登记

本登记册跟踪项目任务的状态与交付物；任务目标、白名单、禁区、停止条件与报告路径以 `.trae/execution/active/` 对应任务包为准，本表不复制任务细节。

| 任务 | 名称 | 状态 | 交付物 |
|---|---|---|---|
| M00-T001 | 治理与事实源基线 | 已验证（V-001、V-007 均确认；V-007 NTFS ACL 于 2026-08-26 由管理员执行并核验） | governance、rules、索引、登记册 |
| M00-T002 | Git 与仓库基线 | 已验证（Git 安装、仓库初始化与推送完成，2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig`；Git for Windows + Git LFS 已安装（用户执行）；仓库已初始化并推送远程 |
| M00-T003 | UE5.8 工程与工具链基线 | 已验证（approved，编译成功） | 编译成功、编辑器启动验证通过、MCP 连通性已记录 |
| M00-T004 | VR/OpenXR/PICO 基线 | approved（2026-08-13：真机验收通过，审核批准；遗留 Neo3 卡顿 TD-011） | Step 1-3 编辑器核验已完成（UE5.8）；UE5.6 迁移完成：项目重建、PICO 插件迁移至项目 Plugins、swapchain 补丁编译生效、Neo3 真机场景可见；2026-08-12 输入映射按 PICO 官方文档绑定（5 个 IMC 全部配置 PICO Neo3 键）；2026-08-13 VRPawn 挂载 SM_PICONeo3_L/R 手柄模型、隐藏骨骼手部、修复手柄模型碰撞导致的 SpawnActor 失败（均经 MCP 自动化 + 真机验证）；遗留：Neo3 卡顿性能优化 |
| M00-T005 | 系统骨架与数据驱动边界 | approved（2026-08-15：审核批准。CHECKS 修正后全部通过，M01 接管运行时验证+VRPawn 挂载） | 22 个 C++ 文件编译通过；7 接口/8 DA/状态机/能力组件/TestDummy + L_SkeletonTest 关卡 |
| M00-T006 | 自动化、诊断与交付门禁 | approved（2026-08-19：审核批准。12/12 测试通过、V-006 已验证；遗留场景规划表终版 M01 接管） | 6 个自动化测试文件（VRDataAssetSpec/VRInterfaceSpec/VRGameFlowSpec）；12/12 通过（8 DA + 2 GameFlow + 2 接口）；8 日志分类验证；性能基线（stat 命令 + LogVRSanguoPerf）；场景规划初版（1v1/武器训练/4v4）；Win64 与 Android 门禁通过（Android 含 APK 打包）；工具链修复：UEBridgeMCP bUseUnity=false（用户批准）、VRExpansionPlugin 换官方 5.6-Locked + SceneProxy override（用户批准）；报告 `execution/reports/tasks/M00-T006.md` |
| M00-DOC-001 | 治理文档最终收口 | approved | 合并重复事实源、迁移引用、删除清单与完整性报告 |
| M01-T001 | 武器抓取与 VRE 集成 | in_progress（2026-08-30 认领 session-20260830-001：自建 VRE 角色+GameMode 设为项目默认、握持 socket 复核、标记球附着修复；抓握键→GripObject 路线已决策（路线 A + Grip 键，TD-013 登记）；待用户 PICO 真机验证 TC-01~06） | BP_WeaponBase 蓝图、BP_TestSword、BP_VRCharacter、HandSocket 握持姿势、关卡放置、实施指南 `execution/reports/tasks/M01-T001.md` |
| M01-T002 | 伤害结算与命中保护 | 待生成 | 依赖：M01-T001 approved；预估：3h；交付：伤害组件、命中判定、防误伤保护、VRPawn 生命接口 |
| M01-T003 | 挥砍检测与格挡 | 待生成 | 依赖：M01-T002；预估：3h；交付：挥砍检测算法、格挡组件、轨迹采样与统一生命联动 |
| M01-T004 | 基础 AI 战斗 | 待生成 | 依赖：M01-T002；预估：4h；交付：AI 控制器、感知、行为树、攻击/格挡决策、TestDummy 升级 |
| M01-T005 | 灰盒竞技场关卡 | 执行中（2026-08-24 口径修正：TD-012 偿还未闭环——PICO 串流 VR 模式未自动切换、中文标注（待字体资产）、PIE 帧率（待串流解决）、Lightmass 烘焙（需 GUI）；2026-08-19 核心交付曾通过 VR Preview 补验，偿还完成后重新提交审批） | 1v1 测试场景 `Content/VRSanguo/Dev/L_Prototype_1v1.umap`、NavMesh、灰盒布局、VR Preview 验证 |
| M01-T006 | 1v1 测试流程 | 待生成 | 依赖：M01-T003, M01-T004；预估：2h；交付：1v1 自动测试流程、回放与判定、报告模板 |
| M01-T007 | Direct Preview 验证（TD-012） | 待生成 | 依赖：M01-T005；预估：1h；交付：Direct Preview 配置文档、TD-012 偿还结果记录、回归脚本 |
| M02-PREP-001 | M02 资产生成准备与平台选型 | approved（2026-08-24：验收通过，两附带条件闭环——CR-20260824-001 命名对齐实施关闭 + AST-009 关卡路径对齐 v2；证据 V-009） | 平台选型、骨架/武器/动画规格、美术参考 |

任务进入 `approved` 前由用户或授权审批人验收；状态变化同步 `.trae/CHANGELOG.md` 与本表。

> M01 规划任务说明：T002/T003/T004/T006/T007 已在 `execution/M01-CombatSlice.md` 中规划，待 T001 approved 后逐批生成任务包；当前以「待生成」状态进入登记册，看板按 planned 显示，T001 blocked 不阻塞其规划展示。
