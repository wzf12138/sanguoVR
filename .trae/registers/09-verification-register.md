# 验证登记

记录 M00 基线期各项验证的层级、状态与证据。未执行或待执行的验证必须保持标注，不得包装成通过；真机证据不得以桌面或静态检查替代。

| ID | 验证 | 关联任务 | 层级 | 状态 | 证据 |
|---|---|---|---|---|---|
| V-001 | 治理、规则、VR、系统、登记册与任务文件物理存在与可读；`.trae` 恢复清单逐份读取 | M00-T001 | 文件 | 已确认 | 文件工具逐份读取：治理契约、操作模型、规则、标准、VR、系统、Design 详规、登记册、里程碑任务详规及 active 任务包；报告索引见 `execution/reports/tasks/README.md` |
| V-002 | Git 安装、仓库初始化、LFS 配置与远程推送 | M00-T002 | 文件 | 已验证（2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.lfsconfig`；`../standards/10-git-standard.md`；Git for Windows + Git LFS 已安装，`origin/master` 已推送远程 |
| V-003 | UE5.8 工程文件生成与 Editor 编译 | M00-T003 | 构建 | 已验证（编译成功） | `Rebuild.bat VRSanguoYanWuchangEditor Win64 Development` Result: Succeeded（33.35s，10 动作）；UBT 自动生成 makefile；MCP `list_toolsets` 连通、`LogLoad` 无错误 |
| V-004 | OpenXR 编辑器启动与 VR 能力 | M00-T004 | 编辑器 | 部分验证（编辑器阶段已完成，真机未完成） | `xrCreateInstance succeeded`（SteamVR/OpenXR 2.14.5）；插件运行中全部启用；VR 模板资产核对通过（详见 `../vr/PicoValidationMatrix.md`） |
| V-005 | PICO Neo3 安装、启动、输入与断网（UE5.8 路线） | M00-T004 | 真机 | 验证失败（xrCreateSession 拒绝，引擎/运行时组合不兼容） | APK 构建安装成功；经三轮配置修复（Swappy 禁用/多视图关闭/OpenXR 启用）后，OpenXR 运行时加载成功（Pico XRT 3.0.1）但 `xrCreateSession` 返回 `XR_ERROR_INITIALIZATION_FAILED`，应用停在 LOADING；UE5.8 与 Neo3 系统 OpenXR 运行时不兼容，非配置可解；已决策降级 UE5.6（详见 `../knowledge/TechnicalDecisions.md`） |
| V-008 | UE5.6 + PICO OpenXR Plugin（OS 5）真机：swapchain、场景渲染、输入与手柄模型 | M00-T004 | 真机 | 已验证（2026-08-13） | UE5.6 项目重建 + PICO 插件（v1.6.1）迁移至项目 `Plugins/`；swapchain 补丁（`PICO_HMD.cpp` 拦截 `xrCreateSwapchain` 剥离 format list）符号已确认编译进 libUnreal.so（`PICOLayerCreateSwapchain` 等 3 符号）；Neo3 真机场景可见、无 swapchain 崩溃；2026-08-12 输入映射按 PICO 官方文档绑定 5 个 IMC（二进制核验）；2026-08-13 手柄模型挂载（`SM_PICONeo3_L/R` + 隐藏骨骼手部，实例实测 bVisible=False）+ 碰撞修复（NoCollision，解决 SpawnActor 失败），真机确认手柄显示、输入生效；遗留：Neo3 卡顿性能优化（TD-011） |
| V-006 | 系统骨架自动化测试 | M00-T005/T006 | 自动化 | 待验证 | Automation 报告 |
| V-007 | NTFS ACL 应用与恢复 | M00-T001 | 系统权限 | 待用户管理员执行 | 管理脚本输出 |

## 旧编号映射

| 旧编号 | 来源文件 | 处置 |
|---|---|---|
| V-001、V-002 | `verification-register.md` | 并入 V-001、V-002 |
| V-001—V-007 | `VerificationRegister.md` | 并入 V-001—V-007 |

任何验证状态变化须附证据并同步 `.trae/CHANGELOG.md` 与本表。
