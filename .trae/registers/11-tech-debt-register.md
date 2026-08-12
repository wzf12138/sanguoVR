# 技术债登记

本登记册记录项目中有意接受的临时实现、占位方案和已知缺陷，追踪其影响范围与偿还计划。技术债不等同于风险（风险是"可能发生的问题"），而是"已经存在的妥协"。

每次审核任务交付时，审核模型应检查是否引入新债务并登记。债务偿还后标记为 `resolved`，保留记录供审计。

## 当前技术债

| ID | 描述 | 位置 | 引入原因 | 影响 | 偿还计划 | 优先级 | 状态 |
|---|---|---|---|---|---|---|---|
| TD-001 | UE5.8 与 PICO Neo3 不兼容，项目需降级到 UE5.6 | 引擎版本 / 全项目 | M00-T004 真机验证发现 Neo3 运行时 3.0.1 与 UE5.8 xrCreateSession 不兼容 | 阻塞 PICO 真机验证；需重建项目 | 用户决策后重建 UE5.6 项目，迁移 Source/ 和 Content/ | 高 | open |
| TD-002 | systems/ 指引缺少接口契约定义 | systems/01-07 | M00 规划期侧重职责边界，未到接口定义阶段 | M01+ 实现时接口依赖隐式约定 | 已补充规划级接口契约（2026-08-11） | 中 | resolved |
| TD-003 | 决策登记缺少 ADR 上下文 | registers/01-decision-register.md | 表格格式侧重快速浏览，未记录备选方案和后果 | 关键决策的"为什么"不可追溯 | 已补充关键决策 ADR 上下文（2026-08-11） | 中 | resolved |
| TD-004 | 无代码-文档漂移检测机制 | governance/ReviewProtocol.md | M00 阶段无实际代码，漂移问题尚未显现 | 实现推进后 systems/ 指引可能静默失效 | 已在 ReviewProtocol 增加文档同步验证（2026-08-11） | 中 | resolved |
| TD-005 | PICO 插件源码级 swapchain 补丁（拦截 `xrCreateSwapchain` 剥离 format list） | Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRHMD/Private/PICO_HMD.cpp | Neo3 系统 OpenXR 运行时（R2.1.12.0）Vulkan swapchain format list 触发 ION ENOTTY 崩溃 | 渲染格式受限（固定 B8G8R8A8_SRGB）；PICO 插件升级可能覆盖补丁；换新设备后补丁可能不再需要 | 补丁已编译进 libUnreal.so 并真机验证场景可见（V-008）；升级插件后须重打补丁；新设备接入时评估是否保留（见 DeviceConfigurationMatrix） | 高 | open |
| TD-006 | PICO 插件从引擎 Marketplace 迁移至项目 Plugins（含 Build.cs `PrecompileForTargets`、uplugin `Installed=false`） | Plugins/PICOOpen174f9f81d266V8 | 安装版引擎对 Marketplace 插件强制 precompiled 处理、增量构建检测不到引擎目录源码变化 | 插件不再随引擎自动更新；Fab 后续升级需手工迁移；引擎原插件已改名 `.disabled` | Fab 发布新版本时评估：迁移回引擎目录并重打补丁，或维持项目内插件并手工更新 | 中 | open |
| TD-007 | 输入映射为 Quest 风格，未按 PICO Touch 绑定；OpenXR Input 缺 PlayerMappableInputConfig | Content/VRTemplate/Input/*.uasset、Config/DefaultInput.ini | 基于 UE5.6 官方 VR 模板（Quest 默认按键）；PICO 官方文档要求绑定 PICO Touch 按键 | 真机手柄按键不可用、手柄模型不显示 | **部分偿还（2026-08-12）**：5 个 IMC 已按 PICO 官方文档绑定 PICO Neo3 键（IMC_Default/Hands/Menu/Weapon×2，二进制核验通过）；遗留：OpenXR Input PlayerMappableInputConfig 配置、VRPawn 挂载 Neo3 手柄模型（StaticMesh 组件）、真机复测 | 高 | open |
| TD-008 | `DefaultInput.ini` 曾指向不存在的 `/Game/XRFramework/Input/`（5.8 迁移残留） | Config/DefaultInput.ini | UE5.8→5.6 迁移时 IMC 路径未同步 | 曾导致 5 个 IMC 全部加载失败、输入不可用 | 已修复为 `/Game/VRTemplate/Input/`（2026-08-11，v3 日志确认 IMC 加载成功） | 高 | resolved |
| TD-009 | 安装版引擎 `Engine\Intermediate\Build\BuildRules\` 被误删（UE5Rules.dll） | 引擎目录（项目外） | 排障时误将引擎 BuildRules 当缓存删除 | UE5Rules.dll 本机无法从源码完整重建（引擎裁剪工具源码），曾阻塞全部构建 | 已用 Epic Launcher「验证/修复」恢复（2026-08-11）；经验已写入 PicoNeo3BuildGuide「已知构建坑」 | 高 | resolved |

## 债务管理规则

- **引入**：执行模型在实现中做出妥协时，在任务报告中声明并登记。
- **追踪**：每次审核检查新增债务；里程碑验收时审查未偿还债务清单。
- **偿还**：偿还后在登记册标记 `resolved`，保留记录；在 CHANGELOG 记录偿还事件。
- **升级**：高优先级 `open` 债务在下一个里程碑开始前必须偿还或有明确计划。
- **关联**：技术债可能关联风险（RSK-ID）或决策（DEC-ID），在描述中注明关联。
