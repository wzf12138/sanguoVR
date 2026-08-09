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