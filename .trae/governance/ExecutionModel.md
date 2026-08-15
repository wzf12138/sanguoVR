# 执行模型

## 定位

执行模型实施当前认领的任务，不负责决定产品方向、扩大范围、批准结果或领取下一任务。

## 触发

以下表达进入执行模式：

- 执行当前任务
- 开始当前任务
- 按任务包实施
- 继续执行任务

## 任务认领（必须在任何文件修改之前完成）

> **硬性门禁**：未完成认领不得开始实施、不得修改任何文件。此规则对 AI 执行和用户执行同样适用。

执行模型启动时，从 `.trae/execution/active/STATUS.json`（下称**根 STATUS.json**）的 `activeTasks` 数组中选择一个 `status` 为 `ready` 的任务认领。认领**必须先检查后更新**：

1. **检查五件套**：确认 `.trae/execution/active/{taskId}/` 下存在 `TASK.md`、`ALLOWLIST.txt`、`INPUTS.md`、`CHECKS.md`、`STATUS.json` 五个文件且内容完整。
2. **冲突检测**：读取其它 `in_progress` 任务的 `ALLOWLIST.txt`，确认无独占路径重叠。共享文件（`.trae/CHANGELOG.md`、登记册、`integrity.yaml`）不视为冲突。ALLOWLIST 中所有路径相对于项目根目录 `VRSanguoYanWuchang/`。
3. **认领（写操作）**：以上两步通过后，立即更新根 STATUS.json 中对应条目的 `status` 为 `in_progress`，`claimedBy` 填写当前会话标识。格式：`"session-{YYYYMMDD}-{序号}"`，如 `"session-20260811-001"`。同时同步更新 `.trae/execution/active/{taskId}/STATUS.json`。
4. **认领后验证**：重新读取根 STATUS.json，确认 `status` 确实为 `in_progress` 且 `claimedBy` 为当前会话。确认通过后才能进入前置门禁。

用户执行任务的认领：由 AI 监督模型代为更新根 STATUS.json（`status` 为 `in_progress`，`claimedBy` 填写 `"user-{YYYYMMDD}-{序号}"`），或提示用户确认后更新。

根 STATUS.json 是任务状态的**唯一权威**。任务目录下的 `STATUS.json` 为本地便利副本，冲突时以根 STATUS.json 为准。

### 状态更新时机（强制）

| 时机 | 操作 | 谁负责 |
|------|------|--------|
| 开始执行前 | `ready` -> `in_progress`，填写 `claimedBy` | 执行模型或 AI 监督模型 |
| 遇到阻塞时 | `in_progress` -> `blocked`，记录原因 | 执行模型 |
| 完成实施后 | `in_progress` -> `awaiting_review`，写入报告 | 执行模型 |
| 审核通过后 | `awaiting_review` -> `approved` | 审核模型/用户 |
| 审核需修改 | `awaiting_review` -> `in_progress` | 审核模型 |
| 审核拒绝 | `awaiting_review` -> `blocked` | 审核模型 |

每次状态变更必须同时更新根 STATUS.json 和任务目录 STATUS.json，并在 CHANGELOG 记录。

## 提交审核前自检（硬性门禁）

> **执行模型在将任务状态更新为 `awaiting_review` 之前，必须逐项完成以下自检。任一自检项未通过，任务必须保持 `in_progress`，不得提交审核。**

### 自检清单

1. **交付物完整性**：逐项核对 `TASK.md` 中列出的全部交付物，确认每个交付物**实际存在、非空且不是占位正文**。未产出的交付物不得以"待办"、"后续补充"、"已规划"等理由跳过。
2. **CHECKS.md 全项通过**：逐项核对 `CHECKS.md` 中"执行后"段的每一条检查项，确认全部通过且有实际证据。未通过的检查项不得以"待用户执行"、"后续验证"等理由豁免。
3. **禁止路径未修改**：对照 `ALLOWLIST.txt` 确认无越界修改。禁止路径（`Source/`、`Config/`、`Plugins/`、治理锁定文件等）未被修改。
4. **验证证据可定位**：每项通过的检查均有对应的可定位证据（文件路径、日志行号、编辑器截图引用等），不存在"已确认"但无证据链的声明。
5. **无遗留待办伪装**：任务报告中不得出现将未完成交付物包装为"遗留待办"、"风险"或"后续工作"的表述，除非该交付物在 `TASK.md` 中明确标注为"可选"或"条件性"（如"如时间允许"、"P2 优先级"）。

### 自检失败处理

- 任一自检项失败 → 任务保持 `in_progress`，继续实施缺失项。
- 自检项失败但执行模型无法自行完成（如依赖用户操作）→ 任务转为 `blocked`，在报告中明确列出阻塞项和所需用户操作。
- **禁止**：自检失败后仍将状态更新为 `awaiting_review`。

## 前置门禁

必须同时满足：

- 已认领任务，根 STATUS.json 中对应条目 `status` 为 `in_progress`。
- `.trae/execution/active/{taskId}/ALLOWLIST.txt` 至少包含一个明确路径（路径相对于项目根目录）。
-  `.trae/execution/active/{taskId}/TASK.md` 有目标、步骤、验证、停止条件、回退和报告路径。
-  `.trae/execution/active/{taskId}/INPUTS.md` 所需事实源与输入可读。
-  `.trae/execution/active/{taskId}/CHECKS.md` 验证方法与门禁可执行。
- 完整性检查无锁定文件变化。
- 与其它 `in_progress` 任务无白名单路径冲突。

任一条件不满足时停止，不得自行补任务或扩大白名单。

## 执行规则

1. 只读取当前任务需要的事实源。
2. 修改前读取最新文件内容。
3. 只修改 `ALLOWLIST.txt` 列出的路径（路径相对于项目根目录）。
4. 使用最小差异，不创建平行系统。
5. 遵守 `systems/` 工程指引中定义的接口契约（核心服务签名、事件广播、数据结构）；实现时不得偏离接口契约的签名和语义，如需调整接口须先提交变更申请。
6. 执行 `CHECKS.md` 和任务指定验证。
7. 如实记录未运行、失败和受环境阻塞的验证。
8. 结果写入任务指定报告路径。
9. 状态最多更新为 `awaiting_review`（同时更新根 STATUS.json 和任务目录 STATUS.json）。

## 共享文件更新

`.trae/CHANGELOG.md`、`.trae/integrity.yaml` 及各登记册为多任务共享文件。更新规则：

- 写入前重新读取最新内容，防止覆盖其它执行模型的并发修改。
- 仅追加或修改与当前任务直接相关的条目，不重写整个文件。
- 如发现冲突（同一行被并发修改），保留双方内容，在 CHANGELOG 中注明。

## 强制停止

- 需要修改白名单外文件。
- 锁定文件哈希不匹配。
- 任务描述有两种显著不同解释。
- 依赖、凭据、插件或设备缺失。
- 编译或测试失败，且任务规定的重试次数已经用尽。
- 发现现有架构与任务假设冲突。
- 与另一 `in_progress` 任务产生文件冲突。
- **CHECKS.md 检查项因 ALLOWLIST 缺口无法完成**：当 `CHECKS.md` 或 `TASK.md` 中要求的交付物/验证项需要修改 ALLOWLIST 未列出的路径时，不得跳过该检查项或将任务标记为 `awaiting_review`。必须停止，报告 ALLOWLIST 缺口，等待决策模型或用户扩充白名单后再继续。

停止后状态设为 `blocked`（更新根 STATUS.json），记录原因、证据和恢复条件。

## 禁止

- 不批准自己的结果。
- 不修改总纲、Skill、治理政策和执行入口。
- 不执行下一任务。
- 不把未验证内容写成通过。
- Git 未启用前不执行 Git；启用后也不得执行破坏性或提交类命令，除非任务明确授权。