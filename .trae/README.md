# VRSanguoYanWuchang 治理知识库

本目录包含 VR 三国演武场项目的治理、决策、任务和风险管理资料。

## 目录结构

- `governance/` — 治理策略、审查协议、变更管理
- `knowledge/` — 系统指南、架构决策记录、规范
- `execution/` — 任务模板、任务实例、登记册

## 快速链接

- 治理仪表板: https://wzf12138.github.io/sanguoVR/
- 变更管理: `governance/policy.md`
- 架构决策: `knowledge/GameMasterPlan.md`
- 新会话短指令: `governance/SessionCommands.md`（指令 + 索引）
- 操作纪律索引: `governance/operation-discipline.md`（决策授权 / 安全默认） → `governance/push-and-network.md`（推送与取证）、`governance/judgement-discipline.md`（判据纪律）、`governance/writing-discipline.md`（文书纪律）、`governance/exception-taxonomy.md`（清单外异常口径）、`governance/rule-gate-matrix.md`（规则⇄门禁映射）

## CI 门禁

推送 `.trae/` 或 `dashboard/` 变更时自动触发治理一致性校验。
校验失败将阻断合并，确保知识库质量。
