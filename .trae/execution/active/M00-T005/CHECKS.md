# M00-T005 检查

## 始终禁止
- 修改治理锁定文件、Skill、总纲或 Design 产品详规
- 修改白名单外文件
- 修改 T004 白名单内的文件（Source/** 等，防止并发冲突）
- 创建第二 Skill 或平行知识库
- 执行 Git 命令
- 把未执行的验证写成通过
- 在 M01 之前创建接口的具体实现类
- 使用 VRS 前缀命名新文件（使用 VR 前缀）

## 执行前
- **认领任务**：更新根 STATUS.json 为 `in_progress` 并填写 `claimedBy`，同步任务目录 STATUS.json。未认领不得修改任何文件。
- 任务状态以 `active/M00-T005/STATUS.json` 为唯一权威
- 确认与 `in_progress` 任务无白名单冲突
- 确认 UE 5.6 编辑器可正常打开项目
- 确认 `Source/VRSanguoYanWuchang/` 目录结构存在
- 逐份对照 systems/01-07 接口契约，确认接口签名一致

## 执行后
- Step 1-6 依次完成，每步编译通过后再进入下一步
- 七项接口编译通过，头文件可被外部引用
- 8 个日志分类可用，`UE_LOG` 不报错
- 八个 Data Asset 基类可在编辑器中创建蓝图子类，SchemaVersion 字段存在
- 流程状态机合法迁移与幂等重置通过（RequestPhaseTransition / StartMatch / EndMatch / ResetMatch）
- 玩家 VRPawn 挂载 `VRCharacterCapabilityComponent`
- 不删除任何模板 VR 交互（手部、抓取、瞬移仍可用）
- 空场景可生成玩家占位 + TestDummy + 重置
- 接口签名与 systems/01-07 接口契约一致
- 任务报告写入 `.trae/execution/reports/tasks/M00-T005.md`
- `active/M00-T005/STATUS.json` 更新为 `awaiting_review`

## 阻塞处理
- 编译失败：检查 UE 5.6 API 兼容性，记录错误日志
- 模板 Pawn 子类化后抓取/瞬移失效：回退子类化，仅添加组件
- Data Asset 字段过多导致编辑器卡顿：只保留最小字段集
- 接口签名冲突：停止并报告，按权威链消解
