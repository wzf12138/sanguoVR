# 事件与接口标准

## 核心接口

- `IInteractable`：抓取、放下、吸附与交互提示
- `IWeaponSource`：武器数据、持握状态和攻击轨迹
- `IDamageable`：接收已解析伤害与死亡结果
- `IDefenseProvider`：格挡面、盾牌状态与防御消耗
- `IMovementMode`：瞬移、平滑移动及后续坐骑移动
- `IBattleParticipant`：出生、战斗状态、胜负与重置

### C++ 接口声明

```cpp
// 抓取与交互
UINTERFACE(BlueprintType)
class UInteractable : public UInterface { GENERATED_BODY() };
class IInteractable
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, Category = "Interaction") bool CanGrab(AVRHand* Hand) const;
    UFUNCTION(BlueprintNativeEvent, Category = "Interaction") void OnGrabbed(AVRHand* Hand);
    UFUNCTION(BlueprintNativeEvent, Category = "Interaction") void OnReleased(AVRHand* Hand);
    UFUNCTION(BlueprintNativeEvent, Category = "Interaction") void OnHoverStart(AVRHand* Hand);
    UFUNCTION(BlueprintNativeEvent, Category = "Interaction") void OnHoverEnd(AVRHand* Hand);
};

// 武器数据与轨迹
UINTERFACE(BlueprintType)
class UWeaponSource : public UInterface { GENERATED_BODY() };
class IWeaponSource
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, Category = "Weapon") UVRWeaponDefinition* GetWeaponData() const;
    UFUNCTION(BlueprintNativeEvent, Category = "Weapon") bool IsTwoHanded() const;
    UFUNCTION(BlueprintNativeEvent, Category = "Weapon") TArray<FWeaponTrajectorySample> GetTrajectory() const;
};

// 伤害接收
UINTERFACE(BlueprintType)
class UDamageable : public UInterface { GENERATED_BODY() };
class IDamageable
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, Category = "Combat") void ReceiveDamage(const FCombatResult& Result);
    UFUNCTION(BlueprintNativeEvent, Category = "Combat") bool IsAlive() const;
    UFUNCTION(BlueprintNativeEvent, Category = "Combat") float GetHealthRatio() const;
};

// 防御提供
UINTERFACE(BlueprintType)
class UDefenseProvider : public UInterface { GENERATED_BODY() };
class IDefenseProvider
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, Category = "Defense") bool IsBlocking() const;
    UFUNCTION(BlueprintNativeEvent, Category = "Defense") FDefenseResult TryBlock(const FAttackRequest& Request);
};

// 移动模式
UINTERFACE(BlueprintType)
class UMovementMode : public UInterface { GENERATED_BODY() };
class IMovementMode
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, Category = "Movement") bool RequestTeleport(const FVector& Target, FRotator TargetRotation);
    UFUNCTION(BlueprintNativeEvent, Category = "Movement") void SetSmoothMove(const FVector2D& Input);
    UFUNCTION(BlueprintNativeEvent, Category = "Movement") EMovementState GetMovementState() const;
};

// 战斗参与者
UINTERFACE(BlueprintType)
class UBattleParticipant : public UInterface { GENERATED_BODY() };
class IBattleParticipant
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintNativeEvent, Category = "Battle") void OnBattleStart();
    UFUNCTION(BlueprintNativeEvent, Category = "Battle") void OnBattleEnd(EBattleOutcome Outcome);
    UFUNCTION(BlueprintNativeEvent, Category = "Battle") void ResetForNextRound();
};
```

## 事件语义

事件描述已经发生的事实，如 `OnWeaponGrabbed`、`OnAttackStarted`、`OnHitResolved`、`OnBattleEnded`。请求使用 `Request` 或函数返回值，不把“请求瞬移”命名成“瞬移已完成”。

## 依赖方向

UI 订阅战斗状态，不直接修改生命值；武器提交命中候选，不直接扣血；AI 请求动作，不绕过角色动作与硬直；关卡流程控制出生和重置，不计算战斗伤害。

## 状态一致性

战斗、攻击、抓取、拉弓和移动采用明确枚举状态。每次状态变化记录来源与时间。重开时由竞技场流程统一广播重置，所有订阅者清理临时对象、计时器、委托和引用。

## 失败处理

接口调用失败必须返回可诊断原因。无效瞬移、无效命中、搭箭失败和缺失反馈资源不应造成软锁或未捕获空引用。