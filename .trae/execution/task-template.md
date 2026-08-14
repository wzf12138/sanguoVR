# 代码任务模板

> 适用于：C++ 类、组件、接口、系统骨架、Blueprint 基类、配置逻辑等代码任务。
> 不适用于：模型/动画/材质等 UE Content 资产（使用 `task-template-asset.md`）；关卡设计（使用 `task-template-level.md`）。

## 0. 认领协议（在任何文件修改之前完成）

执行方在开始实施前必须认领任务：
1. 读取根 `.trae/execution/active/STATUS.json`，确认目标任务 `status` 为 `ready`
2. 检查五件套完整、无白名单冲突
3. 更新根 STATUS.json：`status` -> `in_progress`，`claimedBy` 填写会话标识
4. 同步更新任务目录 STATUS.json
5. 重新读取根 STATUS.json 确认更新成功

未完成认领不得修改任何文件。用户执行任务由 AI 监督模型代为更新。

## 1. 任务标识

- 任务编号：`MXX-TNNN`
- 任务类型：（C++ 类 / 组件 / 接口 / 系统骨架 / 配置 / 其他）
- 关联里程碑：
- 前置依赖任务：
- 后置依赖任务：

## 2. 任务目标

- 目标描述：
- 关联系统指引：（如 `systems/03-combat-resolution-system.md`）
- 关联接口契约：（引用系统指引中的接口契约段落）
- 关联标准：（如 `standards/03-blueprint-cpp-boundary-standard.md`）

## 3. 验收标准

- [ ] 代码位于 `Source/` 指定路径下，命名符合 `standards/02-naming-and-path-standard.md`
- [ ] C++/蓝图边界符合 `standards/03-blueprint-cpp-boundary-standard.md`（规则层在 C++，表现层在蓝图）
- [ ] 接口签名与 `systems/` 工程指引中的接口契约一致
- [ ] DataAsset 使用符合 `standards/04-data-asset-standard.md`（参数从 DataAsset 读取，不硬编码）
- [ ] 编译通过（Development 配置）
- [ ] 无编译警告（或警告已记录原因）
- [ ] 调试数据暴露为只读（如适用）

## 4. 白名单路径

```
# 代码产出路径（相对于项目根目录 VRSanguoYanWuchang/）
Source/VRSanguo/...
.trae/execution/reports/tasks/MXX-TNNN.md
.trae/CHANGELOG.md
```

## 5. 禁止路径

- Config/（不修改项目配置，除非任务明确要求）
- Plugins/（不安装或修改插件）
- Content/（代码任务不产出 Content 资产，除非任务明确要求）
- .trae/governance/（锁定文件）
- .trae/rules/（锁定文件）
- .trae/skills/（锁定文件）

## 6. 验证方法

- [ ] 编译检查：`Rebuild.bat` 或 IDE 编译通过，无错误
- [ ] 代码回读：逐份回读交付文件，确认标题、类名、接口签名正确
- [ ] 接口一致性：对照 systems/ 指引接口契约，确认签名和语义一致
- [ ] 边界检查：确认规则层在 C++、表现层在蓝图，无反模式
- [ ] 编辑器加载：UE 编辑器可正常加载，无模块加载错误（如适用）

## 7. 停止条件

- 编译失败且重试次数用尽
- 发现接口契约与任务假设冲突
- 依赖的系统中指引或标准缺失
- 需要修改白名单外文件
- 与另一 `in_progress` 任务产生文件冲突

## 8. 报告路径

`.trae/execution/reports/tasks/MXX-TNNN.md`

## 报告要求

任务报告必须包含以下内容，禁止无证据总结：

- 结果：实际完成的工作，与任务步骤一一对应。
- 验证状态：区分 `已验证` / `已实现未验证` / `验证失败`，不得把未执行或未通过的内容写成通过。
- 证据：引用验证登记册（`registers/09-verification-register.md` 对应 V-ID）与知识库证据文件路径；真机验证须附设备与结果描述，不得以静态检查替代。
- 偏差：与任务规划不一致处、未完成项、阻塞原因与恢复条件。
- 变更：任务执行期间修改的文件清单；白名单外修改必须注明原因。

## 9. 用户确认流程

1. 执行模型完成任务后，报告写入指定路径，状态设为 `awaiting_review`
2. 报告必须包含：修改文件清单、编译结果、接口一致性确认
3. 用户或授权审核人审核代码回读和编译证据
4. 用户确认后，任务状态更新为 `approved`
