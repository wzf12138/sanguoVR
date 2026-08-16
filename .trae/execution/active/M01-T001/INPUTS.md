# M01-T001 输入

## 治理与规则
- `.trae/governance/ExecutionModel.md`
- `.trae/rules/project_rules.md`

## 前置任务产出
- M00-T005：VRCharacterCapabilityComponent、VRGameFlowComponent（接口骨架）
- M00-T004：PICO Neo3 输入映射（5 个 IMC 已配置）

## VRE 插件
- `Plugins/VRExpansionPlugin/`（5.6 官方版，已编译通过）
- 核心组件：`GripMotionControllerComponent`、`HandSocketComponent`、`GrippableSkeletalMeshActor`

## VRE 示例参考（只读，不复制素材）
- `E:\AWork\VRExpPluginExample\Content\VRE\Grippables\Weapons\Melee\` — 近战武器抓取蓝图
- `E:\AWork\VRExpPluginExample\Content\VRE\Grippables\Weapons\TwoHandedGrip\` — 双手握持蓝图
- `E:\AWork\VRExpPluginExample\Content\VRE\Core\HandSockets\` — 手部姿势配置

## 战斗系统设计
- `.trae/knowledge/Design\CombatSystem.md`（碰撞与解卡、有效攻击）
- `.trae/knowledge/Design\WeaponsAndInteraction.md`（抓取与双手、统一接口）

## 工程文件
- `Content/VRSanguo/Dev/L_SkeletonTest.umap`（测试关卡）
- `VRSanguoYanWuchang.uproject`（只读参考，确认插件已启用）

## 禁止推断
- 不修改 VRE 插件源码
- 不替换现有 VRPawn 为 VRCharacter
- 不修改 PICO Neo3 输入映射
- 不复制示例项目的素材/模型/材质