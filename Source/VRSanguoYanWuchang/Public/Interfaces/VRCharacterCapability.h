// VR 三国演武场 - ICharacterCapability 接口
// 统一角色能力入口：玩家（VR 手柄/Enhanced Input）与 AI（行为树/战术评分）共用
// DEC-011 决策 + systems/05 契约

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "Core/VRTypes.h"
#include "VRCharacterCapability.generated.h"

UINTERFACE(BlueprintType)
class UCharacterCapability : public UInterface
{
	GENERATED_BODY()
};

class ICharacterCapability
{
	GENERATED_BODY()

public:
	/** 请求执行一个能力动作（攻击/格挡/移动/瞬移/交互/切武器）。
	 *  统一入口：不区分控制源是玩家还是 AI。 */
	UFUNCTION(BlueprintNativeEvent, Category = "Capability")
	bool RequestAction(const FCapabilityRequest& Request);

	/** 该能力当前是否允许执行 */
	UFUNCTION(BlueprintNativeEvent, Category = "Capability")
	bool IsActionAllowed() const;

	/** 当前能力状态 */
	UFUNCTION(BlueprintNativeEvent, Category = "Capability")
	ECapabilityState GetCapabilityState() const;
};
