// VR 三国演武场 - 接口自动化测试实现
// T006 Step 4：用例对齐 T005 实际实现（桩行为）
// BlueprintNativeEvent 接口在 C++ 中必须通过 Execute_ 静态包装调用（不能直接调 Event 函数）

#include "Tests/VRInterfaceSpec.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Combat/VRCharacterCapabilityComponent.h"
#include "Combat/VRTestDummy.h"
#include "Core/VRTypes.h"

bool FVRCharacterCapabilitySpec::RunTest(const FString& Parameters)
{
	// 组件可挂载到任意 Actor
	AActor* Host = NewObject<AActor>();
	UVRCharacterCapabilityComponent* Capability = NewObject<UVRCharacterCapabilityComponent>(Host);
	TestNotNull(TEXT("Capability 组件应创建成功"), Capability);
	if (!Capability)
	{
		return true;
	}

	// 实现 ICharacterCapability 接口
	TestTrue(TEXT("Capability 应实现 ICharacterCapability"), Capability->Implements<UCharacterCapability>());

	// RequestAction 桩：返回 false（BlueprintNativeEvent 需 Execute_ 包装调用）
	FCapabilityRequest Request;
	Request.ActionTag = FGameplayTag::EmptyTag;
	TestFalse(TEXT("RequestAction 桩应返回 false（未实现）"),
		ICharacterCapability::Execute_RequestAction(Capability, Request));

	// IsActionAllowed 桩：返回 false
	TestFalse(TEXT("IsActionAllowed 桩应返回 false"),
		ICharacterCapability::Execute_IsActionAllowed(Capability));

	// GetCapabilityState 桩：返回 Idle
	TestEqual(TEXT("GetCapabilityState 桩应返回 Idle"),
		ICharacterCapability::Execute_GetCapabilityState(Capability), ECapabilityState::Idle);

	return true;
}

bool FVRTestDummySpec::RunTest(const FString& Parameters)
{
	// AVRTestDummy 可生成（NewObject 未注册进 World，接口 Event 走默认实现；
	// 桩值断言通过 _Implementation 直接验证，ReceiveDamage 日志通过 Execute_ 验证接口调用路径）
	AVRTestDummy* Dummy = NewObject<AVRTestDummy>();
	TestNotNull(TEXT("AVRTestDummy 应创建成功"), Dummy);
	if (!Dummy)
	{
		return true;
	}

	// 实现 IDamageable / IBattleParticipant
	TestTrue(TEXT("TestDummy 应实现 IDamageable"), Dummy->Implements<UDamageable>());
	TestTrue(TEXT("TestDummy 应实现 IBattleParticipant"), Dummy->Implements<UBattleParticipant>());

	// 桩实现：IsAlive 固定 true（直接验证 _Implementation，绕开未注册 Actor 的 ProcessEvent 默认路径）
	TestTrue(TEXT("TestDummy IsAlive 桩应返回 true"), Dummy->IsAlive_Implementation());

	// 桩实现：GetHealthRatio 固定 1.0
	TestEqual(TEXT("TestDummy GetHealthRatio 桩应返回 1.0"), Dummy->GetHealthRatio_Implementation(), 1.0f);

	// ReceiveDamage 接口调用路径：Execute_ 触发（日志输出验证在 Output Log）
	FCombatResult Hit;
	Hit.Outcome = ECombatOutcome::Hit;
	Hit.Damage = 15.0f;
	Hit.bWasBlocked = false;
	Hit.HitZoneFlags = 1 << (int32)EHitZone::Torso;
	IDamageable::Execute_ReceiveDamage(Dummy, Hit); // 输出 LogVRSanguoCombat 日志

	// IBattleParticipant 桩调用不崩溃
	IBattleParticipant::Execute_OnBattleStart(Dummy);
	IBattleParticipant::Execute_OnBattleEnd(Dummy, EBattleOutcome::Victory);
	IBattleParticipant::Execute_ResetForNextRound(Dummy);

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
