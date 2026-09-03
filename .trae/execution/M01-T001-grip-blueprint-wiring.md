# M01-T001 蓝图接线清单（降级方案 B - 用户手动搭）

> 背景：ue-bridge 的图编辑工具（`edit-blueprint-graph`）在执行写入时触发
> `UEBridgeMCP.dll!FMcpToolRegistry::ExecuteTool()` 崩溃（manager 已确认该插件不稳定）。
> 即使禁用 `execute_python` 仍崩溃（崩溃栈相同），满足 manager 裁决中的降级条件
> （"编辑器再次崩溃" + "图工具写入后无法确认"）。故按方案 B 产出本清单交由用户手动接线，
> 执行模型只负责后续编译 + PIE 验证。
>
> 生成时间：2026-08-31　依据：manager 裁决 `msg-20260831-090524-manager-001`。

## 0. 前置确认（请在搭线前核对）

1. 编辑器可正常打开 `BP_VRCharacter`（路径 `/Game/VRSanguo/VR/BP_VRCharacter`）。
2. 蓝图事件图名称为 `EventGraph`（默认）。
3. 蓝图里可见来自父类 `AVRCharacter`/`AVRBaseCharacter` 的成员：
   - 变量 `LeftMotionController`（`UGripMotionControllerComponent*`，蓝图可读）
   - 变量 `RightMotionController`（`UGripMotionControllerComponent*`，蓝图可读）
4. 输入动作资产（已存在于 `/Game/VRTemplate/Input/Actions/`）：
   - `IA_Grab_Right_Pressed` / `IA_Grab_Right_Released`
   - `IA_Grab_Left_Pressed` / `IA_Grab_Left_Released`
5. C++ 函数库（已编译，出现在蓝图右键"调用函数"列表，分类 `VRGrip`）：
   - `TryGrip(MotionController, SphereRadius, ForwardDistance, OptionalSocketName)` → bool
   - `ReleaseGrip(MotionController)` → bool
6. 剑的可抓取 socket 名：`VRGripP__0`（主手）/ `VRGripS__0`（副手）。

## 1. 右手（主手）抓取 → 两根连线

**节点 A：EnhancedInputAction 事件（IA_Grab_Right_Pressed）**
- 在事件图空白处右键 → 搜索 `IA_Grab_Right_Pressed` → 选择"增强输入动作事件（Enhanced Input Action Event）"。
- 确认节点标题显示 `IA_Grab_Right_Pressed`。
- 使用其执行输出引脚 **`Started`**（按下瞬间触发；也可用 `Triggered`，二者皆可，建议 `Started`）。

**节点 B：Get（取变量）**
- 右键 → 搜索 `RightMotionController` → 选择 `Get RightMotionController`（或直接拖 `Right Motion Controller` 到图）。
- 输出引脚：`UGripMotionControllerComponent`（返回值）。

**节点 C：调用函数 `TryGrip`**
- 双击空白 → 搜索 `TryGrip` → 选中（分类 `VRGrip`）。
- 输入引脚：
  - **`MotionController`** ← 连 节点B(Get 的输出)；注意不要连成 `self`（会在后续出错，必须在引脚菜单选择正确对象）。
  - `SphereRadius` = 12
  - `ForwardDistance` = 30
  - `OptionalSocketName` = `VRGripP__0`
- 执行输入 `then` ← 连 节点A 的 `Started`。

**连线关系**：
```
[IA_Grab_Right_Pressed .Started]  →  [TryGrip .then]
[Get RightMotionController .返回值] →  [TryGrip .MotionController]
```

## 2. 右手（主手）释放 → 两根连线

**节点 D：EnhancedInputAction 事件（IA_Grab_Right_Released）**
- 右键 → 搜索 `IA_Grab_Right_Released` → 增强输入动作事件。
- 使用执行输出引脚 **`Completed`**（松开瞬间）。

**节点 E：Get（取变量）**
- 同节点 B：取 `RightMotionController`。

**节点 F：调用函数 `ReleaseGrip`**
- 双击 → 搜索 `ReleaseGrip`（分类 `VRGrip`）。
- 输入引脚：`MotionController` ← 连 节点E(Get) 的输出。
- 执行输入 `then` ← 连 节点D 的 `Completed`。

**连线关系**：
```
[IA_Grab_Right_Released .Completed] →  [ReleaseGrip .then]
[Get RightMotionController .返回值] →  [ReleaseGrip .MotionController]
```

## 3. 左手（副手）抓取 → 两根连线

**节点 G：EnhancedInputAction 事件（IA_Grab_Left_Pressed）**
- 同节点 A，但搜索 `IA_Grab_Left_Pressed`，用 **`Started`**。

**节点 H：Get（取变量）**
- 取 `LeftMotionController`。

**节点 I：调用函数 `TryGrip`**
- 输入引脚：
  - `MotionController` ← 连 节点H(Get) 的输出
  - `SphereRadius` = 12
  - `ForwardDistance` = 30
  - `OptionalSocketName` = `VRGripS__0`   ← 副手 socket
- 执行输入 `then` ← 连 节点G 的 `Started`。

## 4. 左手（副手）释放 → 两根连线

**节点 J：EnhancedInputAction 事件（IA_Grab_Left_Released）**
- 搜索 `IA_Grab_Left_Released`，用 **`Completed`**。

**节点 K：Get（取变量）**
- 取 `LeftMotionController`。

**节点 L：调用函数 `ReleaseGrip`**
- 输入引脚：`MotionController` ← 连 节点K(Get) 的输出。
- 执行输入 `then` ← 连 节点J 的 `Completed`。

## 5. 保存与编译（接线完成后）

1. 点击蓝图左上角 **Compile**，确认无错误（若 `TryGrip`/`ReleaseGrip` 变红，说明函数未识别，请先在 `Build` 菜单确认已编译该模块或重启编辑器加载新 DLL）。
2. 点击 **Save**。
3. 关掉蓝图，回到关卡保存关卡（Ctrl+S）。

## 6. 验证要点（留给执行模型，或用户初测）

- 编译通过后，在桌面 PIE（编辑器内按 Play）测试：手柄对剑按 Grip → 剑被抓起；松开 → 剑被释放。
- 抓取半径 12cm、前方 30cm；若手感不对可调大 `SphereRadius`。
- 若抓握点不贴合，检查 `OptionalSocketName` 是否为 `VRGripP__0`/`VRGripS__0`（与关卡中剑的 socket 名一致）。

## 7. 常见坑提醒

- **不要用 `self` 作为函数参数来源**，`TryGrip` 的第一个参数必须是 `GripMotionControllerComponent`（取 `LeftMotionController`/`RightMotionController` 变量），把 `SELF` 接上去会编译报类型错误。
- `EnhancedInputAction` 事件节点需要蓝图**已处于启用 Enhanced Input 的角色**才能被触发；本项目 `BP_VRGameMode` 默认 Pawn 已是 `BP_VRCharacter`，且 `IMC_Default` 已全局注册这四个动作，无需额外配置。
- 若 `IA_Grab_*_Pressed/Released` 事件在搜索框搜不到，请确认蓝图编辑器的"上下文"上下文选择器未过滤手柄层。
