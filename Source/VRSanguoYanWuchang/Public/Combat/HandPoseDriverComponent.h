// VR 三国演武场 - UHandPoseDriverComponent 手部姿势驱动组件
// M01-T001 缺陷④（手指弯曲）：每帧读取 EnhancedInput 轴值（握把=握拳、扳机=食指），
// 写入手部 SkeletalMesh 动画实例（ABP_MannequinsXR）的官方姿势 alpha 变量。
// 姿势资产全部为官方 MannequinsXR 现成资产，本组件只做输入→动画变量桥接，不改 ABP 资产。

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HandPoseDriverComponent.generated.h"

class UInputAction;
class USkeletalMeshComponent;
class UAnimInstance;
class UEnhancedPlayerInput;
class UGripMotionControllerComponent;

UCLASS(ClassGroup = (VRSanguo), meta = (BlueprintSpawnableComponent))
class VRSANGUOYANWUCHANG_API UHandPoseDriverComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UHandPoseDriverComponent();

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	// ===== 输入资产引用（实例上配置）=====

	/** 右手握把轴（握拳）——IMC_Hands: PICONeo3/OculusTouch Right Grip_Axis */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VRSanguo|HandPose")
	TObjectPtr<UInputAction> GraspActionRight = nullptr;

	/** 左手握把轴（握拳） */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VRSanguo|HandPose")
	TObjectPtr<UInputAction> GraspActionLeft = nullptr;

	/** 右手扳机轴（食指）——IMC_Hands: Trigger_Axis */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VRSanguo|HandPose")
	TObjectPtr<UInputAction> IndexCurlActionRight = nullptr;

	/** 左手扳机轴（食指） */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VRSanguo|HandPose")
	TObjectPtr<UInputAction> IndexCurlActionLeft = nullptr;

	/** 姿势平滑速度（越大越跟手；<=0 表示直写不平滑） */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "VRSanguo|HandPose", meta = (ClampMin = "0.0", ClampMax = "60.0"))
	float PoseLerpSpeed = 18.0f;

	/** 手部网格组件名（默认与 BP_VRCharacter 一致，无需改动） */
	UPROPERTY(EditAnywhere, Category = "VRSanguo|HandPose")
	FName RightHandMeshName = "HandMeshRight";

	UPROPERTY(EditAnywhere, Category = "VRSanguo|HandPose")
	FName LeftHandMeshName = "HandMeshLeft";

private:
	/** 读取输入轴值并写入两只手的动画实例 */
	void DriveHandPoses(float DeltaTime);

	/** 写入单个手的姿势变量（bMirror 由 ABP_MannequinsXR 的 Mirror 节点消费；bHoldingWeapon 切换握拳/握圆柱姿势） */
	void ApplyPose(USkeletalMeshComponent* Mesh, float GraspAlpha, float CurlAlpha, bool bMirror, bool bHoldingWeapon) const;

	/** 懒查并缓存手部网格组件（按组件名匹配） */
	USkeletalMeshComponent* ResolveHandMesh(bool bRight);

	/** 该手当前是否握着武器（VRE 抓取系统查询：对应手的 GripMotionController 有无握持物） */
	bool ResolveHandHoldingWeapon(bool bRight);

	UEnhancedPlayerInput* ResolveEnhancedInput();

private:
	/** UE5.6 反射直写动画实例蓝图变量（等价蓝图 Set 节点） */
	void WriteAnimDouble(UAnimInstance* AnimInstance, const FName& VarName, float Value) const;
	void WriteAnimBool(UAnimInstance* AnimInstance, const FName& VarName, bool bValue) const;

	UPROPERTY(Transient)
	TObjectPtr<USkeletalMeshComponent> CachedRightMesh = nullptr;

	UPROPERTY(Transient)
	TObjectPtr<USkeletalMeshComponent> CachedLeftMesh = nullptr;

	UPROPERTY(Transient)
	TObjectPtr<UGripMotionControllerComponent> CachedRightController = nullptr;

	UPROPERTY(Transient)
	TObjectPtr<UGripMotionControllerComponent> CachedLeftController = nullptr;

	float CurGraspR = 0.0f;
	float CurGraspL = 0.0f;
	float CurCurlR = 0.0f;
	float CurCurlL = 0.0f;
};
