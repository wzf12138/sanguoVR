// VR 三国演武场 - UVRUnitDefinition 兵种单位数据资产基类
// 兵种类型与 AI 等级分离（standards/04 + SquadAI 详规）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "BehaviorTree/BehaviorTree.h"
#include "VRUnitDefinition.generated.h"
/** 兵种类型（AI 等级与兵种类型分离） */
UENUM(BlueprintType)
enum class EUnitType : uint8
{
	SwordShield		UMETA(DisplayName = "Sword Shield"),
	Spearman		UMETA(DisplayName = "Spearman"),
	Polearm			UMETA(DisplayName = "Polearm"),
	Archer			UMETA(DisplayName = "Archer"),
	Elite			UMETA(DisplayName = "Elite"),
};

/** 战斗风格倾向 */
UENUM(BlueprintType)
enum class ECombatStyle : uint8
{
	Aggressive	UMETA(DisplayName = "Aggressive"),
	Balanced	UMETA(DisplayName = "Balanced"),
	Defensive	UMETA(DisplayName = "Defensive"),
};

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRUnitDefinition : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRUnitDefinition()
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
		if (PerceptionRadius < 0.0f)
		{
			OutError = TEXT("PerceptionRadius 不能为负");
			return false;
		}
		return true;
	}

	/** 兵种类型 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Unit")
	EUnitType UnitType = EUnitType::SwordShield;

	/** 感知半径（cm） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Unit", meta = (ClampMin = "0.0"))
	float PerceptionRadius = 800.0f;

	/** 战斗风格 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Unit")
	ECombatStyle CombatStyle = ECombatStyle::Balanced;

	/** 装备引用（武器/护甲 DA） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Unit")
	TArray<TObjectPtr<UPrimaryDataAsset>> EquipmentRefs;

	/** 行为树引用 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Unit")
	TObjectPtr<UBehaviorTree> BehaviorTreeRef = nullptr;

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
