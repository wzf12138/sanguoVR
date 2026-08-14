# M00-T005 系统骨架与数据驱动边界

- 状态：见 `../active/STATUS.json`（本详规不复制动态状态）
- 优先级：P0
- 前置任务：M00-T004（VR/OpenXR/PICO 基线，当前 awaiting_review；T005 不依赖 T004 真机验证完成）
- 目标：建立 Combat、Weapon、CharacterState、Movement、FullBodyIK、SquadAI、GameModeFlow 与 Diagnostics 的最小代码边界。

> **修订说明（2026-08-13）**：本详规对齐 2026-08-11 架构改版后的系统接口契约（`systems/01-07`）、事件与接口标准（`standards/05`）、Data Asset 标准（`standards/04`）和命名标准（`standards/02`）。原版本使用 `VRS` 前缀和旧接口签名，已全面替换为 `VR` 前缀和系统契约定义的签名。

---

## 这个任务在完整游戏开发中的位置

```
已完成：
  T001 治理基线 ✅ -> 项目怎么管，定了
  T002 Git 基线 ✅   -> 代码怎么存，定了
  T003 编译基线 ✅   -> UE5.6 编译通过、编辑器能跑、MCP 通了
  T004 VR/PICO 基线 ⏳ -> awaiting_review：UE5.6 迁移完成、真机验收通过、遗留卡顿

本任务 T005：
  搭 C++ 模块骨架、核心接口、Data Asset 基类、流程状态机和诊断日志
  ── 这是"后续所有战斗/武器/移动/AI 代码的脚手架"
  ── 接口签名以 systems/01-07 接口契约为准

之后：
  T006 自动化门禁 -> 测试框架
  M01 1v1 战斗切片 -> 开始做真正的战斗玩法
```

---

## 实施步骤

### Step 1：公共类型与日志分类

**新增文件**：

- `Source/VRSanguoYanWuchang/Public/Core/VRTypes.h` - 通用结构体与枚举
- `Source/VRSanguoYanWuchang/Private/Core/VRTypes.cpp` - 类型注册与静态校验
- `Source/VRSanguoYanWuchang/Public/Core/VRLogChannels.h` - 8 个日志分类声明
- `Source/VRSanguoYanWuchang/Private/Core/VRLogChannels.cpp` - 日志分类定义
- `Source/VRSanguoYanWuchang/Public/Core/VRGameplayTags.h` - 项目 GameplayTag 注册
- `Source/VRSanguoYanWuchang/Private/Core/VRGameplayTags.cpp` - Tag 注册实现

**核心枚举**（对齐 systems/01-07 接口契约）：

| 枚举 | 用途 | 值 | 契约来源 |
|------|------|----|----------|
| `EGameSessionPhase` | 游戏会话阶段 | Calibration, Ready, Generate, Combat, Settlement, Reset | systems/01 |
| `ECombatOutcome` | 战斗结算结果 | Miss, Hit, Blocked, Deflected, Parried | systems/03 |
| `EHitZone` | 命中部位 | Head, Torso, LeftArm, RightArm, LeftLeg, RightLeg | systems/03 |
| `EWeaponType` | 武器类别 | OneHandSword, Shield, TwoHandHeavy, Spear, Bow | GameMasterPlan |
| `EMovementMode` | 移动模式 | SmoothLocomotion, TacticalTeleport, None | systems/04 |
| `EMovementFailReason` | 移动失败原因 | None, BlockedByGeometry, BlockedByActor, OutOfRange, OnCooldown, Disabled | systems/04 |
| `EMovementState` | 移动状态 | Idle, Moving, Teleporting | systems/04, standards/05 |
| `EReleaseReason` | 武器释放原因 | Manual, Collision, Timeout, Reset | systems/02 |
| `EBattleOutcome` | 战斗胜负 | Victory, Defeat, Draw | standards/05 |
| `ECapabilityState` | 角色能力状态 | Idle, Attacking, Defending, Staggered, Dead | DEC-011 |
| `EMatchEndReason` | 比赛结束原因 | TimeExpired, TeamEliminated, UserAbort, Draw | systems/01 |
| `EHand` | 手部标识 | Left, Right | systems/02 |

**核心结构体**（对齐 systems/01-07 接口契约）：

| 结构体 | 用途 | 关键字段 | 契约来源 |
|--------|------|----------|----------|
| `FAttackRequest` | 攻击结算输入 | int32 AttackId; AActor* Source; AActor* Target; FWeaponTrajectorySample Trajectory; EHitZone Zone; | systems/03 |
| `FCombatResult` | 战斗结算输出 | ECombatOutcome Outcome; float Damage; bool bWasBlocked; int32 HitZoneFlags; | systems/03 |
| `FDefenseResult` | 防御结算结果 | bool bBlocked; float DeflectedAngle; bool bDeflected; | systems/03 |
| `FWeaponTrajectorySample` | 武器轨迹采样 | FVector Position; FVector Velocity; FQuat Rotation; float Timestamp; | systems/02 |
| `FMovementTarget` | 移动请求目标 | FVector Location; FRotator Rotation; bool bIsTeleport; | systems/04 |
| `FMovementResult` | 移动执行结果 | bool bSuccess; EMovementFailReason FailReason; FVector ActualLocation; | systems/04 |
| `FMatchRuleSet` | 比赛规则集 | int32 TeamSize; TArray<int32> AllowedSizes; int32 RoundCount; float TimeLimit; | systems/01 |
| `FMatchResult` | 比赛结果 | int32 WinnerTeamId; TArray<int32> Scores; float Duration; | systems/01 |
| `FCapabilityRequest` | 统一能力请求 | FGameplayTag ActionTag; AController* SourceController; int32 Priority; | DEC-011 |

**日志分类**（通过 `DECLARE_LOG_CATEGORY_EXTERN` / `DEFINE_LOG_CATEGORY`，对齐 systems/07）：

| 日志分类 | 用途 |
|----------|------|
| `LogVRSanguoCore` | 模块启动、生命周期 |
| `LogVRSanguoVR` | OpenXR、追踪、输入适配 |
| `LogVRSanguoCombat` | 命中结算、伤害、防御 |
| `LogVRSanguoWeapon` | 武器抓取、轨迹、解卡 |
| `LogVRSanguoMovement` | 瞬移、平滑移动、IK |
| `LogVRSanguoAI` | AI 决策、战术、动作 |
| `LogVRSanguoFlow` | 流程状态机、阶段切换 |
| `LogVRSanguoPerf` | 性能采样、帧率统计 |

在 `VRSanguoYanWuchang.cpp` 模块启动中完成注册。

---

### Step 2：七项核心接口

全部放在 `Source/VRSanguoYanWuchang/Public/Interfaces/` 下。每个接口使用 `UINTERFACE`/`IInterface` 模式，声明 `BlueprintNativeEvent` 方法，M01 才创建第一个具体实现类。

接口签名以 `standards/05-event-and-interface-standard.md` 的 C++ 声明和 `systems/01-07` 接口契约为准。

| # | 接口 | 文件 | 核心方法 | 契约来源 |
|---|------|------|----------|----------|
| 1 | `IInteractable` | `VRInteractable.h` | `CanGrab()` / `OnGrabbed()` / `OnReleased()` / `OnHoverStart()` / `OnHoverEnd()` | standards/05 |
| 2 | `IWeaponSource` | `VRWeaponSource.h` | `GetWeaponData()` / `IsTwoHanded()` / `GetTrajectory()` | standards/05 |
| 3 | `IDamageable` | `VRDamageable.h` | `ReceiveDamage(FCombatResult)` / `IsAlive()` / `GetHealthRatio()` | standards/05, systems/03 |
| 4 | `IDefenseProvider` | `VRDefenseProvider.h` | `IsBlocking()` / `TryBlock(FAttackRequest)` | standards/05, systems/03 |
| 5 | `IMovementMode` | `VRMovementMode.h` | `RequestTeleport(FVector, FRotator)` / `SetSmoothMove(FVector2D)` / `GetMovementState()` | standards/05, systems/04 |
| 6 | `IBattleParticipant` | `VRBattleParticipant.h` | `OnBattleStart()` / `OnBattleEnd(EBattleOutcome)` / `ResetForNextRound()` | standards/05 |
| 7 | `ICharacterCapability` | `VRCharacterCapability.h` | `RequestAction(FCapabilityRequest)` / `IsActionAllowed()` / `GetCapabilityState()` | systems/05, DEC-011 |

**`ICharacterCapability` 是 T005 的核心交付**——它是玩家控制源和 AI 控制源的统一适配入口（DEC-011 决策）。玩家输入（VR 手柄 / Enhanced Input）和 AI 决策（行为树 / 战术评分）都通过同一接口驱动角色，确保战斗规则不区分玩家和 AI。

**M01 后扩展**（T005 不创建，仅预留设计空间）：
- `IVRWeapon`：`GetWeaponType()`, `GetTrajectorySource()`, `GetGrabPoints()`（systems/02）
- `IGrabbable`：`TryGrab(EHand)`, `Release(EHand)`, `SwitchHand(EHand)`（systems/02）

**接口设计约束**（参考 `standards/05-event-and-interface-standard.md`）：
- 事件委托使用过去时命名（如 `OnWeaponGrabbed`、`OnHitResolved`）
- 请求使用 `Request` 前缀或函数返回值，不把"请求瞬移"命名成"瞬移已完成"
- 接口调用失败必须返回可诊断原因（日志 + `bool` 返回值）
- UI 订阅战斗状态，不直接修改生命值；武器提交命中候选，不直接扣血；AI 请求动作，不绕过角色动作与硬直

---

### Step 3：八个 Data Asset 基类

全部放在 `Source/VRSanguoYanWuchang/Public/Data/` 下。

类名遵循 `standards/02-naming-and-path-standard.md` 和 `systems/index.md` 数据资产目录。每个 DA 基类继承 `UPrimaryDataAsset`，包含：
- `SchemaVersion`（int32，初始值 1）字段（对齐 `standards/04` Schema 版本约定）
- `PostLoad()` 迁移入口（对齐 `standards/04` 迁移策略代码示例）
- `ValidateData()` 检查函数（空引用、非法区间、重复 ID）
- `UPROPERTY` 标记以确保序列化和编辑器可编辑

| DA 基类 | 文件 | 资产前缀 | 最小字段集 |
|---------|------|----------|-----------|
| `UVRWeaponDefinition` | `VRWeaponDefinition.h` | `DA_Weapon_` | WeaponID(FGuid), WeaponType(EWeaponType), GripPoints, EffectiveSpeedThreshold, DamageRange, AttackDirectionRules, TrajectorySampleInterval, SkeletalMeshRef, CollisionProfile, SchemaVersion |
| `UVRArmorDefinition` | `VRArmorDefinition.h` | `DA_Armor_` | ArmorID(FGuid), CoverageMap(EHitZone->float), ResistanceMap(EHitZone->float), HitZoneModifier, SchemaVersion |
| `UVRMovementProfile` | `VRMovementProfile.h` | `DA_Move_` | MoveSpeed, TeleportMaxDist, TeleportCooldown, TurnAngleDeg, ComfortPreset, SchemaVersion |
| `UVRMatchRuleSet` | `VRMatchRuleSet.h` | `DA_Match_` | DefaultTeamSize(3), AllowedSizes(2-4), RoundCount, TimeLimit, DismemberRule, SchemaVersion |
| `UVRUnitDefinition` | `VRUnitDefinition.h` | `DA_Unit_` | UnitType(Enum), PerceptionRadius, CombatStyle(Enum), EquipmentRef, BehaviorTreeRef, SchemaVersion |
| `UVRCommanderDefinition` | `VRCommanderDefinition.h` | `DA_Commander_` | CommanderID(FGuid), DisplayName, WeaponPool, SpecialMoves, PhaseBehavior, SchemaVersion |
| `UVRArenaDefinition` | `VRArenaDefinition.h` | `DA_Arena_` | ArenaID(FGuid), Boundary, SpawnPoints, NavMeshRef, LightingPreset, SchemaVersion |
| `UVRAvatarProfile` | `VRAvatarProfile.h` | `DA_Avatar_` | SkeletalMeshRef, IKProfile, HitZone->BoneMapping, HandMeshes, SchemaVersion |

**数据驱动原则**（参考 `standards/04-data-asset-standard.md`）：
- 核心逻辑不得通过复制蓝图制造参数变体
- AI 等级与兵种类型分离（支持"等级+刀盾/长矛/弓兵"组合）
- 新增字段必须给出安全默认值（`nullptr`、`0`、空数组或占位引用）
- 缺失资源时使用占位反馈而不是阻断战斗
- Schema 版本变更必须在 `CHANGELOG.md` 记录

---

### Step 4：游戏流程状态机

**新增文件**：
- `Source/VRSanguoYanWuchang/Public/Flow/VRGameFlowComponent.h`
- `Source/VRSanguoYanWuchang/Private/Flow/VRGameFlowComponent.cpp`

**实现**：`UVRGameFlowComponent` 继承 `UActorComponent`（遵循 `standards/02` 命名标准，附着在 GameMode 子类上）

**核心功能**（对齐 systems/01 接口契约）：
- 维护 `EGameSessionPhase` 当前阶段
- `RequestPhaseTransition(EGameSessionPhase Target)`：验证合法迁移 -> 广播 `OnPhaseChanged` 委托 -> 旧阶段资源清理
- `StartMatch(const FMatchRuleSet& Rules)` -> `bool`（成功进入 Ready）
- `EndMatch(EMatchEndReason Reason)` -> 触发 Settlement
- `ResetMatch()` -> 幂等重置，清理所有临时对象

**合法迁移矩阵**（硬编码在 `.cpp`）：

```
Calibration -> Ready -> Generate -> Combat -> Settlement -> Reset -> Ready
任意阶段 -> Calibration（紧急重置）
```

**事件广播**：
- `OnPhaseChanged(EGameSessionPhase Old, EGameSessionPhase New)`
- `OnMatchEnded(EMatchEndReason Reason, const FMatchResult& Result)`

**不依赖**：Combat/Weapon/Movement 等子系统。T005 阶段只维护状态机和委托，不编排具体生成、战斗或结算逻辑（M01 后逐步接入）。

**设计约束**（参考 `systems/01-game-flow-system.md`）：
- 单一所有者，阶段切换可追踪、可中止、可幂等重置
- 失败时返回安全状态并提供诊断原因
- 不在流程层计算伤害或选择 AI 战术

---

### Step 5：角色能力适配组件

**新增文件**：
- `Source/VRSanguoYanWuchang/Public/Combat/VRCharacterCapabilityComponent.h`
- `Source/VRSanguoYanWuchang/Private/Combat/VRCharacterCapabilityComponent.cpp`

**实现**：`UVRCharacterCapabilityComponent` 继承 `UActorComponent`，实现 `ICharacterCapability` 接口

**T005 阶段行为**（最小桩）：
- `RequestAction()` 记录日志 `LogVRSanguoCombat` 并返回 `false`（"能力未实现"）
- `IsActionAllowed()` 始终返回 `false`
- `GetCapabilityState()` 始终返回 `ECapabilityState::Idle`

**M01 后**：内部委托给 Combat、Weapon、Movement 子系统填充实际逻辑。

**与 VR 模板的集成**：
- 附着在 VRPawn 蓝图上（通过子类化模板 Pawn 添加此组件）
- 玩家通过 Enhanced Input -> 蓝图适配器 -> `RequestAction()` 路由
- AI 通过行为树任务节点 -> `RequestAction()` 路由

---

### Step 6：空场景与测试角色

**新增蓝图/关卡**：
- `Content/VRSanguo/Dev/L_SkeletonTest.umap`（测试地图放入 Dev 目录，遵循 `standards/02`）

**新增 C++ 类**：
- `Source/VRSanguoYanWuchang/Public/Combat/VRTestDummy.h`
- `Source/VRSanguoYanWuchang/Private/Combat/VRTestDummy.cpp`

`AVRTestDummy` 是纯数据桩角色，实现 `IDamageable` 和 `IBattleParticipant`：
- `ReceiveDamage(FCombatResult)` 记录日志并打印 `FCombatResult` 各字段
- `OnBattleStart()` / `ResetForNextRound()` 输出日志确认调用
- `IsAlive()` 返回 `true`（固定），`GetHealthRatio()` 返回 `1.0f`（固定）

**验证场景**：
1. 编辑器中打开 `L_SkeletonTest`
2. 玩家 VRPawn 已挂载 `VRCharacterCapabilityComponent`
3. 场景中存在一个 `AVRTestDummy` 实例
4. 运行时日志输出：流程进入 Combat 阶段 -> TestDummy 生成 -> 调用 `ReceiveDamage()` -> 流程 Reset -> TestDummy 清理

---

## 与 VR 模板的集成策略

项目基于 UE5.6 官方 VR 模板重建（2026-08-11），模板资产位于 `Content/VRTemplate/`。

| 模板资产 | 处理方式 | 原因 |
|----------|----------|------|
| 模板 GameMode | 子类化为 `BP_VRGameMode`，添加 `VRGameFlowComponent` | 不修改模板源文件，只扩展 |
| 模板 VRPawn | 子类化为 `BP_VRPlayerPawn`，添加 `VRCharacterCapabilityComponent` | 保留抓取/瞬移/手部表现 |
| `Content/VRTemplate/Input/` 下 IMC | 保留（已按 PICO 官方文档绑定），蓝图适配层调用 `RequestAction()` | 不破坏模板输入链 |
| PICO 手柄模型 `SM_PICONeo3_L/R` | 保留（T004 已挂载） | T005 不涉及模型替换 |
| 抓取组件 | 保留不动 | T005 不涉及武器交互实现 |
| 瞬移组件 | 保留不动 | T005 不涉及移动实现 |

**原则：零删除，只做子类化和适配注入。** 模板提供的 VR 交互能力是 M01 战斗切片的物理基础。

---

## 验收清单

| # | 验收项 | 验证方式 |
|---|--------|----------|
| 1 | 七项接口编译通过，头文件可被外部引用 | 编译 + `#include` 测试 |
| 2 | 8 个日志分类可用，`UE_LOG(LogVRSanguoCombat, ...)` 不报错 | 运行时 Output Log 可见 |
| 3 | 八个 Data Asset 基类可在编辑器中创建蓝图子类，SchemaVersion 字段存在 | Content Browser 右键 -> Miscellaneous -> Data Asset -> 选择基类 |
| 4 | 游戏流程状态机启动、合法迁移、幂等重置 | 自动化测试：`RequestPhaseTransition(Combat)` 成功，`Combat->Reset` 后所有委托清理 |
| 5 | 玩家 VRPawn 挂载 `VRCharacterCapabilityComponent`，AI 桩角色走同一接口 | `IsActionAllowed()` 在玩家和 AI 上返回一致结果 |
| 6 | 不删除任何模板 VR 交互（手部、抓取、瞬移仍可用） | 编辑器 PIE 模式下手柄操作验证 |
| 7 | 无 1v1 硬编码、无单武器引用、无联网依赖 | 代码审查 |
| 8 | 空场景可生成玩家全身占位 + TestDummy + 重置 | 编辑器运行验证关卡 |
| 9 | 接口签名与 systems/01-07 接口契约一致 | 代码审查对照 |

---

## 完成定义（全部满足才算任务完成）

- [ ] Step 1：公共类型与日志分类编译通过、运行时可用
- [ ] Step 2：七项核心接口定义完整，编译通过，签名对齐系统契约
- [ ] Step 3：八个 Data Asset 基类可创建、可编辑、SchemaVersion 与 ValidateData() 可用
- [ ] Step 4：流程状态机合法迁移与幂等重置通过测试
- [ ] Step 5：角色能力适配组件挂载成功，玩家与 AI 走统一接口
- [ ] Step 6：空场景中玩家占位 + TestDummy 生成/交互/重置流程正常
- [ ] VR 模板交互能力完整保留（零删除）
- [ ] 代码无 1v1 / 单武器 / 联网硬编码
- [ ] 代码编译通过（Win64 Development Editor）
- [ ] `STATUS.json` 更新为 `awaiting_review`

---

## 依赖与风险

| 依赖 | 状态 | 说明 |
|------|------|------|
| T004 完成 | awaiting_review | T005 不依赖 T004 真机验证，仅依赖编译环境与 VR 模板资产 |
| VS2026 + MSVC | ✅ | T003 已验证（UE5.6） |
| UBT 编译环境 | ✅ | T003 已验证 |
| VR 模板完整 | ✅ | T004 已核验 UE5.6 模板资产完整性 |
| UEBridgeMCP | ✅ | T004 已安装（TD-010 跟踪 GPL 许可证） |

| 风险 | 概率 | 缓解 |
|------|------|------|
| 模板 Pawn 子类化后抓取/瞬移失效 | 低 | 只添加组件，不修改模板基类逻辑；PIE 下立即验证 |
| Data Asset 字段过多导致编辑器卡顿 | 低 | T005 仅定义最小字段集，M01-M02 逐步扩展 |
| GameFlowComponent 与 GameMode 生命周期冲突 | 低 | 使用 `UActorComponent` 附着在 GameMode 上，随 GameMode 生命周期管理 |
| 接口签名与系统契约存在未发现的细微差异 | 中 | 实现前逐份对照 systems/01-07 接口契约段落 |

---

## 预估耗时

| 步骤 | 预估 | 累计 |
|------|------|------|
| Step 1：类型 + 日志 | 1h | 1h |
| Step 2：核心接口 | 1h | 2h |
| Step 3：Data Asset 基类 | 1.5h | 3.5h |
| Step 4：流程状态机 | 1.5h | 5h |
| Step 5：能力适配组件 | 1h | 6h |
| Step 6：空场景验证 | 1h | 7h |
| **合计** | **~7h** | |

---

## 报告路径

`.trae/execution/reports/tasks/M00-T005.md`
