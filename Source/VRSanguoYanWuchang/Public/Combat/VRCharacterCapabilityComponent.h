// VR 三国演武场 - UVRCharacterCapabilityComponent 角色能力适配组件
// 实现 ICharacterCapability（DEC-011 统一能力接口）
// T005 阶段为最小桩：RequestAction 记录日志并返回 false（能力未实现），M01 后填充实际逻辑

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Interfaces/VRCharacterCapability.h"
#include "Core/VRTypes.h"
#include "VRCharacterCapabilityComponent.generated.h"

UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class VRSANGUOYANWUCHANG_API UVRCharacterCapabilityComponent : public UActorComponent, public ICharacterCapability
{
	GENERATED_BODY()

public:
	UVRCharacterCapabilityComponent();

	// ===== ICharacterCapability（DEC-011）=====

	/** T005 最小桩：记录日志并返回 false（能力未实现） */
	virtual bool RequestAction_Implementation(const FCapabilityRequest& Request) override;

	/** T005 最小桩：始终返回 false */
	virtual bool IsActionAllowed_Implementation() const override;

	/** T005 最小桩：始终返回 Idle */
	virtual ECapabilityState GetCapabilityState_Implementation() const override;
};
