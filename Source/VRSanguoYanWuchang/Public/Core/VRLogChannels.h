// VR 三国演武场 - 日志分类声明
// 对齐 systems/07-save-telemetry-and-diagnostics-system.md

#pragma once

#include "CoreMinimal.h"

// 模块启动、生命周期
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoCore, Log, All);
// OpenXR、追踪、输入适配
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoVR, Log, All);
// 命中结算、伤害、防御
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoCombat, Log, All);
// 武器抓取、轨迹、解卡
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoWeapon, Log, All);
// 瞬移、平滑移动、IK
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoMovement, Log, All);
// AI 决策、战术、动作
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoAI, Log, All);
// 流程状态机、阶段切换
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoFlow, Log, All);
// 性能采样、帧率统计
VRSANGUOYANWUCHANG_API DECLARE_LOG_CATEGORY_EXTERN(LogVRSanguoPerf, Log, All);
