# ChangeLog

## 2026-08-24（看板口径修正：路线图呈现 + 执行中/部分完成状态支持）

- **看板新增里程碑规划范围**：解析 `execution/M00–M06` 七份里程碑文档的目标与交付，数据流区块按里程碑展示"规划交付"清单及"规划 N 项"徽标；未立项里程碑默认展开并注明任务包由决策模型按需拆解，解决"规划任务在看板无体现"。
- **执行中（in_progress）全链路支持**：`classify_task_status` 新增匹配分支、CSS 新增 `.tbadge-inprogress`、前端徽章映射与执行节点文案同步。
- **部分验证（partial）全链路支持**：修复 M00-T001"部分验证"被归为未知的问题，徽章显示"部分完成"（金色）。
- **M01-T005 口径修正**：登记册、两级 STATUS.json、manifest/integrity 快照同步为 in_progress——TD-012 偿还项未闭环（PICO 串流、中文标注、PIE 帧率、Lightmass），偿还完成后重新提交审批。

## 2026-08-24（M02-PREP-001 验收通过：CR 实施关闭 + 同批治理维护）

- **验收结论：通过**。四份规格齐备且用户逐项确认，33 张参考图交付核验吻合。任务状态 `awaiting_review` → `in_progress`（附条件回炉）→ `approved`（两级 STATUS.json 同步），验证证据登记 V-009。
- **CR-20260824-001 实施关闭**：命名标准盾牌/长柄示例名改为 `SK_Weapon_Shield_Han`、`SK_Weapon_Polearm_Ji`，有效标准正文零旧名残留；CR §7/§8 回填关闭。
- **资产登记册**：AST-009 路径对齐 `L_Prototype_1v1_v2.umap` 转 approved；AST-008 批量条目（33 图）转 approved 并补分类计数。
- **登记册同步**：07-task-register M02-PREP-001 行改 approved 口径；09-verification-register 新增 V-009。
- **索引补全**：reports/tasks/README 由 3 条补至 9 条；根 index.md Execution 基线补齐 M00-T006/M01-T001/M01-T005/M02-PREP-001 四个任务包链接。
- **文件卫生**：删除误放脚本 CreateWeaponBlueprints.py；清理 dashboard/__pycache__/；.gitignore 增补 `Content/**/*_BuiltData.uasset`。
- **integrity.yaml**：active_gate 快照同步（补 M01-T001 blocked、修正两处 ready→approved、updated=2026-08-24）。

## 2026-08-24（M02-PREP-001 收尾：动画清单澄清 + 参考图收口 + 命名 CR）

- Step 5 动画清单加用途澄清：37 个动画全部服务于 AI 角色；玩家动作由头显/手柄追踪 + Full Body IK 实时生成，受击反馈用镜头+手柄震动，M02 不得为玩家重复制作移动/攻击动画。
- 参考图收集收口：弓类维持 2 张、Unit 维持 1 张（用户决定不再补）；Scene/General 确认归 M05 启动时再补。Step 2 待办关闭。
- 命名标准变更申请 `CR-20260824-001`（draft）：`Shield_Round`→`Shield_Han`、`Polearm_Glaive`→`Polearm_Ji`，待用户批准后修改 `standards/02-naming-and-path-standard.md`。
- 任务状态 `in_progress` → `awaiting_review`，待用户最终确认关闭 M02-PREP-001。

## 2026-08-24（模块化角色系统架构定稿）

- M02-PREP-001 报告新增 Step 6：模块化角色系统架构。采用 UE `Set Master Pose Component` 方案，头/身体/甲胄分离。
- 三种体型变体：Standard（175cm）、Heavy（180cm，许褚/典韦）、Lean（170cm，赵云/弓兵），共用 MannequinXR 骨架。
- 头部独立：8 个武将头部 + 2 个士兵头部，按里程碑逐步生成。许褚裸上身方案：Heavy 体型 + 不穿躯干甲胄。
- 甲胄模块化：4 级躯干甲胄（布衣/皮甲/札甲/筒袖铠）+ 2 种头盔 + 臂甲/胫甲，对应六部位护甲系统。
- AI 生成工作流优化：分部件生成比完整角色效率高 4-8 倍。混元 3D 每日 20 次额度，17 次可完成全部原型。
- 资产登记册更新：AST-002 废弃，新增 AST-014~026 共 13 个模块化资产。武器前置资产从 AST-002 改为 AST-014。

## 2026-08-22（M01 规划文档结构化 + 登记册同步）

- M01-CombatSlice.md 重构：新增任务依赖链、M00→M01 接管项追踪表、TD-012 解决计划（三条路径 + 复审时机）、退出条件逐项验证方案、M01→M02 前置依赖清单。
- 任务登记册：M01-T001 状态 `awaiting_review` → `blocked`（4 条 PIE 检查未完成，资产创建已完成）。
- 技术债登记册：TD-012 偿还计划更新（Direct Preview 为首选路径，M01 结束前复审）。
- M01-T001 根 STATUS.json + 任务目录 STATUS.json 状态修正为 `blocked`。

## 2026-08-22（审核反馈修复：M01 任务规划补全 + M00 验收记录 + 规划纪律）

- **P0**：M00→M01 接管项整合进已有规划——VRPawn 挂载 CapabilityComponent 作为 M01-T002（伤害结算）前置步骤，运行时流程验证作为 M01-T006（1v1 测试流程）验证步骤。不新建任务，不破坏原始任务编号。
- **P1**：创建 M00 里程碑验收记录（`milestones/M00-acceptance.md`），声明"玩家全身占位"由 M02 全身 IK 任务承接，M00 有条件通过。
- **P1**：TD-012 新增 M01-T007（Direct Preview 验证），不占用原规划 T001-T006 编号。
- **治理**：DecisionModel 新增任务生成门禁第 7 条（任务编号冲突检测），禁止在未读取里程碑规划文档的情况下分配任务编号。
- **回滚**：删除此前错误创建的 M01-T002（能力组件挂载）和 M01-T006（Direct Preview），恢复根 STATUS.json。

## 2026-08-20（治理增强：执行模型证据打包 + 多模态拆分规则）

- ExecutionModel.md：新增"证据打包"硬性要求，提交审核前必须填写结构化验证表（每条 CHECKS 项 → 证据类型 → 状态 → 证据路径），禁止模糊表述。
- ExecutionModel.md：新增"多模态任务特殊规则"，`[PIE]` 检查项执行模型无法完成时任务必须设为 `blocked`，不得设为 `awaiting_review`。
- DecisionModel.md：新增任务生成门禁第 5 条（多模态任务拆分：`[PIE]` ≥ 3 条必须拆分为两个任务）和第 6 条（CHECKS.md 证据类型标注：`[文件]`/`[截图]`/`[日志]`/`[PIE]`）。
- M01-T001 CHECKS.md：更新为新格式示例，所有检查项增加 `[证据类型]` 标注和复选框。

## 2026-08-20（M01-T001 蓝图创建完成 - UEBridgeMCP）

- 使用UEBridgeMCP（HTTP MCP工具，407个工具）完成武器蓝图创建。
- 创建 `BP_WeaponBase`：继承 `GrippableSkeletalMeshActor`，添加2个 `HandSocketComponent`（Primary + Secondary）。
- 创建 `BP_TestSword`：继承 `BP_WeaponBase`。
- 放置 `TestSword_01` 到关卡中（位置 [0, 0, 100]）。
- 任务状态更新为 `awaiting_review`。
- UEBridgeMCP配置：`Config/DefaultUEBridgeMCP.ini`（端口8080，自动启动）。

## 2026-08-19（M01-T001 实施指南生成）

- M01-T001 状态：`ready` → `in_progress` → `awaiting_review`。
- 会话 `session-20260819-001` 认领任务。
- VRExpansionPlugin 5.4 编译状态确认（Binaries/Win64 目录存在）。
- 生成实施指南：`execution/reports/tasks/M01-T001.md`，包含完整蓝图创建步骤、组件配置、HandSocket 握持姿势配置、测试武器创建和编辑器验证流程。
- 资产登记册更新：新增 AST-012（BP_WeaponBase）、AST-013（BP_TestSword），状态 `awaiting_review`。
- 任务登记册更新：M01-T001 状态 `awaiting_review`。
- 待用户在 UE 编辑器中执行蓝图创建和验证后，更新状态为 `approved`。

## 2026-08-19（Git 提交与推送：4 原子 commit + origin/master 同步）

- 校验程序修复：`dashboard/check-integrity.py` 21/21 通过（含 M01-T005 awaiting_review 超时、open 技术债 ≤3、状态交叉引用）。
- 4 个原子 commit 推送到 `origin/master`（`f41fd6b..7843f73`）：
  1. `docs(governance)` M01-T005 审核批准 + TD-011 偿还 + TD-012 deferred（含债务状态定义新增）
  2. `fix(plugins)` PICO 串流还原 Config + UEBridgeMCP 子模块更新 + VRE SceneProxy override
  3. `feat(level)` M01-T005 灰盒竞技场 v2 增量 (L_Prototype_1v1_v2)
  4. `chore(status)` M01-T001 由其他执行模型认领 (session-20260819-001)
- LFS：35 个对象（51 MB）已上传。
- M01-T005 完成：状态 `approved`，VR Preview 补验通过（XR Session FOCUSED + PICO Runtime + 截图）。
- TD-011 偿还（性能基线已建），TD-012 改 `deferred` 状态（PICO 串流问题短期不解决）。
- 新增"债务状态定义"段（`open` / `deferred` / `resolved`），明确门禁规则与复审承诺要求。

## 2026-08-19（M00 里程碑验收通过：正式进入 M01）

- M00 里程碑验收结论：**通过**。
- 退出条件全部满足：空场景可生成占位角色（T005/T006）、双平台构建门禁通过（T003/T004/T006）、规则层无 1v1/单武器/联网硬编码（T005 代码审查）。
- 交付物全部满足：VR 真机可用（V-008）、七大模块边界 + 统一能力接口（T005）、八个 DA 基类（T005）、自动化测试 + 日志 + 性能基线（T006/V-006）。
- 任务状态：T001-T006 + DOC-001 全部 approved（T001 ACL V-007 待管理员，不阻塞）。
- 风险审查：无 M00 阻塞开放风险。技术债 TD-005/006/010/011 均 open 但不阻塞。
- 正式进入 M01 核心战斗技术切片。
- M01 当前状态：M01-T001（武器抓取与 VRE 集成）ready、M01-T005（灰盒竞技场）awaiting_review。

## 2026-08-19（M00-T006 审核批准：approved）

- 审核模型复核通过，用户批准。M00-T006 状态：awaiting_review → approved。
- 核验项：12/12 自动化测试（8 DataAsset + 2 GameFlow + 2 接口）、8 日志分类运行时验证、Win64 + Android（含 APK）双平台构建门禁、性能基线（stat + LogVRSanguoPerf）、V-006 验证登记同步。
- 抽查测试代码质量：VRGameFlowSpec 用例对齐 systems/01 迁移矩阵（合法链路/非法拒绝/幂等/生命周期），断言含中文诊断。
- 偏差均接受：无人值守测试方式（UnrealEditor-Cmd -unattended）、Execute_ 静态包装调用、工具链修复（bUseUnity=false、VRE 5.6-Locked）均用户批准并记录。
- 遗留：测试场景规划表终版 M01 接管。
- **M00 里程碑任务全部 approved**（T001-T006 + DOC-001；T001 ACL 应用 V-007 待用户管理员执行，不阻塞）。
- STATUS.json（根+任务）、07-task-register、M00/README.md 同步。

## 2026-08-16（M01-T005 VR 验证补验：编辑器 GUI + MCP 自动化）

- 用户审核打回：真机验证未完成，不能进审核。
- 补验完成：通过 UEBridgeMCP（HTTP 8080）自动化采集 VR 渲染证据：
  - OpenXR 运行时切换为 PICO Streaming Runtime（绕过 SteamVR pipe broken 问题）
  - XR Session 完整生命周期：IDLE → SYNCHRONIZED → VISIBLE → FOCUSED → STOPPING → EXITING
  - VR Preview 窗口标题确认：`OpenXR PICO XR Runtime (1.1.46)`
  - 截图确认：灰盒竞技场场景在 VR Preview 视口正确渲染（网格地面、围墙、掩体、高台、标注、光照阴影）
  - PICO 驱动姿态正常：`pose recovery mode` 处理 HMD 姿态数据
  - PIE 世界：46 Actor，GameMode=VRGameMode_C
- **未完成**：PICO Connect 10.6.6 串流未自动切换到 VR 模式（停留在桌面串流），头显内未显示 VR 场景。登记 TD-012。
- Config 还原：`bStartInVR=True` 已移除（临时验证用途，验证后还原）。
- 任务报告更新：追加 VR Preview 验证段落、偏差清单更新。
- 技术债新增 TD-012：PICO Connect VR 串流模式切换问题（中优先级 open）。

## 2026-08-16（M01-T001 任务包生成：武器抓取与 VRE 集成）

- 决策模型生成 M01-T001 五件套。利用 VRExpansionPlugin 5.6 建立手部物理抓取武器能力。
- 交付：`TASK.md`、`ALLOWLIST.txt`、`INPUTS.md`、`CHECKS.md`、`STATUS.json`。
- 参考：VRE 示例项目（`E:\AWork\VRExpPluginExample\`）近战武器/双手握持/手部姿势蓝图。
- 状态：ready，待认领。预估 1.5h。

## 2026-08-16（M00-T006 执行完成：自动化测试 12/12 通过）

- Step 1-6 全部完成，状态 awaiting_review：
  - 新增 6 个自动化测试文件（`Source/.../Tests/`）：VRDataAssetSpec（8 DA 校验）、VRInterfaceSpec（2 接口）、VRGameFlowSpec（2 状态机）
  - `Automation RunTests VRSanguo` 12/12 通过（8 DA + 2 GameFlow + 2 接口），V-006 更新为已验证
  - 8 个日志分类运行时验证（Flow 48/Combat 3/其余各 1）
  - 性能基线：stat unit/fps/scenerendering 可用 + LogVRSanguoPerf 注册；场景规划初版（1v1/武器训练/4v4）
  - Win64 门禁通过（73 动作）；Android 门禁通过（UBT Development 构建 + APK 打包成功，2026-08-19）
- 工具链修复（用户批准/指示）：
  - UEBridgeMCP 5 模块 Build.cs 加 `bUseUnity=false`（UE5.6 Unity Build 匿名 namespace 重定义）
  - VRExpansionPlugin 替换为官方 5.6-Locked 分支（原 master 源码 UE5.6 不兼容，4 类 API 错误；官方分支编译通过）
  - 测试代码修正：BlueprintNativeEvent 用 `Execute_` 包装；未注册 Actor 桩值用 `_Implementation` 直验
- 报告：`execution/reports/tasks/M00-T006.md`

## 2026-08-16（M02-PREP-001 执行进度：马槊定稿 + 工具链迁移 E 盘）

- 马槊（AST-011）：用户混元 3D 生成两版，首版（上传骑砍 OBJ 重制）枪头变形弃用；二版（图生 3D）用户确认形制 OK。AI 定标缩放至全长 300cm（混元单位=cm 校准，环首刀 101.89 单位=100cm 验证），1,535 面/UV 保留，OBJ 存临时区 FBX_Low。
- 工具链迁移：用户要求软件与临时文件不得占用 C/D 盘。临时文件迁至 `E:\AWork\Temp\VRSanguoRef`（483MB）；Python 资产处理环境迁移至 `E:\AWork\Tools\venv_asset`（pymeshlab/trimesh/matplotlib 等）；C 盘误装包已卸载；OpenBRF Redux 装至 `E:\AWork\Tools\OpenBRF`。
- 模型预览方案：3ds Max 不可用（GUI 与批处理均无法启动），采用 matplotlib 无头渲染三视角 PNG 供用户确认形制。
- 待办：6 件武器 + 马槊 OBJ 导入 UE 验证（M02 正式任务）；骑砍 OBJ/brf 弃用（面数 140 过低）。

## 2026-08-15（M02-PREP-001 执行进度：六武器低模减面完成）

- 6 件武器 FBX 高模（~50 万面/件）全自动减面完成，输出低模 OBJ（环首刀 3K/刀鞘 800/戟 4K/矛 3K/弓 3K/盾 2K），UV 全部保留。
- 工具链：3ds Max 批处理被许可证阻塞不可用；fast-simplification 不保留 UV；最终采用 pymeshlab（MeshLab 引擎）quadric edge collapse 减面成功，贴图 4096² 压缩至 ≤1024（100-180KB/张）。
- 从 FBX 提取内嵌 PBR 贴图（4 张 4096² + 辅助图），压缩版存 `textures_1024/`。
- 产出位置：`D:\AWork\Temp\VRSanguoRef\FBX_Low\`（项目外临时区），资产登记册 AST-003~007/010 备注同步。
- 待办：6 件 OBJ 导入 UE 验证（材质贴图关联）+ 高模 FBX 备份（PC 端 LOD 源）。

## 2026-08-15（M02-PREP-001 执行进度：参考图落盘 + 模型检查）

- 参考图整理：用户收集 33 张，AI 质检重命名（`REF_Category_Name_NN.ext`）复制至 `Content/VRSanguo/Art/References/`（Sword 7/Shield 4/Polearm 4/Spear 7/Bow 2/Armor 8/Unit 1）。
- FBX 模型检查：用户已生成 6 件武器 FBX（环首刀/刀鞘/卜字戟/矛/角弓/长方盾，暂存临时区），解析 Vertices 确认均为 ~83K tris 高模、58-76MB，须减面至规格（2-4K/鞘 800）后导入 UE。
- 资产登记册：新增 AST-010（刀鞘）；AST-003~007 备注 FBX 生成状态；AST-008 参考图更新为 in_progress（33 张落盘，Scene/General 待补）。
- 弃用：骑砍 .brf 模型与来源不明 DDS 贴图，仅临时区留存。
- 待办：6 模型减面+贴图压缩+导入 UE（M02 正式任务）；Bow 参考图补 1-3 张。

## 2026-08-15（规则新增：磁盘与下载文件存放规则）

- 用户要求：执行模型下载软件时默认下载到 C 盘影响空间，需建立规则约束。
- 修复（用户直接批准）：
  - `rules/project_rules.md`：新增"磁盘与下载规则"段。定义 C:/D:/E: 三盘用途（C: 系统/软件、D: 项目/高频工具、E: 大文件/低频/归档）。强制规则：禁止默认下载到 C 盘；>500MB 文件放 E:；安装包/SDK 压缩包放 E:；下载后清理临时文件。

## 2026-08-15（M00-T005 审核批准：approved）

- M00-T005 审核批准（用户审批）。CHECKS 修正后按新标准逐项核对全部通过。
- 交付：22 个 C++ 文件编译通过、7 接口/8 DA/状态机/能力组件/TestDummy + L_SkeletonTest 关卡。
- M01 接管项：流程状态机运行时验证（Combat→Damage→Reset 链路）、VRPawn 挂载 VRCharacterCapabilityComponent。
- 状态：in_progress → approved。T006 前置依赖已解除。

## 2026-08-15（治理修复：决策模型 CHECKS-ALLOWLIST 交叉验证门禁 + 任务详规矛盾修复）

- 根因：M00-T005 执行模型以"白名单外/编排职责"为由跳过 CHECKS 检查项，溯源发现任务详规自身存在 CHECKS 与 ALLOWLIST 的结构性矛盾。全量审计发现 4 个任务共 7 处矛盾。
- 修复（5 个文件，用户直接批准）：

**任务详规修正（3 个）：**
- `execution/active/M00-T005/CHECKS.md`：流程状态机验证从"运行时通过"改为"代码审查通过"；VRPawn 挂载 + 空场景运行时验证标记为 M01 接管项。新增"M01 接管项"段。
- `execution/active/M00-T006/CHECKS.md`：测试场景规划表从"完整"改为"初版完整（写入任务报告）"，终版标记 M01 接管。新增"M01 接管项"段。
- `execution/active/M02-PREP-001/CHECKS.md`：4 份规格文档明确标注"写入任务报告"。新增"里程碑归属说明"段，标注骨架/武器/动画规格的终版回溯时机（M03）。
- `execution/M00/T005-SystemSkeleton.md`：完成定义 checkbox 同步修正，验收清单新增"归属"列区分 T005/M01。

**治理门禁（1 个）：**
- `governance/DecisionModel.md`：新增"任务生成门禁"段，4 项强制交叉验证：CHECKS-ALLOWLIST 交叉验证、里程碑归属标注、ALLOWLIST 路径完整性、禁止路径冲突检测。在任务设为 ready 前必须逐项核对。

## 2026-08-15（治理修复：ALLOWLIST 缺口禁止跳过检查项）

- 问题：M00-T005 执行模型以"VRPawn 在白名单外"为由跳过 CHECKS.md 硬性检查项（VRPawn 挂载 Capability 组件），将缺口甩给 M01。
- 修复（用户直接批准）：
  - `governance/ExecutionModel.md` §强制停止：新增"CHECKS.md 检查项因 ALLOWLIST 缺口无法完成"停止条件。要求停止并报告 ALLOWLIST 缺口，不得跳过检查项或标记 awaiting_review。

## 2026-08-14（治理修复：推送前自动门禁）

- 问题：git push 前缺少自动校验，导致推送时 integrity/manifest/登记册/看板未同步。
- 修复（2 个文件，用户直接批准）：
  - `governance/SessionCommands.md`：新增"推送"章节，含 6 项推送前必检清单（check-integrity.py → integrity.yaml → manifest.yaml → 登记册 → 看板生成 → CHANGELOG）和 6 步执行流程。标记为硬性门禁，任一未通过不得推送。
  - `skills/three-kingdoms-vr-arena/SKILL.md`：模式路由表新增"推送/git push/上传git/提交并推送"路由，指向 `SessionCommands.md` §推送。

## 2026-08-14（治理核验同步：integrity/manifest/看板/登记册）

## 2026-08-13（M00-T005 系统骨架执行完成）

- Step 1-6 全部完成，状态 awaiting_review：
  - Core/：VRTypes（12 枚举 + 9 结构体）、VRLogChannels（8 日志分类）、VRGameplayTags（11 个 Native Tag）
  - Interfaces/：7 项接口（IInteractable/IWeaponSource/IDamageable/IDefenseProvider/IMovementMode/IBattleParticipant/ICharacterCapability）
  - Data/：8 个 DA 基类（Weapon/Armor/MovementProfile/MatchRuleSet/Unit/Commander/Arena/Avatar，SchemaVersion+PostLoad+ValidateData）
  - Flow/：VRGameFlowComponent 状态机；Combat/：VRCharacterCapabilityComponent + VRTestDummy
  - L_SkeletonTest.umap 关卡（VRTestDummy_0 + Floor_Graybox，12223B 落盘验证）
  - 编译通过（13 动作 Succeeded），编辑器加载 DLL + 类注册验证通过
- 工程修复（用户批准）：`.uproject` 补 Modules 字段（此前缺失导致编辑器不加载游戏模块）；Build.cs 加 GameplayTags + AIModule 依赖
- 实施偏差记录：EMovementMode→EVRMovementMode（引擎同名冲突）；IInteractable 手部参数用 AActor*（AVRHand M01 收紧）
- 遗留：PIE 运行验证（可转 T006 VRGameFlowSpec 自动化覆盖）；VRPawn 挂载 Capability 组件（M01）
- 报告：`execution/reports/tasks/M00-T005.md`

## 2026-08-13（M01-T005 执行完成：灰盒竞技场关卡）

- AI 执行（session-20260813-001）完成 `M01-T005: 灰盒竞技场关卡`，状态 in_progress -> awaiting_review。
- 交付物：`Content/VRSanguo/Dev/L_Prototype_1v1.umap`（26 Actor）——20x20m 地面、4m 围墙、掩体 A/B（1.2m 半身高）、高台 C（1m + 26.6° 斜坡）、PlayerStart/AI TargetPoint 对称出生、武器生成位 x2、NavMeshBoundsVolume 20x20x4、RecastNavMesh（Static 已构建）、DirectionalLight/SkyLight/ExponentialHeightFog、9 个 TextRender 尺寸标注。
- World Settings GameMode 使用模板 `VRGameMode`（M00-T005 的 BP_VRGameMode 未就绪，按任务约定回退）。
- 自动化验证：关卡加载、几何尺寸/对称/材质断言、出生区无障碍、NavMesh 构建日志（`BuildPaths` 触发 `UNavigationSystemV1::Build`）全部 PASS。
- 偏差记录：标注用英文（缺中文字体资产）；Lightmass 烘焙未执行（无头编辑器 DDC/Zen 写入受限，需 GUI 会话）；PIE fps >= 90 待编辑器/真机验证；MapCheck Nanite/VSM 警告待变更申请。
- 登记册同步：07-task-register、10-asset-register（新增 AST-009 MAP）；报告 `execution/reports/tasks/M01-T005.md`。
- 并发说明：执行期间根 STATUS.json 被并行会话更新（M02-PREP-001 用户认领 in_progress、各任务 note 精简），认领写入被覆盖；已重新读取最新内容合并，保留并行条目并将 M01-T005 更新为 awaiting_review。

## 2026-08-13（M02-PREP-002 撤销：回归 M02-PREP-001 统一执行）

- 用户反馈：M02-PREP-001 本身已包含 Step 2（参考图片收集），审核 `requires_changes` 回退到 `in_progress` 后应继续在本任务下完成，无需拆分独立任务包。
- 撤销 M02-PREP-002：删除 `active/M02-PREP-002/` 全部五件套，从根 STATUS.json 和 07-task-register 移除。
- 将 M02-PREP-002 的收集协议细节（子目录结构、命名格式、搜索关键词、六武将名单）合并到 M02-PREP-001 的 TASK.md Step 2 中。
- M02-PREP-001 状态保持 `in_progress`，继续完成 Step 2 后重新提交审核。

## 2026-08-13（M02-PREP-002 任务包创建：美术参考图片收集）

- M02-PREP-001 审核反馈 `requires_changes`：规格决策全部定稿，唯一缺口是参考图片未收集。
- 创建用户执行任务包 `M02-PREP-002: 汉末三国美术参考图片收集`。
- 5 批次逐项收集：五武器（环首刀/盾/戟/矛/弓）、甲胄（札甲/皮甲/盔/护臂/胫甲）、兵种（5 类）、场景（校场/夯土/营帐/军旗/战鼓）、武将（关羽/张飞/赵云）。
- 每批次含搜索关键词、文件命名规则、子目录结构，执行模型逐项引导用户收集并验证。
- 补齐后 M02-PREP-001 可一并提交审核通过。
- 活动任务包五件套创建于 `active/M02-PREP-002/`。

## 2026-08-13（治理修复：禁止执行模型未完成即提交审核）

- 问题：执行模型频繁将未完成交付物包装为"待办"后直接提交 `awaiting_review`，绕过完成定义。M02-PREP-001 为典型案例：参考图片未收集即提交审核。
- 修复（2 个文件，用户直接批准）：
  - `governance/ExecutionModel.md`：新增"提交审核前自检（硬性门禁）"段落，含 5 项自检清单（交付物完整性、CHECKS 全项通过、禁止路径未修改、验证证据可定位、无遗留待办伪装）和自检失败处理规则。位于状态更新时机表之后、前置门禁之前。
  - `governance/definition-of-done.md` §6：新增"禁止提前提交审核"条款，明确未完成交付物不得以"待办/遗留/后续补充/已规划/待用户执行"等任何形式包装为已交付，也不得通过挪入报告"风险/待办"段落绕过完整性检查。

## 2026-08-13（M02-PREP-001 审核：requires_changes）

- 审核模型复核 M02-PREP-001，结论 `requires_changes`。
- 通过项：平台选型（5 平台完整对比）、骨架规格（MannequinXR 兼容）、武器规格（5 类定稿）、动画清单（37 个）、ALLOWLIST 合规、无第二 Skill、无治理锁定文件修改、无新增技术债、无总纲偏离。
- 未通过项：`Content/VRSanguo/Art/References/` 目录未创建，参考图片（35-55 张）未收集。CHECKS.md 要求"参考图片已导入且可在编辑器中预览"，当前不满足。
- 附加发现：`integrity.yaml` 过时（仍记录 2026-08-11 状态），不阻塞本任务但需后续治理同步。
- 状态：`awaiting_review` → `in_progress`。待用户收集图片后重新提交审核。

## 2026-08-13（M02-PREP-001 执行完成：资产生成准备与平台选型）

- 用户执行、AI 监督任务完成 5 步交互引导：平台调研、美术参考收集、骨架规格、武器规格、动画需求清单。
- 平台选型：腾讯混元 3D（每日 20 免费资格）为主生成工具 + 3ds Max 自建修正 + 免费资源补充；动画完全自建（P1 备选 Mixamo 重定向 12 个基础动画）。
- 骨架定稿：UE5.6 MannequinXR 兼容；兵卒 170cm / 武将 180cm；五指骨骼；`weapon_r/weapon_l/weapon_back/weapon_hip/armor_*` 挂载点；FBX。
- 五武器形制定稿：环首刀、钩镶/长方盾、戟、矛/槊、角弓/反曲弓；长度以美术指南为准；模型命名按形制（`Shield_Han`/`Polearm_Ji`），命名标准待变更申请同步。
- 六武将名单：吕布、典韦、关羽、张飞、赵云、马超（"一吕二典三关四张五赵六马"）。
- 动画清单约 37 个（含瞄准姿态、阵线推进、收放/换手；弓箭不做连射；保留盾牌推挤）。
- 报告写入 `execution/reports/tasks/M02-PREP-001.md`；状态 `awaiting_review`；资产登记册新增 AST-002~008（draft）。
- 待办：参考图片收集（用户执行，AI 统一重命名）；命名标准变更申请；混元 3D 输出验证。

## 2026-08-13（认领门禁治理加固：7 文件 + 4 任务包同步）

- 问题：执行模型在另一个会话中开始执行任务但未更新 STATUS.json 状态（仍为 `ready`），导致状态追踪失效。
- 根因：认领规则虽在 ExecutionModel.md 中定义，但缺少强制性前置门禁，执行模型可能跳过认领直接开工。
- 修复（7 个治理文件）：
  - `rules/project_rules.md`：执行规则新增"认领门禁（最高优先级）"为第一条，明确"未认领不得开始实施"。
  - `governance/ExecutionModel.md`：任务认领段提升为第一节，标题加"必须在任何文件修改之前完成"；新增"硬性门禁"声明、认领后验证步骤（第 4 步）、用户执行任务认领说明、状态更新时机表（6 个时机）。
  - `skills/three-kingdoms-vr-arena/SKILL.md`：active 门禁路径新增第 0 步"认领"，明确"未完成认领不得修改任何文件"。
  - `governance/SessionCommands.md`：`执行当前任务`命令增加"先认领任务"前置要求。
  - `execution/task-template.md`：新增"§0 认领协议"段（5 步认领流程）。
  - `execution/task-template-asset.md`：同上。
  - `execution/task-template-level.md`：同上。
- 修复（4 个已有任务包 CHECKS.md）：
  - M00-T005、M00-T006、M01-T005、M02-PREP-001 的"执行前"段新增认领检查项。
  - M02-PREP-001（用户任务）特别标注"AI 监督模型代为更新"。

## 2026-08-13（M01-T005 任务包创建：灰盒竞技场）

- 创建 AI 执行任务包 `M01-T005: 灰盒竞技场关卡`。
- 无前置依赖，可与 T005/T006 并行执行。
- 使用 LevelPrototyping 搭建 20x20m 1v1 测试场景：出生点、掩体、高台、NavMesh、光照。
- 活动任务包五件套创建于 `active/M01-T005/`。
- 根 STATUS.json、07-task-register 同步。

## 2026-08-13（M00-T006 复核与详规扩充：纠正"已批准"状态）

- 调查发现 T006 标记"已批准"但交付物从未实现：V-006 验证状态为"待验证"、Source 无测试文件、无活动任务包、原报告因"4 行记号级"已删除。
- 详规从 25 行扩充为 6 步可执行方案：
  - Step 1：构建门禁验证（Win64 + Android，无 T005 依赖可并行）
  - Step 2：8 个日志分类运行时验证
  - Step 3：DataAsset 校验自动化测试（8 个 DA 基类）
  - Step 4：接口与流程状态机自动化测试
  - Step 5：性能采样基线配置
  - Step 6：测试场景规划表（1v1/4v4/武器训练场）
- M01 范围交付物（武器命中去重、格挡、VR 调试面板）explicitly deferred。
- 活动任务包五件套创建于 `active/M00-T006/`。
- 状态纠正：已批准 -> ready（前置依赖 T005 Step 1-5）。
- 根 STATUS.json、M00/README.md、07-task-register 同步。

## 2026-08-13（M02-PREP-001 任务包创建：用户资产生成准备）

- 创建用户执行任务包 `M02-PREP-001: M02 资产生成准备与平台选型`。
- 执行方：用户执行，AI 监督。可立即开始，与 T005/M01 并行。
- 包含 5 步：平台调研、美术参考收集、骨架规格确定、武器规格确定、动画需求清单。
- 活动任务包五件套创建于 `active/M02-PREP-001/`。
- 根 STATUS.json、07-task-register 同步新增任务条目。

## 2026-08-13（M00-T005 详规修订：对齐架构改版）

- T005 详规全面修订，对齐 2026-08-11 架构改版后的系统接口契约与标准：
  - 接口签名：7 项接口方法全面对齐 `standards/05` C++ 声明和 `systems/01-07` 接口契约（IInteractable/IWeaponSource/IDamageable/IDefenseProvider/IMovementMode/IBattleParticipant/ICharacterCapability）。
  - Data Asset 类名：从 `UVRS*Data` 改为 `UVR*Definition/Profile/RuleSet`，对齐 `systems/index.md` 数据资产目录和 `standards/02` 命名标准；新增 SchemaVersion 与 PostLoad 迁移（对齐 `standards/04`）。
  - 流程状态机：`EGamePhase` -> `EGameSessionPhase`，`UVRSGameFlowSubsystem` -> `UVRGameFlowComponent`，方法签名对齐 `systems/01` 契约（RequestPhaseTransition/StartMatch/EndMatch/ResetMatch）。
  - 公共类型：新增 `FAttackRequest`/`FCombatResult`/`FDefenseResult`/`FMovementTarget`/`FMovementResult` 等（对齐 systems/02-04），替换原 `FDamageResult`。
  - 文件/类命名前缀：`VRS` -> `VR`（对齐 `standards/02`）。
  - VR 模板引用：更新为 UE5.6 模板实际资产路径（`Content/VRTemplate/`）。
  - 前置依赖：T004 状态从 `blocked` 更新为 `approved`。
- 活动任务包五件套同步更新（TASK.md/ALLOWLIST.txt/INPUTS.md/CHECKS.md/STATUS.json）。
- `M00/README.md` 任务状态表同步：T004 -> approved，T005 -> ready（详规修订）。
- `07-task-register.md` T005 条目同步。

## 2026-08-13（M00-T004 审核批准：approved）

- 审核模型复核通过，用户批准。M00-T004 状态：awaiting_review → approved。
- 核心成果：PICO Neo3 真机场景可见、输入可用、手柄模型显示、VRPawn 稳定生成。
- 遗留：Neo3 卡顿（TD-011）、swapchain 补丁（TD-005）、UEBridgeMCP 工具链（TD-010），不阻塞 M00。
- STATUS.json（根+任务）、07-task-register 同步。

## 2026-08-13（M00-T004 审核修正：4 项状态同步）

- 审核模型提出 4 项修正，全部处理：
  1. V-008 状态更新为"已验证（2026-08-13）"，证据链含输入绑定、手柄挂载、碰撞修复（`09-verification-register.md`）。
  2. PicoValidationMatrix 回填真机列：VR-001~VR-005 通过（2026-08-13），VR-006/007/008 保持待验证（未专项测试不包装）（`vr/PicoValidationMatrix.md`）。
  3. 补齐任务报告 `execution/reports/tasks/M00-T004.md`（TASK.md Phase 7 要求）。
  4. TD-001 标记 resolved（UE5.8→UE5.6 降级已于 2026-08-11 完成）（`11-tech-debt-register.md`）。

## 2026-08-13（M00-T004 真机验收通过：手柄模型显示、输入生效）

- VRPawn 手柄模型与碰撞修复（MCP 自动化 + 真机验证）：
  - 挂载 `SM_PICONeo3_L/R` 静态网格到 MotionControllerLeftGrip/RightGrip 下；原骨骼手部组件 HandLeft/HandRight 已隐藏（bVisible=false，生成实例实测验证）。
  - 手柄 StaticMesh 碰撞预设改为 NoCollision（解决 SpawnActor failed at spawn location 导致 VRPawn 无法生成、手柄/输入全失效的根因）。
  - 真机验证（2026-08-13，新 APK 9:46）：手柄单独显示、无手部重叠、操作可用；日志无 SpawnActor 失败。
- 编辑器自动化工具链（TD-010）：安装 UEBridgeMCP（UE5.6 原生兼容，HTTP 8080，407 工具）；UnrealMCP 因 5.6 编译失败移除（备份在临时目录）。GPL-3.0 许可证上架前需评估。
- 遗留（TD-011）：PICO Neo3 真机运行时卡顿，待 T006 性能门禁定位优化。
- 任务状态：M00-T004 → awaiting_review（根 STATUS.json、07-task-register、TD-007 resolved 同步）。

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
