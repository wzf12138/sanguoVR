# Systems 工程实现指引索引

本目录是系统的工程实现指引，描述职责边界、接口方向、状态组织、诊断与落地注意事项。产品规则、玩法能力、数值和验收口径以 [`../knowledge/Design/index.md`](../knowledge/Design/index.md) 中对应权威产品详规为准；系统文件只链接和转译工程边界，不复制产品规则。

| 工程实现指引 | 对应权威产品详规 |
|---|---|
| [`01-game-flow-system.md`](01-game-flow-system.md) | [`GameModesAndProgression.md`](../knowledge/Design/GameModesAndProgression.md) |
| [`02-interaction-and-weapon-system.md`](02-interaction-and-weapon-system.md) | [`WeaponsAndInteraction.md`](../knowledge/Design/WeaponsAndInteraction.md)、[`CombatSystem.md`](../knowledge/Design/CombatSystem.md) |
| [`03-combat-resolution-system.md`](03-combat-resolution-system.md) | [`CombatSystem.md`](../knowledge/Design/CombatSystem.md)、[`HealthAndArmor.md`](../knowledge/Design/HealthAndArmor.md) |
| [`04-movement-system.md`](04-movement-system.md) | [`MovementAndFullBodyIK.md`](../knowledge/Design/MovementAndFullBodyIK.md) |
| [`05-ai-combat-system.md`](05-ai-combat-system.md) | [`SquadAI.md`](../knowledge/Design/SquadAI.md)、[`CombatSystem.md`](../knowledge/Design/CombatSystem.md) |
| [`06-arena-tutorial-ui-system.md`](06-arena-tutorial-ui-system.md) | [`GameModesAndProgression.md`](../knowledge/Design/GameModesAndProgression.md) |
| [`07-save-telemetry-and-diagnostics-system.md`](07-save-telemetry-and-diagnostics-system.md) | [`GameModesAndProgression.md`](../knowledge/Design/GameModesAndProgression.md) |

若工程指引与 Design 详规冲突，停止实现并按治理权威链处理；不得在本目录直接改写产品规则。

## 系统总览

以下为 M00 基线期规划的系统职责划分；`CharacterState` 与 `FullBodyIK` 不单独立文件，分别并入 03 与 04 的工程边界。各系统 M00 状态均为规划，具体实现以待批准任务为准。

| 系统 | 职责 | 主要数据 | 对应指引 | M00 状态 |
|---|---|---|---|---|
| Combat | 攻防判定、伤害请求、硬直与命中去重 | Attack/Hit/Defense Result | 03 | 规划 |
| Weapon | 抓取、持有、武器轨迹、类别能力 | Weapon Definition | 02 | 规划 |
| CharacterState | 生命、护甲、姿态、失能与阵营 | Character State | 03 | 规划 |
| Movement | 平滑移动、战术瞬移、转向、落点校验 | Movement Profile | 04 | 规划 |
| FullBodyIK | HMD/手柄到全身化身映射与校准 | Avatar Profile | 04 | 规划 |
| SquadAI | 小队决策、角色分工、目标与公平性 | Unit/Commander Definition | 05 | 规划 |
| GameModeFlow | 准备、比赛、结算、训练与存档流程 | Match Rule Set | 01 | 规划 |
| Diagnostics | 日志、指标、调试可视化和性能采样 | Diagnostic Snapshot | 07 | 规划 |

## 模块依赖边界

推荐依赖方向：`Input/AI Adapter → Character Capability API → Combat/Weapon/Movement/State → Presentation/Audio/FX/UI`。

- Combat 不读取具体按键，不直接控制 UI。
- Weapon 提供几何、轨迹和能力，不自行决定比赛胜负。
- CharacterState 是生命、护甲和失能状态事实源。
- Movement 不修改伤害规则；瞬移通过能力与比赛规则校验。
- FullBodyIK 只解决表现与命中代理映射，不成为生命和比赛状态事实源。
- SquadAI 通过同一角色能力 API 行动，不绕过体力、硬直和武器规则。
- GameModeFlow 编排系统，不复制各系统内部结算。
- Diagnostics 可观察所有系统，但不得改变正式规则状态。

## 数据资产目录

数据资产具体字段标准见 [`../standards/04-data-asset-standard.md`](../standards/04-data-asset-standard.md)；本目录只登记类名、前缀与关键字段的工程约定。所有数据资产必须有稳定 ID、版本字段、默认值和校验函数；运行时不得依赖资产显示名作为永久 ID。

| 类型 | 建议类名 | 资产前缀 | 关键字段 |
|---|---|---|---|
| 武器定义 | `UVRWeaponDefinition` | `DA_Weapon_` | 类别、质量、抓点、伤害曲线、反馈 |
| 护甲定义 | `UVRArmorDefinition` | `DA_Armor_` | 部位、防护、耐久、破损 |
| 兵种定义 | `UVRUnitDefinition` | `DA_Unit_` | 职责、装备、行为参数 |
| 武将定义 | `UVRCommanderDefinition` | `DA_Commander_` | 身份、风格、能力、语音 |
| 比赛规则 | `UVRMatchRuleSet` | `DA_Match_` | 队伍规模、胜负、时间、重生 |
| 移动配置 | `UVRMovementProfile` | `DA_Move_` | 速度、转向、瞬移与舒适度 |
| 化身配置 | `UVRAvatarProfile` | `DA_Avatar_` | 骨骼、身高、IK 与命中代理 |
