// VR 三国演武场 - 公共类型定义
// 对齐 systems/01-07 接口契约（2026-08-11 架构改版）

#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "VRTypes.generated.h"

// ============================ 枚举 ============================

/** 游戏会话阶段（systems/01） */
UENUM(BlueprintType)
enum class EGameSessionPhase : uint8
{
	Calibration		UMETA(DisplayName = "Calibration"),
	Ready			UMETA(DisplayName = "Ready"),
	Generate		UMETA(DisplayName = "Generate"),
	Combat			UMETA(DisplayName = "Combat"),
	Settlement		UMETA(DisplayName = "Settlement"),
	Reset			UMETA(DisplayName = "Reset"),
};

/** 战斗结算结果（systems/03） */
UENUM(BlueprintType)
enum class ECombatOutcome : uint8
{
	Miss		UMETA(DisplayName = "Miss"),
	Hit			UMETA(DisplayName = "Hit"),
	Blocked		UMETA(DisplayName = "Blocked"),
	Deflected	UMETA(DisplayName = "Deflected"),
	Parried		UMETA(DisplayName = "Parried"),
};

/** 命中部位（systems/03） */
UENUM(BlueprintType)
enum class EHitZone : uint8
{
	Head		UMETA(DisplayName = "Head"),
	Torso		UMETA(DisplayName = "Torso"),
	LeftArm		UMETA(DisplayName = "Left Arm"),
	RightArm	UMETA(DisplayName = "Right Arm"),
	LeftLeg		UMETA(DisplayName = "Left Leg"),
	RightLeg	UMETA(DisplayName = "Right Leg"),
};

/** 武器类别（GameMasterPlan） */
UENUM(BlueprintType)
enum class EWeaponType : uint8
{
	OneHandSword	UMETA(DisplayName = "One Hand Sword"),
	Shield			UMETA(DisplayName = "Shield"),
	TwoHandHeavy	UMETA(DisplayName = "Two Hand Heavy"),
	Spear			UMETA(DisplayName = "Spear"),
	Bow				UMETA(DisplayName = "Bow"),
};

/** 移动模式（systems/04）
 *  命名说明：引擎已有全局 UENUM `EMovementMode`（EngineTypes.h），按 standards/02
 *  VR 前缀约定消解命名冲突，枚举值保持 systems/04 契约不变 */
UENUM(BlueprintType)
enum class EVRMovementMode : uint8
{
	SmoothLocomotion	UMETA(DisplayName = "Smooth Locomotion"),
	TacticalTeleport	UMETA(DisplayName = "Tactical Teleport"),
	None				UMETA(DisplayName = "None"),
};

/** 移动失败原因（systems/04） */
UENUM(BlueprintType)
enum class EMovementFailReason : uint8
{
	None				UMETA(DisplayName = "None"),
	BlockedByGeometry	UMETA(DisplayName = "Blocked By Geometry"),
	BlockedByActor		UMETA(DisplayName = "Blocked By Actor"),
	OutOfRange			UMETA(DisplayName = "Out Of Range"),
	OnCooldown			UMETA(DisplayName = "On Cooldown"),
	Disabled			UMETA(DisplayName = "Disabled"),
};

/** 移动状态（systems/04, standards/05） */
UENUM(BlueprintType)
enum class EMovementState : uint8
{
	Idle		UMETA(DisplayName = "Idle"),
	Moving		UMETA(DisplayName = "Moving"),
	Teleporting	UMETA(DisplayName = "Teleporting"),
};

/** 武器释放原因（systems/02） */
UENUM(BlueprintType)
enum class EReleaseReason : uint8
{
	Manual		UMETA(DisplayName = "Manual"),
	Collision	UMETA(DisplayName = "Collision"),
	Timeout		UMETA(DisplayName = "Timeout"),
	Reset		UMETA(DisplayName = "Reset"),
};

/** 战斗胜负（standards/05） */
UENUM(BlueprintType)
enum class EBattleOutcome : uint8
{
	Victory		UMETA(DisplayName = "Victory"),
	Defeat		UMETA(DisplayName = "Defeat"),
	Draw		UMETA(DisplayName = "Draw"),
};

/** 角色能力状态（DEC-011） */
UENUM(BlueprintType)
enum class ECapabilityState : uint8
{
	Idle		UMETA(DisplayName = "Idle"),
	Attacking	UMETA(DisplayName = "Attacking"),
	Defending	UMETA(DisplayName = "Defending"),
	Staggered	UMETA(DisplayName = "Staggered"),
	Dead		UMETA(DisplayName = "Dead"),
};

/** 比赛结束原因（systems/01） */
UENUM(BlueprintType)
enum class EMatchEndReason : uint8
{
	TimeExpired		UMETA(DisplayName = "Time Expired"),
	TeamEliminated	UMETA(DisplayName = "Team Eliminated"),
	UserAbort		UMETA(DisplayName = "User Abort"),
	Draw			UMETA(DisplayName = "Draw"),
};

/** 手部标识（systems/02） */
UENUM(BlueprintType)
enum class EHand : uint8
{
	Left	UMETA(DisplayName = "Left"),
	Right	UMETA(DisplayName = "Right"),
};

// ============================ 结构体 ============================

/** 武器轨迹采样（systems/02） */
USTRUCT(BlueprintType)
struct FWeaponTrajectorySample
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FVector Position = FVector::ZeroVector;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FVector Velocity = FVector::ZeroVector;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FQuat Rotation = FQuat::Identity;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float Timestamp = 0.f;
};

/** 攻击结算输入（systems/03） */
USTRUCT(BlueprintType)
struct FAttackRequest
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int32 AttackId = 0;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	TObjectPtr<AActor> Source = nullptr;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	TObjectPtr<AActor> Target = nullptr;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FWeaponTrajectorySample Trajectory;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	EHitZone Zone = EHitZone::Torso;
};

/** 战斗结算输出（systems/03） */
USTRUCT(BlueprintType)
struct FCombatResult
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	ECombatOutcome Outcome = ECombatOutcome::Miss;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float Damage = 0.f;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	bool bWasBlocked = false;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int32 HitZoneFlags = 0;
};

/** 防御结算结果（systems/03） */
USTRUCT(BlueprintType)
struct FDefenseResult
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	bool bBlocked = false;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float DeflectedAngle = 0.f;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	bool bDeflected = false;
};

/** 移动请求目标（systems/04） */
USTRUCT(BlueprintType)
struct FMovementTarget
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FVector Location = FVector::ZeroVector;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FRotator Rotation = FRotator::ZeroRotator;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	bool bIsTeleport = false;
};

/** 移动执行结果（systems/04） */
USTRUCT(BlueprintType)
struct FMovementResult
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	bool bSuccess = false;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	EMovementFailReason FailReason = EMovementFailReason::None;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FVector ActualLocation = FVector::ZeroVector;
};

/** 比赛规则集（systems/01） */
USTRUCT(BlueprintType)
struct FMatchRuleSet
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int32 TeamSize = 3;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	TArray<int32> AllowedSizes;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int32 RoundCount = 1;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float TimeLimit = 120.f;
};

/** 比赛结果（systems/01） */
USTRUCT(BlueprintType)
struct FMatchResult
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int32 WinnerTeamId = -1;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	TArray<int32> Scores;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float Duration = 0.f;
};

/** 统一能力请求（DEC-011） */
USTRUCT(BlueprintType)
struct FCapabilityRequest
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FGameplayTag ActionTag;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	TObjectPtr<AController> SourceController = nullptr;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	int32 Priority = 0;
};
