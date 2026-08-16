// VR 三国演武场 - 流程状态机自动化测试声明
// T006 Step 4：验证 VRGameFlowComponent 合法/非法迁移、委托广播、幂等重置

#pragma once

#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"

#if WITH_DEV_AUTOMATION_TESTS

// 合法迁移链路 + 非法迁移拒绝 + 幂等 + 委托广播
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRGameFlowTransitionSpec, "VRSanguo.GameFlow.Transition",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

// StartMatch / EndMatch / ResetMatch 生命周期
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FVRGameFlowMatchLifecycleSpec, "VRSanguo.GameFlow.MatchLifecycle",
	EAutomationTestFlags_ApplicationContextMask | EAutomationTestFlags::EngineFilter);

#endif // WITH_DEV_AUTOMATION_TESTS
