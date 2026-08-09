# 任务登记

本登记册跟踪项目任务的状态与交付物；任务目标、白名单、禁区、停止条件与报告路径以 `.trae/execution/active/` 对应任务包为准，本表不复制任务细节。

| 任务 | 名称 | 状态 | 交付物 |
|---|---|---|---|
| M00-T001 | 治理与事实源基线 | 已验证（ACL 待管理员应用） | governance、rules、索引、登记册 |
| M00-T002 | Git 与仓库基线 | 已实现未验证 | `.gitignore`、`.gitattributes`、`.editorconfig`、`.lfsconfig` |
| M00-T003 | UE5.8 工程与工具链基线 | approved | 编译成功、编辑器启动验证通过、MCP 连通性已记录 |
| M00-T004 | VR/OpenXR/PICO 基线 | ready | Step 1-3 编辑器核验已完成；可继续 Android SDK、UE Android 配置、Launch on Device 与 Standalone APK 真机验证 |
| M00-T005 | 系统骨架与数据驱动边界 | 已批准 | 系统目录、接口与数据资产骨架 |
| M00-T006 | 自动化、诊断与交付门禁 | 已批准 | 测试、日志、性能和构建门禁 |
| M00-DOC-001 | 治理文档最终收口 | approved | 合并重复事实源、迁移引用、删除清单与完整性报告 |

任务进入 `approved` 前由用户或授权审批人验收；状态变化同步 `.trae/CHANGELOG.md` 与本表。
