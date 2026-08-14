// VR 三国演武场 - UVRArenaDefinition 竞技场数据资产基类
// 边界/出生点/导航/光照预设（standards/04）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Engine/World.h"
#include "VRArenaDefinition.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRArenaDefinition : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRArenaDefinition()
		: ArenaID(FGuid::NewGuid())
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
		if (Boundary.X <= 0.0f || Boundary.Y <= 0.0f || Boundary.Z <= 0.0f)
		{
			OutError = TEXT("Boundary 必须为正");
			return false;
		}
		return true;
	}

	/** 稳定标识 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Arena")
	FGuid ArenaID;

	/** 竞技场边界（Box 半长） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Arena")
	FVector Boundary = FVector(2000.0f, 2000.0f, 500.0f);

	/** 出生点（相对竞技场中心） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Arena")
	TArray<FTransform> SpawnPoints;

	/** 导航网格引用 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Arena")
	TObjectPtr<UWorld> NavMeshRef = nullptr;

	/** 光照预设名 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Arena")
	FName LightingPreset = TEXT("Day");

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
