# Execution 索引

## 里程碑

| 里程碑 | 目标 | 文件 |
|---|---|---|
| M00 | 项目基线与自动化骨架 | [`M00-Foundation.md`](M00-Foundation.md)，[`T001-T006`](M00/README.md) |
| M01 | 1v1 核心战斗技术切片 | [`M01-CombatSlice.md`](M01-CombatSlice.md) |
| M02 | 五武器、混合移动与全身 IK | [`M02-PlayerSystems.md`](M02-PlayerSystems.md) |
| M03 | N 对 N、兵种与 3v3 默认战 | [`M03-SquadCombat.md`](M03-SquadCombat.md) |
| M04 | 生涯、自定义、训练与存档 | [`M04-GameModes.md`](M04-GameModes.md) |
| M05 | 三国内容、武将与完整生产替换 | [`M05-ContentComplete.md`](M05-ContentComplete.md) |
| M06 | 4v4 优化、发布候选与首发验收 | [`M06-Release.md`](M06-Release.md) |

## 执行基线

- [任务包模板（代码）](task-template.md)
- [任务包模板（资产）](task-template-asset.md)
- [任务包模板（关卡）](task-template-level.md)
- 当前活动任务：见 `active/STATUS.json`（任务包位于 `active/{taskId}/` 子目录下）
- M00 正式任务详规：`M00/`
- [变更请求模板](../governance/change-request-template.md)
- [任务报告](reports/tasks/README.md)

## 任务包目录结构

每个活动任务位于 `active/{taskId}/` 子目录下，包含五件套：

| 文件 | 用途 |
|---|---|
| `TASK.md` | 任务定义：目标、范围、步骤、停止条件、回退和报告路径 |
| `ALLOWLIST.txt` | 允许修改的路径列表（相对于项目根目录 `VRSanguoYanWuchang/`） |
| `INPUTS.md` | 前置输入：所需事实源与输入文件 |
| `CHECKS.md` | 验证检查：验证方法、门禁条件和禁止事项 |
| `STATUS.json` | 动态状态副本（根 `active/STATUS.json` 为唯一权威，此为便利副本） |

决策模型生成任务时创建全部五个文件；执行模型认领前必须逐份检查完整性。

M01 的 1v1 是底层验证，不是一期开售范围。任何里程碑裁剪都不得改变 [`../knowledge/GameMasterPlan.md`](../knowledge/GameMasterPlan.md) 的完成定义。

Git 已安装并推送远程（2026-08-09 用户确认），`origin/master` 与本地同步；后续提交遵循 `../standards/10-git-standard.md`。
