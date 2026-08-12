# UE 引擎参考知识库

> 基于 Epic 官方文档 2026-08-10 浏览提取。以 UE 5.6 为基准，标注 5.8 差异。
> 本文档是引擎技术参考，不替代 `GameMasterPlan.md` 的产品定义或 `TechnicalDecisions.md` 的决策记录。

## 文档来源

- UE 5.6 文档首页：https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-6-documentation
- UE 5.8 文档首页：https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-documentation

---

## 1. VR 模板（VR Template）

引擎内置 VR 模板是 VR 项目的官方起点，使用 OpenXR 框架。

### 核心结构

| 对象 | 模板中名称 | 位置 | 说明 |
|---|---|---|---|
| Pawn | VRPawn | `Content/VRTemplate/Blueprints` | 物理表示，包含运动控制器输入逻辑 |
| GameMode | VRGameMode | `Content/VRTemplate/Blueprints` | 规则定义，在 Project Settings > Maps & Modes 中设置 |
| PlayerStart | PlayerStart | World Outliner | 生成点，原点为追踪原点，模板定位在地面高度 |

### 内置功能

- **传送移动**：右控制器拇指杆选点，释放后传送。使用 NavMesh 限制可移动区域，`NavModifierVolume` 设置 `NavArea_Null` 可禁行。
- **快速转向**：左控制器拇指杆左右旋转，不依赖头部转动。
- **抓取系统**：`GrabComponent` 蓝图组件，支持 Free（自由）、Snap（固定）、Custom（自定义）三种模式。按 Grip 键触发 SphereTrace，检测到带 GrabComponent 的 Actor 即吸附。`VRInteraction BPI` 蓝图接口抽象公共逻辑。
- **菜单**：UMG Widget，Motion Controller 菜单键弹出。
- **VR Spectator**：桌面观察者模式，按 Tab 切换，不支持 Mobile VR（如 Quest 独立模式）。

### 对项目的影响

本项目不从 VR 模板直接创建，但模板中的传送、抓取、菜单模式可作为蓝图的参考实现。战斗系统（冷兵器挥砍、格挡、脱手）需要在此基础上自定义。

---

## 2. OpenXR

### 运行时（Runtime）

- 每个平台有独立 OpenXR 运行时。
- 多运行时共存时，需用 `OpenXR Explorer` 工具切换，或设置环境变量。
- **重要**：使用 OpenXR 插件时，必须禁用 Oculus、SteamVR、Windows Mixed Reality 插件。

### 插件优先级

引擎按以下顺序检查插件，选择第一个能连接运行时的：

1. Oculus
2. OpenXR
3. Windows Mixed Reality
4. SteamVR

### 引擎内置扩展插件

- `OpenXRHandTracking` — 手部追踪
- `OpenXREyeTracker` — 眼动追踪
- `XRVisualization` — XR 可视化
- `OpenXRMsftHandInteraction` — 微软手部交互
- `HP Motion Controller` — HP 控制器
- `OpenXRViveTracker` — Vive 追踪器
- `XRScribe` — XR 录制

### 支持的设备

| 分类 | 设备 | 验证方式 |
|---|---|---|
| 内部验证 | Meta Quest 2/3（PC + Android）、HTC Vive、Valve Index | Epic 官方测试 |
| 外部验证 | **PICO**（Fab 插件）、Meta Quest、WMR、Varjo、Magic Leap | 厂商负责 |

**PICO 的 OpenXR 支持通过 Fab 插件提供**，不在引擎内置验证范围内。PICO 插件地址：https://www.fab.com/listings/a7eb0f28-d7f1-4b30-8d2d-49d12eeb1d62

### 对项目的影响

- 当前 `.uproject` 已启用 `OpenXR`、`OpenXREyeTracker`、`OpenXRHandTracking`、`PICOController`，方向正确。
- PICO 作为外部验证设备，PC VR Preview 模式走 SteamVR OpenXR 运行时（PICO 串流助手），不走 Android 独立 OpenXR 运行时，因此之前 Neo3 真机 APK 的 EGL compositor 不兼容问题不影响 VR Preview 开发。
- 如需扩展手部追踪或眼动追踪，`OpenXRHandTracking` 和 `OpenXREyeTracker` 插件已就绪。

---

## 3. Enhanced Input（增强输入）

UE5 默认输入系统，项目 Build.cs 已依赖 `EnhancedInput`。

### 核心概念

| 概念 | 说明 |
|---|---|
| **Input Action** | 数据资产，表示"蹲下""开火"等行为。类型：bool、Axis1D(float)、Axis2D(FVector2D)、Axis3D(FVector) |
| **Input Mapping Context** | 输入映射集合，可运行时动态添加/移除/调整优先级。不同场景切换不同 Context |
| **Input Modifier** | 预处理器，修改原始输入值（死区、轴交换、取反、平滑等） |
| **Input Trigger** | 触发器，定义输入如何激活 Action（按下、按住、双击、和弦等） |

### 触发状态

- **Triggered**：触发完成（最常用）
- **Started**：触发评估开始（如双击的第一击）
- **Ongoing**：持续触发中（每帧）
- **Completed**：评估完成
- **Canceled**：触发取消（如按住时间不足）

### C++ 绑定示例

```cpp
void AFooBar::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    UEnhancedInputComponent* Input = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    Input->BindAction(AimingInputAction, ETriggerEvent::Triggered, this, &AFooBar::SomeCallbackFunc);
}

void AFooBar::SomeCallbackFunc(const FInputActionInstance& Instance)
{
    FVector VectorValue = Instance.GetValue().Get<FVector>();
    FVector2D Axis2DValue = Instance.GetValue().Get<FVector2D>();
    float FloatValue = Instance.GetValue().Get<float>();
    bool BoolValue = Instance.GetValue().Get<bool>();
}
```

### 对项目的影响

- VR 输入（Motion Controller 的摇杆、扳机、握把、按钮）通过 Enhanced Input 的 Axis3D 类型映射。
- 战斗动作（挥砍检测、格挡姿态、武器切换）各为一个 Input Action。
- 不同模式（生涯/自定义/训练、菜单/战斗）用不同 Mapping Context 切换，避免输入冲突。

---

## 4. 全身 IK（Control Rig Full Body IK）

> 文档：https://dev.epicgames.com/documentation/zh-cn/unreal-engine/control-rig-full-body-ik-in-unreal-engine

### 概述

FBIK 是 Control Rig 中的节点，基于**位置 IK（Position-Based IK）** 框架，提供速度更快的绑定性能、逐骨骼设置、偏好角度和挤压拉伸。专为程序调整设计（如地面对齐、手臂伸展）。

**前置条件**：启用 `FullBodyIK` 插件（Edit > Plugins），已有 Control Rig 资产。

### 创建流程

1. Control Rig 图表中右键 → **层级 > 全身 IK**，连接到 `Forwards Solve` 节点
2. 设置 **Root** 骨骼（通常为骨盆/臀部）
3. 创建功能按钮（头、手、脚），为每个按钮添加 **执行器（Effector）**
4. 每个执行器设置对应的 **Bone**，并从 `Get Transform` 节点连接变换引脚

### 骨骼设置（Bone Settings）

骨骼设置控制 IK 链中每个骨骼的行为，解决"臀部太激进""腿部僵硬""脚踝不自然"等常见问题：

| 属性 | 说明 |
|---|---|
| **旋转/位置刚度** | 0 = 完全自由，1 = 完全锁定。用于控制骨盆等骨骼的移动幅度 |
| **偏好角度** | 指定关节沿特定轴向弯曲。如膝盖沿 Z 轴正方向弯曲 45° |
| **限值** | 限制骨骼轴旋转范围：Free / Limited（Min-Max）/ Locked。如脚踝 Z 轴限制 -70°~70° |
| **排除骨骼** | 从 FBIK 解算中排除特定骨骼，建议优先使用此方式而非设死刚度 |

### 节点参数

| 参数 | 说明 |
|---|---|
| **执行器 - Position/Rotation Alpha** | 0 = 保持输入姿势，1 = 到达目标 |
| **执行器 - Strength Alpha** | 该执行器对 IK 链的拉力强度 |
| **执行器 - Pull Chain Alpha** | 将骨架划分为多个链，改善稀疏骨骼链结果 |
| **迭代次数** | 增大直到收敛，但增加 CPU 开销。刚度高/质量乘数高时需更多迭代 |
| **质量乘数** | 0~5，骨骼对旋转/平移的抵抗程度 |
| **允许拉伸** | 允许骨骼平移以到达执行器，位置刚度影响拉伸量 |
| **根行为**：Pre Pull | 根和子节点随执行器拉伸平移，适合远距离收敛 |
| **根行为**：Pin to Input | 锁定根骨骼，用于短距离/非全身设置 |
| **根行为**：Free | 根骨骼自由移动 |

### 对项目的影响

- 全身 IK 是 `GameMasterPlan.md` 的硬性要求
- 实现路径：VR 头显/控制器位置 → Control Rig 的 head/hand 功能按钮 → FBIK 节点求解脊柱和腿部
- 骨盆刚度设为 0.8 左右保留自然摆动，膝盖设偏好角度保证向前弯曲
- 脚踝限值防止 VR 追踪抖动导致不自然姿势

---

## 5. 动画系统

### 骨骼动画管线

- Skeletal Mesh → Animation Blueprint → State Machine / Blend Space → 最终姿势
- Animation Blueprint 中可插入 IK Rig 节点进行后处理

### Control Rig

- 编辑器内创建动画绑定，可直接在引擎中制作动画
- 可用于战斗动作的微调（武器轨迹、命中姿势）

### 对项目的影响

- 战斗动画：挥砍、格挡、受击、脱手——需要 Animation Blueprint 状态机管理。
- 武器动画：每种武器需要独立的动画集，通过 Blend Space 或分层混合切换。
- AI 角色动画：与玩家共用骨骼和 IK 系统，Animation Blueprint 通过变量切换行为。

---

## 6. VR 性能优化

### 帧率目标

- GPU 预算 < 11ms（考虑重投影开销）
- 掉帧比传统渲染更严重（导致用户不适）
- 游戏线程、渲染线程、GPU 三者需平衡

### 内容优化清单

- 避免动态光照和阴影
- 避免大量半透明
- 所有资产制作 LOD
- 降低材质复杂度和材质数量
- 烘焙可烘焙的一切
- 避免覆盖玩家的大几何体
- 使用预计算可见性体积
- 屏幕空间特效在立体渲染中可能表现异常

### 引擎性能特性

| 特性 | 说明 | 平台限制 |
|---|---|---|
| **Instanced Stereo** | 减少 CPU 绘制调用，一次渲染两眼 | Windows（DX11/DX12） |
| **Mobile Multiview** | 移动端 Instanced Stereo 等效 | Android（Mali GPU） |
| **VRS + Fixed Foveated Rendering** | 降低视野边缘着色率，提升 GPU 性能 | Windows DX12/Vulkan、Quest |
| **Forward Rendering** | 前向渲染，更快基线，更好的抗锯齿 | 所有平台 |

### 性能剖析命令

- `stat unit`：游戏线程/绘制线程/GPU 时间
- `stat gpu`：GPU 实时统计
- `Ctrl+Shift+,`：GPU Profiler 窗口
- `startfpschart` / `stopfpschart`：帧率分布统计

### Post Process 优化

VR 项目中应禁用以下高开销后处理：
- Lens Flares
- Screen Space Reflections
- Temporal AA（视情况）
- SSAO
- Bloom

### 对项目的影响

- 一期以 4v4 压力场景验证性能（`GameMasterPlan.md` 要求）。
- 灰盒阶段优先使用 Forward Rendering 降低开销。
- Mobile Multiview 在 Neo3 APK 部署时曾因 GPU 驱动兼容问题崩溃（`vr.MobileMultiView=0` 修复），后续 APK 阶段重测。
- Post Process Volume 设置无限制范围并禁用高开销特性。

---

## 7. 5.6 与 5.8 差异

### 5.8 新增（本项目用不到）

- **ModelContextProtocol** 插件：编辑器 MCP 服务器，5.6 中不存在
- **AllToolsets** 插件：编辑器工具集，5.6 中不存在
- 其他渲染、动画、工作流更新（与当前项目阶段无关）

### 5.6 优势

- OpenXR 运行时版本较老，与 PICO Neo3 系统 OpenXR 运行时（3.0.1）兼容性更好
- 社区插件和教程资源更丰富
- 稳定性经过更长时间验证

---

## 8. AI 系统：行为树与 StateTree

### 8.1 行为树（Behavior Tree）

> 文档：https://dev.epicgames.com/documentation/zh-cn/unreal-engine/behavior-tree-in-unreal-engine---overview

#### 核心概念

| 组件 | 说明 |
|---|---|
| **黑板（Blackboard）** | 独立资源，存储 AI 决策所需数据（黑板键），如 HasLineOfSight、TargetLocation |
| **合成节点（Composite）** | Selector（选择子节点直到成功）、Sequence（依次执行直到失败）、Simple Parallel（A+B 并发） |
| **任务节点（Task）** | AI 可执行的动作，如 MoveTo、PlayAnimation |
| **装饰器（Decorator）** | 条件判断，UE 推荐用装饰器替代传统条件叶节点——更直观、可读 |
| **服务节点（Service）** | 关联到合成节点，按周期执行，如定期更新最佳目标 |

#### 关键特性

- **事件驱动**：不每帧轮询，被动监听事件触发变化。避免"我们到了吗？"式轮询，性能更好
- **观察者中止（Observer Aborts）**：装饰器观察黑板值变化，条件不满足时自动中止当前分支。如猫扑老鼠时老鼠逃入洞中立即中止
- **简单平行节点**：两个子项——主任务 + 填充任务，如"攻击敌人，同时向敌人移动"
- **执行流程**：AI 控制器 → RunBehaviorTree → Pawn 关联

### 8.2 StateTree（状态树）

> 文档：https://dev.epicgames.com/documentation/zh-cn/unreal-engine/overview-of-state-tree-in-unreal-engine

**StateTree 是 UE5 新增的通用分层状态机**，组合了行为树的选择器 + 状态机的状态和过渡。比行为树更灵活、更高效，适合复杂 AI 行为。

#### 与行为树对比

| 特性 | 行为树 | StateTree |
|---|---|---|
| 结构 | 树形，Composite + Task | 分层状态，Selector + State + Transition |
| 执行 | 事件驱动，从上到下从左到右 | 选择-激活-过渡，从根向叶遍历 |
| 并发 | 简单平行节点 + Service | 状态内 Tasks 并发执行 |
| 数据流 | 黑板（Blackboard） | 参数 + 上下文数据 + 求值器 + 全局任务 |
| 蓝图扩展 | Task/Decorator/Service 基类 | Task/Evaluator/Condition 基类 |

#### 选择流程

1. 从根开始，对每个状态的 **进入条件（Enter Conditions）** 求值
2. 通过 → 继续到子状态；失败 → 跳过到同级
3. 到达叶状态 → 激活，并发执行所有 Task
4. 首个完成的 Task 触发 **过渡（Transition）** → 重新选择

#### 数据流

| 数据类型 | 说明 |
|---|---|
| **参数（Parameters）** | 外部传入，如动画资产 |
| **上下文数据（Context Data）** | 运行时自动注入，如所属 Actor |
| **求值器（Evaluators）** | 自定义数据源，如时间系统 |
| **全局任务（Global Tasks）** | 树启动到停止期间持续激活 |

#### 对项目的影响

- **AI 队友/敌方**：三层架构——队伍决策（StateTree）→ 个体战术（Behavior Tree）→ 动作执行（Task）
- 队伍层用 StateTree 管理阵型、目标分配、侧翼协同
- 个体层用 Behavior Tree 处理感知、移动、攻击、防御
- 简单 AI（如训练模式假人）可直接用 Behavior Tree

---

## 9. OpenXR 输入

> 文档：https://dev.epicgames.com/documentation/zh-cn/unreal-engine/openxr-input-in-unreal-engine

### 交互配置文件

OpenXR 使用交互配置文件支持各种硬件控制器，运行时自动模拟未显式绑定的映射。**只为你能测试的控制器添加绑定**即可。

### 两个核心姿势

| 姿势 | 说明 |
|---|---|
| **Grip（抓握）** | 用户抓握虚拟对象的位置和方向 |
| **Aim（瞄准）** | 从手/控制器延伸的光线，用于指向目标 |

### 坐标系差异

UE 使用左旋坐标系：+X 向前，+Z 向上，+Y 向右（与 OpenXR 标准不同，引擎自动转换）。

### 对项目的影响

- 挥砍检测用 Aim 姿势的轨迹采样
- 武器握持用 Grip 姿势
- 启用 `OpenXRMsftHandInteraction` 插件可复制追踪手的 Grip/Aim 姿势

---

## 10. 碰撞与物理

> 文档：https://dev.epicgames.com/documentation/zh-cn/unreal-engine/collision-in-unreal-engine

### 碰撞查询类型

| 类型 | 用途 | 适合场景 |
|---|---|---|
| **Line Trace** | 单条射线，返回首个命中 | 精确武器轨迹采样 |
| **Sphere Trace** | 球体扫描 | 挥砍检测（替代多条射线） |
| **Box/Capsule Trace** | 盒体/胶囊扫描 | 范围攻击、推撞检测 |
| **Overlap** | 重叠检测，不拦截 | 触发区域、武器进入判定区 |

### 碰撞通道

项目中建议创建自定义碰撞通道以区分：
- `Weapon`（武器命中）
- `Shield`（盾牌格挡）
- `BodyPart`（身体部位——头/躯干/四肢）
- `Projectile`（弓箭射弹）

### 对项目的影响

- 挥砍检测：每帧在武器刃部采样 Sphere Trace，检测与敌方 `BodyPart` 通道的碰撞
- 连续同一挥击需去重：记录已命中的 Actor+部位，同一挥击内不重复计数
- 碰撞响应区分"轻触"和"有效攻击"：速度阈值 + 入射角 + 有效武器部位

---

## 11. MCP 文档搜索工具

本项目已配置 `unreal-engine-docs-mcp` MCP 服务器，收录 **2415 个** UE 5.6 官方文档页面。

### 使用方式

```
search_docs_list(
  search={en: "英文搜索词", cn: "中文搜索词"},
  keyword=[{en: "关键词1", cn: "关键词1"}, {en: "关键词2", cn: "关键词2"}]
)
```

- 关键词匹配优先于语义搜索，按数组顺序排列优先级
- 向量搜索需要 Ollama 服务（可选），关键词模式无需额外依赖
- 返回结果包含文档标题、描述和官方链接

---

## 维护说明

- 本文档随项目需求补充，不追求覆盖引擎全部功能。
- 新增章节时注明文档来源 URL 和抓取日期。
- 与 `TechnicalDecisions.md` 的技术决策保持同步。
- 需要更详细的技术信息时，优先使用 `search_docs_list` MCP 工具搜索官方文档。