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

*暂无登记资产。资产随里程碑任务产出后登记。*

## 登记规则

- 新资产创建前，决策模型先在本表分配资产 ID，状态设为 `draft`。
- 关联任务认领后，执行模型更新状态为 `in_progress`。
- 资产产出后，执行模型更新状态为 `awaiting_review`，并填写路径。
- 用户视觉确认后，审核模型更新状态为 `approved`。
- 资产废弃时，更新状态为 `deprecated`，不删除记录。
- 并发任务认领前，检查本表确认无重复资产 ID 或路径冲突。