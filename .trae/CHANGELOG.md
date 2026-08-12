# ChangeLog

## 2026-08-12（M00-T004：输入映射按 PICO 官方文档绑定完成）

- 编辑器内配置（用户执行，AI 核验）：
  - 5 个 IMC 全部按 PICO 官方文档（developer.picoxr.com Input mappings）绑定 PICO Neo3 键：IMC_Default（Move/Turn/Grab_L/R/Menu_Toggle）、IMC_Hands（Grasp/IndexCurl/Point/ThumbUp 共 10 键）、IMC_Menu（Interact Trigger + Cursor Thumbstick 2D）、IMC_Weapon_Left/Right（Shoot Trigger Axis）。
  - 插件按键命名确认：`PICONeo3_*`（显示名 "PICO Neo3 Controller" 分类），非官方文档中的 "PICO Touch" 命名。
  - 二进制核验：5 个 IMC 资产均已包含对应 `PICONeo3_*` 键（IMC_Default 6 键、IMC_Hands 10 键、IMC_Menu 4 键、Weapon×2 各 1 键）。
- 任务状态同步：STATUS.json（updatedAt 2026-08-12，note 更新）、07-task-register.md、11-tech-debt-register.md（TD-007 部分偿还标注）。
- 遗留（下次会话继续）：VRPawn 挂载 Neo3 手柄模型（需在 Motion Controller 下新增 StaticMesh 组件挂 `SM_PICONeo3_L/R`，隐藏原 SkeletalMesh 手部）、OpenXR Input PlayerMappableInputConfig 配置、真机复测输入。

## 2026-08-11（M00-T004 UE5.6 迁移执行：swapchain 补丁生效，真机场景可见）

用户决策并批准执行 UE5.6 + PICO OpenXR Plugin（OS 5）降级路线（替代 UE5.8），任务状态从 `blocked` 恢复为 `in_progress`。

**工程执行（项目外治理文档同步）：**

- 项目已基于 UE5.6 官方 VR 模板重建（`Content/VRTemplate`、`Characters/MannequinsXR`、`LevelPrototyping`、`Weapons`；`Config/` 重配；`Source/VRSanguoYanWuchang`）。
- PICO OpenXR Plugin v1.6.1 从引擎 Marketplace 迁移至项目 `Plugins/`（源码编译），11 个模块 Build.cs 加 `PrecompileForTargets=Any`、uplugin `Installed=false`；引擎原插件改名 `.disabled`。
- **swapchain 补丁**：`PICO_HMD.cpp` 拦截 `xrCreateSwapchain` 剥离 `XR_KHR_vulkan_swapchain_format_list`（Neo3 运行时 ION ENOTTY 崩溃）；符号 `PICOLayerCreateSwapchain` 已确认编译进 libUnreal.so；Neo3 真机场景可见（V-008）。
- 修复 `Config/DefaultInput.ini`：IMC 路径从不存在的 `/Game/XRFramework/Input/` 改为 `/Game/VRTemplate/Input/`（v3 日志确认 IMC 加载成功）。
- 补丁包落位：swapchain 补丁备份与恢复脚本迁移至项目内 `Build/Patches/PICOOpenXR/`（随 git 提交，避免项目外临时目录丢失）。
- 构建系统坑已解决并记录：引擎 BuildRules 误删恢复（Epic Launcher 验证/修复）、插件增量构建盲区（迁移项目 Plugins）、规则 DLL 缓存清理、源码时间戳强制重编。

**治理文档同步：**

- `execution/active/STATUS.json`：M00-T004 `blocked` → `in_progress`（claimedBy session-20260811-execution）。
- `registers/07-task-register.md`：M00-T004 状态与交付物同步。
- `registers/09-verification-register.md`：V-005 标注 UE5.8 路线；新增 V-008（UE5.6 真机部分验证）。
- `knowledge/TechnicalDecisions.md`：追加「UE5.6 迁移执行与 swapchain 补丁」。
- `knowledge/PicoNeo3BuildGuide.md`：构建环境切 UE5.6、新增 8 项已知构建坑、插件迁移说明、真机结论与待办。
- `knowledge/DeviceConfigurationMatrix.md`：更新 UE5.6 配置基线；UE5.8 兼容配置降为历史参考。
- `vr/PicoValidationMatrix.md`：回填 Android 构建通过、真机部分通过。
- `registers/11-tech-debt-register.md`：新增 TD-005~TD-009。
- `registers/02-risk-register.md`：新增 RSK-018~RSK-020。

**遗留（待用户编辑器操作）：** IMC 绑定 PICO Touch 按键、OpenXR Input PlayerMappableInputConfig、VRPawn 挂载 Neo3 手柄模型（SM_PICONeo3_L/R）。

## 2026-08-11（架构审核修复）

用户批准：对全部架构进行完整审核后，修复发现的 10 项问题。

**修复中级别问题（4 项）：**

- `governance/policy.md`：第 6 节新增"审核结论与任务状态映射"，将 `requires_changes`→`in_progress`、`rejected`→`blocked` 显式定义。
- `execution/README.md`：新增"任务包目录结构"段落，文档化五件套（TASK.md + ALLOWLIST.txt + INPUTS.md + CHECKS.md + STATUS.json）结构。
- `execution/task-template.md`：从 10 行扁平字段升级为 9 章结构化模板，含验收标准 checkbox、白名单代码块、禁止路径列表、验证方法 checkbox、停止条件、用户确认流程，与资产/关卡模板结构一致。
- `registers/07-task-register.md`：T004 状态描述从"引擎已降级"修正为"降级路线已建议待执行"，与 TD-001(open)、V-005(待决策)、CHECKS.md(需用户先决策) 一致。

**修复中级别问题（2 项）：**

- `vr/index.md`：补充 `PicoValidationMatrix.md` 索引条目（文件已存在但未纳入索引）。
- `standards/05-event-and-interface-standard.md`：新增 C++ 接口声明代码示例，覆盖全部 6 个核心接口（IInteractable/IWeaponSource/IDamageable/IDefenseProvider/IMovementMode/IBattleParticipant）。

**修复低级别问题（4 项）：**

- `governance/DecisionModel.md`：必读列表第 1 项补充 `.trae/index.md`，与 SKILL.md 必读顺序一致。
- `governance/SessionCommands.md`：技术债登记册引用从裸文件名改为完整相对路径 markdown 链接。
- `knowledge/TechnicalDecisions.md`：基础模板和 XR 基础从 UE5.8 修正为 UE5.6，消除版本引用矛盾。
- `execution/active/STATUS.json` + `execution/active/M00-T004/STATUS.json`：T004 阻塞描述从"PICO 真机模拟卡住"修正为"PICO Neo3 与 UE5.8 运行时不兼容，等待用户决策降级引擎或更换设备"。

**未修复（已有 backlog 跟踪）：**

- P-003：`06-performance-standard.md` 缺具体数值目标——standards-backlog.md M06 P1 已跟踪。
- P-005：无独立代码组织标准——standards-backlog.md M00 P0 已跟踪。

**元数据同步：**

- `integrity.yaml`：`local_markdown_links` 更新为 115。

## 2026-08-11（archcore 方法论评估与架构改进）

用户批准：以 archcore 插件方法论为参照，评估项目架构并实施改进，目标是更好地支持游戏开发。分两轮完成，架构一次性到位。

### 第一轮：文档完整性与治理工具补全

**新增文件（1 个）：**

- `registers/11-tech-debt-register.md`：技术债登记册，追踪临时实现、占位方案和已知缺陷，含债务管理规则。

**更新文件（12 个）：**

- `registers/01-decision-register.md`：新增"关键决策 ADR 上下文"段落，为 DEC-003/005/006/010/011/013 六条架构级决策补充上下文、备选方案、后果和复审条件。
- `systems/01-game-flow-system.md`～`07-save-telemetry-and-diagnostics-system.md`：7 份系统指引统一新增"接口契约（规划级）"段落，定义核心服务签名、事件广播、数据结构和依赖接口。
- `governance/ReviewProtocol.md`：审核内容新增第 8 项"文档同步验证（漂移检测）"和第 9 项"技术债检查"。
- `registers/04-requirement-traceability-register.md`：需求追踪表新增"覆盖状态"列（当前全部为"规划"）。
- `governance/definition-of-done.md`：治理同步条款新增"技术债登记册"。
- `registers/index.md`：新增 `11-tech-debt-register.md` 条目。
- `manifest.yaml`：`registers_core` 更新为 11。
- `integrity.yaml`：新增 `tech_debt_register` 检查项，更新链接计数和说明。

### 第二轮：治理模型同步与模式库骨架

**新增文件（1 个）：**

- `knowledge/Patterns/README.md`：实现模式库骨架，含模式格式、8 个预设类别（战斗结算/武器交互/VR 移动/全身 IK/AI 战斗/竞技场流程/数据驱动/性能优化）和添加规则。

**更新治理模型文件（5 个）：**

- `governance/DecisionModel.md`：必读列表新增技术债登记册和 systems 接口契约（实现约束）。
- `governance/ExecutionModel.md`：执行规则新增第 5 条——遵守 systems/ 接口契约的签名和语义，如需调整须先提交变更申请。
- `governance/SessionCommands.md`：决策段新增"登记技术债"短指令。
- `governance/responsibility-matrix.md`：RACI 矩阵新增"技术债追踪与偿还规划"行。
- `skills/three-kingdoms-vr-arena/SKILL.md`：必读顺序新增 Patterns 模式库、接口契约和技术债登记册标注。

**更新索引文件（3 个）：**

- `knowledge/README.md`：新增 Patterns/ 实现模式库链接。
- `index.md`：产品与工程入口新增 Patterns 链接。
- `systems/index.md`：新增"接口契约"段落，明确接口契约为实现的强制约束。

**更新标准文件（3 个）：**

- `standards/02-naming-and-path-standard.md`：新增五武器、兵种、C++ 类与内容路径的实现示例。
- `standards/03-blueprint-cpp-boundary-standard.md`：新增蓝图调用 C++、事件广播、DataAsset 消费和反模式的实现示例。
- `standards/04-data-asset-standard.md`：新增 Schema 版本字段、DataAsset 迁移、保存数据版本化和版本登记规则。

**元数据同步：**

- `manifest.yaml`：`collections` 新增 `pattern_library: 1`。
- `integrity.yaml`：新增 `pattern_library` 检查项；`local_markdown_links` 更新为 113。

## 2026-08-11（Vibecoding 架构补全）

用户批准：为支持美术、开发、动画、关卡等领域的 Vibecoding 并行工作流，补全资产生产治理体系。

**新增文件（6 个）：**

- `execution/task-template-asset.md`：资产任务模板（模型、骨骼、动画、材质、音效、特效、UI 等），含视觉验收流程。
- `execution/task-template-level.md`：关卡任务模板（灰盒/正式场景、NavMesh、光照、性能），含 UE 内加载验证流程。
- `registers/10-asset-register.md`：资产登记册，追踪所有 Content 资产的状态、路径与依赖，防止并发冲突。
- `knowledge/Production/ArtStyleGuide.md`：美术风格指南（色彩体系、材质语言、角色甲胄、场景类型、武器形制）。
- `knowledge/Production/AnimationSpec.md`：动画规范（骨架、动画列表、全身 IK 兼容、战斗时机参考、技术规范）。
- `knowledge/Production/LevelDesignSpec.md`：关卡设计规范（布局指标、VR 舒适度、NavMesh、性能预算、灰盒规范）。

**更新文件（6 个）：**

- `governance/ReviewProtocol.md` §4：区分代码回读验证、UE 编辑器视觉验证、关卡加载验证。
- `governance/definition-of-done.md` §3：补充资产任务和关卡任务的验收证据要求。
- `registers/03-dependency-register.md`：新增资产级依赖链（M01 骨架→动画→武器→DataAsset 链路）与并发安全规则。
- `skills/three-kingdoms-vr-arena/SKILL.md`：必读顺序补充 `knowledge/Production/` 生产规格。
- `index.md`：Execution 基线补充资产/关卡任务模板链接。
- `execution/README.md`、`knowledge/Production/README.md`、`registers/index.md`：索引同步新增文件。

**元数据同步：**

- `manifest.yaml`：`collections` 新增 `task_templates: 3`、`production_specs: 6`；`registers_core` 更新为 10。
- `integrity.yaml`：新增 `task_templates`、`production_specs`、`asset_register` 三项检查。

**核心治理文件零改动**：`policy.md`、`ExecutionModel.md`、`DecisionModel.md`、`SessionCommands.md`、`change-request-template.md`、`responsibility-matrix.md`、`project_rules.md` 均未修改。

## 2026-08-11（冗余文件实际清理）

上轮 CHANGELOG 声称删除但实际未落盘的三份文件，本次完成实际删除：

- 删除 `rules/README.md`（纯重定向，3 行，无引用）。
- 删除 `execution/reports/tasks/M00-T006.md`（4 行记号级报告，内容已被登记册覆盖）。
- 删除 `execution/requests/README.md`（空目录说明，目录内无实际变更请求文件）。
- 更新 `index.md`：`requests/README.md` 链接改为 `governance/change-request-template.md`。
- 更新 `execution/README.md`：同上。
- 更新 `09-verification-register.md` V-001 证据列：移除对已删除报告文件的引用，改为引用实际验证的治理文件与报告索引。

## 2026-08-11（多任务并发治理）

- 用户批准：治理模型从单任务改为多任务并发，每个执行模型认领一个任务。
- `policy.md` §6：从"单任务与状态"改为"多任务与状态"，移除"任一时刻最多一个 in_progress"约束，新增任务认领、文件冲突检测与共享文件协调规则。
- `ExecutionModel.md`：新增"任务认领"章节，前置门禁增加冲突检测，强制停止条件增加文件冲突。
- `SKILL.md`：active 门禁路径从单任务改为多任务（`active/{taskId}/` 子目录结构），新增"并发安全"小节。
- `active/` 目录重构：T004 文件移入 `active/M00-T004/`，新建 `active/M00-T005/` 任务包。
- `active/STATUS.json`：从单任务对象改为 `activeTasks` 数组，支持多任务状态追踪。
- M00-T004 状态：`in_progress` → `blocked`（PICO 真机模拟卡住）。
- M00-T005 状态：`已批准` → `ready`（T004 阻塞期间并发启动）。
- 全盘审计修复（同日期）：`index.md` 断链修复（active/ 旧路径 → 子目录结构）；`manifest.yaml` 与 `integrity.yaml` 更新多任务结构与统计；`DecisionModel.md` 移除单任务约束；`execution/README.md` 断链修复；`M00/README.md` 状态表同步；T003/T005/T006 里程碑详规硬编码状态改为引用 STATUS.json；`SessionCommands.md` 去"唯一"措辞；`T005-SystemSkeleton.md` 前置任务与依赖表更新为阻塞/并发状态。
- 执行模型歧义消除（同日期）：`ExecutionModel.md` 重写，补全 `.trae/execution/` 前缀路径、定义 `claimedBy` 格式（`"session-{YYYYMMDD}-{序号}"`）、认领流程改为先检查后更新、新增共享文件更新时序；`SKILL.md` 门禁路径补全前缀、明确根 STATUS.json 为唯一权威；`policy.md` §5 修正"一个活动任务"为"一个认领的任务"；ALLOWLIST.txt 添加路径基准说明；任务目录 STATUS.json 添加便利副本标注。

## 2026-08-10（防废弃文件加固）

- 用户确认三处加固，防止后续 AI 会话产生新的废弃文件：
- `rules/project_rules.md` 新增创建约束：创建/修改 `.trae/` 文件前必须确认路径属于 active 白名单、任务报告/登记册路径或用户本次明确批准的变更；白名单为空的决策/规划期同样适用，规划输出只写入任务草案或变更申请。
- `skills/three-kingdoms-vr-arena/SKILL.md` 新增「写前校验」：涉及 `.trae/` 写操作时先核对 `integrity.yaml`/`manifest.yaml` 与实际文件一致性，不一致时报告异常并停止，不自行补建。
- `governance/SessionCommands.md` 的「检查项目状态」加入一致性核对（新增文件、重复命名、断链、索引与登记册同步），不一致列为异常报告。

## 2026-08-10（任务报告要求固化）

- 用户确认在 `execution/task-template.md` 新增「报告要求」章节：任务报告必须包含结果、验证状态（已验证/已实现未验证/验证失败）、证据（引用 `09-verification-register.md` 对应 V-ID 与知识库证据路径）、偏差与变更清单；禁止无证据总结，真机验证不得以静态检查替代。
- 目的：防止再次产生"4 行记号级"无意义报告（如本次删除的 M00-T001/T002/T004/T005/T006 报告）。

## 2026-08-10（报告清理与空目录删除）

- 用户确认删除 5 个记号级任务报告（`reports/tasks/M00-T001.md`、`M00-T002.md`、`M00-T004.md`、`M00-T005.md`、`M00-T006.md`）：内容仅 4 行"完成 xx 文档"，与任务本体（T005 系统骨架、T006 自动化门禁）不符或信息已被 `07-task-register.md`、`09-verification-register.md` 覆盖；T004 正式报告将在任务执行时重新生成。
- 删除废弃的 `.trae/tasks/` 空目录（含 `active/M00`，旧第二套任务体系残留，git 已无跟踪文件）。
- 更新 `reports/tasks/README.md` 索引：仅保留 M00-T003、M00-T004-structure-integrity、M00-DOC-001 报告链接，并注明删除原因。
- 保留：`execution/active/TASK.md`、`CHECKS.md`、`M00/T005-SystemSkeleton.md` 中的报告路径引用（指向未来执行时写入位置，非已删文件）。

## 2026-08-10（Git 状态语句清理）

- 清理过时的"Git 未安装/不执行"表述（Git 已于 2026-08-09 安装并推送远程）：`execution/reports/tasks/README.md` 更新说明；`execution/M00/T003-UE58ToolchainBaseline.md` 步骤中 Git 约束改为"已由 M00-T002 安装启用"；`registers/02-risk-register.md` RSK-011 标记为已缓解（差异与回滚可用 `git diff`/`git restore`）。
- 历史审计记录（CHANGELOG 历史条目、`M00-DOC-001.md` 报告）保留原文不改。

## 2026-08-10（状态单一事实源治理优化）

- 用户确认全局优化"状态多处复制"问题：动态任务状态改为只由 `execution/active/STATUS.json` 唯一声明，其他文件一律链接、不复制状态值。
- 变更：`.trae/README.md`、`.trae/index.md` 的"当前执行状态"段落改为指向 `STATUS.json`；`execution/active/TASK.md`、`execution/M00/T004-VROpenXRPicoBaseline.md` 头部状态字段改为引用 `STATUS.json`；`manifest.yaml`、`integrity.yaml` 的 `active_gate.status` 改为 `status_source` 引用；`CHECKS.md` 状态描述改为以 `STATUS.json` 为准。
- 保留：`STATUS.json`（唯一权威）、`registers/07-task-register.md`（任务登记册，按职责登记各任务状态，非复制）。
- 说明双任务定义成因：`execution/M00/T004-*.md`（里程碑正式详规）与 `execution/active/TASK.md`（活动任务包五件套之一）为历史双轨规划遗留，职责不同（档案 vs 执行包），本次仅去除其重复的动态状态字段，不合并文件本体。

## 2026-08-10（决策模型复核修正）

- 命名规范修正：`AVRSanguoBootstrapComponent`（继承 `AActor`）按 UE 规范更名为 `AVRSanguoBootstrapActor`，文件同步改为 `VRSanguoBootstrapActor.h/.cpp`；删除模板残留 `MyClass.h/.cpp`；`EnvironmentSetup.md`、`M00-T003.md` 中相关描述同步更新。
- 任务状态修正：M00-T004 实际已推进到 APK 构建成功、PICO Neo3 真机验证失败（V-005 设备不兼容），但 STATUS/登记仍停留在"Android SDK 准备"。已按真实进度将 `STATUS.json`、`07-task-register.md`、`manifest.yaml`、`integrity.yaml`、`.trae/README.md`、`.trae/index.md`、`TASK.md` 统一更新为 `blocked`（待用户决策换设备或降级引擎）。
- 源码改动未重新编译验证，标记为"已实现未验证"；UE 编辑器/编译验证需用户或后续任务执行。

## 2026-08-10（发布前修正）

- 发布前审核修正（用户确认）：同步 `.trae/README.md`、`.trae/index.md` 任务状态为 `M00-T004 / ready`（原仍写 blocked，与 STATUS.json 矛盾）；`integrity.yaml` 的 git 限制更新为已安装已推送；`governance/README.md` 与 `execution/README.md` 同步 Git 实施状态；`DecisionModel.md` 引用从已删除的 `governance/manifest.json` 改为 `.trae/manifest.yaml`。
- 遗留清理：删除根级 `Set-TraeGovernanceAcl.ps1`（已复制到项目外 `D:\AWork\TraeAdmin\VRSanguoYanWuchang\`）与 `AdminScriptDeployment.txt`；删除根级旧 `Design/` 目录（5 个废弃详规）；删除 `governance/` 旧驼峰命名文件（GovernancePolicy/ChangeControl/DefinitionOfDone/ResponsibilityMatrix）与旧 `manifest.json`。
- 冗余路由清理（用户要求不留已废弃占位）：删除 standards/vr/systems/registers 下全部旧命名重复文件（S0x、VR0x、SYS0x、驼峰命名、小写命名）与旧 register 文件，权威仅保留各目录编号正文与 `index.md`。
- 任务体系清理：删除 `execution/milestones/` 旧任务目录（6 个文件）、`execution/active/` 下 10 个 0 字节空文件与 `M00/` 空目录、`.trae/tasks/` 旧任务体系（5 个文件）；删除 `archive/LegacyDocs.md`、`archive/LegacyRoot.md`（旧树说明已并入 `archive/README.md`）。
- 更新 `execution/M00/T002-GitRepositoryBaseline.md`：交付项引用改为 `standards/10-git-standard.md`，状态更新为已实施（Git 已装、仓库已推）。
- 经 grep 复核：被删文件名在当前保留正文中无残留引用；唯一 Skill、四份治理契约、四份操作模型、Design 详规与编号标准入口保持完整。

## 2026-08-09

- 用户确认解除冻结；结构核验通过后将 M00-T004、manifest、integrity 和任务登记恢复为 `ready`。后续可由执行模型继续 Android SDK/UE Android 配置、PICO 部署与 Standalone APK 验证。
- 重新生成 M00-T004 结构完整性结论：active 五件套、唯一任务入口、M00 正式任务目录、唯一 Skill 和规则唯一入口均通过；结构条件满足恢复 `M00-T004 / ready`，但本次不直接变更状态，等待用户确认解除冻结。
- 完成 M00-T004 最后一次结构核验并生成 `execution/reports/tasks/M00-T004-structure-integrity.md`。active 五件套可读取、当前任务与状态快照统一为 `M00-T004 / blocked`、旧 active 任务引用未发现、唯一 Skill 为 1；由于完整性快照仍有历史限制，任务暂不恢复 `ready`。
- 最小治理修复：确认 active 五件套完整；删除请求中的两个空任务壳因删除接口路径异常未执行，保留待后续人工清理；修正唯一 Skill 的 active 门禁，不再要求 `active/<taskId>.md`；清理 execution 索引中的旧 active 任务链接；将旧 manifest 路径改为 `execution/M00`、`execution/reports` 和 `execution/requests`；任务继续保持 `M00-T004 / blocked`。
- 冻结 M00-T004：将 active 状态、任务登记、manifest 与 integrity 统一为 `M00-T004 / blocked`。冻结期间禁止执行模型进行 SDK 安装、APK 构建或 PICO 真机操作；先完成治理入口只读清点。
- 按用户确认移除根级 `rules.md` 兼容入口依赖，统一当前入口指向 `rules/project_rules.md`；更新 index、README、manifest、rules README、DirectoryConvention、T001 任务和唯一 Skill。
- 清理 execution/active/ 下 10 个非标旧任务文件（M00-T001~T006 自定义子弹格式 + M00/ 子目录五文件），与 execution/M00/T00X-*.md 正式详规形成三重任务定义。文件已清空，需用户手动删除空文件和 M00/ 空目录。
- 全面重写 M00-T004 任务包：7 个 Phase，每步含"为什么/做什么/怎么做/谁做/怎么算做完"。按 UE5.8 官方文档锁定 NDK r27c + build-tools 35.0.1 + JDK 21。重写全部 active 五件套。STATUS 重置为 `ready`。
- 执行 M00-T004 VR/OpenXR/PICO 基线（Step 1-3），状态曾置为 `in_progress`：Step 1-3 通过（VR 模板资产、插件与平台声明、OpenXR 运行时 `xrCreateInstance succeeded`）；`PicoValidationMatrix.md` 更新文件/编辑器列，修复其指向 `VerificationRegister.md` 的旧引用为 `09-verification-register.md`；V-004 更新为已验证（编辑器）。
- 发现并记录偏差：UE5.8 官方要求 NDK r27c（`27.2.12479018`，见引擎 `Android_SDK.json`）与 SDK 推荐 35，任务 Step 0 原写 NDK r25b 为 UE5.4 旧要求；机器无独立 JDK（仅 Android Studio JDK 11），APK 构建前需安装 Temurin JDK 17；`EnvironmentSetup.md` 已补录 Android 环境检查结论。
- Android 构建链路打通：安装 Temurin JDK 21（`D:\AWork\Android_SDK\jdk-21.0.12+8`）、SDK platforms 34/35、build-tools 35.0.1、NDK r27c 27.2.12479018（全部真实落盘并验证）；经 MCP 修正项目 PICO 打包配置（`bPackageForMetaQuest=False`、`bPackageDataInsideApk=True`、`MinSDKVersion=26`、`TargetSDKVersion=35`、`NDKAPILevelOverride=android-26`）；Gradle 8.7 发行版以国内镜像下载并预置 wrapper 缓存（`D:\AWork\.gradle`）；`BuildCookRun -package` 构建 **BUILD SUCCESSFUL**（350s，arm64 APK，包名 com.YourCompany.VRSanguoYanWuchang）；验证矩阵 Android 构建列更新为通过，V-005 部分验证。待办：PICO Neo3 真机安装与 6DoF/双控制器验证。
- 深夜真机调试（M00-T004）：经无线 adb 全程自主调试（PICO 无线连接、UE 日志文件定位、三轮配置修复：ASIS 禁用 Swappy / 关闭 MobileMultiView 修复 framebuffer / 附加 manifest 修复 OpenXR 启用）；OpenXR 运行时加载成功但 `xrCreateSession` 被拒，PICO 日志确认根因 `Failed to make EGL context current / create egl client compositor`（Neo3 运行时 3.0.1 过老）；V-005 最终判定：UE5.8 与 PICO Neo3 不兼容（设备层硬限制），工程配置对 PICO 4+ 可直接运行；M00-T002 已实施（用户完成 Git 安装/初始化/推送）。
- 知识库维护（2026-08-09 深夜）：新增 `knowledge/DeviceConfigurationMatrix.md`（设备配置矩阵与新设备改回清单）；重写 `PicoNeo3BuildGuide.md`（构建/部署/调试全流程）；更新 `EnvironmentSetup.md`、`index.md`、`knowledge/README.md` 索引；删除无用的 Spatial SDK 6.0 语料（`knowledge/pico-sdk/`）；经 PICO 官网 UE 说明书确认官方插件支持矩阵（PICOOpenXR 仅 UE 5.6/5.7 + Vulkan + PICO OS 6 设备，UE5.8 不在官方矩阵），已提炼写入 `PicoNeo3BuildGuide.md`。
- **认知修正**（2026-08-10）：此前混淆了 PICO OpenXR Plugin **OS 6 版**（仅支持 Project Swan 新设备）与 **OS 5 版**（官方支持 Neo3/PICO 4/PICO 4 Ultra）。OS 5 版本要求：UE 5.6/5.7 + Vulkan + 设备系统 ≥ 5.13.0；已修正 `PicoNeo3BuildGuide.md`。路线明确：UE 5.6 + PICO OpenXR Plugin（OS 5）= Neo3 官方组合。

## 2026-08-09（M00-T003）

- 决策模型生成 M00-T004 活动任务包：含用户操作清单（sdkmanager 补齐 android-34 + NDK r25b、APK 构建、PICO 安装命令）和 AI 执行范围（编辑器 VR 模板核对 + Android 环境检查 + 验证登记）。STATUS 置为 `ready`。用户建议在执行前并行运行 Step 0 命令。
- 执行 M00-T003 UE5.8 工程与工具链基线：工具链检查（UE5.8 引擎路径、VS2026/MSVC、Windows SDK、UBT/RunUAT）、`.uproject` 六插件与 Android 平台核对、MCP `list_toolsets` 与编辑器日志验证均完成；用户本机 `Rebuild.bat` 清理编译 `Result: Succeeded`（33.35s），UBT 实际选用 MSVC 14.50.35717 + Windows SDK 10.0.22621.0；编辑器启动验证通过，任务置为 `awaiting_review`。
- 更新 `EnvironmentSetup.md`（工具链实际选择与编译结果）、`TechnicalDecisions.md`（MCP 连接器验证）、`09-verification-register.md`（V-003 已验证）；遗留项：编辑器重启后 MCP 桥接返回空工具集待用户确认，vswhere 识别 VS2026 待注册信息落盘。
- 用户验收通过，M00-T003 置为 `approved` 并归档：MCP 桥接重启后已恢复（list_toolsets 40 工具集）；vswhere 手工注册实例键不被识别（VS2026 非安装器注册的固有表现，不影响构建，正解为安装器修复，超出任务范围）已如实记录于 `EnvironmentSetup.md`。

## 2026-08-09（M00-DOC-001）

- 用户验收 M00-DOC-001 为 `approved`；15 个旧文件已手动删除，合并、断链与 Skill 数量复核完成。
- 决策模型生成 M00-T003 活动任务包（UE5.8 工程与工具链基线）：重写 active 五件套，白名单含 `Intermediate/**`、`Binaries/**`、`.sln` 和 9 个 `.trae/` 可写路径；STATUS 置为 `ready`，等待执行模型激活。
- 执行 M00-DOC-001 治理文档最终收口：Standards、VR、Systems 与 Registers 的重复命名与独有内容合并到编号权威链，状态置为 `awaiting_review`，待删除文件清单等待用户手动删除。
- `systems/index.md` 吸收 `SystemCatalog.md`（系统总览）、`ModuleBoundaries.md`（模块依赖边界）、`DataAssetCatalog.md`（数据资产目录）独有内容；`07-save-telemetry-and-diagnostics-system.md` 吸收 `Diagnostics.md` 的日志分类与最小诊断能力。
- `01-decision-register.md` 新增 DEC-009—DEC-013（`.trae` 唯一根、UE5.8 模板/OpenXR/PICO Neo3、统一角色能力接口、ACL 脚本位置、Git LFS），记录 ADR-001/ADR-2026-00X 旧编号映射。
- `02-risk-register.md` 新增 RSK-012—RSK-017（PICO 兼容、模板合并冲突、LFS、ACL 未应用、缺真机验证、项目外 `.trae` 误写），记录旧 R 系列映射；`03-dependency-register.md` 新增 DEP-009（Git 依赖）。
- 新增编号登记册 `07-task-register.md`、`08-permission-register.md`、`09-verification-register.md`，分别吸收 TaskRegister、PermissionRegister、VerificationRegister 与 verification-register 的独有内容并解决 V 系列 ID 冲突；`registers/index.md` 同步更新。
- 新增 `standards/10-git-standard.md` 作为 Git 标准正式入口，吸收并统一 `git-standard.md` 与 `GitStandard.md` 内容（含 Git 未安装未执行状态声明）；`standards/index.md` 同步更新。
- 同步 `manifest.yaml`、`integrity.yaml`、任务登记与 active 状态；旧文件未删除前保留原文，由用户按删除清单手动删除后复核断链。
- 用户已按删除清单手动删除 15 个旧文件；执行模型完成删除后复核：目录数量与 `index.md` 对照一致，本地链接与新增引用无断链，`integrity.yaml` 标记 `duplicate_document_consolidation: completed`；任务保持 `awaiting_review` 等待用户验收。
- 用户验收通过，M00-DOC-001 置为 `approved` 并归档；`07-task-register.md`、`integrity.yaml` 与任务报告同步，active 五件套按审计保留原位，等待决策模型生成下一任务时重置。

## 2026-08-09（决策模型）

- 决策模型生成唯一活动任务 `M00-DOC-001`，用于最终收口 Standards、VR、Systems 与 Registers 的重复命名、独有内容和旧路径引用；状态为 `ready`，执行范围由 active 白名单限定。
- 新增重复事实源与无 Git 回退风险 `RSK-010`、`RSK-011`；用户已手动删除首批 11 个确认无独有价值的废弃文件。
- 统一 standards、vr、systems、registers 与 Design 的小写索引入口，验证本地 Markdown 链接无断链；active 继续保持 `draft` 且白名单为空。
- 明确 Design 为产品详规、Systems 为工程实现指引，并建立 M00-M06 标准渐进完善待办，避免在缺少真实工程证据时一次性冻结全部细节。
- 修复旧范围标准、玩家身体表现与两份决策登记中的 1v1 Demo/N 对 N/全身 IK 冲突，使其服从 GameMasterPlan。
- 将 `standards/`、`vr/`、`systems/`、`registers/` 与 `knowledge/Design/` 的目录入口统一为实存小写 `index.md`，移除对应 `README.md`。
- 将七份 systems 正文收敛为“工程实现指引”，逐份链接 `knowledge/Design/` 对应权威产品详规，不再复制玩法规则与数值。
- 更新唯一项目 Skill，明确 `rules.md` 兼容入口、`rules/project_rules.md` 权威规则、四份治理契约、四份操作模型及 active 完整门禁路径。
- 新增 `registers/standards-backlog.md`，按 M00-M06 记录标准完善待办、优先级、触发条件与完成定义。
- 同步 `.trae/README.md`、`.trae/index.md`、`manifest.yaml` 与 `integrity.yaml`；实际检查索引文件、链接、Skill frontmatter、active 状态和白名单。
- 验证结果：五个目标目录均存在小写 `index.md` 且无 `README.md`；七份系统指引均链接 Design；唯一 Skill frontmatter 数量为 1；active 状态为 `draft`；白名单有效条目为 0；Markdown 本地链接检查通过。
- Git 未安装、未执行；未声明 Git、编译、编辑器或 PICO 真机验证。

## 2026-08-08

- 将 `TraeAI/KnowledgeBase`、`TraeAI/Execution`、`TraeAI/Archive` 的有效正文迁入 `.trae/knowledge`、`.trae/execution`、`.trae/archive`。
- 删除 `TraeAI`、`Docs`、根级旧规划目录和重复 Skill；项目只保留 `.trae/skills/three-kingdoms-vr-arena/SKILL.md`。
- 统一规则、Skill、Content 说明和 Markdown 链接到 `.trae` 新结构。
- `Build` 未包含项目构建脚本或平台资源，因此不保留空目录；UE 生成目录不纳入整理结果。
- 用户已手动删除旧目录；当前有效 AI 资料统一位于 `.trae/`，后续不再使用 `TraeAI/` 或 `Docs/`。
- 计划基于 UE5.8 官方 VR 模板重建项目；M00 前置步骤与模板核对清单已写入 `.trae/execution/M00-Foundation.md`。
