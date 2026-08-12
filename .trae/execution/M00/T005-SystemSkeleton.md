# M00-T005 系统骨架与数据驱动边界

- 状态：见 `../active/STATUS.json`（本详规不复制动态状态）
- 优先级：P0
- 前置任务：M00-T004（VR/OpenXR/PICO 基线，当前 blocked；T005 已获批准并发启动，不依赖 T004 完成）
- 目标：建立 Combat、Weapon、CharacterState、Movement、FullBodyIK、SquadAI、GameModeFlow 与 Diagnostics 的最小代码边界。

---

## 这个任务在完整游戏开发中的位置

```
已完成：
  T001 治理基线 ✅ → 项目怎么管，定了
  T002 Git 基线 ✅   → 代码怎么存，定了
  T003 编译基线 ✅   → 代码能编译、编辑器能跑、MCP 通了
  T004 VR/PICO 基线 🚫 → PICO 设备阻塞，转为 blocked；T005 并发启动

本任务 T005：
  搭 C++ 模块骨架、核心接口、Data Asset 基类、流程状态机和诊断日志
  ── 这是"后续所有战斗/武器/移动/AI 代码的脚手架"

之后：
  T006 自动化门禁 → 测试框架
  M01 1v1 战斗切片 → 开始做真正的战斗玩法
```

---

## 实施步骤

### Step 1：公共类型与日志分类

**新增文件**：

- `Source/VRSanguoYanWuchang/Public/Core/VRSTypes.h` — 通用结构体与枚举
- `Source/VRSanguoYanWuchang/Public/Core/VRSLogChannels.h` — 8 个日志分类声明
- `Source/VRSanguoYanWuchang/Public/Core/VRSGameplayTags.h` — 项目 GameplayTag 注册
- 对应 `.cpp` 实现文件

**核心类型定义**：

| 类型 | 用途 | 关键字段 |
|------|------|----------|
| `FDamageResult` | 战斗结算结果 | WeaponID, HitZone, BaseDamage, TrajectoryQuality, ArmorMitigation, FinalDamage, HitLocation, HitNormal, AttackInstanceID |
| `FCapabilityRequest` | 统一能力请求 | ActionTag, SourceController, Priority, Context |
| `ECapabilityState` | 角色能力状态枚举 | Idle, Attacking, Defending, Staggered, Dead |
| `EGamePhase` | 游戏阶段枚举 | None, Calibration, Preparation, Spawning, Combat, Resolution, Reset |
| `EHitZone` | 命中部位枚举 | Head, Torso, LeftArm, RightArm, LeftLeg, RightLeg |
| `EWeaponType` | 武器类型枚举 | OneHandSword, Shield, TwoHandHeavy, Spear, Bow |

**日志分类**（通过 `DECLARE_LOG_CATEGORY_EXTERN` / `DEFINE_LOG_CATEGORY`）：

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

全部放在 `Source/VRSanguoYanWuchang/Public/Interfaces/` 下。每个接口只定义纯虚函数，不含实现——M01 才创建第一个具体实现类。

| # | 接口 | 文件 | 核心方法 |
|---|------|------|----------|
| 1 | `IInteractable` | `VRSInteractable.h` | `CanGrab()` / `OnGrabbed()` / `OnReleased()` / `GetInteractionHint()` |
| 2 | `IWeaponSource` | `VRSWeaponSource.h` | `GetWeaponData()` / `GetGripState()` / `GetAttackTrajectory()` / `IsInAttackPhase()` |
| 3 | `IDamageable` | `VRSDamageable.h` | `ApplyDamage(FDamageResult)` / `GetHealth()` / `IsDead()` / `OnDeath()` |
| 4 | `IDefenseProvider` | `VRSDefenseProvider.h` | `GetBlockDirection()` / `IsBlocking()` / `GetShieldState()` / `ConsumeDefense()` |
| 5 | `IMovementMode` | `VRSMovementMode.h` | `RequestTeleport()` / `RequestSmoothMove()` / `GetMovementState()` / `CanMove()` |
| 6 | `IBattleParticipant` | `VRSBattleParticipant.h` | `OnSpawned()` / `GetBattleState()` / `OnVictory()` / `OnDefeat()` / `OnReset()` |
| 7 | `IVRSCharacterCapability` | `VRSCharacterCapability.h` | `RequestAction(FCapabilityRequest)` / `IsActionAllowed()` / `GetCapabilityState()` |

**`IVRSCharacterCapability` 是 T005 的核心交付**——它是玩家控制源和 AI 控制源的统一适配入口。玩家输入（VR 手柄 / Enhanced Input）和 AI 决策（行为树 / 战术评分）都通过同一接口驱动角色，确保战斗规则不区分玩家和 AI。

**接口设计约束**（参考 `.trae/standards/05-event-and-interface-standard.md`）：
- 事件委托使用过去时命名（如 `FOnWeaponGrabbed`、`FOnHitResolved`）
- 请求使用 `Request` 前缀或函数返回值，不把"请求瞬移"命名成"瞬移已完成"
- 接口调用失败必须返回可诊断原因（日志 + `bool` 返回值）
- UI 订阅战斗状态，不直接修改生命值；武器提交命中候选，不直接扣血；AI 请求动作，不绕过角色动作与硬直

---

### Step 3：八个 Data Asset 基类

全部放在 `Source/VRSanguoYanWuchang/Public/Data/` 下。

每个 DA 基类必须包含：
- `DataVersion`（int32）字段
- `ValidateData()` 检查函数（空引用、非法区间、重复 ID）
- `UPROPERTY` 标记以确保序列化和编辑器可编辑

| DA 基类 | 文件 | 最小字段集 |
|---------|------|-----------|
| `UVRSWeaponData` | `VRSWeaponData.h` | WeaponID(FGuid), WeaponType(EWeaponType), GripPoints, EffectiveSpeedThreshold, DamageRange, AttackDirectionRules, TrajectorySampleInterval, SkeletalMeshRef, CollisionProfile |
| `UVRSArmorData` | `VRSArmorData.h` | ArmorID(FGuid), CoverageMap(EHitZone→0-1), ResistanceMap(EHitZone→0-1), HitZoneModifier |
| `UVRSMovementData` | `VRSMovementData.h` | MoveSpeed, TeleportMaxDist, TeleportCooldown, TurnAngleDeg, ComfortPreset |
| `UVRSGameRulesData` | `VRSGameRulesData.h` | DefaultTeamSize(3), AllowedSizes(2-4), RoundCount, TimeLimit, DismemberRule |
| `VRSAIUnitData` | `VRSAIUnitData.h` | UnitType(Enum), PerceptionRadius, CombatStyle(Enum), EquipmentRef, BehaviorTreeRef |
| `UVRSHeroData` | `VRSHeroData.h` | HeroID(FGuid), DisplayName, WeaponPool, SpecialMoves, PhaseBehavior |
| `VRSArenaData` | `VRSArenaData.h` | ArenaID(FGuid), Boundary, SpawnPoints, NavMeshRef, LightingPreset |
| `VRSAvatarData` | `VRSAvatarData.h` | SkeletalMeshRef, IKProfile, HitZone→BoneMapping, HandMeshes |

**数据驱动原则**（参考 `.trae/standards/04-data-asset-standard.md`）：
- 核心逻辑不得通过复制蓝图制造参数变体
- AI 等级与兵种类型分离（支持"等级+刀盾/长矛/弓兵"组合）
- 新增字段必须给出安全默认值
- 缺失资源时使用占位反馈而不是阻断战斗

---

### Step 4：游戏流程状态机

**新增文件**：
- `Source/VRSanguoYanWuchang/Public/Flow/VRSGameFlowSubsystem.h`
- `Source/VRSanguoYanWuchang/Private/Flow/VRSGameFlowSubsystem.cpp`

**实现**：`UVRSGameFlowSubsystem` 继承 `UGameInstanceSubsystem`

**核心功能**：
- 维护 `EGamePhase` 当前阶段
- `TransitionTo(EGamePhase)`：验证合法迁移 → 广播 `FOnPhaseChanged` 委托 → 旧阶段资源清理
- 幂等重置：同一阶段重复 TransitionTo 不产生副作用

**合法迁移矩阵**（硬编码在 `.cpp`）：

```
None → Calibration → Preparation → Spawning → Combat → Resolution → Reset → Preparation
任意阶段 → None（紧急退出）
```

**不依赖**：Combat/Weapon/Movement 等子系统。T005 阶段只维护状态机和委托，不编排具体生成、战斗或结算逻辑（M01 后逐步接入）。

**设计约束**（参考 `.trae/systems/01-game-flow-system.md`）：
- 单一所有者，阶段切换可追踪、可中止、可幂等重置
- 失败时返回安全状态并提供诊断原因
- 不在流程层计算伤害或选择 AI 战术

---

### Step 5：角色能力适配组件

**新增文件**：
- `Source/VRSanguoYanWuchang/Public/Combat/VRSCharacterCapabilityComponent.h`
- `Source/VRSanguoYanWuchang/Private/Combat/VRSCharacterCapabilityComponent.cpp`

**实现**：`UVRSCharacterCapabilityComponent` 继承 `UActorComponent`，实现 `IVRSCharacterCapability` 接口

**T005 阶段行为**（最小桩）：
- `RequestAction()` 记录日志 `LogVRSanguoCombat` 并返回 `false`（"能力未实现"）
- `IsActionAllowed()` 始终返回 `false`
- `GetCapabilityState()` 始终返回 `ECapabilityState::Idle`

**M01 后**：内部委托给 Combat、Weapon、Movement 子系统填充实际逻辑。

**与 VR 模板的集成**：
- 附着在 VRPawn 蓝图上（通过子类化模板 Pawn 添加此组件）
- 玩家通过 Enhanced Input → 蓝图适配器 → `RequestAction()` 路由
- AI 通过行为树任务节点 → `RequestAction()` 路由

---

### Step 6：空场景与测试角色

**新增蓝图/关卡**：
- `Content/VRSanguo/Maps/L_SkeletonTest`（或直接在 `L_XRTemplate` 上扩展）

**新增 C++ 类**：
- `Source/VRSanguoYanWuchang/Public/Combat/VRSTestDummy.h`
- `Source/VRSanguoYanWuchang/Private/Combat/VRSTestDummy.cpp`

`AVRSTestDummy` 是纯数据桩角色，实现 `IDamageable` 和 `IBattleParticipant`：
- `ApplyDamage()` 记录日志并打印 `FDamageResult` 各字段
- `OnSpawned()` / `OnReset()` 输出日志确认调用

**验证场景**：
1. 编辑器中打开 `L_SkeletonTest`
2. 玩家 VRPawn 已挂载 `VRSCharacterCapabilityComponent`
3. 场景中存在一个 `AVRSTestDummy` 实例
4. 运行时日志输出：流程进入 Combat 阶段 → TestDummy 生成 → 调用 `ApplyDamage()` → 流程 Reset → TestDummy 清理

---

## 与 VR 模板的集成策略

| 模板资产 | 处理方式 | 原因 |
|----------|----------|------|
| `BP_XRGameMode` | 子类化为 `BP_VRSGameMode`，注入 `VRSGameFlowSubsystem` | 不修改模板源文件，只扩展 |
| `BP_XRPawn` | 子类化为 `BP_VRSPawn`，添加 `VRSCharacterCapabilityComponent` | 保留抓取/瞬移/手部表现 |
| `IMC_Default/Hands/Weapon_*` | 保留，蓝图适配层调用 `RequestAction()` | 不破坏模板输入链 |
| 手部 SkeletalMesh | 保留不动 | T005 不涉及模型替换 |
| 抓取组件 | 保留不动 | T005 不涉及武器交互实现 |
| 瞬移组件 | 保留不动 | T005 不涉及移动实现 |
| `L_XRTemplate` | 保留为参考 | 新建 `L_SkeletonTest` 做独立验证 |

**原则：零删除，只做子类化和适配注入。** 模板提供的 VR 交互能力是 M01 战斗切片的物理基础。

---

## 验收清单

| # | 验收项 | 验证方式 |
|---|--------|----------|
| 1 | 七项接口编译通过，头文件可被外部引用 | 编译 + `#include` 测试 |
| 2 | 8 个日志分类可用，`UE_LOG(LogVRSanguoCombat, ...)` 不报错 | 运行时 Output Log 可见 |
| 3 | 八个 Data Asset 基类可在编辑器中创建蓝图子类 | Content Browser 右键 → Miscellaneous → Data Asset → 选择基类 |
| 4 | 游戏流程状态机启动、合法迁移、幂等重置 | 自动化测试：`TransitionTo(Combat)` 成功，`Combat→Reset` 后所有委托清理 |
| 5 | 玩家 VRPawn 挂载 `VRSCharacterCapabilityComponent`，AI 桩角色走同一接口 | `IsActionAllowed()` 在玩家和 AI 上返回一致结果 |
| 6 | 不删除任何模板 VR 交互（手部、抓取、瞬移仍可用） | 编辑器 PIE 模式下手柄操作验证 |
| 7 | 无 1v1 硬编码、无单武器引用、无联网依赖 | 代码审查 |
| 8 | 空场景可生成玩家全身占位 + TestDummy + 重置 | 编辑器运行验证关卡 |

---

## 完成定义（全部满足才算任务完成）

- [ ] Step 1：公共类型与日志分类编译通过、运行时可用
- [ ] Step 2：七项核心接口定义完整，编译通过
- [ ] Step 3：八个 Data Asset 基类可创建、可编辑、ValidateData() 可用
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
| T004 完成 | blocked（PICO 设备） | T005 可在 T004 完成前并行执行，仅依赖编译环境与 VR 模板资产 |
| VS2026 + MSVC | ✅ | T003 已验证 |
| UBT 编译环境 | ✅ | T003 已验证 |
| VR 模板完整 | ✅ | T004 Phase 3 已核验资产完整性 |

| 风险 | 概率 | 缓解 |
|------|------|------|
| 模板 Pawn 子类化后抓取/瞬移失效 | 低 | 只添加组件，不修改模板基类逻辑；PIE 下立即验证 |
| Data Asset 字段过多导致编辑器卡顿 | 低 | T005 仅定义最小字段集，M01-M02 逐步扩展 |
| GameFlowSubsystem 与 XRGameMode 生命周期冲突 | 中 | 使用 `UGameInstanceSubsystem`（不绑定 World），在 GameMode 子类中显式调用 TransitionTo |

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
