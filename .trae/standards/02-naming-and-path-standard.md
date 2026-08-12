# 命名与路径标准

## Unreal 资产前缀

| 类型 | 前缀 | 示例 |
|---|---|---|
| Blueprint Actor | `BP_` | `BP_VRPlayerPawn` |
| Actor Component | `BPC_` | `BPC_Combat` |
| Widget | `WBP_` | `WBP_BattleResult` |
| Data Asset | `DA_` | `DA_Weapon_Spear_T1` |
| Data Table | `DT_` | `DT_TutorialSteps` |
| Behavior Tree | `BT_` | `BT_ArenaFighter` |
| Blackboard | `BB_` | `BB_ArenaFighter` |
| Animation Montage | `AM_` | `AM_Sword_Attack_A` |
| Sound Cue | `SC_` | `SC_Block_Perfect` |
| Material Instance | `MI_` | `MI_Armor_Leather` |

## C++ 命名

遵循 Unreal 类型前缀与 PascalCase。组件职责使用领域名：`CombatComponent`、`WeaponComponent`、`DefenseComponent`、`DamageComponent`、`VRMovementComponent`、`InteractionComponent`、`CombatResolver`。布尔值使用 `b` 前缀；事件使用过去时结果名，如 `OnHitResolved`。

## 内容路径

`Content/VRSanguo/` 下按 `Core`、`VR`、`Combat`、`AI`、`Arena`、`UI`、`Audio`、`Art`、`Data`、`Dev` 分类。运行时资产不得引用 `Dev`。测试地图、占位资产和调试 Widget 只能放入 `Dev`。

## 标识符

武器、AI 等级、教程步骤和竞技场配置使用稳定的 Gameplay Tag 或 Name，不用界面中文作为程序主键。重命名时保留重定向并同步登记受影响资产。

## 实现示例

### 五武器完整命名

| 武器类别 | DataAsset | 蓝图 | 模型 | 动画蒙太奇 | C++ 类 |
|---|---|---|---|---|---|
| 单手刀剑 | `DA_Weapon_Sword_T1` | `BP_Weapon_Sword` | `SK_Weapon_Sword_Han` | `AM_Sword_Attack_A`, `AM_Sword_Block` | `AVRWeaponSword` |
| 盾牌 | `DA_Weapon_Shield_T1` | `BP_Weapon_Shield` | `SK_Weapon_Shield_Round` | `AM_Shield_Bash`, `AM_Shield_Block` | `AVRWeaponShield` |
| 双手长柄 | `DA_Weapon_Polearm_T1` | `BP_Weapon_Polearm` | `SK_Weapon_Polearm_Glaive` | `AM_Polearm_Swing_A`, `AM_Polearm_Thrust` | `AVRWeaponPolearm` |
| 长矛 | `DA_Weapon_Spear_T1` | `BP_Weapon_Spear` | `SK_Weapon_Spear_Qiang` | `AM_Spear_Thrust_A`, `AM_Spear_Sweep` | `AVRWeaponSpear` |
| 弓箭 | `DA_Weapon_Bow_T1` | `BP_Weapon_Bow` | `SK_Weapon_Bow_Recurve` | `AM_Bow_Draw`, `AM_Bow_Release` | `AVRWeaponBow` |

### 兵种与武将命名

| 类型 | DataAsset | 蓝图 | 行为树 | 黑板 |
|---|---|---|---|---|
| 刀盾兵 | `DA_Unit_SwordShield` | `BP_Unit_SwordShield` | `BT_Unit_Melee` | `BB_Unit_Melee` |
| 长矛兵 | `DA_Unit_Spearman` | `BP_Unit_Spearman` | `BT_Unit_Melee` | `BB_Unit_Melee` |
| 长柄重兵 | `DA_Unit_Polearm` | `BP_Unit_Polearm` | `BT_Unit_Melee` | `BB_Unit_Melee` |
| 弓兵 | `DA_Unit_Archer` | `BP_Unit_Archer` | `BT_Unit_Ranged` | `BB_Unit_Ranged` |
| 精锐近战 | `DA_Unit_Elite` | `BP_Unit_Elite` | `BT_Unit_Melee` | `BB_Unit_Melee` |
| 武将（示例） | `DA_Commander_GuanYu` | `BP_Commander_GuanYu` | `BT_Commander` | `BB_Commander` |

### C++ 类与接口契约对应

| 系统指引 | 核心 C++ 类 | 文件名 |
|---|---|---|
| 01 游戏流程 | `AVRGameSession`, `UVRGameFlowComponent` | `VRGameSession.h/.cpp` |
| 02 交互武器 | `AVRWeaponBase`, `UVRInteractionComponent`, `IVRWeapon`, `IGrabbable` | `VRWeaponBase.h/.cpp`, `VRInteractionComponent.h/.cpp` |
| 03 战斗结算 | `UVRCombatResolver`, `UVRCharacterStateComponent` | `VRCombatResolver.h/.cpp` |
| 04 移动 | `UVRMovementComponent`, `UVRFullBodyIKComponent` | `VRMovementComponent.h/.cpp` |
| 05 AI 战斗 | `UVRAICombatComponent`, `AVRAIController` | `VRAICombatComponent.h/.cpp` |
| 06 竞技场/UI | `AVRArenaManager`, `UVRTutorialComponent` | `VRArenaManager.h/.cpp` |
| 07 保存诊断 | `UVRSaveSubsystem`, `UVRDiagnosticsSubsystem` | `VRSaveSubsystem.h/.cpp` |

### 内容路径示例

```
Content/VRSanguo/
├── Core/          # C++ 蓝图基类、接口、组件
├── VR/            # VR Pawn、运动控制器、IK 配置
├── Combat/        # 战斗组件、碰撞体、反馈
├── AI/            # 行为树、黑板、感知配置
├── Arena/         # 竞技场关卡、碰撞、NavMesh
├── UI/            # Widget、HUD、菜单
├── Audio/         # 音效、音乐
├── Art/           # 模型、纹理、材质
├── Data/          # DataAsset、Data Table
└── Dev/           # 测试地图、占位资产、调试 Widget（运行时不引用）
```