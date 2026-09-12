# 新会话短指令

新会话工作目录必须选择 `VRSanguoYanWuchang` 项目根目录。

## 决策

### `决策下一步`

读取完整项目状态，审核当前阶段，生成活动任务；只生成任务，不执行。

### `规划这个细节：<主题>`

以决策模型身份设计指定细节。若会改变锁定规则，生成变更申请；若可作为原子任务，生成任务草案。

### `检查项目状态`

只读检查治理、任务、风险、工程和验证状态，不修改文件；同时核对 `integrity.yaml` 与实际文件一致性（新增文件、重复命名、断链、索引与登记册同步），不一致时列为异常报告。

### `登记风险：<内容>`

评估并更新风险登记；不得借此修改产品方向。

### `登记技术债：<内容>`

评估并在 [`../registers/11-tech-debt-register.md`](../registers/11-tech-debt-register.md) 中登记技术债（临时实现、占位方案、已知缺陷）；标注影响、偿还计划和优先级；不得借此修改产品方向或降低验收标准。

## 执行

### `执行当前任务`

先认领任务（更新根 STATUS.json 为 `in_progress` 并填写 `claimedBy`），然后仅在状态为 `in_progress` 且白名单非空时执行。最多提交到 `awaiting_review`。

### `继续执行当前任务`

仅用于状态已为 `in_progress`（已认领）且未触发停止条件的任务。

### `恢复阻塞任务`

进入决策模式核验阻塞是否解除；执行模型不能自行恢复。

## 审核

### `审核当前任务`

对照任务、白名单、实际修改和证据进行审核；只输出 `approved`、`requires_changes`、`blocked` 或 `rejected`。

### `验收当前里程碑`

审核里程碑全部任务和门禁，不实施新功能。

## 变更

### `申请修改：<内容>`

创建变更申请，不直接修改锁定文件。

### `只读分析：<问题>`

只读回答，不创建任务、不改工程。

## 跨会话信箱（AgentHub）

多会话并行时，跨会话消息走全局信箱 Hub：`D:\App\trae\AgentHub\`；权威协议 `D:\App\trae\AgentHub\PROTOCOL.md`（收发信前必读，全局 Skill 名 `agent-hub`）。

本项目会话必须在以下检查点查信：会话开始读完必读文档后；认领任务前；修改共享文件（登记册/STATUS/CHANGELOG）后（向 `channels/registry-changes` 发广播）；进入 blocked 时（向 `channels/blockers` 发信并写明解除条件）；**遇到需拍板的决策问题或执行受阻时**——`type: question` 投 `inboxes/manager/`（普通调度）或 `inboxes/decision/`（方案/规格/范围裁决），随后 `hub_await(role=本会话角色, timeout_sec≤1800)` 值班挂起等回复，来信自醒后按回复执行并回执，不得空等用户传话。

铁律：信箱只是传输；认领、决策、验收等治理后果仍按本治理体系落 STATUS.json 与登记册，信件不构成事实源。


## 纪律索引（**本文件只放"你敲什么"；规则正文一律在别处**）

> 2026-09-12 整理：本文件原为 89 行短指令清单，因"新会话一定会读到"被反复追加立法，**一天涨到 420 行（+275 / −0）**。现按用户指示（**「简短的部分放简短的说明和索引，复杂的地方可以另外开一个文件」**）把正文整段迁出，**本文件恢复为指令 + 索引**。

| 主题 | 权威正文（唯一） |
|---|---|
| 何时推送 / 网络恢复流程 / CI 取证 | `push-and-network.md` |
| 清单外异常口径（口径 ③~⑦） | `exception-taxonomy.md` |
| 判据纪律（量具声明块 / 三态 / 停手分级 / 顺序与剔除规则） | `judgement-discipline.md` |
| 文书纪律（锚点即内容 / 标题形态 / 渲染层书写） | `writing-discipline.md` |
| 决策授权 / 安全默认（含 AFS 密钥） | `operation-discipline.md` |
| 规则 ⇄ 门禁覆盖关系（哪条规则靠机器守、哪条靠人守） | `rule-gate-matrix.md` |
| 判据工具实现规格（条款与 TC） | [`../execution/CR-20260912-001-judgement-tool.md`](../execution/CR-20260912-001-judgement-tool.md) |
| 项目规则正文（含副本与可追溯 29–32） | 根级 [`AGENTS.md`](../../AGENTS.md) |
| 治理权威链 / 文件控制等级 / 状态词表 | [`policy.md`](policy.md) |
| 提交台账与立法登记 | [`../CHANGELOG.md`](../CHANGELOG.md) |
| 唯一可发现 Skill（路由与门禁） | [`../skills/three-kingdoms-vr-arena/SKILL.md`](../skills/three-kingdoms-vr-arena/SKILL.md) |
| 任务 / 风险 / 技术债登记册 | [`../registers/`](../registers/) |

**⇒ 本文件不得再承载规则正文。** 需要新增纪律时：**正文写进上表对应文件，本文件只加一行指针。**

