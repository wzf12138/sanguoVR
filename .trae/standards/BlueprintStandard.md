# 蓝图标准

## 适用范围

适用于 Blueprint Class、Actor Component、Widget Blueprint、Animation Blueprint、Blueprint Function Library 与关卡蓝图。

## 强制规则

- 蓝图负责资产装配、表现编排和轻量规则；复杂算法、持久化、性能敏感循环放入 C++。
- Event Graph 只保留事件入口和高层流程；可复用逻辑提取为函数、宏或组件。
- 每个函数保持单一职责，输入输出命名表达语义；纯查询函数标记 Pure，副作用函数不得标 Pure。
- 节点从左到右排列，执行线不交叉；使用 Reroute、Comment 和局部变量控制可读性。
- Cast 必须有失败分支；跨系统访问优先接口、事件分发器或子系统。
- 默认关闭 Tick；连续更新优先定时器、动画通知、状态事件或有条件 Tick。
- Construction Script 仅做幂等编辑器装配，禁止依赖运行时玩家状态或昂贵全局查询。
- 暴露变量必须配置 Category、Tooltip、合理默认值与编辑限制。
- 修改变量、函数或组件名称后必须修复 Redirector 与引用，再完成全量编译。

## 禁止事项

- 禁止在 Level Blueprint 承载可复用玩法系统。
- 禁止长链 Cast、`Get All Actors Of Class` 高频调用、Delay 驱动核心状态机。
- 禁止无边界循环、递归蓝图流程以及每帧创建 Widget、动态材质或临时数组。
- 禁止提交编译警告、失效节点、孤立节点、测试打印和无说明硬编码资源引用。

## 验证门槛

- 所有蓝图 Compile 无错误和警告。
- Reference Viewer 不出现意外的跨模块硬依赖或大型资源链。
- VR 关键交互在目标帧率下无蓝图热点。
- 关键失败分支、空引用与重复触发均有测试。
