// VR 三国演武场 - UVRGameFlowComponent 游戏流程状态机
// 对齐 systems/01-game-flow-system.md 契约：
//   EGameSessionPhase / RequestPhaseTransition / StartMatch / EndMatch / ResetMatch
//   OnPhaseChanged / OnMatchEnded

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Core/VRTypes.h"
#include "VRGameFlowComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FVROnPhaseChanged, EGameSessionPhase, OldPhase, EGameSessionPhase, NewPhase);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FVROnMatchEnded, EMatchEndReason, Reason, const FMatchResult&, Result);

UCLASS(ClassGroup = (Flow), meta = (BlueprintSpawnableComponent))
class VRSANGUOYANWUCHANG_API UVRGameFlowComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UVRGameFlowComponent();

	// ===== 状态查询 =====

	/** 当前会话阶段 */
	UFUNCTION(BlueprintPure, Category = "Flow")
	EGameSessionPhase GetCurrentPhase() const { return CurrentPhase; }

	// ===== 状态迁移（systems/01 契约）=====

	/** 请求阶段切换：校验合法迁移 -> 广播 OnPhaseChanged -> 清理旧阶段资源。
	 *  返回 false 表示迁移非法或当前状态下不可迁移（可诊断）。 */
	UFUNCTION(BlueprintCallable, Category = "Flow")
	bool RequestPhaseTransition(EGameSessionPhase TargetPhase);

	/** 开始比赛：合法时进入 Ready 阶段 */
	UFUNCTION(BlueprintCallable, Category = "Flow")
	bool StartMatch(const FMatchRuleSet& Rules);

	/** 结束比赛：触发 Settlement 阶段并广播 OnMatchEnded */
	UFUNCTION(BlueprintCallable, Category = "Flow")
	void EndMatch(EMatchEndReason Reason);

	/** 幂等重置：清理所有临时对象并回到 Calibration */
	UFUNCTION(BlueprintCallable, Category = "Flow")
	void ResetMatch();

	// ===== 事件广播（systems/01 契约）=====

	/** 阶段切换广播 */
	UPROPERTY(BlueprintAssignable, Category = "Flow")
	FVROnPhaseChanged OnPhaseChanged;

	/** 比赛结束广播 */
	UPROPERTY(BlueprintAssignable, Category = "Flow")
	FVROnMatchEnded OnMatchEnded;

	/** 当前比赛规则（有效比赛期间可用） */
	UFUNCTION(BlueprintPure, Category = "Flow")
	FMatchRuleSet GetActiveRules() const { return ActiveRules; }

	/** 最近一次比赛结果 */
	UFUNCTION(BlueprintPure, Category = "Flow")
	FMatchResult GetLastResult() const { return LastResult; }

private:
	/** 校验迁移合法性（硬编码迁移矩阵） */
	bool IsTransitionAllowed(EGameSessionPhase From, EGameSessionPhase To) const;

	/** 执行迁移核心逻辑（更新状态 + 广播） */
	void PerformTransition(EGameSessionPhase OldPhase, EGameSessionPhase NewPhase);

	/** 当前阶段 */
	UPROPERTY(VisibleInstanceOnly, Category = "Flow")
	EGameSessionPhase CurrentPhase = EGameSessionPhase::Calibration;

	/** 当前比赛规则 */
	FMatchRuleSet ActiveRules;

	/** 最近一次比赛结果 */
	FMatchResult LastResult;

	/** 比赛是否进行中 */
	bool bMatchInProgress = false;
};
