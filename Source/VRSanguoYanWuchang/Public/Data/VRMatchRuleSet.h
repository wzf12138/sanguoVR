// VR 三国演武场 - UVRMatchRuleSet 比赛规则集数据资产基类
// 队伍规模/回合/时限（standards/04 + systems/01）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "VRMatchRuleSet.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRMatchRuleSet : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRMatchRuleSet()
	{
	}

	/** Schema 版本号 */
	UPROPERTY(EditDefaultsOnly, Category = "Schema")
	int32 SchemaVersion = 1;

	virtual void PostLoad() override
	{
		Super::PostLoad();
		if (SchemaVersion < CurrentSchemaVersion)
		{
			SchemaVersion = CurrentSchemaVersion;
		}
	}

	/** 数据校验 */
	virtual bool ValidateData(FString& OutError) const
	{
		if (DefaultTeamSize < 1 || RoundCount < 1 || TimeLimit < 1.0f)
		{
			OutError = TEXT("比赛规则参数非法（队伍规模/回合/时限）");
			return false;
		}
		return true;
	}

	/** 默认队伍规模 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Match", meta = (ClampMin = "1"))
	int32 DefaultTeamSize = 3;

	/** 允许的队伍规模（2-4 常规） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Match")
	TArray<int32> AllowedSizes;

	/** 回合数 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Match", meta = (ClampMin = "1"))
	int32 RoundCount = 1;

	/** 单回合时限（秒） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Match", meta = (ClampMin = "1.0"))
	float TimeLimit = 120.0f;

	/** 断肢规则开关（占位，M03 后细化） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Match")
	bool bDismemberRule = false;

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
