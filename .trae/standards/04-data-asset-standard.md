# Data Asset 标准

## 数据优先对象

武器、AI 单位、AI 等级、护甲、竞技场、教程步骤、舒适度预设、音效与特效映射必须可配置。核心逻辑不得通过复制蓝图制造参数变体。

## 武器数据

至少包含稳定 ID、类型、持握方式、有效速度阈值、伤害区间、攻击方向规则、硬直、体力影响、轨迹采样、解卡参数、反馈映射、模型与碰撞引用。弓额外包含搭箭吸附、拉距曲线、射程伤害曲线和箭袋容量。

## AI 数据

`AIUnitData` 分为基础属性、感知属性、战斗属性、战术能力和装备配置。AI 等级与兵种类型分离，以支持“等级 + 刀盾/长矛/弓兵”组合及后续骑兵扩展。

## 版本与默认值

每个资产包含数据版本。新增字段必须给出安全默认值；缺失资源时使用占位反馈而不是阻断战斗。数据校验器检查空引用、非法区间、重复 ID 和一体机不合规资源。

## 调参与发布

调试参数可由开发配置覆盖，公开试玩包只读取受控数据资产。任何影响验收阈值的改动必须记录原因、测试场景和回退值。

## Schema 版本与迁移

### 版本字段约定

每个 DataAsset 类和保存结构包含 `int32 SchemaVersion` 字段，初始值为 1。Schema 变更（新增、删除、重命名字段或改变语义）必须递增版本号。

### DataAsset 迁移策略

```cpp
UCLASS()
class UVRWeaponDefinition : public UPrimaryDataAsset
{
public:
    UPROPERTY(EditDefaultsOnly, Category = "Schema")
    int32 SchemaVersion = 1;

    // CDO 加载后自动迁移
    virtual void PostLoad() override
    {
        Super::PostLoad();
        if (SchemaVersion < CURRENT_WEAPON_SCHEMA_VERSION)
        {
            MigrateWeaponSchema(SchemaVersion);
            SchemaVersion = CURRENT_WEAPON_SCHEMA_VERSION;
        }
    }

    void MigrateWeaponSchema(int32 FromVersion);
};
```

- 新增字段必须给出安全默认值（`nullptr`、`0`、空数组或占位引用）。
- 删除字段时保留 `SchemaVersion` 记录，不回退版本号。
- 重命名字段通过 `PostLoad` 迁移函数将旧值映射到新字段。
- 迁移函数中标记 `UPROPERTY` 的 `meta=(DeprecatedProperty)` 提示编辑器警告。

### 保存数据版本化

保存结构与 DataAsset 分开版本化：

```cpp
USTRUCT(BlueprintType)
struct FSaveData
{
    UPROPERTY() int32 SaveSchemaVersion = 1;
    UPROPERTY() FMatchProgress Progress;
    UPROPERTY() TMap<FString, FString> Settings;
    // ... 其他字段
};
```

- 加载时检查 `SaveSchemaVersion`，低于当前版本时逐级迁移。
- 迁移失败时返回安全默认存档，不崩溃。
- 保存版本独立于 DataAsset SchemaVersion，两者不互相依赖。

### 版本登记

Schema 版本变更必须在 `CHANGELOG.md` 记录：版本号、变更内容、迁移逻辑、影响范围和回退方案。重大 Schema 变更需要变更请求批准。