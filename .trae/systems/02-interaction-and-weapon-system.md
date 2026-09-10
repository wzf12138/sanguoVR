# 交互与武器系统工程实现指引

武器类别、抓取体验、脱手恢复与弓箭规则以 [`../knowledge/Design/WeaponsAndInteraction.md`](../knowledge/Design/WeaponsAndInteraction.md) 为权威产品详规；战斗接触语义见 [`../knowledge/Design/CombatSystem.md`](../knowledge/Design/CombatSystem.md)。本文件只规定工程接入方式。

## 工程职责

- 提供统一武器数据、持握点、所有权、轨迹源和反馈接口。
- 管理候选检测、抓取、切手、释放、追踪丢失与重置生命周期。
- 将玩家和 AI 的不同动作来源归一到同一武器与战斗接口。
- 为弓箭等复合交互提供可测试的子状态与对象池边界。

## 实现边界

武器差异通过数据与组件组合表达，不复制平行战斗系统。所有权变更必须原子化；死亡、重置、销毁和追踪异常先解除约束，再回收对象。表现反馈不得写回伤害结果。

## 接口契约（规划级）

以下为 M00 规划阶段的接口契约框架，具体签名在 M00-T005 C++ 骨架中实现并以此为准。

**武器接口**（2026-09-11 更正：下方原记规划名 `IVRWeapon` / `IGrabbable` 在 C++ 骨架落地时更名为 `IWeaponSource` / `IInteractable`，且方法集与规划稿不同。**以实际实现为准**，规划名不得再被引用——见 `../standards/05-event-and-interface-standard.md`）：
- 接口 `IWeaponSource`（`Source/VRSanguoYanWuchang/Public/Interfaces/VRWeaponSource.h`）：提供 `GetWeaponData()`, `IsTwoHanded()`, `GetTrajectory()`
- 接口 `IInteractable`（`Source/VRSanguoYanWuchang/Public/Interfaces/VRInteractable.h`）：提供 `CanGrab(AVRHand*)`, `OnGrabbed(AVRHand*)`, `OnReleased(AVRHand*)`, `OnHoverStart(AVRHand*)`, `OnHoverEnd(AVRHand*)`

**核心服务**：
- `GrabWeapon(AActor* Weapon, EHand Hand)` → `bool`
- `ReleaseWeapon(EHand Hand, EReleaseReason Reason)`
- `GetOwnedWeapon(EHand Hand)` → `AVRWeaponBase*`

**事件广播**：
- `OnWeaponGrabbed(AActor* Weapon, EHand Hand)`
- `OnWeaponReleased(AActor* Weapon, EReleaseReason Reason)`
- `OnWeaponDropped(AActor* Weapon)`（脱手事件）

**数据结构**：
- `FWeaponTrajectorySample`：`FVector Position; FVector Velocity; FQuat Rotation; float Timestamp;`
- `EReleaseReason`：`Manual | Collision | Timeout | Reset`

**依赖接口**：
- Combat: 接收武器轨迹和接触候选
- Diagnostics: 报告武器生命周期事件

## VRExpansionPlugin 接口调用契约（2026-09-09 入库，来源 CR-20260909-001）

VRE 插件的接口方法（`IVRGripInterface` 等）多为 `UFUNCTION(BlueprintNativeEvent)` 声明：C++ 侧调用必须走生成的静态转发 `IVRGripInterface::Execute_<Name>(UObject* Target, ...)`，禁止取得接口指针后 const_cast 直调 `<Name>(...)`——直调版 thunk 内置 ensure 断言（"Do not directly call Event functions in Interfaces"），运行到即崩溃。

- **判别方法**：VRE 头文件中 `BlueprintNativeEvent` 声明的方法 → 调用一律 `Execute_` 前缀。
- **正确范例**：VRE 插件内部全部调用点；**违例案例**：`Source/VRSanguoYanWuchang/Private/Combat/VRSanguoGripLibrary.cpp` L34 直调 `DenyGripping`（2026-09-09 修复，见 CR-20260909-001）。
- **审核对应项**：`governance/ReviewProtocol.md` 审核内容第 12 条。

## 接口与验证

向战斗系统提供攻击窗口、轨迹与接触候选，向流程和诊断系统报告生命周期事件。验证覆盖双手竞争、切手、掉落恢复、重置残留、对象池上限和玩家/AI 共用接口；产品参数从权威详规读取。
