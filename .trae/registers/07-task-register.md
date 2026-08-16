# 任务登记

本登记册跟踪项目任务的状态与交付物；任务目标、白名单、禁区、停止条件与报告路径以 `.trae/execution/active/` 对应任务包为准，本表不复制任务细节。

| 任务 | 名称 | 状态 | 交付物 |
|---|---|---|---|
| M00-T001 | 治理与事实源基线 | 部分验证（V-001 已确认，V-007 ACL 待管理员） | governance、rules、索引、登记册 |
| M00-T002 | Git 与仓库基线 | 已验证（Git 安装、仓库初始化与推送完成，2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig`；Git for Windows + Git LFS 已安装（用户执行）；仓库已初始化并推送远程 |
| M00-T003 | UE5.8 工程与工具链基线 | 已验证（approved，编译成功） | 编译成功、编辑器启动验证通过、MCP 连通性已记录 |
| M00-T004 | VR/OpenXR/PICO 基线 | approved（2026-08-13：真机验收通过，审核批准；遗留 Neo3 卡顿 TD-011） | Step 1-3 编辑器核验已完成（UE5.8）；UE5.6 迁移完成：项目重建、PICO 插件迁移至项目 Plugins、swapchain 补丁编译生效、Neo3 真机场景可见；2026-08-12 输入映射按 PICO 官方文档绑定（5 个 IMC 全部配置 PICO Neo3 键）；2026-08-13 VRPawn 挂载 SM_PICONeo3_L/R 手柄模型、隐藏骨骼手部、修复手柄模型碰撞导致的 SpawnActor 失败（均经 MCP 自动化 + 真机验证）；遗留：Neo3 卡顿性能优化 |
| M00-T005 | 系统骨架与数据驱动边界 | approved（2026-08-15：审核批准。CHECKS 修正后全部通过，M01 接管运行时验证+VRPawn 挂载） | 22 个 C++ 文件编译通过；7 接口/8 DA/状态机/能力组件/TestDummy + L_SkeletonTest 关卡 |
| M00-T006 | 自动化、诊断与交付门禁 | awaiting_review（2026-08-16：执行完成，12/12 测试通过；Android 门禁遗留） | 6 个自动化测试文件（VRDataAssetSpec/VRInterfaceSpec/VRGameFlowSpec）；12/12 通过（8 DA + 2 GameFlow + 2 接口）；8 日志分类验证；性能基线（stat 命令 + LogVRSanguoPerf）；场景规划初版（1v1/武器训练/4v4）；Win64 门禁通过；工具链修复：UEBridgeMCP bUseUnity=false（用户批准）、VRExpansionPlugin 换官方 5.6-Locked（用户指示）；报告 `execution/reports/tasks/M00-T006.md` |
| M00-DOC-001 | 治理文档最终收口 | approved | 合并重复事实源、迁移引用、删除清单与完整性报告 |
| M01-T005 | 灰盒竞技场关卡 | in_progress（2026-08-13：审核打回，待 PIE/真机性能验证） | 1v1 测试场景 `Content/VRSanguo/Dev/L_Prototype_1v1.umap`、NavMesh、灰盒布局、尺寸标注 |
| M02-PREP-001 | M02 资产生成准备与平台选型 | in_progress（2026-08-13：审核 requires_changes。规格定稿，剩余 Step 2 参考图片收集，继续在本任务下完成后重新提交审核） | 平台选型、骨架/武器/动画规格、美术参考 |
| M01-T001 | 武器抓取与 VRE 集成 | ready（2026-08-16：任务包已生成） | BP_WeaponBase 蓝图、HandSocket 握持姿势、BP_TestSword 测试武器 |

任务进入 `approved` 前由用户或授权审批人验收；状态变化同步 `.trae/CHANGELOG.md` 与本表。
