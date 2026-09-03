# M02-PREP-002 编辑器自动化工具链迁移：db-lyon/ue-mcp 替换 UEBridgeMCP

- 任务号：M02-PREP-002
- 里程碑：M02（前置准备）
- 优先级：P1
- 预估：1.5h
- 来源：用户 2026-08-31 批准（方案 A）；调研依据 `inboxes/manager/archive/msg-20260831-092156-res-001.md`（RESEARCH-UEMCP）

## 目标

将编辑器自动化工具链从 UEBridgeMCP（GPL-3.0、蓝图图写入崩溃、维护停滞）迁移至 db-lyon/ue-mcp（MIT、UE5.4-5.8、蓝图写+读回闭环、安全护栏），使 AI 能稳定执行蓝图图编辑（写入+读回验证），消除用户手工接线需求。

## 范围

- 允许：安装 db-lyon/ue-mcp 桥插件（`npx ue-mcp init` 或手动部署至 `Plugins/`）、启用插件、编辑器重启、蓝图**测试副本**上的写读验证、退役 UEBridgeMCP（禁用/移除）、治理同步。
- 禁止：修改 M01-T001 白名单内资产（Content/VRSanguo/VR/**、L_SkeletonTest 等）、修改治理锁定文件、在权威蓝图（BP_VRCharacter）上做写图实验（验证一律用测试副本蓝图）。

## 步骤

1. **前置检查**：`node --version` / `npx --version` 可用性；不可用则先按磁盘规则安装 Node 至 D:（安装包 >500MB 放 E:，否则 D:），并如实报告。
2. **关闭编辑器**（与 M01-T001 会话经信箱协调，其当前无编辑器操作）。
3. **部署**：`npx ue-mcp init`（或按 repo README 手动部署 C++ 桥插件），确认 `.uplugin` 与源码落位 `Plugins/`。
4. **编译**：命令行 UBT 全量 Rebuild（编辑器关闭状态），留存真实日志。
5. **验证（测试副本）**：新建测试蓝图 `L_temp` 外的 `/Game/VRSanguo/Dev/Temp_BPForMcpTest`（或临时目录），执行 add_node → connect_pins → compile → query 读回，核对读回内容与写入一致。
6. **退役旧插件**：`.uproject` 移除 UEBridgeMCP 或目录改名 `.disabled`；重启编辑器确认无缺失模块错误。
7. **冒烟**：打开 `L_SkeletonTest`（只读打开即可）确认工程健康。
8. **收尾**：更新 TD-010（迁移决策+结果）、07 登记册、CHANGELOG、任务报告；回执 manager。

## 测试用例

| 编号 | 给定 | 当 | 则 |
|---|---|---|---|
| TC-01 | 编辑器关闭、Node 可用 | 执行部署+UBT Rebuild | Result: Succeeded（真实日志） |
| TC-02 | 测试副本蓝图存在 | add_node→connect_pins→compile→query | 读回内容与写入一致 |
| TC-03 | UEBridgeMCP 已退役 | 重启编辑器 | 无缺失模块错误，工程正常加载 |

## 重试计划（manager 授权 2026-08-31，db-lyon v1.3.0 编译失败 blocked 后）

原认领会话（session-20260831-001）若已结束，新会话重新认领（更新根 STATUS claimedBy）。按序尝试，每个候选同样受停止条件约束（一次失败即换下一个）：

- **2a. db-lyon 兼容版本排查（先做，便宜）**：检查 db-lyon/ue-mcp 的 GitHub releases/tags（npm v1.3.0 之外），寻找声明或迹象支持 UE5.6 的历史版本；找到则 pin 该版本重跑部署+编译。
- **2b. ChiR24/Unreal_mcp（Top2）**：MIT、声明 5.0-5.8、原生 HTTP 传输。部署（注意其 issue #499 类节点创建崩溃——本项目仅用普通函数调用节点与连线，避开源驱动节点）→ UBT Rebuild → 测试副本蓝图写读验证。
- **2c. 全部失败**：保持 blocked，回执 manager 附两份编译日志，交用户裁决（手动接线兜底 / 移植立项）。

注意：ChiR24 的"5.0-5.8 兼容"声明与 db-lyon 案例同样需要编译实证，不得以声明为准判定通过。

## 停止条件

- Node 不可用且无法按磁盘规则安装 → blocked 报告
- 桥插件 UE5.6 编译失败且 1 轮修复无果 → blocked 报告（附日志），不反复蛮试
- 权威资产（BP_VRCharacter 等 M01-T001 资产）出现任何意外修改 → 立即停止报告

## 回退

- 退役 UEBridgeMCP 前保留其目录（改名 .disabled 而非删除）；迁移失败可一键还原 `.uproject` 并改回目录名恢复旧链路。
