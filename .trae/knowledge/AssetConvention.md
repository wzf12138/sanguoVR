# 资源规范

## 基本原则

- 一期先灰盒验证玩法，不提前堆积正式素材。
- 自制资源统一放入 `Content/VRSanguo`。
- 外购或第三方资源放入 `Content/VRSanguo/ThirdParty`。
- 使用第三方资源前记录来源、版本、许可和修改情况。
- 面向 PICO Neo3 时，必须关注材质复杂度、透明、阴影、贴图尺寸、骨骼数量和 LOD。

## 命名建议

| 类型 | 前缀 | 示例 |
|---|---|---|
| 蓝图 Actor | `BP_` | `BP_TrainingSword` |
| 组件 | `BPC_` | `BPC_WeaponInteraction` |
| 静态网格 | `SM_` | `SM_ArenaFence` |
| 骨骼网格 | `SK_` | `SK_Militia` |
| 材质 | `M_` | `M_Iron` |
| 材质实例 | `MI_` | `MI_Iron_Dark` |
| 纹理 | `T_` | `T_Iron_BC` |
| 动画 | `A_` | `A_SwordAttack01` |
| 动画蒙太奇 | `AM_` | `AM_SwordCombo` |
| Data Asset | `DA_` | `DA_Weapon_Sword` |
| Widget | `WBP_` | `WBP_BattleResult` |
| Niagara | `NS_` | `NS_WeaponHit` |
| 音效 | `S_` | `S_SwordBlock` |
| 地图 | `L_` | `L_PrototypeArena` |

具体规范可以随首批资源导入调整，但调整必须更新本文档。
