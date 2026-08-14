# M00-T006 自动化、诊断与交付门禁

- 任务编号：M00-T006
- 状态：见 `STATUS.json`
- 里程碑：M00
- 优先级：P1
- 前置任务：M00-T005（系统骨架，Step 2-4 依赖其接口与 DA 基类）
- 预估耗时：~5.5h

## 目标

为 T005 产出建立自动化测试、构建门禁和性能采样基线。原 T006 标记"已批准"但交付物从未实现，本次修订纠正状态并扩充为可执行步骤。

## 实施步骤

详细步骤见 `.trae/execution/M00/T006-AutomationDiagnosticsGates.md`。

| Step | 内容 | 预估 | T005 依赖 |
|------|------|------|-----------|
| 1 | 构建门禁验证（Win64 + Android） | 0.5h | 无（可并行） |
| 2 | 8 个日志分类运行时验证 | 0.5h | 依赖 T005 Step 1 |
| 3 | DataAsset 校验自动化测试 | 1.5h | 依赖 T005 Step 3 |
| 4 | 接口与流程状态机自动化测试 | 2h | 依赖 T005 Step 2/4/5 |
| 5 | 性能采样基线配置 | 0.5h | 部分依赖 |
| 6 | 测试场景规划表 | 0.5h | 无 |

## 停止条件

- 编译失败且无法在 3 次重试内修复
- T005 产出存在接口签名偏差导致测试无法编写
- Android 构建环境异常

## 回退

- 删除 `Source/VRSanguoYanWuchang/Public/Tests/` 和 `Private/Tests/` 下新增文件
- 还原 Build.cs 中可能新增的 Automation 模块依赖

## 报告路径

`.trae/execution/reports/tasks/M00-T006.md`
