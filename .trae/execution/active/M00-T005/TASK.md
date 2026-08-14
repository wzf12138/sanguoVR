# M00-T005 系统骨架与数据驱动边界

- 任务编号：M00-T005
- 状态：见 `STATUS.json`
- 里程碑：M00
- 优先级：P0
- 前置任务：M00-T004（VR/OpenXR/PICO 基线，当前 awaiting_review）
- 预估耗时：~7h

## 目标

建立 Combat、Weapon、CharacterState、Movement、FullBodyIK、SquadAI、GameModeFlow 与 Diagnostics 的最小代码边界。这是后续所有战斗/武器/移动/AI 代码的脚手架。

接口签名以 `systems/01-07` 接口契约为强制约束，类名和文件名遵循 `standards/02` 命名标准。

## 实施步骤

详细步骤见 `.trae/execution/M00/T005-SystemSkeleton.md`。

| Step | 内容 | 预估 |
|------|------|------|
| 1 | 公共类型与日志分类（VRTypes.h, VRLogChannels.h, VRGameplayTags.h） | 1h |
| 2 | 七项核心接口（Interfaces/ 下，签名对齐 standards/05 + systems 契约） | 1h |
| 3 | 八个 Data Asset 基类（Data/ 下，类名对齐 systems/index + standards/04） | 1.5h |
| 4 | 游戏流程状态机（VRGameFlowComponent，对齐 systems/01 契约） | 1.5h |
| 5 | 角色能力适配组件（VRCharacterCapabilityComponent） | 1h |
| 6 | 空场景与测试角色（L_SkeletonTest, VRTestDummy） | 1h |

## 停止条件

- 编译失败且无法在 3 次重试内修复
- 需要修改 T004 白名单内的文件（Source/ 等，防止并发冲突）
- 发现 UE 5.6 编译器不兼容的语法
- 模板 Pawn 子类化后抓取/瞬移在 PIE 中失效且无法恢复
- 接口签名与 systems/01-07 接口契约存在无法消解的冲突

## 回退

- 删除本任务创建的 Source/ 和 Content/ 文件
- 还原 `VRSanguoYanWuchang.cpp` 中新增的日志注册代码

## 报告路径

`.trae/execution/reports/tasks/M00-T005.md`
