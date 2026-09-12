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

## 推送

### `推送` / `上传git` / `git push`

> **硬性门禁**：推送前必须完成以下全部检查，任一未通过则不得推送。

**推送前必检清单**：

1. **运行一致性校验**：执行 `$env:PYTHONIOENCODING='utf-8'; & 'D:\App\trae\Traedata\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe' -B -X utf8 dashboard/check-integrity.py`（本机 Python **不在 PATH 上**，必须用绝对路径；缺 `PYTHONIOENCODING` 时输出含 `⚔` 等字符会抛 `UnicodeEncodeError: 'gbk' codec`）。确认 `exit=0`。**注（2026-09-11）**：本条原写「技术债 open 数 >3 的警告可豁免，但需在提交信息中注明」，与 `:95` 的「校验未通过仍推送」禁令**互相矛盾**，且当前 `open` 恰为 3、**无任何余量**。在用户裁定前**按较严读法执行**：`open >3` 即视为校验未通过，不得推送，须先偿还或降级为 `deferred`；确需豁免时必须先立变更申请，写明豁免理由与到期复审时点。
2. **同步 integrity.yaml**：确认 `updated` 日期为当天，`active_tasks` 列表与根 `STATUS.json` 一致，`limitations` 反映最新验证状态。
3. **同步 manifest.yaml**：确认 `updated` 日期为当天，`active_gate.task_packages` 与根 `STATUS.json` 一致。
4. **同步登记册**：`07-task-register.md` 中各任务状态与根 `STATUS.json` 一致。
5. **生成看板**：执行 `$env:PYTHONIOENCODING='utf-8'; & 'D:\App\trae\Traedata\TRAE SOLO CN\ModularData\ai-agent\vm\tools\python\python.exe' -B -X utf8 dashboard/generate-static.py`，确认 `status.json`/`integrity.json`/`index.html` 已更新。
6. **CHANGELOG 完整**：本次会话所有变更已记录在 `.trae/CHANGELOG.md`。

**执行流程**：

```
1. check-integrity.py         → 校验通过
2. 逐项核对 integrity/manifest/登记册/CHANGELOG
3. generate-static.py          → 看板生成
4. git add -- <逐条显式路径>     （禁止 git add -A / . / -u）
5. git commit -m '<描述>'
6. git push origin master
```

**暂存纪律（2026-09-11 固化）**：**禁止 `git add -A` / `git add .` / `git add -u`**。暂存集合必须由**显式路径清单**定义，逐条 `git add -- <path>`。理由：本仓库存在必须排除在外的 E 类条目（`.agent-teams/`、`.dsh-uploads/`、`Docs/`），`-A` 会把它们一并入库；且**计数不可作为判据**——「暂存文件数」与「路径清单条数」本就不等（一个路径可含多个文件），唯一判据是「E 类路径命中数 = 0」。另注：**`git status --porcelain` 期望为空不是有效判据**，`Docs/Scene/` 等被裁定排除项会永久保留 `??` 行。

**禁止**：跳过校验直接推送；校验未通过仍推送；推送后不确认远程同步成功。

**推送卡住时的网络恢复流程**（**本项目已实测的常态：直连超时、经代理可达**——2026-09-10 实测直连 `github.com:443` 会超时（`git ls-remote` 120 秒无返回），而经 `127.0.0.1:7897` 代理**同一时刻 `git ls-remote` exit=0**、`Invoke-WebRequest -Method Head` 返回 HTTP 200。因此**直连失败不得直接判为「网络不可达」**，必须先走本流程。本流程是推送命令权威正文的组成部分）：

症状：`Failed to connect to github.com port 443 ... timed out` 或 `Recv failure: Connection was reset`。

1. **TCP 短超时探测连通性**。不要用 `Invoke-WebRequest` 判断连通性（不可靠），用 TcpClient：

   ```powershell
   $c = New-Object System.Net.Sockets.TcpClient
   $iar = $c.BeginConnect('github.com', 443, $null, $null)
   if ($iar.AsyncWaitHandle.WaitOne(5000, $false) -and $c.Connected) { '可达' } else { '不可达' }
   $c.Close()
   ```

2. **不可达或可达但 git 连接被重置/超时（TLS 层被掐）**：先试**单次借用本地活代理**推送（2026-09-03 首次实证、2026-09-10 再次实证均一次通过）：`git -c http.proxy=http://127.0.0.1:<活端口> push origin master`——仅本次命令生效，**禁止写入持久 git 配置**（严禁 `git config http.proxy`）。随后检查常见本机代理端口（7890 / 7897 / 10809 / 1080 / 8118）是否监听，再查 Windows 系统代理开关（注册表 `ProxyEnable`）。全部关闭时如实报告"网络未恢复"，停止反复空推，等用户确认网络后再试。**顺序说明**：既然「直连超时、代理可达」是本项目实测常态，当症状为 443 超时时**可直接先试代理端口**，不必先凑满 2 次直连失败。
3. **可达但 git 仍失败**：把「探测 → 成功才执行 `git push origin master`」写成临时 PowerShell 脚本循环执行：最多 30 次、每次探测超时 5 秒、间隔 60 秒，成功立即退出。脚本放系统临时目录，用完删除，绝不进项目。
4. **脚本陷阱**：以 `-File` 方式运行时，双引号字符串内的 `$变量` 可能不展开——脚本内的路径、次数、间隔一律硬编码字面量，复杂逻辑写 `.ps1` 文件而非 `-Command` 行内执行。
5. **成功后核验 Actions（强制，2026-09-04 固化）**：推送完成 ≠ 任务完成。本仓库公开，匿名 API 可查（60 次/时限，勿高频轮询）：

   ```powershell
   $r = Invoke-RestMethod 'https://api.github.com/repos/wzf12138/sanguoVR/actions/runs?per_page=6'
   $r.workflow_runs | Select-Object -First 4 | Format-Table name, head_sha, status, conclusion -AutoSize
   ```

   以本次推送的 head_sha（`git rev-parse --short=7 HEAD`）匹配的两个 workflow（治理校验 CI 门禁、看板部署）均 `status=completed` 且 `conclusion=success` 为准；未完成则间隔 15 秒轮询，上限 3 分钟。**全绿才报"推送完成"**；任一 `failure` → 本地复现 `python dashboard/check-integrity.py` → 修复 → 提交重推 → 重新核验（CI 历史红记录不追改，新提交绿即闭环）。API 不可达（限流/断网）时如实报告"未能核验 Actions"，请用户在 GitHub Actions 页面确认。最后删除临时脚本。

   **判据补充（2026-09-11）**：
   - `.github/workflows/ci.yml:27-28` 的严格模式**没有** `continue-on-error`，因此该 job `conclusion=success` **等价于** `check-integrity.py` 在 CI 内 `exit=0`——这是「验收层真绿」的确定性判据，不是「已知红豁免」。
   - 步骤级原始日志端点需认证（实测返回 **403**）。读不到日志原文时，**不得**把结论写成「已核验 CI 日志」，只能写「任务级 + 步骤级 conclusion + 严格模式三重」，并显式登记该证据限制。
   - **「推送完成」必须分两层报告，不得用一层替代另一层**：备份层 = 对象是否真的到达 origin（`git ls-remote` 实测同 SHA、LFS 对象上传、`lfs fsck` OK）；验收层 = CI 是否绿（任务级**与**步骤级均 success）。只绿一层时必须写明缺哪一层。
   - **（2026-09-11 新增，有事故溯源）「本地绿 ≠ CI 绿」——门禁必须在干净检出下复跑一次才算绿。**
     事故：提交 `cb7ab79` 在本机项目根跑出 `EXIT=0`（30 项 / 通过 27 / 警告 3 / 失败 0），**同一提交**在 Actions 判 `failure`（run `34501489803`，步骤级 `治理一致性校验（严格模式）=> failure`）。根因**不是仓库缺陷**：五件套白名单检查把**通配项** `Intermediate/**`、`Binaries/**`、`Saved/**`、`DerivedDataCache/**` 也当作「必须存在的路径」去判，而这些全是 `.gitignore` 的**可再生构建产物目录，干净检出里必然不存在** → 同一份白名单在开发机是 warn、在 CI 变 fail。
     **判据（固化）**：白名单里的**通配项是权限范围（该任务可写哪些路径），不是存在性断言**——只对**具体路径**做存在性判定。要求 CI 先做一次构建才让通配项成立，是错误语义。
     **硬要求**：宣称门禁绿之前，除本机项目根外，**必须在项目外干净浅克隆里跑同一条命令并得 `EXIT=0`**：

     ```powershell
     $env:GIT_LFS_SKIP_SMUDGE='1'
     git -c http.proxy=http://127.0.0.1:7897 clone --depth 1 --branch master https://github.com/wzf12138/sanguoVR.git <项目外临时目录>
     # 在该克隆根执行：python -B -X utf8 dashboard/check-integrity.py  → 期望 EXIT=0
     ```

     注意两点：① 浅克隆里 `Content/**` 的 LFS 文件是**指针文件**（存在但非真实内容），涉及 LFS 真实内容的判定另论；② 该复现克隆属**临时产物**，放项目外临时目录，用完删除。

   **判据补充（2026-09-12，有事故溯源）**：

   - **⚠ 跨本地零点提交前，必须先确认 CHANGELOG 顶部日期 ≥ 当日。**
     事故：提交 `4b89763` / `d9fac2a`（committer 时间 `2026-09-12 00:00:33` / `00:00:56`，**跨零点**）推送后，「CHANGELOG 不滞后于提交」判 **失败**（detail：`顶部条目 2026-09-11，HEAD 提交 2026-09-12`），**本机项目根、项目外干净浅克隆、CI（run `#36`/`#37`）三处同时红**。
     根因：该判据的输入之一是 **HEAD 自身的提交日期**（`git log -1 --format=%cs`，见 `dashboard/check-integrity.py:783-806` 的 `top >= head`）⇒ **任何跨零点后的提交都会自我判红，且提交前那一跑必然绿、无法预知。**
     **⇒ 这是「本地绿 ≠ CI 绿」的一个自指分支：绿的前提被「提交」这个动作本身破坏。**
     **做法**：跨零点提交前先补写**当日如实条目**（记录当日实际发生的事）再提交。**判据不放宽、不加特例；为过检而改写日期数字属造假，禁止。**
   - **⚠ LFS 完整性不得以 `git lfs push --all` 的输出为空作判据。**
     事故：提交 `4b89763`/`d9fac2a` 的两个 LFS 新对象（28,880,650 B），`git push` 无 `Uploading LFS objects` 行、`lfs push --all origin` **连跑两次均 0 行**，但**干净浅克隆内 `git lfs fetch origin --include=<路径>` 实测取回 3 个对象、落地字节与指针 size 逐一精确相符** ⇒ 远端其实**完整**。
     **⇒ 「输出为空」既可能是真阴性也可能是假阴性，二者无法由该输出区分。**
     **做法**：**唯一可靠判据 = 第二种方法** —— 在**干净克隆**内实测 `lfs fetch` 并核对**落地字节数**；配合 `git lfs fsck` OK 与三方同 SHA（`HEAD` = `origin/master` = `git ls-remote`）三者并列陈述。详见 `registers/11-tech-debt-register.md` **TD-018**。
   - **⚠ 工具的自报聚合数字不可作判据。** 同批实测：`git lfs checkout` 自报 `Checking out LFS objects: 100% (369/369), 197 MB`，而**实际仅 3 个被实体化、366 个仍为指针**。凡「已删除 / 已通过 / 已完整」的结论，**必须回读现场**（目录计数、字节数、内容检索），不得引用工具自报。

## 安全默认

## 决策授权（2026-09-12 用户裁定）

**用户原话**：「**其实 git 推送，我觉得可以你自己来定，对于我来说，只要做的东西不会丢失，有版本管理就 OK 了**。」

- **已下放给决策侧**：**常规治理 / 文档改动的提交与推送** —— 决策侧自行判断，**不再逐次请示**。
- **未下放（仍必须用户逐项批准）**：**删除任何文件或内容**、**范围变更**、**破坏性操作**、以及**任何可能造成「东西丢失」的动作**。
- **判据 = 用户给出的那一条**：**做的东西不丢失 + 有版本管理**。凡一次操作**可能违反这一条**，即回到请示。
- **推论（务必遵守）**：**「能推」不等于「能删」** —— 推送**可逆**（git 有历史），删除**不可逆**（尤其被 `.gitignore` 忽略的目录，删除**既不留痕、也检测不出**，见 `registers/11-tech-debt-register.md` **TD-017**）。**两者授权等级不同，不得互相推导。**

### AFS 密钥（`Config/DefaultEngine.ini` 的 `SecurityToken`）—— 无自动兜底，必须人工把守（2026-09-12 探针实证）

- **现状**：`SecurityToken=` 为**空值**；真实取值在项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\keys\afs-security-token.txt`（不进仓库，823 B）。**该值未轮换**，且在历史提交中仍可检索到 —— 动作性质是「**停止继续泄露**」，不是「已消除暴露」。
- **⚠⚠ 门禁抓不到它（2026-09-12 探针实证，非推断）**：`dashboard/check-integrity.py` 的密钥扫描（`check_secret_patterns`，检查项 17）**只匹配厂商格式**（`ghp_…` GitHub、`xox…` Slack 等，见 `check-integrity.py:846-847`）。**把 `SecurityToken=` 填成 32 位十六进制串后，门禁仍判 `30 项 / 通过 29 / 警告 1 / 失败 0 / EXIT=0`**（探针用假值，已即时还原）。该检查的 detail 文本已显式声明覆盖边界并指向 `execution/CR-20260911-002-android-file-server-token.md`。
- **⚠ 编辑器会吃掉该文件里的注释（2026-09-12 事故）**：`4b89763` 在 `DefaultEngine.ini` 写入的 4 行密钥警示注释，**被编辑器于 2026-09-12 10:50:08 重写该文件时整段删除**（`SecurityToken=` 空值行保留）。⇒ **该文件中的人工警示不是持久防护**，且每次编辑器保存都会产生一次「看起来像改动」的 diff。
- **⇒ 由此成立的完整风险链**：本机启用 AFS → 按注释把 token 填回 → 编辑器保存 ini → `git add Config/` → **提交泄露，且没有任何自动检查会拦住。**
- **人工纪律（在轮换或结构性修复落地前，必须执行）**：
  1. **任何提交前，先确认 `SecurityToken=` 为空**（全文检索 `SecurityToken=.` 非空即停）。
  2. **`Config/DefaultEngine.ini` 出现在 `git status` 时，先看它改了什么再决定是否入库**；**编辑器保存造成的注释丢失属预期现象，据实记录，不要「顺手还原」**（还原会被下次保存再删，产生无谓 churn）。
  3. **启用 AFS 前必须先轮换密钥**，不得复用已泄露的历史值。
- **结构性修复（未实施，待立项）**：把 `^SecurityToken=.+` 纳入提交前拦截（`pre-commit` 钩子或门禁检查项），**不再依赖本条纪律**。**注意 `check-integrity.py` 当前处于封版状态**（`77269 B` / `SHA256 A280C20A67AA533904BFA0BBEE04F95246D8C5AB5C9489209AB0479ECB244792`），**加检查项须走变更申请**。


用户意图无法明确归类时，自动使用“只读分析”。不得猜测进入执行模式。
