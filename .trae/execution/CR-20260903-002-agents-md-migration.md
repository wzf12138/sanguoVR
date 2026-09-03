# 集中式变更请求

## 1. 基本信息

- 请求编号：`CR-20260903-002`

- 状态：`draft`

- 请求人：用户（产品负责人） + manager 代拟

- 请求日期：2026-09-03

- 审批人：用户

- 审批日期：

- 关联任务/里程碑：全局（治理结构变更，不影响任何里程碑范围/完成定义）

- 关联决策：用户 2026-09-03 决定采用「方案 A 整体迁移」

## 2. 变更摘要

- 当前基线：项目唯一规则正文位于 `.trae/rules/project_rules.md`；治理政策 §3 单一事实源与唯一 Skill frontmatter 约束；AGENTS.md 业界约定在项目根级不存在。

- 拟议变更：

  1. 在**项目根级**新建 `AGENTS.md`，包含原 `project_rules.md` 全部正文（必读/文件边界/磁盘与下载规则/禁止虚构/确认门禁/证据与验证/执行纪律/沟通规则/UE 重启后必做/权限规则）+ 引导段说明文件性质（迁移版、迁移日期、原文件路径）。
  2. **删除** `.trae/rules/project_rules.md`（根目录已有的规则入口已替代其功能）。
  3. 同步修改所有引用 `.trae/rules/project_rules.md` 的当前活文件（policy.md / SKILL.md / DecisionModel.md / ExecutionModel.md / index.md / manifest.yaml / UEBridgeRefresh.md / 3 个 task-template.md）。
  4. **不动**历史记录类引用（CHANGELOG.md / 已 approved 任务的报告与 INPUTS.md / 今天写的 M00-T001 ACL 报告）——按 policy.md §3「历史材料只供审计，不得作为当前需求、排期或验收依据」原则保留事实原貌。

- 变更原因：

  - `AGENTS.md` 是 GitHub Copilot / Cursor / Aider / Claude Code 等外部 AI 工具识别的**业界标准**约定文件，根级放置可让任何 AI 工具零配置识别项目 AI 行为规范。

  - 当前 `.trae/rules/project_rules.md` 是 Trae 自定义路径，外部 AI 工具默认不读，导致它们进入项目时无据可依。

  - 整体迁移保留单一事实源原则（仅根级一份），仅改变文件位置与文件名。

- 不变范围：

  - 规则正文内容零改动（仅位置/文件名变化）。

  - 治理契约（policy.md / definition-of-done.md / responsibility-matrix.md / change-request-template.md）。

  - 产品总纲、唯一 Skill frontmatter、登记册体系、active 任务体系。

  - 任何工程文件（Source/ / Config/ / Content/ / Plugins/）。

  - 历史记录类文件。

- 预期收益：

  - 任何外部 AI 工具进入项目时自动加载 AGENTS.md，立即获得项目 AI 行为铁律（必读/禁止/确认门禁/证据与验证/沟通规则）。

  - 减少「外部 AI 误删/误改/虚构」风险。

  - 保留项目内部 `.trae/` 治理资料结构不变，对 Trae 内部会话零影响（Skill 路由会同步更新）。

## 3. 影响分析

- 产品范围与玩家体验：无。

- 架构、接口与数据：无。

- 代码、配置、资产与插件：无。

- 测试、性能、VR 舒适度与设备：无。

- 进度、成本与依赖：

  - 实施预计 1 个执行会话（当前 session-20260825-002 可顺手完成）。

  - 无新依赖。

- 治理正文、索引、登记册和 Skill：

  - 治理类文件 7 个需修改引用（最小差异替换相对路径）。

  - 任务模板类 3 个需修改「`.trae/rules/` 是锁定文件」描述为「根级 AGENTS.md 与 `.trae/governance/` 是锁定文件」。

  - `.trae/skills/three-kingdoms-vr-arena/SKILL.md` 同步 3 处。

  - `manifest.yaml` `rules.authoritative` 字段从 `.trae/rules/project_rules.md` 改为 `AGENTS.md`。

  - `CHANGELOG.md` 顶部加本次变更条目（含锁定文件修改记录）。

  - 新建执行报告 `execution/reports/tasks/CR-20260903-002.md` 记录实施证据。

  - 登记册、active 任务体系零变化（无任务需重写或迁移）。

## 4. 执行边界

- 允许修改的绝对路径：

  - 新建：根级 `AGENTS.md`、`.trae/execution/CR-20260903-002-agents-md-migration.md`（本文件）

  - 新建：`.trae/execution/reports/tasks/CR-20260903-002.md`（实施证据）

  - 修改：`.trae/governance/policy.md`、`.trae/governance/DecisionModel.md`、`.trae/governance/ExecutionModel.md`、`.trae/governance/UEBridgeRefresh.md`

  - 修改：`.trae/skills/three-kingdoms-vr-arena/SKILL.md`

  - 修改：`.trae/index.md`、`.trae/manifest.yaml`

  - 修改：`.trae/execution/task-template.md`、`.trae/execution/task-template-level.md`、`.trae/execution/task-template-asset.md`

  - 修改：`.trae/CHANGELOG.md`（顶部加条目）

  - 删除：`.trae/rules/project_rules.md`

- 禁止路径：

  - 历史记录类文件（CHANGELOG.md 现有条目 / 已 approved 任务报告 / 已 approved 任务 INPUTS.md / M00-T001-acl-2026-08-26.md）——这些是事实记录，原貌保留

  - `.trae/rules/` 目录下其他文件（如有）

  - `.trae/governance/change-request-template.md` / `definition-of-done.md` / `responsibility-matrix.md` / `TestSpecification.md` / `SessionCommands.md` / `ReviewProtocol.md`（除引用同步外不动）

  - 任何工程文件

  - 任何根级 `.md` 已有文件（如 .editorconfig、.gitignore、.lfsconfig 等）的非必要修改

- 前置条件：用户已批准本 CR 方案 A。

- 强制停止条件：

  - 任何引用同步后发现逻辑冲突或新发现必须改禁止路径

  - check-integrity.py 失败且无法在本 CR 范围内修复

  - 实施过程中发现 .trae/rules/ 下还有其他必须保留的文件

- 是否需要管理员权限/外部凭据/联网：否（.trae/rules/project\_rules.md 由 PC 用户 Modify 权限可删，前日已 Apply ACL 保护）。

- 是否包含删除、迁移、批量重命名或格式升级：

  - 删除 1 个文件（.trae/rules/project\_rules.md）

  - 实质上是一次文件迁移（位置变更）+ 批量引用同步（11 处）

  - git commit 一次完成全部变更

## 5. 风险与回滚

- 已知风险：

  - **风险 R1**：删除旧文件后，已 approved 任务的 INPUTS.md 中仍引用 `.trae/rules/project_rules.md` 路径（事实记录原貌）。如果未来某天有人按已 approved 任务的 INPUTS.md 引导去读旧路径，会找不到文件。

    - **缓解**：CHANGELOG.md 顶部条目明确标注迁移；CR 实施报告记录映射关系。

  - **风险 R2**：外部 AI 工具读取 AGENTS.md 时如果把 `.trae/` 相对路径误读为「项目根的子目录」（其实是项目根的隐藏治理目录），可能误操作。

    - **缓解**：AGENTS.md 顶部引导段明确说明 `.trae/` 是项目治理资料主目录。

  - **风险 R3**：本 CR 涉及的 7 个治理类文件都是锁定文件，多个修改叠加可能让 check-integrity 校验链路在中间态失败。

    - **缓解**：所有引用同步改完后才跑 check-integrity；任一修改失败立即停止。

- 风险负责人：manager（决策模型）+ 执行模型协同。

- 回滚锚点：本 CR 实施前的 git commit（当前 `3695a25` 之上）。

- 回滚步骤：

  1. `git revert` 实施提交
  2. 检查 `.trae/rules/project_rules.md` 是否恢复
  3. 检查所有引用是否恢复
  4. 重跑 check-integrity.py 确认 21/21

- 回滚验证：

  - `.trae/rules/project_rules.md` 存在且内容完整

  - `policy.md` / `SKILL.md` / `manifest.yaml` 等文件中无 `AGENTS.md` 引用

  - 根级无 `AGENTS.md`

  - check-integrity.py 21/21 全过

## 6. 验证计划

- 静态检查：

  - check-integrity.py 21/21 全过（重点关注：链接完整性、Skill 唯一性、五件套、白名单冲突、交叉引用、验证证据路径、任务登记与验证登记状态一致）

  - 人工逐份回读修改的 7 个治理类文件 + 3 个 task-template.md + AGENTS.md

- 自动化测试：不适用（治理结构变更，无代码逻辑变化）。

- UE 编译/编辑器验证：不适用。

- PICO 真机验证：不适用。

- 文档逐份回读：

  - AGENTS.md（与 project\_rules.md 原文逐条对比，确保零字差异）

  - policy.md / SKILL.md / DecisionModel.md / ExecutionModel.md（确认引用同步）

  - index.md / manifest.yaml（确认导航与权威字段同步）

  - task-template\*.md（确认锁定路径描述准确）

  - CHANGELOG.md（新增条目格式与历史一致）

- 唯一 Skill 检查：仍仅 `.trae/skills/three-kingdoms-vr-arena/SKILL.md` 一个带 frontmatter。

- 证据保存位置：`.trae/execution/reports/tasks/CR-20260903-002.md` + git 提交 + 远程 Actions 运行结果。

## 7. 审批

- 审批结论：`待审批`

- 审批意见：

- 批准的实施范围：

- 附加约束：

## 8. 实施与关闭

- 实施任务编号：当前会话 session-20260825-002（无 active 任务，使用本 CR 作为执行边界，按 project\_rules.md 第 19c 条「用户本次明确批准的变更」授权白名单）

- 实施结果：

- 偏差：

- 验证结果：

- 更新的权威正文：根级 `AGENTS.md`（由原 `.trae/rules/project_rules.md` 迁移）

- 更新的索引/登记册/变更记录：

  - `CHANGELOG.md` 顶部加新条目

  - `index.md` 链接同步

  - `manifest.yaml` `rules.authoritative` 同步

  - `.trae/execution/reports/tasks/CR-20260903-002.md` 实施报告

- 遗留风险与后续任务：

  - 外部 AI 工具首次进入项目时是否真正加载 AGENTS.md 需实测（不在本 CR 范围）

  - 已 approved 任务 INPUTS.md 中旧路径引用是历史事实，不修

- 关闭人：

- 关闭日期：

