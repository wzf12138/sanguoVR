// VR 三国演武场 - UVRMovementProfile 移动配置数据资产基类
// 平滑移动/战术瞬移/转向参数（standards/04 + systems/04）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "VRMovementProfile.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRMovementProfile : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRMovementProfile()
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
		if (MoveSpeed < 0.0f || TeleportMaxDist < 0.0f || TeleportCooldown < 0.0f || TurnAngleDeg < 0.0f)
		{
			OutError = TEXT("移动参数存在负值");
			return false;
		}
		return true;
	}

	/** 平滑移动速度（cm/s） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Movement", meta = (ClampMin = "0.0"))
	float MoveSpeed = 200.0f;

	/** 瞬移最大距离（cm） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Movement", meta = (ClampMin = "0.0"))
	float TeleportMaxDist = 1500.0f;

	/** 瞬移冷却（秒） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Movement", meta = (ClampMin = "0.0"))
	float TeleportCooldown = 0.0f;

	/** 平滑转向角度（度/次） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Movement", meta = (ClampMin = "0.0"))
	float TurnAngleDeg = 45.0f;

	/** 舒适度预设（保留扩展空间，T005 最小占位） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Movement")
	FName ComfortPreset = TEXT("Default");

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
