# M00-T005 输入

## 治理与规则
- `.trae/governance/ExecutionModel.md`
- `.trae/governance/definition-of-done.md`
- `.trae/rules/project_rules.md`

## 产品知识
- `.trae/knowledge/GameMasterPlan.md`
- `.trae/knowledge/EngineReference.md`（VR/OpenXR/Enhanced Input/IK/性能优化）

## 系统接口契约（强制约束）
- `.trae/systems/01-game-flow-system.md`（流程状态机契约：EGameSessionPhase、RequestPhaseTransition、StartMatch/EndMatch/ResetMatch）
- `.trae/systems/02-interaction-and-weapon-system.md`（武器与抓取契约：FWeaponTrajectorySample、EReleaseReason）
- `.trae/systems/03-combat-resolution-system.md`（战斗结算契约：FAttackRequest、FCombatResult、ECombatOutcome）
- `.trae/systems/04-movement-system.md`（移动契约：EMovementMode、FMovementTarget、FMovementResult）
- `.trae/systems/05-ai-combat-system.md`（AI 契约：ICharacterCapability 统一能力接口）
- `.trae/systems/07-save-telemetry-and-diagnostics-system.md`（日志分类与诊断能力）

## 工程标准
- `.trae/standards/02-naming-and-path-standard.md`（C++ 类名与文件名规范：VR 前缀）
- `.trae/standards/04-data-asset-standard.md`（Data Asset 规范：SchemaVersion、PostLoad 迁移）
- `.trae/standards/05-event-and-interface-standard.md`（接口 C++ 声明与事件语义）

## 任务详规
- `.trae/execution/M00/T005-SystemSkeleton.md`（完整实施步骤与验收清单）

## 工程文件
- `VRSanguoYanWuchang.uproject`（模块列表，EngineAssociation=5.6）
- `Source/VRSanguoYanWuchang/Private/VRSanguoYanWuchang.cpp`（模块启动，需注册日志分类）
- `Source/VRSanguoYanWuchang/VRSanguoYanWuchang.Build.cs`（模块依赖：Core/CoreUObject/Engine/InputCore/EnhancedInput/HeadMountedDisplay/XRBase）

## 禁止推断
- 不修改 T004 白名单内的文件
- 不修改 VR 模板资产（Content/VRTemplate/ 下模板文件）
- 不修改 `.uproject` 插件列表
- 不在 M01 之前创建接口的具体实现类
- 不把规划描述为实现，不把编辑器验证描述为 PICO 真机验证
- 不使用 VRS 前缀命名新文件（使用 VR 前缀，遵循 standards/02）
