// VR 三国演武场 - 接口自动化测试声明
// T006 Step 4：验证 T005 接口实现（VRCharacterCapabilityComponent / AVRTestDummy）

#pragma once

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

// 角色能力接口：组件挂载 + RequestAction 桩返回 false + GetCapabilityState Idle
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRCharacterCapabilitySpec, "VRSanguo.Interface.CharacterCapability",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// 测试桩：AVRTestDummy 生成 + ReceiveDamage 日志 + IsAlive true
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRTestDummySpec, "VRSanguo.Interface.TestDummy",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

#endif // WITH_DEV_AUTOMATION_TESTS
