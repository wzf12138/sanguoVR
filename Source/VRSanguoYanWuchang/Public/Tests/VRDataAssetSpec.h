// VR 三国演武场 - DataAsset 校验自动化测试声明
// T006 Step 3：验证 T005 八个 DA 基类的 SchemaVersion/ValidateData/关键字段

#pragma once

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

// 武器数据资产：SchemaVersion 默认值 + ValidateData 区间检测
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRWeaponDefinitionSpec, "VRSanguo.DataAsset.WeaponDefinition",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 护甲数据资产：CoverageMap 非空 + HitZoneModifier 范围
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRArmorDefinitionSpec, "VRSanguo.DataAsset.ArmorDefinition",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 移动配置：TeleportMaxDist > 0 + TeleportCooldown >= 0
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRMovementProfileSpec, "VRSanguo.DataAsset.MovementProfile",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 比赛规则：DefaultTeamSize = 3 + AllowedSizes 覆盖 2-4
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRMatchRuleSetSpec, "VRSanguo.DataAsset.MatchRuleSet",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 兵种单位：UnitType 有效 + EquipmentRefs 可解析
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRUnitDefinitionSpec, "VRSanguo.DataAsset.UnitDefinition",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 武将：CommanderID 非空 + WeaponPool 非空
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRCommanderDefinitionSpec, "VRSanguo.DataAsset.CommanderDefinition",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 竞技场：Boundary 有效 + SpawnPoints >= 2
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRArenaDefinitionSpec, "VRSanguo.DataAsset.ArenaDefinition",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 角色外观：HitZoneBoneMapping 覆盖 6 个部位
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRAvatarProfileSpec, "VRSanguo.DataAsset.AvatarProfile",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

#endif // WITH_DEV_AUTOMATION_TESTS
