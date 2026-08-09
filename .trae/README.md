# 项目 AI 资料中心

本目录是 `VRSanguoYanWuchang` 的治理、知识、工程指引、执行与审计唯一入口。

## 有效入口

- [治理总索引](index.md)
- [四份治理契约](index.md#四份治理契约)
- [四份操作模型](index.md#四份操作模型)
- [权威项目规则](rules/project_rules.md)
- [唯一项目 Skill](skills/three-kingdoms-vr-arena/SKILL.md)
- [产品总纲](knowledge/GameMasterPlan.md)
- [Design 权威产品详规](knowledge/Design/index.md)
- [Standards 工程标准](standards/index.md)
- [VR 工程标准](vr/index.md)
- [Systems 工程实现指引](systems/index.md)
- [Execution 计划与 active 门禁](execution/README.md)
- [Registers 状态登记](registers/index.md)
- [标准完善待办](registers/standards-backlog.md)
- [变更记录](CHANGELOG.md)

## 目录职责

- `governance/`：治理契约与会话操作模型。
- `rules/`：唯一权威项目规则，入口为 `rules/project_rules.md`。
- `knowledge/`：产品总纲、权威产品详规、生产与技术知识。
- `standards/`：工程标准入口，按里程碑和真实证据逐步完善。
- `vr/`：OpenXR、输入、舒适度与设备验证标准。
- `systems/`：工程实现指引，链接 Design 权威详规，不复制产品规则。
- `execution/`：M00-M06 计划、active 五件套、任务包与报告。
- `registers/`：决策、风险、依赖、资产、验证、问题与标准完善状态。
- `archive/`：仅供审计的历史资料。
- `skills/three-kingdoms-vr-arena/SKILL.md`：项目唯一可发现 Skill。

## 当前执行状态

当前任务为 `M00-T004`，状态为 `blocked`（2026-08-10 更新）。Step 1-3 编辑器 VR 核验已通过（V-004）；Android 工具链与 APK 构建成功；PICO Neo3 真机验证 V-005 失败（UE5.8 与 Neo3 OpenXR 运行时硬不兼容），工程配置对 PICO 4+ 可直接运行；阻塞原因：待用户决策换设备或降级引擎。
