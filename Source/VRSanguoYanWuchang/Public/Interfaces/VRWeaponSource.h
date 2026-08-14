// VR 三国演武场 - IWeaponSource 接口
// 武器数据、持握状态和攻击轨迹（standards/05 C++ 声明为准）

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "Core/VRTypes.h"
#include "VRWeaponSource.generated.h"

// 前向声明：UVRWeaponDefinition 由 Step 3 Data Asset 创建
class UVRWeaponDefinition;

UINTERFACE(BlueprintType)
class UWeaponSource : public UInterface
{
	GENERATED_BODY()
};

class IWeaponSource
{
	GENERATED_BODY()

public:
	/** 武器数据资产 */
	UFUNCTION(BlueprintNativeEvent, Category = "Weapon")
	UVRWeaponDefinition* GetWeaponData() const;

	/** 是否双手持握 */
	UFUNCTION(BlueprintNativeEvent, Category = "Weapon")
	bool IsTwoHanded() const;

	/** 攻击轨迹采样 */
	UFUNCTION(BlueprintNativeEvent, Category = "Weapon")
	TArray<FWeaponTrajectorySample> GetTrajectory() const;
};
