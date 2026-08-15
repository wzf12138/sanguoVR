# M00-T006 检查

## 始终禁止
- 修改治理锁定文件、Skill、总纲或 Design 产品详规
- 修改白名单外文件
- 修改 T004/T005 白名单内的文件
- 创建第二 Skill 或平行知识库
- 执行 Git 命令
- 把未执行的验证写成通过
- 实现 M01 范围的战斗测试（命中去重、格挡等）

## 执行前
- **认领任务**：更新根 STATUS.json 为 `in_progress` 并填写 `claimedBy`，同步任务目录 STATUS.json。未认领不得修改任何文件。
- 任务状态以 `active/M00-T006/STATUS.json` 为准
- 确认 T005 已完成（至少 Step 1-5 编译通过）
- 确认与 `in_progress` 任务无白名单冲突
- 确认 UE 5.6 编辑器可正常打开项目

## 执行后
- Step 1-6 依次完成
- Win64 Editor 构建通过
- Android Development 构建通过
- 8 个日志分类在 PIE 中可见
- DataAsset 校验测试全部通过（Automation Test 面板）
- 接口与流程状态机测试全部通过
- 性能采样基线配置可用（stat 命令）
- 测试场景规划表初版完整（写入任务报告 `M00-T006.md` 作为章节；终版需 M01 战斗场景产出后更新）
- 任务报告写入 `.trae/execution/reports/tasks/M00-T006.md`
- V-006 验证登记更新为已验证
- `active/M00-T006/STATUS.json` 更新为 `awaiting_review`

### M01 接管项（T006 范围外，不阻塞 T006 审核）

| 接管项 | 原因 | 接管方 |
|--------|------|--------|
| 测试场景规划表终版（含 M01 战斗场景具体配置） | M00 阶段 M01 关卡/武器/战斗逻辑未产出，规划表只能覆盖 M00 可验证项 | M01 首次战斗测试后更新 |

## 阻塞处理
- 编译失败：检查 UE5.6 Automation Test API 兼容性
- T005 接口签名偏差：停止并报告，与 T005 产出对照
- Android 构建失败：先完成 Win64 门禁，Android 门禁单独排查
