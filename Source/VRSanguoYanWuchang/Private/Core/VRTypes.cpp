// VR 三国演武场 - 公共类型定义实现

#include "Core/VRTypes.h"

// 静态校验：编译期确保核心枚举大小符合预期（uint8）
static_assert(sizeof(EGameSessionPhase) == 1, "EGameSessionPhase should be uint8-backed");
static_assert(sizeof(ECombatOutcome) == 1, "ECombatOutcome should be uint8-backed");
static_assert(sizeof(EHitZone) == 1, "EHitZone should be uint8-backed");
static_assert(sizeof(EWeaponType) == 1, "EWeaponType should be uint8-backed");
static_assert(sizeof(EVRMovementMode) == 1, "EVRMovementMode should be uint8-backed");
static_assert(sizeof(EMovementFailReason) == 1, "EMovementFailReason should be uint8-backed");
static_assert(sizeof(EMovementState) == 1, "EMovementState should be uint8-backed");
static_assert(sizeof(EReleaseReason) == 1, "EReleaseReason should be uint8-backed");
static_assert(sizeof(EBattleOutcome) == 1, "EBattleOutcome should be uint8-backed");
static_assert(sizeof(ECapabilityState) == 1, "ECapabilityState should be uint8-backed");
static_assert(sizeof(EMatchEndReason) == 1, "EMatchEndReason should be uint8-backed");
static_assert(sizeof(EHand) == 1, "EHand should be uint8-backed");
