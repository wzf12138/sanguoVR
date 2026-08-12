# 关卡任务模板

> 适用于：关卡/地图搭建、灰盒布局、场景美术、光照、导航网格、性能调优等关卡相关任务。
> 关卡任务同时涉及资产（Content/）和配置（关卡内放置），可能同时修改 Content/ 和关卡文件。

## 1. 任务标识

- 任务编号：`MXX-TNNN`
- 关卡类型：（灰盒 / 正式竞技场 / 训练场 / 菜单场景）
- 关联里程碑：
- 前置依赖任务：
- 后置依赖任务：

## 2. 关卡规格

- 关卡名称与路径：（如 `Content/VRSanguo/Maps/L_PrototypeArena.umap`）
- 参考来源：（布局草图、参考图、竞技场设计规范路径）
- 关卡尺寸：（UE 单位）
- 分区策略：（单关卡 / 子关卡 / World Partition）
- 玩法配置：
  - 出生点数量与位置：
  - 队伍分区：
  - 障碍物/掩体分布：
  - 可交互区域：
  - 禁入区域：
- 技术规格：
  - 静态网格数量上限：
  - 光源数量上限：
  - 动态物体数量上限：
  - 目标帧率：
- 命名规范：参照 `knowledge/AssetConvention.md`、`knowledge/DirectoryConvention.md`

## 3. 验收标准

- [ ] 关卡文件位于 `Content/VRSanguo/Maps/` 指定路径下
- [ ] 关卡内所有资产引用完整，无缺失依赖
- [ ] 导航网格（NavMesh）已生成且覆盖可行走区域
- [ ] 出生点、队伍分区、障碍物位置符合布局规格
- [ ] 在 UE 编辑器中可正常加载和运行
- [ ] 性能指标在预算范围内（帧率、Draw Call、内存）
- [ ] 关卡照明无异常（无全黑/全白区域、无漏光）
- [ ] 碰撞体正确，无穿墙或掉落漏洞

## 4. 白名单路径

```
# 关卡产出路径（相对于项目根目录 VRSanguoYanWuchang/）
Content/VRSanguo/Maps/...
Content/VRSanguo/Arena/...
.trae/execution/reports/tasks/MXX-TNNN.md
.trae/registers/10-asset-register.md
.trae/CHANGELOG.md
```

## 5. 禁止路径

- Source/（不写代码）
- Config/（不修改项目配置）
- Plugins/（不安装或修改插件）
- Content/VRSanguo/Characters/（不修改角色资产）
- Content/VRSanguo/Weapons/（不修改武器资产）
- .trae/governance/（锁定文件）
- .trae/rules/（锁定文件）
- .trae/skills/（锁定文件）

## 6. 验证方法

- [ ] UE 编辑器：打开关卡，确认加载无错误
- [ ] 导航检查：NavMesh 覆盖所有可行走区域
- [ ] 碰撞检查：角色无法穿墙、掉落或卡住
- [ ] 视觉检查：布局、光照、比例符合设计规格
- [ ] 性能检查：在目标设备上帧率达标
- [ ] 玩法检查：出生点可用、队伍分区正确

## 7. 停止条件

- 依赖资产未就绪（如角色、武器模型未完成）
- 布局规格或参考来源缺失
- 关卡路径与另一 `in_progress` 任务白名单冲突
- 性能指标不达标且优化方案未获批准

## 8. 报告路径

`.trae/execution/reports/tasks/MXX-TNNN.md`

## 9. 用户确认流程

1. 执行模型完成任务后，报告写入指定路径，状态设为 `awaiting_review`
2. 报告必须包含：关卡路径、关卡内容描述、UE 中查看方式、性能数据
3. 用户打开 UE 编辑器，加载关卡，进行以下确认：
   - 视觉：布局、光照、比例是否符合预期
   - 功能：出生点、移动、碰撞是否正常
   - 性能：帧率是否达标
4. 用户确认后，任务状态更新为 `approved`，资产登记册同步更新