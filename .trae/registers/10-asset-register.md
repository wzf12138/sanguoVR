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
| AST-002 | SKM | Content/VRSanguo/Art/Characters/SK_Character_Body | draft | — | M02-PREP-001 | MannequinXR 兼容骨架，规格已定 |
| AST-003 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Sword_Han | draft | AST-002 | M02-PREP-001 | 环首刀；低模 OBJ 已产出（3,000 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-004 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Shield_Han | draft | AST-002 | M02-PREP-001 | 钩镶/长方盾 60×40cm；低模 OBJ 已产出（2,000 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-005 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Polearm_Ji | draft | AST-002 | M02-PREP-001 | 戟（卜字戟）全长~250cm；低模 OBJ 已产出（4,000 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-006 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Spear_Qiang | draft | AST-002 | M02-PREP-001 | 矛/槊 全长~300cm；低模 OBJ 已产出（3,000 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-007 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Bow_Recurve | draft | AST-002 | M02-PREP-001 | 角弓/反曲弓 弓长~120cm，弦独立骨骼；低模 OBJ 已产出（3,000 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-010 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Sword_Sheath | draft | AST-002 | M02-PREP-001 | 环首刀刀鞘（空鞘）；低模 OBJ 已产出（800 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-011 | SKM | Content/VRSanguo/Art/Weapons/SK_Weapon_Mashuo | draft | AST-002 | M02-PREP-001 | 马槊（槊类，全长 300cm）；用户混元图生 3D 生成 + AI 定标缩放，低模 OBJ 已产出（1,535 面/UV 保留，临时区 FBX_Low），待导入 UE |
| AST-008 | TEX | Content/VRSanguo/Art/References/** | in_progress | — | M02-PREP-001 | 参考图 33 张已落盘（Sword 7/Shield 4/Polearm 4/Spear 7/Bow 2/Armor 8/Unit 1），Bow 偏少；Scene/General 待补（后续里程碑） |
| AST-009 | MAP | Content/VRSanguo/Dev/L_Prototype_1v1.umap | awaiting_review | — | M01-T005 | 1v1 灰盒竞技场测试关卡：20x20m 地面、4m 围墙、掩体 A/B、高台 C、NavMesh（Static 已构建）、VRGameMode；26 Actor |

## 登记规则

- 新资产创建前，决策模型先在本表分配资产 ID，状态设为 `draft`。
- 关联任务认领后，执行模型更新状态为 `in_progress`。
- 资产产出后，执行模型更新状态为 `awaiting_review`，并填写路径。
- 用户视觉确认后，审核模型更新状态为 `approved`。
- 资产废弃时，更新状态为 `deprecated`，不删除记录。
- 并发任务认领前，检查本表确认无重复资产 ID 或路径冲突。