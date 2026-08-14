// VR 三国演武场 - AVRTestDummy 测试桩角色
// 纯数据桩：实现 IDamageable + IBattleParticipant，用于 L_SkeletonTest 验证场景

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Interfaces/VRDamageable.h"
#include "Interfaces/VRBattleParticipant.h"
#include "Core/VRTypes.h"
#include "VRTestDummy.generated.h"

class UStaticMeshComponent;

UCLASS()
class VRSANGUOYANWUCHANG_API AVRTestDummy : public AActor, public IDamageable, public IBattleParticipant
{
	GENERATED_BODY()

public:
	AVRTestDummy();

	// ===== IDamageable（systems/03）=====

	/** 记录日志并打印 FCombatResult 各字段 */
	virtual void ReceiveDamage_Implementation(const FCombatResult& Result) override;

	/** T005 固定返回 true */
	virtual bool IsAlive_Implementation() const override { return true; }

	/** T005 固定返回 1.0 */
	virtual float GetHealthRatio_Implementation() const override { return 1.0f; }

	// ===== IBattleParticipant（standards/05）=====

	virtual void OnBattleStart_Implementation() override;

	virtual void OnBattleEnd_Implementation(EBattleOutcome Outcome) override;

	virtual void ResetForNextRound_Implementation() override;

protected:
	/** 可见占位网格（Dev 测试用） */
	UPROPERTY(VisibleAnywhere, Category = "Dummy")
	TObjectPtr<UStaticMeshComponent> MeshComponent = nullptr;
};
