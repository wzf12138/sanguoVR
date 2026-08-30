# 资产登记册

记录项目中所有 Content 资产的创建、状态与依赖关系。并发任务认领前，必须检查本登记册，避免重复创建或依赖冲突。

## 登记条目格式

| 资产ID | 类型 | 路径 | 状态 | 前置资产 | 关联任务 | 备注 |
|---|---|---|---|---|---|---|
| AST-001 | SkeletalMesh | Content/VRSanguo/Characters/SK_Militia | — | — | — | 示例 |

## 状态定义

| 状态 | 含义 |
|---|---|
| `draft` | 已规划，尚未创建任务包 |
| `in_progress` | 关联任务已被认领，正在制作 |
| `awaiting_review` | 资产已产出，等待用户视觉确认 |
| `approved` | 用户确认通过，可用于后续任务 |
| `blocked` | 因依赖缺失或规格未定而阻塞 |
| `deprecated` | 已废弃，不再使用 |

## 资产类型缩写

| 缩写 | 类型 |
|---|---|
| SKM | SkeletalMesh |
| STM | StaticMesh |
| ANM | Animation / AnimMontage |
| ABP | AnimBlueprint |
| MAT | Material / MaterialInstance |
| TEX | Texture |
| AUD | SoundCue / SoundWave |
| NFX | NiagaraSystem |
| WBP | WidgetBlueprint |
| DAT | DataAsset |
| MAP | Level / Map |

## 当前资产

| 资产ID | 类型 | 路径 | 状态 | 前置资产 | 关联任务 | 备注 |
|---|---|---|---|---|---|---|
| AST-002 | SKM | Content/VRSanguo/Art/Characters/SK_Character_Body | deprecated | — | M02-PREP-001 | **已废弃（2026-08-24）**：由模块化体型变体 AST-014/015/016 替代 |
| AST-003 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Sword_Han | draft | AST-014 | M02-PREP-001 | 环首刀；低模 OBJ 已产出，待导入 UE |
| AST-004 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Shield_Han | draft | AST-014 | M02-PREP-001 | 钩镶/长方盾；低模 OBJ 已产出，待导入 UE |
| AST-005 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Polearm_Ji | draft | AST-014 | M02-PREP-001 | 戟（卜字戟）；低模 OBJ 已产出，待导入 UE |
| AST-006 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Spear_Qiang | draft | AST-014 | M02-PREP-001 | 矛/槊；低模 OBJ 已产出，待导入 UE |
| AST-007 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Bow_Recurve | draft | AST-014 | M02-PREP-001 | 角弓/反曲弓；低模 OBJ 已产出，待导入 UE |
| AST-010 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Sword_Sheath | draft | AST-014 | M02-PREP-001 | 环首刀刀鞘；低模 OBJ 已产出，待导入 UE |
| AST-011 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Mashuo | draft | AST-014 | M02-PREP-001 | 马槊；低模 OBJ 已产出，待导入 UE |
| AST-027 | STM | Content/VRSanguo/Art/Weapons/SK_Weapon_Sword_Straight | awaiting_review | — | M02-PREP-001 | 环首刀修直版；低模 OBJ（3K 面）+ 4 张 1024 贴图已产出，待导入 UE 验收 |
| AST-028 | STM | Content/VRSanguo/Art/Armor/SK_Armor_XiHan_TieJia | awaiting_review | — | M02-PREP-001 | 西汉铁甲（齐王墓）；低模 OBJ（8K 面）+ 4 张 1024 贴图已产出 |
| AST-029 | STM | Content/VRSanguo/Art/Armor/SK_Armor_Han_TieJia2 | awaiting_review | — | M02-PREP-001 | 汉铁甲2；低模 OBJ（8K 面）+ 4 张 1024 贴图已产出 |
| AST-030 | STM | Content/VRSanguo/Art/Armor/SK_Armor_Zhajia_Light | awaiting_review | — | M02-PREP-001 | 扎甲轻型；低模 OBJ（8K 面）+ 4 张 1024 贴图已产出 |
| AST-031 | STM | Content/VRSanguo/Art/Armor/SK_Armor_Hubi_Heavy | awaiting_review | — | M02-PREP-001 | 护臂重型；低模 OBJ（2K 面）+ 4 张 1024 贴图已产出 |
| AST-032 | STM | Content/VRSanguo/Art/Armor/SK_Armor_Jingjia_Heavy | awaiting_review | — | M02-PREP-001 | 胫甲重型；低模 OBJ（2K 面）+ 4 张 1024 贴图已产出 |
| AST-033 | STM | Content/VRSanguo/Art/Armor/SK_Armor_Doumou_Heavy | awaiting_review | — | M02-PREP-001 | 铁兜鍪重型；低模 OBJ（3K 面）+ 4 张 1024 贴图已产出 |
| AST-034 | STM | Content/VRSanguo/Art/Armor/SK_Armor_Yulin_Kui | awaiting_review | — | M02-PREP-001 | 鱼鳞盔；低模 OBJ（3K 面）+ 4 张 1024 贴图已产出 |
| AST-008 | TEX | Content/VRSanguo/Art/References/** | approved | — | M02-PREP-001 | 参考图 33 张已质检落盘（Sword 7/Shield 4/Polearm 4/Spear 7/Bow 2/Armor 8/Unit 1），2026-08-24 随 M02-PREP-001 验收同步 approved |
| AST-009 | MAP | Content/VRSanguo/Dev/L_Prototype_1v1_v2.umap | approved | — | M01-T005 | 1v1 灰盒竞技场；2026-08-24 路径对齐现行版本 v2（v1 保留为历史基线），随 M01-T005 验收同步 approved |
| AST-012 | BP | Content/VRSanguo/VR/BP_WeaponBase.uasset | awaiting_review | — | M01-T001 | 武器抓取蓝图基类 |
| AST-013 | BP | Content/VRSanguo/VR/BP_TestSword.uasset | awaiting_review | AST-012 | M01-T001 | 测试用单手剑 |
| AST-014 | SKM | Content/VRSanguo/Art/Characters/SK_Base_Body_Lean | draft | — | M02-PREP-001 | 兵卒体型 170cm（士兵/弓兵/赵云） |
| AST-015 | SKM | Content/VRSanguo/Art/Characters/SK_Base_Body_Standard | draft | — | M02-PREP-001 | 武将体型 180cm（关羽/吕布/张飞/马超） |
| AST-016 | SKM | Content/VRSanguo/Art/Characters/SK_Base_Body_Heavy | draft | — | M02-PREP-001 | 壮硕体型 180cm（许褚/典韦） |
| AST-017 | SKM | Content/VRSanguo/Art/Characters/Heads/SK_Head_Soldier_01 | draft | AST-014 | M02-PREP-001 | 通用士兵头 |
| AST-018 | SKM | Content/VRSanguo/Art/Characters/Heads/SK_Head_Soldier_02 | draft | AST-014 | M02-PREP-001 | 士兵头变体 |
| AST-019 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Torso_Cloth | draft | AST-014 | M02-PREP-001 | 布衣/无甲躯干 |
| AST-020 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Torso_Leather | draft | AST-014 | M02-PREP-001 | 皮甲躯干 |
| AST-021 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Torso_Zhajia | draft | AST-014 | M02-PREP-001 | 札甲躯干 |
| AST-022 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Torso_TongXiu | draft | AST-014 | M02-PREP-001 | 筒袖铠躯干 |
| AST-023 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Helmet_DouMou | draft | AST-014 | M02-PREP-001 | 铁兜鍪 |
| AST-024 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Helmet_LingGuan | draft | AST-014 | M02-PREP-001 | 翎冠（吕布专属） |
| AST-025 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Arm_Vambrace | draft | AST-014 | M02-PREP-001 | 臂甲/护臂 |
| AST-026 | SKM | Content/VRSanguo/Art/Armor/SK_Armor_Leg_Greave | draft | AST-014 | M02-PREP-001 | 胫甲/裙甲 |

## 外部源文件索引（E 盘暂存区，2026-08-30 补录）

**基准路径**：`E:\AWork\Temp\VRSanguoRef\`（2026-08 下旬由 `D:\AWork\Temp\VRSanguoRef\` 迁入；旧报告中的 D: 路径已失效）。

**目录规则**（版本裁决权威）：

| 目录 | 用途 | 是否导入 UE |
|---|---|---|
| `FBX\` | 混元 3D 高模源（含 `.fbm` 贴图），永久保留作 M05 精修源 | 否 |
| `FBX_Low\*.obj` | 减面后低模，**正式导入源** | 是 |
| `FBX_Low\textures_<名称>_1024\` | 压缩贴图（≤1024），**正式导入贴图** | 是 |
| `FBX_Low\textures_<名称>\` | 4K 原始贴图（M05 精修源） | 否 |
| `FBX_Low\textures\`、`textures_1024\` | 早期批次导出，归属待确认 | M02 导入时以各资产目录为准 |
| `OBJ\` | 空目录 | — |
| `图片\` | 原始参考图收集区（已质检部分复制入 `Content/VRSanguo/Art/References/`） | 否 |

**AST ↔ 磁盘实物映射**（`FBX_Low\` 下）：

| AST | 磁盘文件 | 备注 |
|---|---|---|
| AST-003 | `SK_Weapon_Sword_Han.obj` | 弯版，2026-08-30 起降级为历史源 |
| AST-027 | `SK_Weapon_Sword_Straight.obj` | 直版，**环首刀正式源**（形制修正） |
| AST-004 | `SK_Weapon_Shield_Han.obj` | |
| AST-005 | `SK_Weapon_Polearm_Ji.obj` | |
| AST-006 | `SK_Weapon_Spear_Qiang.obj` | |
| AST-007 | `SK_Weapon_Bow_Recurve.obj` | |
| AST-010 | `SK_Weapon_Sword_Sheath.obj` | |
| AST-011 | `SK_Weapon_Mashuo.obj` | |
| AST-028 | `SK_Armor_西汉铁甲（齐王墓铁甲）.obj` | 高模 `FBX\西汉铁甲（齐王墓铁甲）.fbx` |
| AST-029 | `SK_Armor_汉铁甲2.obj` | 高模 `FBX\汉铁甲2.fbx` |
| AST-030 | `SK_Armor_Zhajia_Light.obj` | 高模 `FBX\扎甲-轻型.fbx` |
| AST-031 | `SK_Armor_Hubi_Heavy.obj` | 高模 `FBX\护臂 重型.fbx` |
| AST-032 | `SK_Armor_Jingjia_Heavy.obj` | 高模 `FBX\胫甲 重型.fbx`（Jingjia=胫甲音译） |
| AST-033 | `SK_Armor_Doumou_Heavy.obj` | 高模 `FBX\铁兜鍪-重型.fbx` |
| AST-034 | `SK_Armor_Yulin_Kui.obj` | 高模 `FBX\鱼鳞盔.fbx` |

**生成件与模块化槽位对应注记**（对齐 M02-PREP-001 §6 模块化架构，导入 UE 时逐件复核）：

- AST-033 兜鍪 → AST-023 槽位；AST-031 护臂 → AST-025 槽位；AST-032 胫甲 → AST-026 槽位（直接对应）。
- AST-030 扎甲为整套生成 → M02 导入时拆分取躯干入 AST-021 槽位（拆分工具与流程由 M02 任务确认）。
- AST-028/029 两件铁甲 → AST-022（筒袖铠）槽位候选，二择一待 M02 用户裁决。
- AST-034 鱼鳞盔 → 头盔变体备选；AST-024 翎冠未生成（M02 补）。
- AST-019 布衣、AST-020 皮甲未生成（M02 补）。
- 类型注记：AST-027~034 现登记为 STM；模块化架构要求甲胄件随骨架动画（Set Master Pose Component，需 SKM）。以 SKM 还是 STM 导入属 M02 技术决策，导入时复核并回填本表类型。

**待办（M05 模板清理时处理）**：`Content/Weapons/Rifle/` 下 `M_Weapon.uasset` 与 `Materials/M_Weapon.uasset` 为重复材质（散落份被 `Pistol/Materials/MI_Weapon_Pistol` 引用且自身引用 Materials 份，疑似父子链），须经 UE 引用查看器裁决后删除其一，禁止直接文件删除。

## 登记规则

- 新资产创建前，决策模型先在本表分配资产 ID，状态设为 `draft`。
- 关联任务认领后，执行模型更新状态为 `in_progress`。
- 资产产出后，执行模型更新状态为 `awaiting_review`，并填写路径。
- 用户视觉确认后，审核模型更新状态为 `approved`。
- 资产废弃时，更新状态为 `deprecated`，不删除记录。
- 并发任务认领前，检查本表确认无重复资产 ID 或路径冲突。