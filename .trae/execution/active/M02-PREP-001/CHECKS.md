# M02-PREP-001 检查

## 始终禁止
- 修改 Source/、Config/、Plugins/
- 修改治理锁定文件、Skill、总纲或 Design 产品详规
- 创建 C++ 代码或 Blueprint 逻辑
- 直接使用版权不明的素材作为最终内容

## 执行前
- **认领任务**：AI 监督模型代为更新根 STATUS.json 为 `in_progress`（`claimedBy` 填写 `user-{YYYYMMDD}-{序号}`），同步任务目录 STATUS.json。未认领不得开始交互。
- 确认任务状态以 `active/M02-PREP-001/STATUS.json` 为准
- 读取 `ArtStyleGuide.md` 和 `AnimationSpec.md` 了解视觉和动画规格
- 读取 `WeaponsAndInteraction.md` 了解五武器分类

## 执行后（AI 监督模型检查）
- 平台选型：至少覆盖 3 个平台，含成本/周期/质量对比
- 参考图片：覆盖五武器、五兵种、场景建筑、武将，命名规范（`REF_Category_Name_XX.jpg`）
- 骨架规格：含骨骼列表、Socket 定义、UE5.6 兼容性说明、平台选择
- 武器规格：5 类武器各有面数预算、尺寸、Socket、特殊要求
- 动画清单：覆盖待机/移动/五武器攻击/受击/死亡/IK 标定，含来源选项
- 参考图片已导入 `Content/VRSanguo/Art/References/` 且可在编辑器中预览
- 任务报告写入 `.trae/execution/reports/tasks/M02-PREP-001.md`
- `STATUS.json` 更新为 `awaiting_review`

## 阻塞处理
- 平台均不满足需求：报告问题，考虑自建或外包
- 骨架兼容性问题：与 AI 监督模型讨论替代方案
- 参考资料不足：扩大搜索范围至学术资源或博物馆藏品
