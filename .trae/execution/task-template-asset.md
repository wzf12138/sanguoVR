# 资产任务模板

> 适用于：模型、骨骼、动画、材质、纹理、音效、特效、UI 等 UE Content 资产的生产任务。
> 不适用于：C++ 代码、Blueprint 逻辑、系统架构等代码任务（使用 `task-template.md`）。

## 1. 任务标识

- 任务编号：`MXX-TNNN`
- 资产类型：（SkeletalMesh / StaticMesh / Animation / Material / Texture / Audio / Niagara / Widget / DataAsset）
- 关联里程碑：
- 前置依赖任务：
- 后置依赖任务：

## 2. 资产规格

- 资产名称与路径：（如 `Content/VRSanguo/Weapons/SK_Sword.uasset`）
- 参考来源：（参考图、概念设计、风格指南路径）
- 技术规格：
  - 三角面数预算：
  - 材质数量上限：
  - 贴图尺寸上限：
  - 骨骼数量上限：（骨骼网格）
  - LOD 数量：
  - 碰撞体要求：
- 命名规范：参照 `knowledge/AssetConvention.md`

## 3. 验收标准

- [ ] 资产位于 `Content/VRSanguo/` 指定路径下
- [ ] 命名符合 `AssetConvention.md` 前缀规范
- [ ] 视觉风格符合对应 Production 规格文档
- [ ] 技术规格在预算范围内
- [ ] 在 UE 编辑器 Content Browser 中可正常预览
- [ ] 关联资产引用完整，无缺失依赖
- [ ] 第三方资产已登记来源、版本与许可（如有）

## 4. 白名单路径

```
# 资产产出路径（相对于项目根目录 VRSanguoYanWuchang/）
Content/VRSanguo/...
.trae/execution/reports/tasks/MXX-TNNN.md
.trae/registers/10-asset-register.md
.trae/CHANGELOG.md
```

## 5. 禁止路径

- Source/（代码资产任务不写代码）
- Config/（不修改项目配置）
- Plugins/（不安装或修改插件）
- .trae/governance/（锁定文件）
- .trae/rules/（锁定文件）
- .trae/skills/（锁定文件）

## 6. 验证方法

- [ ] UE 编辑器：打开 Content Browser，导航到资产路径，确认资产存在且可预览
- [ ] 静态检查：命名、路径、引用完整性
- [ ] 性能检查：三角面数、材质数、贴图尺寸在预算内
- [ ] 视觉检查：与参考图/风格指南对比，确认风格一致
- [ ] 第三方资产：来源、版本、许可已登记

## 7. 停止条件

- 依赖资产未就绪
- 参考来源或风格指南缺失
- 资产路径与另一 `in_progress` 任务白名单冲突
- 技术规格超出预算且未获批准

## 8. 报告路径

`.trae/execution/reports/tasks/MXX-TNNN.md`

## 9. 用户确认流程

1. 执行模型完成任务后，报告写入指定路径，状态设为 `awaiting_review`
2. 报告必须包含：资产路径、创建内容描述、UE 中查看方式
3. 用户打开 UE 编辑器，在 Content Browser 中导航到资产路径，进行视觉确认
4. 用户确认后，任务状态更新为 `approved`，资产登记册同步更新