# VRSanguoYanWuchang 项目规则

## 必读

开始任何任务前依次读取：

1. `.trae/README.md`
2. `.trae/governance/policy.md`
3. `.trae/knowledge/GameMasterPlan.md`
4. 当前任务文件与相关系统/规范正文

## 文件边界

- UE 工程：`Config/`、`Content/`、`Plugins/`、`Source/`。
- 治理与 AI 资料：仅 `.trae/`。
- 临时脚本、下载和调试输出：不得进入项目。
- NTFS 管理脚本：仅项目外 `D:/AWork/TraeAdmin/VRSanguoYanWuchang/`。

## 执行规则

- **认领门禁（最高优先级）**：执行模型或用户在任何文件修改之前，必须先将根 `.trae/execution/active/STATUS.json` 中对应任务状态更新为 `in_progress` 并填写 `claimedBy`（格式 `session-{YYYYMMDD}-{序号}`）。未认领不得开始实施。用户执行任务同样适用（由 AI 监督模型代为更新或提示用户）。认领流程详见 `governance/ExecutionModel.md`。
- 不询问已在批准方案中明确的事项；直接实施并验证。
- 修改已有文件前必须先读取，采用最小差异。
- 不把规划描述为实现，不把桌面验证描述为 PICO 真机验证。
- 不建立平行知识库、重复 Skill 或重复规则正文。
- 创建或修改 `.trae/` 内文件前，必须确认路径属于（a）active 白名单内、（b）当前任务报告/登记册路径、或（c）用户本次明确批准的变更；三者皆不是则不得创建。白名单为空的决策/规划期同样适用，规划输出只写入任务草案或变更申请，不直接落盘受控目录。
- 任务必须关联 `MNN-TNNN`；决策、风险和证据同步登记册。
- 未通过编译/编辑器/真机验证的项标记“已实现未验证”或“待验证”。
- 禁止提交密钥、本机路径凭据、UE 生成目录和大型非 LFS 二进制。

## 权限规则

`.trae` 治理资料建议通过项目外管理员脚本设置 NTFS 保护。代理不得尝试绕过 ACL；物理权限未应用时，必须明确说明脚本已交付、需用户以管理员身份运行。
