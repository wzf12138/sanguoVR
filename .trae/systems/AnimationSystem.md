# AnimationSystem

## 职责

管理角色动画状态快照、Anim Instance、状态机、Montage、IK/Retarget、动画 LOD 与表现事件。

## 边界

- Gameplay 是状态真值源；AnimationSystem 不决定伤害、任务、库存或存档结果。
- Animation Blueprint 只消费稳定数据并输出姿态；世界查询由角色或组件预计算。
- 全身 IK 遵循 `FullBodyIKStandard`，架构遵循 `AnimationArchitecture`。

## 数据接口

- 每帧快照包括速度、加速度、朝向、地面状态、姿态、战斗状态、装备、交互目标和跟踪置信度。
- Montage 请求包含动作 ID、Slot、优先级、可打断窗口与失败回调。
- Notify 转换为类型化表现事件，禁止字符串分发。

## 验收

- 状态切换、Montage 互斥、受击打断、抓取、LOD 与跟踪丢失表现稳定。
- 无动画蓝图线程安全警告、循环依赖或每帧昂贵 Cast。
- Pico Neo 3 的动画与 IK 成本处于预算内。
