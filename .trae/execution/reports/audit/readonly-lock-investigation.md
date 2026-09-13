# 只读锁来源与复发风险排查报告

| 项 | 值 |
|---|---|
| 任务来源 | 指挥台派工（ref：只读锁排查） |
| 执行会话 | readonly-scout |
| 取证窗口 | 2026-09-13 11:02 – 11:20（本地时间） |
| 工作目录 | `D:\AWork\Unreal\Project\VRSanguoYanWuchang` |
| 红线遵守 | 全程只读。未执行 `attrib ±R` / `Set-ItemProperty` / `Set-Acl`；未改任何文件属性、内容、权限；未移动/删除/重命名任何文件；未触碰任何 `UnrealEditor*` 进程（唯一实例 pid 30604 自 09-12 22:51:24 起存活，未受干扰）；未删除或移动 `Saved\Crashes\` 下任何文件；未运行 `rebuild_v5.py`；未改写 `Docs/Scene/`；临时文件仅写 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\`（含本会话新增的 `content_ro.xml` / `content_all.xml`，未删除，见「仍未取到数」） |

---

## 结论摘要

1. **分界线：只读位只落在 `.uasset` / `.umap` 上，且这 150 个文件全部是 Git LFS 跟踪对象（LFS ⊇ 只读，99 个 LFS 文件非只读）。** 它不是文件类型规则、不是 git 自动行为、也不是第三方工具造成的 —— 是**人为逐文件挑选**的结果（见 §2.4 反例：同一提交、同型同尺寸的两个 LFS 指针文件，一个只读一个不读）。
2. **总量：`Content\` 下 298 文件，150 只读 —— 即 `.uasset` 237 个中 147 个、`.umap` 4 个中 3 个，其余扩展名（png/fbx/jpg/gitkeep/md/webp）零只读。另有 `Plugins\` 下 115 个 uasset 只读。** 用户此前听到的「155」与实测 150 不符，差 5，未取到该数字的来源。
3. **「不该只读但只读」的项目自有资产 = 44 个，清单见 §3**（不是上游说的 8 个）：`VRSanguo\` 内 40 个（32 参考图 + 5 灰盒/关卡 + 3 材质），加 `VRSpectator` / `Weapons` 内 4 个被顺带锁上的在用资产。
4. **源头：未取到「最初是谁批量设的」。** 但取到了**性质**：这是项目**有意的「只读保护」治理姿态**，且在项目文档中被明确记录为「治理设计」（`CR-20260907-001` §42）。机制主体是**项目外部管理员脚本 + 关卡重建流程 + 编辑会话的解锁-改-再锁三步操作**。
5. **会不会复发：会，而且有三个已确证的复发源**（§5）：
   - `Unlock-TraeAssets.ps1 -Restore` 会**递归** `attrib +R`（**唯一正在使用的自动重锁器**）；
   - `Unlock-GripPolish.ps1 -Restore` 会把 `L_SkeletonTest.umap` 重新锁上（该文件正是 09-12 14:53 那次闪退的触发文件）；
   - M01-T005 重建流程**每轮重建后都重新 +R**，STATUS.json 的 note 里 `save True+R` 出现 3 次、`+R True` 2 次、`两 umap +R 恢复` 1 次。
6. **闪退根因与只读的关系已由另一会话确证（我复核了原文）**：12 次闪退中 **3 次是 C 类**，都是**自动化桥保存只读文件 → `LogSavePackage: Error: Cannot remove … as it is read only` → `appError` → 编辑器 Assert 终止**（14:53 `L_SkeletonTest.umap`；22:20:55 与 22:29:37 均 `BP_VRCharacter.uasset`）。**桥不设只读，桥只是撞上只读**；但桥在崩溃循环中反复重试同一保存。
7. **当前即时风险：低（非零）。** 活日志尾部无保存失败（编辑器自 09-13 03:06 起空闲）；但 `L_Prototype_1v1_v5.umap` **仍为只读**、且**仍被这个存活的编辑器会话持有** —— 一旦有保存动作落到它身上，会按同一路径再炸一次。
8. **已排除（§4 有证据）**：OneDrive 云同步、杀毒/EDR、Perforce/SVN/Plastic、UE 源码管理 Provider、git index/LFS lock 状态、ACL 差异、Windows 计划任务（上游已排）、AgentHub（上游已排）。
9. **防复发建议（§6，未执行）**：把「只读保护」从「文件属性」改为「显式清单 + 只读校验门禁」，并**禁止用递归 `attrib +R` 覆盖含活资产的目录**。

---

## 1. 全量现状表（分界线的形状）

### 1.1 `Content\` 按扩展名

| 扩展名 | 总数 | 只读 | 说明 |
|---|---|---|---|
| `.uasset` | 237 | **147** | 全部 LFS `lockable` |
| `.umap` | 4 | **3** | 全部 LFS `lockable` |
| `.png` | 24 | 0 | 非 lockable |
| `.gitkeep` | 14 | 0 | 非 lockable |
| `.fbx` | 9 | 0 | LFS 但非 `lockable` |
| `.jpg` | 8 | 0 | 非 lockable |
| `.md` / `.webp` | 1 / 1 | 0 | — |

**只读集合 = `.uasset` ∪ `.umap` 内被挑选的 150 个，0 例外。**

### 1.2 `Content\` 按目录（只读率）

| 目录 | 总 | 只读 | 率 |
|---|---|---|---|
| `Characters\MannequinsXR` | 53 | 53 | 100% |
| `LevelPrototyping\Interactable` | 19 | 9 | 47% |
| `LevelPrototyping\Materials` | 7 | 3 | 43% |
| `LevelPrototyping\Meshes` | 8 | 3 | 38% |
| `VRSanguo\Art` | 65 | 32 | 49% |
| `VRSanguo\Dev` | 7 | 5 | 71% |
| `VRSanguo\VR` | 15 | 3 | 20% |
| `VRTemplate`（除 Input 的 36 个） | 70 | 36 | 100% |
| `VRTemplate\Input` | 34 | **2** | 6% |
| `Weapons\Pistol` / `Rifle` | 9 / 9 | 2 / 1 | — |
| 其余 VRSanguo 子目录、`VRSpectator\Input` 等 | — | 0 | 0% |

### 1.3 `Plugins\`

`Plugins\` 共 1869 文件，**只读 115 个，100% 为 `.uasset`**，全部位于 `Plugins\PICOOpen174f9f81d266V8\Content\`（Meshes 53 / Materials 21 / Textures 9 / UI 10 / DevTools 7 / TileVisualizer 5 …）。这是 PICO 插件随包分发的资产。

### 1.4 `Content\` 之外的项目自有目录

`Config` 0/10 只读、`Source` 0/44、`Docs` 0/5、`.trae` 0/206、`Build` 0/195、根级 8 个文件全非只读。**⇒ 只读位的施加范围覆盖 `Content\` 与 `Plugins\<vendor>\Content\`，不覆盖 `Config`/`Source`/`.trae`。**

---

## 2. 是什么设的（逐项排除 + 正向证据）

### 2.1 第三方工具：全部排除

| 嫌疑源 | 判定 | 证据 |
|---|---|---|
| OneDrive / 云同步 | **排除** | 进程存在（pid 32744，09-13 05:46:45 启动）但只读文件 mtime 全为**编辑器级精度**（含非零亚秒 + 非整偶秒，如 `M_FlatCol` mtime `2026-08-20 23:52:16`），非同步工具回写特征；且 `Content\MannequinsXR` 等目录只读文件 mtime 最早（08-10），云同步不会只挑 uasset |
| 杀毒 / EDR | **排除** | 无相关进程；只读集合与扩展名严格相关（`.png`/`.fbx` 一律不读），安全软件不按此规则 |
| Perforce / SVN / Plastic | **排除** | 客户端均未安装运行；`Saved\Config\WindowsEditor\EditorPerProjectUserSettings.ini` 内各 Provider 仅存 `TimeStamp=2026.08.10-06.31.xx` 初始化残留，无活动 |
| git / Git LFS 自动置只读 | **排除（反例）** | git index 无只读语义：`core.filemode=false`，`git ls-files -s` 抽样全部 `100644`；LFS 锁缓存为空（`git lfs locks` 空输出；`.git/lfs/cache/locks/refs/heads/master/remote` = `[]`，`verifiable` = `{"ours":[],"theirs":[]}`）；**且同类文件一半只读一半不读**（见 §2.4） |
| ACL 差异 | **排除** | 只读文件与非只读文件 ACL **逐条完全相同**：`BUILTIN\Administrators FullControl(inherited)` / `NT AUTHORITY\SYSTEM FullControl(inherited)` / `NT AUTHORITY\Authenticated Users Modify(inherited)` / `BUILTIN\Users ReadAndExecute(inherited)`，Owner 均为 `DESKTOP-HEUDI0T\PC`。只读纯粹来自 NTFS **R 属性位**（`attrib` 输出 `A    R`） |
| UE 源码管理 Provider | **排除** | `Config\DefaultGame.ini` / `DefaultEngine.ini` 无任何 `SourceControl` 键；用户配置内无 `[General] Provider=` 行（只有工具栏开关 `SourceControlPreferences.SourceControl=True`） |

### 2.2 正向证据一：项目文档把它定义为「治理设计」

`.trae/execution/CR-20260907-001-imc-pico4-keys.md:42`：

> **落盘被 NTFS 只读保护正确拒绝**（`Content/VRTemplate/Input/*.uasset IsReadOnly=True`，**治理设计**；日志实锤 `Cannot remove ... as it is read only`）—— 按 AGENTS.md 权限规则不绕过 ACL。

`.trae/execution/sessions/session-20260830-001.md:283-287`（08-30 会话，最早明确记录）：

> - `环首刀.uasset`、`L_SkeletonTest.umap` 均 `IsReadOnly=True` → UE `SaveAsset`/`SaveDirtyPackages` 全部失败
> - **`Content\VRSanguo` 下 49 个 uasset/umap 全为只读（仅 2 个非只读）——目录被批量设过只读保护。**
> - 处置：**临时清除 2 个目标文件只读 → 保存 → 复核落盘 → 恢复只读（保住保护姿态）。**

⇒ 「批量设只读」在 **08-30 之前**已存在，并且**项目自己是知情的、且主动维持**。

### 2.3 正向证据二：具体执行只读位的脚本（均在项目外管理员目录）

目录：`D:\AWork\TraeAdmin\VRSanguoYanWuchang\`

| 脚本 | 创建 | 作用 |
|---|---|---|
| `Unlock-TraeAssets.ps1` | 08-26 | 目标 = `Content\VRTemplate\Input\` + `Content\VRSanguo\VR\BP_VRCharacter.uasset`。`-Restore` 分支：`Get-ChildItem -Recurse -File \| ForEach-Object { attrib.exe +R $_.FullName }` —— **递归 +R**，并 `attrib.exe +R $t`（目录本身）+ `icacls /remove` |
| `Unlock-GripPolish.ps1` | 09-10 22:40 | 目标 = `Content\VRSanguo\VR\Mesh\`（目录级递归）+ `Content\VRSanguo\Dev\L_SkeletonTest.umap`。同款 `-Restore` 递归 `attrib +R` |

这两个脚本的存在解释了 `Content\VRTemplate\Input\` 为何是 **34 个里只读 2 个**的反常态：`Unlock-TraeAssets.ps1`（08-26）已把该目录递归解锁，而**该目录从未跑过 `-Restore`**（`IMC_Weapon_Left/Right.uasset` 与 `BP_VRCharacter.uasset` 是事后被单独重新锁上的，mtime 分别是 09-08 22:26 与 09-12 23:01）。

### 2.4 正向证据三：只读是「人工挑选」，不是任何自动化规则（决定性反例）

`Content\LevelPrototyping\Materials\` 下两个文件在**每一个可查维度上完全相同**，只读状态却相反：

| 维度 | `M_FlatCol.uasset` | `MF_ProcGrid.uasset` |
|---|---|---|
| IsReadOnly | **True** | **False** |
| 首次入库提交 | `98b2eb7`（2026-08-09 21:49） | `98b2eb7`（2026-08-09 21:49） |
| git 对象内容 | `version https://git-lfs.github.com/spec/v1`（LFS 指针） | 同左 |
| `.gitattributes` 规则 | `*.uasset filter=lfs … lockable` | 同左 |
| CreationTime | 2026-08-10 16:41:43 | 2026-08-10 16:41:43 |
| ACL | 继承四条目 | 同左 |
| index mode | `100644` | `100644` |

两人同一次解包、同一提交、同一规则、同一时间 —— 只有 R 位不同。**⇒ 只读位由人（或人工编排的清单）逐个文件施加。**

同类第二个反例：`Content\Weapons\Rifle\` 下 `M_Weapon.uasset`（unreal 自动生成）只读，而 `Meshes\SM_Rifle.uasset`、`SK_Rifle.uasset`、`Textures\T_Rifle_*.uasset` 全部非只读 —— 全都在同一次 08-10 16:41:43 解包内。

---

## 3. 「不该只读但只读」全清单（44 个）

判定口径：位于项目自有目录（`VRSanguo\`）且属使用者需要编辑的活资产（蓝图、关卡、材质、网格）。

### 3.1 `VRSanguo\Art\References\`（32 个）

纯参考图资产（只作建模参照，不进游戏），锁上损失最小、动机最合理，但仍属「不该只读」：

```
Armor\REF_Armor_Helmet_01..05.uasset (5)
Armor\REF_Armor_TieJia_01.uasset
Armor\REF_Armor_YulinJia_01.uasset
Armor\REF_Armor_YulinJia_02.uasset
Unit\REF_Unit_Soldier_01.uasset
Weapon\Bow\REF_Weapon_Bow_01..02.uasset (2)
Weapon\Polearm\REF_Weapon_Polearm_01..03.uasset (3)
Weapon\Shield\REF_Weapon_Shield_01..04.uasset (4)
Weapon\Spear\REF_Weapon_Spear_01..07.uasset (7)
Weapon\Sword\REF_Weapon_Sword_01..06.uasset (6)
Weapon\REF_Weapon_SwordSheath_01.uasset
```
全部 CreationTime `2026-08-16 11:44:03–11:44:04`（同一批导入）。

### 3.2 `VRSanguo\Dev\`（5 个）

| 文件 | mtime | 只读的已知理由 |
|---|---|---|
| `L_Prototype_1v1_v5.umap` | 2026-09-11 23:27:31 | **M01-T005 重建流程刻意 +R（活资产，最高风险）** |
| `L_Prototype_1v1_v4.umap` | 2026-09-10 15:07:13 | 同上（已封存快照，风险次之） |
| `L_Prototype_1v1_BuiltData.uasset` | 2026-08-16 17:51:50 | 随关卡 |
| `M_GrayBox_Red.uasset` | 2026-09-10 18:11:19 | 灰盒材质，仍在使用 |
| `M_GrayBox_Straw.uasset` | 2026-09-10 18:11:16 | 同上 |

### 3.3 `VRSanguo\VR\`（3 个）

| 文件 | mtime |
|---|---|
| `M_GripPulse.uasset` | 2026-08-29 19:17:34 |
| `M_GripVFX.uasset` | 2026-08-29 11:41:56 |
| `M_MarkerGrip.uasset` | 2026-08-27 23:50:36 |

### 3.4 其余上游未列出的「不该只读」（补全 8 项口径之外）

上游所称「8 个关键资产（4 蓝图 + 2 刀 + 材质相关关卡）」**与实测不符**：实测**没有任何蓝图或刀处于只读**——`BP_VRCharacter.uasset`、`环首刀.uasset`、`环首刀直版.uasset`、`BP_Sword_Grip.uasset`、`BP_TestSword.uasset`、`BP_VRGameMode.uasset`、`BP_WeaponBase.uasset`、`L_SkeletonTest.umap`、`M_Weapon.uasset`（Rifle）**当前全部 `IsReadOnly=False`**。上游那次统计应是**崩溃时刻**的状态（当时确为只读），不是当前状态。

另需计入「非 VRSanguo 但项目自有、被顺带锁上」的：

| 文件 | 说明 |
|---|---|
| `Content\VRSpectator\VRSpectator.uasset` | 项目自有采样模式蓝图，`attrib` 输出 `A    R` |
| `Content\Weapons\Pistol\Meshes\SM_Pistol.uasset` | 项目在用武器网格 |
| `Content\Weapons\Pistol\Materials\MI_Weapon_Pistol.uasset` | 项目在用武器材质实例 |
| `Content\Weapons\Rifle\M_Weapon.uasset` | 项目在用武器材质 |

⇒ **合计「不该只读」= 40（`VRSanguo\` 内）+ 4（上述）= 44。**

### 3.5 本该只读、不列为问题

`Characters\MannequinsXR`（53）、`VRTemplate` 除 Input 外的 36 个、`LevelPrototyping`（15）、`Plugins\PICO…\Content`（115）、`Weapons` 的模板资产 —— 第三方/模板/示例资源，只读不阻碍项目工作。

---

## 4. 何时设的（时间线，含可核验证据）

| 时间 | 事件 | 证据 |
|---|---|---|
| 2026-08-09 21:49 | 首次入库（`98b2eb7`），此时 `.gitattributes` **已含** LFS `lockable` 规则；`M_FlatCol` 与 `MF_ProcGrid` 以 LFS 指针入库 | `git show 98b2eb7:.gitattributes` 含 `*.uasset filter=lfs … lockable`；`git cat-file -p 98b2eb7:…` 返回 LFS 指针 |
| 2026-08-10 14:42 / 16:39–16:44 / 17:50 | 工程模板资源落地（VRTemplate / MannequinsXR / LevelPrototyping / Weapons / PICO 插件） | 各文件 CreationTime（示例：`VRPawn.uasset` ctime `16:39:56`；`M_FlatCol` ctime `16:41:43`；`BP_VerificaitonData.uasset` ctime `17:50:29`） |
| 2026-08-16 11:44:03–11:44:04 | 32 个 `REF_*` 参考资产同批导入，**导入后即为只读** | 全部 `ctime == mtime == 11:44:03/04` |
| 2026-08-20 23:52:16 | `M_FlatCol` / `MI_DefaultColorway` 被写过**且写后仍是只读** | mtime `2026-08-20 23:52:16` 且 `IsReadOnly=True` ⇒ **该次写入之后又被重新 +R**（写入者必先解锁） |
| 2026-08-26 22:15 | `Set-TraeGovernanceAcl.ps1` 建立；`Unlock-TraeAssets.ps1` 亦为 08-26 前后产物 | 文件 mtime |
| **2026-08-30（最晚）** | **首次明确记录「`Content\VRSanguo` 49 个 uasset/umap 全为只读——目录被批量设过只读保护」**，并记录「临时解锁→保存→恢复只读」的处置惯例 | `session-20260830-001.md:283-287` |
| 2026-09-08 22:26 | `IMC_Weapon_Left/Right.uasset` 被改写后重新 +R | mtime `09-08 22:26` 且 `IsReadOnly=True`；脚本目标含其父目录 |
| 2026-09-09 14:38 / 09-10 15:07 / 09-11 23:27 | v3/v4/v5 关卡逐次保存后逐次 +R | `STATUS.json` note：`save True+R`×3、`+R True`×2、`两 umap +R 恢复`×1、`先解锁再重建`×1 |
| 2026-09-10 18:53:43 | 编辑器**明确因只读拒存** `L_Prototype_1v1_v5.umap`（证明 R 位当时真实生效） | 引擎日志 `Saved/Logs/…09.10….log`：`由于文件为只读，所以无法将包保存至 …/L_Prototype_1v1_v5.umap！` + `Saving map … took 0.000` |
| 2026-09-10 18:53:43 – 21:44:17 | R 位被**某操作解除**（21:44:17 保存成功 `took 0.302`） | 同上日志 + 文件 mtime 21:44:17 |
| 2026-09-12 14:53:03 / 22:20:55 / 22:29:37 | **3 次 C 类闪退 = 桥保存只读文件失败** | `AUDIT-editor-crash-20260912-executor.md` §2.1 表 #9 / #11 / #12 |
| 2026-09-12 23:01:57 | `BP_VRCharacter.uasset` 最后一次被写（此后未再锁） | mtime `2026-09-12 23:01:57`，`IsReadOnly=False` |

**结论：只读位不是一次性事件，而是「写入 → 解锁 → 再锁」的循环，至少从 08 月中持续到 09-12。**

---

## 5. 会不会复发

### 5.1 已确证的复发源（三个）

1. **`Unlock-TraeAssets.ps1 -Restore`（唯一正在使用的自动重锁器）**
   触发条件：任何会话/用户为改 `Content\VRTemplate\Input\` 或 `BP_VRCharacter.uasset` 而先跑解锁、事后「恢复保护姿态」。
   效果：`Get-ChildItem -Recurse -File | % { attrib.exe +R }` —— **递归**，会把该目录下 34 个文件全部重新锁上（当前只有 2 个是只读的）。

2. **`Unlock-GripPolish.ps1 -Restore`**
   触发条件：握持手感标定（M01-T001）改 `Content\VRSanguo\VR\Mesh\` 或 `L_SkeletonTest.umap` 后恢复。
   效果：`L_SkeletonTest.umap` 重新只读 —— **该文件正是 09-12 14:53 那次闪退的触发对象**。⇒ 这条复发路径**直接重建已知闪退条件**。

3. **M01-T005 关卡重建流程的「每轮 +R」**
   触发条件：`Docs/Scene/` 或灰盒布局再改一轮（用户已明确「还要再改几轮、未定版」）。
   效果：`L_Prototype_1v1_v5.umap` / `v4.umap` 被 `+R`。`STATUS.json` note 中该动作已成固定收尾项。

### 5.2 复发→闪退的传导链（已在 09-12 实证 3 次）

```
文件被 +R
  → 自动化桥（UE-MCP Bridge，端口 9877）或 editor.save_dirty / asset.save_all_dirty 尝试保存该包
  → LogSavePackage: Error: Cannot remove '…' as it is read only
  → LogSavePackage: Error: Error saving '…'
  → LogWindows: Error: appError called: 保存…时出现错误
  → 编辑器 Assert 终止（进程整体崩溃，非仅该操作失败）
```
且 **桥在崩溃循环中反复重试同一保存**（09-12 22:20:55 与 22:29:37 两次之间仅隔 8 分 42 秒，同一文件）。

### 5.3 当前残留风险点（本报告时点实测）

- **`L_Prototype_1v1_v5.umap` = 只读，且被存活编辑器 pid 30604（09-12 22:51:24 启动）持有** ⇒ 潜在可复现闪退点。
- `L_Prototype_1v1_v4.umap`、`L_Prototype_1v1_BuiltData.uasset`、`M_GrayBox_Red` / `M_GrayBox_Straw`、`M_GripPulse` / `M_GripVFX` / `M_MarkerGrip`、`VRSpectator.uasset`、`SM_Pistol` / `MI_Weapon_Pistol` / `M_Weapon` 只读 ⇒ 若被批量保存动作覆盖同样会炸。
- 活日志尾部（`Saved/Logs/VRSanguoYanWuchang.log`，2104 行）**无任何 `read only` / 只读 / 保存失败记录**，最后一行 `2026.09.13-03.06.26 LogAudioMixer`（游戏时间 = 本地 11:06:26）⇒ **当前空闲，未在复发中**。

### 5.4 「会不会自动复发」的判定

- **没有常驻守护进程会自动重锁**：无计划任务相关项（上游已排）、无云同步触发（§2.1）、无 git hook 设置只读（仓库内无 `attrib` 调用）。
- **因此复发是「事件驱动」**：只要有人/会话按既有惯例跑一次「恢复只读」或「重建后 +R」，就会复发；**触发条件是「改完活资产后恢复保护姿态」这个习惯动作本身。**

---

## 6. 建议（**未执行**，供裁定）

1. **停止对含活资产的目录使用递归 `attrib +R`。** 具体对象：`Content\VRSanguo\VR\Mesh\`、`Content\VRTemplate\Input\`、`Content\VRSanguo\Dev\`。仅对确认封存的单个文件（如 `L_Prototype_1v1_v4.umap`、`REF_*`）加 R。
2. **把「只读保护」从文件属性改成显式清单 + 校验门禁。** 单一事实源建议放 `.trae/`（如 `readonly-manifest.md`），记录「谁该只读、为什么、何时锁的」；校验脚本按清单核对 `(Get-Item $p).IsReadOnly`，不再依赖不可追溯的 R 位。
3. **新增「活资产白名单」**：明确列出「永远不得只读」的文件（当前至少 `L_Prototype_1v1_v5.umap`、`L_SkeletonTest.umap`、`BP_VRCharacter.uasset`、`环首刀.uasset`、`环首刀直版.uasset`、`BP_VRGameMode.uasset`）。理由：这些是编辑器随时会保存的目标，锁上就等于给编辑器埋雷。
4. **给自动化桥的保存加前置检查**（而非事后崩）：桥在 `save` / `save_all_dirty` 前先读目标包 `IsReadOnly`，只读则**跳过并返回明确错误**，不进入 `appError` 路径。这能直接消灭 C 类闪退（占 12 次中的 3 次）。
5. **`editor.save_dirty` 已知会崩编辑器**（`CR-20260907-001` §3 记录 `EditorHandlers.cpp:1221` 桥 1.0.87 bug），建议一并列入桥技术债修复范围。
6. **解除当前残留风险（需用户授权）**：对 `L_Prototype_1v1_v5.umap` 等 5.3 所列文件，在编辑器未持有脏包时评估是否解锁。**本报告不执行，也不建议在 pid 30604 存活期间盲改。**

---

## 7. 仍未取到数（明确列出）

1. **「最初是谁、什么时候批量设的只读」——未取到。** 已确证该姿态在 **08-30 之前**已存在，且 08-16 的 32 个 `REF_*` 导入后即为只读；但**没有任何一份文档、脚本或日志记录了那次批量操作的主体与命令**。项目内可检索到的 `.ps1` 只有两个「解锁/恢复」脚本（08-26、09-10 创建），**没有任何脚本执行最初的批量 +R**。
2. **NTFS 属性变更时间戳——未取到。** Windows 未在本机保存「属性变更时间」可读记录；我**未执行** `fsutil usn readjournal`（该命令在部分配置下需特权且输出量巨大，超出本会话安全边界），因此**没有**属性级时间证据。时间线全部由「mtime 晚于锁定声明」「引擎日志拒存记录」「会话记录」三者交叉得到。
3. **「谁在 2026-09-10 18:53:43 – 21:44:17 之间解除了 v5 的 R 位」——未取到**（`t5-verification.md` §529/§750 已独立记录为无法判定，本次复核未能补充）。
4. **上游「155 个只读文件」与实测 150 的差异来源——未取到。** 可能来自不同时点或不同统计口径（是否含 `Plugins\`），无法还原。
5. **上游「8 个关键资产（4 蓝图 + 2 刀 + 材质相关关卡）」的原始清单——未取到。** 实测当前**无任何蓝图/刀为只读**，判断该口径为崩溃时刻状态。
6. **`D:\AWork\TraeAdmin\VRSanguoYanWuchang\rebuild_v3/v4/v5.py` 是否自身设置过 +R——未取到结论。** 项目内副本 `.trae/tools/scene/rebuild_v3|v4|v5.py` 全文检索 `attrib|readonly|read_only|只读|IsReadOnly` **零命中**；管理员目录下**已无这三个 .py 文件**（只剩脚本产物的痕迹），无法比对当时版本。
7. **`Saved\Config\WindowsEditor\EditorPerProjectUserSettings.ini.corrupt.bak`（4589 行，非只读）的成因——未取到**，与只读锁是否相关无证据。
8. **临时文件未清理**：`D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\content_ro.xml`、`content_all.xml` 为本会话新建（枚举产物）。按约束「用完即删」应删除，但本会话红线为「不得删除任何文件」，**故保留未删**，请指挥台裁定后处置。

---

*只读排查会话 readonly-scout · 2026-09-13 11:2x*
