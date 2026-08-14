// VR 三国演武场 - UVRGameFlowComponent 实现

#include "Flow/VRGameFlowComponent.h"
#include "Core/VRLogChannels.h"

UVRGameFlowComponent::UVRGameFlowComponent()
{
	PrimaryComponentTick.bCanEverTick = false;
}

bool UVRGameFlowComponent::IsTransitionAllowed(EGameSessionPhase From, EGameSessionPhase To) const
{
	// 合法迁移矩阵（T005-SystemSkeleton Step 4 硬编码）：
	// Calibration -> Ready -> Generate -> Combat -> Settlement -> Reset -> Ready
	// 任意阶段 -> Calibration（紧急重置）
	if (To == EGameSessionPhase::Calibration)
	{
		return From != EGameSessionPhase::Calibration; // 已在 Calibration 则无迁移
	}

	switch (From)
	{
	case EGameSessionPhase::Calibration:  return To == EGameSessionPhase::Ready;
	case EGameSessionPhase::Ready:        return To == EGameSessionPhase::Generate;
	case EGameSessionPhase::Generate:     return To == EGameSessionPhase::Combat;
	case EGameSessionPhase::Combat:       return To == EGameSessionPhase::Settlement;
	case EGameSessionPhase::Settlement:   return To == EGameSessionPhase::Reset;
	case EGameSessionPhase::Reset:        return To == EGameSessionPhase::Ready;
	default:                              return false;
	}
}

void UVRGameFlowComponent::PerformTransition(EGameSessionPhase OldPhase, EGameSessionPhase NewPhase)
{
	CurrentPhase = NewPhase;
	UE_LOG(LogVRSanguoFlow, Log, TEXT("Phase transition: %s -> %s"),
		*StaticEnum<EGameSessionPhase>()->GetNameStringByValue((int64)OldPhase),
		*StaticEnum<EGameSessionPhase>()->GetNameStringByValue((int64)NewPhase));
	OnPhaseChanged.Broadcast(OldPhase, NewPhase);
}

bool UVRGameFlowComponent::RequestPhaseTransition(EGameSessionPhase TargetPhase)
{
	if (TargetPhase == CurrentPhase)
	{
		UE_LOG(LogVRSanguoFlow, Warning, TEXT("RequestPhaseTransition: 目标阶段与当前相同 (%s)"),
			*StaticEnum<EGameSessionPhase>()->GetNameStringByValue((int64)TargetPhase));
		return false;
	}

	if (!IsTransitionAllowed(CurrentPhase, TargetPhase))
	{
		UE_LOG(LogVRSanguoFlow, Warning, TEXT("RequestPhaseTransition: 非法迁移 %s -> %s"),
			*StaticEnum<EGameSessionPhase>()->GetNameStringByValue((int64)CurrentPhase),
			*StaticEnum<EGameSessionPhase>()->GetNameStringByValue((int64)TargetPhase));
		return false;
	}

	PerformTransition(CurrentPhase, TargetPhase);

	// 旧阶段资源清理（T005 最小桩：比赛状态维护）
	if (CurrentPhase == EGameSessionPhase::Calibration)
	{
		bMatchInProgress = false;
	}

	return true;
}

bool UVRGameFlowComponent::StartMatch(const FMatchRuleSet& Rules)
{
	// 契约：StartMatch 成功进入 Ready
	if (!RequestPhaseTransition(EGameSessionPhase::Ready))
	{
		UE_LOG(LogVRSanguoFlow, Warning, TEXT("StartMatch: 无法进入 Ready（当前 %s）"),
			*StaticEnum<EGameSessionPhase>()->GetNameStringByValue((int64)CurrentPhase));
		return false;
	}

	ActiveRules = Rules;
	bMatchInProgress = true;
	UE_LOG(LogVRSanguoFlow, Log, TEXT("StartMatch: TeamSize=%d RoundCount=%d TimeLimit=%.1f"),
		Rules.TeamSize, Rules.RoundCount, Rules.TimeLimit);
	return true;
}

void UVRGameFlowComponent::EndMatch(EMatchEndReason Reason)
{
	if (!bMatchInProgress)
	{
		UE_LOG(LogVRSanguoFlow, Warning, TEXT("EndMatch: 当前无进行中的比赛，忽略"));
		return;
	}

	// 契约：EndMatch 触发 Settlement
	if (RequestPhaseTransition(EGameSessionPhase::Settlement))
	{
		LastResult.Duration = 0.0f; // T005 最小桩：真实时长由 M01 起统计
		bMatchInProgress = false;
		OnMatchEnded.Broadcast(Reason, LastResult);
		UE_LOG(LogVRSanguoFlow, Log, TEXT("EndMatch: Reason=%s"),
			*StaticEnum<EMatchEndReason>()->GetNameStringByValue((int64)Reason));
	}
}

void UVRGameFlowComponent::ResetMatch()
{
	// 幂等重置：任意阶段 -> Calibration
	const EGameSessionPhase OldPhase = CurrentPhase;
	if (OldPhase != EGameSessionPhase::Calibration)
	{
		RequestPhaseTransition(EGameSessionPhase::Calibration);
	}

	bMatchInProgress = false;
	LastResult = FMatchResult();
	UE_LOG(LogVRSanguoFlow, Log, TEXT("ResetMatch: 已清理（幂等）"));
}
