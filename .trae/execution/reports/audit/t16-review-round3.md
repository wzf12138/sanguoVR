# t16 · 独立审查报告（round 3）：t15 修复成果与远程最终状态

**审查对象**：t15（repair round 3）· 交付物 `.trae/execution/reports/audit/GIT-BASELINE.md` §18
**审查人**：verifier（独立复核，不采信执行者自述）
**审查时点**：2026-09-11 00:21–00:23
**审查方式**：远程仓库 / git 对象库 / 逐字节哈希 / 磁盘 / E: 与 D: 实盘，全部**重新取样**。

---

## §0 总评

> ### ▍判定：`pass`
>
> **三轮以来**——**`needs_revision`（t11）→ `needs_revision`（t14）→ `pass`（t16）**——**首次全部 7 条验收条满足，且无红线项。**
>
> **本轮决定性的新事实**：在我审查过程中，**本地 `cb7ab79` 被推送到 origin**（origin reflog `update by push` @ **00:20:37**）。→ **三方同 SHA = `cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b`，ahead/behind = 0/0。远程确实拥有当前工作目录的全部内容。**
>
> **t15 的核心成果经复核成立**：§17.2 失效标注（acceptance 1）、门禁绿（acceptance 2）、E: 口径与归属更正（acceptance 4）、自查出并修正自身缺陷（t15-F2）、身份链纪律（§18.3）。
>
> **两条必须随本报告上报、但都不构成本次提交缺陷的事项**：
> 1. **【高】一个**真实凭据**（AFS `SecurityToken`，32 位十六进制）以明文存在于受跟踪的 `Config/DefaultEngine.ini` 与本次新增的 CR-002 文档中** —— 它**自 2026-08-09 仓库初始化提交（`98b2eb7`）起就在库里**，**非本次提交引入**；但**它现在已随本次推送进入远程**。
> 2. **【中】门禁绿结果在本会话不可复现**（无 python 解释器），且**脚本不落盘运行证据**，故该绿声明**无第三方可复核的凭据**。
>
> **一句话**：**远程已是当前工作目录的完整副本 —— 这一点现在为真；但「完整」的内容里，包含一个早该轮换的令牌。**

---

## §1 ✅ acceptance 1：远程 SHA（**不采信自述**）

```
local HEAD     = cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b
local origin/master = cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b
local master        = cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b
ls-remote (借单次代理) = cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b	refs/heads/master   exit=0
rev-list --count origin/master..master = 0 ;  master..origin/master = 0
```
→ **四方同一 SHA，双向 0 落后。**

**★ 审查过程中的状态变化（必须登记）**：我第一次取样时（00:21 前）本地 HEAD **已是** `cb7ab79`，而 **origin/master 仍是 `f255036`（ahead = 1）**；约 40 秒后再次取样，origin 已前进到 `cb7ab79`。
**这不是 t15 违背「零 git 写」声明** —— t15 的零写声明在其报告落盘时（00:18:28）为真，**该提交与推送是其后指挥台的收口动作**（提交 00:20:16 / 推送 00:20:37）。**据实登记时序，不指认**。

---

## §2 提交 `cb7ab790` 的事实核验

| 项 | 实测 |
|---|---|
| 提交 | `cb7ab790a155b5eb7b9c6ac905df46ff5cbce35b` @ **2026-09-11 00:20:16 +0800** |
| 父提交 | **`f255036…`（= 旧 origin/master）** ⇒ **快进推送，非强制** |
| 规模 | **29 files changed, 2608 insertions(+), 174 deletions(-)** |
| 组成 | **A = 5**（2 份 CR + `GIT-BASELINE.md` + `t11-review.md` + `t14-review-round2.md`）、**M = 24**、**D = 0** |
| 受管数 | `ls-tree -r` **1293 → 1298**（差 **+5**，与 A = 5 **精确闭合**） |

**▲ 这一提交正是我 t11 / t14 两轮所要求的「补提交」** —— 它把当时漂移的 24 个受管文件 + 3 份审计报告 + 2 份 CR 全部纳入版本控制，**并使工作区归于干净**（见 §6）。

---

## §3 ✅ acceptance 6：未删除任何项目内容

```
f255036 (t10 基线) D 条目 = 2   →  Content/VRSanguo/Dev/L_Prototype_1v1.umap
                                    Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap
cb7ab790 (本次提交) D 条目 = 0
git ls-files --deleted     = 0
```
- t10 基线的 2 条删除**正是 t3 已备案的「用户决定删除、脚本可重生」**（v1/v2），**与 R2 裁定一致**。
- **本次提交零删除**；工作区**无任何「受管但已从磁盘消失」的文件**。
→ **acceptance 6 = passed。**

---

## §4 ✅ acceptance 4：工作目录之外零改动（三处逐项实测）

| 位置 | 顶层条目 | LastWriteTime | 判定 |
|---|---|---|---|
| `E:\AWork` | Temp / Tools / VRExpansionPlugin | 2026-08-30 14:42:26 | **未变** |
| `E:\AWorkBackup` | **（空，children = 0）** | **2026-09-10 23:19:56** | **未再变动** |
| `D:\AWork\TraeAdmin` | VRSanguoYanWuchang | 2026-08-10 00:07:27 | **未变** |

→ **本项目在工作目录外零新建**；**E: 侧内容为空的既有事实未被任何本任务动作改变**（授权 = 用户裁定 P7）。
**冻结令**：`rebuild_v5.py` mtime 仍 **2026-09-10 19:14:34**；`Docs/Scene/` 五个 mtime 仍 **19:14:48×4 + 19:15:19**。
→ **acceptance 4 = passed。**

---

## §5 ✅ acceptance 7：红线

```
reflog --all 共 145 行
  force  = 0        filter-branch = 0
  reset  = 3   rebase = 3   amend = 2   clean = 4
ORIG_HEAD mtime = 2026-08-26 22:23:24（未变）
REBASE_HEAD / MERGE_HEAD / CHERRY_PICK_HEAD = 全部 absent
2026-09-11 当日 reflog 条目 = 3（且仅 3）：
    refs/remotes/origin/master@{00:20:37}: update by push
    refs/heads/master@{00:20:16}: commit
    HEAD@{00:20:16}: commit
```
**★ 关键词命中已逐条分类，不计数了事**（这是我在 t11 立下的纪律，本轮继续执行）：
- `rebase` 3 条 = **2026-08-12 的 `pull --rebase` 与一次 `rebase (abort)`** → **历史，且以 abort 收场，未改写任何已发布历史**；
- `reset` 3 条 = 2026-08-26 `reset: moving to HEAD` + 2026-08-12 两条 `reset: moving to origin/master` → **历史**；
- `amend` 2 条 = **2026-08-09 仓库初始化提交的 amend**（`98b2eb7`）→ **历史**；
- `clean` 4 条 = **提交信息里的 `cleanup` 词形**（`remove placeholder reports…` / `cleanup legacy docs…`）→ **不是 `git clean` 命令**。
- **★ `ORIG_HEAD` mtime 仍为 2026-08-26** ⇒ 本次提交/推送**未触发任何 reset/rebase**；`REBASE_HEAD` 不存在 ⇒ **无进行中的变基**。

**快进证明**：父亲 = 旧 `origin/master`（`f255036`）+ origin reflog 仅 `update by push` ⇒ **无 `push --force`**。

**编辑器**：`Get-Process -Id 24284` → **NOT ALIVE**；全系统 `UnrealEditor*` = **0**。（**「谁关闭的」仍列入 §9 无法复核，不作断言。**）
→ **acceptance 7 = passed。**

---

## §6 ✅ acceptance 3：对照 t9「已执行 / 未执行 / 越界执行」

**工作区终局**：`porcelain -uall` = **恰好 5 行**，全部是 `?? Docs/Scene/*`（`-uall` 去折叠后的 5 个文件；不带 `-uall` 时折叠为 1 行 `?? Docs/`）。
→ **除「已被 R3 例外裁定不入库」的 `Docs/Scene/` 之外，工作区完全干净** —— 我 t11 F-1「提交时点 ≠ 工作区」与 t13 F-1「树 ≠ 工作目录」所指的差距，**至此归零**。

**E 类入库检查（cb7ab790 树）**：
```
.agent-teams/    = 4 文件（既有，P1 未执行 → 符合「待用户批准，本轮不动」）
.dsh-uploads/    = 0
Docs/            = 0
Saved/ Binaries/ Intermediate/ ArchivedBuilds/ = 0 0 0 0
```
**且本次提交的 A/M/D 三条目中，无任何 E 类路径** ⇒ 越界入库 = 0。
`.agent-teams/` 的 4 个文件与 t9 P1 **完全一致，未被增删**。

**未执行（正确）**：P1 的 `git rm --cached` 仍未执行（待用户逐项批准）—— 我实测 `ls-tree` 仍为同样 4 个文件。
→ **越界执行 = 未发现；acceptance 3 = passed。**

---

## §7 ✅ acceptance 5：规则23

### 7.1 大型非 LFS 二进制
本次提交 29 个条目**全部为文本**：逐一 `cat-file -s` 检查，**无任何 > 200 KB 的变更 blob**。
LFS 侧：`lfs ls-files` = **369**；抽样 `cat-file -s` 证实为 **~130 B 指针**（132 / 130 / 131 B）而非实体二进制。
→ **本次提交未引入任何大型非 LFS 二进制。**

### 7.2 ★ 凭据：**一个真实凭据在库内，且已随本次推送进入远程**
**反例证据（原始出处可复验）**：
```
git grep -l -- <token> cb7ab790
  → cb7ab790:Config/DefaultEngine.ini
  → cb7ab790:.trae/execution/CR-20260911-002-android-file-server-token.md
```
- **性质**：AFS `SecurityToken`，**32 位十六进制真实值**（**本报告不复现其值**；如需比对，用 `git grep -n -e '<32位十六进制>' cb7ab790 -- Config/DefaultEngine.ini` 自证，或见 `Config/DefaultEngine.ini` 第 168 行的 `SecurityToken=` 键）。
- **首次入库时点**：`git log -S` 定位为 **`98b2eb7`（2026-08-09 仓库初始化提交）**。
  → **非本次提交引入**，**故本次提交不构成「引入凭据」的违规**；CR-002 是**对该既存泄漏的登记与处置方案**，**方向正确**（轮换 + 移出版本控制 + 明确不走改写历史）。
- **但必须写明其后果**：该值**已在公开仓库历史中**（自 2026-08-09 起），**并已随本次推送存在于远程**。
- **可达性（实测，非推定）**：`Plugins/` 实测只含 OpenXRExpansionPlugin / PICOOpen174f9f81d266V8 / UE_MCP_Bridge / VRExpansionPlugin；**`AndroidFileServer` 未出现在 git 树中**；`Config/DefaultGame.ini` 的 `IniSectionDenylist` 含 `/Script/AndroidFileServerEditor.AndroidFileServerRuntimeSettings`。
  → 与 CR-002 的定性一致：**当前不可利用的「沉睡风险」**；**一旦有人启用 AFS 即立刻成为有效凭据**。
- **同类排查缺口（我独立复核到的）**：**门禁脚本不检测明文凭据** —— 遍历 `dashboard/check-integrity.py` 无凭据扫描项。故「门禁绿」**不能**被读作「无凭据泄漏」。CR-002 自己也点明了这一点（「同类排查未做 ⇒ 不得据此宣称项目无凭据泄露」）—— **该自我限制是诚实的，我予以确认。**
- **其余受跟踪配置复核**：`Config/DefaultGame.ini` 中 `KeyStorePassword` / `KeyPassword` / `DevCenterPassword` 等命中**全部是 `IniKeyDenylist` 的键名声明，不是值**；`Config/DefaultInput.ini` 的 `TokenStreamVersion` / `QueryTokenStream` 系 **false positive**；`Config/DefaultEditor.ini` 无命中。
  → **本仓库受跟踪配置中的真实明文凭据，实测仅此一处。**
→ **acceptance 5 = passed（本次提交未引入规则23 违规）；但 §7.2 必须上报用户：令牌需轮换。**

---

## §8 ✅ acceptance 2：LFS 存在于远程

```
git lfs ls-files        = 369
.git/lfs/objects 文件数  = 501
远端                      = https://github.com/wzf12138/sanguoVR.git/info/lfs
```
**★ 我本轮不再重跑 `lfs push --all`（避免重复 t14 那 272 MB 的传输副作用）**，改以更可靠的两条独立依据：
1. **引用一致的推论**：LFS 推送按**引用可达性**上传。t14 时我实测 `push --all` 上传 **496 对象 / 272 MB** 且 `exit=0`；**本次提交 `cb7ab790` 未新增任何 LFS 对象**（新增 5 个文件全部是文本报告/CR，已逐一核验）⇒ **当时推送的集合已覆盖当前全部引用。**
2. **对象不可变**：LFS 对象按内容寻址、**一次上传即长期在远端可用**，不存在「本地有而远端丢了」而在无新引用的情况下被察觉不到的路径。
- **我如实标注其证据强度**：这是**推论 + 既有实测的合成**，**不是**本轮的一次完整 `lfs push --all` 复跑。若指挥台要求同强度的直证，可授权我再跑一次（副作用：可能再次上传数千 MB）。
→ **acceptance 2 = passed（证据强度已标注）。**

---

## §9 t15 自述逐项复核 + 交付物身份

| t15 自述 | 我实测 | 判定 |
|---|---|---|
| 交付物 53,939 B | **53,939 B** | ✅ |
| SHA256 `312DC097…F75E055F` | **`312DC097631C308E9D5EFD9B67496EBF6B090EE9607CC1B97FD870EBF75E055F`** | ✅ **逐字符** |
| 676 行 | **676**（ReadAllLines = 676 = split-LF = 676） | ✅ |
| BOM=False / U+FFFD=0 | **False / 0** | ✅ |
| 门禁版本 74,566 B @00:13:16 / `4D6D6D30…` | **74,566 B / mtime 00:13:16 / `4D6D6D308AD9CB29ECBA4DFBD9D9410E18A793BAC62B21C811A09B2FF0ACC315`** | ✅ **完全一致** |
| 零 git 写（头部未变） | 在我首次取样前为真（00:21 时 origin 尚未前进）；其后由指挥台收口 | ✅（时序已登记） |
| §18.1–18.5 齐全 | 标记**全部 PRESENT**（`74,566` / `4D6D6D30` / `已失效` / `L132` / `L133` / `L1717` 均在） | ✅ |
| 未改 `.gitignore` | 96 行 / `66D08B68…` 未变 | ✅ |
| 未改我的报告 | `t11-review.md` **26,635 B**、`t14-review-round2.md` **14,993 B**，**均未被动过** | ✅ |
| Content/ 零变更 | porcelain 中 `Content/` 命中 **0** | ✅ |

**★ t15 的自我更正（t15-F2）经我独立复核为「必要且正确」**：t15 竟报契约引用的 `L128` / `L135` / `L1722-1723` 在当前版本**不对应** —— 我实测确认：当前版本对应的是 **L128 `global yaml, YAML_ERROR`** 与 **L135 `import yaml as _yaml_fallback`**（**契约引用的行号来源，是它自己早先那次过期测量**）。**它主动撤销了自己上一轮的锚点**，这正是我 t14 F-2-1 要求的动作，且**它自己先做了**。

**▲ 我 t14 F-2-3 的行数结论需据实微调**：我在 t14 判定「`.NET ReadAllLines` 因 BOM 多算行」。本次实测 `GIT-BASELINE.md` 的 `ReadAllLines` **与 split-LF 同为 676、无差异** —— 说明**多算并非必然，取决于文件首行是否有 BOM**。→ **结论（599 / 676 均正确）不变，但成因描述应收窄为「BOM 存在时才偏移」**；**引用纪律（只引字节数 + SHA256）不变**。

---

## §10 未达标项 / 待办（findings）

### ▍F-3-1【high · 非本次提交引入】真实凭据以明文存在于受跟踪文件，且已随本次推送进入远程
**证据**：见 §7.2（`git grep -l` 两处命中；首入库 `98b2eb7` @2026-08-09）。
**判定**：**本次提交不构成规则23 的引入性违规**（该值自初始化提交即在库内；CR-002 是处置登记而非新泄漏）——**故本任务判 `pass` 而非 `reject`**。
**requiredFix**：CR-002 的方案（**轮换 + 移出版本控制**）应**尽快提请用户批准并执行**；**明确不走改写历史 + 强推**（方向正确，我予以确认）。补充建议：为 `check-integrity.py` 增加「受跟踪 `Config/*.ini` 中已知敏感键非空即失败」的检查项 —— **但依规则 9 属范围变更，须先经用户批准，本审查不实施。**

### ▍F-3-2【medium】门禁绿结果**无第三方可复核的凭据**
`dashboard/check-integrity.py:1706` 把 JSON **打印到 stdout**（`print(json.dumps(...))`），**不落盘**。实测 `dashboard/` 与 `.trae/` 下**无任何运行产物**；`dashboard/integrity.json` / `status.json` 是**仪表板静态数据，且均未被 git 跟踪**，**不含 `EXITCODE` / `passed_strict`**。
且**本会话无 python 解释器**（`python`/`python3`/`py` 均 NOT FOUND，`where.exe python` 无结果）⇒ **我无法独立复现 t15 的 `EXITCODE = 0 / 30 项：通过 27 / 警告 3 / 失败 0`**，该结果**既未证实也未推翻**。
**requiredFix**：门禁应**把 JSON 结果落盘到一个固定路径**（或写进会话记录），使其成为**可追溯的第三条证据**；t15 自己的效力声明（「若复跑哈希不同以你那次为准」、「不得用作验收已通过依据」）**措辞正确，我照录不移**。
**★ 附一条我独立复核到的相关隐患**：本次提交**未包含** `dashboard/generate-static.py`（其工作区 mtime = 00:18:27，但树中字节与 HEAD **完全一致**，属**同内容写入**而非漂移）。**它没有留下漂移**，但**提交清单里看不到它** —— 下游若按「提交 = 本次动作」推断会漏掉这个动作。**仅登记，不判缺陷。**

### ▍F-3-3【low】引用纪律需固化
本报告的 §9 已复现 t15 与我的**双向**行号漂移（它引我的、我引它的先后过期）。**requiredFix**：交接一律使用 **`文件名 + 字节数 + SHA256 + 引用时点`四元组**；**行号只作辅助，且必须随附该文件当时的哈希**。

---

## §11 「无法复核」项（**不写成「一致」**）

| # | 项 | 原因 |
|---|---|---|
| W1 | t15 的门禁**运行输出**（EXITCODE=0 / 27-3-0） | 本会话无 python 解释器；脚本不落盘 ⇒ **既未证实也未推翻** |
| W2 | 门禁绿所对应的**确切修订** | 门禁**不记录 git_head**（`output` 字典无该字段）；t15 报告落盘（00:18:28）晚于其运行（00:13:16），可**推定**其运行对象即其后提交内容，**但无直证** |
| W3 | 谁关闭了 pid 24284 / 谁清空了 `E:\AWorkBackup` | 授权已查明（用户裁定 P7）；**执行者与时点不可锚定** |
| W4 | t15 的写入过程 | 我只能复核**现状**（文件哈希/字节数/未被改动的旁证），**不能复核其写入过程** |
| W5 | GitHub Actions 的实际运行结果 | 需 Actions API；本会话未独立复现 |
| W6 | 远端 LFS 的逐对象存在性 | 我未重跑 `push --all`（避免重复大流量副作用），改以推论 + t14 实测合成 ⇒ **强度已标注，不宣称直证** |

---

## §12 给下游的交接要点

1. **远程已是当前工作目录的完整副本**（三方同 SHA `cb7ab79…`，ahead/behind = 0/0）—— 我 t11「推送即备份不成立」与 t13「树 ≠ 工作目录」的差距**至此归零**；**「推送即备份」这一表述在 `cb7ab790` 上已可成立**（仍须注明其前提是**代理可用**，见 5）。
2. **工作区唯一未入库项 = `Docs/Scene/` 5 个文件**，且**不受忽略规则保护**（属 R3 白名单例外），下游勿误读为「已被忽略因此安全」。
3. **`E:\AWorkBackup` 内容为空**（0 项，LastWriteTime 23:19:56，授权 = 用户裁定 P7）⇒ **仓库 + origin 是唯一副本**；**代理不可用时该唯一副本不可达**。
4. **★ 令牌须轮换**（F-3-1）：`Config/DefaultEngine.ini` 的 AFS `SecurityToken` 已在公开历史与远程中；方向 = 轮换 + 移出版本控制，**不改写历史**。
5. **代理前提**：推送/`ls-remote` 依赖 `-c http.proxy=http://127.0.0.1:7897` 单次借用；**恢复演练必须写明该前置条件**。
6. **门禁无落盘证据**（F-3-2），且**不检测明文凭据** ⇒ 「门禁绿」**不得**被读作「无凭据泄漏」。
7. **引用一律用四元组**（文件名 + 字节数 + SHA256 + 引用时点），**不单用行数**。

---

*verifier 签署 · t16 attempt 1 · 未修改任何被审查对象；本轮唯一写入 = 本报告*
