# 权限登记

记录 `.trae` 与项目根的 NTFS ACL 目标策略与物理应用状态。ACL 由项目外管理员脚本管理，代理不尝试绕过 ACL；物理权限未应用时明确标注待用户以管理员身份运行。

| 范围 | 目标策略 | 当前状态 | 应用方式 |
|---|---|---|---|
| 项目根 | 当前用户与 SYSTEM/Administrators 可维护 | 待检查 | 管理员脚本 `-Mode Audit` |
| `.trae` | 当前用户读写；SYSTEM/Administrators 完全控制；移除普通 Users 写权限 | 脚本已规划，待物理应用 | `Set-TraeGovernanceAcl.ps1 -Mode Apply` |
| 项目外管理员目录 | 仅管理员维护，避免项目内代理误改 | 待物理应用 | 同一脚本应用管理员目录 ACL |
| 恢复 | 恢复继承并移除显式治理 ACL | 可用脚本设计 | `Set-TraeGovernanceAcl.ps1 -Mode Restore` |

权限脚本位于 `D:/AWork/TraeAdmin/VRSanguoYanWuchang/`，不纳入项目 Git。物理应用结果由用户管理员执行后登记回本表。
