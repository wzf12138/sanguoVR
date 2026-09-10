# CR-20260905-001 · PICO 插件 battery 绑定门控修复 + 关闭手部交互 EXT

> 状态：**实施完成（2026-09-05）——门禁①②⑤已验，③④待用户串流实测，真机复测待用户（与 TC-01~06 合并）** · 提案：decision/manager（用户批准方案 1+3）· 实施：exec-m01-t001（回执 msg-20260905-134723-exec-m01-t001-001，指挥台四项抽查全过）· 关闭：待③④+真机证据

## 1. 背景

M01-T001 PICO 串流验证（PC PIE + PICO Connect）发现手柄按键全链路失效：追踪正常、IA_Grab 永不触发、TryGrip 0 调用。执行会话诊断回执 msg-20260905-120348-exec-m01-t001-001 + 指挥台三方验真，根因实锤：

1. **PICO 插件无条件 battery 绑定**：`PICOOpenXRInput/Private/PICO_Controller.cpp` OnCreateSession（L342-352）无条件创建 battery action；GetSuggestedBindings（L519-533）为每个 PICO profile 无条件追加 `/user/hand/{left,right}/input/battery/value`。
2. **串流运行时缺扩展**：`Saved/Logs/VRSanguoYanWuchang-backup-2026.09.05-03.43.43.log` L818：`Optional extension XR_EXT_interaction_profile_battery_state_display is not available`；L831 确认运行时 PicoStreamingXR (Standalone) v1.1.46；L1636 PIE 中 `XR_ERROR_PATH_UNSUPPORTED`。
3. **OpenXR 建议绑定原子性**：绑定数组中一条不受支持的路径 → 整个 pico_neo3 profile 建议绑定被拒 → IMC 中仅绑 PICO Neo3 键的 IA_Grab/IA_Move/IA_Turn 全链路无绑定。

## 2. 范围变更（用户批准 2026-09-05）

M01-T001 白名单追加：

- `Plugins/PICOOpen174f9f81d266V8/Source/PICOOpenXRInput/Private/PICO_Controller.cpp`（必要时同目录头文件，最小集）
- `Config/DefaultEngine.ini`（仅 `bEnableHandInteractionEXT` 一行，L191 True→False）

其余一切路径维持原白名单不变；`/Game/VRTemplate/Input/*` 模板资产**不在本次范围**（IMC 零改动）。

## 3. 变更内容（方案 1 + 3）

- **方案 1（根治）**：battery action 创建与建议绑定按 `XR_EXT_interaction_profile_battery_state_display` 可用性门控：扩展不可用 → 跳过创建与追加（设计性跳过，非报错，打一条 Verbose/Log 日志留证）；可用 → 行为不变（真机 standalone 端自适应保留）。对齐同插件 haptic 现成门控写法，最小差异，不重构。
- **方案 3（消噪）**：`bEnableHandInteractionEXT=False`（M01 阶段无手部交互功能；未来需要时改回）。

## 4. 风险与回退

- 风险：真机回归——设计上门控自适应，设备运行时支持该扩展则绑定保留，预期无回归；仍需真机复测确认（规则 13 标注验证层级）。
- 回退：git revert 插件源码改动 + `bEnableHandInteractionEXT` 改回 True。

## 5. 验证门禁（全过才算关闭）

1. UBT 编译通过（真实输出）。
2. 重启编辑器 → 串流 PIE：`XR_ERROR_PATH_UNSUPPORTED` 不再出现；gating 日志行出现；`[TryGrip诊断]` 日志出现（IA_Grab→TryGrip 触发）；Grip 键抓取真剑实测走通（截图/日志）。
3. `bEnableHandInteractionEXT` 读回 False，hand 相关报错同步消失。
4. 用户 PICO 真机 standalone 复测（串流 PIE ≠ 真机，分别标注）。

## 6. 实施记录（2026-09-05）

- 实施会话：exec-m01-t001（= session-20260830-001 认领链）；回执 msg-20260905-134723-exec-m01-t001-001。
- 改动落盘（指挥台 grep 抽查验真）：`PICO_Controller.h` L140 新增 flag；`PICO_Controller.cpp` L335 `IsExtensionEnabled` 判定 + L336/358 门控分支 + L369 跳过日志；`Config/DefaultEngine.ini:191` False。`GetSuggestedBindings` 未改——借 `ControllerBatteryAction == XR_NULL_HANDLE` 自动跳过（设计确认，最小差异）。
- 编译：UBT `Result: Succeeded`，`UnrealEditor-PICOOpenXRInput.dll` 重链接。
- 门禁记分：① PATH_UNSUPPORTED 0 条 ✅　② 门控日志 L833/L1106 ✅　⑤ EXT=False ✅　③④ ⏳ 待用户串流戴头显实测　真机复测 ⏳ 用户侧。
- CHANGELOG：已录 2026-09-05 条目。遗留纪律提醒：实施会话改 STATUS.json 未广播（已由指挥台代发 + 回信提醒）。

## 7. 疑似回归调查（2026-09-05 15:34 起，进行中）

- **报告**：用户反馈改动后 VR 预览双手柄/手部模型不显示不追踪（改动前正常）；来件 msg-20260905-153452-exec-m01-t001-001（urgent）。
- **实施中途变更（V1→V2）**：13:47 回执描述 V1（battery action 创建门控，绑定借空句柄自动跳过）；15:34 信披露 V2（action 无条件创建，仅 GetSuggestedBindings 门控，"避免空 action set"）。指挥台 grep 验实现状=V2（L363 创建 / L530 门控）。中途变更未报备，已责令补报备。
- **指挥台排除项**：方案 3 为纯 no-op（`bIsHandTrackingUsed=False` @ini:190 + 激活条件 L213/231 双真才激活，不 gate 扩展启用）——不可能引起追踪丢失。
- **候选机制 H-REG**：改动前 pico profile 绑定从未在串流注册过；改动后首次注册成功，若 v1.1.46 "建议层接受但设备映射不完整"，位姿解析可能被干扰。未证实，待隔离实验。
- **最大嫌疑**：事发轮 PIE 无 XR 会话（executor 自证：无 FOCUSED、位姿 (0,0,0)）——环境因素即可完整解释症状。
- **裁定（msg-20260905-154736-decision-001）**：C-0 环境复核（源码↔DLL 一致性 + 重连串流只验手柄可见）→ 手柄回来则直接进 ③④；不回来则 B-1 只回退方案 1（git revert 插件、方案 3 保留）再测；A 全回退否决。手柄若因方案 1 回退而恢复 → H-REG 坐实 → V3 设计（串流下跳过整个 PICO profile 建议）+ 抓取串流解法另议（方案 2 双绑定 / 升级 PICO Connect）。
- **状态**：**结案（2026-09-05 16:0x）：无回归。** ① 源码↔DLL↔编辑器一致性通过（DLL 14:31:38 晚于 cpp 14:30:44，运行日志文案与 V2 源码匹配）；② 用户重连串流后 XR 会话 FOCUSED（07:55:10 UTC）、手柄可见、位姿非零（Left=(-14.2,-97.9,162.4) / Right=(-53.5,-146.0,190.7)）→ 回执 msg-20260905-155333。事发轮症状 = 死会话环境因素；H-REG 证伪；B-1 回退未触发。V1→V2 补报备收讫（动机：V1 的 ActionInfo 作用域导致 C2065/C3079 编译失败；V2 录为最终实现，编译 1 次成功）。

## 8. 后续层调查：串流下 grip 值不注入（2026-09-05 16:22 起）

- **新事实**（回执 msg-20260905-162216）：XR 会话正常下，IA_Grab_Right_Pressed / IA_Hand_Grasp_Right（同绑 PICONeo3_Right_Grip_Axis）均无值注入；手柄位姿追踪正常。pico profile 绑定注册成功但值不流动 = 原始问题的下一层（值传递层），非本次改动引入（改动前 grip 同样不工作）。
- **指挥台补充事实**：PICO 插件键表含 Grip_Click 与 Grip_Axis 双键（PICO_Controller.cpp L50/51、L66/67）；插件源码无 grip 路径字符串（键→路径映射走 UE 核心约定）；引擎 Marketplace 存在停用副本 `Engine/Plugins/Marketplace/PICOOpen174f9f81d266V8.disabled/`（勿混淆，实际生效副本在项目 Plugins/）。
- **裁定（msg-20260905-164029-decision-001）**：S1 零触实验先行——串流 PIE 下分别按住 TRIGGER / GRIP 各 2 秒，看 IA_Shoot（五 profile 多键）/ IA_Grip 是否有事件。三分支：a) TRIGGER 触发 → A 双绑定路线；b) TRIGGER 触发且 GRIP 设备级事件在而 IA 不动 → C-CLICK（IMC 换绑 Grip_Click，PICO 键保留）；c) 全不触发 → B（PICO Connect 版本 / SteamVR 对照运行时）。**三分支修复均涉模板 IMC 或用户环境，须指挥台呈报用户批准 + 立 CR 后才动**。IA_Hand_* Description 空警告定性为外观性问题，与下张 IMC CR 打包。
- **S1 结果（msg-20260905-205757，暂定 S1-c）**：串流 PIE + FOCUSED（20:49 本地会话）下，三日志类别 Verbose（LogEnhancedInput/LogPICOOpenXRInput/LogOpenXRInput），用户按 TRIGGER/GRIP 各 2 秒 → EnhancedInput 动作值记录零条。判读"运行时不传任何按钮值"。**指挥台暂不接受为终判**——两洞：① LogOpenXRInput 类别已被 D2 证明不存在，Verbose 静默可能只是不产日志；② TRIGGER 分支依赖 IMC_Weapon_R 挂载，executor 只确认过 IMC_Default。
- **指挥台指令（msg-20260905-212327-decision-001）**：双保险补测——get_applied_imcs 全列五张 + BP_VRCharacter 临时 IA 事件探针（IA_Shoot_Right Started + IA_Grab_Right_Pressed，报备后加、测完删）同轮重跑。探针零事件 + 五 IMC 全挂 → S1-c 坐实 → B 路线并行：PICO Connect 版本/更新 + 注册表 ActiveRuntime（只读）+ SteamVR 对照试验（须用户同意）+ executor web 通道查 PicoStreamingXR 1.1.46 已知缺陷。方案 2 双绑定评估暂停（S1-c 下无意义）。
- **S1-c 终判坐实（msg-20260906-134418）**：① 五 IMC 全挂（get_applied_imcs count=5，洞2关闭）；② LogEnhancedInput Verbose 确认落盘工作（L1584-1586，洞1关闭）；③ 双独立实验零事件 + TryGrip 诊断日志缺席 → **运行时不传任何按钮值**。BP 探针路线放弃：blueprint.add_node 两次触发桥崩溃致编辑器退出（TD-014 已立登记册，STATUS 旧备注误标 TD-010 一并补正）。
- **环境事实**：系统 OpenXR 运行时 ActiveRuntime = PICO Connect 的 `picostreaming-openxr.json`（注册表只读取证）；官方帮助中心提示串流按键问题"经 SteamVR 控制器按键绑定调节"→ PICO Connect 输入链路可能依赖 SteamVR 绑定层（与 TD-012 的 SteamVR 串流替代路径在此交汇）。
- **B 路线授权执行单（msg-20260906-135014-decision-001）**：a) executor 零成本三查（PICO Connect 文件版本 / SteamVR 安装探测 / AvailableRuntimes 列表）；b) 用户侧（版本+更新+头显端 APK）；c) web 查证（帮助中心全文 / 更新日志 action 修复 / Streaming APK v4.3.5 适用范围）；d) SteamVR 对照试验（须用户同意）。方案 2 双绑定维持暂停。
- **状态**：B 路线执行中，待证据。
