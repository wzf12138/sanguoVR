# M00-T005 输入

## 治理与规则
- `.trae/governance/ExecutionModel.md`
- `.trae/governance/definition-of-done.md`
- `.trae/rules/project_rules.md`

## 产品知识
- `.trae/knowledge/GameMasterPlan.md`
- `.trae/knowledge/EngineReference.md`（VR/OpenXR/Enhanced Input/IK/性能优化）

## 任务详规
- `.trae/execution/M00/T005-SystemSkeleton.md`（完整实施步骤与验收清单）

## 工程标准
- `.trae/standards/04-data-asset-standard.md`（Data Asset 规范）
- `.trae/standards/05-event-and-interface-standard.md`（接口与事件委托规范）
- `.trae/systems/01-game-flow-system.md`（流程状态机设计）

## 工程文件
- `VRSanguoYanWuchang.uproject`（模块列表）
- `Source/VRSanguoYanWuchang/Private/VRSanguoYanWuchang.cpp`（模块启动，需注册日志分类）

## 禁止推断
- 不修改 T004 白名单内的文件
- 不修改 VR 模板资产（Content/ 下模板文件）
- 不修改 `.uproject` 插件列表
- 不在 M01 之前创建接口的具体实现类
- 不把规划描述为实现，不把编辑器验证描述为 PICO 真机验证