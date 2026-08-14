// VR 三国演武场 - GameplayTag 注册声明
// 项目级 Tag 统一注册（standards/02 标识符：稳定 Tag 不用界面中文作主键）

#pragma once

#include "CoreMinimal.h"
#include "NativeGameplayTags.h"

// 能力标签（DEC-011 统一能力接口）
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Action_Attack);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Action_Block);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Action_Move);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Action_Teleport);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Action_Interact);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(Action_SwitchWeapon);

// 战斗状态标签
UE_DECLARE_GAMEPLAY_TAG_EXTERN(State_Combat_Idle);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(State_Combat_Attacking);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(State_Combat_Defending);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(State_Combat_Staggered);
UE_DECLARE_GAMEPLAY_TAG_EXTERN(State_Combat_Dead);
