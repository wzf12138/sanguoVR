// VR 三国演武场 - AVRTestDummy 实现

#include "Combat/VRTestDummy.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Core/VRLogChannels.h"

AVRTestDummy::AVRTestDummy()
{
	PrimaryActorTick.bCanEverTick = false;

	MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("MeshComponent"));
	SetRootComponent(MeshComponent);

	// T005：无网格时使用引擎内置占位（编辑器 Dev 场景可见即可）
	static ConstructorHelpers::FObjectFinder<UStaticMesh> CubeMesh(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (CubeMesh.Succeeded())
	{
		MeshComponent->SetStaticMesh(CubeMesh.Object);
	}
	MeshComponent->SetWorldScale3D(FVector(0.5f, 0.5f, 1.5f));
	MeshComponent->SetCollisionEnabled(ECollisionEnabled::NoCollision);
}

void AVRTestDummy::ReceiveDamage_Implementation(const FCombatResult& Result)
{
	UE_LOG(LogVRSanguoCombat, Log, TEXT("[TestDummy] ReceiveDamage: Outcome=%s Damage=%.1f bWasBlocked=%d HitZoneFlags=%d"),
		*StaticEnum<ECombatOutcome>()->GetNameStringByValue((int64)Result.Outcome),
		Result.Damage,
		Result.bWasBlocked ? 1 : 0,
		Result.HitZoneFlags);
}

void AVRTestDummy::OnBattleStart_Implementation()
{
	UE_LOG(LogVRSanguoCombat, Log, TEXT("[TestDummy] OnBattleStart"));
}

void AVRTestDummy::OnBattleEnd_Implementation(EBattleOutcome Outcome)
{
	UE_LOG(LogVRSanguoCombat, Log, TEXT("[TestDummy] OnBattleEnd: Outcome=%s"),
		*StaticEnum<EBattleOutcome>()->GetNameStringByValue((int64)Outcome));
}

void AVRTestDummy::ResetForNextRound_Implementation()
{
	UE_LOG(LogVRSanguoCombat, Log, TEXT("[TestDummy] ResetForNextRound"));
}
