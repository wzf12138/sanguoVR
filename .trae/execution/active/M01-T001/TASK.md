# M01-T001 武器抓取与 VRE 集成

- 任务编号：M01-T001
- 状态：见 `STATUS.json`
- 里程碑：M01
- 优先级：P0
- 前置任务：M00-T005（approved）、VRExpansionPlugin 5.6 已编译通过
- 预估耗时：~1.5h

## 目标

利用 VRE（VRExpansionPlugin）的 `GripMotionControllerComponent` + `HandSocketComponent` 建立 VR 手部物理抓取武器的基础能力。不替换现有 VRPawn，以组件方式集成 VRE 抓取系统。

## 实施步骤

### Step 1：确认 VRE 编译状态（0.1h）

- 读取 `Plugins/VRExpansionPlugin/` 确认 5.6 版本已就位
- 确认上一次编译通过（已由用户验证）

### Step 2：创建武器抓取蓝图基类（0.5h）

- 在 `Content/VRSanguo/VR/` 创建 `BP_WeaponBase`（继承 `GrippableSkeletalMeshActor`）
- 配置 `GripMotionControllerComponent` 抓取参数
- 参考示例：`E:\AWork\VRExpPluginExample\Content\VRE\Grippables\Weapons\Melee\`
- 关键配置项：
  - `GripScriptType`：默认抓取脚本
  - `bAllowSecondaryGrip`：允许双手握持
  - `HandSocketComponent`：武器握持姿势

### Step 3：配置 HandSocket 握持姿势（0.3h）

- 为单手刀剑创建主握持点 HandSocket
- 为长柄武器预留双手握持点（副握持点）
- 参考示例：`VRE/Core/HandSockets/`

### Step 4：创建测试武器（0.3h）

- 基于 `BP_WeaponBase` 创建 `BP_TestSword`（单手剑测试蓝图）
- 使用临时几何体（Cube/Cylinder）作为武器模型
- 放置到 `L_SkeletonTest` 关卡中

### Step 5：编辑器验证（0.3h）

- 编辑器 PIE 运行：确认可抓取/释放武器
- 确认双手握持可用
- 确认手部姿势与武器匹配
- 确认武器不会穿透/卡住

## 测试用例

> 依据 `governance/TestSpecification.md` 设计（新增蓝图 ≥2 条：功能可用 + 边界条件）。TC-01/02/03/06 由原 Step 5 与 CHECKS.md 中 `[PIE]` 检查项正式化而来，TC-04/05 为本次补充的边界用例。

| 用例ID | 测试目标 | 输入/前置条件 | 预期输出 | 证据类型 |
|--------|---------|-------------|---------|---------|
| TC-01 | 单手抓取武器 | 手柄对准 BP_TestSword，扣扳机抓取 | 武器吸附 HandSocket 姿势，Grip 生效 | [PIE 截图] |
| TC-02 | 释放武器掉落 | 抓取状态下松开扳机 | 武器脱手受重力落地，不穿地 | [PIE 截图] |
| TC-03 | 双手握持自动吸附 | 主手握持中，副手接近副握持点 | 副手自动吸附，双手协同转动武器 | [PIE 截图] |
| TC-04 | 双手握持释放主手（边界） | 双手握持中松开主手 | 副手接管或按 VRE 规则掉落，不卡死不穿模 | [PIE 日志] |
| TC-05 | 快速连抓连放（边界） | 1 秒内连续抓取/释放 3 次 | 无崩溃，Grip 状态一致，无幽灵握持残留 | [PIE 日志] |
| TC-06 | 现有 VR 交互回归 | 完整体验模板手部动画、瞬移、原抓取 | 全部正常，无退化 | [PIE 截图] |

## 停止条件

- VRE 编译失败且无法修复
- 现有 VRPawn 的 VR 交互（抓取/瞬移/手部）被破坏
- PICO Neo3 输入映射与 VRE 输入冲突无法解决

## 回退

- 删除 `Content/VRSanguo/VR/BP_WeaponBase` 和 `BP_TestSword`
- 还原对 VRPawn 的任何修改

## 报告路径

`.trae/execution/reports/tasks/M01-T001.md`