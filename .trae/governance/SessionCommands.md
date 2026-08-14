# 新会话短指令

新会话工作目录必须选择 `VRSanguoYanWuchang` 项目根目录。

## 决策

### `决策下一步`

读取完整项目状态，审核当前阶段，生成活动任务；只生成任务，不执行。

### `规划这个细节：<主题>`

以决策模型身份设计指定细节。若会改变锁定规则，生成变更申请；若可作为原子任务，生成任务草案。

### `检查项目状态`

只读检查治理、任务、风险、工程和验证状态，不修改文件；同时核对 `integrity.yaml` 与实际文件一致性（新增文件、重复命名、断链、索引与登记册同步），不一致时列为异常报告。

### `登记风险：<内容>`

评估并更新风险登记；不得借此修改产品方向。

### `登记技术债：<内容>`

评估并在 [`../registers/11-tech-debt-register.md`](../registers/11-tech-debt-register.md) 中登记技术债（临时实现、占位方案、已知缺陷）；标注影响、偿还计划和优先级；不得借此修改产品方向或降低验收标准。

## 执行

### `执行当前任务`

先认领任务（更新根 STATUS.json 为 `in_progress` 并填写 `claimedBy`），然后仅在状态为 `in_progress` 且白名单非空时执行。最多提交到 `awaiting_review`。

### `继续执行当前任务`

仅用于状态已为 `in_progress`（已认领）且未触发停止条件的任务。

### `恢复阻塞任务`

进入决策模式核验阻塞是否解除；执行模型不能自行恢复。

## 审核

### `审核当前任务`

对照任务、白名单、实际修改和证据进行审核；只输出 `approved`、`requires_changes`、`blocked` 或 `rejected`。

### `验收当前里程碑`

审核里程碑全部任务和门禁，不实施新功能。

## 变更

### `申请修改：<内容>`

创建变更申请，不直接修改锁定文件。

### `只读分析：<问题>`

只读回答，不创建任务、不改工程。

## 推送

### `推送` / `上传git` / `git push`

> **硬性门禁**：推送前必须完成以下全部检查，任一未通过则不得推送。

**推送前必检清单**：

1. **运行一致性校验**：执行 `python dashboard/check-integrity.py`，确认全部通过（技术债 open 数 >3 的警告可豁免，但需在提交信息中注明）。
2. **同步 integrity.yaml**：确认 `updated` 日期为当天，`active_tasks` 列表与根 `STATUS.json` 一致，`limitations` 反映最新验证状态。
3. **同步 manifest.yaml**：确认 `updated` 日期为当天，`active_gate.task_packages` 与根 `STATUS.json` 一致。
4. **同步登记册**：`07-task-register.md` 中各任务状态与根 `STATUS.json` 一致。
5. **生成看板**：执行 `python dashboard/generate-static.py`，确认 `status.json`/`integrity.json`/`index.html` 已更新。
6. **CHANGELOG 完整**：本次会话所有变更已记录在 `.trae/CHANGELOG.md`。

**执行流程**：

```
1. check-integrity.py         → 校验通过
2. 逐项核对 integrity/manifest/登记册/CHANGELOG
3. generate-static.py          → 看板生成
4. git add -A
5. git commit -m '<描述>'
6. git push origin master
```

**禁止**：跳过校验直接推送；校验未通过仍推送；推送后不确认远程同步成功。

## 安全默认

用户意图无法明确归类时，自动使用“只读分析”。不得猜测进入执行模式。
