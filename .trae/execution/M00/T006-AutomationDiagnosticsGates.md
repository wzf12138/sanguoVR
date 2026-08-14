# M00-T006 自动化、诊断与交付门禁

- 状态：见 `../active/STATUS.json`（本详规不复制动态状态）
- 优先级：P1
- 前置任务：M00-T005（系统骨架，需接口与 DataAsset 基类就位）
- 目标：建立最小自动化测试、日志验证、性能采样基线和构建门禁。

> **修订说明（2026-08-13）**：原 T006 详规仅 25 行、标记"已批准"但交付物从未实现（V-006 待验证、Source 无测试文件、无活动任务包）。本次修订：扩充为可执行步骤，拆分 T005 后可做与 M01 后 deferred 部分，纠正状态为 ready。

---

## 这个任务在完整游戏开发中的位置

```
已完成：
  T001-T004 ✅ -> 治理、Git、编译、VR/PICO 基线全部 approved

前置：
  T005 系统骨架（ready）-> 提供接口、DA 基类、日志分类、流程状态机

本任务 T006：
  为 T005 产出建立自动化测试、构建门禁和性能基线
  ── 这是"后续 M01+ 战斗测试的自动化基础"

之后：
  M00 里程碑验收 -> M01 战斗切片
```

---

## 实施步骤

### Step 1：构建门禁验证（无 T005 依赖，可并行）

**验证项**：

| 构建目标 | 验证方式 | 预期 |
|----------|----------|------|
| Win64 Development Editor | `Rebuild.bat VRSanguoYanWuchangEditor Win64 Development` | Succeeded |
| Android Development (APK) | `BuildCookRun -platform=Android -configuration=Development` | BUILD SUCCESSFUL |

**新增文件**：
- 无（验证现有构建链路，记录结果）

**交付物**：构建验证记录（写入任务报告）

---

### Step 2：日志分类验证（依赖 T005 Step 1）

验证 T005 定义的 8 个日志分类在运行时可用：

| 日志分类 | 验证方式 |
|----------|----------|
| `LogVRSanguoCore` | 模块启动时输出一条日志 |
| `LogVRSanguoVR` | OpenXR 初始化时输出 |
| `LogVRSanguoCombat` | TestDummy ReceiveDamage 时输出 |
| `LogVRSanguoWeapon` | 武器接口调用时输出 |
| `LogVRSanguoMovement` | 移动接口调用时输出 |
| `LogVRSanguoAI` | AI 接口调用时输出 |
| `LogVRSanguoFlow` | 状态机迁移时输出 |
| `LogVRSanguoPerf` | 性能采样时输出 |

**验证方式**：编辑器 PIE 运行 `L_SkeletonTest`，检查 Output Log 中 8 个分类均有输出。

**交付物**：日志验证截图/记录

---

### Step 3：DataAsset 校验测试（依赖 T005 Step 3）

**新增文件**：
- `Source/VRSanguoYanWuchang/Public/Tests/VRDataAssetSpec.h`
- `Source/VRSanguoYanWuchang/Private/Tests/VRDataAssetSpec.cpp`

**测试内容**（使用 UE Automation Test 框架 `IMPLEMENT_SIMPLE_AUTOMATION_TEST`）：

| 测试 | 验证项 |
|------|--------|
| `FVRWeaponDefinitionSpec` | SchemaVersion 默认值 = 1；ValidateData() 检测空 WeaponID |
| `FVRArmorDefinitionSpec` | CoverageMap 非空；ResistanceMap 值在 0-1 范围 |
| `FVRMovementProfileSpec` | TeleportMaxDist > 0；TeleportCooldown >= 0 |
| `FVRMatchRuleSetSpec` | DefaultTeamSize = 3；AllowedSizes 包含 2-4 |
| `FVRUnitDefinitionSpec` | UnitType 有效；EquipmentRef 非空时可解析 |
| `FVRCommanderDefinitionSpec` | CommanderID 非空；WeaponPool 非空 |
| `FVRArenaDefinitionSpec` | Boundary 非空；SpawnPoints 数量 >= 2 |
| `FVRAvatarProfileSpec` | HitZone->BoneMapping 覆盖 6 个部位 |

**验证方式**：`Running Tests` 面板运行自动化测试，全部通过。

**交付物**：自动化测试通过截图

---

### Step 4：接口与流程状态机测试（依赖 T005 Step 2/4/5）

**新增文件**：
- `Source/VRSanguoYanWuchang/Public/Tests/VRInterfaceSpec.h`
- `Source/VRSanguoYanWuchang/Private/Tests/VRInterfaceSpec.cpp`
- `Source/VRSanguoYanWuchang/Public/Tests/VRGameFlowSpec.h`
- `Source/VRSanguoYanWuchang/Private/Tests/VRGameFlowSpec.cpp`

**接口测试**：

| 测试 | 验证项 |
|------|--------|
| `FVRCharacterCapabilitySpec` | VRCharacterCapabilityComponent 可挂载；RequestAction 返回 false（桩）；GetCapabilityState 返回 Idle |
| `FVRTestDummySpec` | AVRTestDummy 可生成；ReceiveDamage 日志输出 FCombatResult 字段；IsAlive 返回 true |

**流程状态机测试**：

| 测试 | 验证项 |
|------|--------|
| `FVRGameFlowTransitionSpec` | Calibration -> Ready 合法迁移成功 |
| | Ready -> Generate -> Combat -> Settlement -> Reset 合法链路 |
| | Reset -> Ready 可循环 |
| | 非法迁移被拒绝（如 Combat -> Ready 跳过 Settlement） |
| | RequestPhaseTransition 幂等：重复请求同阶段无副作用 |
| | StartMatch/EndMatch/ResetMatch 行为正确 |
| | OnPhaseChanged 委托正确广播 |

**验证方式**：Automation Test 面板运行，全部通过。

**交付物**：自动化测试通过截图

---

### Step 5：性能采样基线（部分依赖 T005）

**配置项**：
- 确认 `stat unit`、`stat fps`、`stat scenerendering` 在编辑器可用
- 确认 `LogVRSanguoPerf` 日志分类可记录帧时间
- 规划性能采样场景模板（空场景基线 + 未来 1v1/4v4 压力场景）

**不实现**：实际性能优化和压力测试（M03/M06 范围）。

**交付物**：性能采样基线配置说明（写入任务报告）

---

### Step 6：测试地图规划（无实现，仅规划）

规划后续里程碑所需的测试场景，不创建实际关卡：

| 场景 | 里程碑 | 内容 |
|------|--------|------|
| 1v1 基线测试场 | M01 | 玩家 + 1 AI + 灰盒竞技场 + 基础武器 |
| 4v4 压力测试场 | M03/M06 | 8 个 AI + 复杂场景 + 性能采样点 |
| 武器训练场 | M02 | 五武器测试区域 + 移动测试区域 + IK 标定区 |

**交付物**：测试场景规划表（写入任务报告）

---

## Deferred 到 M01+（不在 T006 范围）

以下原 T006 交付物依赖战斗系统实现，deferred 到 M01 任务：

| 原 T006 交付项 | Deferred 到 | 原因 |
|----------------|-------------|------|
| 武器命中去重自动化测试 | M01-T001 | 需要战斗结算管线 |
| 格挡和重置自动化测试 | M01-T001 | 需要格挡系统 |
| VR 输入/追踪调试面板 | M01-T004 | 需要实际 VR 输入与 AI 行为 |

---

## 验收清单

| # | 验收项 | 验证方式 |
|---|--------|----------|
| 1 | Win64 Editor 构建通过 | Rebuild.bat 输出 Succeeded |
| 2 | Android Development 构建通过 | BuildCookRun 输出 SUCCESSFUL |
| 3 | 8 个日志分类在 PIE 中可见 | Output Log 截图 |
| 4 | DataAsset 校验测试全部通过 | Automation Test 面板 |
| 5 | 接口与状态机测试全部通过 | Automation Test 面板 |
| 6 | 性能采样基线配置可用 | stat 命令输出截图 |
| 7 | 测试场景规划表完整 | 任务报告审查 |

---

## 完成定义

- [ ] Step 1：构建门禁验证通过
- [ ] Step 2：8 个日志分类运行时可用
- [ ] Step 3：DataAsset 校验测试通过
- [ ] Step 4：接口与流程状态机测试通过
- [ ] Step 5：性能采样基线配置完成
- [ ] Step 6：测试场景规划表完成
- [ ] 代码编译通过（Win64 Development Editor）
- [ ] `STATUS.json` 更新为 `awaiting_review`

---

## 依赖与风险

| 依赖 | 状态 | 说明 |
|------|------|------|
| T005 完成 | ready | T006 Step 2-4 依赖 T005 的接口、DA 基类和流程状态机 |
| Android 构建环境 | ✅ | T004 已验证 APK 构建 |

| 风险 | 概率 | 缓解 |
|------|------|------|
| UE5.6 Automation Test 框架 API 差异 | 低 | 使用标准 IMPLEMENT_SIMPLE_AUTOMATION_TEST 宏 |
| Android 构建门禁耗时过长 | 中 | 可先验证 Win64，Android 门禁异步执行 |

---

## 预估耗时

| 步骤 | 预估 | 累计 |
|------|------|------|
| Step 1：构建门禁 | 0.5h | 0.5h |
| Step 2：日志验证 | 0.5h | 1h |
| Step 3：DataAsset 测试 | 1.5h | 2.5h |
| Step 4：接口与状态机测试 | 2h | 4.5h |
| Step 5：性能基线 | 0.5h | 5h |
| Step 6：场景规划 | 0.5h | 5.5h |
| **合计** | **~5.5h** | |

---

## 报告路径

`.trae/execution/reports/tasks/M00-T006.md`
