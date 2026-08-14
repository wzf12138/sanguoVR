// Copyright Epic Games, Inc. All Rights Reserved.

#include "VRSanguoYanWuchang.h"
#include "Modules/ModuleManager.h"
#include "Core/VRLogChannels.h"
#include "Core/VRGameplayTags.h"

class FVRSanguoYanWuchangModule : public FDefaultGameModuleImpl
{
	virtual void StartupModule() override
	{
		// 项目 GameplayTag 由 NativeGameplayTags 宏在静态初始化期自动注册（见 Core/VRGameplayTags）

		// 启动日志，验证 8 个日志分类可用（对齐 systems/07）
		UE_LOG(LogVRSanguoCore, Log, TEXT("VRSanguoYanWuchang module started"));
		UE_LOG(LogVRSanguoVR, Log, TEXT("VR log channel initialized"));
		UE_LOG(LogVRSanguoCombat, Log, TEXT("Combat log channel initialized"));
		UE_LOG(LogVRSanguoWeapon, Log, TEXT("Weapon log channel initialized"));
		UE_LOG(LogVRSanguoMovement, Log, TEXT("Movement log channel initialized"));
		UE_LOG(LogVRSanguoAI, Log, TEXT("AI log channel initialized"));
		UE_LOG(LogVRSanguoFlow, Log, TEXT("Flow log channel initialized"));
		UE_LOG(LogVRSanguoPerf, Log, TEXT("Perf log channel initialized"));
	}

	virtual void ShutdownModule() override
	{
	}
};

IMPLEMENT_PRIMARY_GAME_MODULE( FVRSanguoYanWuchangModule, VRSanguoYanWuchang, "VRSanguoYanWuchang" );
