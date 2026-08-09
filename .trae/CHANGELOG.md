# ChangeLog

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
