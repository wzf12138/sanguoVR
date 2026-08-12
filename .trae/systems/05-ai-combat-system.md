# AI 战斗系统工程实现指引

N 对 N 编队、兵种、难度与公平性规则以 [`../knowledge/Design/SquadAI.md`](../knowledge/Design/SquadAI.md) 为权威产品详规，战斗动作约束见 [`../knowledge/Design/CombatSystem.md`](../knowledge/Design/CombatSystem.md)。本文件只描述 AI 工程分层。

## 工程职责

- 分离感知快照、战术评分、动作执行与小队协调。
- 通过统一武器、移动和战斗接口执行动作。
- 管理决策频率、动作承诺、冷却、中断和恢复。
- 输出可审计的候选评分、选择原因与动作结果。

## 实现边界

AI 只消费接口提供的当前可感知事实，不读取未来输入或绕过战斗状态。等级、兵种、装备和个体特征以数据组合，不复制行为树主干。小队协调不得直接修改个体战斗结算。

## 接口契约（规划级）

以下为 M00 规划阶段的接口契约框架，具体签名在 M00-T005 C++ 骨架中实现并以此为准。

**分层架构**：
1. 感知层：`UpdatePerception(AActor* Self, const FWorldSnapshot& Snapshot)` → `FAIPerceptionSnapshot`
2. 战术层：`EvaluateTactics(const FAIPerceptionSnapshot& Perception)` → `FTacticDecision`
3. 执行层：`ExecuteAction(const FTacticDecision& Decision)` → `EAIActionResult`

**核心服务**：
- `UpdateSquadTactics(int32 TeamId, const FWorldSnapshot& Snapshot)` → 小队级目标分配
- `CommitAction(int32 UnitId, const FAIAction& Action)` → `bool`

**事件广播**：
- `OnAIActionCommitted(int32 UnitId, const FAIAction& Action)`
- `OnAIInterrupted(int32 UnitId, EAIInterruptReason Reason)`

**数据结构**：
- `FAIPerceptionSnapshot`：`TArray<FPerceivedUnit> Allies; TArray<FPerceivedUnit> Enemies; float AlertLevel;`
- `FTacticDecision`：`EAIActionType ActionType; AActor* Target; FVector MoveDestination; float Priority;`
- `EAIActionType`：`Attack | Block | Move | Flank | Guard | Retreat | SwitchWeapon`

**依赖接口**：
- 统一角色能力 API（DEC-011）：通过 `ICharacterCapability` 接口执行攻击、格挡、移动
- Weapon: `GetOwnedWeapon()`
- Movement: `RequestMovement()`
- Diagnostics: 输出决策评分和选择原因

## 接口与验证

感知数据使用稳定快照，动作执行等待提交点或明确反馈后再决策。验证覆盖不同帧率、多人目标切换、武器差异、中断恢复、无效信息隔离、调试可追踪性和压力场景；具体行为规则从权威详规读取。
