# M01-T005 检查

## 始终禁止
- 修改 Source/、Config/、Plugins/
- 修改治理锁定文件、Skill、总纲或 Design 产品详规
- 修改 VR 模板资产
- 创建 C++ 代码或 Blueprint 逻辑
- 导入外部模型（纯灰盒）
- 修改 T004/T005/T006 白名单内文件

## 执行前
- **认领任务**：更新根 STATUS.json 为 `in_progress` 并填写 `claimedBy`，同步任务目录 STATUS.json。未认领不得修改任何文件。
- 任务状态以 `active/M01-T005/STATUS.json` 为准
- 确认 `Content/LevelPrototyping/` 素材存在
- 确认与 `in_progress` 任务无白名单冲突

## 执行后
- 关卡可在编辑器中打开
- 地面 20x20m，围墙 4m 高
- 出生点对称，掩体和高台就位
- NavMesh 覆盖全部可行走区域，高台可达
- PIE 运行 >= 90fps
- 灰盒材质正确
- 任务报告写入 `.trae/execution/reports/tasks/M01-T005.md`
- 资产登记册同步更新
- `active/M01-T005/STATUS.json` 更新为 `awaiting_review`

## 阻塞处理
- LevelPrototyping 素材缺失：检查模板资产完整性
- NavMesh 异常：简化几何体，检查碰撞设置
- 性能不达标：减少静态网格数量，简化光照
