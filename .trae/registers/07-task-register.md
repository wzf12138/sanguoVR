# 任务登记

本登记册跟踪项目任务的状态与交付物；任务目标、白名单、禁区、停止条件与报告路径以 `.trae/execution/active/` 对应任务包为准，本表不复制任务细节。

| 任务 | 名称 | 状态 | 交付物 |
|---|---|---|---|
| M00-T001 | 治理与事实源基线 | 部分验证（V-001 已确认，V-007 ACL 待管理员） | governance、rules、索引、登记册 |
| M00-T002 | Git 与仓库基线 | 已验证（Git 安装、仓库初始化与推送完成，2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig`；Git for Windows + Git LFS 已安装（用户执行）；仓库已初始化并推送远程 |
| M00-T003 | UE5.8 工程与工具链基线 | 已验证（approved，编译成功） | 编译成功、编辑器启动验证通过、MCP 连通性已记录 |
| M00-T004 | VR/OpenXR/PICO 基线 | approved（2026-08-13：真机验收通过，审核批准；遗留 Neo3 卡顿 TD-011） | Step 1-3 编辑器核验已完成（UE5.8）；UE5.6 迁移完成：项目重建、PICO 插件迁移至项目 Plugins、swapchain 补丁编译生效、Neo3 真机场景可见；2026-08-12 输入映射按 PICO 官方文档绑定（5 个 IMC 全部配置 PICO Neo3 键）；2026-08-13 VRPawn 挂载 SM_PICONeo3_L/R 手柄模型、隐藏骨骼手部、修复手柄模型碰撞导致的 SpawnActor 失败（均经 MCP 自动化 + 真机验证）；遗留：Neo3 卡顿性能优化 |
| M00-T005 | 系统骨架与数据驱动边界 | in_progress（2026-08-13：Step 1-6 完成，待 PIE 运行验证） | 公共类型/8 日志分类/11 GameplayTag（Core/）；7 接口（Interfaces/）；8 Data Asset 基类（Data/，SchemaVersion+PostLoad+ValidateData）；流程状态机 VRGameFlowComponent；能力适配组件 VRCharacterCapabilityComponent；TestDummy + L_SkeletonTest 关卡（VRTestDummy+Floor，落盘验证 12223B）；编译通过（13 动作 Succeeded）；工程修复：.uproject 补 Modules、Build.cs 加 GameplayTags+AIModule（均用户批准）；报告 `execution/reports/tasks/M00-T005.md` |
| M00-T006 | 自动化、诊断与交付门禁 | ready（2026-08-13 修订：原"已批准"纠正为 ready，V-006 待验证、Source 无测试文件、无活动任务包。详规扩充为 6 步可执行方案，M01 范围交付物 deferred） | 自动化测试、日志验证、构建门禁、性能基线 |
| M00-DOC-001 | 治理文档最终收口 | approved | 合并重复事实源、迁移引用、删除清单与完整性报告 |
| M01-T005 | 灰盒竞技场关卡 | in_progress（2026-08-13：审核打回，待 PIE/真机性能验证） | 1v1 测试场景 `Content/VRSanguo/Dev/L_Prototype_1v1.umap`、NavMesh、灰盒布局、尺寸标注 |
| M02-PREP-001 | M02 资产生成准备与平台选型 | in_progress（2026-08-13：审核 requires_changes。规格定稿，剩余 Step 2 参考图片收集，继续在本任务下完成后重新提交审核） | 平台选型、骨架/武器/动画规格、美术参考 |

任务进入 `approved` 前由用户或授权审批人验收；状态变化同步 `.trae/CHANGELOG.md` 与本表。
