// VR 三国演武场 - GameplayTag 注册实现
// 使用 NativeGameplayTags 静态注册（UE5.6 标准宏）

#include "Core/VRGameplayTags.h"

// 能力标签（DEC-011 统一能力接口）
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Action_Attack, "VR.Action.Attack", "角色攻击动作");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Action_Block, "VR.Action.Block", "角色格挡动作");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Action_Move, "VR.Action.Move", "角色平滑移动");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Action_Teleport, "VR.Action.Teleport", "角色战术瞬移");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Action_Interact, "VR.Action.Interact", "角色交互动作");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(Action_SwitchWeapon, "VR.Action.SwitchWeapon", "切换武器");

// 战斗状态标签
UE_DEFINE_GAMEPLAY_TAG_COMMENT(State_Combat_Idle, "VR.State.Combat.Idle", "战斗空闲");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(State_Combat_Attacking, "VR.State.Combat.Attacking", "战斗中攻击");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(State_Combat_Defending, "VR.State.Combat.Defending", "战斗中防御");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(State_Combat_Staggered, "VR.State.Combat.Staggered", "硬直状态");
UE_DEFINE_GAMEPLAY_TAG_COMMENT(State_Combat_Dead, "VR.State.Combat.Dead", "死亡状态");
