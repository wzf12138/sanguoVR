# M00-T006 输入

## 治理与规则
- `.trae/governance/ExecutionModel.md`
- `.trae/governance/definition-of-done.md`
- `.trae/rules/project_rules.md`

## 前置任务产出（T005）
- T005 Step 1：8 个日志分类（VRLogChannels.h）
- T005 Step 2：7 项核心接口（Interfaces/VR*.h）
- T005 Step 3：8 个 DataAsset 基类（Data/VR*Definition.h 等）
- T005 Step 4：VRGameFlowComponent（流程状态机）
- T005 Step 5：VRCharacterCapabilityComponent
- T005 Step 6：AVRTestDummy + L_SkeletonTest

## 系统接口契约
- `.trae/systems/07-save-telemetry-and-diagnostics-system.md`（日志分类与诊断能力）
- `.trae/systems/01-game-flow-system.md`（流程状态机契约，测试目标）

## 工程标准
- `.trae/standards/08-testing-and-acceptance-standard.md`（测试层级与门槛）

## 任务详规
- `.trae/execution/M00/T006-AutomationDiagnosticsGates.md`（完整实施步骤与验收清单）

## 工程文件
- `Source/VRSanguoYanWuchang/VRSanguoYanWuchang.Build.cs`（需新增 Automation 模块依赖）
- `VRSanguoYanWuchang.uproject`（只读参考，不修改）

## 禁止推断
- 不修改 T004/T005 白名单内的文件
- 不修改 VR 模板资产
- 不修改 `.uproject` 插件列表
- 不实现 M01 范围的战斗测试（命中去重、格挡等 deferred）
- 不把规划描述为实现，不把编辑器验证描述为 PICO 真机验证
