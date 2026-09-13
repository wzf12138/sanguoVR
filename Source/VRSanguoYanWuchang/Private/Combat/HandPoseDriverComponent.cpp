// VR 三国演武场 - UHandPoseDriverComponent 实现
// 桥接路径：EnhancedInput 轴值 → UAnimInstance::SetVariable*（按名写，无需 Cast ABP 类型）
// 写入的变量全部来自官方 ABP_MannequinsXR：PoseAlphaGrasp / PoseAlphaIndexCurl / bMirror

#include "Combat/HandPoseDriverComponent.h"

#include "Animation/AnimInstance.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/World.h"
#include "EnhancedPlayerInput.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/PlayerController.h"
#include "GripMotionControllerComponent.h"
#include "InputAction.h"

UHandPoseDriverComponent::UHandPoseDriverComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.TickGroup = TG_PrePhysics;
}

void UHandPoseDriverComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	DriveHandPoses(DeltaTime);
}

void UHandPoseDriverComponent::DriveHandPoses(float DeltaTime)
{
	const UEnhancedPlayerInput* EnhancedInput = ResolveEnhancedInput();
	if (!EnhancedInput)
	{
		return;
	}

	const float GraspR = EnhancedInput->GetActionValue(GraspActionRight).GetMagnitude();
	const float GraspL = EnhancedInput->GetActionValue(GraspActionLeft).GetMagnitude();
	const float CurlR = EnhancedInput->GetActionValue(IndexCurlActionRight).GetMagnitude();
	const float CurlL = EnhancedInput->GetActionValue(IndexCurlActionLeft).GetMagnitude();

	// 平滑：轴值连续但避免姿势跳变；ABP 内 Point/ThumbUp 有自身插值，Grasp/IndexCurl 无，这里统一补
	if (PoseLerpSpeed > KINDA_SMALL_NUMBER)
	{
		const float Alpha = FMath::Clamp(DeltaTime * PoseLerpSpeed, 0.0f, 1.0f);
		CurGraspR = FMath::Lerp(CurGraspR, GraspR, Alpha);
		CurGraspL = FMath::Lerp(CurGraspL, GraspL, Alpha);
		CurCurlR = FMath::Lerp(CurCurlR, CurlR, Alpha);
		CurCurlL = FMath::Lerp(CurCurlL, CurlL, Alpha);
	}
	else
	{
		CurGraspR = GraspR;
		CurGraspL = GraspL;
		CurCurlR = CurlR;
		CurCurlL = CurlL;
	}

	// 空手按 grip = 官方握拳；握着武器按 grip = 圆柱姿势（ABP_MannequinsXR 的 IsGrippingWeapon 开关）
	ApplyPose(ResolveHandMesh(true), CurGraspR, CurCurlR, /*bMirror*/ false, ResolveHandHoldingWeapon(true));
	ApplyPose(ResolveHandMesh(false), CurGraspL, CurCurlL, /*bMirror*/ true, ResolveHandHoldingWeapon(false));
}

void UHandPoseDriverComponent::ApplyPose(USkeletalMeshComponent* Mesh, float GraspAlpha, float CurlAlpha, bool bMirror, bool bHoldingWeapon) const
{
	if (!Mesh)
	{
		return;
	}

	UAnimInstance* AnimInstance = Mesh->GetAnimInstance();
	if (!AnimInstance)
	{
		return;
	}

	// UE5.6 的 UAnimInstance 不暴露 SetVariable* API，直接按反射属性写蓝图变量（等价于蓝图 Set 节点）
	WriteAnimDouble(AnimInstance, TEXT("PoseAlphaGrasp"), GraspAlpha);
	WriteAnimDouble(AnimInstance, TEXT("PoseAlphaIndexCurl"), CurlAlpha);
	WriteAnimBool(AnimInstance, TEXT("bMirror"), bMirror);
	WriteAnimBool(AnimInstance, TEXT("IsGrippingWeapon"), bHoldingWeapon);
}

void UHandPoseDriverComponent::WriteAnimDouble(UAnimInstance* AnimInstance, const FName& VarName, float Value) const
{
	if (const FDoubleProperty* Property = CastField<FDoubleProperty>(AnimInstance->GetClass()->FindPropertyByName(VarName)))
	{
		Property->SetPropertyValue_InContainer(AnimInstance, static_cast<double>(Value));
	}
}

void UHandPoseDriverComponent::WriteAnimBool(UAnimInstance* AnimInstance, const FName& VarName, bool bValue) const
{
	if (const FBoolProperty* Property = CastField<FBoolProperty>(AnimInstance->GetClass()->FindPropertyByName(VarName)))
	{
		Property->SetPropertyValue_InContainer(AnimInstance, bValue);
	}
}

USkeletalMeshComponent* UHandPoseDriverComponent::ResolveHandMesh(bool bRight)
{
	const FName TargetName = bRight ? RightHandMeshName : LeftHandMeshName;
	TObjectPtr<USkeletalMeshComponent>& Cache = bRight ? CachedRightMesh : CachedLeftMesh;

	if (Cache != nullptr)
	{
		// 组件被移除/重建时失效缓存
		if (IsValid(Cache.Get()) && Cache->GetFName() == TargetName)
		{
			return Cache.Get();
		}
		Cache = nullptr;
	}

	AActor* Owner = GetOwner();
	if (!Owner)
	{
		return nullptr;
	}

	USkeletalMeshComponent* Found = nullptr;
	TArray<USkeletalMeshComponent*> Meshes;
	Owner->GetComponents<USkeletalMeshComponent>(Meshes);
	for (USkeletalMeshComponent* Mesh : Meshes)
	{
		if (Mesh && Mesh->GetFName() == TargetName)
		{
			Found = Mesh;
			break;
		}
	}

	if (Found)
	{
		Cache = Found;
	}
	return Found;
}

UEnhancedPlayerInput* UHandPoseDriverComponent::ResolveEnhancedInput()
{
	const APawn* Pawn = GetOwner<APawn>();
	if (!Pawn)
	{
		return nullptr;
	}

	const APlayerController* PC = Cast<APlayerController>(Pawn->Controller);
	return PC ? Cast<UEnhancedPlayerInput>(PC->PlayerInput) : nullptr;
}

bool UHandPoseDriverComponent::ResolveHandHoldingWeapon(bool bRight)
{
	TObjectPtr<UGripMotionControllerComponent>& Cache = bRight ? CachedRightController : CachedLeftController;

	if (Cache != nullptr)
	{
		if (IsValid(Cache.Get()))
		{
			return Cache->HasGrippedObjects();
		}
		Cache = nullptr;
	}

	AActor* Owner = GetOwner();
	if (!Owner)
	{
		return false;
	}

	// 按手别（HandType）匹配对应的 GripMotionController，缓存后每帧只做 HasGrippedObjects 查询
	TArray<UGripMotionControllerComponent*> Controllers;
	Owner->GetComponents<UGripMotionControllerComponent>(Controllers);
	const EControllerHand TargetHand = bRight ? EControllerHand::Right : EControllerHand::Left;

	for (UGripMotionControllerComponent* Controller : Controllers)
	{
		if (!Controller)
		{
			continue;
		}

		EControllerHand Hand = EControllerHand::Left;
		Controller->GetHandType(Hand);
		if (Hand != TargetHand)
		{
			continue;
		}

		Cache = Controller;
		return Controller->HasGrippedObjects();
	}

	return false;
}
