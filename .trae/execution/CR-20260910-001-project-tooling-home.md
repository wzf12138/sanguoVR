# CR-20260910-001 · 项目工具脚本的授权落点（`.trae/tools/`）+ 脚本入库

> 依据 `governance/change-request-template.md` 填写。本 CR 改变的是**规则基线**（`AGENTS.md` §文件边界），故走变更控制。

## 1. 基本信息

- 请求编号：`CR-20260910-001`
- 状态：`已批准`
- 请求人：decision 指挥台（DSH 会话）
- 请求日期：2026-09-10
- 审批人：用户（项目所有者）
- 审批日期：2026-09-10
- 关联任务/里程碑：M01-T005（竞技场关卡）
- 关联决策：不需要

## 2. 变更摘要

- **当前基线**：`AGENTS.md` §文件边界只有「临时脚本、下载和调试输出：不得进入项目」一条，**没有任何授权落点能容纳"会被长期复用、且是某产物单一事实源"的项目工具脚本**。因此 `rebuild_v3.py` / `rebuild_v4.py` / `rebuild_v5.py` / `flip_topdown.ps1` 只能留在项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\`。
- **拟议变更**：① 在 `AGENTS.md` §文件边界新增「项目工具脚本：仅 `.trae/tools/`」一条；② 原「临时脚本…不得进入项目」一条收窄为「一次性排障或迁移用，写项目外临时目录，用完即删」；③ 上述 4 个脚本入库至 `.trae/tools/scene/`，并建 `.trae/tools/README.md` 作索引。
- **变更原因**：**这 4 个脚本是 `L_Prototype_1v1_v5.umap` 与 `Docs/Scene/` 四件套的单一事实源**——丢了脚本，对应产物无法复现。而它们此前**从未进入任何备份**（项目外目录、不入 Git、无第二副本），是实际存在的单点丢失风险，不是形式问题。
- **不变范围**：UE 工程目录边界（`Config/` `Content/` `Plugins/` `Source/`）不变；「临时脚本、下载、调试输出不得进入项目」的**禁止意图不变**；NTFS 管理脚本仍在项目外不变。
- **预期收益**：脚本纳入版本管理与备份；脚本与产物同仓，避免"产物在仓库、生成器在仓库外"的失联；后续同类脚本有明确落点，不再出现"无授权落点"。

## 3. 影响分析

- **产品范围与玩家体验**：无影响。不改变任何玩法、数值或内容。
- **架构、接口与数据**：无影响。4 个脚本均**不依赖自身所在目录**（无 `__file__`、无相对路径解析），搬移不改行为。核验方式：逐文件比对搬运前后 SHA256，4/4 一致。
- **代码、配置、资产与插件**：无影响。脚本不参与构建，不在 UE 的 `Source/`、`Plugins/` 内。
- **测试、性能、VR 舒适度与设备**：无影响。本次**不重跑**任何脚本（重建冻结令同时生效）。
- **进度、成本与依赖**：低。4 个文件共 84,594 字节。
- **治理正文、索引、登记册和 Skill**：改 `AGENTS.md` 一条并新增一条；新增 `.trae/tools/README.md`；`.trae/CHANGELOG.md` 记录。

## 4. 执行边界

- **允许修改的绝对路径**：
  - `D:\AWork\Unreal\Project\VRSanguoYanWuchang\AGENTS.md`
  - `D:\AWork\Unreal\Project\VRSanguoYanWuchang\.trae\tools\`（新建）
  - `D:\AWork\Unreal\Project\VRSanguoYanWuchang\.trae\CHANGELOG.md`
- **禁止路径**：UE 工程四目录；`.trae/governance/`、`.trae/knowledge/GameMasterPlan.md`、`.trae/skills/`（锁定事实源，本次不动）。
- **前置条件**：用户明确批准（2026-09-10 会话内答「搬进项目，纳入备份」）。
- **强制停止条件**：任一脚本搬运后 SHA256 与原件不一致 → 立即停止并报告。
- **是否需要管理员权限/外部凭据/联网**：否。
- **是否包含删除、迁移、批量重命名或格式升级**：包含**迁移**（复制入库）。**原件在推送成功前不删除**（见 §5）。

## 5. 风险与回滚

- **已知风险 ①**：脚本内有指向项目外的绝对路径（`rebuild_v5.py` 的 `TMP_DIR` 指向 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp`；`DOCS_DIR` 指向 `Docs\Scene`）。**判定为有意为之**（临时产物不入项目，符合磁盘与临时文件规则），已在 `.trae/tools/README.md` 注明，**本次不改脚本内容**。
- **已知风险 ②**：移动后旧引用（`CHANGELOG.md` 历史条目、`session-20260908-002.md`、`execution/arena-gameplay-decisions.md`）仍写 `D:/AWork/TraeAdmin/.../rebuild_v5.py`。**处理**：CHANGELOG 为追加式历史，不回溯改写；新记录一律引 `.trae/tools/scene/`；旧路径引用保持可读。
- **已知风险 ③**：`D:\AWork\TraeAdmin\` 无备份。**处理**：先复制入库并逐文件校验 SHA256，**推送成功后才回收原件**——在入库副本进入远程仓库之前，原件保留为唯一回退。
- **风险负责人**：decision 指挥台。
- **回滚锚点**：`D:\AWork\TraeAdmin\VRSanguoYanWuchang\` 四个原件（推送前）；推送后为 git 历史。
- **回滚步骤**：`git rm` 入库副本 + 还原 `AGENTS.md` §文件边界两条 + 删除 `.trae/tools/`。
- **回滚验证**：`dashboard/check-integrity.py` 全绿；`AGENTS.md` 规则编号仍严格递增。

## 6. 验证计划

- **静态检查**：`python dashboard/check-integrity.py` 全 25 项通过。
- **自动化测试**：不适用（无代码变更）。
- **UE 编译/编辑器验证**：不适用（本次不触碰 UE 工程，不重跑脚本）。
- **PICO 真机验证**：不适用。
- **文档逐份回读**：`.trae/tools/README.md`、`AGENTS.md` 逐份回读。
- **唯一 Skill 检查**：仅一个带 frontmatter 的 `SKILL.md`（`check-integrity.py` 覆盖）。
- **证据保存位置**：搬运前后 SHA256 比对输出（本 CR §7），`dashboard/check-integrity.py` 输出。

## 7. 审批

- 审批结论：`已批准`
- 审批意见：用户在 2026-09-10 会话内就"脚本落点"选项明确选择「**搬进项目，纳入备份**」（该选项同时告知需批准一次规则变更）。
- 批准的实施范围：§4 允许修改的绝对路径全部。
- 附加约束：**原件在推送成功前不得删除**；本次不重跑任何脚本。

### 搬运校验（实施证据）

| 脚本 | 字节 | SHA256[:16] 原件 | SHA256[:16] 入库 | 结果 |
|---|---|---|---|---|
| `rebuild_v3.py` | 15,027 | `23187469D0872087` | `23187469D0872087` | 一致 |
| `rebuild_v4.py` | 18,018 | `59D7A6FB45BC3A85` | `59D7A6FB45BC3A85` | 一致 |
| `rebuild_v5.py` | 50,614 | `D3F562935DC9A841` | `D3F562935DC9A841` | 一致 |
| `flip_topdown.ps1` | 935 | `FC68C2D0C0887EA4` | `FC68C2D0C0887EA4` | 一致 |

## 8. 实施与关闭

- 实施任务编号：本 CR 自身（规则变更 + 文件搬运，non-UE 变更，不另立 MNN-TNNN）
- 实施结果：`AGENTS.md` §文件边界已增改；`.trae/tools/scene/` 已建并入库 4 个脚本；`.trae/tools/README.md` 已建。
- 偏差：无。
- 验证结果：见 §6、§7 搬运校验表。
- 更新的权威正文：`AGENTS.md` §文件边界。
- 更新的索引/登记册/变更记录：`.trae/tools/README.md`（新建）、`.trae/CHANGELOG.md`。
- 遗留风险与后续任务：① 推送成功后回收 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\` 的 4 个原件（需用户逐项批准）；② 该目录下另有 `repair_status_json5.js` / `verify2.js` / `verify3.js` 等一次性脚本与 `tmp\` 事故证据链，处置另行裁定。
- 关闭人：decision 指挥台
- 关闭日期：2026-09-10
