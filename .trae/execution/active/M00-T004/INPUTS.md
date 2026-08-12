# M00-T004 输入

## 治理与规则
- `.trae/governance/ExecutionModel.md`
- `.trae/governance/definition-of-done.md`
- `.trae/rules/project_rules.md`

## 产品知识
- `.trae/knowledge/GameMasterPlan.md`（离线运行、VR 能力要求）
- `.trae/knowledge/EnvironmentSetup.md`（Android 工具链状态）
- `.trae/knowledge/TechnicalDecisions.md`（MCP 配置、OpenXR 路线）
- `.trae/knowledge/PicoNeo3BuildGuide.md`（构建指南、验证矩阵）

## 工程文件
- `VRSanguoYanWuchang.uproject`（插件/平台核对）
- `Content/` 下 VR 模板资产

## 验证目标
- `.trae/registers/09-verification-register.md`（V-004/V-005）

## 禁止推断
- 不修改 `.uproject`、`Source/`、`Content/`、`Config/`、`Plugins/`
- 不在缺少真机证据时声明 PICO 验证通过
- 不把 PC/编辑器 VR 结论替代 PICO Neo3 结论
- Android SDK 安装由用户执行，AI 只读检查结果
