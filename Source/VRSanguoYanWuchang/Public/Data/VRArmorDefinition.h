// VR 三国演武场 - UVRArmorDefinition 护甲数据资产基类
// 分部位护甲覆盖率与抗性（standards/04 + HealthAndArmor 详规口径）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Core/VRTypes.h"
#include "VRArmorDefinition.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRArmorDefinition : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRArmorDefinition()
		: ArmorID(FGuid::NewGuid())
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
		if (HitZoneModifier < 0.0f)
		{
			OutError = TEXT("HitZoneModifier 不能为负");
			return false;
		}
		return true;
	}

	/** 稳定标识 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Armor")
	FGuid ArmorID;

	/** 部位覆盖率：EHitZone -> [0,1]，0=未覆盖 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Armor")
	TMap<EHitZone, float> CoverageMap;

	/** 部位抗性：EHitZone -> [0,1]，1=完全免伤 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Armor")
	TMap<EHitZone, float> ResistanceMap;

	/** 部位伤害修正（全局乘数，>1 增伤 <1 减伤） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Armor", meta = (ClampMin = "0.0"))
	float HitZoneModifier = 1.0f;

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
