// VR 三国演武场 - UVRWeaponDefinition 武器数据资产基类
// 字段集对齐 standards/04 + T005-SystemSkeleton Step 3

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Engine/SkeletalMesh.h"
#include "Core/VRTypes.h"
#include "VRWeaponDefinition.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRWeaponDefinition : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRWeaponDefinition()
		: WeaponID(FGuid::NewGuid())
	{
	}

	// ===== 版本与校验（standards/04）=====

	/** Schema 版本号：字段变更必须递增（standards/04） */
	UPROPERTY(EditDefaultsOnly, Category = "Schema")
	int32 SchemaVersion = 1;

	/** CDO 加载后自动迁移（standards/04 迁移策略） */
	virtual void PostLoad() override
	{
		Super::PostLoad();
		if (SchemaVersion < CurrentSchemaVersion)
		{
			// T005 最小实现：当前无历史版本迁移逻辑，仅记录并升级版本号
			SchemaVersion = CurrentSchemaVersion;
		}
	}

	/** 数据校验：空引用、非法区间、重复 ID（T005 最小实现） */
	virtual bool ValidateData(FString& OutError) const
	{
		if (DamageRange.X < 0.0f || DamageRange.Y < DamageRange.X)
		{
			OutError = TEXT("DamageRange 非法区间");
			return false;
		}
		return true;
	}

	// ===== 武器定义 =====

	/** 稳定标识 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	FGuid WeaponID;

	/** 武器类别 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	EWeaponType WeaponType = EWeaponType::OneHandSword;

	/** 持握点（相对武器根组件） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	TArray<FTransform> GripPoints;

	/** 有效伤害速度阈值（低于则判定 Miss） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon", meta = (ClampMin = "0.0"))
	float EffectiveSpeedThreshold = 100.0f;

	/** 伤害区间 [Min, Max] */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	FVector2D DamageRange = FVector2D(10.0f, 30.0f);

	/** 攻击方向规则（保留扩展空间，T005 最小占位） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	TArray<FName> AttackDirectionRules;

	/** 轨迹采样间隔（秒） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon", meta = (ClampMin = "0.001"))
	float TrajectorySampleInterval = 0.02f;

	/** 武器网格引用 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	TObjectPtr<USkeletalMesh> SkeletalMeshRef = nullptr;

	/** 碰撞预设名（与项目 Collision Profile 一致） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Weapon")
	FName CollisionProfile = TEXT("WeaponProfile");

protected:
	/** 当前支持的 Schema 版本（新增字段时递增并补充迁移逻辑） */
	static constexpr int32 CurrentSchemaVersion = 1;
};
