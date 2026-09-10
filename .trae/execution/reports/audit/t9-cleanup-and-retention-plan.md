# t9 · 清理与保留方案（VRSanguoYanWuchang）

- 任务：t9「汇总三份盘点，产出清理与保留方案 + Git 基线构成 + E 盘现场归位建议」
- 归属：AgentTeams 团队 `vrsanguo-audit-backup` / 成员 planner（engineer · 清理与保留方案 / 交接清单）
- 写盘时点：2026-09-10（本机本地时间）
- 输入：t1 `AUDIT-repo.md`、t2 `t2-governance-sessions.md`（42,283 B）、t3 `t3-asset-and-artifact-inventory.md`（31,896 B）；指挥台裁定包（R1–R7、Docs 更正裁定、两项备份缺口、Actions 口径、网络与远程拓扑更正、Q1/Q2 答复）
- 作业性质：**只写文档，不执行任何处置**。唯一写盘路径 = 本文件（`.trae/execution/reports/audit/`，AGENTS.md 规则20(b) 授权）。
- 未做：未删除/移动/重命名任何项目文件；未改 `.gitignore`/`.gitattributes`/STATUS.json/登记册/会话记录/CR；未运行 `check-integrity.py`；未 `git add`/`commit`/`push`；未关闭或触碰 UnrealEditor（pid 24284）；未跑 `rebuild_v3/v4/v5.py`；未改写 `Docs/Scene/`；**未在 E: 或 D: 新建任何文件夹或文件，未移动或删除 E:/TraeAdmin 下任何东西，未移动任何证据或参考图**。
- 只读复核：本方案执行了 `git status --porcelain -uall`、`git rev-parse`、`git for-each-ref`、`git symbolic-ref`、`git ls-files`、目录/文件尺量与读取等**只读**命令（见 §12 证据索引）。所有数字均可按该节命令复算。
- 分类桶（全队共用）：A-废弃 / B-冗余 / C-活跃 / D-待定 / E-不应入库。

### 修订记录

| 版本 | 时点 | 变更 |
|---|---|---|
| v1 | 2026-09-10 | 初版：按指挥台 R3 裁定把 `Docs/Scene/` 5 文件**列为入库** |
| v2 | 2026-09-10 | 依指挥台**更正裁定**把 `Docs/Scene/` **改为排除**（v1 那条是错的，已作废）；并入 R1–R7 裁定、两项备份完整性缺口、Q1/Q2 答复；新增 §1.3 缺口章、§4.6 留痕章；`Saved/` 升级为清理前置条件；暂存清单 48 → **43 条** |
| v3 | 2026-09-10 | 依指挥台**紧急撤销令**：**取消在本次基线内修改 M01-T005 状态**（撞用户既有裁定 `session-20260904-002.md:156`「勿自行改」）→ 2 项 CI 红登记为「已知 / 已立案 / 待用户裁定」，**本次不清零**；**t10 停止条件改写**：`exit≠0` 不再是停止条件，改为「出现白名单之外的新失败项才停」；新增「2 项红」与「5 处副本漂移」的分层说明 |
| v4 | 2026-09-10 | 并入指挥台第二轮裁定：**提交后不自动二次提交**（改为如实记录 + 报告）；**CHANGELOG 追加由指挥台在放行前执行**（t10 只核对、不自行补写）；白名单**恰好 2 条**、第 3 项即停；**P1 降级为独立动作、不进本次基线**；**D22 改为「本机有解释器、只是不在 PATH」并写入实测绝对路径**（已实测 `--version` = Python 3.10.11）；`E:\AWorkBackup` 631MB 已作**第 6 项**呈用户；新增 **§10 放行状态（用户暂缓推送 + git-operator HOLD）**；§12 增加「按来源分层复核」的 t12 交接要求。**▍留痕：v4 写入时其替换串误覆盖了 v3 行，版本历史一度缺环（v1→v2→v4），经本方案自查发现并回补。此处保留该事实，供后人核对 —— 修订表曾被破坏过一次，不是天然完整。** |
| v5 | 2026-09-10 | 并入指挥台**第三轮裁定**：① **流程事裁定 (a) 就地接受**，并在状态说明中**显式登记「任务记录＝v1 内容」的已知偏差** + 补**版本绑定（字节数 + mtime）**；② **体量口径收口** —— 全仓 48 个 / 47.46 MiB 与 `Art/References/` 33 个 / 47.35 MiB **分范围列示并标 MiB/MB 单位**（§5.2、D31、§11.2、§12 同步）；③ **D32/P20 裁定「规则26 不适用、本轮不补建」**（本轮是 DSH AgentTeams 任务，无 `MNN-TNNN`/无 `claimedBy`），并补入已核实事实「**`check-integrity.py` 25 项中无会话记录检查项**」；④ **D26 + D32 合并为一条 CR 候选**；⑤ §10 执行闸门补写「t5 二审通过 + 用户 6 项裁定」 |
| **v6（当前）** | 2026-09-10 | **就地勘误已知错误数字**（指挥台裁定 (i)）：① 受管图片 **「39 个 PNG/JPG 46.6 MB」→「全仓 48 个 / 49,760,737 B = 47.46 MiB」**（≥1 MB 者 18 个 / 44.19 MiB）；② `openbrf.zip` **「39.0 MB」→「11.34 MB」**（11,890,974 B；t3 原记**高估 3.4 倍**）；③ `E:\AWork\Temp\VRExpansionPlugin\` 可回收 **「≈2.95 GB」→「1,926.7 MB」**（毛额 2,947.3 MB 含 **1,020.6 MB 重复计数，必须扣除**；§6.2 合计同步为 **≈1.89 GB**）。**依据来源 = planner 独立复测（F-3 / F-4 / F-8），2026-09-10**。**▍覆盖面说明：勘误不止 3 个单元格** —— 同一事实在 §2.6（3 行）、§3 P8/P9/P15、§4.5、§6.2（2 行）、§9 D12 **共 10 处**同时出现，**已全部改正**，以免文档内部出现两套口径（指挥台要求「避免同一事实出现两套口径」）。**注：指挥台函中此轮写作 v5，但 v5 已用于第三轮裁定，故记为 v6，避免两个不同变更共用同一版本号。** **▍同一轮追加（verifier attempt 2 的 F12 / F13）**：**F12（high）** —— §4.3 第 5 步的期望值「43 条」不成立：**实为「43 条路径 → 48 个 add 行」**（verifier 实测 47 = 41 显式已改动 + audit 当时 6 文件；**planner 复核 48 = 41 + audit 现 7 文件**，差额已完全解释）；`git status --porcelain` 的「期望输出为空」同为错误期望（E 类未跟踪项不受 `.gitignore` 覆盖，必然显示）；另发现 **`.gitignore` 当前干净 → 该行今天不产生 add 行**（§5 增补获批后才成第 49 行）；**校验阈值改由「计数值」改为「不得出现任何 E 类路径」**（§4.3 第 5 步 + §4.7 新增一行 + §10 步骤 7），理由是白名单外第 3 项失败才停的新口径下**错期望值会导致假停机**；§4.3 第 5 步的 `git diff --cached --name-status` 一行按指挥台措辞改为**集合断言**：「**期望 = 清单路径数 ∪ 清单目录下当时的全部文件，且零 E 类路径**」。**F13（medium）** —— `Docs/` 排除的两个连带后果在 §1.3 缺口 1 下显式登记：设计（`Docs/Scene/` 5 文件）与其生成脚本 `rebuild_v5.py` **双双在备份之外**；`scene_topdown.png`（2.85 MB > 1 MB）将来若入库即**触发规则 23**。**▍冻结令**：`audit/` **自本次勘误后即刻冻结**（§10），直到 t10 完成并报告。 **本次为 t9 最后一次改动**，t12 开工前不再改。 |

> **状态说明（诚实声明）**
>
> - **流程裁定（指挥台）= (a) 就地接受，不开修复任务**：同一交付物、同一天内的修订，且上方修订表已把 v1 的 Docs 入库判定标为作废 → 就地接受，不重开任务。
> - **已知且已接受的偏差（显式登记，勿再重开）**：**t9 的任务记录（终态 output）描述的是 v1 的内容，与本文件现状不一致** —— output 记「48 条暂存路径 + `Docs/Scene/` 入库」，本文件已是「**43 条 + `Docs/` 排除**」。**该偏差已知、已由指挥台裁定接受**；**t11 / t12 / verifier 一律以本文件为准**（正呼应 verifier 的 F-9 证据纪律）。
> - **版本绑定（F-9 纪律）**：v1 **62,720 B** / v2 **73,570 B** / v3 **78,219 B** / v4 **81,286 B**（v4 定稿 mtime 2026-09-10 22:51:39）；**v5（本轮：指挥台第三轮裁定）及以后的实测以文件当前值为准** —— 只读命令：`Get-Item <本文件路径> | Select-Object Length,LastWriteTime`。**下游引用纪律（指挥台精确化版）**：引用必须绑定 **文件名 + mtime + 字节数**；**引用前必须重新读取当前 mtime**；**对仍处于编辑中的文件，必须标注「引用时点」，并声明「字节数不是同一性凭据」** —— 并发编辑下字节数本身不是稳定量（本文写作期间观测序列：t1 43,075→48,571→56,275→57,304→59,406 B；t2 42,283→48,957 B；t5 43,230→61,954→71,277 B；本文件 v1→v6）。**只写章节号 = 引用失效。**
> - **t5 复核结果（needs_revision / failed）**：其 12 条更正**不在本文件内改写**（本文件按指挥台指示冻结），而是登记在 `.trae/execution/reports/audit/t12-inputs-t5-corrections.md`（写入时刻快照 12,943 B → 后续增补至约 16 KB；**该目录内报告仍在被改写，引用前请重新实测**），由 **t12** 承载。**本文件原有 3 类已证实错误的数字已按指挥台裁定 (i) 就地勘误**（见 v6 修订行；**实际覆盖 9 处**），**不再由 t12 出更正表**。
> - **执行闸门**：**在 t5 第 2 轮复核通过、且用户就 M01-T005 等 6 项作出裁定之前，§10 的步骤 4–12 一律不得执行**（git-operator 处于 HOLD）。

---

## 0. 结论摘要（先读这一段）

1. **本项目此前不存在任何有效完整备份。** `E:\AWorkBackup\VRSanguoYanWuchang\`（1929 文件 / 631.0 MB）只装了一个已退役插件的编译产物快照，缺 `Content/`、`Config/`、`Source/`、`.trae/`、`.git`（t3 §5.2）；`E:\AWork\Temp\VRSanguoRef\` 1.77 GB 是**活跃资产源库不是备份**（t3 §5.1）。→ **本次 Git 基线提交 + 推送 origin 将是本项目第一个完整备份。**
2. **本次基线必须用显式路径暂存，禁止 `git add -A` / `git add .`**（t3 §9.1）：否则会一次性推入 `.agent-teams/`（团队运行态 6 条、含 57 处本机绝对路径）、`.dsh-uploads/`（3 条、含 2 张用户手机截图）等 E 类内容。显式清单见 §4.3（**43 条**）。
3. **`Docs/Scene/` 5 文件本次排除**（指挥台更正裁定，撤销此前的入库裁定）：`Docs/` 不在 AGENTS.md 任何一类文件边界内，且已被治理判废、从未入库。**由此暴露一个必须让用户看到的缺口** —— 演武场场景设计与它的生成脚本**双双不在备份内**（见 §1.3 缺口 1）。
4. **两个原型关卡的删除随基线提交**（指挥台裁定 R2）。它是**已备案的用户决定**（STATUS.json M01-T005 note），不是意外丢失；两份 LFS 对象在本地对象库命中，**可完整恢复**。见 §2.2。
5. **不得清理 `Saved/`**：那里存着 `L_Prototype_1v1_v3.umap` 的**唯一存活副本**（§1.3 缺口 2）。它已被从「可再生目录」升级为**清理前置条件**（§7）。
6. **CI 门禁当前有 2 项红 —— 已知、已立案、待用户裁定，本次不清零。** 根 `.trae/execution/active/STATUS.json` 中 `M01-T005.status = "completed"` 不在合法集合内，且与登记册不一致。**但这是一个已立案的口径冲突，不是本次提交引入的问题**：verifier 查到用户既有裁定 —— `session-20260904-002.md:156`「（M01-T005 的）收口方式待其汇报后**统一处理，勿自行改**」。→ **本次基线不做任何 M01-T005 状态修改**；处置路径 = 等 `session-20260908-002` 的收口汇报 + 用户裁定。**推送后 CI 若红，只能如实写「云端 CI 红，原因=已知的 M01-T005 口径冲突，非本次提交引入」，绝不写「通过」。** 见 §4.7 与 §10。
7. **推送能不能算「备份」，取决于推送是否成功。** 本次网络实测 github.com:443 直连不可达，须走 `.trae/governance/SessionCommands.md:110` 固化的**单次借用代理**路径；Actions 若同样不可达，结论只能写「**已推送，CI 未核验**」。见 §4.7。
8. **最大的残余风险不是磁盘，是「未落盘」**：编辑器 pid 24284 仍持有若干资产写锁，本次提交只反映**磁盘现状**，推送 ≠ 已保存。见 §8。

---

## 1. 事实源声明（本项目东西以后只在哪里）

### 1.1 一句话模型

> **唯一工作目录 = `D:\AWork\Unreal\Project\VRSanguoYanWuchang`；唯一版本管理 = 该目录内的 Git 仓库（分支 `master`，origin = `https://github.com/wzf12138/sanguoVR.git`）；备份 = 推送到 origin。**
> 今后所有项目内容**只**存在于这一个工作目录里，并由这一条远程历史承载 —— 不在 `D:`、`E:` 或任何位置另建项目副本、镜像目录、bundle 存档或第二个工作目录。

### 1.2 由该模型推出的四条边界

1. **本方案不含任何本地备份副本方案**：没有 robocopy、没有 `git bundle`、没有镜像目录、没有第二个项目目录、没有 E: 备份目录。
2. **E: 的角色 = 大文件 / 低频工具 / 归档 / 素材盘**（AGENTS.md 磁盘与下载规则），**不是**备份目标。红线：**不得在 E: 上自行新建文件夹**；需要写 E: 时必须使用已有存放位置，或先问用户。同时 AGENTS.md 还写着「不保留冗余副本」→ E: 上重复的副本应去重（§6.2）。
3. **`Saved/`、`Intermediate/`、`Binaries/` 等被忽略的目录不在备份范围内**，这是**已知且接受的**；但它们并非都「可再生」—— `Saved/Autosaves/` 里存着 **v3 关卡的唯一存活副本**（§1.3 缺口 2）。**`Saved/` 因此不得清理**（§7）。
4. **清理的对象是「磁盘占用」而不是「仓库内容」**：项目内可再生目录合计 13.50 GB（不含 `Saved/` 为 **12.29 GB**），但全部需要用户批准 + 编辑器关闭后才能执行。

### 1.3 备份完整性缺口（**「推送 = 备份」覆盖不到什么** —— 必须让用户看到）

> 事实源模型是「Git + 推送」，因此**凡是没进 Git 的东西就完全不在保护范围内**。以下两个缺口由**指挥台独立实测**（非成员自述）：

**缺口 1 · 三代关卡重建脚本全在项目外，不在 git、不在任何备份**

- `rebuild_v3.py` / `rebuild_v4.py` / `rebuild_v5.py` 都在项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\`（AGENTS.md 规定「临时脚本不得进入项目」）。
- 而用户删除 v1/v2/v3 的既定决定**以「脚本在外可重生」为前提**（STATUS.json M01-T005 note 原文）。
- **→ 脚本一旦丢失，这个前提就失效：删掉的关卡再也重建不出来。**（因此本方案**不建议删除任何 `rebuild_*.py`**，见 R1 裁定与 P13。）
- 同类：`Docs/Scene/` 的**唯一来源** `rebuild_v5.py` 也在项目外 → 本次排除 `Docs/Scene/` 后，**演武场场景设计稿与生成脚本双双不在备份内**。
- **▍F13（verifier attempt 2 · medium）—— 该连带后果必须显式登记进交接清单**：
  1. 演武场**场景设计**（`Docs/Scene/` 5 文件）**不在备份内** —— 本轮 `Docs/` 排除裁定的直接后果；
  2. 生成它的 `rebuild_v5.py`（项目外 / 50,614 B）**也不在备份内** —— 缺口 1；
  3. → **「设计」与「能重建设计的东西」双双在备份之外**，是**缺口 1 与缺口 2 的同源表现**：**凡不在 git、又不在 E: 备份里的东西，都没有任何副本**；
  4. 该 `scene_topdown.png`（**2,853,240 B = 2.85 MB > 1 MB**）**将来若入库即触发规则 23**（大型非 LFS 二进制）—— 本次因排除 `Docs/` 而不触发（§4.5「本次新增 = 0」正建立在此排除之上）。

**缺口 2 · v3 关卡的唯一存活副本在一处「被忽略的目录」里**

- `Content/VRSanguo/Dev/L_Prototype_1v1_v3.umap` **从未进过 Git**，盘上已不存在；唯一存活副本 = `Saved/Autosaves/Game/VRSanguo/Dev/L_Prototype_1v1_v3_Auto6.umap`（**450,808 B，2026-09-10 14:38:14**，本方案已只读复核存在）。
- 旁证：`Saved/Logs/VRSanguoYanWuchang.log` 有 `[2026.09.09-15.33.17][248]Cmd: MAP LOAD FILE=".../Content/VRSanguo/Dev/L_Prototype_1v1_v3.umap"` → 证明 v3 确曾存在于该路径（指挥台实测）。
- 而 `Saved/` 被 `.gitignore` 覆盖 → **不在备份内**。
- 本方案只读复核补充：同一目录下另有 `L_Prototype_1v1_v3_Auto1.umap`（417,379 B，09-08 23:59）、`Auto2.umap`（418,414 B，09-09 00:09），以及**已删关卡 v2 的 4 份自动存档**（`v2_Auto1–Auto4`，370,689–371,056 B，2026-08-25）、v5 的 `Auto0–Auto9` 10 份、`L_SkeletonTest_Auto1–Auto5`。
- **⚠ 由此得出一条必须交用户的警告：不得清理 `Saved/`。** 删除它会**连带销毁 v3 的最后一份副本**（同时也销毁 v2 的 4 份自动存档与全部 v5 验收证据）。

**缺口的处置口径**：本方案**不在本轮移动任何证据或参考图、不新建任何 E: 目录**（指挥台 R6 + 硬约束）。是否把 v3 唯一下载副本「转正」为受版本管理的资产，列为 **D28**，由用户裁定。

---

## 2. 处置总表

判定传承自 t1/t2/t3；本方案按指挥台裁定对三处口径做了调整（§11 登记差异）。
「处置动作」取值：**保留** / **出库并忽略** / **排除（本次不入库）** / **删除** / **留待用户裁定** / **提交（入库）**。

### 2.1 应入库内容（本次基线提交的对象）

| 对象 | 分类 | 处置动作 | 可逆性 | 风险 | 依据 |
|---|---|---|---|---|---|
| `.trae/**` 治理正文改动（26 项已跟踪修改中的 15 项 .trae 文件） | C | 提交（入库） | 可逆 | 低 | t1 §3.1；指挥台入库判据 R3 |
| `Config/DefaultEngine.ini`、`Config/DefaultGame.ini` | C | 提交（入库） | 可逆 | 低 | t1 §3.1 |
| `Content/VRSanguo/Dev/L_SkeletonTest.umap` | C | 提交（入库） | 可逆 | 低 | t3 C10 |
| `Content/VRSanguo/VR/BP_VRCharacter.uasset` | C | 提交（入库） | 可逆 | 中 | t1 §3.1（LFS 指针变更；见 §8） |
| `Content/VRSanguo/VR/Mesh/环首刀.uasset`（28,041,121 B，LFS） | C | 提交（入库） | 可逆 | 低 | t1 §5.3（工作区 SHA256 已在本地 LFS store 命中） |
| `Content/VRTemplate/Input/IMC_Weapon_Left.uasset`、`IMC_Weapon_Right.uasset` | C | 提交（入库） | 可逆 | 中 | t1 §3.1（见 §8） |
| `Source/VRSanguoYanWuchang/Private/Combat/VRSanguoGripLibrary.cpp` | C | 提交（入库） | 可逆 | 低 | t1 §3.1（最新改动 22:31:52） |
| `Plugins/PICOOpen174f9f81d266V8/Source/**` 3 个源码改动 | D（流程归属待裁） | 提交（入库，防丢失） | 可逆 | 中 | t1 §3.1/§9.2；R3 判据（项目的一部分、不能由一条命令重建） |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap`（673,326 B） | C | 提交（入库） | 可逆 | 低 | t3 §1.2（唯一活跃关卡；rebuild_v5.py:7/597） |
| `Content/VRSanguo/Dev/M_GrayBox_Red.uasset`、`M_GrayBox_Straw.uasset` | C | 提交（入库） | 可逆 | 中 | t3 §1.4（v5 运行期依赖；**不提交则 v5 引用断裂**） |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap`（509,749 B） | A/D | 提交（入库，保留回滚基线） | 可逆 | 低 | t3 R1（去留待用户裁定，但**先入库以免丢失**） |
| `.trae/execution/CR-*.md` ×4（0501/0701/0801/0901） | C | 提交（入库） | 可逆 | 低 | t1 §3.2；指挥台 R3 明示必须入库 |
| `.trae/execution/sessions/session-*.md` ×4（0904-002 / 0906-001 / 0908-001 / 0908-002） | C | 提交（入库） | 可逆 | 低 | t1 §3.2；指挥台 R3 明示必须入库 |
| `.trae/execution/arena-gameplay-decisions.md` | C | 提交（入库） | 可逆 | 低 | t1 §3.2；指挥台 R3 明示必须入库 |
| `.trae/execution/reports/audit/`（本队报告，含本方案） | C | 提交（入库） | 可逆 | 低 | t1 §3.0 第45行；AGENTS.md 规则20(b) |
| `.gitignore`（追加 2 行） | — | 提交（入库） | 可逆 | 低 | 指挥台 R1 + R7 |

> **本次基线不含 `Docs/`**（指挥台更正裁定，见 §2.3 与 §4.4）。

### 2.2 记录删除（随基线提交）

| 对象 | 分类 | 处置动作 | 可逆性 | 风险 | 依据 |
|---|---|---|---|---|---|
| `Content/VRSanguo/Dev/L_Prototype_1v1.umap`（git 记为 ` D`） | A（已裁定） | 提交该删除 | **可恢复** | 低 | 指挥台 R2；t3 §1.1（用户决定，非意外丢失） |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap`（git 记为 ` D`） | A（已裁定） | 提交该删除 | **可恢复** | 低 | 同上 |

**恢复方式（产品语言 + 证据）**

- 一句话：**「删除」只是从工作区消失，不是从历史消失。**
- 两份 LFS 对象在本地对象库中命中（指挥台实测）：`L_Prototype_1v1.umap` sha256 `3fc44947bede3f4e55820280b08ee059478327661f068eeaef835bce8f6a2fb5` / 67,215 B；`L_Prototype_1v1_v2.umap` sha256 `a825dd7a5adcf4682b0a7b2a06579a35c85fe5396baef6e5ba24205ec89aff0a` / 246,266 B。
- 恢复操作（**不由本方案执行**，仅登记给未来的自己）：从本次基线提交的父提交取出该路径 —— `git restore --source=<基线提交>~1 -- <路径>`（或 `git checkout <父提交> -- <路径>`）。对象已在本地 store，**恢复不依赖网络**。
- 旁证：两份关卡在 HEAD 中是 LFS 指针 blob（130 / 131 B，t1 §3.1；t3 §1.1）。
- 补充（v2 的另一重冗余，本方案只读复核）：`Saved/Autosaves/…/L_Prototype_1v1_v2_Auto1–Auto4.umap` 4 份（2026-08-25）亦存在 —— 同样在 `Saved/` 内、同样不在备份内（§1.3）。

### 2.3 不应入库（E 类）与本次排除

| 对象 | 分类 | 处置动作 | 可逆性 | 风险 | 依据 |
|---|---|---|---|---|---|
| `Docs/Scene/` 5 文件（`asset_checklist.md`、`scene_modules.json`、`scene_overview.md`、`scene_plan.html`、`scene_topdown.png` 2,853,240 B） | E/D（**更正**） | **排除（本次不入库）** + 留待用户裁定归属 | 可逆 | 中 | 指挥台更正裁定：`.trae/archive/README.md` 判废 `Docs`；CHANGELOG L894/L897 记「删除 Docs…后续不再使用」；`git log --all -- Docs` 为空；**AGENTS.md 文件边界只承认 `Config/Content/Plugins/Source` 与 `.trae/`，`Docs/` 不在任何一类**。缺口见 §1.3 缺口 1 |
| `Docs/` 目录本体 | A（张力） | 保留（不删） | 可逆 | 低 | t2 §7.1 + 更正裁定 |
| `.agent-teams/vrsanguo-audit-backup/`（团队运行态 6 条，随通信持续增长） | E | 出库并忽略（**不**暂存） | 可逆 | 低 | t2 §7.2；含 57 处本机绝对路径 |
| `.dsh-uploads/session-2a22b421-…/`（3 条 / 3,105,958 B，含 2 张 `com.limelight.root` 手机截图） | E | 出库并忽略（**不**暂存） | 可逆 | 低 | t2 §7.3 |
| `.agent-teams/archive/vrsanguo-survey/**` + `.agent-teams/retired-members.json`（**已跟踪** 4 条 / 41,039 B） | B/E | 留待用户裁定（`git rm --cached`，P1） | 可逆 | 低 | t1 §4.3；指挥台 R1/R7 |
| 项目内 4 个空目录：`active/M00/`、`active/M01-T002/`、`active/M01-T006/`、`execution/requests/` | A | 留待用户裁定（登记后移除） | 不可逆（空目录） | 低 | t2 §2.2/§2.3（生成器会复发；CI 不可见） |
| `gcm-diagnose.log`（8,258 B，项目根，已被 `*.log` 忽略） | 噪音 | 保留（已被忽略）；可选删除需批准（P5） | 可逆 | 低 | t1 §8.1 |

### 2.4 仓库健康与存储方式

| 对象 | 分类 | 处置动作 | 可逆性 | 风险 | 依据 |
|---|---|---|---|---|---|
| `.git/lfs/objects/`（496 文件 / 723,507,226 B = 690 MB） | 不可替代 | **保留，不得清理** | 不可逆（会丢内容） | **高（若误删）** | t1 §6（推送成功前是唯一实体来源） |
| `.git/objects/` 可回收垃圾 = 0 | — | 不动作（`git gc` 收益 ~245 KB，不值得） | — | 低 | t1 §6 |
| **全仓 48 个受索引图片以普通 blob 入库**（**49,760,737 B = 47.46 MiB**，历史遗留；≥1 MB 者 18 个 / 44.19 MiB） | C（内容）/存储方式问题 | **本次不做任何处置**（R5 三选项待用户裁定，§5.2） | 不可逆（若不重写历史） | 中 | **planner 独立复测（F-3）**；指挥台 R5 |
| `.gitattributes` 缺 `*.png/*.jpg` | 缺口 | 本次**不做规则变更**；登记待用户裁定（R5/P14） | 可逆 | 中 | 指挥台 R5 |
| 陈旧本地引用 `refs/remotes/origin/HEAD` → `origin/main` | D | 留待用户裁定（可选本地清理，**需明确授权**） | 可逆 | 低 | §4.7；指挥台 R4 撤回 |
| 远程并列分支 `origin/main`(e5c8a9ae)、`origin/gh-pages`(242f0d5e) | D | **本次不改动，仅登记** | — | 低 | §4.7 |

### 2.5 治理一致性

| 对象 | 分类 | 处置动作 | 可逆性 | 风险 | 依据 |
|---|---|---|---|---|---|
| 根 `STATUS.json` 中 `M01-T005.status = "completed"`（体检 2 项红） | 非法值 + 交叉引用不一致 | **本次不修改**（登记为「已知 / 已立案 / 待用户裁定」，不清零）；等 `session-20260908-002` 收口汇报 + 用户裁定 | 可逆 | 中（已降级：非本次引入） | 指挥台紧急撤销令 + verifier 复现 + `session-20260904-002.md:156`「勿自行改」；t2 §3.2 |
| （**分层说明**）体检的「2 项红」 vs `M01-T005` 的「5 处副本漂移」 | **两个不同层次的问题，不得混为一谈** | — | — | — | verifier 实测：体检脚本的两项红**只读根 `STATUS.json`**，不读 `integrity.yaml` / `manifest.yaml` / 任务包副本 → 「2 项红」= 本次白名单内的门禁失败；「5 处副本漂移」= 治理数据一致性问题（t2 K1，另立处置） |
| v5 关卡只读锁丢失（声明只读 vs 实测 `RO=False`、21:44:17 重写） | 治理漂移 | 登记 + **给 t10 加 SHA256 前后守卫**（R2，§8） | — | 中 | 指挥台 R2；t3 §1.3 |
| `Build/Patches/PICOOpenXR/`（187 受管文件，181/184 与插件源码逐字节相同） | B/D | 保留（补丁基线载体），去留留待用户裁定 | 可逆 | 中 | t1 §2.1/§9.2 |
| M01-T005 的 v3 关卡口径（记录存在、产物不存在） | A | 留待用户裁定（**单独立项**做记录回收） | — | 中 | t2 K2/§4.1；缺口 2 见 §1.3 |
| 6 个被引用但不存在的会话记录（16 处引用） | A | 留待用户裁定（建议加 `sessions/MISSING.md`，P4） | 可逆 | 低 | t2 §5.2 |
| `.trae/index.md` 漏 `M02-PREP-002` 任务包链接 | A | 留待用户裁定（1 行补链，P3） | 可逆 | 低 | t2 §9.1 |

### 2.6 工作目录之外（只登记，团队不得动手 —— 全部需用户批准）

| 对象 | 分类 | 处置动作 | 可逆性 | 风险 | 依据 |
|---|---|---|---|---|---|
| `E:\AWorkBackup\VRSanguoYanWuchang\`（1929 文件 / 631.0 MB） | A | 留待用户裁定（退场/删除，P7）—— **已作为第 6 项呈用户；团队不得动手删** | 不可逆 | 中 | t3 §5.2；§6.1 |
| `E:\AWork\Temp\VRExpansionPlugin\`（毛额 **2,947.3 MB**，**含重复计数 1,020.6 MB** → 净可回收 **1,926.7 MB**） | B | 留待用户裁定（去重保留 1 份，P8） | 不可逆 | 中 | **planner 独立复测（F-4）**；t3 §6.1；§6.2 |
| `E:\AWork\Tools\OpenBRF\openbrf.zip`（**11.34 MB** = 11,890,974 B） | B | 留待用户裁定（去重，P9） | 不可逆 | 低 | **planner 独立复测（F-8）**；t3 §5.3 原记 39 MB 系**高估 3.4 倍** |
| `E:\AWork\Temp\vrsanguo_pie_t0.png`、`vrsanguo_sword_view5.png`、`VRSanguoRef\OBJ\`（空） | A | 留待用户裁定（退场，P10） | 不可逆 | 低 | t3 §5.3 |
| `D:\AWork\TraeAdmin\…` A×11 一次性产物 + `tmp\` 13 文件 | A | 留待用户裁定（清理，P11；**不含任何 `rebuild_*.py`**） | 不可逆 | 中 | t3 §4；§6.3 |
| `D:\AWork\TraeAdmin\…\tmp\STATUS.json.broken-20260910`、`tmp\scene_topdown_raw.png` | D | 留待用户裁定（留档 / 设计内中间产物） | 不可逆 | 低 | t3 §4；§6.3 |
| `E:\AWork\Temp\VRSanguoRef\`（1.77 GB）、`E:\AWork\VRExpansionPlugin\`、`E:\AWork\Tools\venv_asset\` | C | **保留**（位置正确） | — | 低 | t3 §5.1/§5.3 |
| `D:\AWork\TraeAdmin\…\rebuild_v5.py`、`flip_topdown.ps1`、`Set-TraeGovernanceAcl.ps1`、`Unlock-TraeAssets.ps1` | C | **保留**（活跃工具链） | — | 低 | t3 §4；§6.3 |
| `D:\AWork\TraeAdmin\…\rebuild_v3.py`、`rebuild_v4.py` | C（能力前提） | **保留；本方案不建议删除任何 `rebuild_*.py`** | — | 中 | 指挥台 R1 + §1.3 缺口 1 |

---

## 3. 需用户逐项批准清单（不可逆或改变仓库语义的动作 · 一条一句话影响说明）

> **团队在本轮一个都不执行**；每条一句话说明「对项目意味着什么」（产品语言）。

| # | 动作 | 一句话影响说明 | 可逆性 | 风险 |
|---|---|---|---|---|
| P1 | 对 `.agent-teams/` 下 **4 个已跟踪文件**执行 `git rm --cached`（**独立动作，不进本次基线**） | 仓库不再「认领」这 4 个旧的 AI 团队记录文件（**你磁盘上的文件一个都不会少，历史也一个字都不会丢**），只是以后不再跟着项目一起走。**指挥台已采纳本方案的精确化：不执行此动作也能达成干净基线，故它独立于基线、需用户明确批准。** | 可逆 | 低 |
| P2 | 删除 4 个空的任务目录（`active/M00/`、`active/M01-T002/`、`active/M01-T006/`、`execution/requests/`） | 清掉 4 个**里面什么都没有**的空壳文件夹；注意生成器历史上已重建过至少两次，可能再次出现。 | 不可逆（空目录） | 低 |
| P3 | 在 `.trae/index.md` 补 1 行 `M02-PREP-002` 链接 | 让项目目录页能点到一个**已经存在但它没列**的任务包，属于补漏，不改任何结论。 | 可逆 | 低 |
| P4 | 新增 `.trae/execution/sessions/MISSING.md` 显式登记 6 个缺失会话记录 | 把「引用了但找不到的 6 份会话记录」从**隐性断链**变成**写在明面上的已知缺失**。 | 可逆 | 低 |
| P5 | 删除项目根 `gcm-diagnose.log`（8,258 B） | 清掉一个 Git 凭据管理工具自动留下的诊断日志；它已被忽略、本来也不会进仓库。 | 可逆 | 低 |
| P6 | 清理项目内可再生目录（`Intermediate/`、`.vs/`、`Binaries/`、`ArchivedBuilds/`、`DerivedDataCache/`；**`Saved/` 见 P6a**） | 腾出 **12.29 GB** 磁盘；代价是下次打开要**重新编译 + 重新生成缓存**（会明显更慢）。**必须在编辑器关闭后才能做。** | 不可逆 | 中 |
| P6a | 清理 `Saved/`（1.12 GB）—— **前置条件未满足前禁止执行** | ⚠ 删它会**销毁 `L_Prototype_1v1_v3.umap` 的最后一份副本**（以及 v2 的 4 份自动存档、全部 v5 验收证据）。**必须先做完 D28 的裁定**（v3 副本是否转正），否则这 1.12 GB 不能碰。 | 不可逆 | **高** |
| P7 | 删除 `E:\AWorkBackup\VRSanguoYanWuchang\`（631.0 MB） | 清掉一个**名字像备份、其实不是备份**的旧目录；它是已退役旧桥插件的编译产物，与 2026-09-03「彻底删除、不保留回退」的决定一致，回退路径是重新下载上游源码再打补丁。 | 不可逆 | 中 |
| P8 | 对 `E:\AWork\Temp\VRExpansionPlugin\` 三份副本去重（保留 1 份） | 回收 **1,926.7 MB（≈1.88 GB）**：毛额 2,947.3 MB 里 **1,020.6 MB 是同一份解压目录的两份副本**（`Extracted\` 与 `VRExpPluginExample-5.6\` 字节完全一致，属**重复计数，必须扣除**）；实际可回收 = 一份重复目录 1,020.6 MB + 压缩包 906 MB。 | 不可逆 | 中 |
| P9 | 删除 `E:\AWork\Tools\OpenBRF\openbrf.zip`（**11.34 MB**） | 回收 **11.34 MB**：工具已经解压好了，压缩包是多余的副本。（实测 11,890,974 B；t3 原记 39 MB 系高估 3.4 倍） | 不可逆 | 低 |
| P10 | 删除 `E:\AWork\Temp\` 下 2 张一次性抓图与 `VRSanguoRef\OBJ\` 空目录 | 清掉早期调试留下的两张截图和一个空目录，不影响任何正式素材。 | 不可逆 | 低 |
| P11 | 清理 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\` 的 11 个一次性脚本与 `tmp\` 验证输出 | 清掉一次事故修复过程留下的临时脚本与输出；**保留事故证据原件**、**保留全部 `rebuild_*.py`**（本方案不建议删除任何重建脚本）。 | 不可逆 | 中 |
| P12 | `Saved/Evidence/` 里当前代次的验收截图（v5/v56/v56b/v57 共 9 张 / 10.6 MB）**是否转正进 Git** | 现在这些「关卡验收证据」被 Git 忽略，**换台机器就没了**；但**本轮不得移动任何证据文件** —— 移动会打断 M01-T005 的证据链（`check-integrity.py` 的「验证证据文件路径存在」当前 PASS）。要与不要，由你定。 | 可逆 | 中 |
| P13 | `L_Prototype_1v1_v4.umap` 的去留（仅此一项） | 删掉它=失去回退到上一版关卡的能力。**注意：本方案不建议删除任何 `rebuild_*.py`** —— 那些脚本正是「删旧关卡没关系」这句话的前提。 | 不可逆 | 中 |
| P14 | 给 `.gitattributes` 增加 PNG 图片的 LFS 规则 | 本次**不做**（属范围变更）。若将来要做，须区分「限定路径」与「全局 `*.png`」两种写法的不同影响（§5.2）。 | 可逆 | 中 |
| P15 | **全仓 48 个受索引图片（49,760,737 B = 47.46 MiB）**的历史迁移（`git lfs migrate`） | 能一次性把仓库瘦身，但**必须重写历史并强制推送**，与本次「禁止 `push --force`」直接冲突 → 本次不考虑，需另立任务、单独放行。 | 不可逆 | 高 |
| P16 | 修改 `ExecutionModel.md:124`（把「临时文件写 C 盘用户目录」改成项目外临时目录） | 治理文本里有一条**自相矛盾**的规定：一处禁止写 C 盘，另一处却写着临时文件放 C 盘用户目录；这是正文修改，需走变更申请。 | 可逆 | 中 |
| P17 | **R5 备选 (c)**：把 `Content/VRSanguo/Art/References/` 的参考图移出 Git，归档到 E:（推荐项） | **推荐做法**：这些是**给人看的参考图、不是游戏运行时资产**；移到 E: 归档区后，仓库里最大的一类「非 LFS 大文件」直接消失，规则23 风险清零。**但这是内容搬迁，须你批准，且本轮不做。** | 不可逆（搬迁） | 中 |
| P18 | `Docs/Scene/` 的最终归属（本次已排除） | 本次排除后，**演武场场景设计稿与生成它的脚本双双不在备份里**（§1.3 缺口 1）。要不要给它们一个家（进 Git / 移到 E: 归档 / 明确接受丢失），需要你裁。 | 可逆 | 中 |
| P19 | CR 候选：把 `SessionCommands.md:90` 的 `git add -A` 改为「优先使用显式路径」 | 治理正文里的标准推送流程写的是「一把梭全加」，而本项目的 `.gitignore` 有反否定陷阱（`.trae/**` 等会让 `*.log`/`*.tmp` 静默变成可入库）→ 建议改成「优先显式路径」。**是否开 CR 由你决定**，本轮只登记。 | 可逆 | 低 |
| ~~P20~~ | ~~为本轮审计各任务认领补建会话记录~~ | **已裁定：不适用、不补建** —— 本轮是 DSH AgentTeams 任务，不构成 `.trae` 任务认领（无 `MNN-TNNN`、无 `claimedBy`），**不触发规则26**（详见 D32）。**保留此行仅为留痕，不要执行。** | — | — |

---

## 4. Git 基线构成

### 4.1 提交前状态（本次实测钉住）

| 指标 | 实测值 | 命令 |
|---|---|---|
| `HEAD` | `eb319c3689458d7b1a61d1798adfc5ea8df0c494` | `git rev-parse HEAD` |
| `origin/master` | 同上（**完全一致**） | `git rev-parse origin/master` |
| 未推送提交 | 0（t1 §7） | `git log --oneline origin/master..HEAD` |
| 脏项 `git status --porcelain -uall` | **59 行** = 已跟踪修改 26 + 记录删除 2 + 未跟踪 31 | 见下 |
| 暂存区 | 空 | `git status --porcelain` 无 `M ` 行 |

> **⚠ 集合由「路径清单」定义，不由计数定义**（指挥台 Q2 硬要求）。计数只作**证据与对账**，因为团队每写一份报告它就变（43 → 54 → 58 → **59**，本节实测时刻 = 2026-09-10 本方案 v2 写盘时）。t10 执行时请重新跑一次 `git status --porcelain -uall` 并**逐条比对路径**，不要拿 59 当断言。

59 行构成（实测）：

- ` M` 26 项：`.trae` 15 + `Config` 2 + `Content` 5 + `Plugins/PICO…/Source` 3 + `Source` 1
- ` D` 2 项：`Content/VRSanguo/Dev/L_Prototype_1v1.umap`、`…_v2.umap`
- `??` 31 项：`.agent-teams/…` 6 + `.dsh-uploads/…` 3 + `CR-*` 4 + `arena-gameplay-decisions.md` 1 + `reports/audit/` 4 + `sessions/` 4 + `Content/VRSanguo/Dev/` 4 + **`Docs/Scene/` 5（本次排除）**

**对账口径（可复算）**：59 − 排除类 9（`.agent-teams` 6 + `.dsh-uploads` 3）− `Docs/Scene/` 5 = 45；把 `reports/audit/` 的 4 个文件折叠为 1 条目录路径（45 − 4 + 1 = 42）；再加将被修改并暂存的 `.gitignore` = **43** —— 与 §4.3 清单条目数一致。

### 4.2 包含路径集（逐条）

**A. 已跟踪修改（26 条，全部包含）**

```
.trae/CHANGELOG.md
.trae/execution/active/M01-T001/ALLOWLIST.txt
.trae/execution/active/M01-T001/STATUS.json
.trae/execution/active/M01-T005/STATUS.json
.trae/execution/active/STATUS.json
.trae/execution/reports/tasks/M01-T001.md
.trae/execution/reports/tasks/M01-T005.md
.trae/execution/sessions/session-20260830-001.md
.trae/execution/task-template-level.md
.trae/execution/task-template.md
.trae/governance/ExecutionModel.md
.trae/governance/ReviewProtocol.md
.trae/knowledge/TechnicalDecisions.md
.trae/registers/11-tech-debt-register.md
.trae/systems/02-interaction-and-weapon-system.md
Config/DefaultEngine.ini
Config/DefaultGame.ini
Content/VRSanguo/Dev/L_SkeletonTest.umap
Content/VRSanguo/VR/BP_VRCharacter.uasset
Content/VRSanguo/VR/Mesh/环首刀.uasset
Content/VRTemplate/Input/IMC_Weapon_Left.uasset
Content/VRTemplate/Input/IMC_Weapon_Right.uasset
Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp
Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.cpp
Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.h
Source/VRSanguoYanWuchang/Private/Combat/VRSanguoGripLibrary.cpp
```

**B. 记录删除（2 条，包含 —— 指挥台 R2）**

```
Content/VRSanguo/Dev/L_Prototype_1v1.umap
Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap
```

> 已从磁盘删除；`git add -- <路径>`（Git ≥2.0）会记录删除，等价写法 `git rm -- <路径>`。**不要**改成「恢复文件」。

**C. 未跟踪新增 + 新增忽略规则（14 条路径 + `.gitignore`，包含）**

```
.gitignore
.trae/execution/CR-20260905-001-pico-battery-gating.md
.trae/execution/CR-20260907-001-imc-pico4-keys.md
.trae/execution/CR-20260908-001-steamvr-retro-unlock.md
.trae/execution/CR-20260909-001-grip-contract-fix.md
.trae/execution/arena-gameplay-decisions.md
.trae/execution/sessions/session-20260904-002.md
.trae/execution/sessions/session-20260906-001.md
.trae/execution/sessions/session-20260908-001.md
.trae/execution/sessions/session-20260908-002.md
.trae/execution/reports/audit/            # 目录：t1/t2/t3(/t5/t11) 报告 + 本方案
Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap
Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap
Content/VRSanguo/Dev/M_GrayBox_Red.uasset
Content/VRSanguo/Dev/M_GrayBox_Straw.uasset
```

合计 **43 条暂存路径** = 26（已跟踪修改）+ 2（记录删除）+ 14（未跟踪新增路径）+ 1（`.gitignore`）。
> **注意（F12）**：「43」是**路径条数**；`git add` 会把目录路径**递归展开**（`reports/audit/` 1 条 → 6 个文件）→ 实际 add **47 个文件**。**集合由路径清单定义，计数只作对账。**
**`Docs/Scene/` 5 条已从清单中移除**（指挥台更正裁定）。

### 4.3 t10 应使用的显式暂存路径清单（**禁止 `git add -A` / `git add .` / `git add -u`**）

```powershell
# 0) 提交前基线（实测并记录；并先做 v5 SHA256 守卫，见 §8）
git status --porcelain -uall

# 1) 先落 .gitignore 的两行增补（见 §5.1），再暂存它本身
git add -- .gitignore

# 2) 已跟踪修改（26 条）
git add -- `
  .trae/CHANGELOG.md `
  .trae/execution/active/M01-T001/ALLOWLIST.txt `
  .trae/execution/active/M01-T001/STATUS.json `
  .trae/execution/active/M01-T005/STATUS.json `
  .trae/execution/active/STATUS.json `
  .trae/execution/reports/tasks/M01-T001.md `
  .trae/execution/reports/tasks/M01-T005.md `
  .trae/execution/sessions/session-20260830-001.md `
  .trae/execution/task-template-level.md `
  .trae/execution/task-template.md `
  .trae/governance/ExecutionModel.md `
  .trae/governance/ReviewProtocol.md `
  .trae/knowledge/TechnicalDecisions.md `
  .trae/registers/11-tech-debt-register.md `
  .trae/systems/02-interaction-and-weapon-system.md `
  Config/DefaultEngine.ini `
  Config/DefaultGame.ini `
  Content/VRSanguo/Dev/L_SkeletonTest.umap `
  Content/VRSanguo/VR/BP_VRCharacter.uasset `
  Content/VRSanguo/VR/Mesh/环首刀.uasset `
  Content/VRTemplate/Input/IMC_Weapon_Left.uasset `
  Content/VRTemplate/Input/IMC_Weapon_Right.uasset `
  Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp `
  Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.cpp `
  Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.h `
  Source/VRSanguoYanWuchang/Private/Combat/VRSanguoGripLibrary.cpp

# 3) 记录两个关卡的删除（R2）
git add -- Content/VRSanguo/Dev/L_Prototype_1v1.umap Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap

# 4) 未跟踪新增（14 条路径）
git add -- `
  .trae/execution/CR-20260905-001-pico-battery-gating.md `
  .trae/execution/CR-20260907-001-imc-pico4-keys.md `
  .trae/execution/CR-20260908-001-steamvr-retro-unlock.md `
  .trae/execution/CR-20260909-001-grip-contract-fix.md `
  .trae/execution/arena-gameplay-decisions.md `
  .trae/execution/sessions/session-20260904-002.md `
  .trae/execution/sessions/session-20260906-001.md `
  .trae/execution/sessions/session-20260908-001.md `
  .trae/execution/sessions/session-20260908-002.md `
  .trae/execution/reports/audit/ `
  Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap `
  Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap `
  Content/VRSanguo/Dev/M_GrayBox_Red.uasset `
  Content/VRSanguo/Dev/M_GrayBox_Straw.uasset

# 5) 暂存后核对（**硬判据 = 不得出现任何 E 类路径，不是计数**）
git status --porcelain              # 期望：**仅出现 E 类未跟踪项**（.agent-teams/、.dsh-uploads/、Docs/）→ **判据不是「输出为空」**（这三类不在 .gitignore 内，必然显示为 ??）
git add --dry-run -- <上面的 43 条路径>   # 零副作用复核（不写索引）：**现场复算 add 行数**
git diff --cached --name-status     # 期望：暂存集合 == 清单 43 条路径 ∪ 清单内目录在暂存时刻的全部文件；且不得出现任何 E 类路径
git diff --cached --stat | Select-Object -Last 1
```

**暂存后必须看不到的四类路径（▍这就是本次的唯一硬判据 —— 不是条数）**（出现即说明用错了命令）：

```
.agent-teams/        （团队运行态，E）
.dsh-uploads/        （用户上传的手机截图，E）
Docs/                （本次已排除 —— 指挥台更正裁定）
Intermediate/ Binaries/ Saved/ .vs/ DerivedDataCache/ ArchivedBuilds/   （UE 生成目录）
```

> **▍F12（verifier attempt 2 · high）—— 期望值「43 条」不成立；planner 已独立复算，与 verifier 的 47 完全对上**
> `reports/audit/` 在清单里是**1 条目录路径**，但 `git add` 会**递归展开**。**完整算式（只读复算；`git add --dry-run` 由 verifier 执行，planner 未执行写入型命令）**：
> - 43 条路径 = **42 条显式路径 + 1 条目录路径**；
> - 42 条显式中 **41 条已有改动**（26 M + 2 D + 13 未跟踪）+ **1 条无改动**（`.gitignore`，已跟踪且当前干净）；
> - 目录路径展开 = `reports/audit/` 内文件数（**当前 7 个**）；
> - **→ 当前预测 add 行数 = 41 + 7 = 48**；**verifier 实测 47 = 41 + 6** —— 差额恰为 audit 目录**当时 6 文件、现 7 文件**（t12 输入登记件于本轮加入）。**两边完全对上，不是矛盾。**
>
> **由此得出三条不可回避的结论**：
> 1. **这是计数错、不是集合错** —— verifier 已实测路径集合本身正确，dry-run **零 E 类泄漏**（`.agent-teams` / `.dsh-uploads` / `Docs` / `Saved` / `Intermediate` / `Binaries` 全 0 命中）；
> 2. **`.gitignore` 那一行今天根本不会产生 add 行**（它当前未被修改，已跟踪且干净）；只有 §5 增补获批准并写入后才会变成第 **49** 行 —— 即**这个计数还挂在一个尚未裁定的决定上**；
> 3. **→ 校验阈值由「计数值」改为「不得出现任何 E 类路径」。** 理由：在白名单外第 3 项失败才停的新口径下，**一个错的期望值可能直接触发 t10 假停机**。同理，`git status --porcelain` 在暂存后**不会为空**（E 类未跟踪项不受 `.gitignore` 覆盖），原先写的「期望输出为空」是同类错误，已一并改正。

### 4.4 排除路径集及理由（逐条）

| 排除对象 | 理由 | 依据 |
|---|---|---|
| **`Docs/`（含 `Docs/Scene/` 5 文件）** | ① AGENTS.md 文件边界只承认 `Config/Content/Plugins/Source` 与 `.trae/`，**`Docs/` 不在任何一类**；② `.trae/archive/README.md` 判废 `Docs`；③ CHANGELOG L894/L897 记「删除 Docs…后续不再使用」；④ `git log --all -- Docs` 为空（**从未入库**） | 指挥台更正裁定；t2 §7.1 |
| `.agent-teams/`（当前 6 条未跟踪） | DSH 团队运行态；含 57 处本机绝对路径；每次通信都变 → 提交无意义且制造噪音 | t2 §7.2 |
| `.dsh-uploads/`（3 条） | 会话上传中转；含 2 张用户手机截图（隐私） | t2 §7.3 |
| `.git/lfs/objects/`、`.git/` 内部 | 非工作区文件 | — |
| `Intermediate/`、`Binaries/`、`Saved/`、`.vs/`、`DerivedDataCache/`、`ArchivedBuilds/`、`.workbuddy/` | UE 生成目录 / 本机状态，已被 `.gitignore` 正确忽略（**注意 `Saved/` 内有 v3 唯一副本，见 §1.3**） | t1 §2.1；t2 §7.5/§7.6 |
| `dashboard/status.json`、`integrity.json`、`index.html`、`__pycache__/` | 生成物，由 GitHub Actions 在推送时重生成 | t2 §7.4；t3 §7.2 |
| `Plugins/**/Binaries/`、`Plugins/**/Intermediate/`、`Plugins/**/*.pdb`、`Content/**/*_BuiltData.uasset` | 已由后端规则忽略 | `.gitignore:79-86` |
| `gcm-diagnose.log` | 已被 `*.log` 忽略 | t1 §8.1 |
| `E:` 与 `D:\AWork\TraeAdmin\` 全部内容 | 项目外；团队不得动手 | AGENTS.md 文件边界（**含 `rebuild_*.py`：它们是删除旧关卡决定的前提，见 §1.3 缺口 1**） |

### 4.5 规则23 自查（禁止提交密钥 / 本机路径凭据 / UE 生成目录 / 大型非 LFS 二进制）

| 检查项 | 结论 | 依据 / 待办 |
|---|---|---|
| **密钥** | **通过（依据为静态复算，非脚本运行）** | t2 §8 对 14 个待提交文本文件扫 `sk-`/`ghp_`/`AKIA`/私钥块 → 0 命中。本次新增文本（4 份 CR + 4 份会话 + arena + 审计报告 + `.gitignore`）**建议 t10 提交前用同一正则复扫** |
| **本机路径凭据** | **需裁定适用范围（D20）** | `.agent-teams/`（57 处绝对路径）已排除 ✓；但入库文本普遍含本机绝对路径（STATUS.json note、会话记录等），仓库既有惯例如此 → 该词的适用范围需用户裁定 |
| **UE 生成目录** | **通过** | `Intermediate/Binaries/Saved/.vs/DDC/ArchivedBuilds` 全部已忽略；`Build/Android/` 6 文件受管属惯例可接受（t1 §4.2 第 8 条） |
| **大型非 LFS 二进制** | **本次新增 = 0** | 43 条中 ≥1 MB 的非 LFS 文件**为 0** —— 唯一候选项 `Docs/Scene/scene_topdown.png`（2,853,240 B）已随 `Docs/` 一并排除。历史遗留 **全仓 48 个受索引图片 = 49,760,737 B（47.46 MiB）**，其中 ≥1 MB 者 **18 个 / 46,337,015 B（44.19 MiB）**（F-3：planner 独立复测，2026-09-10）本次**不做任何处置**（R5 待裁）。>5 MB 的非 LFS 受管文件 = 0（t1 §5.2） |
| **隐私** | **通过** | 含个人设备画面的 `.dsh-uploads/`（2 张手机截图）已排除 |

### 4.6 与治理正文的偏离留痕（指挥台 Q1 确认口径）

- `.trae/governance/SessionCommands.md:90` 的标准推送流程写的是 **`git add -A`**；本次按指挥台硬要求改用**显式路径清单**（§4.3）。→ **不改治理正文**，只在 t9 §4 与 t12 写明**偏离与理由**。
- 偏离理由（scout-repo 实测的 `.gitignore` 反否定陷阱）：`!.trae/**`、`!Config/**`、`!Source/**`（以及 `!Content/**`、`!Plugins/**`）**会反向取消上级忽略规则**，使这些目录里的 `*.log` / `*.tmp` / `*.bak` / `*.user` / `*.sdf` / `*.suo` / `Thumbs.db` / `Desktop.ini` 重新变为**可入库**；`Content/` 有 `_BuiltData` 对冲、`Plugins/` 有 `Binaries`/`Intermediate`/`pdb` 对冲，**`.trae`、`Config`、`Source` 三个目录没有对冲**（17 个探针实测，t1 §4.1）。当前索引中不含这类文件，尚无实际泄漏。
- **并在 t12 登记一个 CR 候选（P19）**：建议把 `SessionCommands.md:90` 的 `git add -A` 改为「优先显式路径」，由用户决定是否开 CR。

### 4.7 推送核验口径（含 Actions 被墙时的降级写法）

**推送命令（`SessionCommands.md` 第 97–120 行「推送卡住时的网络恢复流程」第 2 步，实测落在第 110 行）**：

```
git -c http.proxy=http://127.0.0.1:7897 push origin master
```

- **只对这一次命令生效**；原文明确「禁止写入持久 git 配置」→ 不得 `git config --global http.proxy …`。
- 网络实测依据：github.com:443 直连被掐（Connection reset / 21 s 超时），而 gitee / ssh.github.com / npm / baidu 的 443 全通，本机 7897 在 LISTEN。**本方案只引用该条，不另设计路由方案。**

**核验顺序**：

1. `git ls-remote origin refs/heads/master` 的 SHA == 本地 `git rev-parse HEAD`；
2. `git lfs push --all origin` 输出**无待上传对象**；
3. 本地 `check-integrity.py` —— **跑并留档，已知会红**（本机已可运行，见 §9 D22）。**`exit≠0` 本身不是停止条件**（红是既知、既立案的）；真正判据见下方「停止条件」；
4. Actions 核验（`SessionCommands.md:113-120` 强制项）：以本次 `head_sha` 匹配的「治理校验 CI 门禁」「看板部署」两个 workflow 均 `completed/success` 才算**通过**。

**▍停止条件（指挥台撤销令后的新口径，务必逐字执行）**

| 情形 | 判据 | 动作 |
|---|---|---|
| `check-integrity.py` exit≠0，但失败项**全部落在白名单内** | 白名单 = ① `active 门禁 → STATUS.json 格式与状态合法`；② `交叉引用 → STATUS.json 与任务登记册一致`（**两项均指向 M01-T005**） | **不停止**，继续提交与推送；报告里如实写「本地预跑：25 项 / 23 通过 / 2 失败（白名单内，已知既立案）」 |
| 出现**白名单之外的任何新失败项** | 即除上述两项以外的任何失败 | **必须停止推送并报告** —— 这是本次提交**新引入**的问题 |
| **暂存后出现任何 E 类路径**（`.agent-teams/`、`.dsh-uploads/`、`Docs/`、UE 生成目录） | 判据 = **E 类路径命中数 > 0**（**不是**「暂存条数 ≠ 某个数」） | **必须停止**：说明暂存命令用错（误用 `git add -A` / `git add .`）；撤销暂存、按 §4.3 重做。**反向亦成立：暂存条数不等于 43（或 47）本身不构成停机理由** —— F12 已证明该期望值曾被算错，**计数不是同一性凭据** |
| 推送后云端 CI 红 | 且原因 = 已知的 M01-T005 口径冲突 | 如实写「**云端 CI 红，原因=已知的 M01-T005 口径冲突，非本次提交引入**」——**绝不写「通过」** |
| 推送后云端 CI 红 | 原因**不是** M01-T005 | 视为新问题，报告并交指挥台处置 |
| **提交后出现新的 ` M` 行** | 期望为空；**若不为空**（极可能是编辑器随后落盘 —— pid 24284 内存里压着 M01-T001 尚未落盘的改动） | **不追加第二次提交**（指挥台裁定）—— 那批内容属于**另一个活跃任务**，不能由一个基线提交替它定型。**如实记录实际条目**并报告指挥台 |
| **实际提交日期 ≠ CHANGELOG 顶部日期** | `check_changelog_freshness` 会转红 | **不自行补写 CHANGELOG**（治理正文，不在任何人本轮的处置范围）→ **停下报告指挥台**（追加由指挥台在放行时执行） |
| 体检出现**第 3 项**失败 | 白名单**恰好 2 条**，第 3 项即越界 | **停止推送**（= 新问题） |

**白名单基线（verifier 已独立复现，与本方案引用一致）**：exit=1｜25 项｜**23 通过 / 2 失败**；且**污染为零** —— porcelain 45→45、`git status -- dashboard` 为空、`git check-ignore -v` 确认 4 个看板产物全被 `dashboard/.gitignore` 拦下（即体检脚本没有把生成物写进待提交集合）。

**Actions 不可达时的口径（降级，不放宽）**：

- 第 120 行已内置兜底：API 不可达（限流/断网）时「**如实报告『未能核验 Actions』，请用户在 GitHub Actions 页面确认**」。
- 结论只能写「**已推送，CI 未核验**」，**不得**写「推送完成」。第 1/2/3 条是**支持性证据，不等于 CI 绿**，须原样披露（AGENTS.md 不虚构规则）。
- **本地预跑 ≠ 云端通过**：本地红一定红；**本地绿不保证绿**（OS/环境差异）。报告须分列「本地预跑结果」与「云端 CI 未核验」两件事。

**远程拓扑（verifier 服务端实测；本次不改动，仅登记）**：

- 真实远程默认分支 = `master` → **推 master 后落地页正确，无需处置**。指挥台已撤回先前判断；误判来源 = **本地陈旧引用**，本次实测 `git symbolic-ref refs/remotes/origin/HEAD` = `refs/remotes/origin/main`（指向 2026-08-09 的 `e5c8a9a`）→ **可选本地清理项，需用户明确授权，不与基线提交混做**。
- `origin/master` 是本地 `master` 的**祖先** → 本次基线是**干净快进**，无分叉、无需合并。
- 远程另有两条并列无关分支线：`main` = `e5c8a9ae`（孤儿，无共同祖先）、`gh-pages` = `242f0d5e`（**本地对象库无此对象，从未 fetch** → 不对其内容作任何断言）。

---

## 5. `.gitignore` 增补清单与图片存储方式（R5）

### 5.1 `.gitignore` 增补（**只增不减**，指挥台 R1 + R7）

现状：93 行；**不含** `.agent-teams/`、`.dsh-uploads/`（t1 §4.2 第 4/5 条，探针实测 `check-ignore` 无命中）。

| 待增行 | 当前是否被跟踪 | 增补后的副作用 |
|---|---|---|
| `.agent-teams/` | **目录内 4 个文件已被跟踪**（`296ebed`）：`archive/vrsanguo-survey/inbox/captain.jsonl`、`…/inbox/qa.jsonl`、`…/team.json`、`retired-members.json`；其余（当前团队 6 条）未跟踪 | 仅阻止**新增**未跟踪文件入库；**对已被跟踪的 4 个文件无效** —— 它们仍是「已跟踪」，只是本方案也不暂存它们（实测 4 个当前**未被修改**，不出现在 status 中，因此不影响基线后仓库变干净）。彻底脱管须 P1（`git rm --cached`，需用户批准）。 |
| `.dsh-uploads/` | **0 个被跟踪** | 无副作用：3 个文件转为「已忽略」，**本地文件原样保留**、不进仓库。 |

**增补片段（追加到 `.gitignore` 末尾，现有 93 行不动）**：

```
# AI tool session runtime (not project content)
.agent-teams/
.dsh-uploads/
```

**可选（需用户批准，属范围变更，本次不做）**：对冲 `!.trae/**`、`!Config/**`、`!Source/**` 反否定（理由见 §4.6）。

### 5.2 图片存储方式 —— R5 三选项（**本次不做任何一项**，登记供用户裁定）

**问题规模（本方案只读复核后闭合）**：`Content/VRSanguo/Art/References/` 全目录 65 文件 / 99,952,138 B，构成：

| 类型 | 文件数 | 字节 | 是否走 LFS |
|---|---|---|---|
| `.uasset` | 32 | 50,305,202 | ✅ 是（LFS 指针） |
| `.png` | 24 | 48,792,998 | ❌ 否（原始二进制） |
| `.jpg` | 8 | 845,346 | ❌ 否（原始二进制） |
| `.webp` | 1 | 8,592 | ❌ 否（原始二进制） |
| **图片合计** | **33** | **49,646,936 ≈ 47.35 MiB** | — |

> **▍两个范围必须分开写（否则会被读成自相矛盾）—— 指挥台收口裁定**
>
> | 范围 | 数量 | 字节 | MiB（1024²） | MB（十进制） | 构成与备注 |
> |---|---|---|---|---|---|
> | **全仓**（仓库内全部受索引图片） | **48** | **49,760,737** | **47.46** | 49.76 | png 39 / 46.64 MiB；jpg 8 / 0.81 MiB；webp 1 / 0.01 MiB。**≥1 MB 者 18 个 / 46,337,015 B = 44.19 MiB**。来源：指挥台/verifier 实测 **+ 本方案独立复测一致**（F-3） |
> | **`Art/References/` 内** | **33** | **49,646,936** | **47.35** | 49.65 | png 24 + jpg 8 + webp 1。该目录**另含 32 个 LFS `.uasset`**（50,305,202 B）→ 目录全量 = 65 文件 / 99,952,138 B。这是 **R5 备选 (c) 搬迁**的实际体量 |
>
> **两者为何如此接近**：`Art/References/` 的 33 个图片占全仓 48 个的 **68.75% 文件数，却占 99.77% 的字节** —— 全仓图片体量几乎就是这一个目录。因此两个数字**不是矛盾，而是两个范围**：一个描述「仓库整体的非 LFS 图片缺口」，一个描述「R5 搬迁选项能消掉多少」。
>
> **单位纪律**：本文件凡写 **MiB** 即 1024² 字节、写 **MB** 即 10⁶ 字节。t3 §3.2 的「32 张参考图 47.34 MB」实为 **47.34 MiB**（且未计 webp）→ 与上表**一致，不是矛盾**。t1 摘要「25 个 / 49 MB」与其自身正文矛盾，**以正文为准**（见 F-3）。

| 选项 | 内容 | 影响 | 本次 |
|---|---|---|---|
| (a) `git lfs migrate import` | 把已入库图片迁入 LFS | **需重写历史 + 强制推送** | **不做** —— 与硬约束「禁止 `push --force`」直接冲突 |
| (b) 新增 `.gitattributes` 规则 | 以后新图走 LFS | 属范围变更；限定路径与全局 `*.png` 两种写法影响差别很大（全局写法会让已有的 39 张图在下次 `git add` 时被静默转成指针） | **不做** —— 属范围变更 |
| **(c) 参考图移出 Git，归档到 E:**（**推荐**） | 把 `Art/References/` 的图片移到 E: 归档区 | AGENTS.md 磁盘规则本就把「素材包 / 参考图集归档」划给 E:，且 E: 已有 `Temp\VRSanguoRef` 暂存区与 `10-asset-register.md:78` 权威映射；参考图**不是运行时资产**，移出后仓库最大的「非 LFS 大文件」类别直接消失，**规则23 风险清零** | **不做** —— 属内容搬迁，需用户批准（P17） |

---

## 6. 工作目录之外三处现场的登记与退场建议（**全部需用户批准，团队不得动手**）

> **口径**：E: 是**允许**的目标盘（大文件/低频工具/归档/素材）；红线只有一条 —— **不得自行新建文件夹**，需要写 E: 时用已有位置或先问用户；同时「不保留冗余副本」。因此建议只分三类：**位置正确但重复的（该去重）**、**位置不当的（该归位）**、**一次性/误导性的（该退场）**。

### 6.1 `E:\AWorkBackup\VRSanguoYanWuchang\` —— 名不副实的「备份」

| 维度 | 结论 |
|---|---|
| 是什么 | 1929 文件 / **631.0 MB**，内容**只有一个** `Plugins\UEBridgeMCP.disabled-old\`；最新文件 2026-08-31 21:52（含 `UnrealEditor-UEBridgeMCPPCG.pdb` 58.45 MB 等编译产物 + 源码）（t3 §5.2） |
| 是不是项目副本 | **不是**。没有 `Content/`、`Config/`、`Source/`、`.trae/`、`.git`。对照：**现役 `Plugins/` 为 1868 文件**（指挥台实测）—— 一个只装退役插件的旧目录与现役插件树完全不是一回事 |
| 有没有唯一内容 | **可能是唯一的退役插件副本** —— 本方案实测项目 `Plugins/` 下只有 4 个插件目录（`OpenXRExpansionPlugin`、`PICOOpen174f9f81d266V8`、`UE_MCP_Bridge`、`VRExpansionPlugin`），**不含 `UEBridgeMCP*`**。同时 `.trae/CHANGELOG.md:83-85` 与 TD-010 记载：2026-09-03 用户裁决为「**彻底删除、不保留回退**」（原「改名 `.disabled` 保留审计」方案因该目录丢失而作废，回退路径改为重新克隆上游源码 + 重打补丁）→ **本目录与该裁决不一致，属裁决执行残留。** |
| 位置是否正确 | 放在 E: 作为归档盘**位置合规**；但目录名 `VRSanguoYanWuchang` 会被误认为「项目完整备份」→ **命名误导** |
| 建议 | **退场（删除）**，回收 631.0 MB；与 2026-09-03 既有用户裁决一致（P7）。**已由指挥台作为「第 6 项」呈给用户裁定（是否清除该 631MB 残留）；团队不得动手删。** |
| 风险 | 中。删除不可逆；但内容是**可重编译的产物 + 上游可重新克隆的源码**，回退路径已由用户裁定 |

> **⚠ 重大警示（t12 的事实源模型必须写明）**：**`E:` 上不存在任何有效项目备份**，不得把 `E:\AWorkBackup\` 当作「项目已有备份」。若误认，会得出「项目已有备份保障」的错误结论 —— 实际本项目自 2026-09-01 之后从未被完整备份过；**本次推送才是该项目的第一个完整备份**。

### 6.2 `E:\AWork\` —— 用户的工具/素材区

| 维度 | 结论 |
|---|---|
| 是什么 | 三个二级目录：`Temp\`、`Tools\`、`VRExpansionPlugin\` |
| 是不是项目副本 | **不是**项目副本，但含项目相关**资产源与工具** |
| 有没有唯一内容 | **有**。`E:\AWork\Temp\VRSanguoRef\`（1.77 GB）是**活跃资产源库**且有正式治理地位：`.trae/registers/10-asset-register.md:78` 记为基准路径（「2026-08 下旬由 `D:\AWork\Temp\VRSanguoRef\` 迁入；旧报告中的 D: 路径已失效」），`:85-88` 定义 `FBX_Low\*.obj` 为正式导入源（t3 §5.1）。`E:\AWork\VRExpansionPlugin\`（3.4 MB）含 `.git`，是插件源码克隆 |
| 位置是否正确 | **正确**：素材/工具/归档 → E:，符合 AGENTS.md 磁盘规则 |
| **去重（位置正确但重复）** | ① `E:\AWork\Temp\VRExpansionPlugin\`：zip **906 MB** + 两个 842 文件 / **1,020.6 MB** 的解压目录（`Extracted\` 与 `VRExpPluginExample-5.6\` **字节完全一致 → 解压两次**）→ 保留 1 份，回收 **1,926.7 MB**（毛额 2,947.3 MB − 重复计数 1,020.6 MB；P8）；② `E:\AWork\Tools\OpenBRF\openbrf.zip` **11.34 MB** → 回收 **11.34 MB**（P9；t3 原记 39 MB 高估 3.4 倍） |
| **退场（一次性产物）** | `E:\AWork\Temp\vrsanguo_pie_t0.png`、`vrsanguo_sword_view5.png`（08-29 一次性抓图）、`E:\AWork\Temp\VRSanguoRef\OBJ\`（空目录）（P10） |
| **保留** | `E:\AWork\Temp\VRSanguoRef\`（1.77 GB，活跃源库）、`E:\AWork\VRExpansionPlugin\`、`E:\AWork\Tools\venv_asset\`（295.3 MB） |
| 风险 | 中。全部为项目外文件，**删除不可逆** → **需用户批准，团队不得动手**。合计可回收 **≈1,938.0 MB ≈ 1.89 GB**（去重 1,926.7 + 11.34；**已扣除 1,020.6 MB 重复计数**） |

### 6.3 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\` —— 项目外「第二现场」

| 维度 | 结论 |
|---|---|
| 是什么 | 20 文件 / 3.1 MB 的**管理脚本现场**（AGENTS.md 指定：「NTFS 管理脚本：仅项目外 `D:/AWork/TraeAdmin/VRSanguoYanWuchang/`」） |
| 是不是项目副本 | **不是** —— 是工具现场 |
| 有没有唯一内容 | **有，而且很关键**：`rebuild_v5.py`（50,614 B）是当前活跃关卡 v5 的**唯一事实源**（`rebuild_v5.py:7`/`:597`）；`rebuild_v3.py` / `rebuild_v4.py` 承载「v1/v2/v3 可重生」这一**用户决定的前提**（§1.3 缺口 1）；`Set-TraeGovernanceAcl.ps1` / `Unlock-TraeAssets.ps1` 是治理配套工具 |
| 位置是否正确 | **正确**：AGENTS.md 规则「临时脚本不得进入项目」+「NTFS 脚本仅项目外」→ **不需要归位** |
| 建议 | **保留 C×5**：`rebuild_v3.py`、`rebuild_v4.py`、`rebuild_v5.py`、`flip_topdown.ps1`、`Set-TraeGovernanceAcl.ps1`、`Unlock-TraeAssets.ps1` —— **本方案不建议删除任何 `rebuild_*.py`**。<br>**可清理（A×11，需批准 P11）**：`repair_status_json5.js`、`verify2.js`、`verify3.js`、`tmp\scan.js`~`scan4.js`、`tmp\verify1.txt`~`verify3.txt`、`tmp\repair-report.txt`、`tmp\STATUS.repaired.json`。<br>**D×2**：`tmp\STATUS.json.broken-20260910`（事故证据原件，建议留档至事故报告归档后再清）、`tmp\scene_topdown_raw.png`（`rebuild_v5.py:661` 明示为**设计内**中间产物落点，每次重建重写）。 |
| 风险 | 中（涉及重建能力与事故证据）→ **需用户批准，团队不得动手** |

---

## 7. 项目内可再生大目录清理评估（本次不执行）

> 全部为**已被 `.gitignore` 正确忽略**的目录 → 清理只影响磁盘占用，**不影响仓库与备份**。**前置条件：编辑器（pid 24284）必须已关闭**。**⚠ `Saved/` 另有前置条件，见下。**

| 目录 | 实测占用 | 可腾空间 | 清理代价（会失去什么 / 需重建什么） | 最佳时机 |
|---|---|---|---|---|
| `Intermediate/` | 5,947,493,818 B（5.54 GB） | 5.54 GB | 失去编译中间产物（`Intermediate/Android` 3,133,684,958 B + `Intermediate/Build` 2,718,017,493 B）；下次需一次**完整 UBT 重编译**（时长**未实测**，本方案不给估算值） | 编辑器关闭后、且短期内不需要连续构建时 |
| `.vs/` | 3,902,485,459 B（3.63 GB） | 3.63 GB | 失去 VS 浏览/智能提示数据库（`ipch` 1.49 GB、`Browse.VC.db` 1.46 GB、语义符号 0.56 GB）；**不影响构建产物** | VS + 编辑器均关闭时 |
| `Binaries/` | 1,375,841,140 B（1.28 GB） | 1.28 GB | 失去已链接的二进制（`Binaries/Android` 1,196,579,417 B）；下次需重新链接/编译 | 编辑器关闭后 |
| `ArchivedBuilds/` | 758,959,580 B（724 MB） | 724 MB | 失去 2026-08-13 的 `VRSanguoYanWuchang-arm64.apk`（328,385,567 B）与 `libUnreal.so`（430,570,488 B）；如需回归需 **Android 工具链重新打包** | 确认无发布/回归需求后 |
| `DerivedDataCache/` | 308,278,290 B（294 MB） | 294 MB | 失去着色器/派生数据缓存；下次启动重建 DDC（**耗时未实测**） | 编辑器关闭后 |
| **小计（可即时清理，不含 `Saved/`）** | — | **12,293,058,287 B ≈ 12.29 GB** | — | — |
| ⚠ `Saved/` | 1,205,590,432 B（1.12 GB） | 1.12 GB | **禁止直接清理（升级为清理前置条件）**：会**销毁 `L_Prototype_1v1_v3.umap` 的唯一存活副本**（450,808 B，09-10 14:38）+ v2 的 4 份自动存档 + `Saved/Evidence/` 43.8 MB 验收证据 + `Autosaves`/`Crashes`/`StagedBuilds` | **仅在 D28（v3 副本是否转正）裁定完成之后**；且 P12（证据去留）需先定 |
| **合计（含 `Saved/`，理论上限）** | — | **13,498,648,719 B ≈ 13.50 GB（12.57 GiB）** | — | — |

> **⚠ 缺口 2 的硬后果**：`Saved/` 不是「可再生目录」—— 它装着**删掉就再也找不回来的 v3 关卡**。所以本节的可腾空间要以 **12.29 GB**（不含 `Saved/`）为实际可执行口径；含 `Saved/` 的 13.50 GB 只有在 D28 裁定「v3 副本不需要保留」之后才成立。

**明确不计入「清理收益」的两项**（避免误算）：

1. `.git/lfs/objects/`（496 文件 / 723,507,226 B = 690 MB）—— **367 个受管二进制的本地实体来源**；推送成功前删它直接丢内容，推送成功后删它也会让后续 checkout/恢复必须重新联网拉取。t1 §6 明确「**不得作为清理收益计入**」。
2. `.git/objects/` 垃圾 —— 实测 `garbage: 0`、`prune-packable: 0`，可安全回收 **0**；唯一理论收益是把 53 个松散对象（244.67 KiB）打包，**不值得跑 `git gc`**（t1 §6）。

---

## 8. 未落盘风险声明

> **一句话**：本次提交只反映**磁盘现状**；`git commit` + `git push` **不会**把编辑器内存中尚未保存的改动写进去 —— **推送 ≠ 已保存**。

**已知事实**：

1. `UnrealEditor` **pid 24284 仍在运行**（启动 2026-09-09 22:06:05，Responding=True）→ **本团队全程不关闭、不重启它**。
2. 该编辑器仍持有资产写锁：`Content/VRSanguo/VR/BP_VRCharacter.uasset` 与 `Content/VRTemplate/Input/*.uasset`（任务书给定事实）。这 3 个文件同时**出现在待提交清单里** —— 提交的是**此刻磁盘上的版本**。
3. **v5 关卡处于可写状态**：实测 `L_Prototype_1v1_v5.umap` **`RO=False`**，mtime **2026-09-10 21:44:17**，晚于 STATUS.json 最后声称「已上锁」的时点 → 与治理声明「v5 只读」**不一致**（t3 §1.3；治理漂移登记见 R2）。含义：编辑器**仍可能回写 v5**，包括在 t10 提交过程中。
4. **已知「仍未落盘」的完整清单 —— 未能取得。** AgentHub `executor` / `exec-m01-t001` 侧对 3 项**已催 3 轮未回**（t2 §6.2）：① L34 代码归属查证；② 09-08~09-10 变更文件清单（区分「已落盘 / 仅内存」）；③ 送达确认。**目前不可得**。
5. **本方案能提供的只是间接证据**（不升级为结论）：正面——26 项已跟踪修改在磁盘上都有 mtime（如 `VRSanguoGripLibrary.cpp` 2026-09-10 22:31:52）；负面——`BP_VRCharacter.uasset` / `IMC_Weapon_*` 的 LFS 指针变更 mtime 停在 **2026-09-08**，而 M01-T001 在 09-09、09-10 仍有大量活动记录 → **存在「编辑器里改过但磁盘未更新」的可能**（依据不足，交由指挥台/该会话核实）。

**据此提出的操作要求**：

- **t10 提交前确认编辑器不会在同一时刻保存这些资产**（至少：提交期间不操作、不做「顺手保存」）。
- **🔒 v5 SHA256 前后守卫（指挥台 R2 强制项）**：t10 必须在**暂存前后各算一次 `L_Prototype_1v1_v5.umap` 的 SHA256 并比对**：
  - 两次一致 → 继续；
  - **两次不一致 → 说明提交期间被编辑器回写 → 停止提交并报告，绝不提交一个「写入中」的状态。**
- **t10 提交后立刻复测** `git status --porcelain -uall`：**期望为空；若不为空，按上述处理并如实记录实际条目**（不要写成「必须为空」）。**指挥台裁定：不自动二次提交** —— 提交后新出现的脏项极可能是编辑器随后落盘所致，而那批内容（M01-T001 的内存中改动）**属于另一个活跃任务，不能由一个基线提交替它定型**；如实记录 + 报告指挥台。
- **不得**在提交窗口内执行任何「顺手保存 / 顺手重启编辑器 / 顺手重建关卡 / 顺手重写 `Docs/Scene`」的动作（两条冻结令仍生效）。

---

## 9. D-待定与治理缺口清单（原样保留，注明裁定人）

> 原则：**依据不足不升级为结论**。以下各项本次**均不处理**。

| # | 待定项 | 现状 / 缺口 | 应由谁裁定 |
|---|---|---|---|
| D1 | M01-T005 是否应当**正式结项** / 如何收口 | **已立案、待用户裁定**：用户既有裁定 `session-20260904-002.md:156` 明示「（M01-T005 的）收口方式待其汇报后**统一处理，勿自行改**」→ 处置路径 = 等 `session-20260908-002` 的收口汇报 + 用户裁定。**本次基线不修改任何 M01-T005 状态**（原本要执行的「改 `in_progress`」已由指挥台紧急撤销） | 用户（汇报由相关会话提供） |
| D2 | `completed` 词表缺口 | 先前的「改值」处置**已被指挥台紧急撤销**（撞用户裁定，见 D1）→ 本次**不清零**；「policy §6 是否补充 `completed` 一词」亦属 policy 正文变更，**另议**，须与 D1 的收口一起考虑 | 用户 |
| D3 | `ExecutionModel.md:124` 磁盘规则自相矛盾 | 该行仍写「临时文件 → `c:\Users\PC\.trae-cn\work\…`」，与 AGENTS.md「禁止写 C:/用户主目录」冲突（该路径实测存在）→ 需走变更申请（P16） | 用户 |
| D4 | 是否向 AgentHub `inboxes/decision` 投信 | 告知「审计备份任务存在 + 冻结遵守情况」；t2 未擅自发信（发信会改变信箱状态） | 指挥台 |
| D5 | M01-T001 会话记录 mtime 停在 09-08 是否违反规则26 | 其 note 证明 09-09/09-10 仍有活动；需**向该会话核实**，不代判 | 指挥台 / 该会话 |
| D6 | M01-T005 的 v3 关卡口径（记录存在、产物不存在） | A 类；涉及报告/会话/STATUS 三处记录回收 → **单独立项**，不在备份任务内做 | 用户 / 决策模型 |
| D7 | 6 个缺失会话记录（16 处引用） | 建议新增 `sessions/MISSING.md` 显式登记（P4） | 用户 |
| D8 | `.trae/index.md` 漏 `M02-PREP-002` 链接 | A 类，1 行补链（P3） | 用户 |
| D9 | `Build/Patches/PICOOpenXR/` 去留 + 插件 3 处源码改动的流程归属 | 181/184 逐字节相同；3 处差异恰为当前脏项 → 需决定「走补丁机制」还是「有意直接维护插件」 | 用户 / 决策模型 |
| D10 | `L_Prototype_1v1_v4.umap` 的去留（**仅此一项**） | 删除会移除回退基线；**注意：任何 `rebuild_*.py` 均为保留项，不在可删范围**（R1） | 用户 |
| D11 | v5 只读锁丢失 | 治理声明 vs 实测 `RO=False` + 21:44 被再写 → 已给 t10 加 SHA256 前后守卫（§8） | 指挥台（执行前确认） |
| D12 | **全仓 48 个受索引图片**（49,760,737 B = 47.46 MiB）的历史 LFS 迁移 | 需重写历史 + force push → 与硬约束冲突（P15），**本次不考虑** | 用户 |
| D13 | `Saved/Evidence/` 当前代次证据（9 张 / 10.6 MB）是否纳入版本管理 | 现状被忽略 → **换机即失去 v5 验收证据**；**本轮不得移动任何证据文件**（会打断 `check-integrity.py` 当前 PASS 的证据链）。与事实源模型一致的处置只有「纳入 Git」或「明确接受丢失」，本方案**不为其设计任何 E: 归档副本**（P12） | 用户 |
| D14 | `gcm-diagnose.log` 是否删除 | 已被忽略、无入库风险（P5） | 指挥台 |
| D15 | 4 个空目录 + 索引漏链的清理执行 | 生成器会复发；CI 对其完全不可见（P2/P3） | 用户 |
| D16 | 陈旧本地引用 `refs/remotes/origin/HEAD` → `origin/main` | 本地缓存（2026-08-09），不是远程事实；可选本地清理，**需明确授权，不与基线提交混做** | 用户 |
| D17 | 远程并列分支 `main`（e5c8a9ae）/ `gh-pages`（242f0d5e） | **本次不改动，仅登记**；`gh-pages` 本地无对象、从未 fetch → 不作内容断言 | 用户（如需处置） |
| D18 | `Content/` 受管口径差异：t1 记 294，t3 记 292（+4 未跟踪 = 297 磁盘） | 两条独立命令差 2，未闭合 | verifier（t5） |
| D19 | `SessionCommands.md:90` 的 `git add -A` 与本次「显式暂存」的**正文级冲突** | 指挥台已**确认留痕口径**：不改治理正文，只在 t9 §4（§4.6）与 t12 写明偏离与理由；并在 t12 登记 **CR 候选**（P19） | 指挥台（已答） / 用户（是否开 CR） |
| D20 | 规则23「本机路径凭据」的适用范围 | 入库文本普遍含本机绝对路径（既有惯例）→ 需明确该词是否仅指凭据类（§4.5） | 用户 |
| D21 | **`Docs/Scene/` 的最终归属**（本次已按更正裁定排除） | 排除后**演武场场景设计稿 + 生成脚本双双不在备份内**（§1.3 缺口 1）。选项：纳入 Git / 移到 E: 归档 / 明确接受丢失 | 用户 |
| D22 | CI 门禁与解释器（**已解决，本方案已实测复核**） | 本机**有**可用解释器，只是**不在 PATH 上**。精确路径：`D:\App\trae\Traedata\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe`（**本方案实测：`exists=True`，`--version` → Python 3.10.11**；pyyaml 6.0.3）。→ **`Get-Command python` 无结果 ≠ 本机缺 Python**（当时得到的只是「不在 PATH」这一现象，**不是**能力结论）。**t10 必须用上面的绝对路径调用，不得写 `python dashboard/check-integrity.py`。** `exit=0` 不是推送门槛（见 §4.7 停止条件） | t10 |
| D23 | `FBX_Low\textures_*_1024\` 是否真 ≤1024 边长 | 未做图像解码 → **未验证，不作结论**（低优先） | 用户 |
| D24 | `CHANGELOG.md` 时效性（**已裁定**） | `check_changelog_freshness` 比较 CHANGELOG 顶部条目日期与 HEAD 提交日期（当前 09-10 vs 09-04 → 通过），**跨日即转红**。→ **裁定：CHANGELOG 追加由指挥台执行**（登记册维护属指挥台职权），时点 = **用户放行推送前**，内容按**实际提交日期**写一条基线提交记录。**t10 若发现顶部日期 ≠ 实际提交日期 → 不要自行补写，停下报告指挥台。** | 指挥台（执行）/ t10（核对后上报） |
| D25 | `Saved/Evidence/M01-T005/` 中 11 张「其他代次」图（5.8 MB）是否仍有引用 | 代次归类依据文件名前缀，未逐张目视确认（t3 §7.1/§10） | 用户（低优先） |
| **D26** | **治理正文未覆盖「只读审计 / 外部编排任务」的边界 → 与 D32 合并为一条 CR 候选** | 同一根因的三个表现：① 生成物入库 vs 规则19（R4）；② 规则26 会话记录要求与「只读审计任务」的边界（D32，**已裁定不适用**）；③ **规则文本与实现不一致** —— 规则26 称「会话记录缺失 = `check-integrity.py` 将判定失败」，但**实测其 25 项中并无会话记录检查项**（15 个检查组：禁止根 / 文件完整性 / 集合数量 / 索引规范 / Skill 唯一性 / 链接完整性 / active 门禁 / 五件套 / 白名单冲突 / 交叉引用 / 技术债 / 流程超时 / 规则文本 / 变更记录 / 仓库卫生）。→ **本轮不裁定**；**在 t12 交接清单单列一条 CR 候选**（建议标题：**「明确『只读审计 / 外部编排任务』在 `.trae` 治理中的边界与豁免」**）。**▍本轮共登记 3 条 CR 候选**（按用户可决策性排序）：① 本条（D26+D32）；② **根 STATUS.json 与任务包副本之间无任何一致性检查**（`check_five_piece_set` 只验副本存在、`check_task_register_consistency` 只比根 vs 登记册 → **K1 与 B-2 这类漂移在自动化上永不可发现，已实际发生至少两次**）；③ `SessionCommands.md:90` 的 `git add -A` 与显式路径暂存的冲突（D19/P19/D30）。三条**均只登记、不执行**，清单由 **t12 单列一节** | 用户（经 CR） |
| **D27** | **R5 三选项**（历史迁移 / 新增 `.gitattributes` 规则 / 参考图移出 Git） | 三选项 + 推荐 (c) + 影响完整登记于 §5.2；本次三项都不做 | 用户 |
| **D28** | **v3 唯一存活副本是否「转正」** | `Saved/Autosaves/…/L_Prototype_1v1_v3_Auto6.umap`（450,808 B）是 v3 的最后一份（§1.3 缺口 2）。选项：纳入 Git（显式路径）/ 移到 E: 已有位置归档（需批准，且不得新建目录）/ 明确接受丢失。**该项未裁定前，`Saved/` 禁止清理（P6a）** | 用户 |
| **D29** | **`rebuild_v3/v4/v5.py` 是否纳入版本管理** | 三代脚本全在项目外、不在 git、不在任何备份（§1.3 缺口 1）；而「删除旧关卡」的决定以它们存在为前提。选项：纳入 Git（需重新界定「临时脚本不进项目」规则）/ 移到 E: 已有位置归档 / 保持现状但登记风险 | 用户 |
| **D30** | **CR 候选：`SessionCommands.md:90` 的 `git add -A` → 「优先显式路径」** | 理由：`.gitignore` 反否定陷阱会让 `*.log`/`*.tmp` 静默可入库（t1 §4.1）；**由用户决定是否开 CR**（P19） | 用户 |
| **D31** | **图片体量口径（已收口）** | **全仓**受索引图片 = **48 个 / 49,760,737 B = 47.46 MiB**（≥1 MB 者 **18 个 / 44.19 MiB**）；**`Art/References/` 内** = **33 个 / 49,646,936 B = 47.35 MiB**（该目录另含 32 个 LFS `.uasset`，目录全量 65 文件 / 99,952,138 B）。**两个范围必须分开写、各自标单位（MiB/MB）**，否则会被读成矛盾（指挥台收口裁定）。t3「32 张 47.34 MB」= 47.34 **MiB**（未计 webp），与上述一致 | **已收口**（t5 第 2 轮可复核） |
| **D32** | **规则26 会话记录缺口 —— 裁定：不适用，本轮不补建** | **指挥台裁定理由**：本轮 **t1–t12 是 DSH AgentTeams 任务，不是 `.trae` 任务包认领** —— 无 `MNN-TNNN` 编号、未写入根 `.trae/execution/active/STATUS.json`、**无 `claimedBy`**。规则26 约束的是「`.trae` 任务认领」这一动作，其判定物是根 STATUS.json 的 `claimedBy` 与 `.trae/execution/sessions/{sessionId}.md` 的对应关系。**本轮不存在 `.trae` 认领 → 不触发规则26 → 不需要补建会话记录**（原 P20 随之作废）。**但**「AgentTeams 任务体系」与「`.trae` 治理体系」的边界**在治理正文中未定义**，属真实缺口 → **已并入 D26 的 CR 候选，不再单列** | **已裁定（不适用）**；边界问题转入 D26 |

---

## 10. 执行时序（t10 前后，含责任人）

> **▍放行状态（2026-09-10 更新）**：**推送已被用户暂缓**（用户原话「希望你理清楚了再推」）。指挥台已对 git-operator 下 **HOLD**：**在用户给出 5 项裁定、并由指挥台放行之前，不认领、不暂存、不提交、不推送。** → 下表**步骤 4–12 在放行前一律不得执行**。**t12 的交接清单必须包含这 5 项裁定的最终结果。**

> **▍冻结令（指挥台，即刻生效 —— 约束 t10/t11 与 planner 自己）**：**本次勘误是本审计产物的最后一次写入。此后 `audit/` 目录冻结**（不等 t10 开始），直到 t10 完成并报告；**期间任何人（含 planner）不得写入**。三个后果：① 提交后工作区不干净（触发 §4.7 停止条件）；② 仓库内的报告版本与引用它的 t12 对不上；③ 违反证据纪律（`audit/` 是 t12 的引用源）。**若确需补写，报指挥台裁定是否补第二次提交；不得自行补写。**

> **▍执行顺序（用户裁定 · 2026-09-10 追加）**：**本地清理与修改（P1–P19）在推送之前完成；推送为最后一步（见 t12 §12.3）。**

| # | 步骤 | 责任人 | 时点 | 前置 / 验证 |
|---|---|---|---|---|
| 1 | **不修改**根 `.trae/execution/active/STATUS.json` 的 M01-T005 状态（撤销先前的修复指令） | **无人执行**（本次基线明确不做） | — | 用户既有裁定 `session-20260904-002.md:156`「收口方式待其汇报后统一处理，**勿自行改**」；撞裁定即越权 |
| 2 | 用**显式解释器路径**跑 `check-integrity.py` 并**留档**（**已知 exit=1，仍要留证据**） | t10 | 提交前 | 预期：25 项 / 23 通过 / **2 失败**，且两项全在白名单内（verifier 已独立复现）。**`exit≠0` 不阻止推送**；出现白名单外的新失败才停止（§4.7 停止条件） |
| 3 | **核对 CHANGELOG 顶部日期与实际提交日期**（D24）。**若不一致 → 不要自行补写**（治理正文），**停下报告指挥台**；追加由**指挥台在放行时执行** | t10（核对）/ 指挥台（追加） | 提交前 | `check_changelog_freshness`；理由：该检查比「CHANGELOG 顶部日期 vs HEAD 提交日期」，**跨日即转红** |
| 4 | 确认 `.gitignore` 两行已落盘 | t10 | 提交前 | §5.1（本次**不**改 `.gitattributes`） |
| 5 | 确认编辑器不会在提交窗口回写资产（不操作、不保存、不重启） | t10 | 提交前 | §8；两条冻结令仍生效 |
| 6 | **算 v5 SHA256（前）** | t10 | 暂存前 | §8 守卫 |
| 7 | 按 §4.3 显式清单 `git add`；核对 **43 条路径**，且**不得出现任何 E 类路径**（**硬判据以 E 类为准，不是计数**；add 行数**现场复算**；F12） | t10 | — | §4.3 第 5 步 |
| 8 | **算 v5 SHA256（后）并比对**；不一致即**停止并报告** | t10 | 暂存后 | §8 守卫（R2 强制） |
| 9 | `git commit`（**不对被提交文件做内容编辑**，`.gitignore` 除外） | t10 | — | §4.5 |
| 10 | `git -c http.proxy=http://127.0.0.1:7897 push origin master`（**单次生效，禁止持久化**） | t10 | — | §4.7 |
| 11 | 核验：`git ls-remote` SHA 一致；`git lfs push --all origin` 无待上传；复测 `git status` 期望为空 | t10 / t11 | 推送后 | §4.7 / §8 |
| 12 | CI 核验：Actions 可达 → 按 workflow 结论**照实写**；Actions 不可达 → 按 `SessionCommands.md:120` 兜底写「已推送，**CI 未核验**」+ 请用户到 Actions 页面确认。**若云端判红且原因=M01-T005 口径冲突 → 写「云端 CI 红，原因=已知的 M01-T005 口径冲突，非本次提交引入」。任何情形都绝不写「通过」。** | t11 | 推送后 | §4.7 停止条件表 |

**全程禁令**：不得关闭/重启 pid 24284；不得运行 `rebuild_*.py`；不得改写 `Docs/Scene/`；不得删除任何项目文件；不得改动 `Content/`、`Config/`、`Source/` 内容（只暂存其已有改动）；不得修改治理正文/登记册/STATUS.json（M01-T005 由指挥台改）；不得在 E: 新建文件夹；**不得移动任何证据或参考图**；**不建议删除任何 `rebuild_*.py`**。

---

## 11. 修订与口径差异登记（可追溯）

### 11.1 本次修订（v1 → v2）

| 项 | v1（已作废） | v2 起（现行 · 含 v3–v6 增量） | 依据 |
|---|---|---|---|
| `Docs/Scene/` 5 文件 | **列为入库** | **排除**（本次基线不含；列 D-待定 + 需用户裁定） | 指挥台更正裁定（撤销先前 R3 裁定） |
| 暂存清单条数 | 48 | **43** | 上一条的连带结果 |
| 规则23「大型非 LFS 二进制」 | 新增 1 个（scene_topdown.png 2.85 MB） | 新增 **0** 个 | 上一条的连带结果 |
| `Saved/` 清理 | 与其他可再生目录并列 | **升级为清理前置条件**（v3 唯一副本，P6a/D28） | 指挥台缺口 2 |
| R2（v5 只读锁） | 仅登记 | 登记 + **t10 SHA256 前后守卫** | 指挥台 R2 |
| `rebuild_*.py` | 未明确禁止删除建议 | **明确不建议删除任何 `rebuild_*.py`** | 指挥台 R1 |
| Q1/Q2 | 待确认 | 已确认（§4.1 集合由路径清单定义；§4.6 留痕口径） | 指挥台答复 |

### 11.2 与三份盘点的口径差异

| 项 | t1/t2/t3 的原判定 | 本方案采用 | 依据 |
|---|---|---|---|
| `Docs/Scene/` | t2：A+E；t3：C + 待裁定 | **排除**（不入库） | 指挥台更正裁定 |
| `.gitignore` 增补范围 | t1 提出 7~8 条缺口 | 本次**只增 2 行**；其余列为可选、需批准 | 指挥台 R1/R7 |
| t1 的「E: 两处现场」第二处 | **未能查明** | t3 已复核：是 `E:\AWork\Temp\VRSanguoRef\`（资产源库）与 `E:\AWork\`（工具素材区） | t3 §5.1/§5.3 |
| 「远程默认分支指向 main」 | 早期判断 | **已推翻并撤回**（来源为本地陈旧 symref） | §4.7；verifier 服务端实测 |
| 图片体量（**两范围分列**） | t3「32 张 47.34 MB」 | **全仓**受索引图片 **48 个 / 49,760,737 B = 47.46 MiB**（≥1 MB 者 18 个 / 44.19 MiB）；**`Art/References/` 内** **33 个 / 49,646,936 B = 47.35 MiB**（该目录另含 32 个 LFS `.uasset`）→ **不是矛盾，是两个范围**（D31 已收口，指挥台裁定） | 本方案复测 + 指挥台收口裁定 |

### 11.3 仍与治理正文存在的张力（登记，不改动）

1. `Docs/` 曾被治理判废（`.trae/archive/README.md` + `CHANGELOG.md:894/:897`），但盘上仍持续产出 `Docs/Scene/` 生成物 → 张力登记于 D21/D26，走 CR 而非本轮裁定。
2. `SessionCommands.md:90` 的 `git add -A` 与本次「显式暂存」冲突 → 留痕 + CR 候选（§4.6、D30）。
3. `ExecutionModel.md:124` 与 AGENTS.md 磁盘规则自相矛盾 → D3/P16。
4. **规则26（会话记录）与「只读审计 / 外部编排任务」的边界**：指挥台已裁定**本轮不触发规则26**（DSH AgentTeams 任务 ≠ `.trae` 任务认领：无 `MNN-TNNN`、无根 STATUS.json `claimedBy`）→ **不补建会话记录**。但**该边界在治理正文中没有定义**，且存在**规则文本与实现不一致**（规则26 声称 `check-integrity.py` 会判定会话记录缺失，**实测 25 项中无此检查项**）→ 已与 D26 **合并为一条 CR 候选**，在 t12 单列。

---

## 12. 可复核证据索引（本方案实测命令）

| 证据 | 命令 | 本次结果 |
|---|---|---|
| HEAD / origin/master | `git rev-parse HEAD` / `git rev-parse origin/master` | 两者均为 `eb319c3689458d7b1a61d1798adfc5ea8df0c494` |
| 远程跟踪引用 | `git for-each-ref --format='%(refname) %(objectname:short)' refs/remotes` | `origin/HEAD e5c8a9a`、`origin/main e5c8a9a`、`origin/master eb319c3` |
| 本地 symref（陈旧证据） | `git symbolic-ref refs/remotes/origin/HEAD` | `refs/remotes/origin/main`（D16） |
| 脏项总数 | `git status --porcelain -uall \| Measure-Object` | **59**（26 ` M` + 2 ` D` + 31 `??`） |
| `Docs/Scene/` 仍未跟踪 | `git status --porcelain -uall \| Select-String 'Docs/'` | 5 条 `??`（本次排除对象） |
| 已跟踪的 `.agent-teams` 文件 | `git ls-files .agent-teams` | 4 条，**当前未被修改** |
| **v3 唯一副本** | `Test-Path Saved/Autosaves/Game/VRSanguo/Dev/L_Prototype_1v1_v3_Auto6.umap` | **True，450,808 B，2026-09-10 14:38:14** |
| 自动存档全表 | `Get-ChildItem Saved/Autosaves/Game/VRSanguo/Dev -File` | v2×4（370,689–371,056 B，08-25）、v3×3（Auto1/Auto2/Auto6）、v5×10（Auto0–Auto9）、L_SkeletonTest×5 |
| **图片体量（两范围分列）** | 全仓：`git ls-files '*.png' '*.jpg' '*.jpeg' '*.webp'` + 工作区尺寸求和；目录：单独求和 | **全仓 48 文件 / 49,760,737 B = 47.46 MiB**（png 39/46.64、jpg 8/0.81、webp 1/0.01；≥1 MB 18 个 / 44.19 MiB）；**`Art/References/` 65 文件 / 99,952,138 B** = `.uasset` 32/50,305,202（LFS）+ `.png` 24/48,792,998 + `.jpg` 8/845,346 + `.webp` 1/8,592；其中图片 33 个 / 49,646,936 B = 47.35 MiB（D31） |
| 项目插件目录 | `Get-ChildItem Plugins -Directory` | 4 个，**不含 `UEBridgeMCP*`**（支撑 §6.1） |
| 本会话 Python | `Get-Command python` / `Get-Command py` | **均无结果**（D22：t10 须用显式路径） |
| 输出文件完整性 | `[System.IO.File]::ReadAllBytes/ReadAllText` 校验 | UTF-8 无 BOM、无替换字符、章节齐全 |
| 规则23 密钥扫描 | t2 §8 静态复算（14 个待提交文本） | 0 命中 |
| CI 门禁基线（**白名单内，已知**） | 指挥台实测 + **verifier 独立复现** | exit=1，**25 项 / 23 通过 / 2 失败**，两项均指向 M01-T005（属 §4.7 停止条件白名单） |
| 体检脚本无污染 | verifier 复现 | porcelain **45→45**（跑前跑后不变）、`git status -- dashboard` 为空、`git check-ignore -v` 确认 4 个看板产物全被 `dashboard/.gitignore` 拦下 |

**未由本方案复核、仅引用的结论**（标注来源，避免混淆归属）：CI 运行结果与 `check-integrity.py` 行为、两份关卡的 sha256/字节数、`VRSanguoYanWuchang.log` 的 MAP LOAD 行、现役 `Plugins/` 1868 文件（**来源=指挥台实测**）；远程 HEAD 与分支拓扑（**来源=verifier 服务端实测**）；E: 与 TraeAdmin 目录规模（**来源=t1/t3 实测**）。

→ **t12 交接清单必须保留这条「按来源分层复核」的要求**：**转述 ≠ 本方复现**，复核时须按来源分层，不得把引用当成自测。

---

## 附录 A：机读摘要

```json
{
  "task": "t9",
  "revision": "v2 (Docs corrected to excluded per captain ruling; R1-R7 folded in)",
  "member": "planner",
  "readonly": true,
  "wroteOnly": [".trae/execution/reports/audit/t9-cleanup-and-retention-plan.md"],
  "factSourceModel": {
    "workingDir": "D:\\AWork\\Unreal\\Project\\VRSanguoYanWuchang",
    "vcs": "local git repo (branch master)",
    "origin": "https://github.com/wzf12138/sanguoVR.git",
    "backup": "push to origin (FIRST complete backup of this project)",
    "localBackupCopies": "none (by design)"
  },
  "backupCompletenessGaps": [
    "rebuild_v3/v4/v5.py live outside the repo (D:/AWork/TraeAdmin/...) - not in git, not in any backup; deleting is the premise of the user's v1/v2/v3 deletion decision",
    "L_Prototype_1v1_v3.umap: never in git, gone from disk; only surviving copy is Saved/Autosaves/.../L_Prototype_1v1_v3_Auto6.umap (450808 B, 2026-09-10 14:38) inside .gitignore-covered Saved/",
    "Docs/Scene/ drafts + their generator rebuild_v5.py are both outside the backup"
  ],
  "baseline": {
    "head": "eb319c3689458d7b1a61d1798adfc5ea8df0c494",
    "originMaster": "eb319c3689458d7b1a61d1798adfc5ea8df0c494",
    "fastForward": true,
    "dirtyCountMeasured": 59,
    "setDefinedBy": "explicit path list (NOT by count)",
    "stagingMode": "explicit paths only; git add -A forbidden",
    "expectedStagedPaths": 43,
    "includeCounts": { "trackedModified": 26, "deletions": 2, "untrackedPaths": 14, "gitignore": 1 },
    "excludeFromBaseline": [".agent-teams/", ".dsh-uploads/", "Docs/", "E:/", "D:/AWork/TraeAdmin/"]
  },
  "requiredUserApprovals": 19,
  "reclaimableInsideProject": {
    "safeNow": { "bytes": 12293058287, "dirs": ["Intermediate", ".vs", "Binaries", "ArchivedBuilds", "DerivedDataCache"] },
    "blockedOnD28": { "bytes": 1205590432, "dir": "Saved", "reason": "only surviving copy of v3 lives in Saved/Autosaves" }
  },
  "mustNotCountAsReclaimable": [".git/lfs/objects (723507226 B, only local source of 367 LFS assets)"],
  "ciStatus": {
    "state": "known / filed / pending user decision - NOT cleared by this baseline",
    "measured": { "exit": 1, "checks": 25, "passed": 23, "failed": 2 },
    "whitelist": ["active 门禁 → STATUS.json 格式与状态合法", "交叉引用 → STATUS.json 与任务登记册一致"],
    "actionThisRound": "none - user ruling session-20260904-002.md:156 says 'do not change it yourself'",
    "escalationPath": "wait for session-20260908-002 closure report + user decision",
    "layering": "the 2 gate failures read ONLY root STATUS.json; they are NOT the same thing as the 5-copy status drift"
  },
  "pushRoute": { "command": "git -c http.proxy=http://127.0.0.1:7897 push origin master", "source": "SessionCommands.md:97-120 step 2 (line 110)", "persistentConfig": false },
  "ciVerification": { "required": true, "docRef": "SessionCommands.md:113-120", "fallback": "'push done, CI unverified'", "caveat": "local red implies red; local green does NOT guarantee green", "neverWritePass": true, "redWording": "'cloud CI red, cause = known M01-T005 wording conflict, NOT introduced by this commit'" },
  "stagingGuards": ["v5 umap SHA256 before/after staging must match, else abort (R2)", "post-commit git status expected empty", "push stop condition: any NEW failure OUTSIDE the whitelist; exit!=0 alone is NOT a stop condition"],
  "remoteTopology": { "defaultBranch": "master (no action needed)", "staleLocalSymref": "refs/remotes/origin/HEAD -> origin/main", "unrelatedBranches": ["main e5c8a9ae", "gh-pages 242f0d5e (never fetched)"] },
  "crCandidates": [
    "CR-1 (D26 + D32 merged): define the boundary/exemption of 'read-only audit / externally orchestrated (DSH AgentTeams) tasks' in .trae governance - covers rule19 vs generated artifacts, rule26 vs AgentTeams tasks (no MNN-TNNN, no claimedBy => not a .trae claim), and the rule-text-vs-implementation gap (rule 26 claims check-integrity.py fails on missing session records, but its 25 checks contain no such item)",
    "CR-2 (NEW): NO consistency check exists between root STATUS.json and per-task package copies - check_five_piece_set only verifies copy existence; check_task_register_consistency only compares root vs register; neither compares root vs task copies => K1 (M01-T005 authority drifted outside its 4 copies) and B-2 (M00-T004 copy not cleared with authority) can never be caught automatically; both already happened at least twice. Suggested fix: add field-level root-vs-copy check, and do 'copy write-back to authority' + 'add the check' together",
    "CR-3: SessionCommands.md:90 'git add -A' conflicts with the explicit-path staging this baseline requires (D19/P19/D30)"
  ],
  "pendingDecisions": 32,
  "unresolvedRisks": ["unlanded-editor-changes list unavailable (mailbox chased 3 rounds, no reply)", "v5.umap RO=False and rewritten at 21:44:17", "48 tracked images / 49,760,737 B (47.46 MiB) non-LFS history left as-is (errata v6: was wrongly recorded as 39 PNG/JPG 46.6MB)", "v3 only copy inside Saved/ which is not backed up"]
}
```

---

*报告完（v2）· planner · 本文件为 t9 唯一写盘产物；除只读命令外，未执行任何处置动作。*
