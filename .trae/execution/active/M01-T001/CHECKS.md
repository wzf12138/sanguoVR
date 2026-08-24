# M01-T001 检查

## 始终禁止
- 修改治理锁定文件、Skill、总纲或 Design 产品详规
- 修改白名单外文件
- 修改 VRE 插件源码（`Plugins/VRExpansionPlugin/Source/`）
- 修改 T004/T005/T006 白名单内的文件
- 替换现有 VRPawn 为 VRCharacter
- 修改 PICO Neo3 输入映射
- 复制示例项目的素材/模型/材质
- 把未执行的验证写成通过

## 执行前
- **认领任务**：更新根 STATUS.json 为 `in_progress`，同步任务目录 STATUS.json
- 确认 VRE 插件编译通过
- 确认与 `in_progress` 任务无白名单冲突
- 确认 UE 5.6 编辑器可正常打开项目
- 确认 PICO Neo3 输入映射可用

## 执行后

- [ ] `[文件]` BP_WeaponBase 蓝图可创建，继承 `GrippableSkeletalMeshActor`
- [ ] `[文件]` 抓取参数配置完成（GripScriptType、bAllowSecondaryGrip）
- [ ] `[文件]` HandSocket 握持姿势配置完成
- [ ] `[文件]` BP_TestSword 已创建并放置到 L_SkeletonTest 关卡
- [ ] `[PIE]` 编辑器 PIE 验证：可单手抓取武器 [PICO Neo3 + VR Preview]
- [ ] `[PIE]` 编辑器 PIE 验证：可释放武器 [PICO Neo3 + VR Preview]
- [ ] `[PIE]` 编辑器 PIE 验证：双手握持可用（副手靠近时自动吸附） [PICO Neo3 + VR Preview]
- [ ] `[PIE]` 现有 VR 交互不被破坏（手部动画、抓取、瞬移仍可用） [PICO Neo3 + VR Preview]
- [ ] `[文件]` 任务报告写入 `.trae/execution/reports/tasks/M01-T001.md`，包含结构化验证证据表
- [ ] `[文件]` 资产登记册同步更新
- [ ] `[文件]` `active/M01-T001/STATUS.json` 更新为 `awaiting_review`（非 `[PIE]` 项全部通过后）或 `blocked`（`[PIE]` 项待用户验证时）

### M02 接管项（T001 范围外，不阻塞 T001 审核）

| 接管项 | 原因 | 接管方 |
|--------|------|--------|
| 武器自定义模型/材质 | 需三国风格资产，M02 产出 | M02 资产生成 |
| Melee GripScript 近战碰撞配置 | 需要伤害系统（M01-T002）和格挡系统（M01-T003）就位后再配置 | M01-T003 |

## 阻塞处理
- VRE 编译失败：检查 UE5.6 兼容性，回退到备份
- VRPawn 交互被破坏：停止，回退 VRPawn 修改
- PICO 输入冲突：记录冲突项，停止并报告