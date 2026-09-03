# M02-PREP-002 输入

1. 调研报告（已归档）：`D:\App\trae\AgentHub\inboxes\manager\archive\msg-20260831-092156-res-001.md`（RESEARCH-UEMCP，含对比表与迁移步骤）
2. 目标插件仓库：https://github.com/db-lyon/ue-mcp（MIT；UE5.4-5.8；蓝图写+读回；注意其 issue #627 类驱动引脚节点崩溃已知问题——本项目用普通表达式/函数调用节点，避开源驱动节点）
3. 旧插件：https://github.com/uuuuzz/UEBridgeMCP（GPL-3.0，v1.19，退役对象；TD-010）
4. 现有调用映射：本项目对 ue-bridge 的使用点为蓝图图编辑（edit-blueprint-graph/query）、编辑器探活（get-project-info）、截图/PIE（take_screenshot/capture-viewport）；迁移后逐一映射到 db-lyon 工具面
5. 用户批准：2026-08-31 用户选方案 A（本会话记录）
