// VR 三国演武场 - UVRAvatarProfile 角色外观数据资产基类
// 网格/IK 配置/部位骨骼映射/手部网格（standards/04）

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "Engine/SkeletalMesh.h"
#include "Core/VRTypes.h"
#include "VRAvatarProfile.generated.h"

UCLASS(BlueprintType)
class VRSANGUOYANWUCHANG_API UVRAvatarProfile : public UPrimaryDataAsset
{
	GENERATED_BODY()

public:
	UVRAvatarProfile()
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
		if (SkeletalMeshRef == nullptr)
		{
			OutError = TEXT("SkeletalMeshRef 为空");
			return false;
		}
		return true;
	}

	/** 主网格引用 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Avatar")
	TObjectPtr<USkeletalMesh> SkeletalMeshRef = nullptr;

	/** IK 配置名 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Avatar")
	FName IKProfile = TEXT("Default");

	/** 部位骨骼映射：EHitZone -> 骨骼名 */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Avatar")
	TMap<EHitZone, FName> HitZoneBoneMapping;

	/** 手部网格（左手/右手） */
	UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Avatar")
	TArray<TObjectPtr<USkeletalMesh>> HandMeshes;

protected:
	static constexpr int32 CurrentSchemaVersion = 1;
};
