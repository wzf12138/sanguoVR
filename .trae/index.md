# VRSanguoYanWuchang 项目治理索引

项目治理根目录：`D:/AWork/Unreal/Project/VRSanguoYanWuchang/.trae`

## 根文件

- [README](README.md)
- [manifest.yaml](manifest.yaml)
- [integrity.yaml](integrity.yaml)
- [变更记录](CHANGELOG.md)

## 四份治理契约

1. [集中式治理政策](governance/policy.md)
2. [集中式变更请求模板](governance/change-request-template.md)
3. [集中式完成定义](governance/definition-of-done.md)
4. [集中式职责边界](governance/responsibility-matrix.md)

## 四份操作模型

1. [决策模型](governance/DecisionModel.md)
2. [执行模型](governance/ExecutionModel.md)
3. [审核协议](governance/ReviewProtocol.md)
4. [新会话短指令](governance/SessionCommands.md)

## 规则与唯一 Skill

- [权威项目规则](rules/project_rules.md)
- [three-kingdoms-vr-arena](skills/three-kingdoms-vr-arena/SKILL.md)

`rules/project_rules.md` 是唯一项目规则入口。`.trae/skills/` 下不得创建第二个带 YAML frontmatter 的 `SKILL.md`。

## 产品与工程入口

- [知识库总入口](knowledge/README.md)（技术决策、环境配置、构建指南、设备配置矩阵、引擎技术参考、实现模式库等）
- [引擎技术参考](knowledge/EngineReference.md)（VR/OpenXR/Enhanced Input/IK/性能/AI/碰撞）
- [实现模式库](knowledge/Patterns/README.md)（可复用实现模式，M01+ 逐步填充）
- [产品总纲](knowledge/GameMasterPlan.md)
- [Design 权威产品详规](knowledge/Design/index.md)
- [Standards 工程标准](standards/index.md)
- [VR 工程标准](vr/index.md)
- [Systems 工程实现指引](systems/index.md)
- [Registers 状态登记](registers/index.md)
- [M00-M06 标准完善待办](registers/standards-backlog.md)

Systems 只描述工程实现边界，产品规则以 `knowledge/Design/` 对应详规为准。

## Execution 基线

- [Execution 索引](execution/README.md)
- [任务包模板（代码）](execution/task-template.md)
- [任务包模板（资产）](execution/task-template-asset.md)
- [任务包模板（关卡）](execution/task-template-level.md)
- [变更请求模板](governance/change-request-template.md)
- [active 状态](execution/active/STATUS.json)
- [M00-T004 任务包](execution/active/M00-T004/)
- [M00-T005 任务包](execution/active/M00-T005/)
- [M00 正式任务详规](execution/M00/)

当前 active 任务与状态以 [`execution/active/STATUS.json`](execution/active/STATUS.json) 为唯一权威，此处不复制动态状态；任务进度历史见 `registers/07-task-register.md`。active 五件套位于各任务子目录 `active/{taskId}/` 下。

## M00-M06

| 里程碑 | 入口 |
|---|---|
| M00 | [项目基线与自动化骨架](execution/M00-Foundation.md) |
| M01 | [1v1 核心战斗技术切片](execution/M01-CombatSlice.md) |
| M02 | [五武器、混合移动与全身 IK](execution/M02-PlayerSystems.md) |
| M03 | [N 对 N、兵种与默认 3v3](execution/M03-SquadCombat.md) |
| M04 | [生涯、自定义、训练与存档](execution/M04-GameModes.md) |
| M05 | [三国内容、武将与生产替换](execution/M05-ContentComplete.md) |
| M06 | [4v4 优化与发布验收](execution/M06-Release.md) |

## 路径与验证约束

- 本项目资料只在 `D:/AWork/Unreal/Project/VRSanguoYanWuchang/.trae` 内维护。
- `D:/AWork/Unreal/Project/.trae` 不属于本项目，不得写入。
- Git 状态：已于 2026-08-09 安装 Git for Windows + Git LFS，仓库已初始化并推送远程（用户确认）；完整记录见 `CHANGELOG.md` 与 `knowledge/EnvironmentSetup.md`。
- 完整性结果以实际绝对路径读取、链接检查和 active 门禁检查为准。
