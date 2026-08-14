// VR 三国演武场 - UVRCommanderDefinition 武将数据资产基类
// 武将 ID/显示名/武器池/特殊技/阶段行为（standards/04）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Data/VRWeaponDefinition.h"
#include "VRCommanderDefinition.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRCommanderDefinition : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRCommanderDefinition()
		: CommanderID(FGuid::NewGuid())
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
		if (DisplayName.IsEmpty())
		{
			OutError = TEXT("DisplayName 为空");
			return false;
		}
		return true;
	}

	/** 稳定标识 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Commander")
	FGuid CommanderID;

	/** 显示名 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Commander")
	FText DisplayName;

	/** 可用武器池 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Commander")
	TArray<TObjectPtr<UVRWeaponDefinition>> WeaponPool;

	/** 特殊技（保留扩展空间，T005 最小占位） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Commander")
	TArray<FName> SpecialMoves;

	/** 阶段行为（战斗阶段 -> 行为配置，T005 最小占位） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Commander")
	TMap<FName, FName> PhaseBehavior;

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
