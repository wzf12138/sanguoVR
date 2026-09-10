# CR-20260908-001 · 串流输入修复攻坚：SteamVR 对照变更回溯 + M01-T001 范围扩展（NTFS 临时解锁）

- 关联任务：M01-T001（武器握持 + VRE 集成）
- 性质：① 回溯登记（SteamVR 对照试验期间三项项目文件变更，用户逐项批准）② 范围扩展裁定（IMC_Weapon 条件授权 + NTFS 临时解锁）
- 实施：exec-m01-t001（session-20260906-001）；裁定与整理：decision 指挥台（2026-09-08，十封积压信批量处理轮）

## A. SteamVR 对照试验攻坚变更回溯（2026-09-08，executor 实施，用户批准）

背景：F3/A SteamVR 运行时对照试验（用户批准切换 ActiveRuntime；注册表已备份，试验完成后回切 PICO）。攻坚五障碍：

1. xrCreateInstance 失败 → SteamVR 共享 IPC 命名空间损坏 → PC 重启解决（环境项，无文件变更）。
2. XR_ERROR_VALIDATION_FAILURE → PICO 插件将 `XR_BD_controller_interaction` 列为 required，SteamVR 不支持该扩展 → **PICO_Controller.cpp required→optional**（用户批准；真机无影响——真机运行时支持该扩展）；编译通过。
3. 仍 VALIDATION_FAILURE → UE 请求 OpenXR API 1.1，SteamVR 仅支持 1.0 → **Config/DefaultGame.ini 钉 OpenXR API 1.0**（PICO 运行时兼容 1.0，无回归影响）。
4. 仍失败 → PICO_HMD 请求 XR_EXT_RENDER_MODEL 缺前置 XR_EXT_UUID → **PICO_HMD.cpp 补依赖**；此后 xrCreateInstance 成功。
5. 成功态：VR Preview 渲染/追踪正常、绑定文件加载、remapping 成功、**SteamVR 绑定测试器按钮点亮（驱动层输入数据正常）**。

注意：三项变更中 ②③④ 超出 M01-T001 原白名单（PICOOpenXRHMD 模块与 DefaultGame.ini 不在列），本 CR 为回溯登记；diff 行号细节由 executor 下次回执校对补充。

## B. 根因闭合（本项目 bug，非串流层主因）

**BP_VRCharacter 的 BeginPlay 从未执行 AddMappingContext**（08-31 桥崩溃后置项一直未补；蓝图事件图 BeginPlay 孤立无连线，仅 IA_Grab 事件→TryGrip/ReleaseGrip 接线存在）。UE5.6 OpenXRInput.cpp L902：每帧只 sync 已激活 IMC 对应的 action set，未激活 → 永远零输入。

- 该缺漏统一解释 PICO 与 SteamVR 双运行时完全相同症状（渲染/追踪正常、按钮全死）。
- 差分证据：模板 Pawn（有完整接线）08-13 真机抓取成功；BP_VRCharacter（无接线）从未真机验证。
- 两个真 bug 叠加史：battery 绑定注册失败（真 bug，CR-20260905-001 已修）+ 输入映射从未激活（真 bug，本 CR 修复）。串流层是否另有独立问题，待 pawn 修复后实测判定。

## C. 范围扩展与解锁裁定（decision，2026-09-08）

- 修复内容：① BP_VRCharacter BeginPlay 补 AddMappingContext 链（白名单内既有授权，先做——决定性测试）② IMC_Weapon_Left/Right 补 IA_Grab→Grip 映射（**条件授权**：executor 须先书面说明必要性——IMC_Default 已有 IA_Grab→PICO 键映射，激活链修好后即应生效，决策侧判定有冗余嫌疑；报 decision 批准后方可触碰）。
- NTFS 临时解锁：用户以管理员运行 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\Unlock-TraeAssets.ps1`（脚本已由指挥台核验：admin 检查 ✓、目标范围 Input 目录 + BP_VRCharacter ✓、-Restore 回锁 ✓）→ **运行行为即视为批准本 CR 范围**；全部完成或中止后立即 `-Restore` 回锁。
- BP 节点编辑风险（TD-014）：BeginPlay 补链优先尝试 `import_nodes_t3d`（单次尝试，改前先 save_all_dirty 保住 IMC 成果），失败则用户编辑器内手工接线（executor 提供节点清单）。
- 落盘纪律（TD-015）：每步修改后立即 `asset.save_all_dirty`；禁用 editor.save_dirty。
- 白名单同步扩展：IMC_Weapon_Left/Right.uasset 两行 + 本 CR 文件（ALLOWLIST.txt 已更新）。

## 状态

- A 项：已实施（本 CR 回溯登记），待 executor 校对 diff 行号。
- B 项：根因闭合，待修复 + VR Preview 决定性测试（IA_Grab/IA_Shoot/IA_Hand + TryGrip 诊断）。
- C 项：已裁定，待用户运行解锁脚本 → executor 修复 → 测试 → -Restore 回锁。
- **2026-09-08 22:2x 结算（msg-20260908-224655）**：用户直接批准并运行解锁脚本（用户即最终决策者，既成事实追认）。executor 于裁定信送达前完成 Phase 2（IMC_Weapon IA_Grab×OculusTouch_Grip_Click 映射，书面理由已采纳——PICO 真机路径 PICONeo3 键与 SteamVR 路径 OculusTouch 键为不同运行环境并行路由非冗余，裁定**维持不回滚**，下轮测试盯 oculus 路径报错刷屏）+ BeginPlay 补链（4 IMC 全激活，add_node 解锁态零崩溃）。**B 项决定性验证通过**：PICO 模式下 IA_Grab_Right_Pressed → TryGrip 蓝图栈日志实锤。
- **2026-09-08 深夜**：抓取路径首次真实执行触发新 bug（VRSanguoGripLibrary.cpp L34 直调接口事件）→ 快速通道修复 + 治理四项裁定见 **CR-20260909-001**。
