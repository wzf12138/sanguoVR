# AUDIT-repo · 仓库与磁盘盘点报告

- 任务：t1（维度：仓库与磁盘）
- 执行者：scout-repo（researcher · 仓库与磁盘盘点）
- 执行时间：2026-09-10 22:30–22:45（本机时区 +08:00）
- 工作目录：D:\AWork\Unreal\Project\VRSanguoYanWuchang
- 仓库：origin = https://github.com/wzf12138/sanguoVR.git，分支 master
- 工具版本：git 2.54.0.windows.1，git-lfs 3.7.1
- 性质：**只读盘点**。未执行任何清理、未改 .gitignore、未动编辑器进程、未跑 rebuild_v5.py。
- 唯一写入路径：本文件（.trae/execution/reports/audit/AUDIT-repo.md，AGENTS.md 规则20(b) 授权）。

分类桶（全队共用）：A-废弃 / B-冗余 / C-活跃 / D-待定 / E-不应入库。

---

## 0. 结论摘要（先读这一段）

1. **工作区三层实测**：受管 1269 个文件 / 256,158,180 B（244.3 MB）；未跟踪 26 个文件 / 7,315,156 B（6.98 MB）；被忽略 19,491 + 1 = 19,492 个普通文件 / 15,079,479,088 B（14.04 GB）。全工作区（含 .git）总计约 16.3 GB。
2. **推送不是硬阻塞（已由指挥台裁定更正）**：本报告初版把「github.com:443 直连失败」判定为 t10 的硬阻塞，**该结论已更正**。项目已有固化做法：**单次借用本机活代理 7897 端口**，只对本次命令生效、禁止持久化写入 git 配置。我在收到裁定后已用只读命令**独立复现成功**（见 §7）。连通性对比（主站不通而 objects.githubusercontent.com / codeload.github.com 通）仍然有效并被采纳，但**不能**由此推出「必须换镜像」或「改口径为待推送」。
3. **远程 HEAD 是 `master`（非 main）**：服务端实测 `ref: refs/heads/master	HEAD`。本地 `.git/refs/remotes/origin/HEAD` 指向 `origin/main` 是 **2026-08-09 的陈旧缓存**，不可采信。`refs/heads/main`(e5c8a9a) 确实存在于远端，但只是同一提交的历史遗留分支，**已废弃**。
4. **不需要新建任何 E: 备份**：远程推送确实能让 origin 成为唯一备份，但前提是推送能成功（推代理路径已复现，见第 2 条）。
4. **B-冗余最大宗**：`Build/Patches/PICOOpenXR/` 受管 187 个文件，其中 `Source/` 184 个文件里 **181 个与 Plugins/PICOOpen174f9f81d266V8/Source 逐字节相同**（SHA256 比对），仅 3 个文件不同 —— 等于把 PICO 插件源码整份复制进仓库。
5. **LFS 覆盖缺口**：`.gitattributes` 覆盖 uasset/umap/fbx/blend/音频/视频/压缩包/dll/lib/pdb/so，**不含 png/jpg/tga/bmp**。后果：39 个受管 .png 全部是普通 Git blob（非 LFS），其中 18 个 ≥1 MB（合计 44.2 MB），最大 4,590,192 B。**但本次基线不受影响**：唯一可能带入大 PNG 的 `Docs/` 已裁定**排除**（见第 6 条），故本次没有新的 PNG 入库；`*.png` 补 LFS 规则按裁定**建议另立任务**、本次不做。受管文件中 ≥5 MB 的 3 个全部是 LFS（uasset）。
6. **`Docs/` 已裁定排除、不入库（指挥台 2026-09-10 更正；原「入库」裁定作废）**：依据 ① AGENTS.md 文件边界只承认 `Config/` `Content/` `Plugins/` `Source/` 与「治理与 AI 资料：仅 `.trae/`」；② `.trae/archive/README.md` 判废 `Docs`；③ `CHANGELOG.md` L894/L897 记「删除 Docs…后续不再使用」；④ `git log --all -- Docs` 为空（从未入库）。原第二判据「不能由一条命令完全重建」已被本报告 §10.5 的时间戳提示命中（`scene_topdown.png` 疑由 `rebuild_v5.py` 于 19:14–19:15 生成）——该提示经指挥台确认正确。→ **基线暂存清单中 `Docs/` 为 0 条。**
7. **`.gitignore` 反否定陷阱（已用探针实测确认）**：`!.trae/**`、`!Content/**`、`!Config/**`、`!Source/**`、`!Plugins/**` 这些反否定规则会让这些目录里的 `*.log` / `*.tmp` 等「本应忽略」的文件重新变为**可入库**。探针证据见 §4.1。
8. **我的探针文件与一条诊断日志（均已清理）**：17 个探针文件已在同一批次内删除干净（残留实测 0）；`git credential-manager diagnose` 产生的 `gcm-diagnose.log`（8,258 B）**已按指挥台裁定删除**并核验（`git status` 行数不变）。两者均登记在 §8，并如实声明「本次审计唯一被删除的文件是我自己的产物，不是项目文件」。

---

## 1. 工作区分层实测（受管 / 未跟踪 / 被忽略）

命令（工作目录 = 项目根）：

```
git ls-files                                                  # 受管
git ls-files --others --exclude-standard                      # 未跟踪
git ls-files --others --ignored --exclude-standard            # 被忽略
```

逐文件累加 `(Get-Item -Force).Length` 得到字节数：

- 受管：**1269** 个文件，**256,158,180 B = 244.3 MB**（与 `git ls-tree -r HEAD` 行数 1269 一致）
- 未跟踪：**26** 个文件，**7,315,156 B = 6.98 MB**
- 被忽略：**19,492** 个文件，**15,079,479,088 B = 14.04 GB**
- 工作区合计（不含 .git）：1269 + 26 + 19492 = **20,787 个文件，约 14.29 GB**

排错记录（不虚构）：`git status --porcelain --ignored=matching` 只给目录摘要，**不列出被忽略文件**（实测只有 22 行 `!!`）；列出被忽略文件的正确命令是 `git status --porcelain --ignored`（无 `=matching`）或 `git ls-files --others --ignored --exclude-standard`。已用 7 个探针文件交叉验证，见 §4.1。

`.git` 目录本体：**585 个文件，882,739,249 B = 841.8 MB**。

---

## 2. 逐目录属性表

字节数 = 该目录下全部文件（含被忽略）递归求和；「.gitignore 覆盖」= `git check-ignore -v --no-index` 的实测结果；「应该覆盖？」= 按 AGENTS.md 规则23（禁止提交生成目录与本机状态）判定。

**覆盖完整性声明**：实测根目录下**恰好 19 个目录**，本表**逐项覆盖全部 19 个**（`.agent-teams` / `.dsh-uploads` / `.git` / `.github` / `.trae` / `.vs` / `.workbuddy` / `ArchivedBuilds` / `Binaries` / `Build` / `Config` / `Content` / `dashboard` / `DerivedDataCache` / `Docs` / `Intermediate` / `Plugins` / `Saved` / `Source`）；根目录文件 8 个（`AGENTS.md`、`README.md`、`.editorconfig`、`.gitattributes`、`.gitignore`、`.lfsconfig`、`.vsconfig`、`VRSanguoYanWuchang.uproject`）亦全部覆盖。任务书列举的名字里 **`.vscode` 在磁盘上不存在**（`.gitignore:8` 已预留该规则）；`dashboard` 的三个子目录（`__pycache__`、`status.json`、`index.html`）因被 `dashboard/.gitignore` 单独处理，列在 §2.1 末尾。

### 2.1 应被忽略且已被忽略的目录（确认覆盖）

- `Intermediate/` — 1825 文件 / 5,947,493,818 B（5.54 GB）；规则 `.gitignore:5`；应该覆盖 → **一致**
- `.vs/` — 47 文件 / 3,902,485,459 B（3.63 GB）；规则 `.gitignore:7`；应该覆盖 → **一致**。最大 3 个：`Insiders/ipch/73720a8c41f37b35.ipch` 1,490,026,496 B、`Browse.VC.db` 1,457,012,736 B、`CopilotIndices/18.9.1268.207/SemanticSymbols.db` 561,197,056 B（均 2026-08-09）
- `Binaries/` — 20 文件 / 1,375,841,140 B（1.28 GB）；规则 `.gitignore:2`；应该覆盖 → **一致**
- `Saved/` — 818 文件 / 1,205,590,432 B（1.12 GB）；规则 `.gitignore:6`；应该覆盖 → **一致**
- `ArchivedBuilds/` — 5 文件 / 758,959,580 B（724 MB）；规则 `.gitignore:40`；应该覆盖 → **一致**。内含 `VRSanguoYanWuchang-arm64.apk` 328,385,567 B、`libUnreal.so` 430,570,488 B（2026-08-13），属 §规则23「大型非 LFS 二进制」范畴但已被忽略，不入库
- `DerivedDataCache/` — 15446 文件 / 308,278,290 B（294 MB）；规则 `.gitignore:4`；应该覆盖 → **一致**
- `.workbuddy/` — 1 文件 / 9,441 B；规则 `.gitignore:93`；应该覆盖 → **一致**（只有 `memory/2026-08-29.md`）
- `dashboard/__pycache__/`、`dashboard/status.json`、`dashboard/integrity.json`、`dashboard/index.html` — 由 `dashboard/.gitignore`（5 行，2026-08-12）覆盖，`check-ignore` 实测命中；应该覆盖 → **一致**（生成物）

### 2.2 未被忽略、且**不应该**入库（E 类缺口）

- `.dsh-uploads/` — 3 文件 / 2,962,458 B；`check-ignore` **未命中**（探针复验：`.dsh-uploads/zzz_probe.png` 在 `git status` 里以 `??` 出现）；性质 = DSH 会话上传的临时附件（2 张 limelight 截图 + 1 张 deepseek logo）；应该覆盖 → **缺口，E**
- `.agent-teams/` — 7 文件 / 96,415 B；`check-ignore` **未命中**（探针复验：`.agent-teams/zzz_probe/team.json` 以 `??` 出现）；性质 = DSH 多代理团队运行态；**其中 4 个文件当前已被 git 跟踪**（见 §3.4）；应该覆盖 → **缺口，E**
- `Docs/` — 5 文件 / 2,948,710 B；`check-ignore` 未命中；`git ls-files Docs` = **0**（从未入库）。Docs/Scene/ 为本次会话产物（全部 mtime 2026-09-10 19:14–19:15），其中 `scene_topdown.png` 2,853,240 B。性质 **D-待定**：`Docs/` 不在 AGENTS.md「文件边界」列举的 UE 工程目录（Config/Content/Plugins/Source）也不在「治理与 AI 资料：仅 .trae/」内，属「治理外但有价值」。**裁定结果：排除（不入库）** —— 见 §9.8 与 §11 第 5 行（指挥台 2026-09-10 更正，原「入库」裁定作废）。
- `dashboard/`（.py 源文件已被跟踪，6 个）— 13 文件 / 503,814 B。**D-待定**：看板脚本是工具源码（像该入库），但同目录下 4 个生成物已被 dashboard/.gitignore 排除。**注意矛盾点**：根 `.gitignore:91 architecture-assessment.html`、`:89 .trae-html-share-packages/` 暗示曾有过「生成 HTML 不该入库」的约定，而 dashboard/index.html 正是生成物 → 现约定一致，无缺口。

### 2.3 未被忽略且应该入库的目录（正常）

- `Content/` — 297 文件 / 226,103,757 B（215.6 MB）；受管 294；`check-ignore` 未命中（`!Content/**`）
- `Config/` — 10 文件 / 96,450 B；受管 10
- `Source/` — 42 文件 / 80,674 B；受管 42
- `Plugins/` — 1868 文件 / 1,604,384,076 B（1.53 GB）；受管 552；其余 1316 文件 / 1,579,546,294 B 被忽略（`Plugins/**/Binaries/`、`Plugins/**/Intermediate/`、`Plugins/**/*.pdb`）
- `.trae/` — 167 文件 / 894,334 B；受管 158；9 个未入库（见 §3.3）
- `Build/` — 195 文件 / 6,207,728 B；受管 193（`Build/Patches/` 187 + `Build/Android/` 6）
- `.github/` — 2 文件 / 1569 B；受管 2
- 根文件：`AGENTS.md`(2026-09-04 10:52)、`README.md`、`.gitattributes`、`.gitignore`、`.editorconfig`、`.vsconfig`、`.lfsconfig`、`VRSanguoYanWuchang.uproject` — 全部受管
- `.git/` — 585 文件 / 841.8 MB（见 §6）

---

## 3. git 脏项逐条分类

### 3.0 精确计数（实测口径，供全队统一）

`git status --porcelain` = **44 行**，构成：

- 未暂存修改 **26**（` M`），已暂存修改 **0**（`M `），删除 **2**（` D`），未跟踪条目 **16**（`??`）
- 16 个未跟踪条目展开为 **26 个真实文件**（其中 10 个条目是整目录折叠：`Docs/`(5) + `.agent-teams/vrsanguo-audit-backup/`(4) + `.dsh-uploads/session-.../`(3) 等）
- 未跟踪真实文件字节合计 **7,315,156 B**

（任务书写「43 条」，与实测 44 条差 1；差异原因未能查明，按实测 44 条盘点，并把口径写在这里供 verifier 复核。）

**盘点后新增的第 45 行（本队自身产物，如实登记）**：我把本报告写入 `.trae/execution/reports/audit/` 之后，脏项计数从 **44 变为 45**，新增条目是 `?? .trae/execution/reports/audit/`（目录折叠，含 `AUDIT-repo.md` 36,460 B @22:38:05 与 scout-governance 的 `t2-governance-sessions.md` 39,862 B @22:38:12）。该计数变化**不是**我的探针残留（探针残留实测为 0），而是本队两份报告的正式落盘。**含义**：这两份审计报告是 C-活跃正文，会进入 Git 基线提交；`!.trae/**` 使它可入库（`git check-ignore --no-index` 命中 `.gitignore:72`），符合 AGENTS.md 规则20(b) 的报告路径约定。

### 3.1 未暂存修改 26 项

**C-活跃（.trae 治理域，19 项）** — 均为 2026-09-05 ~ 2026-09-10 的治理/报告更新，是当前唯一正文：

1. `C` `.trae/CHANGELOG.md` — 114,763 B，mtime 2026-09-10 19:11:48（+66/-0 行）
2. `C` `.trae/execution/active/M01-T001/ALLOWLIST.txt` — 2,154 B，2026-09-09 00:00:30（+15/-0）
3. `C` `.trae/execution/active/M01-T001/STATUS.json` — 1,062 B，2026-09-06 16:24:42
4. `C` `.trae/execution/active/M01-T005/STATUS.json` — 694 B，2026-09-08 22:15:10
5. `C` `.trae/execution/active/STATUS.json` — 26,787 B，2026-09-10 19:17:14（根 STATUS，单一事实源）
6. `C` `.trae/execution/reports/tasks/M01-T001.md` — 24,205 B，2026-09-05 20:48:35（+9/-1）
7. `C` `.trae/execution/reports/tasks/M01-T005.md` — 14,469 B，2026-09-10 19:02:26（+111/-68）
8. `C` `.trae/execution/sessions/session-20260830-001.md` — 49,903 B，2026-09-06 14:22:29（+372/-42）
9. `C` `.trae/execution/task-template-level.md` — 5,647 B，2026-09-10 19:06:46（+19/-0）
10. `C` `.trae/execution/task-template.md` — 5,834 B，2026-09-10 19:06:41（+19/-0）
11. `C` `.trae/governance/ExecutionModel.md` — 14,821 B，2026-09-09 10:23:59（+9/-0）
12. `C` `.trae/governance/ReviewProtocol.md` — 4,998 B，2026-09-09 10:23:59（+4/-1）
13. `C` `.trae/knowledge/TechnicalDecisions.md` — 13,023 B，2026-09-10 21:32:33（+20/-0）
14. `C` `.trae/registers/11-tech-debt-register.md` — 12,174 B，2026-09-09 18:17:48
15. `C` `.trae/systems/02-interaction-and-weapon-system.md` — 3,137 B，2026-09-09 10:23:59（+8/-0）
16. `C` `Config/DefaultEngine.ini` — 20,492 B，2026-09-09 22:06:10
17. `C` `Config/DefaultGame.ini` — 4,236 B，2026-09-09 22:06:10
18. `C` `Content/VRSanguo/VR/BP_VRCharacter.uasset` — 103,914 B，2026-09-08 23:19:13（LFS 指针变更）
19. `C` `Content/VRTemplate/Input/IMC_Weapon_Left.uasset` — 4,599 B，2026-09-08 22:26:05（LFS 指针变更）
20. `C` `Content/VRTemplate/Input/IMC_Weapon_Right.uasset` — 4,616 B，2026-09-08 22:26:05（LFS 指针变更）
21. `C` `Content/VRSanguo/Dev/L_SkeletonTest.umap` — 25,821 B，2026-09-09 22:54:06（LFS 指针变更）
22. `C` `Content/VRSanguo/VR/Mesh/环首刀.uasset` — 28,041,121 B，2026-09-10 15:07:31（LFS 指针变更；见 §5.3 哈希证据）
23. `C` `Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp` — 120,227 B，2026-09-08 13:57:17
24. `C` `Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.cpp` — 85,194 B，2026-09-08 12:58:39（+16/-2）
25. `C` `Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.h` — 6,158 B，2026-09-05 20:48:35
26. `C` `Source/VRSanguoYanWuchang/Private/Combat/VRSanguoGripLibrary.cpp` — 7,402 B，2026-09-10 22:31:52（+46/-12，最新改动）

**D-待定（第三方插件内改动 3 项 —— 按指挥台裁定「保持 D-待定，但升级为治理疑点」）**

- `D`（**治理疑点**）`PICO_HMD.cpp` / `PICO_Controller.cpp` / `PICO_Controller.h`（上列 #23–25）—— 三者位于 `Plugins/PICOOpen174f9f81d266V8/`，是**第三方 PICO 插件的源码**。逐项给出事实与证据，**不替任何会话定性**：
  1. **是否越出白名单？—— 逐文件比对，1 项在外、2 项在内。**
     - M01-T001 白名单授权行：`Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/**`
     - 同文件明写禁令：`# 仅限 PICOOpenXRInput 模块源码；其他 PICO 模块（HMD 等）禁改`
     - `PICO_HMD.cpp` 实际路径 = `Source/**PICOOpenXRHMD**/Private/PICO_HMD.cpp` → **`OUT-OF-WHITELIST`**（模块不同，且被禁令点名）
     - `PICO_Controller.cpp`、`PICO_Controller.h` 实际路径 = `Source/PICOOpenXRInput/Private/...` → `IN-WHITELIST`
  2. **在飞改动的精确内容（`git diff` 原文）**：`PICO_HMD.cpp` 仅 **+1 行**，位置 `FHMDPICO::GetOptionalExtensions`：新增 `OutExtensions.Add(XR_EXT_UUID_EXTENSION_NAME);`（注释说明它是 `XR_EXT_render_model` 的前置，SteamVR 校验该依赖、PICO 运行时不校验）。→ 本次在飞改动**不是** TD-005 那条 swapchain 补丁（那条是 `xrCreateSwapchain` 拦截，2026-08-11/12 已登记并经 V-008 真机验证），在飞的是 **XR_EXT_UUID 依赖修复**。
  3. **仓库自己已书面承认越范围（关键证据，非我推断）**：`.trae/execution/CR-20260908-001-steamvr-retro-unlock.md` 第 14 行记为变更 ④「仍失败 → PICO_HMD 请求 XR_EXT_RENDER_MODEL 缺前置 XR_EXT_UUID → **PICO_HMD.cpp 补依赖**」；第 17 行原文：**「注意：三项变更中 ②③④ 超出 M01-T001 原白名单（PICOOpenXRHMD 模块与 DefaultGame.ini 不在列），本 CR 为回溯登记；diff 行号细节由 executor 下次回执校对补充。」**
  4. **执行侧同时留痕**：`.trae/execution/sessions/session-20260906-001.md` 第 233 行记该修复与「编译 17.9s 成功」。
  5. **登记缺口（供督导/审核判断，我不越权定性）**：`XR_EXT_UUID` 在**整个 `.trae` 的受管文件里搜不到**（`git grep -n XR_EXT_UUID -- .trae` = **0 命中**）；该改动**只被 CR-20260908-001（未跟踪）与 session-20260906-001（未跟踪）记载**，未被 CHANGELOG、登记册或 `.trae/execution/active/M01-T001/STATUS.json`（实测 0 处提及 HMD / XR_EXT_UUID / 超白名单）登记。`CHANGELOG.md:636` 提及的 `PICO_HMD.cpp` 是另一件事（TD-005 swapchain 补丁）。
     - → **待裁定的疑问（请指挥台/verifier 裁定，我不定性）**：这次越范围的 HMD 改动是否完成了「回溯登记」所要求的补全（diff 行号校对、登记册/CHANGELOG 落账），以及是否需要补一份正式范围扩展 CR。
  6. **与 `Build/Patches/` 补丁机制的关系（B-冗余相关）**：`Build/Patches/PICOOpenXR/PICO_HMD.cpp.patched`（120,079 B，2026-08-12）与插件内 `PICO_HMD.cpp`（120,227 B，2026-09-08）**不同** → 补丁基线副本**没有跟上**这两类改动。这支持 §5.4 关于 `Build/Patches/` 定位的 D-待定判断：它到底是「权威补丁基线」还是「一份会过期的副本」，直接决定它算 C 还是 B。

**D-待定 → 已裁定为 A-废弃（指挥台 2026-09-10 22:50 裁定：接受删除，随基线提交）**

- `A`（原 D）`Content/VRSanguo/Dev/L_Prototype_1v1.umap` —— 工作区已删除，HEAD 中受管（LFS 指针 blob 130 B）。取代者证据：同目录现存 `L_Prototype_1v1_v4.umap`(509,749 B, 2026-09-10 15:07:13) 与 `L_Prototype_1v1_v5.umap`(673,326 B, 2026-09-10 21:44:17)。
- `A`（原 D）`Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap` —— 同上（HEAD 指针 blob 131 B）。
- **裁定理由与可恢复性证据**：删除已在磁盘发生，不提交则仓库永久脏 → 接受删除。**「删除」只是从工作区消失，不是从历史消失**：两份 LFS 对象在本地 store 中完整存在，历史可从 HEAD 完整恢复（旧对象 sha256 `3fc44947…` / 67,215 B；`a825dd7a…` / 246,266 B）。
- 注：另见 scout-assets 的交叉证据 —— v1/v2 的删除属**已备案的用户决定**（M01-T005 note：「v1/v2/v3 按用户决定删除（脚本在外可重生…）」），与本次裁定一致。

### 3.2 未跟踪条目 16 项分类

- `E` `.agent-teams/`（目录折叠，4 文件）—— DSH 团队运行态。mtime 2026-09-10 22:31–22:35。**不应入库**：属 AGENTS.md 规则23 的「本机状态/会话临时」。
- `E` `.dsh-uploads/`（目录折叠，3 文件）—— DSH 会话上传附件。mtime 2026-09-09 23:08 ~ 2026-09-10 08:28。**不应入库**。
- `C` `.trae/execution/CR-20260905-001-pico-battery-gating.md` — 10,130 B，2026-09-06 13:51:32。变更申请正文，**已入库目录下的新正文** → C。
- `C` `.trae/execution/CR-20260907-001-imc-pico4-keys.md` — 3,900 B，2026-09-07 21:54:31 → C。
- `C` `.trae/execution/CR-20260908-001-steamvr-retro-unlock.md` — 5,047 B，2026-09-09 00:01:06 → C。
- `C` `.trae/execution/CR-20260909-001-grip-contract-fix.md` — 7,439 B，2026-09-10 19:00:50 → C。
- `C` `.trae/execution/arena-gameplay-decisions.md` — 5,025 B，2026-09-10 19:11:40 → C（是否为唯一正文由 scout-governance 裁定）。
- `C` `.trae/execution/sessions/session-20260904-002.md` — 26,570 B，2026-09-10 19:01:42 → C。
- `C` `.trae/execution/sessions/session-20260906-001.md` — 31,083 B，2026-09-08 18:36:19 → C。
- `C` `.trae/execution/sessions/session-20260908-001.md` — 4,032 B，2026-09-08 22:07:18 → C。
- `C` `.trae/execution/sessions/session-20260908-002.md` — 38,310 B，2026-09-10 19:16:58 → C。
- `C` `Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap` — 673,326 B，2026-09-10 21:44:17 → **最新关卡，必须入库**（`.gitattributes` 已覆盖 `*.umap` → LFS）。
- `D` `Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap` — 509,749 B，2026-09-10 15:07:13。**是否 A-废弃（被 v5 取代）需裁定**：v5 比 v4 晚 6.5 小时且更大（673,326 > 509,749），但 v4 是否仍被引用需关卡侧确认 —— 未查明，写 D。裁定人：指挥台/关卡负责人。
- `C` `Content/VRSanguo/Dev/M_GrayBox_Red.uasset` — 9,603 B，2026-09-10 18:11:19 → 灰盒材质，属 M01-T005 场景用资产（与 `Saved/Evidence/M01-T005/v56b_drumwing.png` 18:54 的取证时间线吻合）→ C。
- `C` `Content/VRSanguo/Dev/M_GrayBox_Straw.uasset` — 9,561 B，2026-09-10 18:11:16 → C。
- `E`（原 D，**指挥台已裁定排除**）`Docs/`（目录折叠，5 文件 / 2,948,710 B，全部 mtime 2026-09-10 19:14–19:15）—— 见 §2.2 与 §9.8：**排除，不入库**（原「入库」裁定已作废）。`git log --all -- Docs` 为空 = 从未入库，故排除后回到历史一致状态。附带影响：因不再入库，PNG 的 LFS 缺口（§5）对本次基线**不构成风险**（仅将来若决定入库才需先补 `*.png` 规则）。

### 3.3 .trae 未入库 9 项（与受管 158 的差集）

`git ls-files .trae` = 158；磁盘实际 = 167；差集 9 项，全部为 CR-2026xxxx / session-2026xxxx 新正文（即 §3.2 中的 9 个 .trae 文件）。`.trae` 受管但磁盘缺失 = **0 项**（无「幽灵索引项」）。

---

## 4. .gitignore 缺口清单

### 4.1 探针实测（关键方法学结论）

我在项目内创建了 17 个 0 字节级探针文件（路径见下），观察 `git status` 的实际判定，随后**在同一批次内全部删除**（残留实测 0 个，`git status --porcelain` 恢复为 44 行）。

**重要排错（供全队复用）**：`git check-ignore` 对**反否定规则**也返回 exit 0 并打印 `!.trae/**` 这类规则，「看起来像被忽略」；但真正的判定要看 `git status --porcelain --ignored`。第一次我用 `--ignored=matching` 得到错误结论（它不列被忽略文件），第二次用 `--ignored`（不带 `=matching`）才拿到正确结果。**不要把 `check-ignore` 的 exit 0 当作「已忽略」的充分证据。**

实测结果（`??` = 会入库 / `!!` = 已忽略）：

- `??` `.trae/zzz_probe.log` —— **反否定导致可入库**（`!.trae/**` 压过了 `*.log`）
- `??` `.trae/zzz_probe.tmp` —— **同上**
- `??` `Content/zzz_probe/log.txt` —— **反否定导致可入库**（`!Content/**`）
- `??` `Config/zzz_probe.txt` —— **反否定导致可入库**（`!Config/**`）
- `??` `Source/zzz_probe.tmp` —— **反否定导致可入库**（`!Source/**`）
- `??` `.dsh-uploads/zzz_probe.png` —— 无任何规则命中
- `??` `.agent-teams/zzz_probe/team.json` —— 无任何规则命中
- `??` `Docs/zzz_probe.txt` —— 无任何规则命中
- `??` `dashboard/zzz_probe.png` —— 无任何规则命中
- `!!` `Intermediate/zzz_probe.txt`、`Saved/zzz_probe.txt`、`Binaries/zzz_probe.dll`、`.vs/zzz_probe.bin`、`DerivedDataCache/zzz_probe.bin`、`ArchivedBuilds/zzz_probe.apk`、`.workbuddy/zzz_probe.md` —— 7 项确认已忽略（与 §2.1 一致）
- `!!` `Content/VRSanguo/Dev/zzz_Probe_BuiltData.uasset` —— 被 `.gitignore:82 Content/**/*_BuiltData.uasset` 正确忽略

**结论：`Content/` 有 `_BuiltData` 补丁规则，`Plugins/` 有 Binaries/Intermediate/pdb 补丁规则，但 `.trae/`、`Config/`、`Source/` 三个反否定目录没有任何对冲规则** → 这三个目录里的 `*.log` / `*.tmp` / `*.bak` / `*.user` 等会静默入库。这是 §4.2 第 1 条缺口的**根本原因**。

### 4.2 缺口清单

1. **`.trae/**` 反否定无对冲** —— `!.trae/**`(.gitignore:72) 使 `.trae` 内 `*.log/*.tmp/*.bak/*.user/*.userprefs/*.pidb/*.sdf/*.suo/Thumbs.db/Desktop.ini` 全部可入库。证据：探针 `.trae/zzz_probe.log` 与 `.trae/zzz_probe.tmp` 均以 `??` 出现。
2. **`Config/**` 反否定无对冲** —— 同上，探针 `Config/zzz_probe.txt` 以 `??` 出现。
3. **`Source/**` 反否定无对冲** —— 同上，探针 `Source/zzz_probe.tmp` 以 `??` 出现。
4. **`.dsh-uploads/` 完全未覆盖** —— DSH 会话上传附件目录，属「会话临时/本机状态」。按 AGENTS.md 规则23 + 「临时脚本、下载和调试输出：不得进入项目」应出库并加忽略。
5. **`.agent-teams/` 完全未覆盖，且已有 4 个文件被跟踪** —— 见 §4.3。属 DSH 团队运行态。
6. **`Docs/` 未覆盖（且从未入库）** —— **已裁定：排除，不入库**（保留为未跟踪、未忽略状态）。判据与依据见 §9.8、§11 第 5 行；本缺口**无需修补**（既然不入库，就不需要为它加 ignore 规则；若将来决定入库，再评估是否同时补 `Docs/` 的 ignore 或 LFS 规则）。
7. **`dashboard/__pycache__` 已覆盖但 `*.pyc` 未在根 .gitignore 覆盖** —— 仅靠 `dashboard/.gitignore`。若将来在别处引入 Python，`__pycache__` 会入库。属**低风险**缺口（当前无实际泄漏：`git ls-files` 中无 `__pycache__`/`.pyc`）。
8. **`Build/` 被跟踪但语义模糊** —— `Build/` 不在 .gitignore 里（`Build/*/FileOpenOrder/` 只忽略一个子路径）。当前受管 193 个文件，其中 187 个是 `Build/Patches/PICOOpenXR/`（§5.4 冗余）。`Build/Android/` 6 个 Java 模板文件是 UE 模板产物，一般属生成物但被广泛纳入版本控制，属**惯例可接受**。

### 4.3 「已被跟踪但属生成物」项（`git ls-files` 证据）

- `.agent-teams/archive/vrsanguo-survey/inbox/captain.jsonl`
- `.agent-teams/archive/vrsanguo-survey/inbox/qa.jsonl`
- `.agent-teams/archive/vrsanguo-survey/team.json`
- `.agent-teams/retired-members.json`
  → 4 个文件，合计 41,131 B（18,410 + 20,473 + 2,027 + 129 = 41,039；`team.json` 另有 129 B 的 retired-members，精确合计 41,039 B），加入于 commit `296ebed`（2026-09-03 22:55，"chore: 同步其他会话累积的工作树改动"）。**性质**：DSH 团队/信箱运行态 —— 属 AGENTS.md 规则23「本机状态 / 会话临时」→ **E-不应入库**，建议 `git rm --cached` + 加 `.gitignore`（**建议，不执行**）。
- 无其他「受管但属生成物」项：`git ls-files` 中不含 `.pyc`、`.log`、`.tmp`、`.bak`、`.swp`、`.pdb`、`Thumbs.db`、`Desktop.ini`、`.vsidx`、`.ipch`（实测筛选结果为空）。
- **例外要注意**：`Content/VRTemplate/Maps/VRTemplateMap_BuiltData.uasset` 5,107,675 B **受管**，但它被 `.gitignore:82 Content/**/*_BuiltData.uasset` 命中 —— 说明它是在该规则生效之前入库的。它同时是「LFS 覆盖内的 5 MB 级文件」（LFS 指针），故不是 §5 的 LFS 缺口，但属**「已被跟踪但按新规则不该入库」的候选**（需裁定：模板自带 BuiltData 是否保留）。

---

## 5. LFS 覆盖审查

### 5.1 现有规则（`.gitattributes`，44 行）

LFS 覆盖：`*.uasset *.umap *.fbx *.blend *.max *.psd *.tif *.tiff *.exr *.wav *.flac *.mp3 *.mp4 *.mov *.zip *.7z *.rar *.so *.dll *.lib *.pdb`（第 24–44 行）。

**未覆盖的二进制类型（与工作区实际的差集）**：`.png`、`.jpg/.jpeg`、`.tga`、`.bmp`、`.gif`、`.webp`、`.ico`、`.dds`、`.hdr`、`.uproject`（文本，无需）、`.db`、`.vsidx`、`.ipch`（后三者已被忽略，无需）。

### 5.2 「非 LFS 且 >1 MB 的受管文件」清单（`git lfs ls-files` 交叉比对）

**18 个，合计 46,337,015 B = 44.2 MB**，全部是 `.png`：

- 4,590,192 `Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_02.png`
- 4,547,335 `Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_04.png`
- 4,024,308 `Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_01.png`
- 3,771,969 `Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_03.png`
- 3,264,636 `Content/VRSanguo/Art/References/Weapon/Sword/REF_Weapon_Sword_01.png`
- 2,840,447 `Content/VRSanguo/Art/References/Weapon/Spear/REF_Weapon_Spear_04.png`
- 2,529,935 `Content/VRSanguo/Art/References/Weapon/Spear/REF_Weapon_Spear_06.png`
- 2,474,949 `Content/VRSanguo/Art/References/Weapon/Bow/REF_Weapon_Bow_02.png`
- 2,435,266 `Content/VRSanguo/Art/References/Weapon/Sword/REF_Weapon_SwordSheath_01.png`
- 2,346,324 `Content/VRSanguo/Art/References/Weapon/Spear/REF_Weapon_Spear_03.png`
- 2,084,942 `Content/VRSanguo/Art/References/Weapon/Sword/REF_Weapon_Sword_02.png`
- 1,873,448 `Content/VRSanguo/Art/References/Weapon/Sword/REF_Weapon_Sword_05.png`
- 1,814,396 `Content/VRSanguo/Art/References/Weapon/Sword/REF_Weapon_Sword_04.png`
- 1,766,613 `Content/VRSanguo/Art/References/Weapon/Spear/REF_Weapon_Spear_02.png`
- 1,734,326 `Content/VRSanguo/Art/References/Weapon/Sword/REF_Weapon_Sword_03.png`
- 1,661,528 `Content/VRSanguo/Art/References/Weapon/Polearm/REF_Weapon_Polearm_02.png`
- 1,495,251 `Content/VRSanguo/Art/References/Weapon/Spear/REF_Weapon_Spear_07.png`
- 1,081,150 `Content/VRSanguo/Art/References/Weapon/Spear/REF_Weapon_Spear_01.png`

**>5 MB 的非 LFS 受管文件：0 个**（全部 3 个 ≥5 MB 的受管文件都是 LFS 指针 —— 28,041,121 `环首刀.uasset`、13,459,323 / 7,803,085 `texture_pbr_20250901*.uasset`）。

### 5.3 LFS 与工作区一致性（哈希级证据）

- `Content/VRSanguo/VR/Mesh/环首刀.uasset`：工作区 SHA256 = `895f89ac85fa2476bd2a720efa5a8a0db1280466b09ded09addbf41187b2a407`；该哈希**存在于本地 LFS store**：`.git/lfs/objects/89/5f/895f89ac...a407`（28,041,121 B）→ 内容真实、可推送。
- 同一文件 HEAD 中的指针指向旧对象 `oid sha256:9ba210a6...607`（size 28,040,934），该对象也在本地 store：`.git/lfs/objects/9b/a2/9ba210a6...607` → 旧版本亦可推送。
- `Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_02.png`：HEAD blob `c12719ba...`，`git cat-file -s` = **4,590,192** —— 与工作区文件同尺寸、且内容头为真 PNG（`89504e470d0a1a0a`）→ **证明确为普通 Git blob，不是 LFS 指针**（若被 LFS 接管，blob 会是约 130 B 的指针文本）。这是「PNG 未走 LFS」的直接证据。
- 受管 LFS 指针文件 **367** 个（uasset 348 / fbx 9 / umap 4 / dll 2 / lib 2 / so 2）；本地 LFS store **495** 个对象文件 / 723,507,226 B。367 个工作区中实际存在 **365**（2 个是被删除的原型关卡）。
- `git lfs fsck` → **Git LFS fsck OK**；`git fsck` → 退出码 0，无错误输出。

### 5.4 LFS 缺口影响评估（对 t10 推送）

- 受管 LFS 文件按工作区尺寸合计 **195,293,495 B = 186.2 MB**（365 个）。若这些对象**已经**在远端，则本次推送只需上传新增/变更的 LFS 对象。
- 本次未推送的 LFS 变更（`git diff --name-only` 命中 7 项中的 5 个现存项）：`环首刀.uasset` 28,041,121 B + `BP_VRCharacter.uasset` 103,914 + `L_SkeletonTest.umap` 25,821 + `IMC_Weapon_Left.uasset` 4,599 + `IMC_Weapon_Right.uasset` 4,616 ≈ **28.18 MB** 新 LFS 对象需上传。
- **PNG 与 LFS 的关系（本次基线已不适用，保留供将来评估）**：若将来有 2 MB 级 PNG 入库（如 `Docs/Scene/scene_topdown.png`，2,853,240 B），它会以普通 blob 进 pack，后续每次修改都会在 `.git/objects/pack` 里留一份全量副本（无法像 LFS 一样只存指针）。**但本次基线不涉及**：`Docs/` 已裁定**排除**（§9.8、§11 第 5 行），其 PNG 不进基线。同时按指挥台裁定，**本次基线提交不做 `*.png` 的 LFS 规则变更**——把现有 39 个受管 PNG 重新归一化会把 44.2 MB 重写进 LFS 并改动历史构成，风险与收益不成比例。→ 已在本报告 §9 记为「**建议另立任务**，由用户在基线之后决定是否执行」，**不是「必须现在做」**。
- **不确定项（已如实标注）**：我**无法**在只读条件下确认远端 GitHub LFS 上 367 个对象是否齐全（`ls-remote` 不能列出 LFS 对象）。间接证据：`.git/logs/refs/remotes/origin/master` 显示**从 1786286961 至 1788527574 共 34 次连续的 `update by push`**（最近一次 2026-09-04 21:12 对应 HEAD=eb319c3），其间无 push 失败记录残留，故推断「此前推送成功、LFS 对象应已上传」。**可验证路径**：推送后按 `SessionCommands.md:113-120` 查 GitHub Actions（匿名 API 可查，本仓库公开，我的 TCP 探测显示 api.github.com 路径可达）。

---

## 6. .git 体积构成与可回收垃圾（只报告，不执行）

`.git` 实测 **585 文件 / 882,739,249 B = 841.8 MB**，构成：

- `objects/` — 58 文件 / 187,169,466 B（178.5 MB）
  - `git count-objects -vH`：`count: 53`（松散对象）、`size: 244.67 KiB`、`in-pack: 2335`、`packs: 1`、`size-pack: 178.19 MiB`、**`prune-packable: 0`、`garbage: 0`、`size-garbage: 0 bytes`**
  - → **可安全回收的垃圾实测为 0**；唯一理论收益是 `git gc` 把 53 个松散对象（244.67 KiB）打包，收益约 245 KB，**不值得为此跑 gc**
- `lfs/` — 496 文件 / 723,507,226 B（690 MB）—— **本地 LFS 对象缓存，不是垃圾**
  - 结构：`.git/lfs/objects/`（495 个对象，两字符前缀分片）；`.git/lfs/tmp`（0 文件）；`.git/lfs/incomplete` **不存在**
  - **警告**：这是 367 个受管二进制的**本地实体来源**。在远程推送成功之前删除它会直接失去内容；即便推送成功，删掉它也会让任何后续 checkout / 恢复都要重新从网络拉取 186 MB。→ **不得作为「清理收益」计入**
- `index` — 184,922 B；`logs/`（reflog）— 5 文件 / 27,992 B（reflog 很干净，无膨胀）；`hooks/` 28,208 B；`refs/` 153 B；`COMMIT_EDITMSG` 83 B
- `FETCH_HEAD` — 98 B，指向 `10062961690b3a966108004df6597d6e891e2045`（branch 'master' of https://github.com/wzf12138/sanguoVR）—— 是**较早**的一次 fetch 残留，不是当前 origin/master（eb319c3），**不代表落后**（见 §7）
- 仓库规模：**60 个提交**，HEAD = `eb319c3689458d7b1a61d1798adfc5ea8df0c494`（2026-09-04 21:12，"docs(governance): manager 会话交接基线记录 session-20260904-001 [M01-T001]"）

**工作区侧的体积热点（全部已被忽略，属「磁盘占用」而非「仓库问题」）**：`Intermediate/Android` 3,133,684,958 B、`Intermediate/Build` 2,718,017,493 B、`.vs/VRSanguoYanWuchang` 3,896,300,903 B、`Binaries/Android` 1,196,579,417 B、`Plugins/PICOOpen174f9f81d266V8`（被忽略部分）837,072,976 B、`Plugins/UE_MCP_Bridge`（被忽略部分）421,155,067 B、`Saved/StagedBuilds` 351,761,942 B、`Saved/Autosaves` 245,645,617 B、`DerivedDataCache/Buckets` 167,166,076 B、`Saved/Crashes` 116,831,793 B。另：`Saved/*.tmp` 里 5 份 `环首刀*.tmp` 各 ≈28 MB（合计 ≈140 MB，其中 2 份尺寸 28,040,934 = HEAD 旧版本、3 份 28,041,121 = 当前版本）。

---

## 7. 推送可行性只读检查（**不触发任何交互式认证**）

> **本节结论已于 2026-09-10 22:50 由指挥台裁定更正。** 初版 §7 只检查了**持久化** git 配置里的代理，得出「无代理 → 推送是硬阻塞」的结论，**这是错的**：项目固化做法是**单次借用**本机活代理端口，无需（也禁止）写入 git 配置。保留原始探测数据，但结论已改。

- **直连 github.com:443：确实失败（此数据仍然有效）**
  - `git ls-remote origin` → `fatal: unable to access 'https://github.com/wzf12138/sanguoVR.git/': Recv failure: Connection was reset`，exit 128
  - 加超时参数复测 → `fatal: ... Failed to connect to github.com port 443 after 21066 ms: Could not connect to server`，exit 1
  - TCP 探测：`github.com`(20.205.243.166):443 = **False**；对比 `objects.githubusercontent.com`(185.199.108.133):443 = **True**、`codeload.github.com`(20.205.243.165):443 = **True**、`gitee.com`:443 = True、`www.baidu.com`:443 = True、`registry.npmjs.org`:443 = True
  - DNS 正常（`github.com -> 20.205.243.166`）
  - → 外网整体通，唯独 github.com 主站 443 直连不可达。这**不是**认证问题。该对比已被指挥台采纳为有效情报，但**不构成阻塞结论**。
- **单次借用代理即可推送（已独立复现成功）**
  - 代理端口实测：`127.0.0.1:7897` = **listening True**；对比 `7890`/`10809`/`1080`/`8118` 全部 **False** → 唯一活代理是 7897
  - 只读复现（未推送任何东西）：`git -c http.proxy=http://127.0.0.1:7897 ls-remote --symref origin HEAD` → **exit 0**，返回：
    ```
    ref: refs/heads/master	HEAD
    eb319c3689458d7b1a61d1798adfc5ea8df0c494	HEAD
    ```
  - 同一命令查分支：`refs/heads/master` = `eb319c3...`（与本地 HEAD 一致）、`refs/heads/main` = `e5c8a9ae910658d24ec0a7da6f2a0500f6a774a8`
  - **持久配置零改动（已核验）**：`git config --get http.proxy` 仍返回**空** → `-c` 选项确实只对当次命令生效
  - **权威依据**：`.trae/governance/SessionCommands.md` **第 97–120 行**「推送卡住时的网络恢复流程」，其中第 **110 行**（步骤 2）原文即 `git -c http.proxy=http://127.0.0.1:<活端口> push origin master`，并明写「仅本次命令生效，禁止写入持久 git 配置」。t10 将使用 `git -c http.proxy=http://127.0.0.1:7897 push origin master`。
- **本地是否有未推送提交**：`git log --oneline origin/master..HEAD` → **空**（0 条）。`git rev-parse origin/master` = `eb319c3...` = `git rev-parse HEAD` → **当前 HEAD 与 origin/master 完全一致，无未推送提交**。
- **未推送的内容 = 44 条工作区脏项**（26 修改 + 2 删除 + 16 未跟踪条目），`git diff --stat` = 28 files changed, 752 insertions(+), 157 deletions(-)；`git diff --cached` = 0（**暂存区为空**）。
- **credential.helper**：`file:D:/AWork/Git/etc/gitconfig` → `manager`（Git Credential Manager）。`git credential-manager diagnose` 自检输出含 `>>>>  GitHub API [ OK ]`。未发起任何交互式认证。
- **本地分支/引用全景（含一处已自行更正的错误）**：`master`(eb319c3) / `origin/master`(eb319c3) / `origin/main`(e5c8a9a, 2026-08-09) / `origin`(e5c8a9a, 2026-08-09)。
  - **更正**：初版把 `origin/main` 列为「正常本地引用、仅 `origin` 陈旧」，**不准确**。实测 `.git/refs/remotes/origin/HEAD` 内容为 `ref: refs/remotes/origin/main`（`git symbolic-ref refs/remotes/origin/HEAD` → `refs/remotes/origin/main`）——**这才是那个陈旧缓存本身**，它让本地误以为默认分支是 main，而服务端 HEAD 实为 **master**。任何依赖 `origin/HEAD` 的判断都会指向错的分支，**不可采信**。`refs/heads/main` 在服务端确实存在（e5c8a9a），属同一提交的历史遗留分支。
  - D-待定：是否 `git remote set-head origin -a` 修正本地缓存、以及是否清理历史遗留分支 `main`——均需指挥台裁定，本报告不执行。
- `git stash`：**空**。

---

## 8. 本次盘点的副作用登记（如实声明，不隐瞒）

1. `git credential-manager diagnose` 在**项目根**生成了 `gcm-diagnose.log`（8,258 B，mtime 2026-09-10 22:32:46）。`git check-ignore -v` 命中 `.gitignore:25 *.log` → **未入库**，且从未出现在 `git status --porcelain` 中。
   - **指挥台已裁定「允许删除」**（理由：它是本次审计自己产生的调试输出、未跟踪、被 .gitignore 覆盖，且 AGENTS.md 明写「临时脚本、下载和调试输出：不得进入项目」）。
   - **处置：已删除（2026-09-10 约 22:53）**，删除前后均已核验：删除前 `Test-Path` = True / 8,258 B；删除后 `Test-Path` = **False**，项目根不再有 `.log` 文件（`root_log_count=0`）；`git status --porcelain` 行数**不变**（45 → 45，该文件本就未跟踪、被忽略，删除不影响仓库状态）；项目根恢复为 8 个受管文件。**这是本次审计中唯一被删除的文件，且删除对象是我自己的产物，不是项目文件。**
2. §4.1 的 17 个探针文件（路径见该节）已**全部删除**，事后核验残留 = 0（`Get-ChildItem -Filter 'zzz_probe*'` 计数 0；`git status --porcelain` 恢复为 44 行，与盘点开始时一致）。
3. 未修改 `.gitignore`、`.gitattributes`、任何 `Content/`/`Config/`/`Source/`/`Plugins/` 文件；未执行 `git gc` / `prune` / `clean` / `reset`；未访问编辑器进程 pid 24284。

---

## 9. 交给下游（planner / git-operator）的关键事实与待裁定项

**A. 可直接进入「清理与保留方案」的事实（证据已给出，无需再测）**

1. `.agent-teams/` 与 `.dsh-uploads/` 应出库 + 加 ignore（E）；其中 `.agent-teams/` 已有 4 个文件在索引里（`296ebed`）。
2. `Build/Patches/PICOOpenXR/` 是插件源码的整份副本（181/184 逐字节相同）→ B-冗余候选，**但它是「插件补丁基线」的载体**（`restore_pico_patch.ps1` 在场），删除会影响补丁恢复流程 → **必须由指挥台/决策者裁定，不能由盘点自动定 A**。差异化 3 个文件恰是当前脏项，说明插件内的改动已偏离补丁基线。
3. `.gitattributes` 缺 `*.png`（以及 jpg/tga/bmp/dds 等）→ 若将来有 2 MB 级 PNG 入库，会走普通 blob 而非 LFS。**本次基线不受影响**：`Docs/` 已裁定排除（§9.8），其 2.85 MB PNG 不进基线，所以本次**没有**PNG 入库。
4. `.trae/`、`Config/`、`Source/` 三个反否定目录缺对冲规则，会静默吸收 `*.log/*.tmp/*.bak/*.user` 等本机垃圾。

**B. 阻塞 / 需裁定（t10 直接受影响）**

5. ~~**推送阻塞**~~ → **已由指挥台裁定更正：推送不是硬阻塞。** t10 使用单次借代理命令 `git -c http.proxy=http://127.0.0.1:7897 push origin master`（依据 `SessionCommands.md:110`；我已只读复现成功，见 §7）。**不要再写「换镜像」或「改口径为待推送」。**
6. **删除 2 个原型关卡：指挥台已裁定「接受删除，随基线提交」。** 理由：删除已在磁盘发生，不提交则仓库永久脏。**「删除」只是从工作区消失，不是从历史消失** —— 已实测两份 LFS 对象在本地 store 中完整存在，历史可从 HEAD 完整恢复（旧对象 sha256 `3fc44947…` / 67,215 B；`a825dd7a…` / 246,266 B）。→ 桶位从 D 改为 **A-废弃（已裁定接受删除）**。
7. **`L_Prototype_1v1_v4.umap` 是否被 v5 取代：保持 D-待定，不得升级为结论。** 我无 UE 资产引用查询手段，且不允许触碰编辑器 → 留待 M01-T001 收口后由关卡侧查证。
8. **`Docs/` 入库：指挥台初裁「入库」，随后（2026-09-10）更正为「排除」，原裁定作废** —— 落定口径为 **排除**，不再入库。四条依据（照录）：① AGENTS.md 文件边界只承认 `Config/` `Content/` `Plugins/` `Source/` 与「治理与 AI 资料：仅 `.trae/`」，`Docs/` 不属任何一类；② `.trae/archive/README.md` 判废 `Docs`；③ `CHANGELOG.md` L894/L897 记「删除 Docs…后续不再使用」；④ `git log --all -- Docs` 为空（从未入库）。
   - **原第二判据「不能由一条命令完全重建」已被本报告 §10.5 的张力提示命中**（`Docs/Scene/scene_topdown.png` 疑由 `rebuild_v5.py` 于 19:14–19:15 生成）—— 指挥台确认**该提示是对的，原样保留**（见 §10.5）。
   - **`*.png` 补 LFS 规则本次仍不做**（不变）：把现有 39 个受管 PNG 重新归一化会把 44.2 MB 重写进 LFS 并改动历史构成，风险与收益不成比例。→ 记为「**建议另立任务**，由用户在基线之后决定」，**不是「必须现在做」**。
   - **对本次基线的影响**：`Docs/` 5 个文件（2,948,710 B，含 2.85 MB 非 LFS PNG）**不进入基线提交**；t10 的暂存清单中 `Docs/` 应为 **0 条**。这也使本报告曾担心的「2.85 MB 以普通 blob 进 pack」在本次基线中**不会发生**（该风险仅在将来决定入库时才需重新评估）。
9. **PICO 插件 3 处源码改动：保持 D-待定，但已升级为治理疑点。** 完整证据见 §3.1：其中 `PICO_HMD.cpp`（`PICOOpenXRHMD` 模块）**在白名单外，且被 ALLOWLIST 明文点名禁改**；仓库自己在 `CR-20260908-001` 第 17 行书面承认「②③④ 超出 M01-T001 原白名单……本 CR 为回溯登记」。**是否越出白名单 = 是（`PICO_HMD.cpp` 1 项）**，2 项在名单内。我不替任何会话定性，只交证据。
10. **E: 盘口径**（已做穷尽式只读搜索，见 §10）：
    - 实测 **只有一处** 项目相关备份：`E:\AWorkBackup\VRSanguoYanWuchang\`（2026-09-01 22:11，内含且仅含一个 `Plugins/` 目录，1,929 文件 / 661,663,548 B = 631 MB）→ **只备份了 Plugins，是「残缺且已过期」的现场**（对照当前 `Plugins/` 1,868 文件 / 1.60 GB）。
    - **第二处现场未能查明**：`E:\` 根下无 `Backup`/`VRSanguo`/`backups`/`VRSanguoYanWuchang` 等直名目录；对 `E:\` 全部一级目录做二级名称匹配 `VRSanguo|sanguo|Sanguo` 的穷尽搜索，唯一命中仍是上面那一处；`E:\备份\` 内只有个人视频素材（红米 k40 等），与本项目无关。**请 scout-assets 复核**（可能是指 `E:\AWork\*` 下的工具/素材，或任务书口径有误）。
    - E: 可用空间 **794.8 GB**（已用 1,068.2 GB）；D: 可用 283.0 GB；C: 可用 72.1 GB。
    - **关于 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\`（AGENTS.md 指定的项目外管理脚本现场，不在 E:）**：实测存在 9 个脚本 + `tmp/` 13 个文件（含 `rebuild_v3.py`/`rebuild_v4.py`/`rebuild_v5.py`、`flip_topdown.ps1`、`Set-TraeGovernanceAcl.ps1`、`repair_status_json5.js`）。**我未打开 `rebuild_v5.py`**（冻结令点名禁止运行它；为稳妥也未读取其内容）。其中 `tmp\scene_topdown_raw.png` 3,090,912 B @2026-09-10 19:14 —— 与 `Docs\Scene\scene_topdown.png`（2,853,240 B @19:15）时间戳仅差 1 分钟、尺寸接近，**很可能就是后者的生成源**，这条线索交给 scout-assets 判定「Docs/Scene 是生成物还是正文」。
11. 陈旧本地引用 `origin` / `origin/main`（e5c8a9a，2026-08-09）是否清理（D）。
12. `Content/VRTemplate/Maps/VRTemplateMap_BuiltData.uasset`（5.1 MB，LFS）是「新规则之前入库的生成物」，保留 or 出库（D）。

---

## 10. E: 盘与盘外现场登记（穷尽式只读搜索）

命令口径：对 `E:\` 每个一级目录做二级目录名正则匹配 `VRSanguo|sanguo|Sanguo`；对候选目录做递归文件数与字节求和。**未新建任何 E: 目录、未复制、未删除。**

### 10.1 E: 根目录全景（20 个一级条目）

`$RECYCLE.BIN`、`AWork`(2026-08-30 14:42)、`AWorkBackup`(2026-09-01 22:11)、`BaiduNetdiskDownload`、`EpicGame`、`game`、`NvidiaVideo`、`Program Files (x86)`、`QQMusicCache`、`Recovery`、`Resource`、`SteamLibrary`、`System Volume Information`、`VrGame`、`WeGameApps`、`WeSingCache`、`备份`、`直播`、`视频剪辑`、`迅雷下载`、`迅雷云盘`、`邵皓怡`

### 10.2 唯一命中：`E:\AWorkBackup\VRSanguoYanWuchang\`

- mtime 2026-09-01 22:11
- 内容：**仅一个 `Plugins/` 目录**（无 Content/Config/Source/.trae/.git 等）
- 规模：1,929 文件 / 661,663,548 B = 631 MB
- 对照当前 `Plugins/`：1,868 文件 / 1,604,384,076 B = 1.53 GB
- **判定 E-不应保留为「备份」**：它不是可用备份 —— 缺 UE 工程主体、缺 `.git`、且比当前现场旧 9 天、内容规模与当前不一致。作为「完整备份」的替代品没有价值；作为「插件历史快照」才有一点意义。**处置建议留给 planner/指挥台**（我不执行删除）。

### 10.3 `E:\AWork\` 二级目录（无项目备份）

`Temp`(2026-08-29 19:19)、`Tools`(2026-08-15 23:55)、`VRExpansionPlugin`(2026-08-16 11:40)

注：`E:\AWork\VRExpansionPlugin` 与仓库内 `Plugins/VRExpansionPlugin`（受管 321 文件 / 321,318,251 B 的忽略部分）同名，**是否重复未能查明**（属 scout-assets 维度）。

### 10.4 第二处现场：未能查明（保留 D）

- `E:\` 根下不存在 `Backup` / `VRSanguo` / `backups` / `VRSanguoYanWuchang` 等直名目录
- 一级目录全景中除 `AWorkBackup` 外无任何项目相关名称
- `E:\备份\` 内容为个人素材：`其他视频`、`吴章峰&邵皓怡婚礼现场图片视频素材`、`红米k40的图片`、`红米k40的视频`、`红米k40的视频（五岳以后的视频）`、`红米k40的视频（大西北之后到五岳的视频）` —— 与本项目无关
- → **写 D-待定，请 scout-assets 复核第二处现场位置**（可能是任务书口径有误，或指 D:\AWork\TraeAdmin 现场）

### 10.5 盘外管理脚本现场：`D:\AWork\TraeAdmin\VRSanguoYanWuchang\`（登记，供交叉核对）

- 脚本 9 个：`rebuild_v3.py`(15,027 B, 2026-09-09 23:37)、`rebuild_v4.py`(18,018 B, 2026-09-10 14:53)、`rebuild_v5.py`(**50,614 B**, 2026-09-10 19:14)、`flip_topdown.ps1`(935 B, 17:52)、`repair_status_json5.js`、`verify2.js`、`verify3.js`、`Set-TraeGovernanceAcl.ps1`(2026-08-26)、`Unlock-TraeAssets.ps1`(2026-09-08)
- `tmp\` 13 个文件，其中值得注意：
  - `tmp\scene_topdown_raw.png` — 3,090,912 B, 2026-09-10 19:14
  - `tmp\STATUS.json.broken-20260910` — 22,331 B, 2026-09-10 18:15
  - `tmp\STATUS.repaired.json` — 25,113 B, 2026-09-10 18:49
  - `tmp\repair-report.txt`、`scan.js`–`scan4.js`、`verify1.txt`–`verify3.txt`
  - `tmp\` 目录 mtime 2026-09-10 22:35
- **我未打开 `rebuild_v5.py`**（冻结令点名禁止运行；为稳妥亦未读取内容）。`rebuild_v3/v4/v5.py` 三代并存 → **B-冗余候选**（同主题多版本脚本），但**处置需指挥台裁定**：它们是对应各代场景的唯一重生成手段，删旧版可能失去回退能力。
- **时间戳链（重要线索，交 scout-assets）**：`tmp\scene_topdown_raw.png`(19:14, 3,090,912 B) → `Docs\Scene\scene_topdown.png`(19:15, 2,853,240 B) → `Docs\Scene\` 其余 4 文件同为 19:14:48 → `rebuild_v5.py`(19:14)。→ 支持「`Docs/Scene/*` 是 `rebuild_v5.py` 的生成物」而非人工正文。这与 §2.2 把 `Docs/` 列为 D-待定一致，并给出一条可验证假设。

---

## 11. 指挥台裁定登记（2026-09-10 22:50 · 对本报告的更正与落定）

本节记录指挥台对本报告初版结论的**更正**与**裁定**，全部已回写进上文相应章节。**下游（planner / git-operator / verifier）应以本节为最终口径**，不要引用初版结论。

> **口径时效声明（指挥台指令，2026-09-10 补）**：§11 记录的是**截至回写时刻**的指挥台裁定；**指挥台此后的更正文优先于本表**（例如第 5 行「`Docs/` 是否入库」，已由指挥台后续指令更正为**排除**）。遇到本表与后续指令冲突，一律以后续指令为准。

| # | 我初版的结论 | 裁定 | 落定后的口径 |
|---|---|---|---|
| 1 | 推送是**硬阻塞**（github.com 直连不可达） | **更正**：不是硬阻塞 | 单次借代理 7897 可推送，权威依据 `SessionCommands.md:110`。我已只读复现成功。见 §7 |
| 2 | `origin/main` 是「正常本地引用」，仅 `origin` 陈旧 | **更正**：远程 HEAD 是 `master` | 本地 `.git/refs/remotes/origin/HEAD` → `origin/main` 是 2026-08-09 陈旧缓存，**不可采信**。见 §7 |
| 3 | 2 个原型关卡删除 → D-待定 | **裁定：接受删除** | 改判 **A-废弃**，随基线提交。「删除」只是从工作区消失，不是从历史消失（LFS 旧对象在本地可恢复）。见 §3.1 |
| 4 | `L_Prototype_1v1_v4.umap` 是否被 v5 取代 | **保持 D-待定** | 不得升级为结论；我无 UE 引用查询手段、不许碰编辑器，留待 M01-T001 收口后查 |
| 5 | `Docs/` 是否入库 | **排除（指挥台 2026-09-10 更正；原「入库」裁定已作废）** | 四条依据：① AGENTS.md 文件边界只承认 `Config/` `Content/` `Plugins/` `Source/` 与「治理与 AI 资料：仅 `.trae/`」，**`Docs/` 不属于任何一类**；② `.trae/archive/README.md` 判废 `Docs`；③ `CHANGELOG.md` L894/L897 记「删除 Docs…后续不再使用」；④ `git log --all -- Docs` **为空（从未入库）**。另：原第二判据「不能由一条命令完全重建」**已被本报告 §10.5 的张力提示命中**（`Docs/Scene/scene_topdown.png` 疑由 `rebuild_v5.py` 于 19:14–19:15 生成）——**该提示被指挥台确认正确并保留**。→ **基线暂存清单中 `Docs/` 为 0 条。** 见 §9.8 |
| 6 | 建议补 `*.png` LFS 规则 | **本次不做** | 39 个 PNG 重新归一化会把 44.2 MB 重写进 LFS 并改动历史构成，风险与收益不成比例 → 记为「**建议另立任务**」，由用户在基线之后决定。**不是「必须现在做」**。见 §5.4 |
| 7 | PICO 插件改动 → D-待定 | **保持 D-待定，升级为治理疑点** | 我实测：`PICO_HMD.cpp` **在白名单外且被 ALLOWLIST 点名禁改**，仓库自己在 CR-20260908-001:17 书面承认超范围。我只交证据，不替任何会话定性。见 §3.1 |
| 8 | `gcm-diagnose.log` 请裁定是否删 | **允许删除** | **已删除并核验**（2026-09-10）；`git status` 行数不变。这是本次审计唯一被删除的文件，且是我自己的产物。见 §8.1 |
| 9 | 脏项计数 43 vs 44 | **按实测 44** | 写明「差异原因未查明」即可，不必再追。另载明：写入本队报告后为 45（`?? .trae/execution/reports/audit/`）。见 §3.0 |

**对我自己方法学的更正（如实记录）**：初版 §7 只检查了**持久化** git 配置（`git config --get http.proxy`）就断言「无代理」，因而把可解的网络问题误判为不可解阻塞。**教训**：判定「有没有可用代理」时，除了查持久配置，还必须**探测本机代理端口是否在监听**（本次实测 7897 存活、其余 7890/10809/1080/8118 全部关闭）。这条已写进 §7 供其他人复用。

---

## 附录 A：本报告用到的关键原始输出（便于 verifier 复算）

```
$ git count-objects -vH
count: 53
size: 244.67 KiB
in-pack: 2335
packs: 1
size-pack: 178.19 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes

$ git rev-parse HEAD        -> eb319c3689458d7b1a61d1798adfc5ea8df0c494
$ git rev-parse origin/master -> eb319c3689458d7b1a61d1798adfc5ea8df0c494
$ git log --oneline origin/master..HEAD -> (空)
$ git rev-list --count HEAD -> 60
$ git lfs fsck              -> Git LFS fsck OK
$ git fsck --no-progress    -> (无输出, exit 0)
$ git stash list            -> (空)

$ git ls-remote origin
fatal: unable to access 'https://github.com/wzf12138/sanguoVR.git/': Recv failure: Connection was reset   (exit 128)

$ git check-ignore -v --no-index -- Docs/zzz_probe.txt          -> exit 1 (无规则)
$ git check-ignore -v --no-index -- .dsh-uploads/zzz_probe.png   -> exit 1 (无规则)
$ git check-ignore -v --no-index -- .agent-teams/zzz_probe/team.json -> exit 1 (无规则)
$ git status --porcelain --ignored --untracked-files=all | (探针筛选)
!! Intermediate/zzz_probe.txt
!! Saved/zzz_probe.txt
!! Binaries/zzz_probe.dll
!! .vs/zzz_probe.bin
!! DerivedDataCache/zzz_probe.bin
!! ArchivedBuilds/zzz_probe.apk
!! .workbuddy/zzz_probe.md
?? .trae/zzz_probe.log
?? .trae/zzz_probe.tmp
?? .dsh-uploads/zzz_probe.png

--- 推送可行性：更正后的关键输出（2026-09-10 约 22:52）---

$ (TCP 探测本机代理端口，SessionCommands.md 步骤2)
127.0.0.1:7897  = reachable
127.0.0.1:7890  = listening False
127.0.0.1:10809 = listening False
127.0.0.1:1080  = listening False
127.0.0.1:8118  = listening False

$ git -c http.proxy=http://127.0.0.1:7897 ls-remote --symref origin HEAD
ref: refs/heads/master	HEAD
eb319c3689458d7b1a61d1798adfc5ea8df0c494	HEAD
(exit 0)

$ git -c http.proxy=http://127.0.0.1:7897 ls-remote origin master main
e5c8a9ae910658d24ec0a7da6f2a0500f6a774a8	refs/heads/main
eb319c3689458d7b1a61d1798adfc5ea8df0c494	refs/heads/master

$ git config --get http.proxy          -> (空)      # 持久配置零改动，-c 仅当次生效
$ git symbolic-ref refs/remotes/origin/HEAD -> refs/remotes/origin/main   # 陈旧缓存

--- PICO 白名单疑点：关键输出 ---

allowed pattern (M01-T001 ALLOWLIST.txt):
  Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/**
  # 仅限 PICOOpenXRInput 模块源码；其他 PICO 模块（HMD 等）禁改

OUT-OF-WHITELIST  Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp
IN-WHITELIST      Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.cpp
IN-WHITELIST      Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.h

$ git diff -- .../Source/PICOOpenXRHMD/Private/PICO_HMD.cpp
@@ -333,6 +333,7 @@ bool FHMDPICO::GetOptionalExtensions(TArray<const ANSICHAR*>& OutExtensions)
 	OutExtensions.Add(XR_EXT_INTERACTION_PROFILE_BATTERY_STATE_DISPLAY_EXTENSION_NAME);
+	OutExtensions.Add(XR_EXT_UUID_EXTENSION_NAME);  // Prerequisite of XR_EXT_render_model; SteamVR validates this dependency (PICO runtime does not).
 	OutExtensions.Add(XR_EXT_RENDER_MODEL_EXTENSION_NAME);

$ git grep -n -I -E 'XR_EXT_UUID' -- .trae
(受管文件 0 命中)   # 该改动仅见于未跟踪的 CR-20260908-001 与 session-20260906-001

CR-20260908-001-steamvr-retro-unlock.md 第 17 行（仓库自述，非我方推断）：
  注意：三项变更中 ②③④ 超出 M01-T001 原白名单（PICOOpenXRHMD 模块与 DefaultGame.ini 不在列），本 CR 为回溯登记；diff 行号细节由 executor 下次回执校对补充。

$ (SHA256 逐字节比对) Build/Patches/PICOOpenXR/Source vs Plugins/PICOOpen174f9f81d266V8/Source
patches_source_files=184 identical=181 different=3 only_in_patches=0
plugin_source_files=184
DIFF  \PICOOpenXRHMD\Private\PICO_HMD.cpp
DIFF  \PICOOpenXRInput\Private\PICO_Controller.cpp
DIFF  \PICOOpenXRInput\Private\PICO_Controller.h
```

## 附录 B：本报告未证明的事项（避免过度断言）

1. 远端 GitHub 上 LFS 对象是否齐全 —— 网络不可达，**未能查明**（只有 34 次连续 push 成功日志作间接推断）。
2. 任务书「43 条脏项」与实测 44 条的差异原因 —— **未能查明**。
3. `L_Prototype_1v1_v4.umap` 是否仍被任何关卡/蓝图引用 —— **未能查明**（需要 UE 资产引用查询，超出只读命令行盘点范围，且不得碰编辑器）。
4. `Docs/Scene/*` 是否为其他会话的活跃产物 —— 由 scout-governance / scout-assets 交叉确认。
5. E: 盘「两处现场」中第二处的确切路径 —— **未能查明**（见 §9.10）。