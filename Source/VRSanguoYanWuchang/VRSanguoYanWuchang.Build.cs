// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class VRSanguoYanWuchang : ModuleRules
{
	public VRSanguoYanWuchang(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput", "GameplayTags", "AIModule" });

		// Automation 测试宏（IMPLEMENT_SIMPLE_AUTOMATION_TEST）位于 Core 模块 Misc/AutomationTest.h，无需独立模块依赖
		PrivateDependencyModuleNames.AddRange(new string[] { });

		// VR / OpenXR
		PublicDependencyModuleNames.AddRange(new string[] { "HeadMountedDisplay", "XRBase" });

		// Uncomment if you are using Slate UI
		// PrivateDependencyModuleNames.AddRange(new string[] { "Slate", "SlateCore" });
		
		// Uncomment if you are using online features
		// PrivateDependencyModuleNames.Add("OnlineSubsystem");

		// To include OnlineSubsystemSteam, add it to the plugins section in your uproject file with the Enabled attribute set to true
	}
}
