# 战斗结算系统工程实现指引

攻击、格挡、伤害、硬直与解卡规则以 [`../knowledge/Design/CombatSystem.md`](../knowledge/Design/CombatSystem.md) 为权威产品详规，生命与分部位护甲口径以 [`../knowledge/Design/HealthAndArmor.md`](../knowledge/Design/HealthAndArmor.md) 为准。本文件只描述结算管线的工程组织。

## 工程职责

- 维护攻击实例、阶段和连续轨迹采样。
- 将接触候选归一为单一结算请求与结构化结果。
- 提供攻击内去重、多碰撞体合并和规则数据入口。
- 将结算结果发布给生命护甲、反馈、AI、统计和诊断系统。

## 实现边界

规则结算由单一服务拥有；碰撞体、动画、音效和 UI 不得直接改写伤害或胜负。攻击标识、来源、目标、部位和结果需可追踪。解卡属于接触约束恢复，不生成额外伤害。

## 接口契约（规划级）

以下为 M00 规划阶段的接口契约框架，具体签名在 M00-T005 C++ 骨架中实现并以此为准。

**核心服务**：
- `ResolveAttack(const FAttackRequest& Request)` → `FCombatResult`
- `ResolveDefense(const FDefenseRequest& Request)` → `FDefenseResult`
- `RegisterAttackInstance(const FAttackInstance& Instance)` → `int32 AttackId`

**事件广播**：
- `OnHitDealt(const FHitResultData& HitData)`
- `OnHitBlocked(const FBlockResultData& BlockData)`
- `OnStaggerApplied(AActor* Target, float Duration)`
- `OnUnstuckTriggered(AActor* Weapon, AActor* Obstacle)`

**数据结构**：
- `FAttackRequest`：`int32 AttackId; AActor* Source; AActor* Target; FWeaponTrajectorySample Trajectory; EHitZone Zone;`
- `FCombatResult`：`ECombatOutcome Outcome; float Damage; bool bWasBlocked; int32 HitZoneFlags;`
- `ECombatOutcome`：`Miss | Hit | Blocked | Deflected | Parried`
- `EHitZone`：`Head | Torso | LeftArm | RightArm | LeftLeg | RightLeg`

**依赖接口**：
- CharacterState（并入本系统）：`ApplyDamage(AActor* Target, float Amount)`
- Weapon: `GetTrajectorySource()`
- Diagnostics: 发布结算结果用于调试可视化

## 接口与验证

输入只包含当前可观测的攻击与防御事实，输出为不可歧义的结果类型及数值载荷。验证覆盖高低帧率轨迹、重复碰撞、同时接触、格挡边界、部位映射、软锁恢复与结果重放一致性；具体规则从权威详规读取。
