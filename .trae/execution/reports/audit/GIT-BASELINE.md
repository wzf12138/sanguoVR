# GIT-BASELINE.md — t10 Git 基线提交与推送 origin

- 任务：t10（implementation round 1）｜执行者：git-operator｜attempt 1
- 放行依据：指挥台《放行令 · t10 执行 Git 基线提交 + 推送 origin》（2026-09-10）
- 事实源模型：唯一工作目录 `D:\AWork\Unreal\Project\VRSanguoYanWuchang` + 该目录内 Git（master）；**备份 = 推送 origin**；全程**不创建任何本地备份副本**（无 robocopy / 无 bundle / 无镜像 / 无第二工作目录），**不在 E: 新建任何文件或目录**。
- 本文件自身**未纳入本次基线**（自我描述悖论：基线报告无法记录它自己所在的提交），故结束后为未跟踪状态，见 §3.2。

> 本文件所有数值均为**落地当刻实测值**，不引用对话函件中的旧值。三元组格式 = (字节数, SHA256[:16], mtime)，见 §13。

---

## 0. 结论：两层口径

| 层 | 判据 | 本次结论 |
|---|---|---|
| **备份层**（对象是否到达远程） | 本地 HEAD = origin/master = `ls-remote origin refs/heads/master` 三者同一 SHA；`git lfs push --all origin` 报无待上传对象 | **已完成** — 三者同为 `f2550366827a717575332bed6a93c56d42c71f9c`；LFS 9/9 对象（29 MB）已上传；补跑 `lfs push --all` exit=0 且无 Uploading 输出 |
| **验收层**（`governance/SessionCommands.md:113–120`） | 两条 workflow 均 `completed` + `success`，且步骤级无失败 | **已核验通过** — 见 §9。本次 CI **实测全绿**（不是「已知红」豁免路径）。 |

**声明**：验收层是**已核验**状态，非「未核验」。若未来 Actions 不可达，按指挥台口径只能写「已推送，CI 未核验」，不得写「完成」；本次不适用该分支。

---

## 1. 基线快照（任何写入之前）

| 项 | 值 |
|---|---|
| 分支 | `master` |
| 起始 HEAD | `eb319c3689458d7b1a61d1798adfc5ea8df0c494`（2026-09-04 21:12:49 +0800） |
| 起始 origin/master（缓存 ref） | `eb319c3689458d7b1a61d1798adfc5ea8df0c494` |
| `git status --porcelain=v1` | 50 行 |
| `git status --porcelain=v1 -uall` | 72 行 |
| `git ls-files` 计数 | 1269 |
| `git lfs ls-files` 计数 | 367 |
| stash | 0 |

**E 类预检（写操作前复跑，按放行令 §一）**

```
$ git -c http.proxy=http://127.0.0.1:7897 ls-remote --symref origin HEAD
ref: refs/heads/master	HEAD
eb319c3689458d7b1a61d1798adfc5ea8df0c494	HEAD
exit=0
```

代理端口 7897 确在监听（`LISTEN :::7897 pid=30200`）。直连不可达（t1 结论，本任务未复跑直连，按放行令不空推）。

---

## 2. 暂存集合：由路径清单定义，不由计数定义

**显式路径 52 条 → 实际暂存 58 文件**（`.trae/execution/reports/audit/` 为目录路径，递归展开为当时实际的 7 个文件 —— 与 t9 §4.3 F12 所述机制一致）。

```
$ git add -- <52 条显式路径>
git add exit=0
$ git diff --cached --name-only | Measure-Object
58
$ git diff --cached --name-status | 状态字母分布
A x26   D x2   M x30     （合计 58）
```

**禁止项**：全程未使用 `git add -A` / `git add .` / `git add -u`；未使用 `git checkout` / `restore` / `reset` / `clean` / `stash`。

### 2.1 记录删除（2 条，按指挥台 R2 裁定随基线提交）

```
D	Content/VRSanguo/Dev/L_Prototype_1v1.umap
D	Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap
```

二者**在本次任务开始前就已从磁盘消失**（起始 `git status` 即显示 ` D`，任何本任务写入之前）。裁定依据为 M01-T005 note「v1/v2/v3 按用户决定删除（脚本在外可重生）」，**不是丢失**。LFS 历史对象仍可回溯（指挥台已实测本地对象命中）。**未做任何「恢复文件」动作。**

### 2.2 `.gitignore` 增补（只增不减）

增补片段（t9 §5.1，追加至文件末尾，现有 93 行未动）：

```
# AI tool session runtime (not project content)
.agent-teams/
.dsh-uploads/
```

| 增补行 | 理由 | 当前是否被跟踪 | 副作用 |
|---|---|---|---|
| `.agent-teams/` | DSH 团队运行态，含 57 处本机绝对路径（规则23 形态）；每次通信都变，提交无意义且制造噪音 | 目录内**另有 4 个旧文件已被跟踪**（`296ebed`），本次未暂存、未被修改，故不影响基线后变干净 | 仅阻止**新增**未跟踪文件入库；对已跟踪的 4 个无效（彻底脱管须 P1，需用户批准，**本次未做**） |
| `.dsh-uploads/` | 会话上传中转，含 3 个文件 / 3,105,958 B（其中 2 张 `com.limelight.root` 手机截图，含个人设备隐私） | 0 个 | 3 个文件转为已忽略，**本地文件原样保留** |

**生效验证**（`check-ignore -q`，exit 0 = 已忽略）：

```
exit=0  .agent-teams/vrsanguo-audit-backup/team.json
exit=0  .dsh-uploads/session-2a22b421-.../693ce656e56ba26e-deepseek-whale-400.png
exit=1  Docs/Scene/scene_topdown.png            <- 仍未被忽略（本轮靠路径清单排除，非靠 gitignore）
exit=1  Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap
```

编码保真：增补前/后均 **BOM=False**，换行风格由 93×LF 保持为 96×LF（未引入 CRLF），且以换行结尾。写盘用 `[System.IO.File]::WriteAllText` + `UTF8Encoding($false)`，未使用 `Set-Content`。

---

## 3. E 类排除与残留

### 3.1 暂存自检（硬停判据）——通过

```
$ git diff --cached --name-only | Where-Object { .agent-teams/ 或 .dsh-uploads/ 或 Docs/ 前缀 }
E-CLASS HITS = 0
```

判定口径按放行令 §七：**真正的失败判据是 E 类被暂存/被提交**，而不是「`git status` 为空」。**未触发硬停。**

`Docs/Scene/` 5 个未跟踪文件的排除方式（未纳入暂存）与 t9 记载一致，未出现需停机的不符。

### 3.2 提交后残留（预期，非失败）

```
$ git status --porcelain=v1 -uall
?? Docs/Scene/asset_checklist.md
?? Docs/Scene/scene_modules.json
?? Docs/Scene/scene_overview.md
?? Docs/Scene/scene_plan.html
?? Docs/Scene/scene_topdown.png
（共 5 行；` M` / ` D` 行数 = 0）
```

- 5 项全部为 `Docs/Scene/` —— 按指挥台更正裁定**本次基线不入库**，属**预期残留**。
- `.agent-teams/`、`.dsh-uploads/` 已不再出现在 `-uall` 输出中（已被新增忽略规则覆盖）。
- **本文件 `GIT-BASELINE.md` 自身**为第 6 个未跟踪项（§0 声明），属自我描述悖论，非「本应入库」内容；其归属建议由 t12 裁定。

**审计说明（诚实登记）**：`audit/` 在 t5 冻结快照中记为 `t9 = 96,309 B @23:08:20`，本任务落地时实测已为 `96,426 B @23:14:11`（即快照之后又有一次写入）。按放行令 §十「用你当刻实测值」，本任务提交的是**提交时刻的实际 7 个文件**，未引用任何预测数字。

---

## 4. v5 SHA256 守卫（唯一守卫；尺寸绝不可当守卫）

目标：`Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap`（仅此一个文件）。

| 时点 | 字节数 | SHA256 | mtime |
|---|---|---|---|
| `git add` **之前** | 673326 | `63AFECDF89DA19C8FC6A316DDF8D0A868FC04ED7215CA7D94F3A470BBE7A9BD6` | 2026-09-10 21:44:17 |
| `commit` **之前** | 673326 | `63AFECDF89DA19C8FC6A316DDF8D0A868FC04ED7215CA7D94F3A470BBE7A9BD6` | 2026-09-10 21:44:17 |
| 推送完成后复测 | 673326 | `63AFECDF89DA19C8FC6A316DDF8D0A868FC04ED7215CA7D94F3A470BBE7A9BD6` | 2026-09-10 21:44:17 |

- **自比（硬停判据）**：两次一致 → **未触发硬停**。
- **与审计基线比对**：`63AFECDF…BE7A9BD6` 逐字符相同 → **自审计以来未变**，无需报告差值。
- 未使用文件大小作为守卫。

---

## 5. 规则23 提交内容自查（四项逐条）

| 项 | 核查方式 | 结论 |
|---|---|---|
| **密钥 / 凭据** | 对待提交集合的 46 个文本文件跑正则（`sk-` / `ghp_` / `AKIA` / 私钥块 / `xox[baprs]-` / `AIza` / `glpat-` / `password\|api_key\|secret\|token\s*[:=]`），另由 `check-integrity.py` 的「无密钥令牌泄漏」项复算 | **1 命中，经核实为既有项、非本次引入** —— `Config/DefaultEngine.ini:168 SecurityToken=28DADB…A1A48A2`，属 UE **Android File Server** 运行时设置（`bIncludeInShipping=False`）。`git show HEAD:Config/DefaultEngine.ini` 显示该行**已存在于 HEAD**（即已在 origin 公开历史中），本文件本次 diff 为 2 增 1 删、**与 Token 无关**。→ 本次提交**未新增任何凭据**。**建议**：单独立项（CR）评估是否将其改为本机私有配置或轮换，**本任务未做任何改动**。 |
| **本机路径凭据** | 含 57 处绝对路径的 `.agent-teams/` 已整目录排除（§3.1 零泄漏） | **通过**（就本任务可控范围）；仓库既有文本（STATUS.json note、会话记录）普遍含本机路径，属 t9 D20 待裁定的**适用范围**问题，本任务未改口径 |
| **UE 生成目录** | 暂存集合中无 `Binaries/`、`Intermediate/`、`Saved/`、`DerivedDataCache/`、`.vs/` | **通过**（生成目录均已被既有规则忽略） |
| **大型非 LFS 二进制** | 对暂存文件逐个 `check-attr filter` + 尺寸统计 | **通过** —— ≥1 MB 的非 LFS 文件 = **0**；≥5 MB 的非 LFS 文件 = **0**。全部大文件均为 LFS：`环首刀.uasset` 28,041,121 B、`v5.umap` 673,326 B、`v4.umap` 509,749 B 等。暂存合计 30,565,548 B（29.15 MB） |

---

## 6. 本地治理门禁（提交之前实跑）

命令（绝对路径解释器；Windows 需 UTF-8，否则 GBK 控制台在打印符号时崩溃）：

```
$env:PYTHONIOENCODING='utf-8'
& 'D:\App\trae\Traedata\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe' -B -X utf8 dashboard/check-integrity.py
```

| 指标 | 实测 |
|---|---|
| **exit code** | **0** |
| 末段汇总 | `总计: 25 项  通过: 25  失败: 0` / `✓ 全部校验通过` |
| 污染检查 | `git status --porcelain -uall` **63 → 63（POLLUTION = 0）**；`git status --porcelain -- dashboard` **为空** |

与指挥台 §二所述「25/25、exit=0」**独立复现一致**。本次未重跑 `dashboard/generate-static.py`（按放行令要求）。

---

## 7. 提交

```
$ git commit -m "chore(baseline): 审计基线提交 — 盘点报告 + 治理同步 + .gitignore 增补" -m "..."
[master f255036] chore(baseline): 审计基线提交 — 盘点报告 + 治理同步 + .gitignore 增补
 58 files changed, 6914 insertions(+), 162 deletions(-)
commit exit=0
```

- 新 HEAD：`f2550366827a717575332bed6a93c56d42c71f9c`（提交时间 2026-09-10 23:53:00 +0800）
- 提交者：`WZF12138 <1429540285@qq.com>`（仓库既有身份，未改动）
- **提交内容只反映磁盘现状**；除 `.gitignore` 外未对任何被提交文件做内容编辑。
- **提交后未自动追加第二次提交**；且 ` M` 行数 = 0，**未出现需二次提交的「提交后落盘」证据**（该硬停条件未触发）。

---

## 8. 推送与推送后核验

```
$ git -c http.proxy=http://127.0.0.1:7897 push origin master
Uploading LFS objects: 100% (9/9), 29 MB | 2.9 MB/s, done.
To https://github.com/wzf12138/sanguoVR.git
   eb319c3..f255036  master -> master
push exit=0
```

- **仅推送一次**；未 force、未重推、未推 `main`。
- 代理**仅以 `-c` 内联参数生效**，**未写入任何持久 git 配置**（未执行 `git config http.proxy`）。

| 核验项 | 命令 | 结果 |
|---|---|---|
| 三方 SHA 一致 | `git rev-parse HEAD` / `git rev-parse origin/master` / `git ls-remote origin refs/heads/master` | 三者同为 `f2550366827a717575332bed6a93c56d42c71f9c` |
| LFS 无待上传 | `git lfs push --all origin` | exit=0，**无 Uploading 输出**（证明对象确已在远程） |
| LFS 计数对比 | `git lfs ls-files \| Measure-Object -Line` | 提交前 **367** → 提交后 **369**（+4 新增 LFS 文件 −2 删除 LFS 文件 = +2，闭合） |
| 跟踪文件计数 | `git ls-files \| Measure-Object -Line` | 提交前 **1269** → 提交后 **1293**（+26 新增 −2 删除 = +24，闭合） |
| LFS 完整性 | `git lfs fsck` | `Git LFS fsck OK`，exit=0 |
| 对象完整性 | `git fsck --no-progress --no-dangling` | **无输出、无 error**，exit=0 |
| 对象库 | `git count-objects -vH` | in-pack 2335；pack 178.19 MiB；`prune-packable 0`；`garbage 0` |

---

## 9. 验收层：GitHub Actions 核验（`SessionCommands.md:113–120`）

经代理调用匿名 API（`-Proxy http://127.0.0.1:7897`），匹配本次 head_sha `f255036`：

| workflow | run id | 任务级 status | 任务级 conclusion |
|---|---|---|---|
| 治理校验 CI 门禁 | 34498608200 | completed | **success** |
| 看板部署 | 34498607791 | completed | **success** |

**步骤级复核（按放行令 §八，针对 `deploy.yml:30 continue-on-error: true`）**：

```
JOB integrity-check status=completed conclusion=success
   step#1 Set up job              success
   step#2 Run actions/checkout@v4 success
   step#3 安装依赖                 success
   step#4 治理一致性校验（严格模式）     success
   step#8 Post Run actions/checkout@v4  success
   step#9 Complete job            success

JOB deploy status=completed conclusion=success
   step#1 Set up job              success
   step#2 Run actions/checkout@v4 success
   step#3 安装依赖                 success
   step#4 运行治理一致性校验（报告模式）  success
   step#5 生成静态看板             success
   step#6 准备部署目录             success
   step#7 上传 Pages 产物          success
   step#8 部署到 GitHub Pages     success
   step#16 Post Run actions/checkout@v4 success
   step#17 Complete job            success
```

**关于 `continue-on-error` 掩盖风险的确定性排除**：`.github/workflows/ci.yml:27-28` 的「治理一致性校验（严格模式）」**没有** `continue-on-error`，即 `check-integrity.py` 一旦非零退出该 job 必然失败。该 job 实测 `completed/success` → **CI 中该脚本 exit=0 得证**（与 §6 本地 exit=0 相互印证）。故 `deploy.yml` 那个被容忍的步骤是否成功已不影响结论。

**步骤日志取证受限声明（不修饰）**：`GET /actions/jobs/{job_id}/logs` 返回 **403 Forbidden**（该端点需认证），因此**未能**直接读取 CI 原始日志。上述结论建立在「任务级 + 步骤级 conclusion + 严格模式无豁免」三重证据上，**不是**基于日志原文。此限制如实登记。

`看板部署` 与 `治理校验 CI 门禁` 的触发路径为 `.trae/**`、`dashboard/**`，本次提交含这两类路径，故确有触发（run 创建时间 2026-09-10T15:53:38Z = 本地 23:53:38）。

---

## 10. ⚠ 编辑器事件（重要发现，须指挥台裁定）

**事实**：`UnrealEditor` **pid 24284 在任务开始时存活，任务结束时不复存在。**

| 时点 | 观测 |
|---|---|
| 任务基线（本任务写入之前） | `Get-Process -Id 24284` → `Id=24284 ProcessName=UnrealEditor StartTime=2026/9/9 22:06:05 Responding=True` |
| 任务结束 | `Get-Process -Id 24284` → **Cannot find a process**；`Get-Process -Name UnrealEditor` → **无任何结果** |

**退出性质 = 有序正常关闭，非崩溃**（`Saved\Logs\VRSanguoYanWuchang.log` 尾部逐行）：

```
[2026.09.10-15.52.59:664] LogExit: Transaction tracking system shut down
[2026.09.10-15.53.00:466] LogExit: Object subsystem successfully closed.
[2026.09.10-15.53.00:925] LogMCPBridge: [UE-MCP] Bridge server stopped
[2026.09.10-15.53.03:103] LogExit: Exiting.
Log file closed, 09/10/26 23:53:03
```

配套关闭痕迹：`Saved\Config\WindowsEditor\EditorPerProjectUserSettings.ini` @23:53:03、`Saved\Autosaves\PackageRestoreData.json` @23:52:59、`Saved\AutoScreenshot.png` @23:52:57。Windows 应用程序事件日志中**无任何 UnrealEditor 相关崩溃事件**。

**因果说明（不推诿、不臆断）**：本任务全程只执行 git 命令、文件读取/哈希、以及一次只读 Python 门禁脚本与 HTTP 查询；**未调用任何进程终止/重启手段**（无 `Stop-Process`、无 `taskkill`、无编辑器桥控制调用），也未运行 `rebuild_*.py`。上述有序关闭序列（含 MCP 桥正常停服、对象子系统正常关闭）**不可能由 git/文件操作产生**。退出时点（23:53:03）与提交时点（23:53:00）相邻，但两者无因果路径。

**对交付的影响（已核验为零）**：关闭只写入了 `Saved/`（已被 `.gitignore` 覆盖），提交后 `git status` 中 ` M` / ` D` 行数 = **0**；v5 三元组自始至终未变。→ **基线提交仍然准确反映磁盘现状，推送成果不受影响。**

**仍需指挥台裁定的事项**：
1. t2 记录的两条冻结令（重建冻结、重启窗口冻结）以「编辑器存活」为前提，该前提现已失效；
2. 编辑器关闭后 `Binaries\Win64\*.dll|pdb`、`Intermediate\Build\...` 出现 23:54:02–03 的写入（均在 gitignore 覆盖范围内，**对仓库零影响**），推测为热重载/构建活动，**本任务未触发亦未干预**；
3. 若需重新进入「需要关闭编辑器」的清理项（P6/P6a/P12），当前状态**恰好满足前置条件** —— 是否利用由指挥台/用户决定，**本任务不擅自推进**。

---

## 11. acceptance 逐条对照

| # | 验收条款 | 结论 | 证据 |
|---|---|---|---|
| 1 | push 成功；本地 HEAD / origin/master / `ls-remote` 三者同一 SHA | **passed** | §8：三者同为 `f2550366827a717575332bed6a93c56d42c71f9c`；push exit=0 |
| 2 | LFS：`lfs fsck` 通过；`lfs push --all` 无待上传；前后计数对比 | **passed** | §8：`Git LFS fsck OK`；`lfs push --all` exit=0 无输出；367 → 369 |
| 3 | `git fsck` 无 error；提交后无「本应入库」的未跟踪内容 | **passed** | §8 fsck exit=0 无输出；§3.2 残留仅 5 项 `Docs/Scene/`（按裁定排除，属预期）+ 本报告自身 |
| 4 | 提交自查：无密钥/凭据、无本机路径凭据、无 UE 生成目录、无大型非 LFS 二进制 | **passed**（含 1 项既有披露） | §5：非 LFS ≥1 MB = 0；`DefaultEngine.ini` 的 AFS Token 系 **HEAD 既有**、本次未引入，已披露并建议立 CR |
| 5 | 未在唯一工作目录之外创建任何文件或目录 | **passed** | §12 三处顶层条目前后完全一致（E:\AWork 3 项 / E:\AWorkBackup 0 项 / D:\AWork\TraeAdmin 1 项）；本任务未在 E: 建任何东西，也未使用临时目录 |
| 6 | 未删除任何项目内容 | **passed** | 提交后 ` D` 行数 = **0**（若本任务删过文件必然在此显现）；提交内的 2 条 `D` 在任务起始基线即已存在，属用户既定决定（R2） |
| 7 | 全程无非交互挂起 | **passed** | 全程 `GIT_TERMINAL_PROMPT=0` 且 `GIT_ASKPASS=''`；所有命令均返回；无认证提示；push 一次成功 exit=0 |
| 8 | 编辑器 pid 24284 任务前后仍存活 | **failed** | 任务开始时存活（Id/StartTime/Responding 已取证）；**结束时该进程不存在**。非本任务所致（有序关闭、无崩溃、本任务无任何进程干预手段）—— 详见 §10 |
| 9 | `.gitignore` 只增不减；每条增补给理由；忽略项未被提交 | **passed** | §2.2：93 → 96 行，仅追加 2 条规则 + 1 行说明；`check-ignore` exit=0；E 类暂存命中 0 |
| 10 | 遇「需用户逐项批准」动作即停并报告，不代替用户批准 | **passed** | 未执行 P1（`git rm --cached`）、P13（删 v4 关卡）、P12（证据转正）、P6/P6a 等任何需批准动作；未删除任何项目文件 |

> 依契约「completed 仅当成功标准全部满足」，**因第 8 条未满足，本任务不予声明 completed**（不把未完成项包装为遗留待办）。其余 9 条均有原始输出支撑。

---

## 12. 未在唯一工作目录之外创建任何文件/目录 —— 前后对比

| 位置 | 任务前顶层条目 | 任务后顶层条目 | 一致 |
|---|---|---|---|
| `E:\AWork` | `Temp` / `Tools` / `VRExpansionPlugin` | `Temp` / `Tools` / `VRExpansionPlugin` | ✅ |
| `E:\AWorkBackup` | （0 项） | （0 项） | ✅ |
| `D:\AWork\TraeAdmin` | `VRSanguoYanWuchang` | `VRSanguoYanWuchang` | ✅ |

未移动、未删除、未改名上述任一位置的既有内容；`D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\` 存在但**本任务未向其写入任何文件**（全程未使用临时文件）。

---

## 13. 落地当刻三元组（字节数, SHA256[:16], mtime）

| 文件 | 字节数 | SHA256[:16] | mtime |
|---|---|---|---|
| `.gitignore` | 1405 | `66D08B6836224717` | 2026-09-10 23:51:45 |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap` | 673326 | `63AFECDF89DA19C8` | 2026-09-10 21:44:17 |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap` | 509749 | `120E7F15DC5E53DD` | 2026-09-10 15:07:13 |
| `.trae/execution/reports/audit/t9-cleanup-and-retention-plan.md` | 96426 | `7EEBA5D0AA475561` | 2026-09-10 23:14:11 |
| `.trae/execution/reports/audit/AUDIT-repo.md` | 59603 | `E011D131321A7239` | 2026-09-10 22:57:22 |
| `.trae/execution/reports/audit/t5-verification.md` | 103094 | `229113A0A29A6C3C` | 2026-09-10 23:07:20 |
| `.trae/CHANGELOG.md` | 118700 | `34C5E76F64D41554` | 2026-09-10 23:43:25 |
| `AGENTS.md` | 9641 | `9C558FE2186073ED` | 2026-09-10 23:41:37 |
| `audit/` 目录实时文件数 | 7 | — | — |

---

## 14. 未做 / 开口声明

1. **顺序差异（继承指挥台 §十一）**：t9 L652「本地清理与修改（P1–P19）在推送之前完成」在本会话**未成立**，由指挥台裁定保留为已知差异、交由 t12 声明。本任务按放行令执行推送，**未因此停工**。
2. **未执行**：P1 / P6 / P6a / P12 / P13 及其他「需用户逐项批准」动作；未删任何项目文件；未改 `Content/`、`Config/`、`Source/`、`Plugins/` 内容（仅暂存其既有改动）；未改治理正文、登记册、STATUS.json；未跑 `rebuild_*.py`；未写 E:。
3. **未核验**：CI 步骤原始日志（403 需认证），见 §9 受限声明。
4. **待裁定**：§10 编辑器事件与两条冻结令前提失效；§3.2 本报告自身的入库归属；§5 既有 AFS Token 的处置。

---

*本文件由 t10 执行者 git-operator 生成；唯一写入路径 `.trae/execution/reports/audit/GIT-BASELINE.md`，未纳入本次基线提交。*

## 15. Attempt 2 复验（重派后的幂等核对，全程只读）

本任务被重派为 **attempt 2**。因 **attempt 1 已完成提交与推送**，本次**未执行任何写操作** —— 未 git add、未 git commit、未再次推送、未修改任何项目文件、未改 .gitignore。
依据：放行令明文「推送成功即停止，**禁止自动追加第二次提交/重推**」；重做不仅违反该禁令，且不产生任何新增信息（提交已存在于 origin）。

### 15.1 幂等复验（全部为只读命令，实测输出）

| 核验项 | 实测值 | 与 attempt 1 一致性 |
|---|---|---|
| git rev-parse HEAD | `f2550366827a717575332bed6a93c56d42c71f9c` | 一致 |
| git rev-parse origin/master | `f2550366827a717575332bed6a93c56d42c71f9c` | 一致 |
| git ls-remote origin master（经代理） | `f2550366827a717575332bed6a93c56d42c71f9c`	refs/heads/master（exit=0） | **三者同一 SHA**，远程基线仍在 |
| git ls-files 计数 | 1293 | 一致 |
| git lfs ls-files 计数 | 369 | 一致 |
| git lfs fsck | Git LFS fsck OK（exit=0） | 一致 |
| git lfs push --all origin | exit=0，**无任何 Uploading 输出** | 一致：确无待上传 LFS 对象 |
| git fsck --no-progress --no-dangling | 无输出、无 error（exit=0） | 一致 |
| git count-objects -vH | count 145 / 747.92 KiB / in-pack 2335 / pack 178.19 MiB / **prune-packable 0 / garbage 0** | 一致 |
| v5 三元组 | 673326 B / 63AFECDF89DA19C8…BE7A9BD6 / 2026-09-10 21:44:17 | **自 attempt 1 起始终未变** |
| E:\AWork 顶层 | Temp / Tools / VRExpansionPlugin | 一致 |
| E:\AWorkBackup 顶层 | （0 项） | 一致 |
| D:\AWork\TraeAdmin 顶层 | VRSanguoYanWuchang | 一致 |
| 工作区文件数（不含 .git） | 20757 | 相对 attempt 1 的 20756 **恰好 +1**，即本报告文件自身；**无任何文件消失** |

### 15.2 残留集合（相对 attempt 1 无新增）

```
 M .trae/execution/sessions/session-20260830-001.md      <- 其它会话写入，本任务 out-of-scope
?? .trae/execution/reports/audit/GIT-BASELINE.md          <- 本报告自身
?? Docs/Scene/{asset_checklist.md,scene_modules.json,scene_overview.md,scene_plan.html,scene_topdown.png}
```

-  M 行的写入方仍是**另一会话**（M01-T001 执行会话），**不在本任务 inScope**（契约明确将 .trae/execution/sessions/ 列为 out-of-scope）→ 本次**未处置、未提交**，保持原样。
- 5 项 Docs/Scene/ 为既定例外裁定（不入库），属预期残留。

### 15.3 attempt 2 的操作边界声明

- 只读命令：git rev-parse / git ls-remote / git status / git ls-files / git lfs ls-files / git lfs fsck / git lfs push --all（无待上传对象时为纯查询）/ git fsck / git count-objects / Get-ChildItem / Get-Process / Get-FileHash。
- 唯一写入 = **本报告文件自身的追加**（.trae/execution/reports/audit/GIT-BASELINE.md），位于 inScope 路径内，且为未跟踪文件，**对仓库状态零影响**。
- 未触碰 Content/、Config/、Source/、Plugins/、Docs/、.trae/governance/、.trae/registers/、.trae/knowledge/、.trae/execution/active/、.trae/execution/sessions/；未写 E:；未写 C: 或用户主目录；未使用任何临时文件。

### 15.4 状态判定

attempt 2 开始时 Get-Process -Id 24284 与 Get-Process -Name UnrealEditor **均无结果** —— 编辑器在**本次尝试开始之前**即已不存在（其关闭时间与成因见 §10，为外部有序关闭）。因此 acceptance 第 8 条「编辑器 pid 24284 在任务**前后**仍存活」在本次尝试中**同样无法满足**（前后皆不存在），**仍记为 failed**，不写作通过。

除第 8 条外，其余 9 条在 attempt 2 中均**再次独立复核为 passed**（见 §15.1 与 §11）。

**处置建议（供指挥台裁定，二选一）**
- **(A) 认定第 8 条因外部原因作废**：该进程的关闭由其它会话按既定计划执行（§10 已附 UE 有序关闭日志与会话记录原文），本任务无任何进程干预手段。若采纳，请据此将 t10 判为通过，并在 t11/t12 的交接中记录「编辑器存活前提自 2026-09-10 23:53:03 起失效」。
- **(B) 要求字面满足**：待编辑器重启后告知，我可在 5 分钟内完成一次最小复验（Get-Process -Id <新 pid> 前后各一次 + 三条 SHA + v5 三元组），据实补记。

在指挥台裁定前，t11/t12 不具备「第 8 条已满足」的前提，**不应据此推进**。

---

*§15 由 t10 attempt 2 追加；追加前文件 22217 B / 351 行。*
## 16. 指挥台裁定记录（2026-09-11 凌晨）—— 本节结论优先于 §11 第 8 条与 §15.4

指挥台对 t10 两份报告的 findings 作出裁定如下，逐条照录并在本报告内生效。**本报告 §11 第 8 条的 failed 判定与 §15.4 的二选一建议，均被本节取代。**

### 16.1 F1（编辑器判据）—— 判据由规划方承担，本任务无过错

> `acceptance` 第 8 条写的是「编辑器 pid 24284 任务前后仍存活」。这条判据**是规划期定的，形状错了**：它把「另一个会话对世界做了什么」当成了 t10 的成败条件。正确的判据应当是对 **t10 自身动作**的否定式检查 —— 「t10 未终止编辑器」，而这一条已由完整证据链满足。

据此，**第 8 条规范含义 = 「t10 未终止编辑器」→ 满足（passed）**。其字面事实同时照实保留：

- 规范层（满足）：本任务全程只执行 git 命令、文件读取/哈希、只读门禁脚本与 HTTP 查询，**无任何进程终止手段**（无 Stop-Process、无 `taskkill`、无桥控制调用），亦未运行 `rebuild_*.py`。
- 事实层（外部事件）：该进程已于 **2026-09-10 23:53:03** 被**外部会话有序关闭**，非本任务所致。证据链：UE 日志 LogExit: Transaction tracking system shut down → Object subsystem successfully closed → Bridge server stopped → LogExit: Exiting. → Log file closed 23:53:03；Windows 事件日志**无崩溃记录**；另一会话 23:56:29 的会话记录载明「明早顺序：重开编辑器+桥探活」。

**t10 终态据此重报为 completed。**

### 16.2 F2（session-20260830-001.md 的 +10 行）—— 由指挥台收敛

> 该 10 行**不单独提交**，由指挥台今晚的合并提交一并收敛。停下来报告是正确的行为。

本任务对该 out-of-scope 路径**未处置、未提交**，维持原样。

### 16.3 F3（AFS SecurityToken）—— 同意立 CR，处置方向 = 轮换，不改历史

Config/DefaultEngine.ini:168 的 UE AndroidFileServer SecurityToken 立项 CR，方向已明确：

- 该值**已存在于 eb319c3**，即 **2026-09-10 本次提交之前就已在公开 origin 历史里** → **本次推送未新增任何暴露**。
- 补救手段 = **轮换 Token**（使已泄露值作废）+ 使其不再进入版本控制。
- **明确不走「改写历史 + 强制推送」路线** —— 与项目红线（禁 force push）冲突，且对一个已公开的旧值收益为零。
- CR 须写清：暴露时间窗、影响面（AFS 为**局域网调试文件传输通道**）、轮换步骤、以及「历史里的旧值不追改」的理由。

### 16.4 GIT-BASELINE.md 归属 —— 允许存在

> 审计目录冻结的意图是**冻结 scout 的盘点报告作为证据**，不是禁止任务交付物写入合同指定路径。它是 t10 契约 step 7 的产物，属**交付物**，不是审计发现。它没进本次基线是对的（自我描述悖论），将进入指挥台今晚的合并提交。

### 16.5 两条冻结令（仅通报，本任务不执行）

编辑器已关闭，两条冻结令的前提确实失效；但：

- **重建冻结继续有效** —— `rebuild_v5.py` 一跑就会覆盖现存的 120m 校场，而 120m 口径本身仍在等用户裁定。
- **Docs/Scene/ 冻结继续有效** —— 属 E 类不入库，无需改动。

本任务对此**未采取任何动作**（未跑 `rebuild_v5.py`、未改写 Docs/Scene/）。

### 16.6 重报后的 t10 终态

**completed** —— 未重新提交、未重新推送（按裁定二，禁止再跑任何 git 写操作）；已推送对象仍为 `f2550366827a717575332bed6a93c56d42c71f9c`，本地 HEAD = origin/master = ls-remote 三方同一 SHA，全程未被触碰。

---

*§16 由 t10 执行者 git-operator 追加；追加前文件 26765 B / 407 行。*
## 17. 口径修正（t13 repair round 2 · 2026-09-11 00:1x）—— **本节结论取代本报告 §0 与 §11 关于「推送即备份」的口径**

本节回应 t11 审查报告（.trae/execution/reports/audit/t11-review.md，判定 
eeds_revision）。**t11 的核心事实复核结果：成立。** 以下为据实修正，**不辩解、不淡化**。

### 17.1 口径降级（三级，全部区分开）

| 层级 | 原口径 | **修正后口径** | 证据 |
|---|---|---|---|
| 对象层 | 「推送即备份」 | **「远程已建立基线；但该基线 ≠ 当前工作目录」** | 提交建树于 **23:53:00**；工作区此后持续被改写 |
| 完整性 | 隐含「工作目录完整快照」 | **「远程持有 23:53:00 时刻的受管快照；此后新增的改动尚未入库」** | 见下表 19 个受管文件 |
| E: 侧 | 「E: 无有效**完整**备份（不完整）」 | **「E: 上不存在任何项目备份（彻底没有）」** | §17.3 |

**截至本次实测（2026-09-11 00:1x），工作区已有 19 个受管文件晚于基线提交**（t11 采样时为 15 个，**仍在增长**）：

```
 M .trae/CHANGELOG.md                                    M .trae/standards/05-event-and-interface-standard.md
 M .trae/execution/M01-CombatSlice.md                    M .trae/standards/06-performance-standard.md
 M .trae/execution/sessions/session-20260830-001.md      M .trae/standards/09-content-and-historical-style-standard.md
 M .trae/governance/SessionCommands.md                   M .trae/standards/10-git-standard.md
 M .trae/index.md                                        M .trae/systems/02-interaction-and-weapon-system.md
 M .trae/integrity.yaml                                  M .trae/vr/03-hand-grab-and-haptics.md
 M .trae/registers/04-requirement-traceability-register.md  M .trae/vr/05-spatial-ui-tutorial-and-accessibility.md
 M .trae/registers/07-task-register.md                   M dashboard/check-integrity.py
 M .trae/registers/11-tech-debt-register.md
 M .trae/skills/three-kingdoms-vr-arena/SKILL.md
 M .trae/standards/02-naming-and-path-standard.md
```

另有 **9 项 ?? 未入库**：4 项应入库（GIT-BASELINE.md、`t11-review.md`、CR-20260911-001-governance-consistency-repair.md、CR-20260911-002-android-file-server-token.md）+ 5 项 Docs/Scene/（裁定不入库）。

**「补提交」列为待办**：这 19 个受管文件 + 4 项交付物的当期版本**仅存在于本地磁盘**，远程只有其被提交时的旧版本（或完全没有）。**在该补提交完成前，本节起不得再使用「推送即备份」这一表述。**
（**合规说明**：t10 未追加第二次提交符合指挥台预置裁定「提交后新出现的  M 不自动二次提交，如实记录」—— 本项**不是对 t10 的越界指控**，是目标口径必须修正。）

### 17.2 门禁复跑（t13 要求）—— **结论：门禁当前无法运行，故对当前状态不存在任何「全绿」声明**

> **【§18.1 标注 · 2026-09-11 —— 本条已失效，不得被下游当作当前状态证据引用】**
> 本节结论**仅是对 `dashboard/check-integrity.py` 在 2026-09-11 **00:08:48** 版本（**73,880 B / SHA256 `FC533DB90E79A839F16C61A164651E9DCB9F1446F94C5FF1AF987DFC317731FD`**）的一次快照**。该版本**已被在办者重写取代，缺陷亦已修复**。
> **正确引用方式**：只能作为「00:08:48 版本当时崩溃」的**历史记录**引用；**不得据此推断当前门禁状态**。
> **当前状态请改引 §18.2**（**74,566 B / SHA256 `4D6D6D308AD9CB29ECBA4DFBD9D9410E18A793BAC62B21C811A09B2FF0ACC315`**，exit=0）。

| 项 | 实测值 |
|---|---|
| 命令 | & <python> -B -X utf8 dashboard/check-integrity.py（cwd = 项目根） |
| 解释器 | D:\App\trae\Traedata\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe，**Python 3.10.11** |
| 脚本版本（运行**前**） | **73,880 B @ 2026-09-11 00:08:48，SHA256 FC533DB90E79A839F16C61A164651E9DCB9F1446F94C5FF1AF987DFC317731FD** |
| 脚本版本（运行**后**） | 同上，**hash 未变** → 结果可归因于该版本 |
| **EXITCODE** | **1** |
| 输出 | **仅 6 行，未完成任何检查项** |
| 异常 | UnboundLocalError: local variable 'yaml' referenced before assignment @ check-integrity.py:1698（main() 由 L1724 调用） |

**根因（已定位到行）**：main() 内 **L1704 import yaml** 与 **L1707 yaml = None** 使 yaml 成为 main() 的**局部名**，而 **L1698 if yaml is not None:** 在该局部名赋值之前读取它 → UnboundLocalError。main() 开头（L1689）只声明了 global YAML_ERROR，**未声明 global yaml**。
**一行修复方向**：L1689 改为 global YAML_ERROR, yaml（**本任务不改 —— dashboard/ 不在 t13 inScope**，仅报告）。

**归属（对照 HEAD，非基线引入）**：
- HEAD 版本 dashboard/check-integrity.py = **718 行**，第 16 行为模块级 import json, os, re, sys, yaml，**不含** if yaml is not None（计数 0），**无此缺陷**。
- 工作区版本 = 1724 行（git diff --numstat = +1123 / −117），**含**该缺陷（计数 1）。
- → **该缺陷由提交之后的重写引入**，基线自身的门禁版本结构完好。

**因此（本报告的关键修正）**：
1. **t10 报告中的「门禁 exit=0 / 25 项全过 / 零污染」只覆盖 23:5x 的脚本版本，不覆盖当前工作区** —— t11 对该证据失效的判断**成立且被本次复跑坐实**（不只是「版本漂移」，是**当前版本直接崩溃**）。
2. 在当前版本修复前，**任何以 check-integrity.py 退出码为依据的「合规」或「CI 必绿」推断都不得成立**。
3. **未运行 HEAD 版本作为对照**：把它复制到项目外执行会使脚本的 TRAE_ROOT（基于 __file__ 解析）指向错误位置，**产生假阴性**；故我据静态对照（行数 / 模块级 import / 缺陷计数）判定，并**明确声明这是静态结论而非执行结论**。

**附带证明（门禁是只读的）**：运行前后 git status --porcelain=v1 -uall **均为 28 行且逐条一致**（Compare-Object 无差异）→ 该脚本的崩溃**未污染工作区**。

### 17.3 E: 现场 —— 事实陈述（**非 t10 违约**，归属已严格分界）

```
E:\AWorkBackup                            EXISTS=True  TYPE=DIR  TOP_ENTRIES=0  RECURSIVE_FILES=0
                                          LastWriteTime = 2026-09-10 23:19:56
                                          CreationTime  = 2026-09-01 22:11:14
E:\AWorkBackup\VRSanguoYanWuchang          EXISTS=False  (ABSENT)
E:\AWork                                  EXISTS=True  TEMP | TOOLS | VREXPANSIONPLUGIN
```

- **事实**：E:\AWorkBackup 目录本身仍在（CreationTime 未变），**其内容已被清空**，最后写盘 **2026-09-10 23:19:56**。t1/t3 曾实测的 VRSanguoYanWuchang\（1,929 文件 / 631 MB，含 08-31 的 UEBridgeMCP.disabled-old）**已不存在**。
- **归属（严格分界，不推定）**：该时刻 **23:19:56 早于** t10 的提交（23:53:00）与推送（23:53:35）；且 t10 的**任务开始快照与结束快照都显示该目录已是空**（我的两次 Get-ChildItem E:\AWorkBackup -Force 均返回 0 项）—— 即**该删除在 t10 开始之前就已发生，t10 侧不可见，本任务全程亦无任何 E: 写操作**。→ **不是本基线/推送任务所为。**
- ~~**无法归因**：无审计日志可锚定何进程；$RECYCLE.BIN 存在不等于可归因（该不确定性原样保留）。~~
  **【更正 · 依指挥台裁定 · 见 §18.4】上述「无法归因 / 不明灭失」的表述<u>不成立</u>，系我越过证据边界**：`E:\AWorkBackup` 的清理是**用户裁定项的执行结果**（t9 的 P7；`t12-inputs-t5-corrections.md:402` 记「删掉 ✅ 已执行」），**不是不明灭失**。我的实测只能证明「早于 t10、非本任务所为」，**据此断言归因不明属过度推断** —— 缺的正是这条授权链。**独有内容是经授权清理，不是意外损失**，故本节原先基于「若独有内容随之灭失」的紧迫性论证相应降级；「尽快补齐未入库改动」的理由改为**纯粹的事实性缺口**（那批改动仅存在于本地磁盘），不再依赖该事件。
- **对用户目标的口径改写（按 t13 要求）**：「E: 上不存在任何**有效完整**项目备份」**强度不足** → 正确表述为「**E: 上不存在任何项目备份**」。团队「远程即唯一备份」的论断**不仅合理，且是当前唯一可行的完整备份形态**。
- **紧迫性**：若 08-31 UEBridgeMCP.disabled-old 等独有内容随之灭失，则**其唯一可回退载体已灭失**。→ **这抬高了尽快补齐 §17.1 那 19 个受管文件 + 4 项交付物的紧迫性**（补提交 = 当前唯一能把这批改动落进远程的手段）。

### 17.4 规则23「大」的阈值 —— **请指挥台裁定**（finding 标记 `resolved:false`：裁定未做出，非执行者未修）

**同一目录、同一基名的对照硬证据（排除一切争议）**：
```
check-attr filter  Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_02.uasset -> filter: lfs
cat-file -s HEAD:…/REF_Weapon_Shield_02.uasset                                                -> 132 B   (LFS 指针)
check-attr filter  Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_02.png    -> filter: unspecified
cat-file -s HEAD:…/REF_Weapon_Shield_02.png                                                   -> 4,590,192 B (仓库内真实二进制)
```

**清点**：Content/VRSanguo/Art/References/Weapon/ 受管 **47 文件 / 96,234,850 B（91.8 MB）**；其中**非 LFS 且 ≥900 KB = 18 个 / 46,337,015 B（44.2 MB）**，全部为武器参考图 PNG（1.06–4.59 MB）。

**问题**：此前「>5MB 的非 LFS 受管文件为 0」这一数字**属实但属阈值产物** —— 换 ≥900KB 口径即得 18 个。**「0 命中」不能继续被当作「不违反规则23」的证明。**
**请求裁定**：规则23 的「大」**是否含 MB 级 PNG**？
- 若**含** → 转 **CR（.gitattributes 补 *.png）**，**不是**改写历史（改写历史 + 强推与项目红线冲突，且对已公开内容收益为零）。
- 若**不含** → **应在判据里写明阈值**，使「0 命中」成为可复核的判定而非偶然结果。
**本任务不改 .gitattributes**（不在 inScope；且属 CR 范围）。

### 17.5 (a)(b) 两项确认

**(b) Docs/Scene/ 5 文件 —— 确认「未被任何忽略规则覆盖」（两项独立证据一致）**
```
git check-ignore -v --no-index -- Docs/Scene/scene_topdown.png   -> 无输出，exit=1（无规则匹配）
git status --porcelain=v1 -uall                                   -> 仍以 "?? Docs/Scene/…" 出现（未被忽略）
```
→ 它是**显式白名单排除**的结果，**不是忽略保护**的结果。**下游不得误以为它受 .gitignore 保护** —— 一旦有人改用 git add -A/git add .，这 5 个文件**会**被加入。（对照：.agent-teams/ 与 .dsh-uploads/ 才是真忽略态。）

**(a) GIT-BASELINE.md 未蒸发**：实测仍在，**30,618 B @ 00:01:08，SHA256 D98FE1892115C519A479057A3D9477B34BCAEB0EEA4D884B0C549052427C517D**。按指挥台裁定其属交付物、随合并提交入库 —— 此处仅作确认。

### 17.6 .agent-teams/ 4 个已跟踪文件 —— 仅登记，本轮不动

```
.agent-teams/archive/vrsanguo-survey/inbox/captain.jsonl
.agent-teams/archive/vrsanguo-survey/inbox/qa.jsonl
.agent-teams/archive/vrsanguo-survey/team.json
.agent-teams/retired-members.json
```
**忽略已生效**：git check-ignore -v --no-index .agent-teams/retired-members.json → .gitignore:95:.agent-teams/ 命中。
**但库内 4 个文件仍在**（忽略规则**不会**自动取消跟踪）。依 t9 §2 R1，其 git rm --cached 属**需用户批准的 P1**，**本轮不动**，待用户批准后处置。

> **仪器更正（本任务踩到并已更正的第二个坑，必须沉淀）：git check-ignore 不带 --no-index 时，对【已被跟踪】的文件返回 exit=1（不匹配）**—— 因为默认会跳过索引中已跟踪的路径。若据此判定「忽略规则没生效」即为误判。本任务首轮对 .agent-teams/retired-members.json 正是得到 exit=1，**加 --no-index 后立刻得到规则命中行**。（第一个坑：手写 cat-file HEAD:<path> 漏了 Weapon/Shield/ 一层目录而报「does not exist in HEAD」—— 系我方路径笔误，非仓库问题；改用 ls-files 原样输出后得 **4,590,192 B** 的真实值。**两次都靠第二种方法复核才发现。**）

### 17.7 本任务未做的动作（逐项声明）

未 git add / commit / push / `rebase` / stash；**未二次提交、未重推**；**未改 .gitignore**（见下）；未改 dashboard/（不在 inScope，**只报不改**）；**未改 Content/**（用户红线；Content/VRSanguo/Art/References/Weapon/ 仅只读核查，**零写入**）；未改 .trae/execution/reports/audit/t11-review.md（**属 verifier 的审查报告，执行者不宜改写**）；未在 E: 新建/移动/删除/改名任何内容；未碰编辑器（Get-Process -Id 24284 → 不存在）；未跑 `rebuild_*.py`；未改写 Docs/Scene/；未使用任何临时文件。
**.gitignore 无需增补**（保持 **96 行 / 1,405 B / SHA256 66D08B6836224717622F73ABC2C2860970DA11B7C821D3A962A9C21DD49C7234** 不变）：E 类两目录已覆盖；Docs/Scene/ 属显式白名单排除（非忽略）；CR 与交付物属**应入库**内容而非应忽略内容 —— 无可增项。

---

*§17 由 t13（git-operator）追加；追加前文件 30618 B / 457 行。*
### 17.8 观测序列 —— 「漂移未收敛」的直接证据（为收尾时序提供依据）

| 采样时点 | 来源 | 受管  M 文件数 |
|---|---|---|
| 2026-09-11 00:0x | t11-review.md F-1 | **15** |
| 2026-09-11 00:1x | 本任务首轮快照 | **19** |
| 2026-09-11 00:1x（数分钟后） | 本任务复查 | **21**（新增 .trae/governance/ExecutionModel.md、.trae/knowledge/EnvironmentSetup.md） |

**含义（供收尾裁定）**：同一时段内漂移**在审查进行期间仍持续增长**。**只要其它会话仍在写治理文件，「补提交」就无法在单一时点收敛** —— 补提交完成的一刻就会立即落后于新写入。
→ **建议：由指挥台先冻结治理写入窗口，再执行补提交**；否则「补提交」本身会重复陷入同一状态。
**另**：`t11-review.md` 于 00:10:52 由 20,176 B 增至 26,327 B（verifier 正在修订），**t11 结论以其最新版为准**。**本报告 §17.1 的「19」与本节一致，均为带时刻的采样值，不是固定常量。**

---

*§17.8 由 t13 追加。*

---

## 18. t15（repair round 3）记录 —— §17.2 失效标注 + 门禁最终态运行证据 + 引用纪律

### 18.1 §17.2 失效标注（t15 acceptance 1）

- 已在本文件 **§17.2 标题下**加注失效标注，声明其**仅为 00:08:48 版本的快照结论**、**不得作为当前状态证据**、当前状态改引 §18.2。
- **根因方向予以保留**（模块级 import 与局部赋值遮蔽）。**独立佐证**：当前代码**自身注释**（**L1717-1719**）载明「本函数内**不得**再出现 `import yaml` 或对裸名 yaml 的赋值——那会把 yaml 变成 main() 的局部变量、遮蔽模块级导入，并在未走到赋值分支时抛 UnboundLocalError（**2026-09-11 实发事故**）」，与 §17.2 的判定一致。
- **据实更正（契约引用的行号已不对应）**：t15 契约引用的 **L128 / L135** 与 **L1722-1723**，在当前版本**均不对应** —— 当前 **L132** 是 `global YAML_ERROR`、**L133** 是 `if yaml is not None`、注释在 **L1717-1719**、`main()` 的 yaml 处理已抽到模块级 **L120-138 的 `ensure_yaml_ready()`**。原因是**修复方案本身在两次重写之间改变了**（由「main() 内局部别名」改为「抽出模块级函数，`main()` 内彻底不出现裸名 `yaml`」）。→ **这恰是 §18.3 引用纪律所针对的问题：行号不是稳定标识符。**

### 18.2 门禁运行证据（t15 acceptance 2）—— **首次真实运行 = exit 0**

| 项 | 值 |
|---|---|
| 版本（运行**前**） | **74,566 B @ 2026-09-11 00:13:16，SHA256 `4D6D6D308AD9CB29ECBA4DFBD9D9410E18A793BAC62B21C811A09B2FF0ACC315`** |
| 版本（运行**后**） | **同上，hash 未变** → 结果可归因于该版本 |
| 命令 | `python -B -X utf8 dashboard/check-integrity.py`（Python **3.10.11**，cwd = 项目根） |
| **EXITCODE** | **0** |
| 结果 | **30 项：通过 27 / 警告 3 / 失败 0**，收尾行为 `全部校验通过，有 3 项警告（不阻断）` |
| 只读性 | 运行前后 `git status --porcelain=v1 -uall` **逐条一致** → 门禁**未写盘** |

**3 项警告（全部为既存治理漂移，非本次引入，且不阻断）**：
1. `integrity.yaml 链接计数一致` —— 缺 scope，无法判定 checked（声明 163，脚本全量实测 163）。
2. `五件套结构（根↔目录↔taskId↔ALLOWLIST）` —— **6 条历史路径引用**：M00-T005 / M00-T006 的白名单路径不存在（含 `Plugins/UEBridgeMCP/**` 5 条）。
3. `根 ↔ 任务包 STATUS.json 镜像` —— **3 条副本字段漂移**：M00-T004 `claimedBy`；M01-T001、M01-T005 的 `updatedAt` 副本滞后。

> **效力声明（照录 t15 口径：结构判断 ≠ 运行证据）**：上表是**我方一次真实运行的原始结果**，已钉版本哈希。**若指挥台在其冻结的最终版本上复跑且哈希与此不同，以指挥台那次为准**；**本表不得被用作「验收已通过」的依据**。

### 18.3 引用纪律（t15 acceptance 3）—— 只引字节数 + SHA256，不引行数

- **方法论点**：**行数不是跨工具可比的量**（不同工具对末尾换行、CRLF、折叠的计数不同）；**引用行数时必须同时给出字节数或哈希**。
- **本文件身份链（每次改动必须递补，否则同一哈希会被引向不同内容）**：

| 修订 | 字节数 | SHA256 | 状态 |
|---|---|---|---|
| §0–§16（t10 交付） | 30,618 B | `D98FE1892115C519A479057A3D9477B34BCAEB0EEA4D884B0C549052427C517D` | 已被 §17 取代 |
| §17（t13 追加） | **43,982 B** | **`3BAA0CF56B2F364F32CB9222B4BB0B5A13418FE041C9D97B151D8B70E57D04DD`** | t15 起始时**双重吻合**（字节+哈希实测一致，见 §18.5） |
| §18（t15 追加，本修订） | 见 §18.5 | 见 §18.5 | **当前** |

- **为何必须递补**：acceptance 1 要求**修改本文件**，而 acceptance 3 把本文件**钉在 43,982 B / `3BAA0CF5…`** —— 两者**只有在「发布新哈希 + 显式登记 old→new 迁移」时才能同时成立**。故在此登记该迁移，并声明：**自本修订起，`3BAA0CF5…` 标识 §17 版本，不再标识当前文件。**

### 18.4 E: 口径（t15 acceptance 4）—— **无本轮动作**

- 按「**E: 上已无任何备份（彻底没有）**」口径收录，由 **t12 交接清单**承接，并说明由此抬高补齐未入库改动的紧迫性。
- **归属更正（依指挥台裁定，已在 §17.3 内联标注）**：该清理是**用户裁定项的执行结果**（t9 的 P7，`t12-inputs-t5-corrections.md:402` 记「删掉 ✅ 已执行」），**不是不明灭失**。我在 §17.3 写「无法归因」**属越过证据边界**——实测只能证明「早于 t10、非本任务所为」。
- **不重建该目录**（红线：不得在 E: 新建任何文件或目录）。本轮对 `E:\AWorkBackup` **零动作**，仅只读登记其当前为 0 项。

### 18.5 本修订身份 + 未做动作声明

- **本修订的字节数与 SHA256 在写入完成后实测，并发布于 t15 任务记录与指挥台回报** —— **不写入本文件内部**：自指悖论（任何写入内部的值在写入完成时即已失效）。§17 头部同理。
- **t15 起始时的双重吻合复核（实测）**：`GIT-BASELINE.md` = **43,982 B**，SHA256 = **`3BAA0CF56B2F364F32CB9222B4BB0B5A13418FE041C9D97B151D8B70E57D04DD`** → 与 acceptance 3 引用的值**逐字符一致**。
- **未做动作**：未 `git add` / `commit` / `push`（指挥台放行前零写操作）；**未修改 `dashboard/check-integrity.py`**（仅**运行**它，且已证明其只读——`dashboard/` 的修复属门禁加固子任务，非本任务）；未改 `Content/`（变更 = 0）；未改 `.gitignore`（仍 1,405 B / `66D08B68…`）；未改 `Docs/Scene/`；未在 E: 新建/移动/删除/改名；未碰编辑器（pid 24284 已不存在）；未跑 `rebuild_*.py`；未使用临时文件。

---

*§18 由 t15（git-operator）追加。*
### 18.6 本交付物自身的仪器缺陷与修复（据实披露，不掩饰）

- **缺陷**：本文件 **§16 与 §17** 系由 **PowerShell 双引号 here-string** 生成，而 PowerShell 的反引号是**转义字符**——每个反引号都会**吞掉其后一个字符**。后果有两类：
  1. **11 处行内代码跨度被破坏为不可见控制字符**：`CR`×6（→ `rebuild_v5.py`、`resolved:false`、`rebase`）、`TAB`×3（→ `taskkill`、`t11-review.md`）、`BEL`×1 与 `FF`×4（→ 一个 SHA 与 `acceptance`）。
  2. **§16 与 §17 的其余行内代码跨度被剥掉反引号、退化为纯文本**（**语义无损，仅格式差异**）—— 见下方量测。
- **机制复现（已实测，非推测）**：`"A`f255036B` C`t11-review D`r"` → `A<FF>255036B C<TAB>11-review D<CR>` —— **开闭两枚反引号被同时吞掉**，故不闭合的代码跨度正是该机制的指纹。
- **已修复**：**13 组替换 + 逐组断言匹配数**（12 组×1 + 1 组×2），全部命中后才落盘。修复后**控制字符仅剩 5 个 TAB，且全部来自粘贴的 git 原始输出**（`ls-remote` / `refs` 分隔符），其余为 **0**；`U+FFFD` 恒为 0。
- **未修复（据实保留）**：§0–§17 其余行内代码跨度的反引号**无法逐一定位还原**，保留为纯文本。**语义与数值未受影响** —— 全部 SHA、字节数、路径、命令均逐字符可用。**§18 起改用单引号 here-string**（无反引号转义），实测该区段控制字符数 = **0**。
- **量测对照（实测）—— 并据此撤回我先前的推断**：行内反引号密度 = **§0–§15 21.5/千字符（378 个行内跨度，完全未受损）**、**§16 6.0**、**§17 5.4**、**§18 24.6**（§18 为单引号 here-string 基准）。→ **受损区段是 §16 与 §17，不是全部**。我在本节上一稿写「§0–§17 系由双引号 here-string 生成、其余行内跨度全部退化为纯文本」**属未经验证的推断，现予撤回** —— 这正是 t15 要根除的那类表述。
- **教训沉淀（第三个已实测陷阱）**：**凡含反引号代码跨度的中文交付物，一律用单引号 here-string 或文件 API 写入；双引号 here-string 只可用于无反引号的文本。**（前两个陷阱见 §17.6：`check-ignore` 对已跟踪文件须加 `--no-index`；手写 `cat-file HEAD:<path>` 会因路径笔误假报不存在。）

---

*§18.6 由 t15 追加。至此本文件全部内联标注与披露完成。*