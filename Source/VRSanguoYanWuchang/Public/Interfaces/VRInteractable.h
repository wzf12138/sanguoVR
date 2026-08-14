// VR 三国演武场 - IInteractable 接口
// 抓取、放下、吸附与交互提示（standards/05 + systems/02 契约）
// 签名说明：systems 契约声明"具体签名以 M00-T005 C++ 骨架为准"。
// 手部参数 T005 阶段用通用 AActor*（AVRHand 于 M01 创建后收紧为 AVRHand*）。

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "VRInteractable.generated.h"

class AActor;

UINTERFACE(BlueprintType)
class UInteractable : public UInterface
{
	GENERATED_BODY()
};

class IInteractable
{
	GENERATED_BODY()

public:
	/** 是否可被抓取（Hand：执行抓取的手部 Actor） */
	UFUNCTION(BlueprintNativeEvent, Category = "Interaction")
	bool CanGrab(AActor* Hand) const;

	/** 被抓取 */
	UFUNCTION(BlueprintNativeEvent, Category = "Interaction")
	void OnGrabbed(AActor* Hand);

	/** 被释放 */
	UFUNCTION(BlueprintNativeEvent, Category = "Interaction")
	void OnReleased(AActor* Hand);

	/** 悬停开始 */
	UFUNCTION(BlueprintNativeEvent, Category = "Interaction")
	void OnHoverStart(AActor* Hand);

	/** 悬停结束 */
	UFUNCTION(BlueprintNativeEvent, Category = "Interaction")
	void OnHoverEnd(AActor* Hand);
};
