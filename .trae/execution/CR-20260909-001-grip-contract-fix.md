# CR-20260909-001 · 抓取接口契约修复（快速通道）+ VRE 契约知识入库 + 审核增项 + 死区重验规则

- 关联任务：M01-T001；来源：抓取路径首次真实执行触发崩溃（用户点名治理自查，msg-20260908-235429）
- 裁定：decision 指挥台（2026-09-08 深夜）

## A. 事故记录

输入链修复后（BeginPlay 激活 4 IMC，CR-20260908-001），抓取路径**首次真实执行**立即崩溃：

- 断言：`IVRGripInterface::DenyGripping` 直调 thunk（VRGripInterface.gen.cpp:468）——"Do not directly call Event functions in Interfaces. Call Execute_DenyGripping instead."
- 元凶：`Source/VRSanguoYanWuchang/Private/Combat/VRSanguoGripLibrary.cpp` L34 直调接口事件（全项目 grep 唯一调用点；VRE 插件自身均正确使用 Execute_ 形式）
- 定位链：崩溃日志蓝图栈 + 断言文本 → grep 10 分钟锁定（事故响应链正常）
- 代码归属：待 executor 查会话记录确认（代码含"[TryGrip诊断]"日志，疑为输入诊断期实现），确认后补记本 CR（规则 21 关联）

## B. 修复裁定（快速通道，指挥台技术裁定通过；生效以用户批准为准）

- 变更：L26-34 段替换为 `return !IVRGripInterface::Execute_DenyGripping(Actor, Controller);`——Execute_ 静态转发是 BlueprintNativeEvent 接口事件的标准调用形式，自带 Implements 检查，前置 Cast 一并移除（语义等价性 executor 已核）
- 途径：live_coding 热编译（方法体级改动，约 1 分钟，不重启编辑器）
- 白名单：VRSanguoGripLibrary.h/.cpp 已扩展（ALLOWLIST）
- 验证：用户重测 TC-01（抓剑 + 摇杆移动）

## C. 治理修订（用户批准 2026-09-09；决策模型执笔，非执行模型转写）

三层防线系统性知识缺口（executor 自查采纳）：VRE 插件契约知识未入库 → 实现照猜写、审核无从对照、运行时验证被上游 bug 阻塞成验证债务。经决策侧生命周期覆盖映射（任务设计→实现→审核→验证→验收→维护），最终修订集六项：

| # | 修订 | 落点 |
|---|------|------|
| C-1 | 第三方插件 API 调用形式（审核增项 + 新插件 API 契约回写义务） | ReviewProtocol.md 审核内容 12 |
| C-2 | 死区代码验证债务（债务锚进 TD 登记册/后续任务，任务关闭不消债；上游解除后 grep 路径逐项重验） | ReviewProtocol.md 审核内容 13 |
| C-3 | TC 验证环境钉死（四类环境 + 禁自选/降级 + 结论带环境标签） | ReviewProtocol.md 审核内容 14 |
| C-4 | 后置与阻塞工作登记（登记锚点三选一、禁散文后置、复审触发必填） | ExecutionModel.md 新节"后置与阻塞工作登记（强制）" |
| C-5 | 白名单与交付物对账（审核内容 1 强化：changedPaths vs ALLOWLIST + 白名单缺口=强制停止项） | ReviewProtocol.md 审核内容 1 |
| C-6 | VRExpansionPlugin 接口调用契约（BlueprintNativeEvent → Execute_ 硬规则 + 违例/范例案例） | systems/02-interaction-and-weapon-system.md 新节 |

全部为现有规则（AGENTS.md 6/12/13/15/22）的操作化，不改动 AGENTS.md 正文。以上 C-1~C-6 已由决策模型于 2026-09-09 直接落笔完成。

## D. 登记册事故：截断型写入器破坏根 STATUS.json（2026-09-10，decision 指挥台修复并留痕）

- 现象：根 `.trae/execution/active/STATUS.json` 自 2026-09-10 18:15 起不可解析（22,331 字节），`dashboard/check-integrity.py` 读取它的 6 处校验（L248 / L273 / L306 / L353 / L461 / L599）全部失败，治理一致性校验整体不可用。
- 根因（实证）：M01-T005 的 note 被"2000 字符上限"的截断型写入器改写。原文 `（用户反馈"朝向杂乱/不是扁旗"）` 被压成 `（用户反馈朝向杂乱/不是扁旗"）`——**第一个内层开引号被吃掉、行尾多出的那个引号提前闭合了 JSON 字符串**，其后 9,534 字符沦为裸文本。
- 同源第二处：M01-T001 的 note 有 5 个非法反斜杠转义（Windows 路径 `D:\AGame\Steam\...`、`steamapps\common\SteamVR\` 未转义），同一写入器所致；该 note 亦被截断写入。
- 修复（decision 执行）：可读前缀原样保留；断掉的尾部按信箱已归档回执原文（msg-20260910-164121 / msg-20260910-173231）补回；未重写历史正文、未编造内容。产出 25,113 字节，JSON 可解析，7 个 active 任务齐全（M00-T004/T005/T006、M01-T001 `in_progress`、M01-T005 `completed`、M02-PREP-001/002 `approved`）。
- 备份：破损原件 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\tmp\STATUS.json.broken-20260910`（项目外，符合文件边界）。修复器 `repair_status_json5.js` 同目录。
- 写入合规：M01-T001 与 M01-T005 的 ALLOWLIST.txt 均列有 `.trae/execution/active/STATUS.json`（规则 20 路径门禁满足）。

### D-1 机制红线（立即生效，全模型适用）

**禁止任何"读取截断 → 回写"的写入路径。** 处理 STATUS.json 等含大字段的文件时：

1. 一次写入必须**整文件写入**，内容不得被单次字符上限截断；写入前先自检目标字符串长度是否与预期一致。
2. 写入后**立即用 JSON.parse 回读校验**；解析失败即视为写入失败，恢复备份并报告，不得让破损文件留在原地。
3. 登记册类文件冻结期间不得写入；解冻需由 decision 广播。

**事故计数：同类机制已造成两次数据损坏**（第一次 M01-T005 note、第二次 M01-T001 note），第二次即本次。此为既有规则 18（最小差异、修改前先读）与"禁止虚构"（1）在文件写入路径上的操作化，不改动 AGENTS.md 正文。

## E. 教训入库：Live Coding 补丁不跨进程存活（2026-09-09 实证，2026-09-10 登记）

- 事实：本 CR B 节的重编译途径（`live_coding` 热编译）只把方法体补丁写进**当前编辑器进程的内存**。进程退出后补丁消失；**只有 UBT 完整编译并写入二进制（`Binaries/`）的改动才跨进程存活**。
- 实证：同源崩溃在进程重启后复现，追溯确认 live_coding 结果未落二进制；改走 UBT 完整编译后症状消除。
- 操作规则（执行模型适用）：
  1. 任何"修好并验证通过"的 C++ 改动，交付前必须确认**它是怎么进二进制的**，并在交接/回执中写明"已 UBT 完整编译"或"仅 live_coding（进程内存态，重启即失效）"。
  2. 只做了 live_coding 的改动，一律标记为**未持久化**，不得计入已完成；须补 UBT 编译后再验证。
  3. 交接快照/会话记录必须区分这两类改动（与 D-1 的"回读校验"同一纪律层级）。
- 落点：`knowledge/TechnicalDecisions.md`（"Live Coding 补丁与二进制"节）+ 本 CR。

## 状态

- A：已记录；代码归属待那个正在调整 M01-T001 的 DSH 会话汇报后补认。
- B：修复方案已批准并落地（UBT 完整编译进二进制）；用户重测状态等该会话汇报。
- C：**已完成（2026-09-09 决策侧落笔）**：ReviewProtocol（第 1 条强化 + 新增 12/13/14 条）、ExecutionModel（新节）、systems/02（新节）。
- D：**已修复（2026-09-10 决策侧）**：根 STATUS.json 恢复可解析；D-1 机制红线立此生效。
- E：**已入库（2026-09-10 决策侧）**：Live Coding 不跨进程存活，落点 TechnicalDecisions + 本 CR。