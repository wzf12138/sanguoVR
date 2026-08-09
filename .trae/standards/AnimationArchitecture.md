# 动画架构标准

## 分层

1. Gameplay 层产生角色状态、移动参数、战斗意图和交互目标。
2. Animation Instance 读取稳定快照，计算 Locomotion、Combat、Interaction 与 IK 状态。
3. Anim Graph 负责姿态混合；Montage 负责有明确起止的动作片段。
4. Control Rig、IK Rig/Retargeter 负责程序化修正与重定向，不反向驱动玩法真值。

## 强制规则

- 动画蓝图不得作为生命值、命中判定、装备状态或任务状态的唯一真值源。
- 状态机转换必须由明确布尔量、枚举或 Gameplay Tag 驱动，禁止依赖脆弱的剩余时间链。
- Anim Notify 只发出表现或时序事件；关键命中结果由权威玩法逻辑验证。
- Montage Slot 按用途固定：全身、上半身、交互、受击；并规定互斥与打断策略。
- Root Motion 使用场景必须逐动作声明；网络、碰撞和 VR 玩家位移需单独验证。
- 动画线程可运行路径不得访问非线程安全对象或做世界查询。
- 角色 LOD 必须逐级关闭次要曲线、骨骼、Control Rig 与 IK 成本。

## VR 与全身表现

- HMD、控制器和跟踪器数据先转换到统一角色空间，再进入 IK。
- 跟踪丢失时使用平滑降级姿态，禁止骨骼瞬移到原点。
- 本地身体与远端/镜像身体可采用不同更新策略，但姿态语义一致。

## 验证门槛

- Animation Insights 无异常 Game Thread/Worker Thread 热点。
- 转换、打断、连击、受击、抓取和跟踪丢失均有可重复测试。
- 目标设备上动画预算满足 `PicoNeo3PerformanceBudget`。
