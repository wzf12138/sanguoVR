# M00-T001 治理与事实源基线

- 状态：已实现未验证
- 优先级：P0
- 目标：建立唯一事实源、变更控制、完成定义、任务流程、登记册和项目规则。

## 输入

`.trae/README.md`、`rules/project_rules.md`、`knowledge/GameMasterPlan.md`、已批准治理方案。

## 交付

- `.trae/governance/`
- `.trae/execution/active/` 与 `.trae/execution/M00/`
- `.trae/standards/`
- `.trae/rules/project_rules.md`
- `.trae/registers/`
- 项目外 NTFS 管理脚本

## 验收

1. 所有索引与正文可由文件工具读取。
2. 权威链和状态词唯一明确。
3. 管理员脚本支持 `Audit`、`Apply`、`Restore`。
4. ACL 未实际应用时明确记录“待用户管理员执行”。

## 回滚

删除新增治理目录并恢复修改前索引；ACL 使用管理员脚本 `-Mode Restore`。
