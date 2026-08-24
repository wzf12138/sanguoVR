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

## 登记规则

- 新资产创建前，决策模型先在本表分配资产 ID，状态设为 `draft`。
- 关联任务认领后，执行模型更新状态为 `in_progress`。
- 资产产出后，执行模型更新状态为 `awaiting_review`，并填写路径。
- 用户视觉确认后，审核模型更新状态为 `approved`。
- 资产废弃时，更新状态为 `deprecated`，不删除记录。
- 并发任务认领前，检查本表确认无重复资产 ID 或路径冲突。