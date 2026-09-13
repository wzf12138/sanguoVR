# 操作纪律（VRSanguoYanWuchang）

**性质**：本项目**操作纪律的索引**。正文按主题分置于下列文件；**本文件不复制正文**。

**权威关系**：治理契约见 `policy.md` / `change-request-template.md` / `definition-of-done.md` / `responsibility-matrix.md`；规则正文见根级 `AGENTS.md`；本目录各操作模型服从治理契约。

## 主题索引

| 主题 | 权威正文 |
|---|---|
| **推送决策 / 暂存边界 / 网络恢复 / CI 取证** | `push-and-network.md` |
| **判据纪律**（量具 / 三态 / 停手分级 / 取数口径） | `judgement-discipline.md` |
| **文书纪律**（编辑锚点 / 标题形态 / 渲染层书写） | `writing-discipline.md` |
| **清单外异常口径**（口径 ③~⑦） | `exception-taxonomy.md` |
| **判据工具实现规格**（条款与 TC） | `../execution/CR-20260912-001-judgement-tool.md` |
| **规则正文 / 副本与可追溯** | 根级 `AGENTS.md` |
| **治理权威链 / 文件控制等级 / 状态词表** | `policy.md` |
| **规则 ⇄ 门禁覆盖关系** | `rule-gate-matrix.md` |
| **短指令清单** | `SessionCommands.md` |

---

## 安全默认

### AFS 密钥（`Config/DefaultEngine.ini` 的 `SecurityToken`）—— 无自动兜底，必须人工把守（2026-09-12 探针实证）

- **现状**：`SecurityToken=` 为**空值**；真实取值在项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\keys\afs-security-token.txt`（不进仓库，823 B）。**该值未轮换**，且在历史提交中仍可检索到 —— 动作性质是「**停止继续泄露**」，不是「已消除暴露」。
- **⚠⚠ 门禁抓不到它（2026-09-12 探针实证，非推断）**：`dashboard/check-integrity.py` 的密钥扫描（`check_secret_patterns`，检查项 17）**只匹配厂商格式**（`ghp_…` GitHub、`xox…` Slack 等，见 `check-integrity.py:846-847`）。**把 `SecurityToken=` 填成 32 位十六进制串后，门禁仍判 `30 项 / 通过 29 / 警告 1 / 失败 0 / EXIT=0`**（探针用假值，已即时还原）。该检查的 detail 文本已显式声明覆盖边界并指向 `execution/CR-20260911-002-android-file-server-token.md`。
- **⚠ 编辑器会吃掉该文件里的注释（2026-09-12 事故）**：`4b89763` 在 `DefaultEngine.ini` 写入的 4 行密钥警示注释，**被编辑器于 2026-09-12 10:50:08 重写该文件时整段删除**（`SecurityToken=` 空值行保留）。⇒ **该文件中的人工警示不是持久防护**，且每次编辑器保存都会产生一次「看起来像改动」的 diff。
- **⇒ 由此成立的完整风险链**：本机启用 AFS → 按注释把 token 填回 → 编辑器保存 ini → `git add Config/` → **提交泄露，且没有任何自动检查会拦住。**
- **人工纪律（在轮换或结构性修复落地前，必须执行）**：
  1. **任何提交前，先确认 `SecurityToken=` 为空。** **⚠ 原判据 `SecurityToken=.` 已被实测证伪（假阳性），不得再用** —— 改用下面的严格口径：
     - **正确口径（两条必须同时成立才算安全）**：① `SecurityToken=([^\r\n]*)` **捕获组长度 = 0**；② **全文 32 位十六进制串命中数 = 0**。
     - **⚠ 错误口径的根因（2026-09-12 实测，非推断）**：`Config/DefaultEngine.ini` **全文 CRLF（242 个 CRLF / 0 个裸 LF）**，而正则 `.` **会匹配 `\r`** ⇒ 等号后的行尾 `\r` 被当成「值」，**空值被误报为「非空」**，会让提交无谓中止。**对照实验**：同一模式在 **LF 化的 HEAD blob** 上命中 = **0** ⇒ 命中物是 CR，不是值。
     - **复核位置**：在**索引 blob / HEAD blob** 上做，**不要只看工作区文件**（工作区可被编辑器随时重写）。
     - **通用教训**：**凡用 `.` 或 `\s` 匹配行尾内容的判据，必须显式排除 `\r`，或改用 `[^\r\n]*`。**
  2. **`Config/DefaultEngine.ini` 出现在 `git status` 时，先看它改了什么再决定是否入库**；**编辑器保存造成的注释丢失属预期现象，据实记录，不要「顺手还原」**（还原会被下次保存再删，产生无谓 churn）。
  3. **启用 AFS 前必须先轮换密钥**，不得复用已泄露的历史值。
- **结构性修复（未实施，待立项）**：把 `^SecurityToken=.+` 纳入提交前拦截（`pre-commit` 钩子或门禁检查项），**不再依赖本条纪律**。**注意 `check-integrity.py` 当前处于封版状态**（`77269 B` / `SHA256 A280C20A67AA533904BFA0BBEE04F95246D8C5AB5C9489209AB0479ECB244792`），**加检查项须走变更申请**。

## 决策授权（2026-09-12 用户裁定）

**用户原话**：「**其实 git 推送，我觉得可以你自己来定，对于我来说，只要做的东西不会丢失，有版本管理就 OK 了**。」

- **已下放给决策侧**：**常规治理 / 文档改动的提交与推送** —— 决策侧自行判断，**不再逐次请示**。
- **未下放（仍必须用户逐项批准）**：**删除任何文件或内容**、**范围变更**、**破坏性操作**、以及**任何可能造成「东西丢失」的动作**。
- **判据 = 用户给出的那一条**：**做的东西不丢失 + 有版本管理**。凡一次操作**可能违反这一条**，即回到请示。
- **推论（务必遵守）**：**「能推」不等于「能删」** —— 推送**可逆**（git 有历史），删除**不可逆**（尤其被 `.gitignore` 忽略的目录，删除**既不留痕、也检测不出**，见 `registers/11-tech-debt-register.md` **TD-017**）。**两者授权等级不同，不得互相推导。**

### 何时推送（推送决策 · 2026-09-12 用户裁定「就这么定」）

**目的**：让**新决策模型无需询问即可自行判断**何时推、何时必须先问、何时一律不推。**本小节是「何时推」的唯一权威正文**（「怎么推」见本节其余部分）。

| 情形 | 授权 |
|---|---|
| **治理 / 文档 / 规则 / 登记册 / CHANGELOG / 会话记录 / CR** | **决策侧自行判断，可直接推** |
| **工程资产**（`Content/`、`Source/`、`Config/`、`Plugins/`） | **必须先问用户** |
| **任何删除、范围变更、里程碑验收结论** | **必须先问用户** |
| **清单外 `M` 类文件** / **门禁非 `EXIT=0`** / **含密钥凭据** / **含 `Saved/` 等生成目录** / **目标文件正在被写入** | **一律不推** |

**⇒ 放行前提（每次推送均须满足，无一例外）**：① 门禁**提交前后各一次** `EXIT=0`；② 清单**固定且逐条点名**（**严禁 `git add -A` / `.` / `-u`**）；③ 暂存集**严格等于清单**（显式断言）；④ **三方同 SHA**（本机 == `origin/master` == 干净浅克隆）；⑤ 报告**分两层**（备份层 = 对象到达 origin / 验收层 = CI 绿），**不得用一层替代另一层**。
**⇒ 与「唯一权威副本」联动（`AGENTS.md` 规则 29–32）**：**推送是"防丢"的唯一手段** —— **推送可逆、删除不可逆**，**两者授权等级不同，不得互相推导**（见上「推论」）。

## 活资产只读白名单（AGENTS.md 规则 33 的细节与工具）

**规则正文只在 `AGENTS.md` 规则 33；本节是它的清单与工具落点。**

### 永远不得置只读的资产

| 资产 | 说明 |
|---|---|
| `Content/VRSanguo/Dev/L_SkeletonTest.umap` | M01-T001 关卡 |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap` | M01-T005 坛景关卡 |
| `Content/VRSanguo/VR/BP_VRCharacter.uasset` | 角色蓝图（输入 / 手指弯曲落点） |
| `Content/VRSanguo/VR/BP_VRGameMode.uasset` | 游戏模式蓝图 |
| `Content/VRSanguo/VR/Mesh/`（整目录） | 含环首刀两版，握持 socket 落点 |
| `Content/VRTemplate/Input/`（整目录） | 含 5 个 IMC 输入映射 |

### 工具层

项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\` 下两个脚本内置同一白名单，**`-Restore`（重锁）跳过白名单**：

- `Unlock-TraeAssets.ps1` —— 目标 `Content/VRTemplate/Input`、`BP_VRCharacter.uasset`
- `Unlock-GripPolish.ps1` —— 目标 `Content/VRSanguo/VR/Mesh`、`L_SkeletonTest.umap`

**2026-09-13 修复两处缺陷**（原文件备份 `.bak-20260913`）：

1. **`-ErrorAction SilentlyContinue` 误传原生命令。** 该参数是 PowerShell 公共参数，`attrib.exe` / `icacls.exe` 不解析，会被原样当作 argv 传入 ⇒ 命令报「unknown option」失败，而 `| Out-Null` 吞掉报错 ⇒ **脚本照常打印 `LOCKED`/`UNLOCKED` 而实际什么都没做**（共 4 处：两脚本各 2 处）。**修法**：去掉该参数，改用 `Invoke-Native` 检查 `$LASTEXITCODE`。
2. **无回读断言。** 声称成功必须证明成功。**修法**：每次操作后复读 `IsReadOnly`，与期望不符即 `throw`。

**⇒ 归族**：两处缺陷与 `judgement-discipline.md` §3.22 同族 —— **机制不同（原生参数误传 + 管道吞错），后果相同（声称成功而实际失败）**。
