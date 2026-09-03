# M02-PREP-002 检查单

## 执行后

1. `[日志]` 桥插件编译通过：UBT 全量 Rebuild 真实日志含 `Result: Succeeded`，且包含新桥模块编译条目（TC-01）。
2. `[文件]` `Plugins/` 下存在 db-lyon/ue-mcp 桥插件目录（.uplugin + Source），`VRSanguoYanWuchang.uproject` 已启用对应插件；UEBridgeMCP 已退役（.uproject 移除或目录 .disabled）。
3. `[日志]` 蓝图测试副本验证（TC-02）：add_node → connect_pins → compile → query 读回，读回输出与写入操作一致（编辑器层级验证，非真机）。测试副本置于 Dev 临时路径并在验证后删除。
4. `[日志]` 编辑器重启后无缺失模块错误（TC-03）：LogLoad 无 error 级缺失模块记录；打开 L_SkeletonTest 冒烟正常。
5. `[文件]` TD-010 已更新（迁移决策+结果+GPL 插件退役记录）；07 任务登记册、根 STATUS.json、CHANGELOG、integrity/manifest 同步；任务报告 `execution/reports/tasks/M02-PREP-002.md` 完成。
6. `[截图]` 编辑器中测试蓝图读回结果截图（图节点与连线可见）。

## 证据类型标注

- 全部检查项为 AI 可执行；无 [PIE] 用户操作项（编辑器级验证由执行模型完成，标注编辑器层级）。
