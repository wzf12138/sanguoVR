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

## CI 门禁

推送 `.trae/` 或 `dashboard/` 变更时自动触发治理一致性校验。
校验失败将阻断合并，确保知识库质量。
