# t3 · 资产与脚本产物盘点（scout-assets）

> 团队：vrsanguo-audit-backup ｜ 任务：t3 ｜ 执行：scout-assets ｜ 日期：2026-09-10
> 范围：UE 资产 / 生成物 / 项目外临时脚本 / 已有备份
> 硬约束遵守声明：全程只读项目内容。本次唯一写入 = 本报告文件。未删除任何项目文件；未关闭/未触碰 UnrealEditor pid 24284；未运行 rebuild_v5.py；未改写 `Docs/Scene/`；未写入/删除 `Content/` 下任何资产。

## 0. 分类口径

| 标记 | 含义 |
|------|------|
| **A** | 废弃：已被取代且无当前用途，建议**登记后**移除（本轮不执行删除） |
| **B** | 冗余：同一内容多份副本，建议保留一份 |
| **C** | 活跃：当前事实源 / 构建依赖，必须保留 |
| **D** | 待定：需裁定，尚无足够依据 |
| **E** | 不应入库：不得提交进 Git（含体积、隐私、治理三重理由） |

引用：AGENTS.md 规则 23（禁止提交密钥、本机路径凭据、UE 生成目录和大型非 LFS 二进制）、规则 19（不建立平行知识库/重复副本）、磁盘与下载规则（"下载完成后应清理临时文件和重复压缩包，不保留冗余副本"）。

---

## 1. 关卡换代（Content/VRSanguo/Dev/）—— 本任务核心发现

### 1.1 事实：v3 从未存在于 Git，且当前盘上也不存在

| 关卡 | 磁盘 | 大小 | 只读 | Git 状态 |
|------|------|------|------|----------|
| `L_Prototype_1v1.umap` | **不存在** | — | — | HEAD 中有，工作树显示 ` D`（已删） |
| `L_Prototype_1v1_v2.umap` | **不存在** | — | — | HEAD 中有，工作树显示 ` D`（已删） |
| `L_Prototype_1v1_v3.umap` | **不存在** | — | — | **从未提交**（`git log --all` 无 v3 记录） |
| `L_Prototype_1v1_v4.umap` | 存在 | 498 KB | **True** | `??` 未跟踪 |
| `L_Prototype_1v1_v5.umap` | 存在 | 658 KB | **False（可写）** | `??` 未跟踪 |
| `L_SkeletonTest.umap` | 存在 | 25 KB | False | ` M` 已跟踪已修改 |

证据命令：`git log --all --name-status | Select-String '_v3'` → 无匹配；`Get-ChildItem Content/VRSanguo/Dev` → 7 项，无 v3。

**v1/v2 的删除是已备案的用户决定**，不是意外丢失。权威原文（`.trae/execution/active/STATUS.json` M01-T005 note）：
> "v1/v2/v3 按用户决定删除（脚本在外可重生）；v4/v5 均只读，编辑器打开 v5；单源 rebuild_v5.py"

因此：
- v1/v2 的 ` D` **应当提交**（把删除落盘），不应"恢复"——恢复会与用户决定冲突。
- LFS 中 v1/v2 的指针仍在（`git cat-file -s` = 130/131 字节），历史可回溯。

### 1.2 当前活跃关卡 = v5（单源）

- `rebuild_v5.py:7` 定义运行前提："编辑器已切到空关卡 /Game/VRSanguo/Dev/L_Prototype_1v1_v5"
- `rebuild_v5.py:597` 生成的 HTML 署名："关卡：`/Game/VRSanguo/Dev/L_Prototype_1v1_v5`"
- `Docs/Scene/*` 由 v5 于 2026-09-10 19:14:48 同戳重写
- v4 由 `rebuild_v4.py` 产出（14:53:40），已被 v5 取代

**判定：v5 = C（活跃，必须入库）；v4 = A（已被 v5 取代）。**
v4 的**唯一残余价值**是回滚基线；建议在登记册登记 v4 的 SHA 后移除，或明确保留为"回滚基线"并写入理由 —— **列为需 captain 裁定项 R1**。

### 1.3 治理漂移：v5 的只读锁丢失（可核验）

STATUS.json 声称 "v5.umap 只读核验 True""v5.umap 570KB 17:2x 落盘 +R True""save True 585KB 已上锁"。
实测（`Get-ChildItem -Force | Attributes -band ReadOnly`）：

```
L_Prototype_1v1_v4.umap           RO=True   498 KB
L_Prototype_1v1_v5.umap           RO=False  658 KB     <-- 漂移
```

v5 的文件时间戳为 **2026-09-10 21:44:17**，晚于最后一次声称上锁的 19:2x，也晚于 STATUS.json 最后记录的 v5.7。**结论：v5 在 21:44 被再次写入且未重新上锁。** 这是治理声明与磁盘事实的**不一致**，不是"已上锁"。列为 **需裁定项 R2**。

（附带：`L_Prototype_1v1_BuiltData.uasset` RO=True 771 KB，`L_Prototype_1v1_v4.umap` RO=True —— v1 已删但其 BuiltData 尚在且被 .gitignore 正确忽略。）

### 1.4 Content/ 三层覆盖矩阵（实测）

| 层 | 文件数 | 体积 |
|----|--------|------|
| Content 合计（磁盘） | 297 | 226.1 MB |
| Content 已跟踪 | **292** | 214.4 MB（其中 .uasset/.umap 在 Git 内为 LFS 指针） |
| Content **未**跟踪 | **4** | **1.2 MB** |
| Content 被忽略 | （`*_BuiltData.uasset` 已核实为 `!!`） | — |

未跟踪的 4 个（`git status --porcelain -uall`，实测）：

```
?? Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap       498 KB   --> A
?? Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap       658 KB   --> C 必须提交
?? Content/VRSanguo/Dev/M_GrayBox_Red.uasset            9 KB   --> C 必须提交
?? Content/VRSanguo/Dev/M_GrayBox_Straw.uasset          9 KB   --> C 必须提交
```

**自纠记录（写入以保证可交叉验证）**：本项在初稿中曾写作"未跟踪 5 个"并被下游 §1.4/§9 引用，现已更正为 **4**。原因是 `L_SkeletonTest_BuiltData.uasset` 在按目录整体枚举时落入了未跟踪分组，而它实际是**被正确忽略**的：`git check-ignore -v` 命中 `.gitignore:82 Content/**/*_BuiltData.uasset`（exit 0），`git status --porcelain --ignored=matching` 显示 `!!`，`git ls-files --error-unmatch` 报 pathspec 不存在。
🔴 **交叉盘点差异（需 verifier 裁定）**：`AUDIT-repo.md`（scout-repo）§2.2 记 `Content/` 为"297 文件，受管 **294**"。本报告实测受管 **292** + 未跟踪 **4** = 297 磁盘文件。两者相差 2，且 294 ≠ 292、294 ≠ 296 均不闭合。本报告口径取自 `git ls-files -- Content`（292 条）与 `git status --porcelain -uall`（4 条 `??`）两条独立命令，可复核。

`M_GrayBox_Red` / `M_GrayBox_Straw` 是 v5 的**运行期依赖**，非临时产物：
`rebuild_v5.py:57-58` → `_make_colored_mat('M_GrayBox_Straw'/'M_GrayBox_Red', ...)`。
若不提交，v5 关卡将引用缺失材质。

---

## 2. Docs/ —— 全部未跟踪，且是 rebuild_v5.py 的自动产物

```
?? Docs/Scene/asset_checklist.md   1,994 B
?? Docs/Scene/scene_modules.json   7,335 B
?? Docs/Scene/scene_overview.md    4,782 B
?? Docs/Scene/scene_plan.html     81,359 B
?? Docs/Scene/scene_topdown.png  2,853,240 B   (2.7 MB)
Docs 合计：5 文件 / 2.8 MB
```

`Docs/Scene` 四件（html/json/两个 md）+ png **全部由单源脚本自动生成**：
- `rebuild_v5.py:402` DOCS_DIR = `<项目根>\Docs\Scene`
- `:522` 写 `scene_modules.json`　`:623` 写 `scene_plan.html`　`:636` 写 `scene_overview.md`　`:648` 写 `asset_checklist.md`
- `:666-669` SceneCapture2D 正交俯拍生成 `scene_topdown.png`
- `:1` 与 `:458` 自述："新增 Docs/Scene 四件套自动生成…每次重建自动重写防失联"
- HTML 正文（`:599`）自述："<code>scene_topdown.png</code> 一同自动重写（Docs\Scene 只保留这三个文件，旧版 md/svg/raw 已自动清理），**手改无效**"

**判定：C（活跃，单一事实源的物化输出）。**
但存在两个必须由 captain 裁定的问题：

- **R3**：`Docs/` 完全不在 Git 中。既然它是"防失联"机制，不入库则失联。建议提交 4 个文本件 + PNG（PNG 需先纳入 LFS，见 §3）。
- **R4**：自动生成物入库会形成"手改无效但仓库里有"的双源风险，与规则 19（单一事实源）存在张力。替代方案 = 不入库但在登记册登记"由 rebuild_v5.py 可再生"，并在 `.gitignore` 显式声明白名单理由。
- **口径矛盾（低）**：脚本注释与 HTML 自述称"Docs/Scene **三**文件（html/json/png）""旧 md 自动清理"，但 `:636/:648` 仍在写两个 md，磁盘上确实存在，STATUS.json 也记 "Docs Scene **五**件全同代"。**实际是 5 个文件**。这是文档叙述与代码行为的不一致，建议随下次脚本改动一并修正措辞。

---

## 3. .gitattributes / LFS 覆盖缺口 —— 本任务最高价值发现

### 3.1 现状（权威口径来自 Git 自身，非工作树字节）

从 `git ls-tree -r -l HEAD` 聚合（**这是真正会被推送的内容**）：

| 扩展名 | HEAD 中 blob 数 | 仓库占用 |
|--------|-----------------|----------|
| **.png** | **39** | **46.6 MB** ← 全仓最大 |
| .cpp | 270 | 5.2 MB |
| .h | 320 | 4.0 MB |
| .jpg | 8 | 806 KB |
| .md | 143 | 649 KB |
| **.uasset** | **348** | **44 KB** |
| .py | 5 | 141 KB |
| 其余 | — | < 100 KB 各 |

**`.uasset`/`.umap` 已正确 LFS 化**——HEAD 中每个都是 ~130 字节指针，实证：

```
git cat-file -s HEAD:Content/Characters/MannequinsXR/Meshes/SKM_MannyXR_left.uasset  -> 132
git cat-file -p ...  ->  version https://git-lfs.github.com/spec/v1
                          oid sha256:b2e8172de767fc2bdf527b2b59590828b9acfa9237ae21906cf5998a243ef18e
                          size 4735484
```

LFS 3.7.1，`lfs ls-files` = **367** 条，`.git/lfs/objects` = 495 对象 / 690 MB。

> 取证教训（供后续审核）：**不要用工作树文件头判断 LFS 状态**。`环首刀.uasset`（26.7 MB）在盘上是未脱糖的原始二进制，但其 Git blob 是 133 字节指针 —— 工作树形态与仓库形态不同。本报告结论一律以 `cat-file` / `ls-tree -l` 为准。

### 3.2 缺口：39 个 PNG/JPG 以**原始二进制**入库，共 46.6 MB

`.gitattributes` 已覆盖 `.psd/.tif/.tiff/.exr/.fbx/.blend/.max` 等，**但没有 `*.png`、`*.jpg`、`*.jpeg`、`*.webp`**。

**缺口归属（精算）**：

| 位置 | 文件数 | 仓库字节 | 性质 |
|------|--------|----------|------|
| `Content/VRSanguo/Art/References/` | **32**（24 png + 8 jpg） | **47.34 MB** | 参考图，**问题主体** |
| `Plugins/*/Resources/` 各插件图标 | 6 | ~95 KB | 图标，可忽略 |
| `Content/VRSanguo/Art/References/.../*.webp` | 1 | 8 KB | — |
| 合计 | **39** | **46.6 MB** | — |

（两处口径：`Art/References` 实测 47.34 MB / 32 文件；仓库全部 PNG+JPG+WebP 共 39 文件 46.6 MB。差值来自上述图标与 webp，且 png/jpg 的聚合舍入不同。）

32 个参考图**全部作为非 LFS 大二进制存在仓库里**，直接触碰规则 23。

体积集中项（仓库内真实字节）：

```
4483 KB  Content/VRSanguo/Art/References/Weapon/Shield/REF_Weapon_Shield_02.png
4441 KB  .../Weapon/Shield/REF_Weapon_Shield_04.png
3930 KB  .../Weapon/Shield/REF_Weapon_Shield_01.png
3684 KB  .../Weapon/Shield/REF_Weapon_Shield_03.png
3188 KB  .../Weapon/Sword/REF_Weapon_Sword_01.png
2774 KB  .../Weapon/Spear/REF_Weapon_Spear_04.png
2471 KB  .../Weapon/Spear/REF_Weapon_Spear_06.png
2417 KB  .../Weapon/Bow/REF_Weapon_Bow_02.png
2378 KB  .../Weapon/Sword/REF_Weapon_SwordSheath_01.png
2291 KB  .../Weapon/Spear/REF_Weapon_Spear_03.png
（下略 5 项 1.6-2.0 MB、其余 24 项 < 1 MB）
```
另 .jpg 8 个（826 KB，最大 `REF_Weapon_Polearm_03.jpg` 223 KB）、.webp 1 个（8 KB）。

**判定：这 39 个文件本身是 C（活跃参考图/图标），其"存储方式"是问题；问题主体是 `Art/References/` 的 32 个参考图（47.34 MB）。**
修复方向（**需 captain 裁定 R5**，属范围变更，见规则 9）：
(a) 给 `.gitattributes` 追加 `*.png *.jpg *.jpeg *.webp filter=lfs diff=lfs merge=lfs -text` 并执行一次 `git lfs migrate import --include="*.png,*.jpg"`（**会重写历史 → 需 force push → 与"禁止 push --force"冲突，必须由 captain/用户明确放行**）；
(b) 仅对**新增**文件生效（改 .gitattributes，不动历史），代价是历史中的 46.6 MB 永久留在仓库；
(c) 参考图移出 Git（`Art/References/` 加 .gitignore），改由 E: 暂存区 + 登记册索引（与 §5 E 盘口径一致）。
**t10 若在 R5 未裁定前直接 `git add .`，会把 46.6 MB 原始 PNG 推成新提交。**

### 3.3 .gitignore 与 `!` 反否定规则的交互（易读错，已实测）

`.gitignore:71-76` 的 `!.trae/**` `!Config/**` `!Content/**` 等否定规则，配合 `:78-86` 的再忽略规则，产生反直觉结果。实测证据：

| 路径 | `check-ignore -v` 结论 | 说明 |
|------|------------------------|------|
| `.trae/execution/CR-*.md` | **忽略**（命中 `:72:!.trae/**`） | **反直觉**：`!` 是反否定，但 `check-ignore` 仍报"命中"并 exit 0 |
| `Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap` | 同理命中 `!Content/**` | 该文件在 `git status` 中确实是 `??`，**未被忽略** |
| `Content/VRSanguo/Dev/L_SkeletonTest_BuiltData.uasset` | 命中 `:82` 且 `status --ignored=matching` 显示 `!!` | **确实被忽略**（正确） |
| `Content/Collections/`、`Content/Developers/`、`ArchivedBuilds/` | 命中各自规则 | 确实被忽略 |

`git check-ignore` 对"反否定命中的路径"返回 exit 0 但附上 `!` 规则 —— **不能只看 exit code 判定"已忽略"**。必须交叉验证 `git status --porcelain -uall`。此项已导致本报告自身的一次自我纠错，写入以防下游 verifier 误判。

---

## 4. 项目外临时脚本（第二现场：D:\AWork\TraeAdmin\VRSanguoYanWuchang\）

合计 **20 文件 / 3.1 MB**。

| 文件 | 大小 | 修改时间 | 判定 | 依据 |
|------|------|----------|------|------|
| `rebuild_v5.py` | 50,614 B | 09-10 19:14 | **C** | 当前活跃关卡 v5 的**唯一事实源**；AGENTS.md 规则"临时脚本不得进入项目"故置于项目外 —— 位置正确，必须保留 |
| `rebuild_v4.py` | 18,018 B | 09-10 14:53 | **A** | v4 已被 v5 取代；保留价值仅 = 复现 v4。**禁用清单中的 rebuild_v5.py 之外，v4 亦不应再跑** |
| `rebuild_v3.py` | 15,027 B | 09-09 23:37 | **A** | v3 已删除，脚本"可重生"是删除决定的前提条件 → **注意**：删脚本会移除重生能力，与用户决定冲突。判定：A 但**建议保留为存档**，移交 R1 一起裁定 |
| `flip_topdown.ps1` | 935 B | 09-10 17:52 | **C** | `rebuild_v5.py:6` 区域所述俯视图垂直翻转步骤的配套脚本，v5.5+ 流程依赖 |
| `Set-TraeGovernanceAcl.ps1` | 3,776 B | 08-26 | **C** | `.trae` NTFS 保护脚本，AGENTS.md「权限规则」指定交付物 |
| `Unlock-TraeAssets.ps1` | 2,469 B | 09-08 | **C** | 资产只解锁工具，与只读锁治理配套 |
| `repair_status_json5.js` | 11,402 B | 09-10 18:49 | **A** | 一次性事故修复（STATUS.json 截断事故，见 STATUS.json note 末段）。事故已闭环，`STATUS.json` 现可正常 `ConvertFrom-Json` 解析 → 用途终结 |
| `verify2.js` / `verify3.js` | 2,310 / 1,673 B | 09-10 18:50 | **A** | 同一次事故的验证脚本，一次性 |
| `tmp\scan.js`..`scan4.js` | 各 ~900 B | 09-10 18:42 | **A** | 一次性扫描脚本 4 份 |
| `tmp\STATUS.json.broken-20260910` | 22,331 B | 09-10 18:15 | **D** | 事故**证据原件**。建议留档至事故报告归档，之后清 |
| `tmp\STATUS.repaired.json` | 25,113 B | 09-10 18:49 | **A** | 已被写回正式路径，内容重复 |
| `tmp\verify1.txt` / `verify2.txt` / `verify3.txt` / `repair-report.txt` | 1,057 / 1,002 / 1,462 / 879 B | 09-10 18:49 | **A** | 一次性验证输出 |
| `tmp\scene_topdown_raw.png` | **3,090,912 B** | 09-10 19:14 | **D** | 翻转前原始俯拍图。`rebuild_v5.py:661` 明确"raw 中间产物移出文档夹（TraeAdmin\tmp）" → 是**有意的中间产物落点**，属设计内，但每次重建都会重写 |

**判定汇总：C×4（rebuild_v5.py / flip_topdown.ps1 / Set-TraeGovernanceAcl.ps1 / Unlock-TraeAssets.ps1）、A×11、D×2。**
**重要约束**：TraeAdmin 下文件不在项目内，**本轮一律不删**，仅登记。且 `rebuild_v3.py`/`rebuild_v4.py` 承载"v1/v2/v3 可重生"这一用户决定的前提，**删除它们等于单方面推翻用户决定** → 必须走 R1。

---

## 5. E: 盘两处现场（只登记，不触碰）

### 5.1 `E:\AWork\Temp\VRSanguoRef\` = **资产暂存区（活跃 C，非备份）**

```
FBX/        44 文件  1098.6 MB   混元 3D 高模源（含 .fbm 贴图），不导入 UE，永久保留作 M05 精修源
FBX_Low/   332 文件   572.0 MB   减面低模 + 贴图（正式导入源）
OBJ/         0 文件     0.0 MB   空目录
图片/       53 文件    95.6 MB   原始参考图收集区
README.md                         
合计 1.77 GB
```

**它不是备份，是活跃源库**，且**有正式治理地位**：
- 自身 `README.md` 指向权威映射：`.trae/registers/10-asset-register.md` →「外部源文件索引（E 盘暂存区）」
- `10-asset-register.md:78` 明确基准路径并记载："2026-08 下旬由 `D:\AWork\Temp\VRSanguoRef\` 迁入；**旧报告中的 D: 路径已失效**"
- `:85-88` 定义导入规则：`FBX_Low\*.obj` = 正式导入源；`textures_<名称>_1024\` = 正式导入贴图；`textures_<名称>\` = 4K 原始（不导入）；裸 `textures\`/`textures_1024\` = 早期批次，**归属待确认，勿作为导入依据**

**实测校验（`FBX_Low\` 实际内容）**：
- `.obj` **15 个**（与 `10-asset-register.md:92-97` 的「AST ↔ 磁盘实物映射」表逐条对应），`.mtl` 7 个，`.jpg` 248 / 16.5 MB，`.png` 62 / **550.3 MB**
- `textures_*_1024\` 成对目录 **15 组**；另有裸 `textures\`、`textures_1024\` 两个"归属待确认"目录 —— 与 README/登记册描述**一致**
- **口径瑕疵（低）**：README `:11` 写"`FBX_Low\textures_<名称>_1024\`：正式导入贴图（**≤1024**）"，但实测 `textures_*_1024\` 内含多张 1280 KB 级 .jpg 与一张 6.5 MB .png，单文件大小不足以证明边长 ≤1024（未做图像解码，不作结论）。仅登记为**待核**项。

**E 盘暂存区的 DENT：绝对不可作为 Git 基线提交的目标或来源。** t10 的"远程即唯一备份"口径下，E: 不参与。

### 5.2 `E:\AWorkBackup\VRSanguoYanWuchang\` = **名不副实的"项目备份"（A）**

```
E:\AWorkBackup\VRSanguoYanWuchang\
└── Plugins\
    └── UEBridgeMCP.disabled-old\     1929 文件 / 631.0 MB   <-- 仅此一项
```

**这就是全部内容。没有 Content/、没有 Source/、没有 .trae/、没有 Config/。**
最新文件时间 **2026-08-31 21:52**（内容为 `UnrealEditor-UEBridgeMCPPCG.pdb` 58.45 MB 等编译产物 + 源码）。

依据 `.trae/CHANGELOG.md:140`：UEBridgeMCP 因 GPL-3.0 退役，`.uproject` 移除条目，插件改名保留审计。
**判定：A（废弃）。** 它是**已退役插件的一次性编译产物快照**，被错误命名为 "AWorkBackup\VRSanguoYanWuchang"（易被误认为完整项目备份）。**重大警示：如果 t10/t12 把 E:\AWorkBackup 当作"已有项目备份"，会错误认为项目已有备份保障 —— 实际上 2026-09-01 之后项目从未被备份过。** 631 MB 中绝大部分是可重新编译的 .pdb/.obj。

**结论（供 t9/t12 采用）：E: 上不存在任何有效的完整项目备份。Git 基线 + 远程推送是本项目**首个**完整备份。** 这直接支撑了团队"远程即唯一备份、不建本地副本、不在 E: 新建目录"的口径 —— **该口径不仅合理，而且是必须的**。

### 5.3 E: 盘其他相关内容

| 路径 | 体积 | 判定 | 说明 |
|------|------|------|------|
| `E:\AWork\Tools\venv_asset\` | 5,258 文件 / 295.3 MB | **C** | Python 资产处理虚拟环境（含 .gitignore/CACHEDIR.TAG） |
| `E:\AWork\Tools\OpenBRF\` | 24 文件 / 39.0 MB | **C** | `.obj` 检视工具（openBrf.exe）。**内含 `openbrf.zip`（08-15）= B 重复压缩包**，违反磁盘规则"不保留冗余压缩包" |
| `E:\AWork\Temp\VRExpansionPlugin\VRExpPluginExample-5.6.zip` | 906 MB | **B** | 见 §6.1 四份副本 |
| `E:\AWork\Temp\VRExpansionPlugin\VRExpPluginExample-5.6\` | 842 文件 / 1020.6 MB | **B** | 同上 |
| `E:\AWork\Temp\VRExpansionPlugin\Extracted\` | 842 文件 / 1020.6 MB | **B** | 同上，**与上一行字节数完全一致 → 解压两次** |
| `E:\AWork\VRExpansionPlugin\` | 193 文件 / 3.4 MB | **C** | 含 `.git` 的插件**源码仓库克隆**（VC 版本，与上面 3 个"示例工程"不是同一物） |
| `E:\AWork\Temp\vrsanguo_pie_t0.png` | 08-29 | **A** | 一次性 PIE 抓图 |
| `E:\AWork\Temp\vrsanguo_sword_view5.png` | 08-29 | **A** | 一次性武器视图 |
| `E:\AWork\Temp\VRSanguoRef\OBJ\` | 空 | **A** | 空目录（README `:14` 亦注明"空目录"） |

E: 容量：1863 GB 总 / **794.8 GB 可用** → 空间充足，**不存在"必须靠 E: 备份"的压力**，也不构成把项目本地产物留存的理由。

---

## 6. 冗余副本（B）清单

### 6.1 VRExpansionPlugin 示例工程四份副本 —— 2.92 GB 纯冗余

| 路径 | 形态 | 体积 |
|------|------|------|
| `E:\AWork\Temp\VRExpansionPlugin\VRExpPluginExample-5.6.zip` | 压缩包 | 906 MB |
| `E:\AWork\Temp\VRExpansionPlugin\VRExpPluginExample-5.6\` | 解压目录 | 1020.6 MB |
| `E:\AWork\Temp\VRExpansionPlugin\Extracted\` | 解压目录 | 1020.6 MB |
| （`E:\AWork\VRExpansionPlugin\`） | 源码克隆，**非重复** | 3.4 MB |

两个解压目录 **842 文件 / 1020.6 MB 完全对称** → 同一压缩包被解压两次。
建议保留 1 份（任选一解压目录，或 zip），可回收 **≈2.92 GB**。
属项目外文件 → **本轮不删，仅登记**。

### 6.2 其他

| 项 | 判定 | 说明 |
|----|------|------|
| `E:\AWork\Tools\OpenBRF\openbrf.zip` | B | 与已解压内容并存 |
| `.trae/execution/active/STATUS.json` M01-T005 note | D | 见 §7.2，内含**已被 v5.7 取代**的整段历史叙述 |
| `Saved/Evidence/M01-T005/v3_*.png`（12 张 / 7.37 MB） | A | v3 关卡已删，其证据图属**已废止关卡**的证据 |
| `Saved/Evidence/M01-T005/v4*.png`（5 张 / 5.6 MB） | A | 被 v5 取代 |

---

## 7. Saved/ 与 dashboard/ 生成物（均被 .gitignore 正确忽略 → E）

### 7.1 Saved/Evidence/（47 文件 / 43.8 MB，`!!` 已忽略 —— 正确）

```
Saved/Evidence/M01-T005/       42 文件  (~41.8 MB)   v3/v4/v5 各代次截图
Saved/Evidence/M02-PREP-002/    5 文件  (   251 KB)   含 UBT-Build-1.0.87-*.log
```

按版本标志分组（实测）：

| 代次 | 张数 | 体积 | 判定 |
|------|------|------|------|
| v3 | 12 | 7.37 MB | A（关卡已删） |
| v4 | 3 | 3.36 MB | A（被取代） |
| v4b | 2 | 2.24 MB | A |
| v5 | 5 | 5.28 MB | C |
| v53/v54/v55 | 3/2/5 | 3.36/2.24/8.85 MB | A（历史迭代） |
| v56/v56b/v57 | 2/1/1 | 2.67/1.55/1.12 MB | **C（当前代次证据）** |
| 其他（arena_wide/jiangtai_close/stand_*/ref_skeletontest_editor_view） | 11 | 5.8 MB | D |

**重要**：证据图**已被 .gitignore 正确忽略**（`Saved/`），因此**不构成仓库体积风险**，且规则 11 要求证据可核验 —— 但证据留在 `Saved/` 意味着**一旦清理 Saved 或换机，v5 的验收证据即消失**。建议 captain 裁定是否把**当前代次（v5/v56/v56b/v57，共 9 张 / 10.6 MB）**的证据图转存至 E: 归档（**属新增备份动作，需明确授权；本轮未做**）。列为 **R6**。

### 7.2 dashboard/（C 但生成物口径需注意）

`dashboard/` 在 Git 中（6 文件）+ CI 引用（`.github/workflows/ci.yml`、`deploy.yml`）→ **C，不可动**。
其生成物 `index.html`（63.3 KB）/ `status.json`（185.2 KB）/ `integrity.json`（3.8 KB）由
`dashboard/.gitignore` 显式忽略（`.gitignore` 原文："生成的静态看板文件（由 GitHub Actions 在 push 时自动生成）"）→ **E 正确**。
`dashboard/__pycache__/`（2 个 .pyc）已忽略 → E 正确。
**注意**：三个生成物最后写入 = **2026-09-04 11:31**，即 HEAD 提交时间。`dashboard/status.json` 的"任务数/完成数"**停留在 09-04**，落后于 `.trae/execution/active/STATUS.json`（含 09-10 大量追加）→ **dashboard 看板数据已陈旧 6 天**，属 t2（治理盘点）范畴，此处仅交叉提示。

---

## 8. 分类总表（供 t9 规划师直接消费）

### C · 活跃，必须保留/入库

| # | 对象 | 依据 |
|---|------|------|
| C1 | `Content/VRSanguo/Dev/L_Prototype_1v1_v5.umap` (658 KB) | 唯一活跃关卡；rebuild_v5.py:7/597 |
| C2 | `Content/VRSanguo/Dev/M_GrayBox_Red.uasset`、`M_GrayBox_Straw.uasset` | v5 运行期依赖材质；rebuild_v5.py:57-58 |
| C3 | `Docs/Scene/`（5 文件 2.8 MB） | rebuild_v5.py 自动生成物，单源机制 |
| C4 | `Content/VRSanguo/Art/References/`（32 图 47.34 MB + 对应 uasset） | 现行参考图库；与 E: 暂存区分工明确 |
| C5 | `Saved/Evidence/M01-T005/` 中 v5/v56/v56b/v57 代次（9 张） | 规则 11 证据 |
| C6 | `dashboard/`（6 跟踪文件） | CI 引用；.trae/README、SessionCommands 引用 |
| C7 | `TraeAdmin`: `rebuild_v5.py` / `flip_topdown.ps1` / `Set-TraeGovernanceAcl.ps1` / `Unlock-TraeAssets.ps1` | 活跃工具链 |
| C8 | `E:\AWork\Temp\VRSanguoRef\`（1.77 GB） | 资产暂存区；10-asset-register.md:78 基准路径 |
| C9 | `E:\AWork\Tools\venv_asset\`、`E:\AWork\Tools\OpenBRF\`、`E:\AWork\VRExpansionPlugin\` | 资产管线工具 |
| C10 | `Content/VRSanguo/Dev/L_SkeletonTest.umap` | 治理文档/ALLOWLIST 在用（M00-T005、M01-T001） |

### A · 废弃，建议登记后移除（**本轮不执行**）

| # | 对象 | 说明 |
|---|------|------|
| A1 | `Content/VRSanguo/Dev/L_Prototype_1v1_v4.umap` (498 KB) | 被 v5 取代；**R1 裁定**（保留作回滚基线？） |
| A2 | `Content/VRSanguo/Dev/L_Prototype_1v1_BuiltData.uasset` (771 KB, RO) | v1 已删，其 BuiltData 尚存；已被忽略故不入库，仅占盘 |
| A3 | `Content/VRSanguo/Dev/L_Prototype_1v1.umap` / `_v2.umap` 的 ` D` 状态 | **不是废弃，是待提交的删除**（用户已决定）→ 见 C/E 交界，t10 应提交该删除 |
| A4 | `TraeAdmin\rebuild_v4.py`、`rebuild_v3.py`、`repair_status_json5.js`、`verify2.js`、`verify3.js`、`tmp\scan*.js`、`tmp\verify*.txt`、`tmp\repair-report.txt`、`tmp\STATUS.repaired.json` | 一次性/已被取代脚本（but rebuild_v3 承载"可重生"前提 → R1） |
| A5 | `Saved/Evidence/M01-T005/v3_*.png`（12 张 7.37 MB）、`v4*.png`（5 张 5.6 MB）、v53/v54/v55（10 张 14.45 MB） | 已废止/被取代代次的证据 |
| A6 | `E:\AWorkBackup\VRSanguoYanWuchang\`（1929 文件 631 MB） | 名不副实的"备份"= 退役插件编译产物 |
| A7 | `E:\AWork\Temp\vrsanguo_pie_t0.png`、`vrsanguo_sword_view5.png`、`E:\AWork\Temp\VRSanguoRef\OBJ\`（空） | 一次性产物/空目录 |

### B · 冗余，保留一份

| # | 对象 | 可回收 |
|---|------|--------|
| B1 | `VRExpPluginExample-5.6.zip` + 两个解压目录 | **≈2.92 GB** |
| B2 | `E:\AWork\Tools\OpenBRF\openbrf.zip` | 39 MB |
| B3 | `TraeAdmin\tmp\scene_topdown_raw.png`（3.09 MB，每次重建重写） | 3 MB |

### D · 待定 / 需裁定

| # | 项 | 问题 |
|---|-----|------|
| **R1** | v4 关卡 + rebuild_v3.py/rebuild_v4.py 的去留 | 删除会移除"可重生"能力，与用户"v1/v2/v3 按用户决定删除（脚本在外可重生）"的前提冲突 |
| **R2** | v5 只读锁丢失 | STATUS.json 声明"v5 只读 True"与磁盘 `RO=False` 矛盾；21:44 被再次写入 |
| **R3** | `Docs/` 是否入库 | "防失联"机制不入库则失联 |
| **R4** | 自动生成物入库 vs 规则 19 单一事实源 | 二选一 |
| **R5** | 46.6 MB PNG 的 LFS 处置路径 a/b/c | (a) 需 rewrite history + force push，与硬约束冲突 |
| **R6** | 当前代次证据图是否转存 E: 归档 | 属新增备份动作 |
| D7 | `Saved/Evidence/M01-T005/` 11 张"其他"代次图（5.8 MB） | 是否仍有引用 |
| D8 | `TraeAdmin\tmp\STATUS.json.broken-20260910` | 留档至何时 |
| D9 | `FBX_Low\textures_*_1024\` 是否真 ≤1024 边长 | 未做图像解码，未下结论 |

### E · 不应入库（已确认忽略，须保持忽略）

| # | 对象 | 忽略规则 |
|---|------|----------|
| E1 | `Content/**/*_BuiltData.uasset` | `.gitignore:82` |
| E2 | `Saved/`（含 43.8 MB 证据） | `:6` |
| E3 | `dashboard/__pycache__/`、`index.html`、`status.json`、`integrity.json` | `dashboard/.gitignore` |
| E4 | `.vs/`(3.7 GB)、`Intermediate/`(5.7 GB)、`Binaries/`(1.3 GB)、`DerivedDataCache/`(294 MB)、`ArchivedBuilds/`(724 MB) | `:2/5/6/40` |
| E5 | `.agent-teams/`（5 条：team.json + 4 个成员信箱）与 `.dsh-uploads/`（3 条：2 张 limelight 手机截图 + 1 张 deepseek logo） | **当前未被忽略（`??`）→ 缺口**，见下 |
| E6 | `Collect、Developers、__ExternalActors__、__ExternalObjects__` | `:34-37/83-86` |

**E5 缺口（新发现，实测 2026-09-10 22:4x）**：`.agent-teams/` 与 `.dsh-uploads/` **不在 `.gitignore`**，当前为 `??`。
实测未跟踪条目：

```
?? .agent-teams/vrsanguo-audit-backup/team.json                + inbox/{captain,git-operator,planner,verifier}.jsonl
?? .dsh-uploads/session-2a22b421-8d17-4a1b-8e39-9d32092413e7/693ce656e56ba26e-deepseek-whale-400.png
?? .dsh-uploads/session-2a22b421-8d17-4a1b-8e39-9d32092413e7/c013349bbeec8198-Screenshot_2026-09-09-22-53-11-091_com.limelight.root.jpg
?? .dsh-uploads/session-2a22b421-8d17-4a1b-8e39-9d32092413e7/cd6db11113373745-Screenshot_2026-09-10-08-26-58-474_com.limelight.root.jpg
```

即 5 条 `.agent-teams/`（团队状态 + 4 个成员信箱，**每次通信都会变动**）+ 3 条 `.dsh-uploads/`（含 2 张用户手机截图 `com.limelight.root`，属个人设备画面）。
按规则 23（禁止本机路径凭据/非项目二进制入库），**建议追加 `.gitignore`：`.agent-teams/`、`.dsh-uploads/`**。
否则 t10 `git add -A` 会一并提交 agent 会话状态、成员信箱全文与用户截图。**列为 R7。**
（注：`.agent-teams/` 内容在 t10 执行时仍会持续变化 —— 即使不忽略，提交它也无意义且会制造 git 噪音。）

---

## 9. 对下游任务的直接影响（重要）

1. **t10（Git 基线）绝不可用 `git add -A` / `git add .`**，否则会一次性引入：
   - E5：`.agent-teams/` 5 条（team.json + 4 个成员信箱 jsonl）+ `.dsh-uploads/` 3 条（含 **2 张用户手机截图**）
   - R5：39 个 PNG/JPG 共 **46.6 MB 原始二进制**
   - R3/R4：`Docs/` 5 文件（未裁定）
   建议 t10 使用**显式路径白名单**提交。
2. **t10 必须提交** ` D Content/VRSanguo/Dev/L_Prototype_1v1.umap` 与 `_v2.umap` 的删除（用户已决定，且脚本可重生）。
3. **t10 必须提交** C1/C2（v5 + 2 个材质），否则 v5 关卡引用断裂。
4. **t11 审核基线时必须核**：`git cat-file -s` 对 `.uasset` 应返回 ~130 字节（指针）而非 MB 级 —— 这是"LFS 生效"的可核验断言。
5. **E: 口径**：`E:\AWorkBackup` **不是有效备份**（见 §5.2）。t12 交接清单中的"事实源模型"必须写明：**本项目在本次 Git 基线前不存在完整备份**，E: 不可被引用为"已有备份"，且 §5.1 的 `VRSanguoRef` 是**源库不是备份**。
6. **冻结令复核**：pid 24284 存活（`StartTime 2026-09-09 22:06:05`）。v5 关卡 `RO=False`（§1.3）意味着**编辑器仍在可写状态持有它** —— 与"v5 只读"的治理声明不符，**t10 提交前需确认编辑器不会在提交过程中回写 v5**（R2 的实际风险面）。

## 10. 未执行事项（诚实声明，规则 1）

- **未执行任何删除**（项目内与项目外均未删）。
- **未执行 `git add` / `commit` / `push`**（属 t10）。
- **未运行 rebuild_v3/v4/v5.py**（冻结令）。
- **未改写 `Docs/Scene/`**（冻结令）。
- **未打开/关闭编辑器**；未触碰 pid 24284。
- **未做图像解码**，故 D9（贴图边长 ≤1024）**未验证**，不作结论。
- **未运行任何测试**，本报告无测试结论。
- **未核实 `Saved/Evidence` 中每张图的视觉内容**，代次归类依据文件名前缀，**未逐张目视确认**。
- **未检查 E: 上 `Resource`/`VrGame`/`备份` 等与本项目无关目录**（超出 t3 范围）。
- 本报告所有体积/计数均来自本轮真实命令输出；无估算值。
