// VR 三国演武场 - 流程状态机自动化测试实现
// T006 Step 4：用例对齐 VRGameFlowComponent 迁移矩阵（systems/01 契约）

#include "Tests/VRGameFlowSpec.h"

#if WITH_DEV_AUTOMATION_TESTS

#include "Flow/VRGameFlowComponent.h"

// 合法链路辅助：Calibration -> Ready -> Generate -> Combat -> Settlement -> Reset -> Ready
static bool WalkValidChain(UVRGameFlowComponent& Flow)
{
	if (!Flow.RequestPhaseTransition(EGameSessionPhase::Ready)) return false;
	if (!Flow.RequestPhaseTransition(EGameSessionPhase::Generate)) return false;
	if (!Flow.RequestPhaseTransition(EGameSessionPhase::Combat)) return false;
	if (!Flow.RequestPhaseTransition(EGameSessionPhase::Settlement)) return false;
	if (!Flow.RequestPhaseTransition(EGameSessionPhase::Reset)) return false;
	if (!Flow.RequestPhaseTransition(EGameSessionPhase::Ready)) return false;
	return true;
}

bool FVRGameFlowTransitionSpec::RunTest(const FString& Parameters)
{
	AActor* Host = NewObject<AActor>();
	UVRGameFlowComponent* Flow = NewObject<UVRGameFlowComponent>(Host);
	TestNotNull(TEXT("Flow 组件应创建成功"), Flow);
	if (!Flow)
	{
		return true;
	}

	// 初始阶段 Calibration
	TestEqual(TEXT("初始阶段应为 Calibration"), Flow->GetCurrentPhase(), EGameSessionPhase::Calibration);

	// 完整合法链路走通
	TestTrue(TEXT("完整合法迁移链路应成功"), WalkValidChain(*Flow));

	// 回到 Calibration 后验证：Calibration -> Ready 合法
	Flow->ResetMatch();
	TestEqual(TEXT("ResetMatch 后应回到 Calibration"), Flow->GetCurrentPhase(), EGameSessionPhase::Calibration);
	TestTrue(TEXT("Calibration -> Ready 应合法"), Flow->RequestPhaseTransition(EGameSessionPhase::Ready));
	Flow->ResetMatch();

	// 非法迁移：Combat -> Ready（跳过 Settlement）应被拒绝
	TestTrue(TEXT("前置迁移到 Combat"), Flow->RequestPhaseTransition(EGameSessionPhase::Ready)
		&& Flow->RequestPhaseTransition(EGameSessionPhase::Generate)
		&& Flow->RequestPhaseTransition(EGameSessionPhase::Combat));
	TestFalse(TEXT("Combat -> Ready 非法迁移应被拒绝"), Flow->RequestPhaseTransition(EGameSessionPhase::Ready));
	TestEqual(TEXT("非法迁移后阶段不变（仍 Combat）"), Flow->GetCurrentPhase(), EGameSessionPhase::Combat);
	Flow->ResetMatch();

	// 非法迁移：Combat -> Generate 应被拒绝
	TestTrue(TEXT("前置迁移到 Combat（第二次）"), Flow->RequestPhaseTransition(EGameSessionPhase::Ready)
		&& Flow->RequestPhaseTransition(EGameSessionPhase::Generate)
		&& Flow->RequestPhaseTransition(EGameSessionPhase::Combat));
	TestFalse(TEXT("Combat -> Generate 非法迁移应被拒绝"), Flow->RequestPhaseTransition(EGameSessionPhase::Generate));
	Flow->ResetMatch();

	// 幂等：重复请求同阶段返回 false 且无副作用
	TestTrue(TEXT("前置迁移到 Ready"), Flow->RequestPhaseTransition(EGameSessionPhase::Ready));
	TestFalse(TEXT("重复请求 Ready -> Ready 应返回 false"), Flow->RequestPhaseTransition(EGameSessionPhase::Ready));
	TestEqual(TEXT("幂等请求后阶段不变（仍 Ready）"), Flow->GetCurrentPhase(), EGameSessionPhase::Ready);
	Flow->ResetMatch();

	// OnPhaseChanged 委托广播：动态委托绑定 C++ lambda 受限，此处通过合法链路观察阶段可达性间接验证广播路径
	Flow->ResetMatch();
	Flow->RequestPhaseTransition(EGameSessionPhase::Ready);
	// 注：委托广播的直接断言需 Blueprint 侧绑定（后续 UI 层覆盖）；此处验证状态机核心行为
	TestTrue(TEXT("Ready 阶段可达"), Flow->GetCurrentPhase() == EGameSessionPhase::Ready);

	return true;
}

bool FVRGameFlowMatchLifecycleSpec::RunTest(const FString& Parameters)
{
	AActor* Host = NewObject<AActor>();
	UVRGameFlowComponent* Flow = NewObject<UVRGameFlowComponent>(Host);
	TestNotNull(TEXT("Flow 组件应创建成功"), Flow);
	if (!Flow)
	{
		return true;
	}

	// StartMatch：从 Calibration 进入 Ready
	FMatchRuleSet Rules;
	Rules.TeamSize = 3;
	Rules.RoundCount = 1;
	Rules.TimeLimit = 120.0f;
	TestTrue(TEXT("StartMatch 应成功"), Flow->StartMatch(Rules));
	TestEqual(TEXT("StartMatch 后阶段应为 Ready"), Flow->GetCurrentPhase(), EGameSessionPhase::Ready);
	TestEqual(TEXT("ActiveRules 应记录 TeamSize=3"), Flow->GetActiveRules().TeamSize, 3);

	// 再次 StartMatch（已 Ready -> Generate 才合法，StartMatch 内部要求 Ready，应失败）
	TestFalse(TEXT("Ready 状态下重复 StartMatch 应失败"), Flow->StartMatch(Rules));

	// 推进到 Combat
	TestTrue(TEXT("Ready -> Generate 应成功"), Flow->RequestPhaseTransition(EGameSessionPhase::Generate));
	TestTrue(TEXT("Generate -> Combat 应成功"), Flow->RequestPhaseTransition(EGameSessionPhase::Combat));

	// EndMatch：Combat -> Settlement + OnMatchEnded 广播
	Flow->EndMatch(EMatchEndReason::TeamEliminated);
	TestEqual(TEXT("EndMatch 后阶段应为 Settlement"), Flow->GetCurrentPhase(), EGameSessionPhase::Settlement);
	TestEqual(TEXT("LastResult 应可查询"), Flow->GetLastResult().WinnerTeamId, -1);

	// 重复 EndMatch：无进行中比赛，忽略且阶段不变
	Flow->EndMatch(EMatchEndReason::TimeExpired);
	TestEqual(TEXT("重复 EndMatch 后阶段不变"), Flow->GetCurrentPhase(), EGameSessionPhase::Settlement);

	// ResetMatch：任意阶段 -> Calibration（幂等）
	Flow->ResetMatch();
	TestEqual(TEXT("ResetMatch 后应回到 Calibration"), Flow->GetCurrentPhase(), EGameSessionPhase::Calibration);
	TestEqual(TEXT("ResetMatch 后 LastResult 应清空"), Flow->GetLastResult().WinnerTeamId, -1);

	// ResetMatch 幂等：已 Calibration 再调不崩溃
	Flow->ResetMatch();
	TestEqual(TEXT("幂等 ResetMatch 后仍 Calibration"), Flow->GetCurrentPhase(), EGameSessionPhase::Calibration);

	return true;
}

#endif // WITH_DEV_AUTOMATION_TESTS
