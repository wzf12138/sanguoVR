# t2 盘点报告 · 治理与会话产物

- 任务：t2「盘点治理与会话产物：.trae 分层、孤儿任务目录、三方状态一致性、会话记录、AgentHub 信箱」
- 归属：AgentTeams 团队 `vrsanguo-audit-backup` / 成员 scout-governance
- 盘点时点：2026-09-10 22:4x（本机本地时间）
- 作业性质：**只读**。本次未修改 `.trae` 下任何既有文件、未改动 STATUS.json / 登记册 / 会话记录 / CR、未移动或归档任何 AgentHub 信件（`hub_check` 全部 `archive=false`）、未关闭编辑器和 pid 24284、未运行 `rebuild_v5.py`、未改写 `Docs/Scene/`。
- 本文件是本任务唯一写盘产物（授权路径，AGENTS.md 规则 20b）。
- 判定口径：A=废弃、B=冗余、C=活跃、D=待定、E=不应入库。

---

## 0. 结论速览（给指挥台的动作项）

| # | 结论 | 判定 | 证据锚点 |
|---|---|---|---|
| K1 | **治理层状态不是"一处权威"，而是 5 处副本漂移**：根 STATUS.json 权威值与 `07-task-register.md`、`integrity.yaml`、`manifest.yaml`、任务包本地 `STATUS.json` 三方以上不一致，其中 M01-T005 已 approved/completed 却仍被 2 份治理契约声明为 in_progress | B | §3.1 矩阵 |
| K2 | **M01-T005 记的"v3 关卡"在磁盘和 Git 里都不存在**：`L_Prototype_1v1_v3.umap` 从未进过 Git，当前 `Content/VRSanguo/Dev/` 下也没有；而根 STATUS.json（5641 字 note）与报告、会话记录以"已保存+只读"口径记录它 | A | §4.1 |
| K3 | **M01-T005 状态用了非法词 `completed`**，不在 policy.md §6 允许集合内，且 `check-integrity.py` 关键词表无此词 → CI 此刻对 M01-T005 必然判不一致 | D | §3.2 |
| K4 | **3 个空的孤儿任务目录**（`active/M00/`、`active/M01-T002/`、`active/M01-T006/`）+ 1 个空目录 `execution/requests/`；项目历史上同类空目录被明确清理过，工具会再生成 → 会持续复发 | A | §2.2 |
| K5 | **6 个被引用的会话记录文件不存在**（session-20260811-001 / 20260813-001 / 20260819-001 / 20260824-001 / 20260824-002 / 20260825-001），共 16 处引用；规则 26 要求会话记录是认领的前置条件，断链后不可回溯 | A | §5.1 |
| K6 | **AgentHub 信箱有 13 封未回信（含 7 封 urgent）**，最新两封是 2026-09-10 21:42 的"重建冻结令/编辑器共享进程冲突预警"；冻结令里明确禁止重跑 `rebuild_v5.py`，与本次备份任务同源风险 | C（活跃信源） / D（待裁定） | §6 |
| K7 | **`Docs/` 已在本项目被治理判定为废弃、且从未进过 Git**；现又出现未跟踪的 `Docs/Scene/` 生成物（含 2.85MB PNG），其自身文档写明"勿手改：单源 rebuild_v5.py 重跑生成" | A / E | §7.1 |
| K8 | **`.agent-teams/` 当前团队运行态会被基线提交吃进去**：`.agent-teams/vrsanguo-audit-backup/`（含 team.json 51KB + inbox jsonl）未被 .gitignore 覆盖，且内含 57 处本机绝对路径 | E | §7.2 |
| K9 | **`.dsh-uploads/`（3.1MB，含 2 张 1.4MB 手机截图）未被忽略且与项目内容无关** | E | §7.3 |
| K10 | **本会话无 Python 解释器**（PATH 无 `python`/`py`/`python3`，常见安装位与 `D:\App\trae` 下均无 `python.exe`）→ 治理门禁 `dashboard/check-integrity.py` 与 CI 无法在本会话执行；我按脚本源码做了静态复算（§8） | 未能查明（运行态） |
| K11 | 治理文件自身的"磁盘红线"存在一处**内部冲突**：`ExecutionModel.md:124` 仍写"临时文件 → `c:\Users\PC\.trae-cn\work\...`"，与 AGENTS.md 磁盘规则（禁止写 C: / 用户主目录）及本任务画像（临时文件仅 `D:\AWork\TraeAdmin\...\tmp\`）直接矛盾 | D | §9 |
| K12 | `.trae` 目录本身健康度尚可：167 文件 / 874KB，markdown 本地链接 **161 条 0 断链**（复算 `check-integrity.py` 同款算法） | C | §1.2 |

**给指挥台的最小动作建议**（本任务不执行，仅建议）：
1. 基线提交前先裁定 K2/K3/K4/K5/K7/K8/K9 —— 否则首推即把"记录不存在之物"和"运行态/临时物"一起固化进历史。
2. K6 的 21:42 冻结令**必须先确认是否仍然生效**：若生效，`git-operator` 的提交动作本身不违反它（冻结只针对编辑器/关卡重建），但任何"重启编辑器"类动作禁止。
3. K1/K3/K4/K5 属治理一致性缺陷，建议单独立修复任务（不要塞进本备份任务）。

---

## 1. `.trae` 分层盘点

### 1.1 体量与分布（只读统计）

| 顶层项 | 文件数 | 字节 | 说明 |
|---|---|---|---|
| `CHANGELOG.md` | 1 | 114,763 | 900 行，全 LF；单文件占 `.trae` 总字节 13.1% |
| `execution/` | 86 | 495,595 | 最大分区；含 active 任务包、CR、会话、报告、模板 |
| `knowledge/` | 24 | 92,638 | |
| `governance/` | 11 | 60,629 | |
| `registers/` | 13 | 57,927 | |
| `standards/` | 11 | 23,817 | |
| `systems/` | 8 | 22,585 | |
| `vr/` | 7 | 9,511 | |
| `skills/` | 1 | 6,671 | 唯一 Skill，带 frontmatter |
| `archive/` | 1 | 399 | |
| 根文件（index/manifest/integrity/README） | 4 | 9,799 | |
| **合计** | **167** | **~894,334** | |

- 目录数：10 个一级目录 / 18 个二级目录。空目录 4 个（见 §2.2、§2.3）。
- 全 `.trae` 文本文件**无混行尾**（复算：CRLF 与 bare LF 混用的文件数 = 0；CHANGELOG 为 899 LF / 0 CRLF）。

### 1.2 链接与结构完整性（我复算，非引用 integrity.yaml）

- 复算 `check-integrity.py` 的 `check_markdown_links()` 同款算法（同正则、同相对解析、排除 http/https/mailto/#）：**检查 161 条本地链接，断链 0 条**。
- 注意：`integrity.yaml` 记的是 `checked: 115, broken: 0`（2026-08-14 口径，文末注明"全量复查顺延"）。**115 与实际 161 不符属陈旧计数**，不是断链。
- 唯一 Skill 约束成立：`skills/` 下带 frontmatter 的 `SKILL.md` 数量 = 1。
- 五份必需小写 `index.md`（standards/vr/systems/registers/knowledge/Design）全部存在，无对应 `README.md` → 与 `check_lowercase_indexes` 期望一致。
- `manifest.yaml` 声明的全部路径均存在 → 与 `check_manifest_files` 期望一致。
- `collections` 八项计数与磁盘实况逐项相符（task_templates 3、standards 10、vr 5、systems 7、registers 11、production 6、pattern 1、backlog 1）→ 与 `check_collection_counts` 期望一致。

---

## 2. `.trae/execution` 分层与孤儿任务目录

### 2.1 active 任务包（7 个，五件套完整）

| 任务包 | 五件套 | 额外文件 | 本地 STATUS.json 与根权威 | 会话记录 |
|---|---|---|---|---|
| `M00-T004` | 5/5 | — | MATCH（approved） | 引用 `session-20260811-execution`（**该字符串不符合 `session-{YYYYMMDD}-{序号}` 格式**） |
| `M00-T005` | 5/5 | — | MATCH（approved） | — |
| `M00-T006` | 5/5 | — | MATCH（approved） | — |
| `M01-T001` | 5/5 | — | MATCH（in_progress） | `session-20260906-001` 存在 |
| `M01-T005` | 5/5 | — | **MISMATCH**：本地 in_progress（updatedAt 2026-09-08）vs 根 completed | `session-20260908-002` 存在 |
| `M02-PREP-001` | 5/5 | `CR-20260824-001.md`（CR 放进任务包而非 `execution/CR-*.md`，与其余 6 份 CR 命名位置不一致） | MATCH（approved） | — |
| `M02-PREP-002` | 5/5 | — | MATCH（approved） | `session-20260831-001` 存在 |

- 根 STATUS.json 的 `activeTasks` 7 项与磁盘 7 个"有内容的"任务包一一对应，无"根里有、盘上没有"的任务 → `check_five_piece_set` 对现有 7 包会判通过。

### 2.2 孤儿任务目录（A 类）

三个**完全空**的目录，无任何文件：

| 目录 | mtime | 判定 |
|---|---|---|
| `.trae/execution/active/M00/` | 2026-08-10 00:09 | A（废弃外壳） |
| `.trae/execution/active/M01-T002/` | 2026-08-22 22:35 | A（计划任务外壳） |
| `.trae/execution/active/M01-T006/` | 2026-08-22 22:28 | A（计划任务外壳） |

- 成因可证：`07-task-register.md` L15/L19 把 M01-T002/M01-T006 登记为"待生成"（依赖 M01-T001 approved），说明是**提前建壳**；M00/ 是同名里程碑目录与任务包目录同处一层的歧义残留。
- **关键**：`dashboard/check-integrity.py:271-302` 只遍历根 STATUS.json 的 `activeTasks`，**从不遍历 active 目录本身** → 这 3 个空目录对治理门禁完全不可见，无任何检查项会报它。这是它们能长期留存、并被反复重建的直接原因。
- 历史先例（同一份 CHANGELOG 两处）：L834「删除 `execution/active/` 下 10 个 0 字节空文件与 `M00/` 空目录」；L807「删除废弃的 `.trae/tasks/` 空目录（含 `active/M00`…）」；L846「`M00/` 空目录…需用户手动删除」。→ **已删过至少两次，仍再次出现**，说明每次任务生成器都会重建，属"复发型冗余"，不是一次性遗留。

### 2.3 其它空目录

| 目录 | 判定 | 依据 |
|---|---|---|
| `.trae/execution/requests/` | A | 目录存在但内无任何文件；CHANGELOG L774 已记「删除 `execution/requests/README.md`（空目录说明，目录内无实际变更请求文件）」→ 说明该目录的**用途本体已被判定为空**，仅目录壳残留 |

> `execution/milestones/` 与 `execution/M00/` 均**非**孤儿：前者含 `M00-acceptance.md`（2623B，M00 验收记录），后者含 `README.md` + `T001`~`T006` 六份里程碑正式详规（CHANGELOG L821 明确"档案 vs 执行包，职责不同，不合并"）→ 判定 **C（活跃档案，保留）**。

### 2.4 变更请求（CR）

- 磁盘 7 份 CR，位置：`execution/` 下 6 份（`CR-20260903-001/002`、`CR-20260905-001`、`CR-20260907-001`、`CR-20260908-001`、`CR-20260909-001`）+ `active/M02-PREP-001/` 内 1 份（`CR-20260824-001`）。
- 全库 7 个 CR ID 引用 → 7 个文件存在，**0 悬空引用、0 无引用文件**（双向干净）。→ C 类。
- 唯一瑕疵：`CR-20260903-001.md` 是 7 份里唯一**文件名不含语义 slug** 的（其余 6 份均为 `CR-日期-序号-主题.md`）→ 轻微 B（命名不一致，不影响功能）。

---

## 3. 三方（多方）状态一致性

### 3.1 一致性矩阵（只读实测）

权威：根 `.trae/execution/active/STATUS.json`（ExecutionModel.md:29 声明"唯一权威"）。其余为副本/引用。

| 任务 | 根 STATUS.json（权威） | 任务包本地 STATUS.json | `registers/07-task-register.md` | `integrity.yaml` | `manifest.yaml` |
|---|---|---|---|---|---|
| M00-T004 | approved | approved ✅ | "已验证" | approved | approved |
| M00-T005 | approved | approved ✅ | approved | approved | approved |
| M00-T006 | approved | approved ✅ | approved | approved | approved |
| M01-T001 | in_progress | in_progress ✅ | in_progress ✅ | in_progress ✅ | in_progress ✅ |
| **M01-T005** | **completed** | **in_progress ❌** | **"执行中" ❌** | **in_progress ❌** | **in_progress ❌** |
| M02-PREP-001 | approved | approved ✅ | approved ✅ | approved | approved |
| M02-PREP-002 | approved | approved ✅ | approved ✅ | approved | approved |
| M00-DOC-001 | （不在 active） | — | approved | — | — |
| M01-T002/T003/T004/T006/T007 | （不在 active） | — | "待生成" | — | — |

**M01-T005 一处权威变更漂移到了 4 份副本之外**（本地副本停在 2026-09-08，登记册停在"执行中"，两份治理契约停在 in_progress）。规则冲突点：`ExecutionModel.md:42`「每次状态变更必须同时更新根 STATUS.json 和任务目录 STATUS.json，并在 CHANGELOG 记录」——本次未同时更新。

### 3.2 `completed` 是非法状态词（D 类，需裁定）

- `policy.md` §6 允许集合：`draft` / `ready` / `in_progress` / `blocked` / `awaiting_review` / `approved` / `archived`。
- `ExecutionModel.md:33-40` 状态迁移表：`in_progress → awaiting_review → approved|blocked`，**无 completed 一档**。
- 根 STATUS.json 里 M01-T005 的 `status = "completed"`，是 7 个任务中唯一一个不在允许集合内的取值。
- 直接后果（静态复算 `check-integrity.py:377-388`）：`status_keywords` 无 `"completed"` 键 → 回退为 `[json_status]` = `["completed"]`；而登记册该行文本是"执行中（2026-08-24 口径修正…）"，不含 "completed" → **该项必判不一致**（"STATUS.json='completed' vs 登记册='执行中'"）。
- 若登记册按 K1 改成 approved 口径，该检查会转绿；但 **`completed` 本身仍是允许集合外的词，属治理词表缺口**，需决定是"补词"还是"改值"。建议按 authority chain（policy.md §2 层级 > ExecutionModel）**把值改成 policy 允许词**，而不是给 policy 加词。

### 3.3 登记册时效性（B 类）

- `07-task-register.md` mtime = 2026-09-08 22:03；根 STATUS.json = 2026-09-10 19:17。→ **登记册落后权威 2 天**。
- 具体落后项：M01-T001 行仍写"2026-08-30 认领 session-20260830-001"，而根权威 `claimedBy = session-20260906-001`（2026-09-06 接手），且 M01-T001 的 note 已 8040 字、含 09-08~09-10 大量新事实 → 登记册该行**严重滞后**。
- `integrity.yaml` / `manifest.yaml` 均 `updated: 2026-08-30`，落后 11 天。

---

## 4. 证据链缺口（最需要指挥台注意的实质问题）

### 4.1 M01-T005 的"v3 关卡"：记录存在、物证不存在（A 类）

**记录侧**（三份文件都以既成事实口径描述 v3）：
- 根 `STATUS.json` M01-T005 note（5641 字）：「全新单脚本重建 `L_Prototype_1v1_v3`（`/Game/VRSanguo/Dev/`，**已保存+只读**；v2 umap 恢复只读）…证据：Saved/Evidence/M01-T005/（14 张…）…脚本单源 `D:/AWork/TraeAdmin/VRSanguoYanWuchang/rebuild_v3.py`」
- `.trae/execution/reports/tasks/M01-T005.md`、`.trae/execution/sessions/session-20260908-002.md` 同样引用 `L_Prototype_1v1_v3`。

**物证侧**（实测）：
- 磁盘 `Content/VRSanguo/Dev/` 实有：`L_SkeletonTest.umap`、`L_Prototype_1v1_v4.umap`、`L_Prototype_1v1_v5.umap`、`L_Prototype_1v1_BuiltData.uasset`、`L_SkeletonTest_BuiltData.uasset`、`M_GrayBox_Red.uasset`、`M_GrayBox_Straw.uasset` —— **无 `_v3`**。
- Git：`git log --all -- Content/VRSanguo/Dev/L_Prototype_1v1_v3.umap` → **空**（从未被提交）；`git ls-files Content/VRSanguo/Dev/` 只列 `L_Prototype_1v1.umap`、`L_Prototype_1v1_BuiltData.uasset`、`L_Prototype_1v1_v2.umap`、`L_SkeletonTest.umap`。
- `git status` 亦无 v3 的删除项（说明它从未进入索引）。
- 全库文本 grep（排除 `.git`）命中 `L_Prototype_1v1_v3` 的仅 3 处治理文本 + 1 处 `Saved/SourceControl/UncontrolledChangelists.json`。

**推论（需注意不要过度解读）**：v3 可能走过"生成→保存→随后被 v4 单源脚本覆盖/替换"的路径；但从治理可见性看，与 v3 绑定的**结论、验收证据引用（Saved/Evidence/M01-T005/14 张）、脚本单源（rebuild_v3.py）**都指向一个当前无可核验产物的版本，且 v2（同类旧版本）在 Git 里是"已删除"状态。这与 AGENTS.md 规则 1/2/5（不编造测试结果、不编造文件路径、不把规划描述为实现）的**形式要件**冲突——不是因为有人编造，而是因为记录没有随产物替换而回收。**判定 A（记录与产物脱钩），建议单独立"记录回收/版本口径统一"整改项，不在本备份任务内做。**

### 4.2 两个已跟踪的 umap 在磁盘上不存在（跨界提示，交 scout-repo/scout-assets）

`git status` 显示 ` D Content/VRSanguo/Dev/L_Prototype_1v1.umap` 与 ` D Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap`，实测 `Test-Path` 两者均为 **False**。我未删除它们（只读作业）。这意味着 **Git 基线提交若不做显式处置，会把这两个删除动作一并提交**（"删掉两个曾经的关卡版本"）。该动作是否被授权属于指挥台裁定范围（本任务不代裁）。

---

## 5. 会话记录盘点（`.trae/execution/sessions/`）

### 5.1 现存 9 份（均含恢复上下文）

| 文件 | 字节 | mtime | 关联任务 | 状态线索 |
|---|---|---|---|---|
| `session-20260825-002.md` | 3,606 | 2026-09-04 | M01-T001/M01-T005（规划维护） | 无阻塞 |
| `session-20260829-001.md` | 6,786 | 2026-09-05 | M01-T001（认领） | — |
| `session-20260830-001.md` | 49,903 | 2026-09-06 | M01-T001 续 | — |
| `session-20260831-001.md` | 4,882 | 2026-08-31 | M02-PREP-002 | — |
| `session-20260904-001.md` | 2,710 | 2026-09-04 | manager/decision（**已退役**交接） | 状态=退役 |
| `session-20260904-002.md` | 26,570 | 2026-09-10 19:01 | manager/decision 指挥台 | 状态=运作中 |
| `session-20260906-001.md` | 31,083 | 2026-09-08 18:36 | M01-T001（**当前认领会话**） | — |
| `session-20260908-001.md` | 4,032 | 2026-09-08 22:07 | M01-T005 续期 | — |
| `session-20260908-002.md` | 38,310 | 2026-09-10 19:16 | M01-T005（**当前认领会话**） | — |

- mtime 规则 26 复核：根权威的 3 个 `claimedBy`（M01-T005→session-20260908-002、M01-T001→session-20260906-001、M02-PREP-002→session-20260831-001）**对应会话文件都存在**。
- **但 M01-T001 的会话记录 `session-20260906-001.md` mtime 停在 2026-09-08 18:36**，而其 note 证明 09-09、09-10 仍有大量活动（且执行侧 09-10 的汇报活动有 AgentHub 侧证，见 §6）。→ 疑似违反 `ExecutionModel.md:143`「CK-02/CK-04/CK-05 汇报前必须先写入会话记录」与规则 26 的持续维护要求。**判定：待定（D），需向该会话核实，不得由我代判。**

### 5.2 被引用但文件不存在的会话（A 类）

| 缺失会话 ID | 引用处数 | 引用位置（示例） |
|---|---|---|
| `session-20260825-001` | 7 处 | `session-20260825-002.md`（"M01-T005 正由 session-20260825-001 执行光照迭代"）、`session-20260904-001/002.md`、`session-20260908-001.md` 明写"初始扩建会话，STATUS.json 中 claimedBy 仍登记为 session-20260825-001，需更新"、`ExecutionModel.md`、`CHANGELOG.md` |
| `session-20260824-002` | 3 处 | `M02-PREP-001.md`、`reports/tasks/README.md`、`active/M02-PREP-001/CR-20260824-001.md` |
| `session-20260813-001` | 2 处 | `reports/tasks/M01-T005.md`、`CHANGELOG.md` |
| `session-20260811-001` | 1 处 | `ExecutionModel.md`（**格式示例**，非真实引用，不计） |
| `session-20260819-001` | 1 处 | `CHANGELOG.md` |
| `session-20260824-001` | 1 处 | `active/M02-PREP-001/CR-20260824-001.md` |
| `session-20260831-002` | 1 处 | `session-20260904-002.md`；**该会话文件实际存在于项目外** `D:\App\trae\AgentHub\sessions\session-20260831-002.md`（2890B，2026-09-03） |

- 排除"格式示例"性质的引用后，**6 个真实缺失会话、共 16 处引用**。`sessions/` 下无 `archive/` 子目录，这些记录确实不在项目内。
- 治理后果：规则 26 把"会话记录缺失"直接判为"认领未完成"，而现在引用它们的却是**已 approved 的任务报告与 CR**（M02-PREP-001、M01-T005）→ 事后不可回溯。
- **判定 A**；但**不建议删除这些引用文本**（历史审计价值），建议在 `sessions/` 加一份 `README.md`（或 MISSING 索引）如实登记"以下会话记录未留存"，把断链变成显式事实。是否做由指挥台裁定。

### 5.3 会话记录的双现场（B 类）

项目外 `D:\App\trae\AgentHub\sessions\` 另有 2 份：`session-20260830-001.md`（4,975B，2026-08-30 18:39）与 `session-20260831-002.md`（2,890B，2026-09-03）。
- 其中 `session-20260830-001` **与项目内同名文件不同内容**（项目内 49,903B）→ 同一 sessionId 存在两份正文，属"平行事实源"(policy.md §3 禁止)。
- 项目外这份的定位应由指挥台裁定：属 AgentHub 体系自身记录（`AgentHub\PROTOCOL.md` 管辖，不在本项目仓库范围），**不建议搬进项目**（会与项目内 49KB 权威版重复）。

---

## 6. AgentHub 信箱盘点（**全程只读，`archive=false`，未移动/未删除/未归档任何信件**）

位置：`D:\App\trae\AgentHub\`（项目外，`AGENTS.md` 规则 27 指定的跨会话信箱）。总量 139 文件 / 329,194 字节。

### 6.1 未回执清单（13 封，全部 ack: pending）

| 收件箱 | 未读 | 已归档 | 最新未读时间 | 优先级 | 类型 | ref |
|---|---|---|---|---|---|---|
| `inboxes/exec-m01-t001` | **10** | 13 | 2026-09-10 21:42 | **urgent** | dispatch | M01-T001 |
| `inboxes/executor` | **3** | 13 | 2026-09-10 21:35 | **urgent** | status | M01-T005 |
| `decision` | 0 | 37 | — | — | — | — |
| `manager` | 0 | 11 | — | — | — | — |
| `exec-duty` | 0 | 1 | — | — | — | — |
| `relay` | 0 | 2 | — | — | — | — |
| `research` | 0 | 1 | — | — | — | — |
| `gen-assets` | 0 | 0 | — | — | — | — |

`exec-m01-t001` 未读 10 封明细（按时间）：09-09 00:01、09-09 08:58、09-09 09:11（manager，编辑器归还）、09-09 18:17、09-10 18:38（urgent，冻结令）、09-10 18:53（解冻）、09-10 19:11（M01-T005 玩法裁定）、09-10 21:32（urgent）、09-10 21:35（urgent，落盘先于一切）、09-10 21:42（urgent，权限真相更正）。
`executor` 未读 3 封：09-10 18:38（urgent 冻结）、09-10 18:53（解冻）、09-10 21:35（urgent 环境更正）。

### 6.2 已可归档 / 需要处置的判定（**建议，不执行**）

| 组 | 内容 | 建议 |
|---|---|---|
| 已失效通知（可归档） | 09-10 18:38 冻结令（2 封副本）+ 09-10 18:53 解冻令 | 冻结与解冻已配对闭环，属历史通知 → **可归档** |
| **仍在生效的指令（不可归档，需回执）** | 09-10 21:32「重建冻结令」（`channels/blockers/msg-20260910-213225`）+ 09-10 21:42「共享编辑器进程冲突预警」（`msg-20260910-214225`） | **仍需回执**；21:42 那封的解冻条件"落盘→回读→汇报→decision 广播解冻"**至今未见解冻广播** |
| 未回执的实质派工 | 09-10 21:35「落盘先于一切」、09-10 21:42「权限真相+落盘窗口方案」 | 需执行侧回执（含文件大小/时间的事实回读） |
| 反复催办未回的 3 项 | ① L34 代码归属查证 ② 09-08~09-10 变更文件清单（区分已落盘/仅内存）③ 送达确认 | **已催 3 轮未回**（18:38、18:53、21:42 三封均列）。这三项是"未落盘改动清单"这一最大失分点的唯一补救线索 |

### 6.3 频道（未回执）

| 频道 | 封数 | 最新 | 性质 |
|---|---|---|---|
| `channels/registry-changes` | 29 | 2026-09-10 19:17 | 登记变更广播（含 19:12 decision 的玩法裁定广播、18:53 解冻广播） |
| `channels/blockers` | 2 | **2026-09-10 21:42** | **两封都在生效中**：重建冻结令、编辑器共享进程冲突预警 |

### 6.4 与本次备份任务的**直接冲突点（最高优先级提示）**

`channels/blockers/msg-20260910-214225-decision-001.md` 明写两条**当前有效冻结**：
1. **重建冻结**：M01-T001 落盘收敛前，M01-T005 侧不得重跑 `rebuild_v5.py`、不得重写 `Docs/Scene`；
2. **重启窗口冻结**：任何人不得擅自关闭/重启 pid 24284。

我方复核：`UnrealEditor` **pid 24284 仍在运行**（StartTime 2026-09-09 22:06:05，工作集 2049MB，Responding=True）→ 冻结条件**依旧成立**。
→ 对本次任务的直接含义：`git-operator` 的"只提交+推送"不触碰上述两条禁令（**不重启编辑器、不跑 rebuild_v5.py**），因此**可以在冻结生效期间执行**；但必须**明确禁止**任何"顺手重启编辑器/顺手重建关卡/顺手重写 Docs/Scene"的动作。建议指挥台把这一条写进 t10 的显式禁令。

### 6.5 派工板与中继

`dispatch.md`（628B，2026-09-03）当前为「**空闲（撤单）**」，内容明确要求中继会话勿认领 M02-PREP-002。→ **C 类，现状正确，无需动作**。

### 6.6 信箱体系定位（供指挥台裁定）

`AGENTS.md` 规则 27 规定"多会话协作一律走 AgentHub"，但本次审计备份任务运行在 **DSH AgentTeams** 体系（`.agent-teams/vrsanguo-audit-backup/`）。两套体系并存，存在"指挥台换班、旧信箱无人值班"的结构性风险——`inboxes/decision` 未读 0（说明 decision 侧在正常消费），但 `exec-m01-t001` / `executor` 的 13 封未回正是该风险的具体表现。
→ **判定 D（需指挥台裁定）**：本次任务是否需要在收尾时向 `inboxes/decision` 投一封信，告知"审计备份任务的存在与其冻结遵守情况"。我未擅自发信（发信会改变信箱状态，超出只读授权）。

---

## 7. 项目内其它治理/会话产物的边界判定

### 7.1 `Docs/`（A + E）

- `Docs/Scene/` 5 个文件（未跟踪）：`scene_plan.html` 81,359B、`scene_topdown.png` **2,853,240B**、`scene_modules.json` 7,335B、`scene_overview.md` 4,782B、`asset_checklist.md` 1,994B；mtime 均为 2026-09-10 18:53~19:15。
- **自证为生成物**：`scene_overview.md:3`「勿手改：单源 rebuild_v5.py 重跑生成；交互版见 scene_plan.html，俯视图见 scene_topdown.png」；`:17`「全部由 rebuild_v5.py 单源生成；改场景=改脚本重跑（文档自动重生成）；禁止编辑器手改」。`scene_modules.json` 头部含 `"stamp": "2026-09-10 19:14"`、`"script": "rebuild_v5.py"`、`"props": 353`。
- **治理判定早已明确**：`.trae/archive/README.md`「历史旧树（**`Docs/`**、根级 `Design/`、`TraeAI/` 等）的有效正文已迁入 knowledge/、execution/，**旧目录本体已删除，不再保留兼容入口**」；CHANGELOG L894「删除 `TraeAI`、**`Docs`**、根级旧规划目录和重复 Skill」；L897「后续不再使用 `TraeAI/` 或 `Docs/`」。
- **Git 史**：`git log --all -- Docs` 为空 → `Docs/` 从未进过 Git。
- **判定**：目录本身 **A（已被治理判废并删除过的路径）**；内容 **E（由项目外脚本重跑即可完全重生成的派生物，不应入库）**。另：`scene_topdown.png` 2.85MB 不被任何 LFS 规则覆盖（`.gitattributes` 无 `*.png`），一旦入库即为非 LFS 大二进制。
- 与本次任务的关系：`rebuild_v5.py` 属 t10 的显式禁令对象，`Docs/Scene` 属冻结令保护对象 → **两份约束叠加，建议基线提交明确排除 `Docs/`**。

### 7.2 `.agent-teams/`（B + E）

- **已跟踪（旧团队）**：`.agent-teams/archive/vrsanguo-survey/{team.json,inbox/captain.jsonl,inbox/qa.jsonl}` + `.agent-teams/retired-members.json`，由 commit `296ebed`（2026-09-03）引入。→ **B（历史团队运行态，非项目内容）**；`team.json` 18,410B，`captain.jsonl` 20,473B。
- **未跟踪（当前团队）**：`.agent-teams/vrsanguo-audit-backup/{team.json 51,648B, inbox/captain.jsonl 5,949B, inbox/git-operator.jsonl 3,258B, inbox/planner.jsonl 2,809B}`。
- **三处硬证据表明不应入库**：
  1. `.gitignore` **没有**任何 `.agent-teams` 规则（实测 `git check-ignore` 对 `.agent-teams/vrsanguo-audit-backup/team.json` 返回无匹配）→ 当前处于"会被提交"状态（`git status` 显示 `?? .agent-teams/vrsanguo-audit-backup/`）。
  2. 全库 grep（含 AGENTS.md、README.md、integrity.yaml、manifest.yaml、check-integrity.py）**零处**提及 `agent-teams` / `dsh-uploads` → 不属任何治理白名单，也**不属 CI 检查的"排除目录"集合**（`check_large_files` 的排除集为 `.git/.vs/Intermediate/Binaries/DerivedDataCache/...`，不含它）。
  3. 内容含 **57 处本机绝对路径**（如 `D:\\AWork\\Unreal\\Project\\VRSanguoYanWuchang`、`D:\\AWork\\TraeAdmin\\VRSanguoYanWuchang\\tmp\\`）——属 AGENTS.md 规则 23「禁止提交…本机路径凭据」的形态。
- **判定 E**：当前团队运行态（含成员 inbox 原始 jsonl）**不应进入基线提交**。

### 7.3 `.dsh-uploads/`（E）

- 3 个文件 / **3,105,958 字节**，未跟踪、未被忽略：
  `693ce656e56ba26e-deepseek-whale-400.png` 70,024B、`c013349bbeec8198-Screenshot_2026-09-09-22-53-11-091_com.limelight.root.jpg` 1,474,431B、`cd6db11113373745-Screenshot_2026-09-10-08-26-58-474_com.limelight.root.jpg` 1,418,003B。
- 性质：DSH 会话的**用户上传中转目录**（文件名含 sessionId `session-2a22b421-...`；两张截图来自手机端 Moonlight 串流 App），非项目内容；`.jpg` 不被任何 LFS 规则覆盖。
- **判定 E**：本地诊断素材，不应入库。

### 7.4 `dashboard/`（C，健康）

- 已跟踪仅 6 个源文件（`.gitignore`、`__init__.py`、`asset_scanner.py`、`check-integrity.py`、`generate-static.py`、`server.py`）。
- 生成物 `status.json`（189,625B）、`integrity.json`（3,858B）、`index.html`（64,825B）、`__pycache__/` 均被 `dashboard/.gitignore` 正确忽略（实测 `check-ignore` 三项全部命中）。→ **C，无需动作**。

### 7.5 `.workbuddy/`（C，已处置）

已被根 `.gitignore:93` `.workbuddy/` 覆盖（实测命中）→ **已正确排除，无需动作**。

### 7.6 项目根零星忽略项（C）

`gcm-diagnose.log`（Git Credential Manager 诊断日志，被 `*.log` 忽略）、`.vs/`、`ArchivedBuilds/`、`Binaries/`、`Build/Android/FileOpenOrder/`、`DerivedDataCache/`、`Intermediate/`、`Saved/`、`Plugins/*/{Binaries,Intermediate}/`、`Content/VRSanguo/Dev/L_SkeletonTest_BuiltData.uasset` → 全部按设计忽略，**C**。

---

## 8. 治理门禁可执行性（**未能查明 = 未执行**，如实记录）

> ### ⚠ 更正注记（2026-09-10，依指挥台指令补记）
>
> **本节所依据的「本会话无解释器」前提已被推翻。**
> 本机**有**可用解释器：`D:\App\trae\Traedata\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe`。本报告作者已复核该路径存在且可用，实测输出：`py 3.10.11 | pyyaml 6.0.3`。它**只是不在 PATH 上**——故 `Get-Command python` / `py` 查不到，我当时搜索的若干常见安装目录也不是它的位置。**「PATH 上没有」不等于「本机没有」**，本节原结论正是在此处失准。
>
> **已实际发生**：指挥台**实跑** `check-integrity.py` → `exit=1｜25 项检查｜23 通过｜2 失败`，两项失败均指向 M01-T005（`非法状态 'completed'`；与登记册不一致）。verifier **独立复现**，逐项与指挥台一致，并实测污染为 0（`git status -- dashboard` 为空，四个产物全被 `dashboard/.gitignore` 拦下）。结果见 t5 报告。
>
> **本节证据等级据此下调**：下方静态复算**仅作方法论留痕，不得被下游当作实证引用**；一切以 t5 报告的实跑输出为准。
>
> 与本节结论的对照（留痕用）：本节静态复算预判「至少 1 项会红（`check_task_register_consistency`）」，实跑为 **2 项失败、且两项同源**（都指 M01-T005 的 `completed`）——方向一致但**项数不精确**，这正是静态推断不能替代实跑的直接例证。

- **本会话无 Python 解释器（实测）**：`Get-Command python` / `py` / `python3` 均无结果；`C:\Program Files`、`C:\` 根、`C:\Users\PC\AppData\Local\Programs` 下无 Python 目录；`D:\App\trae`、`D:\App\deepseekharness`、`D:\App\workbuddy` 下（深度 6）无 `python.exe`。**（← 该实测只能说明「不在 PATH 及上述目录」，不能推出「本机无解释器」；见上方更正注记。）**
- 因此 `dashboard/check-integrity.py` **在本会话无法执行**。注意：`main()` 在缺 PyYAML 时会 `pip install PyYAML`（写入 C:），我不具备执行条件也**不应**触发该分支。
- 替代做法（已做）：**按脚本文法静态复算**，结果如下表。标注"复算"即由我按同款算法实测得出，非脚本运行输出。

| 检查项（脚本函数） | 静态复算结论 | 依据 |
|---|---|---|
| `check_forbidden_root` | 通过 | `D:\AWork\Unreal\Project\.trae` 不存在 |
| `check_manifest_files` | 通过 | manifest 声明的 12 条路径全存在 |
| `check_collection_counts` | 通过（8/8） | §1.2 逐项相符 |
| `check_lowercase_indexes` | 通过 | 5 目录均有 index.md 无 README.md |
| `check_skill_frontmatter` | 通过 | 1 个带 frontmatter |
| `check_markdown_links` | **通过** | 161 链接 / 0 断链（复算） |
| `check_active_gate` | 通过（预期） | 根 STATUS.json 可解析、7 项齐全 |
| `check_five_piece_set` | 通过（预期） | 7 包全部 5/5 |
| `check_allowlist_conflict` | **未能查明** | 需比对 2 个 in_progress（M01-T001、M01-T005 —— 后者因根权威=completed 而不计入）的 ALLOWLIST 独占路径；未逐行复算 |
| `check_task_register_consistency` | **会失败** | M01-T005：`completed` vs 登记册"执行中"（§3.2） |
| `check_verification_evidence` | **未能查明** | `09-verification-register.md` 仅校验其中 `.trae/` 形式的路径；未逐条复算 |
| `check_task_verif_consistency` | **存疑** | M01-T005 任务行含"执行中"不属"已验证/approved"，若 V-00x 标"已验证"则触发不一致；未逐条复算 |
| `check_tech_debt_status` | **未能查明** | `11-tech-debt-register.md`（12,174B）open 计数未复算 |
| `check_awaiting_review_timeout` | 通过 | 无 awaiting_review 任务 |
| `check_rules_numbering` | 通过 | AGENTS.md 各节内编号严格递增（实测 28 条，节内无重复/回退） |
| `check_changelog_freshness` | **会失败**（提交前） | CHANGELOG 顶部条目日期 2026-09-10 vs HEAD 提交日期 2026-09-04（HEAD=eb319c3）→ `top >= head` 成立，**实际会通过**；提交后若 CHANGELOG 不再更新而新提交日期超过 09-10，则转为失败。**基线提交时必须同批更新 CHANGELOG** |
| `check_large_files` | 通过（预期） | 复算：排除集外的可提交范围内无 >100MB 文件（最大 `环首刀.uasset` 28.0MB） |
| `check_secret_patterns` | 通过（复算） | 对 14 个待提交文本文件扫 `sk-`/`ghp_`/`AKIA`/私钥块 → 0 命中 |

**结论**：CI 门禁在当前工作树上**至少 1 项（任务登记册一致性）会红**，另有 5 项未能查明。建议指挥台在 t10 之前先行修复 §3.1 的 M01-T005 口径，或明确接受"首推红门禁"并记录原因。

---

## 9. 治理正文内部矛盾（D 类，需裁定）

`governance/ExecutionModel.md:124`（"铁律启动验证"第 2 条·磁盘规则自检）：

> 2. **磁盘规则自检**：在创建任何文件前，确认目标路径符合磁盘规则（项目文件 → D: 项目内；**临时文件 → `c:\Users\PC\.trae-cn\work\...`**；大文件下载 → E:）。

- 与 AGENTS.md 磁盘规则直接冲突：「**禁止将任何文件写入 C 盘或用户主目录**（`C:\Users\`）」。
- 实测 `C:\Users\PC\.trae-cn\work` **确实存在**（说明该路径曾被实际使用，非纯笔误），且本任务画像/团队约束明确"临时文件只写 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\`"。
- 权威链（policy.md §2）：3=治理契约（definition-of-done / responsibility-matrix / 已批准 CR）> 4=根级 AGENTS.md 与唯一 Skill。`ExecutionModel.md` 未列入 §2 显式层级，但属"四份操作模型"；**无论按哪一级，都不应凌驾 AGENTS.md 的 C 盘禁令**。
- **判定 D**：需指挥台裁定改法（建议改为指向项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\`）。注意 `ExecutionModel.md` 属治理正文，AGENTS.md 规则 24 的锁定文件清单未列它，但修改仍应走变更申请（policy.md §8）。

### 9.1 其它不一致（B 类；B-2 已按裁断升级，严重度高于一般 B）

- **B-2 · `active/M00-T004`：副本未随权威清空（已按指挥台 2026-09-10 裁断升级）**
  两文件实测对照（指挥台已亲自复核，为权威口径）：

  | 文件 | `claimedBy` | 其它字段 |
  |---|---|---|
  | **根权威** `.trae/execution/active/STATUS.json:4-11` | **JSON `null`**（第 7 行） | `status=approved`、`startedAt`/`updatedAt`、`note`；**无 `approvedAt`** |
  | **任务副本** `.trae/execution/active/M00-T004/STATUS.json` | `"session-20260811-execution"`（第 6 行，len=26） | **多 `approvedAt: "2026-08-13"`**；用 `info` 而非 `note`；第 2 行 `_note` 自述「冲突时以根 STATUS.json 为准」 |

  - **条目定性**：不是「claimedBy 格式异类」，而是「**副本未随权威清空**」。
  - **性质（本轮升级要点）**：副本**自己声明**「冲突时以根 STATUS.json 为准」，却仍留着权威已清空的值；且字段结构同时漂移（`approvedAt` 只存在于副本、`info` vs `note`）。→ **这是「副本自身声明从属、却未跟随权威」的实例**，与 **K1（M01-T005 一处权威漂移到 4 份副本之外）同型**。
  - **门禁缺口（关键）**：`dashboard/check-integrity.py` 对这类**根↔副本漂移无任何检查覆盖** —— 它的 `check_five_piece_set` 只验副本存在性、`check_task_register_consistency` 只比"根 vs 登记册"，**从不比对根 vs 副本**。故本缺陷此前不可能被任何自动化发现，只能靠人工盘点（即本项）。
  - **实际严重度高于一般 B**：因其同时具备 ①从属声明被自身违反 ②无门禁可发现 ③结构字段额外漂移 三重特征。建议修复时"副本回灌权威"与"补一条根/副本字段一致性检查"同时做。
  - **本报告作者的取证留痕（已闭环）**：我按 AGENTS.md 规则 2/18 重读原文件复核后**未按转述的「空字符串」改写本项**，而是留实证请裁断——原文含 `  "claimedBy": "session-20260811-execution",`，结构化读回 `claimedBy=[session-20260811-execution] (len=26)`，该字符串另在 `.trae/CHANGELOG.md` 独立出现。指挥台复核后**裁定实证成立**，并明确 verifier 的「空字符串」措辞不准确——根权威里是 **JSON `null`**，不是 `""`（不是读错文件，而是类型描述不精确）；verifier 已去函在 F-6 中订正为 `null`。
  - **状态**：争议已闭，本条按上述口径定稿。

- `M02-PREP-001` 的 CR 放在任务包内（`active/M02-PREP-001/CR-20260824-001.md`），其余 6 份 CR 在 `execution/` 根 → 位置不一致。
- `integrity.yaml` 的 `local_markdown_links.checked: 115` 与实况 161 不符（陈旧计数）；`active_gate` 内 7 条状态有 5 条与根权威不符（表见 §3.1）。
- `.trae/index.md` 的 Execution 基线段（L61-66）列了 6 个任务包链接，**漏 `M02-PREP-002 任务包`** —— 而该任务包存在且状态 approved。属索引漏项（**A，需补**）。

---

## 10. 判定汇总（A/B/C/D/E）

### A · 废弃

1. `active/M00/`、`active/M01-T002/`、`active/M01-T006/` —— 3 个空孤儿目录（历史已删过 ≥2 次，会复发）。
2. `execution/requests/` —— 空目录（其唯一文件的历史处置记录见 CHANGELOG L774）。
3. 「M01-T005 的 v3 关卡口径」—— 记录存在、产物不存在（记录与产物脱钩，需记录回收）。
4. `Docs/` 目录本体 —— 已被 `archive/README.md` + CHANGELOG 判废并删除过。
5. 6 个不存在的会话记录 ID 的"隐性绿链"（引用仍在、文件无）——建议改为显式登记。
6. `.trae/index.md` 缺失的 `M02-PREP-002` 任务包链接 —— 索引漏项。

### B · 冗余

1. M01-T005 状态在 4 份副本（任务包 STATUS / 登记册 / integrity.yaml / manifest.yaml）中的陈旧副本。
2. 登记册与 integrity/manifest 的时效落后（09-08 / 08-30 vs 09-10）。
3. `AgentHub\sessions\session-20260830-001.md` 与项目内同名文件正文不同 → 平行正文。
4. **B-2 · `M00-T004` 副本未随权威清空**（按指挥台 2026-09-10 裁断升级、已定稿）：根权威 `claimedBy = null` 而任务副本仍为 `"session-20260811-execution"`；副本第 2 行 `_note` 自述「冲突时以根 STATUS.json 为准」却未跟随；且字段结构漂移（`approvedAt` 仅存于副本、`info` vs `note`）。**这是「副本自身声明从属、却未跟随权威」的实例，与 K1 同型**；`check-integrity.py` **从不比对根 vs 副本，对此类漂移零覆盖**（详见 §9.1）。**实际严重度高于一般 B**，修复时建议「副本回灌权威」与「补一条根/副本字段一致性检查」同做。
5. `CR-20260824-001` 位置异类（在任务包内）；`CR-20260903-001` 缺 slug。
6. `.agent-teams/archive/vrsanguo-survey/` 4 个已跟踪文件（旧团队运行态）。

### C · 活跃（保留）

`.trae` 五份治理契约 + 四份操作模型 + 唯一 Skill + `standards/vr/systems/registers/knowledge` 编号正文 + `execution/M00/` 里程碑档案 + `execution/milestones/` + 7 个任务包 + 7 份 CR + 9 份会话记录 + `dashboard/` 6 个源文件 + AgentHub 信箱本体（`PROTOCOL.md`/`HANDOVER.md`/`dispatch.md`/`RELAYS.md` 等）+ `channels/*`。

### D · 待定（需裁定）

1. `completed` 非法状态值的处置方式（补词 vs 改值）。
2. M01-T001 会话记录 mtime 停在 09-08 是否违反规则 26（需向该会话核实，不代判）。
3. `ExecutionModel.md:124` 的 C 盘临时路径改法。
4. 本次任务是否需向 `inboxes/decision` 投信（跨体系通知）。
5. `git status` 中两个 umap 的删除是否纳入基线提交（属指挥台裁定；我只报事实）。
6. `agent_teams` / `dsh-uploads` 是否补进 `.gitignore` 与 `check_large_files` 排除集（改 `.gitignore` 本身也是提交内容，需先裁定）。

### E · 不应入库

1. `.agent-teams/vrsanguo-audit-backup/`（当前团队运行态，57 处本机路径）。
2. `.dsh-uploads/`（3.1MB 会话上传中转，含 2 张手机截图）。
3. `Docs/Scene/`（rebuild_v5.py 单源生成物，含 2.85MB 非 LFS PNG；且属当前冻结令保护对象）。

---

## 11. 建议的「清理与保留」要点（交 planner）

1. **保留原位、只登记不删除**：A 类全部。本任务硬约束禁止删除任何项目文件，故 A 类只能作为"待清理清单"交付。
2. **优先级顺序建议**：先修 D1（状态词，直接影响 CI 门禁）→ 再补 A6（索引漏链，1 行）→ 再处置 E1/E2/E3（排除出提交范围）→ 最后处理 A1/A2（空目录，需确认生成器不会立即再建）。
3. **A3（v3 口径）单独立项**：涉及报告/会话/STATUS 三处记录回收，且与 M01-T005 已 approved 的验收链相关，不应在备份任务里顺手改。
4. **A5（缺失会话）建议加 `sessions/MISSING.md` 显式登记**，把"断链"变为"已知缺失"，零风险且立即提升可审计性。
5. **C 类一律不动**，尤其 `execution/M00/`（正式详规档案）与 `milestones/M00/`，CHANGELOG L821 已裁定"不合并文件本体"。

---

## 12. 证据索引（可核验命令与原始输出摘要）

| 证据 | 命令 / 位置 | 结果摘要 |
|---|---|---|
| `.trae` 体量 | `Get-ChildItem .trae -File -Recurse` | 167 文件 / 894,334 字节 |
| 空目录 | `Get-ChildItem .trae/execution/active -Directory` + 子项计数 | M00/M01-T002/M01-T006 children=0；requests/ 无文件 |
| 五件套 | 逐目录 `Test-Path` 五项 | 7 包 5/5；3 空目录 0/5 |
| 状态矩阵 | `ConvertFrom-Json` 根 + 逐包 + 登记册 + 两份 yaml | M01-T005 四处不一致 |
| v3 物证 | `git log --all -- …v3.umap` / `git ls-files Content/VRSanguo/Dev/` / `Test-Path` | 从未提交；磁盘无 |
| 会话断链 | 全库正则 `session-\d{8}-\d{3}` + 文件存在性 | 6 个真实缺失 / 16 处引用 |
| 信箱 | `hub_status` + `hub_check(archive=false)` ×2 | 13 未读（7 urgent）/ 47 已归档 |
| 冻结令 | `channels/blockers/*` 全文 | 21:32 重建冻结、21:42 重启窗口冻结，条件仍成立 |
| 编辑器 | `Get-Process -Id 24284` | 仍在运行，启动 2026-09-09 22:06:05，Responding=True |
| Docs 生成性 | `Docs/Scene/scene_overview.md:3,17` + `scene_modules.json` 头 | 自述"勿手改，rebuild_v5.py 生成"，stamp 2026-09-10 19:14 |
| Docs 判废 | `.trae/archive/README.md` + CHANGELOG L894/L897 + `git log --all -- Docs`（空） | 已判废、已删过、从未入库 |
| .gitignore 缺口 | `git check-ignore -v .agent-teams/... .dsh-uploads/ Docs/` | 仅 `.workbuddy/` 命中（`.gitignore:93`） |
| 链接复算 | 复刻 `check_markdown_links` 算法 | 161 链接 / 0 断链 |
| Python 缺失 | `Get-Command python/py/python3` + 目录搜索 | 全部无结果 |

---

## 13. 机读摘要（供 planner / verifier 结构化消费）

```json
{
  "task": "t2",
  "member": "scout-governance",
  "scope": "governance / task-packages / sessions / AgentHub mailbox",
  "readonly": true,
  "wroteOnly": [".trae/execution/reports/audit/t2-governance-sessions.md"],
  "trae": { "files": 167, "bytes": 894334, "emptyOrphanDirs": 4, "mdLinksChecked": 161, "mdLinksBroken": 0 },
  "activeGate": { "authoritative": ".trae/execution/active/STATUS.json", "tasks": 7, "legalStatusValues": 6, "illegalStatusValues": ["completed"] },
  "stateDrift": [
    { "task": "M01-T005", "root": "completed", "packageLocal": "in_progress", "taskRegister": "执行中", "integrityYaml": "in_progress", "manifestYaml": "in_progress", "verdict": "B" }
  ],
  "orphanTaskDirs": [".trae/execution/active/M00/", ".trae/execution/active/M01-T002/", ".trae/execution/active/M01-T006/"],
  "orphanEmptyDirs": [".trae/execution/requests/"],
  "missingSessionRecords": ["session-20260811-001", "session-20260813-001", "session-20260819-001", "session-20260824-001", "session-20260824-002", "session-20260825-001", "session-20260831-002"],
  "sessionRecordsPresent": 9,
  "mailbox": {
    "root": "D:/App/trae/AgentHub",
    "totalFiles": 139,
    "totalBytes": 329194,
    "unread": { "exec-m01-t001": 10, "executor": 3 },
    "archived": { "decision": 37, "manager": 11, "exec-m01-t001": 13, "executor": 13, "exec-duty": 1, "relay": 2, "research": 1, "gen-assets": 0 },
    "urgentUnread": 7,
    "newestUnread": "2026-09-10T21:42:19+08:00",
    "activeBlockers": [
      "channels/blockers/msg-20260910-213225-decision-001.md (重建冻结令)",
      "channels/blockers/msg-20260910-214225-decision-001.md (共享编辑器进程冲突预警 / 重启窗口冻结)"
    ],
    "readonlyOps": "hub_status + hub_check(archive=false) x2"
  },
  "editorProcess": { "pid": 24284, "name": "UnrealEditor", "start": "2026-09-09T22:06:05", "wsMB": 2049, "responding": true },
  "frozenConditionsStillValid": true,
  "excludeFromBaseline": [".agent-teams/vrsanguo-audit-backup/", ".dsh-uploads/", "Docs/"],
  "unverifiable": ["（已作废，见 correctionNote）本会话曾判 check-integrity.py 25 项不可执行"],
  "correctionNote": {
    "date": "2026-09-10",
    "section": "§8",
    "overturnedPremise": "「本会话无 python 解释器」不成立；解释器在 PATH 之外",
    "interpreterPath": "D:/App/trae/Traedata/TRAE SOLO CN/ModularData/ai-agent/vm/tools/python/python.exe",
    "interpreterVersion": "Python 3.10.11 + PyYAML 6.0.3",
    "authoritativeResult": "指挥台实跑 exit=1 / 25 项 / 23 通过 / 2 失败（均指 M01-T005 completed）；verifier 独立复现一致，污染为 0；见 t5 报告",
    "evidenceGradeOfSection8": "static-inference-only；不得被下游当作实证引用",
    "lesson": "PATH 上没有 != 本机没有"
  },
  "ciExpectedFailures": ["check_task_register_consistency (M01-T005 completed vs 登记册执行中)", "check_active_gate 状态合法性 (M01-T005 completed 非 policy §6 允许词) —— 实跑 2 项失败即此两者，静态复算仅命中其一"],
  "openDisputes": [],
  "resolvedDisputes": [
    {
      "id": "D-M00T004-claimedBy",
      "resolution": "closed-2026-09-10",
      "ruling": "指挥台亲自复核后裁定：本报告作者实证成立，条目按 B-2 升级为「副本未随权威清空」；verifier 的「空字符串」措辞不准确——根权威为 JSON null 而非 \"\"（属类型描述不精确，非读错文件），verifier 已去函在 F-6 订正为 null",
      "rootAuthoritative": { "path": ".trae/execution/active/STATUS.json", "line": "4-11", "claimedBy": null, "hasApprovedAt": false, "usesField": "note" },
      "packageCopy": { "path": ".trae/execution/active/M00-T004/STATUS.json", "claimedBy": "session-20260811-execution", "claimedByLength": 26, "hasApprovedAt": true, "approvedAt": "2026-08-13", "usesField": "info" },
      "sameTypeAs": "K1（一处权威漂移到多份副本之外）",
      "gateGap": "check-integrity.py 从不比对根 vs 副本，此类漂移零覆盖",
      "severityNote": "高于一般 B：同时具备 ①从属声明被自身违反 ②无门禁可发现 ③结构字段额外漂移",
      "processNote": "本报告作者按 AGENTS.md 规则 2/18 未按转述改写，改以留证请裁断；指挥台认定该做法正确"
    }
  ],
  "counts": { "A": 6, "B": 6, "C": "多处（治理正文/任务包/CR/会话/信箱本体）", "D": 6, "E": 3 }
}
```

---

*报告完 · scout-governance · 本文件为 t2 唯一写盘产物，其余全程只读。*
