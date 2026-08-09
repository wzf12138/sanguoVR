# 验证登记

记录 M00 基线期各项验证的层级、状态与证据。未执行或待执行的验证必须保持标注，不得包装成通过；真机证据不得以桌面或静态检查替代。

| ID | 验证 | 关联任务 | 层级 | 状态 | 证据 |
|---|---|---|---|---|---|
| V-001 | 治理、规则、VR、系统、登记册与任务文件物理存在与可读；`.trae` 恢复清单逐份读取 | M00-T001 | 文件 | 已验证 | 文件工具逐份读取；`M00-T001.md` 至 `M00-T006.md` 报告 |
| V-002 | Git 安装、仓库初始化、LFS 配置与远程推送 | M00-T002 | 文件 | 已验证（2026-08-09 用户确认） | `.gitignore`、`.gitattributes`、`.lfsconfig`；`../standards/10-git-standard.md`；Git for Windows + Git LFS 已安装，`origin/master` 已推送远程 |
| V-003 | UE5.8 工程文件生成与 Editor 编译 | M00-T003 | 构建 | 已验证（编译成功） | `Rebuild.bat VRSanguoYanWuchangEditor Win64 Development` Result: Succeeded（33.35s，10 动作）；UBT 自动生成 makefile；MCP `list_toolsets` 连通、`LogLoad` 无错误 |
| V-004 | OpenXR 编辑器启动与 VR 能力 | M00-T004 | 编辑器 | 已验证（编辑器） | `xrCreateInstance succeeded`（SteamVR/OpenXR 2.14.5）；插件运行中全部启用；VR 模板资产核对通过（详见 `../vr/PicoValidationMatrix.md`） |
| V-005 | PICO Neo3 安装、启动、输入与断网 | M00-T004 | 真机 | 验证失败（xrCreateSession 拒绝，引擎/运行时组合不兼容） | APK 构建安装成功；经三轮配置修复（Swappy 禁用/多视图关闭/OpenXR 启用）后，OpenXR 运行时加载成功（Pico XRT 3.0.1）但 `xrCreateSession` 返回 `XR_ERROR_INITIALIZATION_FAILED`，应用停在 LOADING；UE5.8 与 Neo3 系统 OpenXR 运行时不兼容，非配置可解；待用户决策换设备或降级引擎（详见 `../knowledge/TechnicalDecisions.md`） |
| V-006 | 系统骨架自动化测试 | M00-T005/T006 | 自动化 | 待验证 | Automation 报告 |
| V-007 | NTFS ACL 应用与恢复 | M00-T001 | 系统权限 | 待用户管理员执行 | 管理脚本输出 |

## 旧编号映射

| 旧编号 | 来源文件 | 处置 |
|---|---|---|
| V-001、V-002 | `verification-register.md` | 并入 V-001、V-002 |
| V-001—V-007 | `VerificationRegister.md` | 并入 V-001—V-007 |

任何验证状态变化须附证据并同步 `.trae/CHANGELOG.md` 与本表。
