# 任务登记

本登记册跟踪项目任务的状态与交付物；任务目标、白名单、禁区、停止条件与报告路径以 `.trae/execution/active/` 对应任务包为准，本表不复制任务细节。

| 任务 | 名称 | 状态 | 交付物 |
|---|---|---|---|
| M00-T001 | 治理与事实源基线 | 已验证（ACL 待管理员应用） | governance、rules、索引、登记册 |
| M00-T002 | Git 与仓库基线 | 已实施（Git 安装、仓库初始化与推送完成，2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig`；Git for Windows + Git LFS 已安装（用户执行）；仓库已初始化并推送远程 |
| M00-T003 | UE5.8 工程与工具链基线 | approved | 编译成功、编辑器启动验证通过、MCP 连通性已记录 |
| M00-T004 | VR/OpenXR/PICO 基线 | blocked（V-005 真机验证失败，设备不兼容，待用户决策换设备或降级引擎） | Step 1-3 编辑器 VR 核验已通过（V-004）；Android 工具链与 APK 构建成功；PICO Neo3 真机验证失败（UE5.8 与 Neo3 OpenXR 运行时硬不兼容），配置对 PICO 4+ 可直接运行；详见 `TechnicalDecisions.md`、`DeviceConfigurationMatrix.md` |
| M00-T005 | 系统骨架与数据驱动边界 | 已批准 | 系统目录、接口与数据资产骨架 |
| M00-T006 | 自动化、诊断与交付门禁 | 已批准 | 测试、日志、性能和构建门禁 |
| M00-DOC-001 | 治理文档最终收口 | approved | 合并重复事实源、迁移引用、删除清单与完整性报告 |

任务进入 `approved` 前由用户或授权审批人验收；状态变化同步 `.trae/CHANGELOG.md` 与本表。
