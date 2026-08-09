# Unreal 命名标准

## 通用格式

- 文件夹、资产与 C++ 标识符使用英文；采用 `PascalCase`，不使用空格、拼音或无语义编号。
- 资产格式为 `Prefix_BaseName_Variant_Suffix`；名称应能在脱离目录时识别用途。
- 临时、测试、废弃资产必须放入明确隔离目录，不得混入正式内容。

## 资产前缀

| 类型 | 前缀 |
| --- | --- |
| Blueprint / Actor | `BP_` |
| Actor Component | `BPC_` |
| Widget Blueprint | `WBP_` |
| Animation Blueprint | `ABP_` |
| Animation Sequence / Montage | `AS_` / `AM_` |
| Blend Space | `BS_` |
| Skeleton / Skeletal Mesh | `SKEL_` / `SK_` |
| Static Mesh | `SM_` |
| Material / Instance | `M_` / `MI_` |
| Texture | `T_` |
| Niagara System | `NS_` |
| Sound Wave / Cue / MetaSound | `SW_` / `SC_` / `MS_` |
| Input Action / Mapping Context | `IA_` / `IMC_` |
| Data Asset / Data Table | `DA_` / `DT_` |
| Gameplay Tag 配置语义 | `Domain.Feature.State` |
| SaveGame Class | `SG_` |
| Automation Map | `TestMap_` |

## 后缀约定

- 纹理使用 `_D`、`_N`、`_ORM`、`_M`、`_E` 等通道语义。
- LOD、左右手、阵营与规格使用 `_LOD0`、`_L`、`_R`、`_Ally`、`_Enemy` 等稳定后缀。
- 不允许 `_New`、`_Final`、`_Final2`；版本由源控管理。

## 路径规则

- 项目资产位于 `/Game/VRSanguoYanWuchang/<Domain>/...`。
- 领域目录优先：`Characters`、`Combat`、`Interaction`、`UI`、`Audio`、`Maps`、`Data`、`VR`、`Tests`。
- 禁止直接修改 Marketplace/Vendor 原始目录；项目适配资产放在项目命名空间。

## 验证门槛

- Content Browser 无命名冲突、无未修复 Redirector。
- 自动扫描不出现空格、非约定前后缀、`New`/`Final` 临时命名。
