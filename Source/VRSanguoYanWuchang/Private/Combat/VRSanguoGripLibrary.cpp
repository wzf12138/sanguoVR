// VR 三国演武场 - UVRSanguoGripLibrary 实现

#include "Combat/VRSanguoGripLibrary.h"

#include "Core/VRLogChannels.h"
#include "GripMotionControllerComponent.h"
#include "VRGripInterface.h"

#include "Components/PrimitiveComponent.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

// 覆盖引擎自带 PrimitiveComponent 头，避免与 VRE 的 Forward/Included 头冲突
#include "Engine/Engine.h"

namespace
{
	/** 判断 Actor 是否为 VRE 可抓取对象（实现 IVRGripInterface 且未被禁止抓取） */
	bool IsGrippableActor(AActor* Actor, UGripMotionControllerComponent* Controller)
	{
		if (!IsValid(Actor) || !Actor->Implements<UVRGripInterface>())
		{
			return false;
		}

		// DenyGripping 为 true 时禁止抓取，默认允许
		const IVRGripInterface* GripInterface = Cast<IVRGripInterface>(Actor);
		if (!GripInterface)
		{
			return false;
		}

		// 注意：DenyGripping 不是 const 成员函数，需经非 const 化后调用
		return !const_cast<IVRGripInterface*>(GripInterface)->DenyGripping(Controller);
	}
}

bool UVRSanguoGripLibrary::TryGrip(
	UGripMotionControllerComponent* MotionController,
	float SphereRadius,
	float ForwardDistance,
	FName OptionalSocketName)
{
	if (!IsValid(MotionController))
	{
		UE_LOG(LogVRSanguoWeapon, Warning, TEXT("TryGrip: 无效手柄组件"));
		return false;
	}

	UWorld* World = MotionController->GetWorld();
	if (!IsValid(World))
	{
		UE_LOG(LogVRSanguoWeapon, Warning, TEXT("TryGrip: 无 World"));
		return false;
	}

	// 探测起点与方向：手柄世界位置 + 手柄前向
	const FVector Start = MotionController->GetComponentLocation();
	const FVector Forward = MotionController->GetForwardVector();
	// 终点：手柄前方 ForwardDistance 处
	const FVector End = Start + Forward * ForwardDistance;

	// 球形扫掠/重叠检测：寻找手柄前方最近的可抓取物
	TArray<FHitResult> Hits;
	FCollisionShape Shape = FCollisionShape::MakeSphere(SphereRadius);

	// 从手柄到前方终点做球体扫掠，避免漏掉手柄与目标之间的物体
	FCollisionQueryParams QueryParams(TEXT("VRSanguoGripSweep"), false);
	QueryParams.bTraceComplex = false;
	QueryParams.AddIgnoredActor(MotionController->GetOwner());

	const bool bHit = World->SweepMultiByChannel(
		Hits,
		Start,
		End,
		FQuat::Identity,
		ECC_Visibility,
		Shape,
		QueryParams);

	if (!bHit || Hits.Num() == 0)
	{
		UE_LOG(LogVRSanguoWeapon, Verbose, TEXT("TryGrip: 前方未检测到物体"));
		return false;
	}

	// 在命中集中挑选最近的可抓取 Actor
	AActor* BestActor = nullptr;
	double BestDistance = TNumericLimits<double>::Max();
	for (const FHitResult& Hit : Hits)
	{
		AActor* HitActor = Hit.GetActor();
		if (!IsGrippableActor(HitActor, MotionController))
		{
			continue;
		}
		const double DistSq = (HitActor->GetActorLocation() - Start).SizeSquared();
		if (DistSq < BestDistance)
		{
			BestDistance = DistSq;
			BestActor = HitActor;
		}
	}

	if (!IsValid(BestActor))
	{
		UE_LOG(LogVRSanguoWeapon, Verbose, TEXT("TryGrip: 命中集中无可抓取物"));
		return false;
	}

	// 世界偏移使用 IdenticalTransform（相对）+ socket 吸附由 VRE 自动匹配
	// 说明：传入有效 socket 名时 VRE 会吸附到该 socket；NAME_None 则自动匹配含 "Grip" 的 socket。
	const FTransform WorldOffset = FTransform::Identity;
	const bool bGripped = MotionController->GripObject(
		BestActor,
		WorldOffset,
		/*bWorldOffsetIsRelative*/ false,
		OptionalSocketName,
		NAME_None,
		EGripCollisionType::InteractiveCollisionWithPhysics,
		EGripLateUpdateSettings::NotWhenCollidingOrDoubleGripping,
		EGripMovementReplicationSettings::ForceClientSideMovement,
		/*GripStiffness*/ 2250.0f,
		/*GripDamping*/ 140.0f,
		/*bIsSlotGrip*/ false);

	if (bGripped)
	{
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("TryGrip: 抓取成功 Actor=%s Socket=%s"),
			*BestActor->GetName(), *OptionalSocketName.ToString());
	}
	else
	{
		UE_LOG(LogVRSanguoWeapon, Warning, TEXT("TryGrip: GripObject 返回失败 Actor=%s"), *BestActor->GetName());
	}

	return bGripped;
}

bool UVRSanguoGripLibrary::ReleaseGrip(UGripMotionControllerComponent* MotionController)
{
	if (!IsValid(MotionController))
	{
		UE_LOG(LogVRSanguoWeapon, Warning, TEXT("ReleaseGrip: 无效手柄组件"));
		return false;
	}

	// 取出当前握持的所有对象，逐个释放
	TArray<UObject*> GrippedObjects;
	MotionController->GetGrippedObjects(GrippedObjects);

	if (GrippedObjects.Num() == 0)
	{
		UE_LOG(LogVRSanguoWeapon, Verbose, TEXT("ReleaseGrip: 手柄当前未抓取任何物体"));
		return false;
	}

	bool bAnyReleased = false;
	for (UObject* Obj : GrippedObjects)
	{
		if (IsValid(Obj))
		{
			const bool bDropped = MotionController->DropObject(
				Obj,
				/*GripIdToDrop*/ 0,
				/*bSimulate*/ false,
				FVector::ZeroVector,
				FVector::ZeroVector);
			bAnyReleased |= bDropped;
			UE_LOG(LogVRSanguoWeapon, Log, TEXT("ReleaseGrip: 释放 %s -> %s"),
				*Obj->GetName(), bDropped ? TEXT("成功") : TEXT("失败"));
		}
	}

	return bAnyReleased;
}
