// VR 三国演武场 - IDefenseProvider 接口
// 格挡面、盾牌状态与防御消耗（standards/05 + systems/03 契约）

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "Core/VRTypes.h"
#include "VRDefenseProvider.generated.h"

UINTERFACE(BlueprintType)
class UDefenseProvider : public UInterface
{
	GENERATED_BODY()
};

class IDefenseProvider
{
	GENERATED_BODY()

public:
	/** 当前是否处于格挡状态 */
	UFUNCTION(BlueprintNativeEvent, Category = "Defense")
	bool IsBlocking() const;

	/** 尝试格挡一次攻击，返回防御结果（含是否成功/弹反角度） */
	UFUNCTION(BlueprintNativeEvent, Category = "Defense")
	FDefenseResult TryBlock(const FAttackRequest& Request);
};
