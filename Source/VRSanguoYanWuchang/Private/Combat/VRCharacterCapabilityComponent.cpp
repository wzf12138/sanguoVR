// VR 三国演武场 - UVRCharacterCapabilityComponent 实现

#include "Combat/VRCharacterCapabilityComponent.h"
#include "Core/VRLogChannels.h"

UVRCharacterCapabilityComponent::UVRCharacterCapabilityComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

bool UVRCharacterCapabilityComponent::RequestAction_Implementation(const FCapabilityRequest& Request)
{
	// T005 最小桩：能力未实现（M01 后委托给 Combat/Weapon/Movement 子系统）
	UE_LOG(LogVRSanguoCombat, Warning, TEXT("RequestAction: 能力未实现 Tag=%s Priority=%d"),
		*Request.ActionTag.ToString(), Request.Priority);
	return false;
}

bool UVRCharacterCapabilityComponent::IsActionAllowed_Implementation() const
{
	return false;
}

ECapabilityState UVRCharacterCapabilityComponent::GetCapabilityState_Implementation() const
{
	return ECapabilityState::Idle;
}
