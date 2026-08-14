// VR 三国演武场 - IBattleParticipant 接口
// 出生、战斗状态、胜负与重置（standards/05 C++ 声明为准）

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "Core/VRTypes.h"
#include "VRBattleParticipant.generated.h"

UINTERFACE(BlueprintType)
class UBattleParticipant : public UInterface
{
	GENERATED_BODY()
};

class IBattleParticipant
{
	GENERATED_BODY()

public:
	/** 战斗开始 */
	UFUNCTION(BlueprintNativeEvent, Category = "Battle")
	void OnBattleStart();

	/** 战斗结束并给出胜负结果 */
	UFUNCTION(BlueprintNativeEvent, Category = "Battle")
	void OnBattleEnd(EBattleOutcome Outcome);

	/** 重置以准备下一回合 */
	UFUNCTION(BlueprintNativeEvent, Category = "Battle")
	void ResetForNextRound();
};
