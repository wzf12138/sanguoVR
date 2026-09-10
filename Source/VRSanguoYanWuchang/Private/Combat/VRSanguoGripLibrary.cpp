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
		// 接口事件必须经 Execute_ 静态转发调用：直调生成代码中的 thunk 会触发引擎断言崩溃
		// （事故案例：2026-09-08 抓剑闪退，VRGripInterface.gen.cpp:468 "Call Execute_DenyGripping instead"）
		return !IVRGripInterface::Execute_DenyGripping(Actor, Controller);
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

	UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断] 起点=(%.1f,%.1f,%.1f) 前向=(%.2f,%.2f,%.2f) 终点=(%.1f,%.1f,%.1f) 半径=%.1f 前距=%.1f Socket=%s"),
		Start.X, Start.Y, Start.Z, Forward.X, Forward.Y, Forward.Z,
		End.X, End.Y, End.Z, SphereRadius, ForwardDistance, *OptionalSocketName.ToString());

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
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断] 前方未检测到物体（bHit=%d, 命中数=%d）"), (int)bHit, Hits.Num());
		return false;
	}

	UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断] 扫掠命中 %d 个物体，开始筛选最近的可抓取物"), Hits.Num());

	// 在命中集中挑选最近的可抓取 Actor
	AActor* BestActor = nullptr;
	double BestDistance = TNumericLimits<double>::Max();
	for (const FHitResult& Hit : Hits)
	{
		AActor* HitActor = Hit.GetActor();
		if (!IsValid(HitActor))
		{
			UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断]   命中无效 actor，跳过"));
			continue;
		}
		if (!IsGrippableActor(HitActor, MotionController))
		{
			UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断]   命中 %s 不可抓取（未实现接口或 DenyGripping=true），跳过"), *HitActor->GetName());
			continue;
		}
		const double DistSq = (HitActor->GetActorLocation() - Start).SizeSquared();
		const double Dist = FMath::Sqrt(DistSq);
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断]   命中 %s 可抓取，距离=%.1fcm"), *HitActor->GetName(), Dist);
		if (DistSq < BestDistance)
		{
			BestDistance = DistSq;
			BestActor = HitActor;
		}
	}

	if (!IsValid(BestActor))
	{
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGrip诊断] 命中集中无可抓取物（共 %d 个命中均不可抓）"), Hits.Num());
		return false;
	}

	UE_LOG(LogVRSanguoWeapon, Log, TEXT("选定最近可抓取物=%s"), *BestActor->GetName());

	// [TryGripV2] 特征日志：证明新代码生效链 + socket 检测结果（姿态问题的决定性诊断）
	if (UPrimitiveComponent* RootComp = Cast<UPrimitiveComponent>(BestActor->GetRootComponent()))
	{
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGripV2] Socket=%s HasSocket=%d CollisionType=AttachmentGrip(9) bIsSlotGrip=1"),
			*OptionalSocketName.ToString(),
			(int)RootComp->DoesSocketExist(OptionalSocketName));
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
		// AttachmentGrip：纯对齐握持，刀姿态完全由 socket transform 冞定（物理交互式会被台座等碰撞顶偏姿态）
		EGripCollisionType::AttachmentGrip,
		EGripLateUpdateSettings::NotWhenCollidingOrDoubleGripping,
		EGripMovementReplicationSettings::ForceClientSideMovement,
		/*GripStiffness*/ 2250.0f,
		/*GripDamping*/ 140.0f,
		// 传入 socket 名即为 slot grip：启用 socket 的位置+旋转对齐（否则仅吸附位置、姿态保持抓取瞬间）
		/*bIsSlotGrip*/ true);

	if (bGripped)
	{
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("TryGrip: 抓取成功 Actor=%s Socket=%s"),
			*BestActor->GetName(), *OptionalSocketName.ToString());

		// [TryGripV2] 姿态决定性诊断：打印 grip 实际使用的相对变换（socket 分支应为 socket 逆变换）
		TArray<FBPActorGripInformation> ActiveGrips;
		MotionController->GetAllGrips(ActiveGrips);
		for (const FBPActorGripInformation& GripInfo : ActiveGrips)
		{
			if (GripInfo.GrippedObject == BestActor)
			{
				UE_LOG(LogVRSanguoWeapon, Log, TEXT("[TryGripV2] GripDetail Slot=%s RelTrans=%s CollType=%d"),
					*GripInfo.SlotName.ToString(), *GripInfo.RelativeTransform.ToString(), (int32)GripInfo.GripCollisionType);
				break;
			}
		}
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
