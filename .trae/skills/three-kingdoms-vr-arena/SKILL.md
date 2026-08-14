---
name: "three-kingdoms-vr-arena"
description: "执行 VR 三国演武场的集中式治理、事实源定位、工程边界与验收门禁。涉及本项目规划、代码、资产、测试、文档或变更时调用。"
---

# VR 三国演武场唯一项目 Skill

本文件是项目唯一可发现 Skill。它负责路由、边界与门禁，不复制治理、产品、标准或系统规则正文；不得创建第二个带 frontmatter 的 `SKILL.md`。

## 规则入口与权威关系

- `.trae/rules/project_rules.md` 是项目唯一规则正文，不存在根级兼容入口。
- 用户最新明确批准内容仍按 `.trae/governance/policy.md` 的权威链处理。

## 四份治理契约

以下四份文件定义“什么受控、谁能做、怎样变更、何时算完成”：

1. `.trae/governance/policy.md`
2. `.trae/governance/change-request-template.md`
3. `.trae/governance/definition-of-done.md`
4. `.trae/governance/responsibility-matrix.md`

它们是治理契约，不是会话操作命令。

## 四份操作模型

以下四份文件定义“会话如何决策、执行、审核和触发”：

1. `.trae/governance/DecisionModel.md`
2. `.trae/governance/ExecutionModel.md`
3. `.trae/governance/ReviewProtocol.md`
4. `.trae/governance/SessionCommands.md`

操作模型服从四份治理契约，不得反向修改治理权威正文。

## 必读顺序

1. `.trae/README.md` 与 `.trae/index.md`
2. 四份治理契约
3. `.trae/rules/project_rules.md`
4. 与用户意图对应的操作模型
5. `.trae/knowledge/GameMasterPlan.md`、相关 `knowledge/Design/` 权威产品详规
6. `.trae/knowledge/EngineReference.md`（引擎技术参考，VR/OpenXR/Enhanced Input/IK/性能优化）
7. `.trae/knowledge/Production/` 生产规格（资产任务时必读：`ArtStyleGuide.md`、`AnimationSpec.md`、`LevelDesignSpec.md`）
8. 相关 standards、vr、systems 工程实现指引（含接口契约）与 registers（含技术债登记册 `11-tech-debt-register.md`）
9. `.trae/knowledge/Patterns/README.md` 实现模式库（M01+ 逐步填充，执行时查阅同类模式）
10. 当前 active 任务包和真实工程证据

## 写前校验

会话涉及创建或修改 `.trae/` 内文件时，先核对 `integrity.yaml` 与 `manifest.yaml` 与实际文件一致性（新增文件、重复命名、断链、索引与登记册同步）；不一致时在报告异常并停止，不自行补建。创建路径必须属于 active 白名单、当前任务报告/登记册路径或用户本次明确批准的变更，三者皆不是则不得创建。

## 模式路由

| 用户意图 | 模式 | 入口 |
|---|---|---|
| 决策下一步、规划、生成任务、登记风险 | 决策模式 | `DecisionModel.md` |
| 执行当前任务、开始或继续实施 | 执行模式 | `ExecutionModel.md` |
| 审核任务、验收结果或里程碑 | 审核模式 | `ReviewProtocol.md` |
| 状态检查、解释、咨询、分析 | 只读模式 | 不修改文件 |
| 修改治理、规则、Skill、总纲或其他锁定事实源 | 变更申请模式 | `change-request-template.md` |

短指令以 `SessionCommands.md` 为准。意图不明确时进入只读模式。

## active 完整门禁路径

执行模式必须逐份读取并同时满足：

0. **认领（必须在任何文件修改之前）**：从根 STATUS.json 选择 `status` 为 `ready` 的任务，检查五件套完整、无白名单冲突后，立即将根 STATUS.json 中对应条目 `status` 更新为 `in_progress`、`claimedBy` 填写会话标识。用户执行任务由 AI 监督模型代为更新。未完成认领不得修改任何文件。
1. `.trae/execution/active/STATUS.json`（根 STATUS.json，任务状态唯一权威）：`activeTasks` 数组中至少存在一个 `status` 为 `ready` 或 `in_progress` 的任务。
2. 认领目标任务后，`.trae/execution/active/{taskId}/ALLOWLIST.txt`：至少一行非空、非注释的明确相对路径（路径相对于项目根目录 `VRSanguoYanWuchang/`）。
3. `.trae/execution/active/{taskId}/TASK.md`：目标、范围、步骤、停止条件、回退和报告路径完整。
4. `.trae/execution/active/{taskId}/INPUTS.md`：所需事实源与输入可读。
5. `.trae/execution/active/{taskId}/CHECKS.md`：验证方法与门禁可执行。

任务目录下的 `STATUS.json` 为本地便利副本，冲突时以根 STATUS.json 为准。里程碑任务详规从 `.trae/execution/M00/` 等正式目录读取，不在 `active/` 下复制。任一五件套文件缺失、根 STATUS.json 中状态不是 `ready` 或 `in_progress`、`taskId` 为空或白名单无有效路径时立即停止，不自行激活、补写或扩大任务。

### 并发安全

认领任务前必须检查与其它 `in_progress` 任务的白名单无重叠（共享文件除外）。认领后将根 STATUS.json 中对应条目的 `status` 更新为 `in_progress`，`claimedBy` 填写会话标识（格式 `"session-{YYYYMMDD}-{序号}"`）。

## 文件与事实边界

- 治理、规则、知识、执行、登记和归档资料只写入项目 `.trae/` 对应目录。
- systems 是工程实现指引；产品规则以 `knowledge/Design/` 对应权威详规为准，不在 systems 复制规则。
- UE 工程内容分别写入 `Source/`、`Config/`、`Content/`、`Plugins/`。
- 临时脚本、下载、缓存、日志和调试输出不得污染项目。
- 一个主题只保留一个可编辑权威正文；其他位置只链接。

## 执行与停止

执行时只修改有效白名单路径，修改前先读，使用最小差异；同步相关索引、登记册、任务报告和 `.trae/CHANGELOG.md`，并逐份回读。需要越界、锁定文件未获批准、证据不足、验证失败、权限或外部依赖缺失、发现第二 Skill 或平行事实源时停止并报告。执行模型最多把状态更新为 `awaiting_review`，不得自审自批。

## 交付门禁

- 规划、实现和验证分开陈述，未验证项明确标记。
- 四份治理契约和四份操作模型均可读且角色不混淆。
- `rules/project_rules.md` 唯一规则入口可读且无根级重复规则文件。
- active 五件套、任务详情和里程碑包按完整路径核验。
- 索引、manifest、integrity、登记册与变更记录和实际文件一致。
- `.trae/skills/` 下仅本文件具有有效 YAML frontmatter。
