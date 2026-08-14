// VR 三国演武场 - IDamageable 接口
// 接收已解析伤害与死亡结果（standards/05 + systems/03 契约）

#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "Core/VRTypes.h"
#include "VRDamageable.generated.h"

UINTERFACE(BlueprintType)
class UDamageable : public UInterface
{
	GENERATED_BODY()
};

class IDamageable
{
	GENERATED_BODY()

public:
	/** 接收已解析的伤害结果 */
	UFUNCTION(BlueprintNativeEvent, Category = "Combat")
	void ReceiveDamage(const FCombatResult& Result);

	/** 是否存活 */
	UFUNCTION(BlueprintNativeEvent, Category = "Combat")
	bool IsAlive() const;

	/** 生命值比例 [0,1] */
	UFUNCTION(BlueprintNativeEvent, Category = "Combat")
	float GetHealthRatio() const;
};
