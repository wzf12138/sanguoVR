# M00 项目基线与自动化骨架

## 前置：基于官方 VR 模板重建项目（2026-08-09）

用户手动执行：在 UE5.8 中使用官方 Virtual Reality 模板创建新项目，项目名保持 `VRSanguoYanWuchang`，目录选择 `D:\AWork\Unreal\Project\VRSanguoYanWuchang`。

创建后必须立即核对：

- `.trae/` 是否仍完整存在；若模板向导覆盖目录，将 `.trae/` 从备份移回项目根。
- `.uproject` 启用 OpenXR、OpenXREyeTracker、OpenXRHandTracking、PICOController，目标平台含 Android。
- `Content/` 存在模板自带 VR 内容（VR Pawn、手部、抓取、瞬移、输入资产）。
- 模板为蓝图版还是 C++ 版：C++ 版直接编译；蓝图版需要按 M00 要求补充 C++ 模块。
- 重建前把当前 `Config/`、`Source/` 的自定义项导出记录，重建后按差异合并，不整文件覆盖模板内容。

重建完成后，AI 在 M00 后续步骤中：

1. 验证 VS2026、MSVC、Windows SDK、UBT 和 Git。
2. 生成工程文件并清理编译 `VRSanguoYanWuchangEditor`。
3. 核对模板 VR 输入、移动与交互能力是否可用。
4. 建立本项目战斗与系统模块边界，不删除模板已提供的 VR 交互能力。
5. 调试 MCP 连接器（UE 编辑器 MCP 服务器或项目外 MCP 工具），记录配置、授权、端口和调用验证结果到 `.trae/knowledge/TechnicalDecisions.md`。

## 目标

建立可持续开发的 UE 项目骨架、文档权威链、模块边界、数据资产约定、输入基线和自动化测试入口。

## 交付

- VR 目标设备工程可构建、安装、启动和断网运行。
- Combat、Weapon、CharacterState、Movement、FullBodyIK、SquadAI、GameModeFlow 模块边界建立。
- 玩家与 AI 控制源通过统一能力请求接入角色。
- 建立武器、护甲、兵种、武将和比赛规则数据资产基类。
- 建立最小自动化测试、日志分类和性能采样场景。

## 退出条件

空场景中可生成玩家全身占位和数据驱动测试角色；项目可完成开发与目标设备构建；规则层不存在 1v1、单武器或联网依赖的硬编码。
