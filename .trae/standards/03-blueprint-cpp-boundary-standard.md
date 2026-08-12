# 蓝图与 C++ 边界标准

## 分层

- 表现层：蓝图、动画、音效、震动、特效、UI 和流程展示
- 规则层：C++ 基类与可扩展组件，决定命中、伤害、防御、移动限制和状态转换
- 内容层：Data Asset、Data Table、行为树和蓝图子类，提供参数与内容组合

## C++ 负责

连续轨迹检测、同次攻击去重、CombatResolver、伤害与硬直计算、武器解卡判定、瞬移合法性、冷却防绕过、对象清理和可测试状态机。任何会影响胜负或造成帧间不一致的规则不得只藏在关卡蓝图。

## 蓝图负责

手部与武器表现、动画蒙太奇选择、命中特效、音效、触觉反馈、教程提示、菜单和竞技场展示。蓝图可以请求规则计算，不直接覆写计算结果。

## 扩展约束

新增武器或 AI 优先新增数据和表现，不复制核心战斗图。跨系统通信使用接口、委托或 Gameplay Tag；禁止角色、武器、UI 相互保存不必要的具体蓝图类引用。

## 调试要求

规则层暴露只读调试数据：攻击阶段、命中 ID、速度阈值、格挡结果、瞬移失败原因和 AI 当前战术。Shipping 构建关闭屏幕调试输出。

## 实现示例

### 蓝图调用 C++ 规则（正确）

```cpp
// C++ 规则层：CombatResolver 提供原子结算
UCLASS()
class UVRCombatResolver : public UObject
{
public:
    UFUNCTION(BlueprintCallable, Category = "VRCombat")
    FCombatResult ResolveAttack(const FAttackRequest& Request);

    UFUNCTION(BlueprintCallable, Category = "VRCombat")
    void RegisterAttackInstance(const FAttackInstance& Instance);
};
```

```text
蓝图（表现层）：武器碰撞触发 → 调用 ResolveAttack() → 根据返回的 FCombatResult 播放命中特效
```

### C++ 广播事件给蓝图（正确）

```cpp
// C++ 规则层：声明委托广播
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHitDealt, const FHitResultData&, HitData);

UCLASS()
class UVRCombatResolver : public UObject
{
public:
    UPROPERTY(BlueprintAssignable, Category = "VRCombat")
    FOnHitDealt OnHitDealt;
};
```

```text
蓝图（表现层）：Bind Event to OnHitDealt → 收到事件后播放音效、震动、特效
```

### DataAsset 被 C++ 消费（正确）

```cpp
// C++ 规则层：从 DataAsset 读取参数，不硬编码
UCLASS()
class AVRWeaponBase : public AActor
{
public:
    UPROPERTY(EditDefaultsOnly, Category = "Weapon")
    UVRWeaponDefinition* WeaponData; // 指向 DA_Weapon_Sword_T1

    void InitializeFromData()
    {
        DamageRange = WeaponData->DamageRange;
        SpeedThreshold = WeaponData->EffectiveSpeedThreshold;
    }
};
```

### 禁止的反模式

```text
❌ 蓝图直接修改伤害值：Set Damage = 50（绕过 CombatResolver）
❌ 蓝图直接判定格挡成功：Branch → Set bBlocked = true（绕过规则层）
❌ C++ 硬编码武器参数：float Damage = 30.0f（应从 DataAsset 读取）
❌ 蓝图相互引用具体类：BP_Sword 引用 BP_Archer（应通过接口或 Gameplay Tag）
```