// VR 三国演武场 - DataAsset 校验自动化测试实现
// T006 Step 3：用例对齐 T005 实际字段（详规 2026-08-15 修正）

#include "Tests/VRDataAssetSpec.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Data/VRWeaponDefinition.h"
#include "Data/VRArmorDefinition.h"
#include "Data/VRMovementProfile.h"
#include "Data/VRMatchRuleSet.h"
#include "Data/VRUnitDefinition.h"
#include "Data/VRCommanderDefinition.h"
#include "Data/VRArenaDefinition.h"
#include "Data/VRAvatarProfile.h"

bool FVRWeaponDefinitionSpec::RunTest(const FString& Parameters)
{
	// SchemaVersion 默认值 = 1
	UVRWeaponDefinition* Weapon = NewObject<UVRWeaponDefinition>();
	TestEqual(TEXT("Weapon SchemaVersion 默认值应为 1"), Weapon->SchemaVersion, 1);

	// ValidateData()：默认 DamageRange(10,30) 合法
	FString Error;
	TestTrue(TEXT("Weapon 默认数据应通过 ValidateData"), Weapon->ValidateData(Error));

	// 非法区间：DamageRange.X < 0
	Weapon->DamageRange = FVector2D(-5.0f, 30.0f);
	TestFalse(TEXT("Weapon DamageRange.X<0 应被拒绝"), Weapon->ValidateData(Error));
	TestTrue(TEXT("拒绝时应返回错误信息"), !Error.IsEmpty());

	// 非法区间：DamageRange.Y < DamageRange.X
	Error.Empty();
	Weapon->DamageRange = FVector2D(30.0f, 10.0f);
	TestFalse(TEXT("Weapon DamageRange.Y<X 应被拒绝"), Weapon->ValidateData(Error));

	// 有效速度阈值不应为负
	Weapon->DamageRange = FVector2D(10.0f, 30.0f);
	Weapon->EffectiveSpeedThreshold = 0.0f; // 合法边界
	TestTrue(TEXT("Weapon 阈值 0 仍应通过"), Weapon->ValidateData(Error));

	return true;
}

bool FVRArmorDefinitionSpec::RunTest(const FString& Parameters)
{
	UVRArmorDefinition* Armor = NewObject<UVRArmorDefinition>();
	TestEqual(TEXT("Armor SchemaVersion 默认值应为 1"), Armor->SchemaVersion, 1);

	// CoverageMap 非空（默认空，填充 2 个部位）
	TestTrue(TEXT("Armor CoverageMap 默认应为空"), Armor->CoverageMap.Num() == 0);
	Armor->CoverageMap.Add(EHitZone::Torso, 1.0f);
	Armor->CoverageMap.Add(EHitZone::Head, 1.0f);
	TestEqual(TEXT("Armor CoverageMap 填充后应为 2"), Armor->CoverageMap.Num(), 2);

	// HitZoneModifier 默认 1.0（在 0-1 范围）
	TestEqual(TEXT("Armor HitZoneModifier 默认应为 1.0"), Armor->HitZoneModifier, 1.0f);

	// ValidateData：默认通过
	FString Error;
	TestTrue(TEXT("Armor 默认数据应通过 ValidateData"), Armor->ValidateData(Error));

	// 非法：HitZoneModifier < 0
	Armor->HitZoneModifier = -1.0f;
	TestFalse(TEXT("Armor HitZoneModifier<0 应被拒绝"), Armor->ValidateData(Error));
	Armor->HitZoneModifier = 1.0f;

	return true;
}

bool FVRMovementProfileSpec::RunTest(const FString& Parameters)
{
	UVRMovementProfile* Profile = NewObject<UVRMovementProfile>();
	TestEqual(TEXT("Movement SchemaVersion 默认值应为 1"), Profile->SchemaVersion, 1);

	// TeleportMaxDist > 0（默认 1500）
	TestTrue(TEXT("Movement TeleportMaxDist 应 > 0"), Profile->TeleportMaxDist > 0.0f);

	// TeleportCooldown >= 0（默认 0）
	TestTrue(TEXT("Movement TeleportCooldown 应 >= 0"), Profile->TeleportCooldown >= 0.0f);

	// ValidateData：默认通过；负值拒绝
	FString Error;
	TestTrue(TEXT("Movement 默认数据应通过 ValidateData"), Profile->ValidateData(Error));
	Profile->TeleportMaxDist = -100.0f;
	TestFalse(TEXT("Movement TeleportMaxDist<0 应被拒绝"), Profile->ValidateData(Error));
	Profile->TeleportMaxDist = 1500.0f;

	return true;
}

bool FVRMatchRuleSetSpec::RunTest(const FString& Parameters)
{
	UVRMatchRuleSet* Rules = NewObject<UVRMatchRuleSet>();
	TestEqual(TEXT("MatchRuleSet SchemaVersion 默认值应为 1"), Rules->SchemaVersion, 1);

	// DefaultTeamSize = 3
	TestEqual(TEXT("MatchRuleSet DefaultTeamSize 默认应为 3"), Rules->DefaultTeamSize, 3);

	// AllowedSizes 填充 2-4
	Rules->AllowedSizes = { 2, 3, 4 };
	TestTrue(TEXT("MatchRuleSet AllowedSizes 应包含 2"), Rules->AllowedSizes.Contains(2));
	TestTrue(TEXT("MatchRuleSet AllowedSizes 应包含 3"), Rules->AllowedSizes.Contains(3));
	TestTrue(TEXT("MatchRuleSet AllowedSizes 应包含 4"), Rules->AllowedSizes.Contains(4));

	// ValidateData：默认通过；DefaultTeamSize=0 拒绝
	FString Error;
	TestTrue(TEXT("MatchRuleSet 默认数据应通过 ValidateData"), Rules->ValidateData(Error));
	Rules->DefaultTeamSize = 0;
	TestFalse(TEXT("MatchRuleSet DefaultTeamSize=0 应被拒绝"), Rules->ValidateData(Error));
	Rules->DefaultTeamSize = 3;

	return true;
}

bool FVRUnitDefinitionSpec::RunTest(const FString& Parameters)
{
	UVRUnitDefinition* Unit = NewObject<UVRUnitDefinition>();
	TestEqual(TEXT("Unit SchemaVersion 默认值应为 1"), Unit->SchemaVersion, 1);

	// UnitType 默认 SwordShield（有效枚举值）
	TestEqual(TEXT("Unit UnitType 默认应为 SwordShield"), Unit->UnitType, EUnitType::SwordShield);

	// EquipmentRefs 默认空（无引用可解析问题）
	TestTrue(TEXT("Unit EquipmentRefs 默认应为空"), Unit->EquipmentRefs.Num() == 0);

	// ValidateData：默认通过
	FString Error;
	TestTrue(TEXT("Unit 默认数据应通过 ValidateData"), Unit->ValidateData(Error));

	return true;
}

bool FVRCommanderDefinitionSpec::RunTest(const FString& Parameters)
{
	UVRCommanderDefinition* Commander = NewObject<UVRCommanderDefinition>();

	// CommanderID 非空（构造函数生成 FGuid）
	TestTrue(TEXT("Commander CommanderID 应为有效 GUID"), Commander->CommanderID.IsValid());

	// WeaponPool 默认空（非空时需可解析——T005 阶段默认空通过）
	TestTrue(TEXT("Commander WeaponPool 默认应为空"), Commander->WeaponPool.Num() == 0);

	// ValidateData：DisplayName 为空默认拒绝（T005 校验规则）
	FString Error;
	TestFalse(TEXT("Commander DisplayName 为空应被拒绝"), Commander->ValidateData(Error));
	Commander->DisplayName = FText::FromString(TEXT("关羽"));
	TestTrue(TEXT("Commander 设置 DisplayName 后应通过"), Commander->ValidateData(Error));

	return true;
}

bool FVRArenaDefinitionSpec::RunTest(const FString& Parameters)
{
	UVRArenaDefinition* Arena = NewObject<UVRArenaDefinition>();
	TestEqual(TEXT("Arena SchemaVersion 默认值应为 1"), Arena->SchemaVersion, 1);

	// Boundary 默认 (2000,2000,500) 全正
	TestTrue(TEXT("Arena Boundary.X 应 > 0"), Arena->Boundary.X > 0.0f);
	TestTrue(TEXT("Arena Boundary.Y 应 > 0"), Arena->Boundary.Y > 0.0f);
	TestTrue(TEXT("Arena Boundary.Z 应 > 0"), Arena->Boundary.Z > 0.0f);

	// SpawnPoints 填充 2 个
	Arena->SpawnPoints.Add(FTransform());
	Arena->SpawnPoints.Add(FTransform());
	TestTrue(TEXT("Arena SpawnPoints 应 >= 2"), Arena->SpawnPoints.Num() >= 2);

	// ValidateData：默认通过；Boundary 负值拒绝
	FString Error;
	TestTrue(TEXT("Arena 默认数据应通过 ValidateData"), Arena->ValidateData(Error));
	Arena->Boundary = FVector(0.0f, 1000.0f, 500.0f);
	TestFalse(TEXT("Arena Boundary.X<=0 应被拒绝"), Arena->ValidateData(Error));
	Arena->Boundary = FVector(2000.0f, 2000.0f, 500.0f);

	return true;
}

bool FVRAvatarProfileSpec::RunTest(const FString& Parameters)
{
	UVRAvatarProfile* Avatar = NewObject<UVRAvatarProfile>();
	TestEqual(TEXT("Avatar SchemaVersion 默认值应为 1"), Avatar->SchemaVersion, 1);

	// HitZoneBoneMapping 默认空；填充 6 个部位后断言覆盖
	TestTrue(TEXT("Avatar HitZoneBoneMapping 默认应为空"), Avatar->HitZoneBoneMapping.Num() == 0);
	Avatar->HitZoneBoneMapping.Add(EHitZone::Head, TEXT("head"));
	Avatar->HitZoneBoneMapping.Add(EHitZone::Torso, TEXT("spine_02"));
	Avatar->HitZoneBoneMapping.Add(EHitZone::LeftArm, TEXT("clavicle_l"));
	Avatar->HitZoneBoneMapping.Add(EHitZone::RightArm, TEXT("clavicle_r"));
	Avatar->HitZoneBoneMapping.Add(EHitZone::LeftLeg, TEXT("thigh_l"));
	Avatar->HitZoneBoneMapping.Add(EHitZone::RightLeg, TEXT("thigh_r"));
	TestEqual(TEXT("Avatar HitZoneBoneMapping 应覆盖 6 个部位"), Avatar->HitZoneBoneMapping.Num(), 6);

	// ValidateData：SkeletalMeshRef 为空默认拒绝（T005 校验规则）
	FString Error;
	TestFalse(TEXT("Avatar SkeletalMeshRef 为空应被拒绝"), Avatar->ValidateData(Error));

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
