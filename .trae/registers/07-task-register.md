# 任务登记

本登记册跟踪项目任务的状态与交付物；任务目标、白名单、禁区、停止条件与报告路径以 `.trae/execution/active/` 对应任务包为准，本表不复制任务细节。

| 任务 | 名称 | 状态 | 交付物 |
|---|---|---|---|
| M00-T001 | 治理与事实源基线 | 部分验证（V-001 通过，V-007 ACL 待管理员） | governance、rules、索引、登记册 |
| M00-T002 | Git 与仓库基线 | 已验证（Git 安装、仓库初始化与推送完成，2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig`；Git for Windows + Git LFS 已安装（用户执行）；仓库已初始化并推送远程 |
| M00-T003 | UE5.8 工程与工具链基线 | 已验证（approved，编译成功） | 编译成功、编辑器启动验证通过、MCP 连通性已记录 |
| M00-T004 | VR/OpenXR/PICO 基线 | in_progress（2026-08-12：编辑器验证通过，真机验证中） | Step 1-3 编辑器核验已完成（UE5.8）；UE5.6 迁移执行中：项目重建、PICO 插件迁移至项目 Plugins、swapchain 补丁编译生效、Neo3 真机场景可见；2026-08-12 输入映射按官方文档绑定（IMC_Default/Hands/Menu/Weapon×2 全部配置 PICO Neo3 键）；遗留：VRPawn 挂载 Neo3 手柄模型（StaticMesh 组件）、OpenXR Input PlayerMappableInputConfig、真机复测输入 |
| M00-T005 | 系统骨架与数据驱动边界 | ready（2026-08-11：T004 阻塞期间并发启动） | 系统目录、接口与数据资产骨架 |
| M00-T006 | 自动化、诊断与交付门禁 | 已批准 | 测试、日志、性能和构建门禁 |
| M00-DOC-001 | 治理文档最终收口 | approved | 合并重复事实源、迁移引用、删除清单与完整性报告 |

任务进入 `approved` 前由用户或授权审批人验收；状态变化同步 `.trae/CHANGELOG.md` 与本表。
