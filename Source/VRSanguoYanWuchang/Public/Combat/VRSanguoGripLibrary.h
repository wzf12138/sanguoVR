// VR 三国演武场 - UVRSanguoGripLibrary 抓握交互函数库
// 依据 standards/03-blueprint-cpp-boundary-standard.md：
//   C++ 管规则（输入→检测→GripObject→DropObject），蓝图（表现层）只负责调函数。
// 依据 manager 裁决 msg-20260830-231000-manager-002：
//   最小范围，只封装"检测→GripObject→DropObject"三步，左右手通用（传手柄引用与半径）。
//   本封装是将来 systems/02 IGrabbable 接口桥的雏形（TD-013 继续挂）。
// 说明：VRE 的 GripObject 必须显式传入 ObjectToGrip，不会自动扫描附近物体，
//   因此本库负责用 Sphere Overlap 检测最近的可抓取物。

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "VRSanguoGripLibrary.generated.h"

class UGripMotionControllerComponent;
class AActor;

/**
 * 抓取交互函数库（左右手通用）。
 * 用途：VR 角色把手柄的 Grip 输入接入"检测→抓取→释放"。
 */
UCLASS()
class VRSANGUOYANWUCHANG_API UVRSanguoGripLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:
	/**
	 * 尝试用指定手柄抓取前方最近的可交互物体。
	 * @param MotionController   目标手柄（左/右 GripMotionControllerComponent，传 _0 或 _1）。
	 * @param SphereRadius       检测球半径（厘米）。
	 * @param ForwardDistance    手柄前方沿轴向继续探测的距离（厘米），用于覆盖手柄前方一段区域。
	 * @param OptionalSocketName 指定 socket 吸附名；留 NAME_None 则使用 VRE 自动匹配（找含 "Grip" 的 socket）。
	 * @return 抓取是否成功。
	 */
	UFUNCTION(BlueprintCallable, Category = "VRGrip", meta = (DisplayName = "TryGrip"))
	static bool TryGrip(
		UGripMotionControllerComponent* MotionController,
		float SphereRadius = 12.0f,
		float ForwardDistance = 30.0f,
		FName OptionalSocketName = NAME_None);

	/**
	 * 释放指定手柄当前抓取的物体。
	 * @param MotionController 目标手柄。
	 * @return 是否成功释放（手柄未抓取任何物体时返回 false）。
	 */
	UFUNCTION(BlueprintCallable, Category = "VRGrip", meta = (DisplayName = "ReleaseGrip"))
	static bool ReleaseGrip(UGripMotionControllerComponent* MotionController);
};
