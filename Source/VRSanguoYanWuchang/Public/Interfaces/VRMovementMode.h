// VR 三国演武场 - IMovementMode 接口
// 瞬移、平滑移动及后续坐骑移动（standards/05 + systems/04 契约）

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "Core/VRTypes.h"
#include "VRMovementMode.generated.h"

UINTERFACE(BlueprintType)
class UMovementMode : public UInterface
{
	GENERATED_BODY()
};

class IMovementMode
{
	GENERATED_BODY()

public:
	/** 请求战术瞬移到目标点，返回是否成功 */
	UFUNCTION(BlueprintNativeEvent, Category = "Movement")
	bool RequestTeleport(const FVector& Target, FRotator TargetRotation);

	/** 设置平滑移动输入（摇杆值） */
	UFUNCTION(BlueprintNativeEvent, Category = "Movement")
	void SetSmoothMove(const FVector2D& Input);

	/** 当前移动状态 */
	UFUNCTION(BlueprintNativeEvent, Category = "Movement")
	EMovementState GetMovementState() const;
};
