# CR-20260907-001 · IMC 临时加 PICO4 键映射（验证性变更）

- 关联任务：M01-T001（武器握持 + VRE 集成）
- 类型：临时验证性变更（可回退）
- 提出会话：exec-m01-t001（session-20260906-001）
- 用户批准：chat ask_user_question 2026-09-07（"做这个试验（推荐）"）

## 背景

S1-c（按钮值不注入 Enhanced Input）于 2026-09-06 晚有效复现（XR 会话 FOCUSED 全程 + 用户头显可见游戏场景 + 按键多次 + 三层日志零事件）。根因候选收敛：

**主假设**：Neo3 手柄硬件与 PICO4 手柄同款，PicoStreamingXR 1.1.46 可能把设备 interaction profile 上报为 `/interaction_profiles/bytedance/pico4_controller`（PICO 插件已注册 PICO4 键前缀），而项目 IMC 仅用 `PICONeo3_*` 键（挂 `pico_neo3_controller` profile）→ action 绑定挂在无设备 profile 上 → 位姿正常（xrLocateViews 不走 action）、按键全无；IMC 现有 ValveIndex/OculusTouch/Vive/MixedReality 多键也不含 PICO4 → 全不匹配。所有症状自洽。

支持证据：
1. 运行时支持 `XR_BD_controller_interaction`（日志两次打印）→ bytedance 命名空间 profile 被认识。
2. PICO 插件 `GetInteractionProfiles`（PICO_Controller.cpp L467-521）无门控注册 pico_neo3/pico4 双 profile。
3. PIE 按键窗口内 PICO 输入插件完全沉默、引擎 LogOpenXRInput 零输出、无绑定失败记录（2026-09-07 日志深查）。

## 变更内容（最小差异，2 条映射）

- `/Game/VRTemplate/Input/IMC_Weapon_Right.IMC_Weapon_Right`：
  1. `IA_Shoot_Right` 增加 `PICO4_Right_Trigger_Click`
  2. `IA_Grip_Right` 增加 `PICO4_Right_Grip_Axis`

## 白名单

- `/Game/VRTemplate/Input/IMC_Weapon_Right.uasset`（仅此一资产）

## 验证

- PIE（L_SkeletonTest）+ 用户实按（右手扳机 2s + 侧键 2s）+ 日志判定（IA_Shoot/IA_Grip 事件、[TryGrip诊断]）。
- 有事件 = pico4 profile 假设实锤 → 映射保留并转正式方案；无事件 = 假设排除 → 移除 2 条映射回退。

## 回退方式

- `remove_imc_mapping` 移除上述 2 条（或 asset.set_property 还原 IMC 数组）。

## 状态

- 实施记录（2026-09-07 晚）：
  1. 2 条映射已在编辑器内存生效（IMC_Weapon_Right: IA_Shoot_Right+PICO4_Right_Trigger_Click；IMC_Default: IA_Grab_Right_Pressed+PICO4_Right_Grip_Axis）。注：IA_Grip_Right 实际名为 IA_Grab_Right_Pressed（本 CR 初稿笔误，已在实施中修正）。
  2. **落盘被 NTFS 只读保护正确拒绝**（Content/VRTemplate/Input/*.uasset IsReadOnly=True，治理设计；日志实锤 `Cannot remove ... as it is read only`）——按 AGENTS.md 权限规则不绕过 ACL。试验用内存态即可（PIE 加载内存版资产）。
  3. editor.save_dirty 桥 handler 崩溃编辑器一次（EditorHandlers.cpp:1221，桥 1.0.87 bug，**新桥技术债**）；改用 asset.save_all_dirty 路径（仍因只读未落盘，符合预期）。
- **试验结果（2026-09-07 21:50 PIE，XR FOCUSED 实证）**：用户实按扳机+侧键后 IA_Shoot/IA_Grab/TryGrip **仍零事件**（日志窗口 67 行内无任何输入事件）→ **pico4 profile 假设排除**。
- 同窗口新证据：LogHMD 打印全部 IA/IMC 的 OpenXR action 创建警告（Description 重复类，无害）→ **引擎 OpenXRInput action 管线工作正常**（IMC→action 创建成功、绑定建议被接受、无报错）。
- 收敛判定：action 创建 ✅ + 绑定建议 ✅ + 位姿 ✅（xrLocateViews）+ 摇杆疑似有值（历史实测可移动）——**grip/trigger 值不流动 = PicoStreamingXR 1.1.46 串流运行时对 grip/trigger 输入路径的路由缺陷（候选实锤方向）**。
- 映射处置：暂留内存（编辑器重启自然消失；若走 F3 切 SteamVR 运行时可能复用做二次判定）；是否持久化待根因闭环后按正式方案定。
