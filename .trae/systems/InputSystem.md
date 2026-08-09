# InputSystem

## 职责

把 Enhanced Input 的设备信号转换为移动、转向、抓取、战斗、UI 与调试命令，并管理输入上下文和玩家偏好。

## 边界

- 遵循 `EnhancedInputStandard`；设备绑定留在 Input Action/Mapping Context，业务系统只接收语义命令。
- UI、交互与移动通过焦点和上下文优先级仲裁，禁止各系统独立读取同一原始按键。
- 平台系统键、控制器连接状态和 Tracking 状态由适配层统一发布。

## 状态

- 最少支持 Gameplay、UI、Paused、Cinematic、Disabled、Debug。
- 状态切换必须成对添加/移除 Mapping Context，并在失焦时清空保持值。
- 用户设置包含主手、移动参考、转向模式、死区与可重映射键位。

## 验收

- 左右手、断连重连、暂停恢复、UI/世界焦点竞争、重复绑定均行为确定。
- 输入事件不触发同步加载、存档或高成本世界扫描。
- 真机动作反馈延迟无可感知异常。
