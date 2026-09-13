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

## 外部参考工程（示例来源）

需要 VRE（VRExpansionPlugin）官方示例工程时，**从 E 盘取**。**不得回答"本地没有"，不得重新下载**。

- **权威来源**：`E:\AWork\Temp\VRExpansionPlugin\VRExpPluginExample-5.6\VRExpPluginExample-5.6-Locked\`
  —— 842 个源树文件 / 1,020.6 MB，UE **5.6**，LF 换行，非 git，**实测 0 只读**（目录名带 `Locked` 是历史残留，里面没锁）。
  `Content\` 582 文件 / 1,017.7 MB，含官方示例姿势、手部动画、示例蓝图与关卡。
- **另有 D 盘一份**：`D:\AWork\Unreal\Project\VRE\`（932 文件，git 仓库，CRLF，UE 5.6）。**用户 2026-09-13 手工下载用于查看，去留待定。**
- **本项目内插件版本是 5.4，E 盘示例工程是 5.6** —— 版本不一致时以 E 盘为准。

## CI 门禁

推送 `.trae/` 或 `dashboard/` 变更时自动触发治理一致性校验。
校验失败将阻断合并，确保知识库质量。
