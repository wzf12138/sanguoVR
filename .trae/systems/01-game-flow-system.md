# 游戏流程系统工程实现指引

产品模式、流程规则、结算与存档口径以 [`../knowledge/Design/GameModesAndProgression.md`](../knowledge/Design/GameModesAndProgression.md) 为权威产品详规。本文件只描述工程实现边界，不复制玩法规则。

## 工程职责

- 维护会话阶段状态机及合法迁移。
- 编排校准、准备、生成、战斗、结算与重置服务。
- 统一门控输入、伤害、AI 决策和重复提交。
- 汇总各系统事件，不在流程层计算伤害或选择 AI 战术。

## 实现边界

流程状态使用单一所有者；阶段切换必须可追踪、可中止并支持幂等重置。生成、计时、异步加载和临时对象通过明确生命周期管理，失败时返回安全状态并提供诊断原因。

## 接口契约（规划级）

以下为 M00 规划阶段的接口契约框架，具体签名在 M00-T005 C++ 骨架中实现并以此为准。

**状态机**：
- 枚举 `EGameSessionPhase`：`Calibration | Ready | Generate | Combat | Settlement | Reset`
- 状态迁移必须经过 `RequestPhaseTransition(EGameSessionPhase Target)` 统一入口

**核心服务**：
- `StartMatch(const FMatchRuleSet& Rules)` → `bool`（成功进入 Ready）
- `EndMatch(EMatchEndReason Reason)` → 触发 Settlement
- `ResetMatch()` → 幂等重置，清理所有临时对象

**事件广播**：
- `OnPhaseChanged(EGameSessionPhase Old, EGameSessionPhase New)`
- `OnMatchEnded(EMatchEndReason Reason, const FMatchResult& Result)`

**依赖接口**（本系统调用其他系统）：
- Combat: `ResolveAttack()`
- AI: `UpdateSquadTactics()`
- Movement: `RequestMovement()`
- Save: `SaveMatchResult()`

## 接口与验证

依赖战斗、AI、交互、移动、UI 和保存系统的事件或服务接口，不直接写入其内部状态。验证覆盖合法迁移、重复结束、连续重开、加载失败、XR 失焦和输入失联；具体产品结果以权威详规为准。
